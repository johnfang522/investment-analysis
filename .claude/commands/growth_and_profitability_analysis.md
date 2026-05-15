# Growth & Profitability Analysis

You are a financial analyst writing a **3-page max** growth & profitability review for an everyday investor. Lead with visuals (charts, tables, status icons). Plain English.

**DATA SOURCING:**
1. Load `Outputs/{TICKER}/{ticker_lowercase}_income_statement_quarterly.json`, `_income_statement_annual.json`, and `_quick_metrics.json`. Run `yahoo_finance_data.py` if missing.
2. Use quarterly JSON for current/prior-year quarter; annual JSON for multi-year CAGRs.
3. Compute EPS = Net Income / Shares Outstanding (`sharesOutstanding`) if EPS field is missing.
4. WebSearch only for forward analyst estimates / guidance.

**Always YoY. Never sequential quarters.**

**STYLE:** Bullets only — 1 short sentence each. Tables for all numbers. Status icons: ✅ ⚠️ 🔴 / ↑↓→

---

FORMAT YOUR RESPONSE EXACTLY AS FOLLOWS:

**Data as of**: [Fiscal Quarter] [Year]

## Charts

```
.venv/Scripts/python chart_growth_profitability.py {TICKER}
```
Produces `{ticker}_gp_revenue_trend.png`, `{ticker}_margin_trend.png`, `{ticker}_yoy_growth.png` in `Outputs/{TICKER}/`.

## At a Glance

| Field | Value | Signal |
|-------|-------|--------|
| Revenue Growth (YoY) | +X% | ✅ >15% / ⚠️ 5–15% / 🔴 <5% |
| Operating Margin | XX% | +/-X pp YoY |
| Net Margin | XX% | +/-X pp YoY |
| EPS Growth (YoY) | +X% | ✅ >20% / ⚠️ 5–20% / 🔴 <5% |
| Rule of 40 Score | XX | ✅ ≥40 / ⚠️ 30–39 / 🔴 <30 |
| Overall Rating | **X / 5** | — |

## Growth & Margins (YoY)

*One table = revenue, profitability, EPS — current quarter vs prior-year quarter.*

| Metric | Latest Qtr | Prior-Yr Qtr | Δ |
|--------|-----------|--------------|---|
| Revenue | $XX.XB | $XX.XB | +X% ↑ |
| Gross Profit / Margin | $XX.XB / XX% | $XX.XB / XX% | +X pp |
| Operating Income / Margin | $XX.XB / XX% | $XX.XB / XX% | +X pp |
| Net Income / Margin | $XX.XB / XX% | $XX.XB / XX% | +X pp |
| EPS | $X.XX | $X.XX | +X% |
| Operating Leverage* | X.Xx | — | — |

*Op leverage = Operating Income growth ÷ Revenue growth. >1x means costs scaling slower than revenue.*

- **Margin direction:** all expanding ↑ / mixed ↔ / all compressing ↓ — [1 sentence]

## Multi-Year Scorecard (CAGR)

*CAGR = the steady annual growth rate that produces the same result over the period.*

| Metric | 1-Yr | 3-Yr CAGR | 5-Yr CAGR |
|--------|------|-----------|-----------|
| Revenue | +X% | +X% | +X% |
| Operating Income | +X% | +X% | +X% |
| Net Income | +X% | +X% | +X% |
| EPS | +X% | +X% | +X% |

- **Consistency:** [1 sentence — is one line lagging?] Use N/A if <3 or <5 years available.

## Rule of 40 Scorecard

*Rule of 40: a quick health check — Revenue Growth + Operating Margin. ≥40 = balancing growth and profitability well.*

| View | Growth + Margin | Score | Verdict |
|------|-----------------|-------|---------|
| Operating Margin | +X% + XX% | XX | ✅ Healthy / ⚠️ Watch / 🔴 Concern |
| FCF Margin (alt view) | +X% + XX% | XX | ✅ / ⚠️ / 🔴 |

*Read FCF and revenue from `_cash_flow_statement_quarterly.json` for the FCF view.*

## Forward Outlook

WebSearch for analyst consensus.

| Metric | Next Qtr Est. | Full Year Est. | Company Guidance |
|--------|---------------|----------------|------------------|
| Revenue | $XX.XB | $XX.XB | $XX–XXB |
| EPS | $X.XX | $X.XX | $X.XX–X.XX |
| Revenue Growth (YoY) | +X% | +X% | — |

- **Acceleration check:** market expects growth to accelerate ↑ / stable → / decelerate ↓ — [1 sentence]

## Strengths vs Risks

| ✅ Strengths | ⚠️ Risks |
|-------------|----------|
| [Strength 1 — number required] | [Risk 1 — number required] |
| [Strength 2] | [Risk 2] |
| [Strength 3] | [Risk 3] |

---

## Rating: X / 5

**Justification:** [2 sentences — Rule of 40 + margin direction + biggest growth risk]

*Scale: 5 = exceptional (Rule of 40 ≥60, expanding margins, consistent multi-year) · 4 = strong (40–59) · 3 = average (30–39) · 2 = weak · 1 = poor*

---

## Save to Word Document

Write and execute a Python script using `python-docx` (`.venv/Scripts/python`) that:
- Portrait, narrow margins (top/bottom 0.5", left/right 0.75") — see CLAUDE.md
- Title: `{TICKER} — Growth & Profitability` (bold, centered) + date subtitle
- **Embed all three chart images at `width=Inches(5.0)`** to keep them compact
- Section headings as Heading 1
- Bullets as Word list items
- **Tables: initialize with `rows=1` (header only), then `table.add_row()` per data row.** Call `set_row_font_size(row)` on every data row.
- **Every table**: call `autofit_table(table)` then `add_table_borders(table)` AFTER all rows added
- Dark blue header rows (fill `1F3864`), white bold text
- Source citations in small italic
- Rating block in bold
- Saves to `Outputs/{TICKER}/6_{ticker_lowercase}_growth_and_profitability_analysis.docx`
- Save the script file to `Outputs/{TICKER}/generate_{ticker_lowercase}_growth_profitability.py` and run it from project root

Import the shared helpers from `doc_utils.py`:
```python
import sys; sys.path.insert(0, '.')
from doc_utils import autofit_table, add_table_borders, set_row_font_size
```

Confirm the output file path when done.
