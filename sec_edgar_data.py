"""
Primary data source for income statement, balance sheet, and cash flow data:
fetches directly from SEC EDGAR's XBRL "company facts" API instead of Yahoo
Finance, since Yahoo is often several weeks stale after an earnings release.
SEC EDGAR reflects numbers as soon as the company's 10-Q/10-K is filed and
XBRL-tagged, typically within a day or two of the press release.

yahoo_finance_data.py remains the source for price history and quick_metrics
(market cap, P/E, dividend yield, beta, analyst targets — quote/market data
that has no SEC EDGAR equivalent). This script covers everything else:
income statement, balance sheet, and cash flow statement.

Output JSON uses the same file paths and Yahoo-style line-item names
(e.g. "Total Revenue", "Operating Income") as the old yahoo_finance_data.py
statement fetchers, so chart_*.py and key_stock_metrics.py did not need to
change their field lookups.

Usage:
    .venv/Scripts/python sec_edgar_data.py AAPL
"""

import json
import os
import sys
import time
from datetime import date

import requests

# SEC requires a descriptive User-Agent with a contact email on every request,
# or it will reject the request. Replace with your own contact info.
USER_AGENT = "investment-analysis-toolkit johnfang522@yahoo.com"

HEADERS = {"User-Agent": USER_AGENT}

TICKER_CIK_URL = "https://www.sec.gov/files/company_tickers.json"
COMPANY_FACTS_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"

# US-GAAP XBRL tags to pull for each statement, keyed by the Yahoo-style line
# item name that chart_*.py / key_stock_metrics.py already look for. Each tag
# list is a priority-ordered set of fallback tags — companies don't always
# use the exact same tag (e.g. some use "Revenues" instead of
# "RevenueFromContractWithCustomerExcludingAssessedTax") — the first one
# present in the company's facts is used.
INCOME_STATEMENT_TAGS = {
    "Total Revenue": ["RevenueFromContractWithCustomerExcludingAssessedTax", "RevenueFromContractWithCustomerIncludingAssessedTax", "Revenues", "SalesRevenueNet"],
    "Cost Of Revenue": ["CostOfGoodsAndServicesSold", "CostOfRevenue"],
    "Gross Profit": ["GrossProfit"],
    # NOTE: despite the tag name, us-gaap:OperatingExpenses (and its
    # CostsAndExpenses fallback) is typically *total* costs and expenses,
    # i.e. it already includes cost of revenue. Do not treat this as
    # SG&A/R&D-only opex — see _backfill_income_statement below.
    "_TotalCostsAndExpenses": ["OperatingExpenses", "CostsAndExpenses"],
    "Operating Income": ["OperatingIncomeLoss"],
    "Net Income": ["NetIncomeLoss", "ProfitLoss"],
    "Interest Expense": ["InterestExpense", "InterestExpenseOperating", "InterestExpenseNonoperating", "InterestExpenseDebt", "InterestIncomeExpenseNonoperatingNet"],
    "Diluted EPS": ["EarningsPerShareDiluted"],
    "Basic EPS": ["EarningsPerShareBasic"],
}
# XBRL unit override for tags whose natural unit isn't USD.
INCOME_STATEMENT_UNITS = {
    "Diluted EPS": "USD/shares",
    "Basic EPS": "USD/shares",
}

BALANCE_SHEET_TAGS = {
    "Total Assets": ["Assets"],
    "Current Assets": ["AssetsCurrent"],
    "Cash And Cash Equivalents": ["CashAndCashEquivalentsAtCarryingValue"],
    "Total Liabilities": ["Liabilities"],
    "Current Liabilities": ["LiabilitiesCurrent"],
    "Long Term Debt": ["LongTermDebtNoncurrent", "LongTermNotesAndLoans", "LongTermNotesPayable"],
    "_ShortTermDebt": ["DebtCurrent", "LongTermDebtCurrent", "NotesPayableCurrent"],
    "Stockholders Equity": ["StockholdersEquity"],
    # Mezzanine/temporary equity (e.g. redeemable convertible preferred
    # stock) sits on the balance sheet between Liabilities and permanent
    # Stockholders' Equity under US GAAP — Assets = Liabilities +
    # Temporary Equity + Stockholders Equity. Without this, "Stockholders
    # Equity" alone understates total capitalization for any filer carrying
    # such an instrument, and Assets - Liabilities - Stockholders Equity
    # will NOT reconcile to zero (by design, not a bug) until it converts
    # or redeems. Captured for transparency; D/E and other ratios
    # elsewhere intentionally still use only permanent Stockholders Equity.
    "Temporary Equity": ["TemporaryEquityCarryingAmountAttributableToParent", "RedeemableNoncontrollingInterestEquityCarryingAmount"],
}

