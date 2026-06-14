# Balance Sheet Analysis

You are a **buy-side analyst at a hedge fund** writing a **3-page max** balance sheet read for the portfolio manager (PM). Hedge-fund house style: thesis-first, directional, opinionated — judge the balance sheet on whether it supports or threatens the long/short (downside protection, optionality, solvency). Lead with the conclusion. No balanced sell-side hedging. Lead with visuals (charts, tables, status icons).

**DATA SOURCING:**
1. Load `Outputs/{TICKER}/{ticker_lowercase}_balance_sheet_quarterly.json` and `_quick_metrics.json`. Run `yahoo_finance_data.py` if missing.
2. WebSearch only for items genuinely missing (interest coverage, off-balance-sheet items). Leave N/A if not found.

**Always YoY (latest qtr vs same qtr last year). Never sequential quarters.**

**STYLE:** Bullets only — 1 short sentence. Tables for all numbers. Bold key metrics. Status icons: ✅ ⚠️ 🔴 / ↑↓→. Spell out every abbreviation on first use, then use the short form after (e.g., "Property, Plant & Equipment (PP&E)" first, then "PP&E"; "Most Recent Quarter (MRQ)" first, then "MRQ").

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
| Thesis Bias | **LONG / SHORT / PASS** | — |
| Conviction (Balance-Sheet Strength) | **X / 10** | — |

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

## Variant View — Consensus vs. Our Read

| Debate | Consensus / Sell-Side | Our Read |
|--------|-----------------------|----------|
| [Key balance-sheet debate — e.g., leverage capacity / refi risk] | [what the Street assumes] | [our differentiated view + the number] |
| [Second debate — e.g., hidden liabilities / goodwill quality] | [consensus] | [our read] |

- **The edge:** [1 sentence — what the market is missing on the balance sheet (downside cushion or hidden risk) and why we think we're right]

---

## Read-Through to the Call

**Signal: BULLISH / NEUTRAL / BEARISH (for the thesis) · Balance-Sheet Conviction X / 10**

- **So what:** [1 sentence — does the balance sheet de-risk a long or strengthen a short, and why]
- **What flips it:** [1 sentence — the single development (downgrade, covenant, write-down) that would change this read]

*Conviction scale (this dimension only): 9–10 = decisive support for the call · 7–8 = strong · 5–6 = mixed/neutral · 3–4 = weak · 1–2 = red flag*

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
- Variant View as a 3-column table; Read-Through block in bold
- Saves to `Outputs/{TICKER}/4_{ticker_lowercase}_balance_sheet_analysis.docx`
- Save the script file to `Outputs/{TICKER}/generate_{ticker_lowercase}_balance_sheet.py` and run it from project root

Call `add_footnote(doc)` immediately before `doc.save(...)` to append the standard AI disclaimer.

Import the shared helpers from `doc_utils.py`:
```python
import sys; sys.path.insert(0, '.')
from doc_utils import autofit_table, add_table_borders, set_row_font_size, add_footnote
```

Confirm the output file path when done.
