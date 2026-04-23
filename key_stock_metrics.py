import json
import sys
from datetime import date
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font, Alignment
from openpyxl.utils import get_column_letter

GREEN  = PatternFill("solid", fgColor="C6EFCE")
YELLOW = PatternFill("solid", fgColor="FFEB9C")
RED    = PatternFill("solid", fgColor="FFC7CE")
GREY   = PatternFill("solid", fgColor="D9D9D9")

BOLD = Font(bold=True)
ITALIC_SM = Font(italic=True, size=9)
SM = Font(size=9)

INDENT = "    "

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
            # Unwrap single-key dicts (e.g. {"TTM": 123} or {"2024-01-01": 123})
            if isinstance(v, dict):
                vals = [x for x in v.values() if x is not None]
                v = vals[0] if vals else None
            if v is not None:
                return v
    return default

def fmt_pct(v):
    return f"{v*100:.1f}%" if v is not None else "N/A"

def fmt_ratio(v):
    return f"{v*100:.0f}%" if v is not None else "N/A"

def fmt_num(v, decimals=1):
    return f"{v:.{decimals}f}" if v is not None else "N/A"

def fmt_revenue(v):
    return f"${v/1e9:.2f}B" if v is not None else "N/A"

def compute_metrics(ticker):
    q = load_quick(ticker)
    t = ticker.lower()
    base = f"Outputs/{ticker.upper()}"

    results = {}

    # 0. Market Cap
    results["market_cap"] = get(q, "marketCap")

    # 1. Revenue (TTM)
    rev = get(q, "totalRevenue")
    if rev is None:
        ttm_is = load_json(f"{base}/{t}_income_statement_ttm.json")
        rev = get(ttm_is, "Total Revenue", "TotalRevenue")
    results["revenue"] = rev

    # 2. Revenue Growth Rate
    rev_growth = get(q, "revenueGrowth")
    if rev_growth is None:
        ann = load_json(f"{base}/{t}_income_statement_annual.json")
        tr = ann.get("Total Revenue") or ann.get("TotalRevenue")
        if tr and isinstance(tr, dict):
            vals = [v for v in tr.values() if v is not None]
            if len(vals) >= 2:
                rev_growth = (vals[0] - vals[1]) / abs(vals[1]) if vals[1] else None
    results["rev_growth"] = rev_growth

    # 3. Gross Margin
    gm = get(q, "grossMargins")
    if gm is None:
        ttm_is = load_json(f"{base}/{t}_income_statement_ttm.json")
        total_rev = get(ttm_is, "Total Revenue", "TotalRevenue")
        cost_rev = get(ttm_is, "Cost Of Revenue", "CostOfRevenue", "Cost of Revenue")
        if total_rev and cost_rev is not None:
            gm = (total_rev - cost_rev) / total_rev
    results["gross_margin"] = gm

    # 4. Operating Margin
    op_margin = get(q, "operatingMargins")
    if op_margin is None:
        ttm_is = load_json(f"{base}/{t}_income_statement_ttm.json")
        total_rev = get(ttm_is, "Total Revenue", "TotalRevenue") or rev
        op_inc = get(ttm_is, "Operating Income", "OperatingIncome", "Total Operating Income As Reported")
        if total_rev and op_inc is not None:
            op_margin = op_inc / total_rev
    results["op_margin"] = op_margin

    # 5. Net Income Margin
    ni_margin = get(q, "profitMargins")
    if ni_margin is None:
        ttm_is = load_json(f"{base}/{t}_income_statement_ttm.json")
        total_rev = get(ttm_is, "Total Revenue", "TotalRevenue") or rev
        ni = get(ttm_is, "Net Income", "NetIncome", "Net Income Common Stockholders")
        if total_rev and ni is not None:
            ni_margin = ni / total_rev
    results["ni_margin"] = ni_margin

    # 6. ROE
    results["roe"] = get(q, "returnOnEquity")

    # 7. D/E
    de_raw = get(q, "debtToEquity")
    results["de"] = de_raw / 100 if de_raw is not None else None

    # 8. Interest Coverage
    interest_cov = None
    ttm_is = load_json(f"{base}/{t}_income_statement_ttm.json")
    ebit = get(ttm_is, "Operating Income", "OperatingIncome", "Total Operating Income As Reported", "EBIT")
    interest_exp = get(ttm_is, "Interest Expense", "InterestExpense")
    if ebit is not None and interest_exp is not None and interest_exp != 0:
        interest_cov = ebit / abs(interest_exp)
    results["interest_cov"] = interest_cov

    # 9. Current Ratio
    cur_ratio = get(q, "currentRatio")
    if cur_ratio is None:
        bs = load_json(f"{base}/{t}_balance_sheet_quarterly.json")
        cur_assets = get(bs, "Current Assets", "CurrentAssets", "Total Current Assets")
        cur_liab = get(bs, "Current Liabilities", "CurrentLiabilities", "Total Current Liabilities Net Minority Interest")
        if cur_assets and cur_liab:
            cur_ratio = cur_assets / cur_liab
    results["cur_ratio"] = cur_ratio

    # 10. FCF Margin
    fcf = get(q, "freeCashflow")
    results["fcf_margin"] = (fcf / rev) if (fcf is not None and rev) else None

    # 11. Rule of 40
    results["r40"] = (rev_growth * 100 + op_margin * 100) if (rev_growth is not None and op_margin is not None) else None

    # 12. Valuation
    results["trailing_pe"]    = get(q, "trailingPE")
    results["forward_pe"]     = get(q, "forwardPE")
    results["peg"]            = get(q, "pegRatio", "trailingPegRatio")
    results["price_to_sales"] = get(q, "priceToSalesTrailing12Months")

    return results