CASH_FLOW_TAGS = {
    "Operating Cash Flow": ["NetCashProvidedByUsedInOperatingActivities"],
    "Capital Expenditure": ["PaymentsToAcquirePropertyPlantAndEquipment"],
    "Investing Cash Flow": ["NetCashProvidedByUsedInInvestingActivities"],
    "Financing Cash Flow": ["NetCashProvidedByUsedInFinancingActivities"],
    "Cash Dividends Paid": ["PaymentsOfDividends"],
}

# Internal-only keys (leading underscore) used to derive display line items
# but not written to the final output.
_INTERNAL_KEYS = {"_TotalCostsAndExpenses", "_ShortTermDebt"}


def _get(url: str) -> dict:
    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    return resp.json()


def _get_json(url: str) -> dict:
    return _get(url)


def get_cik(ticker: str) -> str:
    """
    Look up a ticker's 10-digit zero-padded CIK via SEC's ticker-to-CIK map.
    """
    ticker = ticker.upper()
    data = _get(TICKER_CIK_URL)
    for entry in data.values():
        if entry["ticker"].upper() == ticker:
            return str(entry["cik_str"]).zfill(10)
    raise ValueError(f"Could not find CIK for ticker {ticker}")


def get_company_facts(cik: str) -> dict:
    """
    Fetch the full XBRL company-facts payload for a given CIK.
    Contains every US-GAAP-tagged fact the company has ever reported.
    """
    return _get(COMPANY_FACTS_URL.format(cik=cik))


def _days_between(start: str, end: str) -> int:
    return (date.fromisoformat(end) - date.fromisoformat(start)).days


def _extract_one_tag(tag_data: dict, unit: str, instant: bool):
    """Extract {end: value} (instant) or {"quarterly":.., "annual":..} (duration) for one XBRL tag."""
    series = tag_data.get("units", {}).get(unit)
    if not series:
        return None

    if instant:
        by_end_date = {}
        for item in series:
            end = item.get("end")
            val = item.get("val")
            filed = item.get("filed", "")
            if end is None or val is None:
                continue
            existing = by_end_date.get(end)
            if existing is None or filed >= existing[1]:
                by_end_date[end] = (val, filed)
        if not by_end_date:
            return None
        return {end: val for end, (val, _filed) in sorted(by_end_date.items())}

    by_period = {}
    for item in series:
        start, end, val = item.get("start"), item.get("end"), item.get("val")
        filed = item.get("filed", "")
        if not start or not end or val is None:
            continue
        key = (start, end)
        existing = by_period.get(key)
        if existing is None or filed >= existing[1]:
            by_period[key] = (val, filed)

    groups = {}
    for (start, end), (val, _filed) in by_period.items():
        groups.setdefault(start, []).append((end, val))

    quarterly, annual = {}, {}
    for start, entries in groups.items():
        entries.sort(key=lambda e: e[0])
        prev_end, prev_val = start, 0
        for end, cumulative_val in entries:
            discrete_val = cumulative_val - prev_val
            if 80 <= _days_between(prev_end, end) <= 100:
                quarterly[end] = discrete_val
            if 350 <= _days_between(start, end) <= 380:
                annual[end] = cumulative_val
            prev_end, prev_val = end, cumulative_val

    if not quarterly and not annual:
        return None
    return {"quarterly": dict(sorted(quarterly.items())), "annual": dict(sorted(annual.items()))}


def _freshest_date(result, instant: bool):
    if instant:
        return max(result.keys(), default=None)
    return max(list(result["quarterly"].keys()) + list(result["annual"].keys()), default=None)


