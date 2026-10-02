# Balance Sheet Analysis

You are a **buy-side analyst at a hedge fund** writing a **3-page max** balance sheet read for the portfolio manager (PM). Hedge-fund house style: thesis-first, directional, opinionated — judge the balance sheet on whether it supports or threatens the long/short (downside protection, optionality, solvency). Lead with the conclusion. No balanced sell-side hedging. Lead with visuals (charts, tables, status icons).

**DATA SOURCING:**
1. **Always re-download first:** `.venv/Scripts/python -c "from get_financial_data import fetch_all; fetch_all(['{TICKER}'], price_history=False)"` — overwrites stale JSON before reading anything (`price_history=False`: this skill never reads price history, so it is not downloaded.). **If invoked by `/single_stock_deep_research`, skip this download — the parent already downloaded all data once at its start.**
2. Load `Outputs/{TICKER}/{ticker_lowercase}_balance_sheet_quarterly.json` and `_quick_metrics.json`.
3. WebSearch only for items genuinely missing (interest coverage; all off-balance-sheet items — see the OBS Analysis section, which requires 10-K/10-Q footnote research). Leave N/A if not found.

**Always YoY (latest qtr vs same qtr last year). Never sequential quarters.**

**STYLE:** Bullets only — 1 short sentence. Tables for all numbers. Bold key metrics. Status icons: ✅ ⚠️ 🔴 / ↑↓→. Spell out every abbreviation on first use, then use the short form after (e.g., "Property, Plant & Equipment (PP&E)" first, then "PP&E"; "Most Recent Quarter (MRQ)" first, then "MRQ").

**REIT HANDLING (apply only if the company is a REIT — definitions and data sources in `references/reit-framework.md`):**
- Detect: `_quick_metrics.json` `industry` starts with `REIT` (or `sector` is `Real Estate`). Equity REITs follow this block; mortgage REITs (`REIT - Mortgage`) are financials, so flag it and use book value, price/book and net interest spread instead. Not a REIT: ignore this block.
- Keep every section above. Add REIT leverage and liquidity metrics: **net debt / annualized adjusted EBITDAre**, fixed-charge coverage, debt maturity ladder, weighted-average maturity and rate, fixed vs floating share, unsecured vs secured mix, liquidity (cash + undrawn revolver), and credit ratings (cite source and date).
- Current, quick and cash ratios and generic Debt/Equity do not apply to an unclassified REIT balance sheet: show them as N/A or "not meaningful" and lead with the REIT measures. Compute interest coverage on an EBITDAre basis, not GAAP operating income.
- SEC EDGAR `Total Debt` is frequently untagged for REITs: sum notes payable, term loans, credit facility and mortgages from the latest 10-Q balance sheet and state which figure you used.
- In the Off-Balance-Sheet section pay particular attention to unconsolidated joint ventures and funds (equity-method stakes, pro-rata debt, any guarantees), ground leases where the REIT is lessee, forward equity agreements and development/purchase commitments, and note large goodwill/lease intangibles after mergers.

---

FORMAT YOUR RESPONSE EXACTLY AS FOLLOWS:

**Data as of**: [Fiscal Quarter] [Year]

## Charts

```
.venv/Scripts/python chart_balance_sheet.py {TICKER}
```
Produces in `Outputs/{TICKER}/`:
- `{ticker}_balance_sheet_composition.png` — latest-quarter stacked bars: assets (current / non-current) vs. funding (current liabilities, long-term debt, other long-term liabilities, equity)
- `{ticker}_balance_sheet_trend.png` — **grouped bars, not lines**: total assets, total equity, total liabilities, total debt and cash for each of the **last 8 quarters** (x-axis "Qtr Ended Mon YYYY"), with **every bar labeled** with its amount. Read the leverage and liquidity trend straight off the labels — cash vs. debt direction, liabilities vs. equity growth — and cite those same figures (SEC EDGAR) in the Trend bullet rather than re-deriving them. Total Debt is `0`/blank for filers that don't tag it (see CLAUDE.md); if that bar is missing or looks wrong, fall back to `_quick_metrics.json` or the 10-Q and say so under the chart.

## At a Glance

| Field | Value | Signal |
|-------|-------|--------|
| Total Assets | $XX.XB | +X% YoY ↑/↓ |
| Net Cash / (Net Debt) | $X.XB | ✅ Net Cash / ⚠️ Manageable / 🔴 Heavy Debt |
| Current Ratio | X.Xx | ✅ >1.5 / ⚠️ 1–1.5 / 🔴 <1 |
| Debt / Equity | X.Xx | ✅ <0.5 / ⚠️ 0.5–1.5 / 🔴 >1.5 |
| Interest Coverage | X.Xx | ✅ >5 / ⚠️ 2–5 / 🔴 <2 |
| OBS Risk Score | X / 14 | ✅ 0–3 / ⚠️ 4–7 / 🔴 8+ |
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

## Off-Balance-Sheet (OBS) Analysis

*Forensic layer: what liabilities sit outside reported debt, and what is "true" leverage once they are added back?* SEC EDGAR JSON has no footnote data, so source everything from the latest 10-K/10-Q footnotes via WebSearch (terms: "{TICKER} 10-K commitments and contingencies", "variable interest entity", "operating lease maturity", "pension funded status", "purchase obligations", "guarantees", "equity method investees"). Cite filing + date for every figure. Leave N/A if not found — never guess.

