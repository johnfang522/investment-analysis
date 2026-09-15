import json
import sys
from datetime import date
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font, Alignment
from openpyxl.utils import get_column_letter
from openpyxl.formatting.rule import ColorScaleRule
from openpyxl.comments import Comment

# Manual fills (used only for current_price special coloring)
GREEN  = PatternFill("solid", fgColor="C6EFCE")
YELLOW = PatternFill("solid", fgColor="FFEB9C")
PINK   = PatternFill("solid", fgColor="FFB6C1")

# Gradient CF palette (Excel standard traffic-light)
CF_GREEN  = "63BE7B"
CF_YELLOW = "FFEB84"
CF_RED    = "F8696B"

BOLD      = Font(bold=True)
ITALIC_SM = Font(italic=True, size=9)
SM        = Font(size=9)
INDENT    = "    "


def make_cf_rule(lo, mid, hi, reverse=False):
    """3-color gradient. reverse=True → low value is green (lower is better)."""
    s_color, e_color = (CF_GREEN, CF_RED) if reverse else (CF_RED, CF_GREEN)
    return ColorScaleRule(
        start_type="num", start_value=lo,  start_color=s_color,
        mid_type="num",   mid_value=mid,   mid_color=CF_YELLOW,
        end_type="num",   end_value=hi,    end_color=e_color,
    )


def load_quick(ticker):
    path = f"Outputs/{ticker.upper()}/{ticker.lower()}_quick_metrics.json"
    with open(path) as f:
        return json.load(f)

def load_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except Exception:
        return {}

def get(d, *keys, default=None):
    for k in keys:
        v = d.get(k)
        if v is not None:
            if isinstance(v, dict):
                vals = [x for x in v.values() if x is not None]
                v = vals[0] if vals else None
            if v is not None:
                return v
    return default


def _calc_rsi(path, period=14):
    all_prices = [v for v in load_json(path).values() if v is not None]
    if len(all_prices) < period + 1:
        return None
    deltas = [all_prices[i] - all_prices[i-1] for i in range(1, len(all_prices))]
    gains  = [max(d, 0)      for d in deltas]
    losses = [abs(min(d, 0)) for d in deltas]
    avg_gain = sum(gains[:period])  / period
    avg_loss = sum(losses[:period]) / period
    for g, l in zip(gains[period:], losses[period:]):
        avg_gain = (avg_gain * (period - 1) + g) / period
        avg_loss = (avg_loss * (period - 1) + l) / period
    if avg_loss == 0:
        return 100.0
    return 100 - (100 / (1 + avg_gain / avg_loss))


def _latest(series):
    """Given a {date: value} dict, return the value for the most recent date."""
    if not series:
        return None
    latest_date = max(series.keys())
    return series[latest_date]


# Source labels — used to footnote every computed metric with where its
# number actually came from. Note these describe the ACTUAL source used at
# runtime, not just the intended primary source: a metric whose SEC-derived
# value is unavailable falls back to Yahoo and is labeled SRC_YAHOO for
# that ticker, even though its "primary source" is SEC EDGAR for tickers
# where the SEC data is present. Always read sources from the dict
# `compute_metrics(ticker, with_sources=True)` returns — never assume a
# metric's source from its key name alone.
SRC_SEC     = "SEC EDGAR"
SRC_YAHOO   = "Yahoo Finance"
SRC_HYBRID  = "Hybrid (SEC EDGAR + Yahoo Finance)"
SRC_COMPUTED = "Computed (Yahoo Finance price history)"
SRC_NA      = "N/A (no data available)"


