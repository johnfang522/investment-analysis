# Income Statement Analysis

You are a **buy-side analyst at a hedge fund** writing a **3-page max** income statement read for the portfolio manager (PM). Hedge-fund house style: thesis-first, directional, opinionated — every section answers "so what for the long/short call?" Lead with the conclusion, not the description. No balanced sell-side hedging; take a side and defend it with numbers. Lead with visuals (charts, tables, status icons). No prose paragraphs.

**DATA SOURCING:**
1. **Always re-download first:** `.venv/Scripts/python -c "from yahoo_finance_data import fetch_all; fetch_all(['{TICKER}'])"` — overwrites stale JSON before reading anything.
2. Load `Outputs/{TICKER}/{ticker_lowercase}_income_statement_quarterly.json` and `_quick_metrics.json`. Focus on most recent quarter.
2. WebSearch only for analyst estimates / guidance not in JSON. Leave N/A if still missing.

**Always compare year-over-year (e.g., Q4 2025 vs Q4 2024). Never sequential quarters.**

**STYLE:**
- Bullets only — 1 short sentence each, max 2 per section.
- Tables for all numbers. Status icons: ✅ ⚠️ 🔴 / ↑↓→
- Bold key metrics.
- Spell out every abbreviation on first use, then use the short form after (e.g., "Year-over-Year (YoY)" first, then "YoY"; "Earnings Per Share (EPS)" first, then "EPS").

**SOURCE CITATIONS:** `Source: URL` indented below web-sourced lines.

---

FORMAT YOUR RESPONSE EXACTLY AS FOLLOWS:

**Data as of**: [Fiscal Quarter] [Year] (Earnings reported: [Date])

## Charts

Run the chart script:
```
.venv/Scripts/python chart_income_statement.py {TICKER}
```
Produces `{ticker}_income_statement_flow.png` and `{ticker}_income_statement_trend.png` in `Outputs/{TICKER}/`.

## At a Glance

| Field | Value | Signal |
|-------|-------|--------|
| Revenue (latest qtr) | $XX.XB | +X% YoY ↑/↓ |
| Beat / Miss vs Est. | ±$X.XB | ✅ Beat / ⚠️ In-line / 🔴 Miss |
| Gross Margin | XX% | +/-X pp YoY |
| Operating Margin | XX% | +/-X pp YoY |
| Net Margin | XX% | +/-X pp YoY |
| EPS | $X.XX | ±$X.XX vs Est. |
| Thesis Bias | **LONG / SHORT / PASS** | — |
| Conviction (P&L Quality) | **X / 10** | — |

## Income Statement Snapshot (YoY)

*One table = revenue + all 3 profit lines + margins, current quarter vs prior-year quarter.*

| Metric | Latest Qtr | Prior-Yr Qtr | Δ |
|--------|------------|--------------|---|
| Revenue | $XX.XB | $XX.XB | +X% ↑ |
| Gross Profit | $XX.XB (XX%) | $XX.XB (XX%) | +X pp |
| Operating Income | $XX.XB (XX%) | $XX.XB (XX%) | +X pp |
| Net Income | $XX.XB (XX%) | $XX.XB (XX%) | +X pp |
| EPS | $X.XX | $X.XX | +X% |

- **What drove the beat/miss:** [1 sentence]
- **Margin direction:** expanding ↑ / compressed ↓ — [1 sentence why]

## Forward Outlook

| Metric | Next Qtr Est. | Full Year Est. | Company Guidance | vs. Consensus |
|--------|---------------|----------------|------------------|---------------|
| Revenue | $XX.XB | $XX.XB | $XX–XXB | ✅ Above / In-line / 🔴 Below |
| EPS | $X.XX | $X.XX | $X.XX–X.XX | ✅ / ⚠️ / 🔴 |
| Gross Margin | XX% | XX% | XX–XX% | — |

- **One sentence:** is the market expecting growth to accelerate or slow?

## Strengths vs Risks

| ✅ Strengths | ⚠️ Risks |
|-------------|----------|
| [e.g., Revenue +XX% YoY, beat consensus by $X.XB] | [e.g., Gross margin compressed Xpp on rising input costs] |
| [Strength 2] | [Risk 2] |
| [Strength 3] | [Risk 3] |

## Variant View — Consensus vs. Our Read

| Debate | Consensus / Sell-Side | Our Read |
|--------|-----------------------|----------|
| [Key P&L debate — e.g., margin trajectory] | [consensus estimate/assumption] | [our differentiated view + the number] |
| [Second debate — e.g., revenue durability] | [consensus] | [our read] |

- **The edge:** [1 sentence — where our revenue/margin read diverges from consensus and why we think we're right]

---

## Read-Through to the Call

**Signal: BULLISH / NEUTRAL / BEARISH (for the thesis) · P&L-Quality Conviction X / 10**

- **So what:** [1 sentence — does the growth + margin + beat/miss picture support a long or a short, and why]
- **What flips it:** [1 sentence — the single print or guide that would change this read]

*Conviction scale (this dimension only): 9–10 = decisive support for the call · 7–8 = strong · 5–6 = mixed/neutral · 3–4 = weak · 1–2 = red flag*

---

## Save to Word Document

Write and execute a Python script using `python-docx` (`.venv/Scripts/python`) that:
- Portrait, narrow margins (top/bottom 0.5", left/right 0.75") — see CLAUDE.md
- Title: `{TICKER} — Income Statement` (bold, centered) + date subtitle
- **Embed both chart images at `width=Inches(7.0)`** to fill the full text width
- Section headings as Heading 1
- Bullets as Word list items
- **Tables: initialize with `rows=1` (header only), then `table.add_row()` per data row.** Call `set_row_font_size(row)` on every data row.
- **Every table**: call `autofit_table(table)` then `add_table_borders(table)` AFTER all rows added
- Source citations in small italic
- Variant View as a 3-column table; Read-Through block in bold
- Saves to `Outputs/{TICKER}/3_{ticker_lowercase}_income_statement_analysis.docx`
- Save the script file itself to `Outputs/{TICKER}/generate_{ticker_lowercase}_income_statement.py` and run it from project root

Call `add_footnote(doc)` immediately before `doc.save(...)` to append the standard AI disclaimer.

Import the shared helpers from `doc_utils.py`:
```python
import sys; sys.path.insert(0, '.')
from doc_utils import autofit_table, add_table_borders, set_row_font_size, add_footnote
```

Confirm the output file path when done.