**Score each category 0–2** (0 = none/immaterial ✅ · 1 = present, moderate ⚠️ · 2 = material or structured to stay off-balance-sheet 🔴):

| # | Category | What to check | Finding | Score |
|---|----------|---------------|---------|-------|
| 1 | Leases | Post-ASC 842 (Accounting Standards Codification)/IFRS 16 most operating leases are on-balance-sheet — check lease footnote: total future minimum payments vs. capitalized liability; synthetic leases, sale-leasebacks (retail, airlines, shipping) | [$ / none] | 0–2 |
| 2 | SPEs / VIEs / securitization | Special Purpose Entities (SPEs) and Variable Interest Entities (VIEs): unconsolidated stakes with guarantees or first-loss exposure; receivables sold to a trust (retained interest only on balance sheet) | [$ / none] | 0–2 |
| 3 | Guarantees & contingencies | Third-party debt/loan guarantees, warranty exposure, litigation disclosed but not reserved | [$ / none] | 0–2 |
| 4 | Joint ventures / equity-method | Company's share of JV debt (equity method shows one net line only); proportional-consolidation debt | [$ / none] | 0–2 |
| 5 | Pension & post-retirement | Funded status (underfunding), discount-rate and return assumptions vs. peers (aggressive = understated liability) | [$ / none] | 0–2 |
| 6 | Purchase obligations / take-or-pay | Non-cancelable supply commitments and minimum purchases in the footnote table — debt-like | [$ / none] | 0–2 |
| 7 | Stock-Based Compensation (SBC) dilution | Not classic OBS, but a non-cash add-back: SBC as % of Free Cash Flow (FCF) and net share-count change; compute SBC-adjusted FCF | [% / none] | 0–2 |

- **OBS Risk Score:** **X / 14** — ✅ 0–3 clean · ⚠️ 4–7 watch · 🔴 8+ material hidden leverage
- **Structured-to-hide flag:** [Yes/No — any arrangement that appears designed specifically to stay off-balance-sheet; this signal matters more than the dollar amount]

**Adjusted vs. Reported Leverage** — add back capitalized lease-equivalents not already in debt, proportional JV debt, unfunded pension deficit, and material guarantees:

| Metric | Reported | OBS-Adjusted | Gap |
|--------|----------|--------------|-----|
| Total Debt | $X.XB | $X.XB | +X% |
| Debt / Equity | X.Xx | X.Xx | +X.Xx |
| Net Debt / EBITDA | X.Xx | X.Xx | +X.Xx |

- **So what:** [1 sentence — is the gap large enough (e.g., >0.5x Net Debt / EBITDA) to change the balance-sheet conviction? A big gap is a red flag.]
- If nothing material: "No significant off-balance-sheet concerns identified." and skip the adjusted table.

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
- **Note:** If the balance sheet read aligns with consensus, state that explicitly — a clean or stressed balance sheet is a fact, not a differentiated view.

---

## Read-Through to the Call

**Signal: BULLISH / NEUTRAL / BEARISH (for the thesis) · Balance-Sheet Conviction X / 10**

- **So what:** [1 sentence — does the balance sheet de-risk a long or strengthen a short, and why]
- **What flips it:** [1 sentence — the single development (downgrade, covenant, write-down) that would change this read]

*Conviction scale (this dimension only): 9–10 = decisive support for the call · 7–8 = strong · 5–6 = mixed/neutral · 3–4 = weak · 1–2 = red flag*

---

## Save to Word Document

Write and execute a Python script using `python-docx` (`.venv/Scripts/python`) that:
- Landscape, narrow margins (0.5" all sides), Arial 10pt body text — call `setup_document(doc)` right after `Document()` — see CLAUDE.md
- Title: `{TICKER} — Balance Sheet` (bold, centered) + date subtitle
- **Embed both chart images at `width=Inches(9.5)`** to fill the full landscape text width: composition under the Balance Sheet Snapshot table, the 8-quarter trend chart under Liquidity & Leverage (next to the Trend bullet). Add a small italic source line under each ("SEC EDGAR")
- Section headings as Heading 1
- Bullets as Word list items
- **Tables: initialize with `rows=1` (header only), then `table.add_row()` per data row.** Call `set_row_font_size(row)` on every data row.
- **Every table**: call `autofit_table(table)` then `add_table_borders(table)` AFTER all rows added
- Dark blue header rows (fill `1F3864`), white bold text
- Source citations in small italic (OBS figures: cite the 10-K/10-Q filing and date)
- OBS section: scored checklist table + adjusted-vs-reported leverage table, both following the table rules
- Variant View as a 3-column table; Read-Through block in bold
- Saves to `Outputs/{TICKER}/4_{ticker_lowercase}_balance_sheet_analysis.docx`
- Save the script file to `Outputs/{TICKER}/generate_{ticker_lowercase}_balance_sheet.py` and run it from project root

Call `add_footnote(doc)` immediately before `doc.save(...)` to append the standard AI disclaimer.

Import the shared helpers from `doc_utils.py`:
```python
import sys; sys.path.insert(0, '.')
from doc_utils import setup_document, autofit_table, add_table_borders, set_row_font_size, add_footnote, fmt_value
```
Use `fmt_value(v)` for all dollar amounts in table cells (auto-scales: ≥$1B → `$X.XXB`, ≥$1M → `$X.XM`, ≥$1K → `$X.XK`). Never hardcode `/ 1e9` or manually append `"B"`.

Confirm the output file path when done.