def compute_metrics(ticker, with_sources=False):
    """
    Compute all metrics for a ticker.

    Statement-derived metrics (revenue, growth, margins, ROE, D/E, interest
    coverage, current ratio, FCF margin, Rule of 40, payout ratio) are
    computed from SEC EDGAR data (sec_edgar_data.py output) since it is not
    subject to Yahoo Finance's multi-week post-earnings lag. Market-quote
    metrics with no SEC EDGAR equivalent (current price, 52-week range,
    market cap, forward P/E, PEG, dividend yield, sector) come from Yahoo's
    quick_metrics. Trailing P/E and Price/Sales are hybrids of SEC EDGAR
    fundamentals + Yahoo's current price. Yahoo fields are used as a
    fallback wherever the SEC-derived value is unavailable (e.g. a tag the
    filer doesn't use).

    Args:
        ticker (str): Ticker symbol.
        with_sources (bool): If True, return (results, sources) — a second
            dict, same keys as results, mapping each metric to the label
            (SRC_SEC / SRC_YAHOO / SRC_HYBRID / SRC_COMPUTED / SRC_NA)
            describing where that metric's value actually came from for
            this specific ticker. If False (default), return only results,
            unchanged from prior behavior — existing callers need no
            changes.

    Returns:
        dict, or (dict, dict) if with_sources=True.
    """
    q = load_quick(ticker)
    t = ticker.lower()
    base = f"Outputs/{ticker.upper()}"

    results = {}
    sources = {}

    def set_result(key, value, source):
        results[key] = value
        sources[key] = source

    # Price (Yahoo quote data — no SEC EDGAR equivalent)
    set_result("current_price", get(q, "currentPrice", "regularMarketPrice"), SRC_YAHOO)
    set_result("week52_low", get(q, "fiftyTwoWeekLow"), SRC_YAHOO)
    set_result("week52_high", get(q, "fiftyTwoWeekHigh"), SRC_YAHOO)
    set_result("rsi", _calc_rsi(f"{base}/{t}_price_history.json"), SRC_COMPUTED)

    # Size
    set_result("market_cap", get(q, "marketCap"), SRC_YAHOO)

    ttm_is = load_json(f"{base}/{t}_income_statement_ttm.json")
    ttm_cf = load_json(f"{base}/{t}_cash_flow_statement_ttm.json")
    ann_is = load_json(f"{base}/{t}_income_statement_annual.json")
    bs     = load_json(f"{base}/{t}_balance_sheet_quarterly.json")

    rev = get(ttm_is, "Total Revenue")
    if rev is not None:
        set_result("revenue", rev, SRC_SEC)
    else:
        rev = get(q, "totalRevenue")
        set_result("revenue", rev, SRC_YAHOO)

    # Growth — from two most recent annual periods
    rev_growth = None
    tr = ann_is.get("Total Revenue")
    if tr:
        dates = sorted(tr.keys(), reverse=True)
        if len(dates) >= 2:
            latest_v, prior_v = tr[dates[0]], tr[dates[1]]
            if prior_v:
                rev_growth = (latest_v - prior_v) / abs(prior_v)
    if rev_growth is not None:
        set_result("rev_growth", rev_growth, SRC_SEC)
    else:
        set_result("rev_growth", get(q, "revenueGrowth"), SRC_YAHOO)

    # Margins
    total_rev = get(ttm_is, "Total Revenue") or rev
    cost_rev  = get(ttm_is, "Cost Of Revenue")
    gm = (total_rev - cost_rev) / total_rev if (total_rev and cost_rev is not None) else None
    if gm is not None:
        set_result("gross_margin", gm, SRC_SEC)
    else:
        set_result("gross_margin", get(q, "grossMargins"), SRC_YAHOO)

    op_inc = get(ttm_is, "Operating Income")
    op_margin = (op_inc / total_rev) if (total_rev and op_inc is not None) else None
    if op_margin is not None:
        set_result("op_margin", op_margin, SRC_SEC)
    else:
        op_margin = get(q, "operatingMargins")
        set_result("op_margin", op_margin, SRC_YAHOO)

    ni = get(ttm_is, "Net Income")
    ni_margin = (ni / total_rev) if (total_rev and ni is not None) else None
    if ni_margin is not None:
        set_result("ni_margin", ni_margin, SRC_SEC)
    else:
        set_result("ni_margin", get(q, "profitMargins"), SRC_YAHOO)

    # Returns / leverage
    equity = _latest(bs.get("Stockholders Equity", {}))
    roe = (ni / equity) if (ni is not None and equity) else None
    if roe is not None:
        set_result("roe", roe, SRC_SEC)
    else:
        set_result("roe", get(q, "returnOnEquity"), SRC_YAHOO)

    total_debt = _latest(bs.get("Total Debt", {}))
    de = (total_debt / equity) if (total_debt is not None and equity) else None
    if de is not None:
        set_result("de", de, SRC_SEC)
    else:
        de_raw = get(q, "debtToEquity")
        set_result("de", de_raw / 100 if de_raw is not None else None, SRC_YAHOO)

    ebit = op_inc
    interest_exp = get(ttm_is, "Interest Expense")
    interest_cov = (ebit / abs(interest_exp)
                    if ebit is not None and interest_exp else None)
    set_result("interest_cov", interest_cov, SRC_SEC if interest_cov is not None else SRC_NA)

    cur_assets = _latest(bs.get("Current Assets", {}))
    cur_liab   = _latest(bs.get("Current Liabilities", {}))
    cur_ratio = (cur_assets / cur_liab) if (cur_assets and cur_liab) else None
    if cur_ratio is not None:
        set_result("cur_ratio", cur_ratio, SRC_SEC)
    else:
        set_result("cur_ratio", get(q, "currentRatio"), SRC_YAHOO)

    fcf = get(ttm_cf, "Free Cash Flow")
    fcf_source = SRC_SEC
    if fcf is None:
        fcf = get(q, "freeCashflow")
        fcf_source = SRC_YAHOO
    fcf_margin = (fcf / rev) if (fcf is not None and rev) else None
    set_result("fcf_margin", fcf_margin, fcf_source if fcf_margin is not None else SRC_NA)

    r40 = (rev_growth * 100 + op_margin * 100) if (rev_growth is not None and op_margin is not None) else None
    # Rule of 40 inherits its inputs' sources — hybrid only if one leg came
    # from SEC EDGAR and the other from Yahoo; otherwise same as both.
    r40_source = SRC_NA
    if r40 is not None:
        rg_src = sources["rev_growth"]
        om_src = sources["op_margin"]
        r40_source = rg_src if rg_src == om_src else SRC_HYBRID
    set_result("r40", r40, r40_source)

    # Valuation
    # Trailing P/E and Price/Sales are hybrids: SEC EDGAR supplies the
    # fundamentals (Diluted EPS TTM; Shares Outstanding from the filing
    # cover page) but the price/market-cap side has no SEC EDGAR
    # equivalent, so current_price (Yahoo) is still required. Only
    # meaningful for positive EPS, matching Yahoo's own convention of
    # returning no trailing P/E for loss-making companies.
    price = results["current_price"]
    diluted_eps = get(ttm_is, "Diluted EPS")
    trailing_pe = (price / diluted_eps
                   if (price is not None and diluted_eps and diluted_eps > 0) else None)
    if trailing_pe is not None:
        set_result("trailing_pe", trailing_pe, SRC_HYBRID)
    else:
        set_result("trailing_pe", get(q, "trailingPE"), SRC_YAHOO)

    shares_out = _latest(bs.get("Shares Outstanding", {}))
    price_to_sales = ((price * shares_out) / rev
                       if (price is not None and shares_out and rev) else None)
    if price_to_sales is not None:
        set_result("price_to_sales", price_to_sales, SRC_HYBRID)
    else:
        set_result("price_to_sales", get(q, "priceToSalesTrailing12Months"), SRC_YAHOO)

    # Forward P/E and PEG have no SEC EDGAR equivalent at all — both
    # require forward-looking consensus analyst estimates (next-FY EPS,
    # expected growth rate), which SEC filings never contain (only actual
    # reported historicals). Always sourced from Yahoo quote data.
    set_result("forward_pe", get(q, "forwardPE"), SRC_YAHOO)
    set_result("peg", get(q, "pegRatio", "trailingPegRatio"), SRC_YAHOO)

    dividends_paid = get(ttm_cf, "Cash Dividends Paid")
    payout_ratio = (abs(dividends_paid) / ni) if (dividends_paid is not None and ni) else None
    if payout_ratio is not None:
        set_result("payout_ratio", payout_ratio, SRC_SEC)
    else:
        set_result("payout_ratio", get(q, "payoutRatio"), SRC_YAHOO)

    set_result("sector", q.get("sector", ""), SRC_YAHOO)

    forward_dy  = q.get("dividendYield")
    trailing_dy = q.get("trailingAnnualDividendYield")
    if forward_dy:
        set_result("dividend_yield", forward_dy / 100, SRC_YAHOO)
    elif trailing_dy:
        set_result("dividend_yield", trailing_dy, SRC_YAHOO)
    else:
        set_result("dividend_yield", None, SRC_NA)

    if with_sources:
        return results, sources
    return results