# ── Color functions ──────────────────────────────────────────────────────────

def color_none(v):
    return None

def color_rev_growth(v):
    if v is None: return None
    return GREEN if v > 0.20 else (YELLOW if v >= 0.10 else RED)

def color_gm(v):
    if v is None: return None
    return GREEN if v > 0.60 else (YELLOW if v >= 0.40 else RED)

def color_op(v):
    if v is None: return None
    return GREEN if v > 0.30 else (YELLOW if v >= 0.15 else RED)

def color_ni(v):
    if v is None: return None
    return GREEN if v > 0.20 else (YELLOW if v >= 0.10 else RED)

def color_roe(v):
    if v is None: return None
    return GREEN if v >= 0.20 else (YELLOW if v >= 0.15 else RED)

def color_de(v):
    if v is None: return None
    return GREEN if v < 1.0 else (YELLOW if v <= 2.0 else RED)

def color_interest(v):
    if v is None: return None
    return GREEN if v > 10 else (YELLOW if v >= 5 else (YELLOW if v >= 3 else RED))

def color_cur(v):
    if v is None: return None
    return GREEN if v > 2.0 else (YELLOW if v >= 1.5 else (YELLOW if v >= 1.0 else RED))

def color_fcf(v):
    if v is None: return None
    return GREEN if v > 0.20 else (YELLOW if v >= 0.10 else RED)

def color_r40(v):
    if v is None: return None
    return GREEN if v > 40 else (YELLOW if v >= 30 else RED)

def color_peg(v):
    if v is None: return None
    return GREEN if v < 1 else (YELLOW if v <= 2 else RED)

def color_pe(v):
    if v is None: return None
    return GREEN if v < 20 else (YELLOW if v <= 30 else RED)

def color_ps(v):
    if v is None: return None
    return GREEN if v < 3 else (YELLOW if v <= 6 else RED)

# ── Metric definitions ───────────────────────────────────────────────────────

