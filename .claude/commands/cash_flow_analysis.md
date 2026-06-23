# Cash Flow Analysis

You are a **buy-side analyst at a hedge fund** writing a **3-page max** cash flow read for the portfolio manager (PM). Hedge-fund house style: thesis-first, directional, opinionated — judge cash generation and capital allocation on whether they support the long/short (FCF quality, self-funding, earnings-to-cash conversion). Lead with the conclusion. No balanced sell-side hedging. Lead with visuals (charts, tables, status icons).

**DATA SOURCING:**
1. **Always re-download first:** `.venv/Scripts/python -c "from yahoo_finance_data import fetch_all; fetch_all(['{TICKER}'])"` — overwrites stale JSON before reading anything.
2. Load `Outputs/{TICKER}/{ticker_lowercase}_cash_flow_statement_quarterly.json` and `_quick_metrics.json`.
3. WebSearch only for items genuinely missing (interest expense, dividend totals). Leave N/A if not found.

**Always YoY. Never sequential quarters.**

**STYLE:** Bullets only — 1 short sentence each. Tables for all numbers. Status icons: ✅ ⚠️ 🔴 / ↑↓→. Spell out every abbreviation on first use, then use the short form after (e.g., "Operating Cash Flow (OCF)" first, then "OCF"; "Free Cash Flow (FCF)" first, then "FCF"; "Capital Expenditures (CapEx)" first, then "CapEx").

---

FORMAT YOUR RESPONSE EXACTLY AS FOLLOWS:

**Data as of**: [Fiscal Quarter] [Year]

## Charts

```
.venv/Scripts/python chart_cash_flow.py {TICKER}
```
Produces `{ticker}_cash_flow_waterfall.png` and `{ticker}_cash_flow_trend.png` in `Outputs/{TICKER}/`.

## At a Glance

| Field | Value | Signal |
|-------|-------|--------|
| Operating Cash Flow | $X.XB | +X% YoY ↑/↓ |
| Free Cash Flow | $X.XB | +X% YoY ↑/↓ |
| FCF Margin | XX% | ✅ >15% / ⚠️ 5–15% / 🔴 <5% |
| FCF Conversion (FCF ÷ NI) | X.Xx | ✅ >1 / ⚠️ ~1 / 🔴 <1 |
| Capital Allocation Bias | Buybacks / Dividends / M&A / Reinvest | — |
| Thesis Bias | **LONG / SHORT / PASS** | — |
| Conviction (Cash-Flow Quality) | **X / 10** | — |

## Cash Flow Snapshot (YoY)

*One table = OCF, FCF, CapEx and the key margins, current quarter vs prior-year quarter.*

| Metric | Latest Qtr | Prior-Yr Qtr | Δ |
|--------|-----------|--------------|---|
| Operating Cash Flow | $X.XB | $X.XB | +X% ↑ |
| OCF Margin | XX% | XX% | +X pp |
| CapEx | $X.XB | $X.XB | +X% |
| Free Cash Flow | $X.XB | $X.XB | +X% |
| FCF Margin | XX% | XX% | +X pp |
| FCF / Net Income | X.Xx | X.Xx | — |

- **What drove the change:** [1 sentence — working capital, CapEx surge, etc.]

## Capital Allocation


| Use of Cash | Latest Qtr | Prior-Yr Qtr | Δ |
|-------------|-----------|--------------|---|
| CapEx | $X.XB | $X.XB | +X% |
| Buybacks | $X.XB | $X.XB | +X% |
| Dividends | $X.XB | $X.XB | +X% |
| Debt Repayment | $X.XB | $X.XB | +X% |

- **Red flag check:** [e.g., "Buybacks rising while debt grows" — or "None identified"]

## Financial Safety

| Coverage Ratio | Latest | Plain English |
|----------------|--------|---------------|
| Interest Coverage (OCF ÷ interest) | X.Xx | Higher = safer |
| Dividend Coverage (FCF ÷ dividends) | X.Xx | >1 means dividend covered |
| Debt Coverage (OCF ÷ total debt) | X.Xx | Years to repay all debt from OCF |

- **Could the company self-fund through a bad year?** Yes / Tight / No — [1 sentence]

## Strengths vs Risks

| ✅ Strengths | ⚠️ Risks |
|-------------|----------|
| [e.g., FCF $X.XB at XX% margin — ahead of net income] | [e.g., CapEx +XX% YoY pressuring FCF margin] |
| [Strength 2] | [Risk 2] |
| [Strength 3] | [Risk 3] |

## Variant View — Consensus vs. Our Read

| Debate | Consensus / Sell-Side | Our Read |
|--------|-----------------------|----------|
| [Key cash-flow debate — e.g., FCF durability vs. capex cycle] | [what the Street assumes] | [our differentiated view + the number] |
| [Second debate — e.g., earnings quality / conversion] | [consensus] | [our read] |

- **The edge:** [1 sentence — where our cash-conversion read diverges from consensus and why we think we're right]

---

## Read-Through to the Call

**Signal: BULLISH / NEUTRAL / BEARISH (for the thesis) · Cash-Flow-Quality Conviction X / 10**

- **So what:** [1 sentence — does FCF generation + allocation support a long or a short, and why]
- **What flips it:** [1 sentence — the single development (capex surge, FCF miss, buyback halt) that would change this read]

*Conviction scale (this dimension only): 9–10 = decisive support for the call · 7–8 = strong · 5–6 = mixed/neutral · 3–4 = weak · 1–2 = red flag*

---

## Save to Word Document

Write and execute a Python script using `python-docx` (`.venv/Scripts/python`) that:
- Portrait, narrow margins (top/bottom 0.5", left/right 0.75") — see CLAUDE.md
- Title: `{TICKER} — Cash Flow` (bold, centered) + date subtitle
- **Embed both chart images at `width=Inches(7.0)`** to fill the full text width
- Section headings as Heading 1
- Bullets as Word list items
- **Tables: initialize with `rows=1` (header only), then `table.add_row()` per data row.** Call `set_row_font_size(row)` on every data row.
- **Every table**: call `autofit_table(table)` then `add_table_borders(table)` AFTER all rows added
- Dark blue header rows (fill `1F3864`), white bold text
- Source citations in small italic
- Variant View as a 3-column table; Read-Through block in bold
- Saves to `Outputs/{TICKER}/5_{ticker_lowercase}_cash_flow_analysis.docx`
- Save the script file to `Outputs/{TICKER}/generate_{ticker_lowercase}_cash_flow.py` and run it from project root

Call `add_footnote(doc)` immediately before `doc.save(...)` to append the standard AI disclaimer.

Import the shared helpers from `doc_utils.py`:
```python
import sys; sys.path.insert(0, '.')
from doc_utils import autofit_table, add_table_borders, set_row_font_size, add_footnote, fmt_value
```
Use `fmt_value(v)` for all dollar amounts in table cells (auto-scales: ≥$1B → `$X.XXB`, ≥$1M → `$X.XM`, ≥$1K → `$X.XK`). Never hardcode `/ 1e9` or manually append `"B"`.

Confirm the output file path when done.