# ── Metric definitions ───────────────────────────────────────────────────────
# num_fmt : Excel number-format string applied to the cell
# scale   : multiply raw value by this before writing to cell (default 1)
# cf      : (lo, mid, hi, reverse) for ColorScaleRule, or None

METRICS = [
    {
        "key":     "current_price",
        "label":   "1. Current Price",
        "desc":    "Most recent market price of the stock.",
        "bench":   "Green = bottom third of 52-wk range | Yellow = middle third | Pink = top third",
        "num_fmt": '$#,##0.00',
        "scale":   1,
        "cf":      None,   # handled via manual fill
    },
    {
        "key":     "week52_low",
        "label":   "2. 52-Week Low",
        "desc":    "Lowest traded price over the trailing 52 weeks.",
        "bench":   "Informational — no threshold coloring",
        "num_fmt": '$#,##0.00',
        "scale":   1,
        "cf":      None,
    },
    {
        "key":     "week52_high",
        "label":   "3. 52-Week High",
        "desc":    "Highest traded price over the trailing 52 weeks.",
        "bench":   "Informational — no threshold coloring",
        "num_fmt": '$#,##0.00',
        "scale":   1,
        "cf":      None,
    },
    {
        "key":     "rsi",
        "label":   "4. RSI (14-Day)",
        "desc":    "Wilder's 14-day Relative Strength Index. Measures momentum and overbought/oversold conditions.",
        "bench":   "≤30 → Oversold / potential buy | 30–70 → Neutral | ≥70 → Overbought / potential sell",
        "num_fmt": '0.0',
        "scale":   1,
        "cf":      (20, 50, 80, True),   # lower = oversold = green
    },
    {
        "key":     "market_cap",
        "label":   "5. Market Cap",
        "desc":    "Total market value of all outstanding shares (Price × Shares Outstanding).",
        "bench":   "Informational — no threshold coloring",
        "num_fmt": '$#,##0.0"B"',
        "scale":   1e-9,
        "cf":      None,
    },
    {
        "key":     "revenue",
        "label":   "6. Revenue (TTM)",
        "desc":    "Total revenue over the trailing twelve months.",
        "bench":   "Informational — no threshold coloring",
        "num_fmt": '$#,##0.0"B"',
        "scale":   1e-9,
        "cf":      None,
    },
    {
        "key":     "rev_growth",
        "label":   "7. Revenue Growth Rate (YoY)",
        "desc":    "YoY revenue growth from quick metrics or computed from two most recent annual periods.",
        "bench":   ">20% → Strong | 10–20% → Solid | <10% → Slow",
        "num_fmt": '0.0%',
        "scale":   1,
        "cf":      (-0.05, 0.10, 0.25, False),
    },
    {
        "key":     "gross_margin",
        "label":   "8. Gross Margin",
        "desc":    "(Total Revenue − Cost of Revenue) / Total Revenue (TTM).",
        "bench":   ">60% → High quality | 40–60% → Decent | <40% → Watch for pricing pressure",
        "num_fmt": '0.0%',
        "scale":   1,
        "cf":      (0.15, 0.40, 0.65, False),
    },
    {
        "key":     "op_margin",
        "label":   "9. Operating Margin",
        "desc":    "Operating Income (TTM) / Total Revenue (TTM).",
        "bench":   ">30% → Strong pricing power | 15–30% → Decent | <15% → Watch for cost pressure",
        "num_fmt": '0.0%',
        "scale":   1,
        "cf":      (0.0, 0.15, 0.35, False),
    },
    {
        "key":     "ni_margin",
        "label":   "10. Net Income Margin",
        "desc":    "Net Income (TTM) / Total Revenue (TTM). Bottom-line profitability after all expenses.",
        "bench":   ">20% → Strong | 10–20% → Decent | <10% → Thin",
        "num_fmt": '0.0%',
        "scale":   1,
        "cf":      (0.0, 0.10, 0.25, False),
    },
    {
        "key":     "roe",
        "label":   "11. Return on Equity (ROE)",
        "desc":    "Net Income (TTM) / Stockholders Equity (MRQ).",
        "bench":   "≥20% → Ideal | ≥15% → Good | <15% → Below threshold",
        "num_fmt": '0.0%',
        "scale":   1,
        "cf":      (0.0, 0.12, 0.25, False),
    },
    {
        "key":     "de",
        "label":   "12. Debt-to-Equity (D/E)",
        "desc":    "Total Debt (MRQ) / Stockholders Equity (MRQ). Measures financial leverage.",
        "bench":   "<0.5 → Very conservative | 0.5–1.0 → Healthy | 1.0–2.0 → Moderate | >2.0 → High risk",
        "num_fmt": '0%',
        "scale":   1,
        "cf":      (0.0, 1.0, 3.0, True),  # lower is better
    },
    {
        "key":     "interest_cov",
        "label":   "13. Interest Coverage",
        "desc":    "EBIT (TTM) / Interest Expense (TTM). Ability to service debt from operating earnings.",
        "bench":   ">10× → Very safe | 5–10× → Adequate | 3–5× → Watch | <3× → At risk",
        "num_fmt": '0.0"×"',
        "scale":   1,
        "cf":      (1.0, 5.0, 15.0, False),
    },
    {
        "key":     "cur_ratio",
        "label":   "14. Current Ratio",
        "desc":    "Current Assets (MRQ) / Current Liabilities (MRQ). Short-term liquidity.",
        "bench":   ">2.0 → Very liquid | 1.5–2.0 → Healthy | 1.0–1.5 → Adequate | <1.0 → Liquidity risk",
        "num_fmt": '0.00',
        "scale":   1,
        "cf":      (0.5, 1.5, 3.0, False),
    },
    {
        "key":     "fcf_margin",
        "label":   "15. FCF Margin",
        "desc":    "Free Cash Flow (TTM) / Total Revenue (TTM). Cash generated per dollar of revenue after capex.",
        "bench":   ">20% → High quality | 10–20% → Solid | <10% → Low",
        "num_fmt": '0.0%',
        "scale":   1,
        "cf":      (-0.05, 0.10, 0.30, False),
    },
    {
        "key":     "r40",
        "label":   "16. Rule of 40",
        "desc":    "Revenue Growth Rate (YoY%) + Operating Margin (TTM%). Balances growth and profitability.",
        "bench":   ">40 → Healthy/investible | 30–40 → Borderline | <30 → Warning zone",
        "num_fmt": '0.0',
        "scale":   1,
        "cf":      (0, 25, 50, False),
    },
    {
        "key":     "trailing_pe",
        "label":   "17a. Trailing P/E",
        "desc":    "Price / Trailing Twelve Months EPS. How much investors pay per dollar of past earnings.",
        "bench":   "<15 → Cheap | 15–25 → Fair | >25 → Expensive",
        "num_fmt": '0.0',
        "scale":   1,
        "cf":      (10, 25, 50, True),  # lower is better
    },
    {
        "key":     "forward_pe",
        "label":   "17b. Forward P/E",
        "desc":    "Price / Next Twelve Months EPS Estimate. Investors' view of future earnings power.",
        "bench":   "<15 → Cheap | 15–25 → Fair | >25 → Expensive",
        "num_fmt": '0.0',
        "scale":   1,
        "cf":      (8, 20, 40, True),   # lower is better
    },
    {
        "key":     "peg",
        "label":   "17c. PEG Ratio",
        "desc":    "Trailing P/E / Earnings Growth Rate. Adjusts valuation for expected growth.",
        "bench":   "<1 → Potentially undervalued | 1–2 → Fair | >2 → Expensive relative to growth",
        "num_fmt": '0.00',
        "scale":   1,
        "cf":      (0.5, 1.5, 3.0, True),  # lower is better
    },
    {
        "key":     "price_to_sales",
        "label":   "17d. Price / Sales (TTM)",
        "desc":    "Market Cap / Total Revenue (TTM). Useful for low-earnings companies; lower is cheaper.",
        "bench":   "<3 → Cheap | 3–6 → Fair | >6 → Expensive",
        "num_fmt": '0.0',
        "scale":   1,
        "cf":      (1, 4, 10, True),    # lower is better
    },
    {
        "key":     "dividend_yield",
        "label":   "18. Dividend Yield",
        "desc":    "Annual dividend per share / current price. Shown when available; N/A otherwise.",
        "bench":   ">4% → High yield | 2–4% → Moderate | <2% → Low yield",
        "num_fmt": '0.0%',
        "scale":   1,
        "cf":      (0.005, 0.025, 0.05, False),  # higher is better
    },
    {
        "key":     "payout_ratio",
        "label":   "19. Dividend Payout Ratio",
        "desc":    "Dividends paid / Net Income (TTM). Measures what fraction of earnings is returned to shareholders as dividends. Note: for REITs, net income understates true cash earnings — AFFO payout ratio (dividends / AFFO) is the appropriate metric; values shown here for REITs will appear artificially high and should be interpreted with caution.",
        "bench":   "<50% → Sustainable | 50–75% → Moderate | >75% → High / potential cut risk | >100% → Unsustainable (REITs: use AFFO payout ratio instead)",
        "num_fmt": '0%',
        "scale":   1,
        "cf":      (0.2, 0.6, 1.0, True),  # lower is better (more sustainable)
    },
]