METRICS = [
    {
        "key":   "market_cap",
        "label": "0. Market Cap",
        "desc":  "Total market value of all outstanding shares (Price × Shares Outstanding).",
        "bench": "Informational — no threshold coloring",
        "fmt":   fmt_revenue,
        "color": color_none,
    },
    {
        "key":   "revenue",
        "label": "1. Revenue (TTM)",
        "desc":  "Total revenue over the trailing twelve months. Raw scale indicator.",
        "bench": "Informational — no threshold coloring",
        "fmt":   fmt_revenue,
        "color": color_none,
    },
    {
        "key":   "rev_growth",
        "label": "2. Revenue Growth Rate (YoY)",
        "desc":  "Year-over-year revenue growth from quick metrics or computed from two most recent annual periods.",
        "bench": ">20% → Strong | 10–20% → Solid | <10% → Slow",
        "fmt":   fmt_pct,
        "color": color_rev_growth,
    },
    {
        "key":   "gross_margin",
        "label": "3. Gross Margin",
        "desc":  "(Total Revenue − Cost of Revenue) / Total Revenue (TTM). Measures pricing power after direct costs.",
        "bench": ">60% → High quality | 40–60% → Decent | <40% → Watch for pricing pressure",
        "fmt":   fmt_pct,
        "color": color_gm,
    },
    {
        "key":   "op_margin",
        "label": "4. Operating Margin",
        "desc":  "Operating Income (TTM) / Total Revenue (TTM). Measures profitability from core operations before interest and taxes.",
        "bench": ">30% → Strong pricing power | 15–30% → Decent | <15% → Watch for cost pressure",
        "fmt":   fmt_pct,
        "color": color_op,
    },
    {
        "key":   "ni_margin",
        "label": "5. Net Income Margin",
        "desc":  "Net Income (TTM) / Total Revenue (TTM). Bottom-line profitability after all expenses.",
        "bench": ">20% → Strong | 10–20% → Decent | <10% → Thin",
        "fmt":   fmt_pct,
        "color": color_ni,
    },
    {
        "key":   "roe",
        "label": "6. Return on Equity (ROE)",
        "desc":  "Net Income (TTM) / Stockholders Equity (MRQ). Measures how efficiently management generates profit from shareholders' equity.",
        "bench": "≥20% → Ideal | ≥15% → Good | <15% → Below threshold",
        "fmt":   fmt_pct,
        "color": color_roe,
    },
    {
        "key":   "de",
        "label": "7. Debt-to-Equity (D/E)",
        "desc":  "Total Debt (MRQ) / Stockholders Equity (MRQ). Measures financial leverage and balance sheet risk.",
        "bench": "<0.5 → Very conservative | 0.5–1.0 → Healthy | 1.0–2.0 → Moderate leverage | >2.0 → High risk",
        "fmt":   fmt_ratio,
        "color": color_de,
    },
    {
        "key":   "interest_cov",
        "label": "8. Interest Coverage",
        "desc":  "EBIT (TTM) / Interest Expense (TTM). Measures ability to service debt from operating earnings.",
        "bench": ">10× → Very safe | 5–10× → Adequate | 3–5× → Watch | <3× → At risk",
        "fmt":   lambda v: fmt_num(v) + "×" if v is not None else "N/A",
        "color": color_interest,
    },
    {
        "key":   "cur_ratio",
        "label": "9. Current Ratio",
        "desc":  "Current Assets (MRQ) / Current Liabilities (MRQ). Measures short-term liquidity.",
        "bench": ">2.0 → Very liquid | 1.5–2.0 → Healthy | 1.0–1.5 → Adequate | <1.0 → Potential liquidity risk",
        "fmt":   lambda v: fmt_num(v) if v is not None else "N/A",
        "color": color_cur,
    },
    {
        "key":   "fcf_margin",
        "label": "10. FCF Margin",
        "desc":  "Free Cash Flow (TTM) / Total Revenue (TTM). Measures how much cash a company generates per dollar of revenue after capex.",
        "bench": ">20% → High quality | 10–20% → Solid | <10% → Low",
        "fmt":   fmt_pct,
        "color": color_fcf,
    },
    {
        "key":   "r40",
        "label": "11. Rule of 40",
        "desc":  "Revenue Growth Rate (YoY%) + Operating Margin (TTM%). A benchmark balancing growth and profitability for technology companies.",
        "bench": ">40 → Healthy/investible | 30–40 → Borderline | <30 → Warning zone",
        "fmt":   lambda v: fmt_num(v) if v is not None else "N/A",
        "color": color_r40,
    },
    {
        "key":   "trailing_pe",
        "label": "12a. Trailing P/E",
        "desc":  "Market Price / Trailing Twelve Months EPS. Measures how much investors pay per dollar of past earnings.",
        "bench": "Lower is generally cheaper relative to earnings history",
        "fmt":   lambda v: fmt_num(v) if v is not None else "N/A",
        "color": color_pe,
    },
    {
        "key":   "forward_pe",
        "label": "12b. Forward P/E",
        "desc":  "Market Price / Next Twelve Months EPS Estimate. Measures how much investors pay per dollar of expected earnings.",
        "bench": "Lower forward P/E vs trailing P/E implies expected earnings growth",
        "fmt":   lambda v: fmt_num(v) if v is not None else "N/A",
        "color": color_pe,
    },
    {
        "key":   "peg",
        "label": "12c. PEG Ratio",
        "desc":  "Trailing P/E / Earnings Growth Rate. Adjusts the P/E ratio for expected growth to identify relative over/undervaluation.",
        "bench": "PEG <1 → Potentially undervalued | PEG 1–2 → Fair | PEG >2 → Expensive relative to growth",
        "fmt":   lambda v: fmt_num(v) if v is not None else "N/A",
        "color": color_peg,
    },
    {
        "key":   "price_to_sales",
        "label": "12d. Price / Sales (TTM)",
        "desc":  "Market Cap / Total Revenue (TTM). Useful for comparing companies with low or no earnings; lower is generally cheaper.",
        "bench": "<3 → Cheap | 3–6 → Fair | >6 → Expensive",
        "fmt":   lambda v: fmt_num(v) if v is not None else "N/A",
        "color": color_ps,
    },
]

