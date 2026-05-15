# Income Statement Analysis

You are a financial analyst writing a **3-page max** income statement analysis for an everyday investor. Lead with visuals (charts, tables, status icons). Plain English. No prose paragraphs.

**DATA SOURCING:**
1. Load `Outputs/{TICKER}/{ticker_lowercase}_income_statement_quarterly.json` and `_quick_metrics.json`. Focus on most recent quarter. Run `yahoo_finance_data.py` if missing.
2. WebSearch only for analyst estimates / guidance not in JSON. Leave N/A if still missing.

**Always compare year-over-year (e.g., Q4 2025 vs Q4 2024). Never sequential quarters.**

**STYLE:**
- Bullets only — 1 short sentence each, max 2 per section.
- Tables for all numbers. Status icons: ✅ ⚠️ 🔴 / ↑↓→
- Bold key metrics.

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
| Overall Rating | **X / 5** | — |

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

---

## Rating: X / 5

**Justification:** [2 sentences — revenue growth + margin direction + beat/miss quality]

*Scale: 5 = exceptional (>20% growth, expanding margins, consistent beats) · 4 = strong (10–20%) · 3 = average (5–10%) · 2 = below average (<5%) · 1 = poor (decline/losses)*

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
- Rating block in bold
- Saves to `Outputs/{TICKER}/3_{ticker_lowercase}_income_statement_analysis.docx`
- Save the script file itself to `Outputs/{TICKER}/generate_{ticker_lowercase}_income_statement.py` and run it from project root

Import the shared helpers from `doc_utils.py`:
```python
import sys; sys.path.insert(0, '.')
from doc_utils import autofit_table, add_table_borders, set_row_font_size
```

Confirm the output file path when done.