# ── Helpers ──────────────────────────────────────────────────────────────────

def color_current_price(metrics):
    """Manual fill: green = bottom third, yellow = middle third, pink = top third of 52-wk range."""
    price = metrics.get("current_price")
    low   = metrics.get("week52_low")
    high  = metrics.get("week52_high")
    if price is None or low is None or high is None or high == low:
        return None
    pos = (price - low) / (high - low)
    if pos < 1/3:   return GREEN
    if pos <= 2/3:  return YELLOW
    return PINK


def _short_comment(key, val, metrics=None):
    if val is None:
        return ""
    if key == "current_price":
        low  = (metrics or {}).get("week52_low")
        high = (metrics or {}).get("week52_high")
        if low is not None and high is not None and high != low:
            pos  = (val - low) / (high - low)
            zone = ("Near 52-wk low" if pos < 1/3
                    else ("Mid-range" if pos <= 2/3 else "Near 52-wk high"))
            return f"{zone} ({pos*100:.0f}% of range)"
        return ""
    if key == "rsi":
        if val >= 70: return "Overbought (≥70)"
        if val <= 30: return "Oversold (≤30)"
        return "Neutral (30–70)"
    if key == "rev_growth":
        if val > 0.20:  return "Strong (>20%)"
        if val >= 0.10: return "Solid (10–20%)"
        return "Slow (<10%)"
    if key == "gross_margin":
        if val > 0.60:  return "High quality (>60%)"
        if val >= 0.40: return "Decent (40–60%)"
        return "Watch for pricing pressure (<40%)"
    if key == "op_margin":
        if val > 0.30:  return "Strong pricing power (>30%)"
        if val >= 0.15: return "Decent (15–30%)"
        return "Watch for cost pressure (<15%)"
    if key == "ni_margin":
        if val > 0.20:  return "Strong (>20%)"
        if val >= 0.10: return "Decent (10–20%)"
        return "Thin (<10%)"
    if key == "roe":
        if val >= 0.20: return "Ideal (≥20%)"
        if val >= 0.15: return "Good (≥15%)"
        return "Below threshold (<15%)"
    if key == "de":
        if val < 0.5:  return "Very conservative"
        if val <= 1.0: return "Healthy"
        if val <= 2.0: return "Moderate leverage"
        return "High risk"
    if key == "interest_cov":
        if val > 10: return "Very safe (>10×)"
        if val >= 5: return "Adequate (5–10×)"
        if val >= 3: return "Watch (3–5×)"
        return "At risk (<3×)"
    if key == "cur_ratio":
        if val > 2.0:  return "Very liquid (>2.0)"
        if val >= 1.5: return "Healthy (1.5–2.0)"
        if val >= 1.0: return "Adequate (1.0–1.5)"
        return "Liquidity risk (<1.0)"
    if key == "fcf_margin":
        if val > 0.20:  return "High quality (>20%)"
        if val >= 0.10: return "Solid (10–20%)"
        return "Low (<10%)"
    if key == "r40":
        if val > 40:  return "Healthy / investible (>40)"
        if val >= 30: return "Borderline (30–40)"
        return "Warning zone (<30)"
    if key == "peg":
        if val < 1:  return "Potentially undervalued (<1)"
        if val <= 2: return "Fair (1–2)"
        return "Expensive relative to growth (>2)"
    if key == "payout_ratio":
        sector = (metrics or {}).get("sector", "")
        if sector == "Real Estate":
            return "⚠ REIT — use AFFO payout ratio; net income understates cash earnings"
        if val < 0.5:  return "Sustainable (<50%)"
        if val <= 0.75: return "Moderate (50–75%)"
        if val <= 1.0:  return "High — potential cut risk (75–100%)"
        return "Unsustainable (>100%)"
    return ""