def _extract_tag_series(facts: dict, tags: list[str], unit: str = "USD", instant: bool = False):
    """
    Given a company-facts payload and a list of candidate XBRL tags, return
    period data from whichever tag has the MOST RECENT data — not simply
    the first tag in the list that has any data at all. Filers routinely
    retire a tag mid-history and switch to a successor with no overlap
    (e.g. COHR stopped tagging us-gaap:InterestExpense after FY2024 Q3 and
    switched to us-gaap:InterestExpenseOperating with no announcement) — if
    the retired tag happens to be listed first and has years of old data,
    "first tag with any data" would silently lock onto it and never see the
    current numbers. Ties (same freshest date) break toward the earlier tag
    in `tags`, since list order still encodes which tag name is preferred
    when multiple are equally current.

    Duration facts (income statement / cash flow line items carry both a
    "start" and "end" date) are grouped by their "start" date — every fact
    reported for a given fiscal year (a discrete Q1, a 6-month or 9-month
    year-to-date (YTD) figure, and the full-year 10-K total) shares that
    fiscal year's start date. Sorting each group by end date and taking
    successive differences turns however the filer chose to report interim
    periods (discrete quarters, cumulative YTD, or a mix) into clean
    discrete quarters — this is necessary because:
      - Many fiscal-year filers (e.g. COHR) never tag a discrete Q4 fact at
        all — only the 10-K's full-year total — so Q4 has to be derived as
        FY total minus the 9-month YTD figure.
      - Cash flow statements in particular are very commonly reported as
        cumulative YTD in 10-Qs (a 6-month figure for Q2, a 9-month figure
        for Q3) rather than discrete 3-month figures — naively bucketing by
        each fact's own (end - start) span drops these entirely, since a
        184-day or 273-day span fits neither a "quarterly" nor "annual"
        bucket.
    A discrete period is classified as "quarterly" when its own span
    (this end minus the previous end) is 80-100 days, and the group's
    running total is recorded as "annual" once the cumulative span from the
    group's start reaches 350-380 days (i.e. it's the fiscal year total).
    Returns {"quarterly": {...}, "annual": {...}}.

    Instant facts (balance sheet line items carry only an "end" date, no
    duration) are returned as a single {end_date: value} dict.

    Duplicate (start, end) pairs (e.g. a value re-reported in a later
    filing) keep the most recently filed value.
    """
    us_gaap = facts.get("facts", {}).get("us-gaap", {})
    best_result, best_date, best_coverage = None, None, -1
    for tag in tags:
        tag_data = us_gaap.get(tag)
        if not tag_data:
            continue
        result = _extract_one_tag(tag_data, unit, instant)
        if result is None:
            continue
        freshest = _freshest_date(result, instant)
        # Granularity tiebreak: when two tags are equally fresh (e.g. a
        # filer switches tags mid-year but both still carry the same
        # annual 10-K total), prefer whichever has more quarterly data
        # points rather than silently keeping the first-listed tag, which
        # may carry only the annual figure.
        coverage = 0 if instant else len(result["quarterly"])
        is_better = best_date is None or (freshest and freshest > best_date) or (
            freshest == best_date and coverage > best_coverage
        )
        if is_better:
            best_result, best_date, best_coverage = result, freshest, coverage
    if best_result is not None:
        return best_result
    return {} if instant else {"quarterly": {}, "annual": {}}


STALE_LINE_ITEM_DAYS = 500


def _drop_stale_line_items(items: dict, anchor_key: str, days: int = STALE_LINE_ITEM_DAYS) -> None:
    """
    Mutates `items` ({line_item: {date_str: value}}) in place: any non-anchor
    line item whose most recent date is more than `days` older than the
    anchor line item's most recent date is cleared to {} — i.e. treated as
    unavailable rather than served next to current data for everything else.

    This is the generic fix for a filer that stops tagging a concept
    entirely, with no successor tag anywhere in its filings (e.g. Oracle
    hasn't tagged CostOfRevenue/GrossProfit since FY2018; the mechanism
    applies just the same to any balance sheet or cash flow line item for
    any ticker). It's distinct from the freshness-based tag SELECTION in
    _extract_tag_series, which only helps when a fresher candidate tag
    exists to select — here there may be none. Left unchecked, a chart or
    metric silently mixes years-old data for one line item next to the
    current filing's data for every other line item — e.g. implying a
    small, stale quarter's Gross Profit belongs to the current, much larger
    quarter's Revenue.

    Always check against the statement's own most recently filed measure
    (the anchor) — never a hardcoded date — so this holds for every ticker
    and updates automatically as new quarters are filed.
    """
    anchor_series = items.get(anchor_key)
    if not anchor_series:
        return
    anchor_latest = max(date.fromisoformat(d) for d in anchor_series)
    for line_item, series in items.items():
        if line_item == anchor_key or not series:
            continue
        item_latest = max(date.fromisoformat(d) for d in series)
        if (anchor_latest - item_latest).days > days:
            items[line_item] = {}


