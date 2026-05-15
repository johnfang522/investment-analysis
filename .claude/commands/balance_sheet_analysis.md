# Balance Sheet Analysis

You are a financial analyst writing a **3-page max** balance sheet review for an everyday investor. Lead with visuals (charts, tables, status icons). Plain English.

**DATA SOURCING:**
1. Load `Outputs/{TICKER}/{ticker_lowercase}_balance_sheet_quarterly.json` and `_quick_metrics.json`. Run `yahoo_finance_data.py` if missing.
2. WebSearch only for items genuinely missing (interest coverage, off-balance-sheet items). Leave N/A if not found.

**Always YoY (latest qtr vs same qtr last year). Never sequential quarters.**

**STYLE:** Bullets only — 1 short sentence. Tables for all numbers. Bold key metrics. Status icons: ✅ ⚠️ 🔴 / ↑↓→

---

FORMAT YOUR RESPONSE EXACTLY AS FOLLOWS:

**Data as of**: [Fiscal Quarter] [Year]

## Charts

```
.venv/Scripts/python chart_balance_sheet.py {TICKER}
```
Produces `{ticker}_balance_sheet_composition.png` and `{ticker}_balance_sheet_trend.png` in `Outputs/{TICKER}/`.

## At a Glance

| Field | Value | Signal |
|-------|-------|--------|
| Total Assets | $XX.XB | +X% YoY ↑/↓ |
| Net Cash / (Net Debt) | $X.XB | ✅ Net Cash / ⚠️ Manageable / 🔴 Heavy Debt |
| Current Ratio | X.Xx | ✅ >1.5 / ⚠️ 1–1.5 / 🔴 <1 |
| Debt / Equity | X.Xx | ✅ <0.5 / ⚠️ 0.5–1.5 / 🔴 >1.5 |
| Interest Coverage | X.Xx | ✅ >5 / ⚠️ 2–5 / 🔴 <2 |
| Overall Rating | **X / 5** | — |

## Balance Sheet Snapshot (YoY)

*One table = key asset, liability, and equity lines, current quarter vs prior-year quarter.*

| Line Item | Latest Qtr | Prior-Yr Qtr | Δ |
|-----------|-----------|--------------|---|
| Total Assets | $XX.XB | $XX.XB | +X% ↑ |
| Cash & Equivalents | $XX.XB | $XX.XB | +X% |
| PP&E (net) | $XX.XB | $XX.XB | +X% |
| Goodwill & Intangibles | $XX.XB | $XX.XB | +X% |
| Total Debt | $XX.XB | $XX.XB | +X% |
| Current Liabilities | $XX.XB | $XX.XB | +X% |
| Total Equity | $XX.XB | $XX.XB | +X% |

- **Biggest YoY shift:** [1 sentence — what changed and why]

## Liquidity & Leverage

*Liquidity = can it pay near-term bills. Leverage = how much it relies on borrowed money.*

| Ratio | Latest | Prior-Yr | Plain English |
|-------|--------|----------|---------------|
| Current Ratio | X.Xx | X.Xx | Short-term assets vs short-term bills |
| Quick Ratio | X.Xx | X.Xx | Same, excluding inventory |
| Cash Ratio | X.Xx | X.Xx | Cash alone vs short-term bills |
| Debt / Equity | X.Xx | X.Xx | Debt size vs shareholder capital |
| Interest Coverage | X.Xx | X.Xx | Operating profit ÷ interest |
| Net Debt / EBITDA | X.Xx | X.Xx | Years of profit to repay all debt |

- **Trend:** liquidity improving ↑ / steady → / tightening ↓ — [1 sentence]

## Hidden Risks

WebSearch: "{TICKER} operating leases contingent liabilities [year]"
- Material off-balance items (leases, lawsuits, pensions, purchase commitments). If none: "No significant off-balance-sheet concerns identified."

## Strengths vs Risks

| ✅ Strengths | ⚠️ Risks |
|-------------|----------|
| [e.g., Net cash of $X.XB — fortress balance sheet] | [e.g., Goodwill $X.XB — write-down risk if M&A underperforms] |
| [Strength 2] | [Risk 2] |
| [Strength 3] | [Risk 3] |

---

## Rating: X / 5

**Justification:** [2 sentences — net cash/debt position + key ratios + biggest single risk]

*Scale: 5 = fortress (net cash, current >2x, low debt) · 4 = healthy · 3 = adequate · 2 = stretched · 1 = distressed*

---

## Save to Word Document

Write and execute a Python script using `python-docx` (`.venv/Scripts/python`) that:
- Portrait, narrow margins (top/bottom 0.5", left/right 0.75") — see CLAUDE.md
- Title: `{TICKER} — Balance Sheet` (bold, centered) + date subtitle
- **Embed both chart images at `width=Inches(7.0)`** to fill the full text width
- Section headings as Heading 1
- Bullets as Word list items
- **Tables: initialize with `rows=1` (header only), then `table.add_row()` per data row.** Call `set_row_font_size(row)` on every data row.
- **Every table**: call `autofit_table(table)` then `add_table_borders(table)` AFTER all rows added
- Dark blue header rows (fill `1F3864`), white bold text
- Source citations in small italic
- Rating block in bold
- Saves to `Outputs/{TICKER}/4_{ticker_lowercase}_balance_sheet_analysis.docx`
- Save the script file to `Outputs/{TICKER}/generate_{ticker_lowercase}_balance_sheet.py` and run it from project root

Import the shared helpers from `doc_utils.py`:
```python
import sys; sys.path.insert(0, '.')
from doc_utils import autofit_table, add_table_borders, set_row_font_size
```

Confirm the output file path when done.