# ── Sheet writers ─────────────────────────────────────────────────────────────

HDR_FILL = PatternFill("solid", fgColor="1F3864")
HDR_FONT = Font(bold=True, color="FFFFFF")


def _add_source_note(cell, source):
    """Attach a hover-note (Excel's native footnote) citing where a value came from."""
    if not source:
        return
    cell.comment = Comment(f"Source: {source}", "key_stock_metrics.py")


def _write_value_cell(ws, row, col, val, m, ticker_metrics=None, source=None):
    """Write a numeric value cell with number format, manual fill or CF rule."""
    cell = ws.cell(row=row, column=col)
    cell.alignment = Alignment(horizontal="center")

    if val is None:
        cell.value = "N/A"
        _add_source_note(cell, source)
        return

    cell.value = val * m["scale"]
    cell.number_format = m["num_fmt"]
    _add_source_note(cell, source)

    # Current price: manual fill based on 52-wk range
    if m["key"] == "current_price" and ticker_metrics is not None:
        fill = color_current_price(ticker_metrics)
        if fill:
            cell.fill = fill


def _apply_cf(ws, cell_range, m):
    """Apply ColorScaleRule to a cell range for metrics that have CF defined."""
    if m["cf"] is None or m["key"] == "current_price":
        return
    lo, mid, hi, reverse = m["cf"]
    rule = make_cf_rule(lo * m["scale"], mid * m["scale"], hi * m["scale"], reverse)
    ws.conditional_formatting.add(cell_range, rule)