def _build_duration_statement(facts: dict, tag_map: dict, unit_overrides: dict = None, anchor_key: str = None) -> dict:
    unit_overrides = unit_overrides or {}
    quarterly, annual = {}, {}
    for line_item, tags in tag_map.items():
        unit = unit_overrides.get(line_item, "USD")
        series = _extract_tag_series(facts, tags, unit=unit, instant=False)
        quarterly[line_item] = series["quarterly"]
        annual[line_item] = series["annual"]

    # Check quarterly against the quarterly anchor and annual against the
    # annual anchor separately (not combined) — a line item could have
    # stale quarterly data but current annual data, or vice versa, and
    # combining them could mask either case.
    if anchor_key:
        _drop_stale_line_items(quarterly, anchor_key)
        _drop_stale_line_items(annual, anchor_key)

    return {"quarterly": quarterly, "annual": annual}


def _build_instant_statement(facts: dict, tag_map: dict, anchor_key: str = None) -> dict:
    statement = {
        line_item: _extract_tag_series(facts, tags, unit="USD", instant=True)
        for line_item, tags in tag_map.items()
    }
    if anchor_key:
        _drop_stale_line_items(statement, anchor_key)
    return statement


def _best_ttm(statement: dict, anchor_key: str) -> dict:
    """
    Choose the freshest available TTM approximation for a duration statement.

    Some filers (e.g. LITE) stop tagging discrete quarterly duration facts
    entirely partway through a fiscal year — only the annual (10-K) fact
    keeps getting filed — so summing "the most recent 4 quarters" silently
    locks onto a stale window while a materially more current annual figure
    sits right there. Compare the most recent date in `anchor_key`'s
    quarterly series against its most recent annual date; if annual is
    newer, use the latest annual period directly as "TTM" (every line item
    that has a value on that exact date) instead of a stale quarterly sum.
    """
    latest_q = max(statement["quarterly"].get(anchor_key, {}).keys(), default=None)
    latest_a = max(statement["annual"].get(anchor_key, {}).keys(), default=None)
    if latest_a and (latest_q is None or latest_a > latest_q):
        return {
            line_item: {"TTM": series[latest_a]}
            for line_item, series in statement["annual"].items()
            if latest_a in series
        }
    return _ttm_from_quarterly(statement["quarterly"], anchor_key)


def _ttm_from_quarterly(quarterly: dict, anchor_key: str) -> dict:
    """
    Sum four quarters for each line item to approximate TTM, matching the
    approach yahoo_finance_data.py used to use.

    All line items use the SAME four end-dates — the most recent four dates
    of `anchor_key`'s own series — rather than each line item picking its
    own "last 4 available dates" independently. Without this, line items
    that got a different fiscal-Q4 gap filled by _backfill_missing_fiscal_q4
    (some filers have enough history to backfill an older gap but not the
    latest one) end up with mismatched 12-month windows, e.g. Revenue TTM
    covering one span while Operating Income TTM covers a different one —
    which silently corrupts any ratio computed between them (margins, etc).
    Line items missing a value on one of the anchor dates are omitted from
    TTM entirely rather than substituting a different date.
    """
    anchor_dates = sorted(quarterly.get(anchor_key, {}).keys(), reverse=True)[:4]
    if len(anchor_dates) < 4:
        return {}
    ttm = {}
    for line_item, series in quarterly.items():
        if all(d in series for d in anchor_dates):
            ttm[line_item] = {"TTM": sum(series[d] for d in anchor_dates)}
    return ttm