# ── Sheet writers ─────────────────────────────────────────────────────────────

def write_ticker_sheet(wb, ticker, metrics):
    ws = wb.create_sheet(title=ticker)
    ws.column_dimensions["A"].width = 30
    ws.column_dimensions["B"].width = 14
    ws.column_dimensions["C"].width = 42

    ws.cell(row=1, column=1, value=f"{ticker} — Key Stock Metrics").font = Font(bold=True, size=13)
    ws.append([])

    HDR_FILL = PatternFill("solid", fgColor="1F3864")
    HDR_FONT = Font(bold=True, color="FFFFFF")
    for col, heading in enumerate(["Metric", "Value", "Comment"], start=1):
        c = ws.cell(row=3, column=col, value=heading)
        c.font = HDR_FONT
        c.fill = HDR_FILL
        c.alignment = Alignment(horizontal="center")

    for row, m in enumerate(METRICS, start=4):
        val = metrics.get(m["key"])
        val_str = m["fmt"](val)
        fill = m["color"](val)
        comment = _short_comment(m["key"], val)

        ws.cell(row=row, column=1, value=m["label"]).font = BOLD
        val_cell = ws.cell(row=row, column=2, value=val_str)
        val_cell.alignment = Alignment(horizontal="center")
        if fill:
            val_cell.fill = fill
        ws.cell(row=row, column=3, value=comment).font = SM