def write_ticker_sheet(wb, ticker, metrics, sources=None):
    sources = sources or {}
    ws = wb.create_sheet(title=ticker)
    ws.column_dimensions["A"].width = 30
    ws.column_dimensions["B"].width = 16
    ws.column_dimensions["C"].width = 42
    ws.column_dimensions["D"].width = 30

    ws.cell(row=1, column=1, value=f"{ticker} — Key Stock Metrics").font = Font(bold=True, size=13)
    ws.append([])

    for col, heading in enumerate(["Metric", "Value", "Comment", "Source"], start=1):
        c = ws.cell(row=3, column=col, value=heading)
        c.font = HDR_FONT
        c.fill = HDR_FILL
        c.alignment = Alignment(horizontal="center")

    for i, m in enumerate(METRICS):
        row = i + 4
        val = metrics.get(m["key"])
        src = sources.get(m["key"])
        ws.cell(row=row, column=1, value=m["label"]).font = BOLD
        _write_value_cell(ws, row, 2, val, m, ticker_metrics=metrics, source=src)
        ws.cell(row=row, column=3, value=_short_comment(m["key"], val, metrics)).font = SM
        ws.cell(row=row, column=4, value=src or "").font = SM
        cell_addr = f"B{row}"
        _apply_cf(ws, cell_addr, m)


