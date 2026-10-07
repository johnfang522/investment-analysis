"""
digest.py TICKER SECTION

Prints a compact, pre-computed JSON digest of the cached statement JSON for one
skill, so a skill reads ~1-2K tokens of exact figures instead of 3-6 raw JSON
files (and never does the arithmetic by hand). Every figure carries its source.

    PYTHONIOENCODING=utf-8 .venv/Scripts/python digest.py TSLA cash_flow

Sections: cash_flow
Reads Outputs/{TICKER}/ only; run get_financial_data.fetch_all() first if JSON is missing.
"""
import json
import os
import sys
from datetime import date

from doc_utils import fmt_value

SEC, YAHOO, HYBRID, COMPUTED = "SEC EDGAR", "Yahoo Finance", "SEC EDGAR × Yahoo Finance (hybrid)", "computed"


def _load(ticker, name):
    path = f"Outputs/{ticker}/{ticker.lower()}_{name}.json"
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _series(data, key):
    """{date: value} for one line item, TTM key dropped, oldest first."""
    raw = data.get(key) or {}
    return dict(sorted((d, v) for d, v in raw.items() if d != "TTM" and v is not None))


def _ttm(data, key):
    return (data.get(key) or {}).get("TTM")


def _prior_year_date(dates, latest):
    """The period end closest to one year before `latest` (within 20 days), or None."""
    y, m, d = map(int, latest.split("-"))
    target = date(y - 1, m, min(d, 28))
    best = min(dates, key=lambda s: abs((date(*map(int, s.split("-"))) - target).days), default=None)
    if best and abs((date(*map(int, best.split("-"))) - target).days) <= 20:
        return best
    return None


def _ratio(a, b):
    if a is None or b in (None, 0):
        return None
    return round(a / b, 2)


def _pct(a, b):
    """Margin or share in percent."""
    r = _ratio(a, b)
    return None if r is None else round(a / b * 100, 1)


def _yoy(a, b):
    """YoY % change; 'n/m' when the sign flips or the base is negative (quote the $ change instead)."""
    if a is None or b in (None, 0):
        return None
    if b < 0 or (a < 0) != (b < 0):
        return "n/m"
    return round((a - b) / b * 100, 1)


def _money(v):
    return {"value": v, "fmt": fmt_value(v)}