def _backfill_income_statement(statement: dict) -> None:
    """
    Fill gaps left by inconsistent/retired XBRL tagging:
      - Gross Profit, where untagged: Total Revenue - Cost Of Revenue
      - Cost Of Revenue, where untagged but Gross Profit IS directly tagged
        (e.g. LITE's us-gaap:CostOfGoodsAndServicesSold tag goes stale
        while it keeps tagging us-gaap:GrossProfit directly): Total Revenue
        - Gross Profit. Only used as a last resort — a directly-tagged
        Gross Profit is authoritative, so back into Cost Of Revenue from it
        rather than leave a mismatched/partial Cost Of Revenue tag (e.g. one
        that excludes D&A) produce a Gross Profit that doesn't reconcile.
      - Operating Income, where untagged (e.g. COHR stopped tagging
        us-gaap:OperatingIncomeLoss after FY2024 with no successor tag):
        Total Revenue - _TotalCostsAndExpenses (which is itself a total
        costs-and-expenses figure that already includes cost of revenue —
        do not also subtract Cost Of Revenue, or COGS gets double-counted)
      - Operating Expense (SG&A/R&D, excluding COGS, for chart display):
        always derived as Gross Profit - Operating Income, which keeps the
        waterfall identity (Revenue - COGS - OpEx = Operating Income) exact
        regardless of which raw tags were available.
    """
    for period in ("quarterly", "annual"):
        revenue = statement[period].get("Total Revenue", {})
        cost = statement[period].setdefault("Cost Of Revenue", {})
        tagged_gross_profit = dict(statement[period].get("Gross Profit", {}))
        total_costs = statement[period].get("_TotalCostsAndExpenses", {})

        for end_date in set(revenue) & set(tagged_gross_profit):
            if end_date not in cost:
                cost[end_date] = revenue[end_date] - tagged_gross_profit[end_date]
        statement[period]["Cost Of Revenue"] = dict(sorted(cost.items()))

        gross_profit = statement[period].setdefault("Gross Profit", {})
        for end_date in set(revenue) & set(cost):
            if end_date not in gross_profit:
                gross_profit[end_date] = revenue[end_date] - cost[end_date]

        op_income = statement[period].setdefault("Operating Income", {})
        for end_date in set(revenue) & set(total_costs):
            if end_date not in op_income:
                op_income[end_date] = revenue[end_date] - total_costs[end_date]

        opex = statement[period].setdefault("Operating Expense", {})
        for end_date in set(gross_profit) & set(op_income):
            opex[end_date] = gross_profit[end_date] - op_income[end_date]

        statement[period]["Gross Profit"] = dict(sorted(gross_profit.items()))
        statement[period]["Operating Income"] = dict(sorted(op_income.items()))
        statement[period]["Operating Expense"] = dict(sorted(opex.items()))

    for period in ("quarterly", "annual"):
        for key in _INTERNAL_KEYS:
            statement[period].pop(key, None)


def _backfill_balance_sheet(statement: dict) -> None:
    """
    Total Debt = Long Term Debt + short-term/current portion of debt.

    Total Liabilities, where untagged (e.g. Oracle doesn't tag an aggregate
    us-gaap:Liabilities figure at all): Total Assets - Stockholders Equity -
    Temporary Equity, an exact accounting identity (Assets = Liabilities +
    Temporary Equity + Stockholders Equity), not an estimate — only used to
    fill dates missing from the direct tag, never to override it.
    """
    lt_debt = statement.get("Long Term Debt", {})
    st_debt = statement.get("_ShortTermDebt", {})
    total_debt = {}
    for end_date in set(lt_debt) | set(st_debt):
        total_debt[end_date] = lt_debt.get(end_date, 0) + st_debt.get(end_date, 0)
    statement["Total Debt"] = dict(sorted(total_debt.items()))
    for key in _INTERNAL_KEYS:
        statement.pop(key, None)

    assets = statement.get("Total Assets", {})
    equity = statement.get("Stockholders Equity", {})
    temp_equity = statement.get("Temporary Equity", {})
    total_liab = statement.setdefault("Total Liabilities", {})
    for end_date in set(assets) & set(equity):
        if end_date not in total_liab:
            total_liab[end_date] = assets[end_date] - equity[end_date] - temp_equity.get(end_date, 0)
    statement["Total Liabilities"] = dict(sorted(total_liab.items()))


def _backfill_cash_flow(statement: dict) -> None:
    """Free Cash Flow = Operating Cash Flow - Capital Expenditure."""
    for period in ("quarterly", "annual"):
        ocf = statement[period].get("Operating Cash Flow", {})
        capex = statement[period].get("Capital Expenditure", {})
        fcf = statement[period].setdefault("Free Cash Flow", {})
        for end_date in set(ocf) & set(capex):
            if end_date not in fcf:
                fcf[end_date] = ocf[end_date] - capex[end_date]
        statement[period]["Free Cash Flow"] = dict(sorted(fcf.items()))


def get_income_statement(facts: dict) -> dict:
    statement = _build_duration_statement(facts, INCOME_STATEMENT_TAGS, INCOME_STATEMENT_UNITS, anchor_key="Total Revenue")
    _backfill_income_statement(statement)
    return statement