def write_comparison_sheet(wb, tickers, all_metrics, all_sources=None):
    all_sources = all_sources or {}
    ws = wb.create_sheet(title="Comparison")
    wb.move_sheet(ws, offset=-(len(wb.sheetnames) - 1))

    ws.column_dimensions["A"].width = 28
    for col in range(2, len(tickers) + 2):
        ws.column_dimensions[get_column_letter(col)].width = 13

    # ── Header row ────────────────────────────────────────────────────────────
    c = ws.cell(row=1, column=1, value="Metric")
    c.font = HDR_FONT; c.fill = HDR_FILL; c.alignment = Alignment(horizontal="center")
    for col, ticker in enumerate(tickers, start=2):
        c = ws.cell(row=1, column=col, value=ticker)
        c.font = HDR_FONT; c.fill = HDR_FILL; c.alignment = Alignment(horizontal="center")

    # ── Data rows ─────────────────────────────────────────────────────────────
    # Each value cell carries a hover note citing its source (SEC EDGAR /
    # Yahoo Finance / Hybrid / Computed) since sources can differ by ticker
    # for the same metric — whichever ticker's SEC-derived value happened
    # to be unavailable falls back to Yahoo for that ticker only. A visible
    # per-ticker Source column isn't practical here without doubling the
    # sheet width; see the ticker sheets for a visible Source column.
    for r, m in enumerate(METRICS, start=2):
        ws.cell(row=r, column=1, value=m["label"]).font = BOLD
        for col, ticker in enumerate(tickers, start=2):
            val = all_metrics[ticker].get(m["key"])
            src = all_sources.get(ticker, {}).get(m["key"])
            _write_value_cell(ws, r, col, val, m,
                              ticker_metrics=all_metrics[ticker] if m["key"] == "current_price" else None,
                              source=src)

        # Apply CF across all ticker columns for this row
        if len(tickers) == 1:
            cf_range = f"{get_column_letter(2)}{r}"
        else:
            cf_range = f"{get_column_letter(2)}{r}:{get_column_letter(len(tickers)+1)}{r}"
        _apply_cf(ws, cf_range, m)

    # ── Metric descriptions & benchmarks ─────────────────────────────────────
    desc_start = len(METRICS) + 3
    ws.cell(row=desc_start, column=1,
            value="Metric Descriptions & Benchmarks").font = Font(bold=True, size=12)
    row = desc_start + 2
    for m in METRICS:
        ws.cell(row=row,   column=1, value=m["label"]).font = BOLD
        ws.cell(row=row+1, column=1, value=f"{INDENT}Description:").font = ITALIC_SM
        ws.cell(row=row+1, column=2, value=m["desc"]).font = SM
        ws.cell(row=row+2, column=1, value=f"{INDENT}Benchmarks:").font = ITALIC_SM
        ws.cell(row=row+2, column=2, value=m["bench"]).font = SM
        row += 4

    # ── Source legend ─────────────────────────────────────────────────────────
    legend_start = row + 1
    ws.cell(row=legend_start, column=1,
            value="Data Source Legend").font = Font(bold=True, size=12)
    legend_rows = [
        ("SEC EDGAR", "Computed from sec_edgar_data.py's XBRL company-facts output (income statement, balance sheet, cash flow) — current as of the latest 10-Q/10-K filing."),
        ("Yahoo Finance", "From yahoo_finance_data.py's quick_metrics (quote/market data with no SEC EDGAR equivalent, e.g. current price, market cap; or a fallback when the SEC-derived value was unavailable for that ticker)."),
        ("Hybrid (SEC EDGAR + Yahoo Finance)", "SEC EDGAR fundamentals combined with Yahoo Finance's current price (Trailing P/E, Price/Sales) — SEC filings never contain a trading price."),
        ("Computed (Yahoo Finance price history)", "Derived locally from Yahoo Finance daily price history (RSI via Wilder's 14-day method)."),
        ("N/A (no data available)", "Neither SEC EDGAR nor Yahoo Finance had the data needed to compute this metric for this ticker."),
    ]
    row = legend_start + 2
    for label, desc in legend_rows:
        ws.cell(row=row, column=1, value=label).font = BOLD
        ws.cell(row=row, column=2, value=desc).font = SM
        row += 1
    ws.cell(row=row + 1, column=1,
            value="Hover over any value cell (in this sheet or a ticker sheet) to see its specific source.").font = ITALIC_SM


# ── Entry point ───────────────────────────────────────────────────────────────

def main(tickers):
    all_metrics = {}
    all_sources = {}
    for t in tickers:
        print(f"Computing metrics for {t}...")
        all_metrics[t], all_sources[t] = compute_metrics(t, with_sources=True)

    wb = Workbook()
    wb.remove(wb.active)

    for t in tickers:
        write_ticker_sheet(wb, t, all_metrics[t], sources=all_sources[t])

    write_comparison_sheet(wb, tickers, all_metrics, all_sources=all_sources)

    out = f"Outputs/key_stock_metrics_{date.today().strftime('%Y%m%d')}.xlsx"
    wb.save(out)
    print(f"Saved: {out}")
    return out


if __name__ == "__main__":
    if len(sys.argv) > 1:
        tickers = [t.upper() for t in sys.argv[1:]]
    else:
        sys.path.insert(0, ".")
        from get_financial_data import load_tickers
        tickers = load_tickers()
    main(tickers)