def _short_comment(key, val):
    if val is None:
        return ""
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
        if val < 0.5:  return "Very conservative (<50%)"
        if val <= 1.0: return "Healthy (50%–100%)"
        if val <= 2.0: return "Moderate leverage (100%–200%)"
        return "High risk (>200%)"
    if key == "interest_cov":
        if val > 10: return "Very safe (>10×)"
        if val >= 5: return "Adequate (5–10×)"
        if val >= 3: return "Watch (3–5×)"
        return "At risk (<3×)"
    if key == "cur_ratio":
        if val > 2.0:  return "Very liquid (>2.0)"
        if val >= 1.5: return "Healthy (1.5–2.0)"
        if val >= 1.0: return "Adequate (1.0–1.5)"
        return "Potential liquidity risk (<1.0)"
    if key == "fcf_margin":
        if val > 0.20:  return "High quality (>20%)"
        if val >= 0.10: return "Solid (10–20%)"
        return "Low (<10%)"
    if key == "r40":
        if val > 40:  return "Healthy / investible (>40)"
        if val >= 30: return "Borderline (30–40)"
        return "Warning zone (<30)"
    if key == "peg":
        if val < 1:  return "Potentially undervalued (PEG<1)"
        if val <= 2: return "Fair (PEG 1–2)"
        return "Expensive relative to growth (PEG>2)"
    return ""


def write_comparison_sheet(wb, tickers, all_metrics):
    ws = wb.create_sheet(title="Comparison")
    wb.move_sheet(ws, offset=-(len(wb.sheetnames) - 1))

    HDR_FILL = PatternFill("solid", fgColor="1F3864")
    HDR_FONT = Font(bold=True, color="FFFFFF")

    ws.column_dimensions["A"].width = 28
    for col, _ in enumerate(tickers, start=2):
        ws.column_dimensions[get_column_letter(col)].width = 12

    # ── Part 1: Comparison table ──────────────────────────────────────────────
    ws.cell(row=1, column=1, value="Metric").font = HDR_FONT
    ws.cell(row=1, column=1).fill = HDR_FILL
    ws.cell(row=1, column=1).alignment = Alignment(horizontal="center")
    for col, ticker in enumerate(tickers, start=2):
        c = ws.cell(row=1, column=col, value=ticker)
        c.font = HDR_FONT
        c.fill = HDR_FILL
        c.alignment = Alignment(horizontal="center")

    for r, m in enumerate(METRICS, start=2):
        ws.cell(row=r, column=1, value=m["label"]).font = BOLD
        for col, ticker in enumerate(tickers, start=2):
            val = all_metrics[ticker].get(m["key"])
            cell = ws.cell(row=r, column=col, value=m["fmt"](val))
            cell.alignment = Alignment(horizontal="center")
            fill = m["color"](val)
            if fill:
                cell.fill = fill

    # ── Part 2: Metric descriptions & benchmarks ──────────────────────────────
    desc_start = len(METRICS) + 3
    ws.cell(row=desc_start, column=1, value="Metric Descriptions & Benchmarks").font = Font(bold=True, size=12)

    row = desc_start + 2
    for m in METRICS:
        ws.cell(row=row, column=1, value=m["label"]).font = BOLD
        ws.cell(row=row+1, column=1, value=f"{INDENT}Description:").font = ITALIC_SM
        ws.cell(row=row+1, column=2, value=m["desc"]).font = SM
        ws.cell(row=row+2, column=1, value=f"{INDENT}Benchmarks:").font = ITALIC_SM
        ws.cell(row=row+2, column=2, value=m["bench"]).font = SM
        row += 4


# ── Entry point ───────────────────────────────────────────────────────────────

def main(tickers):
    all_metrics = {}
    for t in tickers:
        print(f"Computing metrics for {t}...")
        all_metrics[t] = compute_metrics(t)

    wb = Workbook()
    wb.remove(wb.active)

    for t in tickers:
        write_ticker_sheet(wb, t, all_metrics[t])

    write_comparison_sheet(wb, tickers, all_metrics)

    out = f"Outputs/key_stock_metrics_{date.today().strftime('%Y%m%d')}.xlsx"
    wb.save(out)
    print(f"Saved: {out}")
    return out


if __name__ == "__main__":
    if len(sys.argv) > 1:
        tickers = [t.upper() for t in sys.argv[1:]]
    else:
        sys.path.insert(0, ".")
        from yahoo_finance_data import load_tickers
        tickers = load_tickers()
    main(tickers)