def _get_shares_outstanding(facts: dict) -> dict:
    """
    Shares outstanding as stated on the filing's cover page — reported
    under the "dei" (Document and Entity Information) namespace, not
    "us-gaap" like every other tag this module reads, and in "shares" units
    rather than "USD". Used to compute Price/Sales from SEC EDGAR data
    (Market Cap = Price x Shares Outstanding) without needing Yahoo
    Finance's marketCap field.
    """
    dei = facts.get("facts", {}).get("dei", {})
    tag_data = dei.get("EntityCommonStockSharesOutstanding")
    if not tag_data:
        return {}
    return _extract_one_tag(tag_data, unit="shares", instant=True) or {}


def get_balance_sheet(facts: dict) -> dict:
    # Balance sheet items are instant facts (a single as-of date), not spans.
    statement = _build_instant_statement(facts, BALANCE_SHEET_TAGS, anchor_key="Total Assets")
    _backfill_balance_sheet(statement)
    statement["Shares Outstanding"] = _get_shares_outstanding(facts)
    return statement


def get_cash_flow_statement(facts: dict) -> dict:
    statement = _build_duration_statement(facts, CASH_FLOW_TAGS, anchor_key="Operating Cash Flow")
    _backfill_cash_flow(statement)
    return statement


def fetch_edgar_statements(ticker: str) -> dict:
    """
    Fetch income statement, balance sheet, and cash flow data for a ticker
    directly from SEC EDGAR and save each as JSON to Outputs/{TICKER}/,
    using the same file paths yahoo_finance_data.py's statement fetchers
    used to write (so chart_*.py / key_stock_metrics.py need no path changes).

    Output files:
        Outputs/{TICKER}/{ticker_lower}_income_statement_quarterly.json
        Outputs/{TICKER}/{ticker_lower}_income_statement_annual.json
        Outputs/{TICKER}/{ticker_lower}_income_statement_ttm.json
        Outputs/{TICKER}/{ticker_lower}_balance_sheet_quarterly.json
        Outputs/{TICKER}/{ticker_lower}_cash_flow_statement_quarterly.json
        Outputs/{TICKER}/{ticker_lower}_cash_flow_statement_annual.json
        Outputs/{TICKER}/{ticker_lower}_cash_flow_statement_ttm.json

    Raises:
        ValueError: If fewer than four quarters of Total Revenue are
            available to compute TTM (e.g. a recent IPO).
    """
    ticker = ticker.upper()
    print(f"Looking up CIK for {ticker}...")
    cik = get_cik(ticker)

    print(f"Fetching company facts for CIK {cik}...")
    facts = get_company_facts(cik)
    # Be polite to SEC's rate limits (documented max ~10 req/sec) if this is
    # extended to loop over multiple tickers.
    time.sleep(0.2)

    income = get_income_statement(facts)
    cash_flow = get_cash_flow_statement(facts)
    balance_sheet = get_balance_sheet(facts)

    has_quarterly = len(income["quarterly"].get("Total Revenue", {})) >= 4
    has_annual = len(income["annual"].get("Total Revenue", {})) >= 1
    if not has_quarterly and not has_annual:
        raise ValueError("Not enough quarterly data to calculate TTM.")

    income_ttm = _best_ttm(income, anchor_key="Total Revenue")
    cash_flow_ttm = _best_ttm(cash_flow, anchor_key="Operating Cash Flow")

    base_path = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(base_path, "Outputs", ticker)
    os.makedirs(output_path, exist_ok=True)

    files = {
        f"{ticker.lower()}_income_statement_quarterly.json": income["quarterly"],
        f"{ticker.lower()}_income_statement_annual.json": income["annual"],
        f"{ticker.lower()}_income_statement_ttm.json": income_ttm,
        f"{ticker.lower()}_balance_sheet_quarterly.json": balance_sheet,
        f"{ticker.lower()}_cash_flow_statement_quarterly.json": cash_flow["quarterly"],
        f"{ticker.lower()}_cash_flow_statement_annual.json": cash_flow["annual"],
        f"{ticker.lower()}_cash_flow_statement_ttm.json": cash_flow_ttm,
    }
    for filename, data in files.items():
        output_file = os.path.join(output_path, filename)
        with open(output_file, "w") as f:
            json.dump(data, f, indent=2)
        print(f"Saved {output_file}")

    return {
        "income_statement": {**income, "ttm": income_ttm},
        "balance_sheet": balance_sheet,
        "cash_flow_statement": {**cash_flow, "ttm": cash_flow_ttm},
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: .venv/Scripts/python sec_edgar_data.py TICKER")
        sys.exit(1)

    fetch_edgar_statements(sys.argv[1])