def _compact(obj):
    """Collapse {"value", "fmt"} pairs to their fmt string (plus source when present) for printing."""
    if isinstance(obj, dict):
        if "fmt" in obj and "value" in obj:
            return f"{obj['fmt']} [{obj['source']}]" if "source" in obj else obj["fmt"]
        return {k: _compact(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_compact(v) for v in obj]
    return obj


def _period(cf, inc, when):
    """Cash-flow block for one period; `when` is a date string or 'TTM'."""
    get_cf = (lambda k: _ttm(cf["ttm"], k)) if when == "TTM" else (lambda k: _series(cf["q"], k).get(when))
    get_inc = (lambda k: _ttm(inc["ttm"], k)) if when == "TTM" else (lambda k: _series(inc["q"], k).get(when))
    rev, ni = get_inc("Total Revenue"), get_inc("Net Income")
    ocf, capex, fcf = get_cf("Operating Cash Flow"), get_cf("Capital Expenditure"), get_cf("Free Cash Flow")
    div = get_cf("Cash Dividends Paid")
    out = {
        "period": when,
        "revenue": _money(rev), "net_income": _money(ni),
        "operating_cash_flow": _money(ocf), "capex": _money(capex), "free_cash_flow": _money(fcf),
        "dividends_paid": _money(div),
        "ocf_margin_pct": _pct(ocf, rev), "fcf_margin_pct": _pct(fcf, rev),
        "ocf_to_net_income": _ratio(ocf, ni) if ni and ni > 0 else None,
        "fcf_to_net_income": _ratio(fcf, ni) if ni and ni > 0 else None,
    }
    if ni is not None and ni <= 0:
        out["conversion_note"] = "net income <= 0: conversion ratios not meaningful"
    return out


def cash_flow(ticker):
    cf = {"q": _load(ticker, "cash_flow_statement_quarterly"), "ttm": _load(ticker, "cash_flow_statement_ttm"),
          "a": _load(ticker, "cash_flow_statement_annual")}
    inc = {"q": _load(ticker, "income_statement_quarterly"), "ttm": _load(ticker, "income_statement_ttm")}
    bs = _load(ticker, "balance_sheet_quarterly")
    qm = _load(ticker, "quick_metrics")
    if not cf["q"]:
        sys.exit(f"No cash flow JSON for {ticker}: run get_financial_data.fetch_all(['{ticker}']) first")

    dates = list(_series(cf["q"], "Operating Cash Flow"))
    latest = dates[-1]
    prior = _prior_year_date(dates, latest)
    L, P, T = _period(cf, inc, latest), (_period(cf, inc, prior) if prior else None), _period(cf, inc, "TTM")

    yoy = {}
    if P:
        for k in ("operating_cash_flow", "capex", "free_cash_flow", "revenue", "net_income", "dividends_paid"):
            yoy[k + "_pct"] = _yoy(L[k]["value"], P[k]["value"])
        for k in ("ocf_margin_pct", "fcf_margin_pct"):
            if L[k] is not None and P[k] is not None:
                yoy[k.replace("_pct", "_change_pp")] = round(L[k] - P[k], 1)

    trend = []
    for d in dates[-8:]:
        p = _period(cf, inc, d)
        trend.append({"period": d, "net_income": p["net_income"]["fmt"], "ocf": p["operating_cash_flow"]["fmt"],
                      "fcf": p["free_cash_flow"]["fmt"], "fcf_to_ni": p["fcf_to_net_income"]})

    annual = []
    for d in list(_series(cf["a"], "Operating Cash Flow"))[-4:]:
        annual.append({"fiscal_year_end": d,
                       **{k: fmt_value(_series(cf["a"], src).get(d)) for k, src in
                          (("ocf", "Operating Cash Flow"), ("capex", "Capital Expenditure"), ("fcf", "Free Cash Flow"))}})

    # Coverage: SEC debt first, Yahoo fallback; a 0/missing SEC debt line is missing data, not zero debt.
    bs_date = list(_series(bs, "Total Assets"))[-1] if bs else None
    sec_debt = _series(bs, "Total Debt").get(bs_date) if bs_date else None
    debt, debt_src = sec_debt, SEC
    yahoo_debt = qm.get("totalDebt")
    if not sec_debt:
        debt, debt_src = yahoo_debt, f"{YAHOO} (SEC EDGAR Total Debt missing/0 — untagged, verify in 10-Q)"
    elif yahoo_debt and sec_debt < 0.5 * yahoo_debt:
        debt_src = (f"{SEC} — WARNING: under half of Yahoo totalDebt {fmt_value(yahoo_debt)}; the EDGAR tag is "
                    "likely incomplete (finance leases / other notes), confirm total debt in the 10-Q")
    cash = _series(bs, "Cash And Cash Equivalents").get(bs_date) if bs_date else None
    interest = _ttm(inc["ttm"], "Interest Expense")
    ocf_t, fcf_t, div_t = T["operating_cash_flow"]["value"], T["free_cash_flow"]["value"], T["dividends_paid"]["value"]
    mcap = qm.get("marketCap")

    industry, sector = qm.get("industry") or "", qm.get("sector") or ""
    return {
        "ticker": ticker,
        "company": qm.get("longName") or qm.get("shortName"),
        "industry": industry, "sector": sector,
        "is_reit": industry.startswith("REIT") or sector == "Real Estate",
        "units_note": "capex is a positive outflow; $ strings are fmt_value() output — paste as-is; pct = percent, pp = points",
        "sources": {"statements": SEC, "market_cap_price": YAHOO, "fcf_yield": HYBRID, "ratios": COMPUTED},
        "latest_quarter": L, "prior_year_quarter": P, "ttm": T, "yoy": yoy,
        "trend_8q": trend, "annual": annual,
        "coverage": {
            "balance_sheet_date": bs_date,
            "total_debt": {**_money(debt), "source": debt_src},
            "cash": {**_money(cash), "source": SEC},
            "interest_expense_ttm": {**_money(interest), "source": SEC},
            "ocf_to_interest": _ratio(ocf_t, abs(interest)) if interest else None,
            "ocf_to_total_debt": _ratio(ocf_t, debt),
            "fcf_to_dividends": _ratio(fcf_t, abs(div_t)) if div_t else None,
        },
        "market": {"price": qm.get("currentPrice"), "market_cap": _money(mcap),
                   "fcf_yield_ttm_pct": _pct(fcf_t, mcap)},
        "missing_from_sec": "no D&A, SBC, working-capital, buyback or debt repayment lines — WebSearch the 10-Q/10-K",
    }


SECTIONS = {"cash_flow": cash_flow}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in SECTIONS:
        sys.exit(__doc__)
    print(json.dumps(_compact(SECTIONS[sys.argv[2]](sys.argv[1].upper())), indent=1, ensure_ascii=False))
