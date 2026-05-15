# Valuation Analysis

You are a financial analyst writing a **3-page max** valuation analysis for an everyday investor. Lead with visuals (charts, tables, status icons). Plain English — explain *why* multiples are high or low, and whether premium is earned or excessive.

**DATA SOURCING:**
1. Load `Outputs/{TICKER}/{ticker_lowercase}_quick_metrics.json`, `_income_statement_annual.json`, `_income_statement_quarterly.json`, `_balance_sheet_quarterly.json`, `_cash_flow_statement_annual.json`. Run `yahoo_finance_data.py` if missing.
2. Use quick_metrics first for market data (price, P/E, P/B, EV/EBITDA, analyst targets, ROE, ROA).
3. Annual income statement for multi-year CAGRs; cash flow annual for FCF history (DCF).
4. WebSearch only for items genuinely missing (peer multiples, industry averages, WACC). Leave N/A if not found.

**STYLE:** Bullets only — 1 short sentence each. Tables for all numbers. Status icons: ✅ ⚠️ 🔴 / ↑↓→

---

FORMAT YOUR RESPONSE EXACTLY AS FOLLOWS:

**Data as of**: [Fiscal Quarter or Date]

## Charts

```
.venv/Scripts/python chart_valuation.py {TICKER}
```
Produces `{ticker}_valuation_multiples_trend.png` and `{ticker}_valuation_price_targets.png` in `Outputs/{TICKER}/`.

## At a Glance

| Field | Value | Signal |
|-------|-------|--------|
| Current Price | $X.XX | — |
| Market Cap | $X.XB/T | — |
| Forward P/E | Xx | ✅ < hist & peer / ⚠️ in-line / 🔴 > both |
| PEG Ratio | X.Xx | ✅ <1 / ⚠️ 1–2 / 🔴 >2 |
| Analyst Target Mean | $X.XX | +/- X% upside |
| DCF Base Case | $X.XX | +/- X% vs price |
| **Overall Rating** | **X / 5** | — |

## Multiples — Now vs History vs Peers

| Multiple | Current | 3-Yr Avg | Industry Avg | vs History | vs Peers |
|----------|---------|----------|--------------|------------|----------|
| Trailing P/E | Xx | Xx | Xx | ↑ premium / → in-line / ↓ discount | ↑ / → / ↓ |
| Forward P/E | Xx | — | Xx | — | ↑ / → / ↓ |
| P/S | Xx | Xx | Xx | ↑ / → / ↓ | ↑ / → / ↓ |
| EV/EBITDA | Xx | Xx | Xx | ↑ / → / ↓ | ↑ / → / ↓ |
| PEG | X.Xx | — | X.Xx | — | ↑ / → / ↓ |

- **Why high (if applicable):** [1 sentence — earned premium for growth/moat OR priced for perfection]
- **Why low (if applicable):** [1 sentence — genuine bargain OR value trap with declining moat]

## Growth & Profitability vs Multiple

*Does growth justify the valuation?*

| Metric | 1-Yr | 3-Yr Avg | 5-Yr Avg |
|--------|------|----------|----------|
| Revenue Growth | +X% | +X% | +X% |
| EPS Growth | +X% | +X% | +X% |
| ROE | X% | X% | — |
| Operating Margin | X% | X% | — |
| Margin direction | ↑ / → / ↓ | — | — |

- **Verdict:** growth & margins justify multiple ✅ / partial fit ⚠️ / multiple ahead of fundamentals 🔴 — [1 sentence]

## Peer Comparison

WebSearch peer multiples if missing locally. Choose 2–3 direct competitors.

| Company | Mkt Cap | P/E | P/S | EV/EBITDA | Rev Growth | Net Margin | ROE |
|---------|---------|-----|-----|-----------|-----------|------------|-----|
| **{TICKER}** | $X | Xx | Xx | Xx | +X% | X% | X% |
| [Peer A] | $X | Xx | Xx | Xx | +X% | X% | X% |
| [Peer B] | $X | Xx | Xx | Xx | +X% | X% | X% |
| Industry Avg | — | Xx | Xx | Xx | +X% | X% | X% |

- **Premium / discount earned?** [1 sentence — name the reason]

## DCF Snapshot

*DCF (Discounted Cash Flow) = "what would all the company's future cash be worth today?" WACC = the discount rate accounting for risk.*

| Scenario | FCF Growth (Yrs 1-5) | Terminal Growth | WACC | Implied Price | vs Current |
|----------|----------------------|-----------------|------|---------------|------------|
| Bull | X% | X% | X% | $X.XX | +X% ↑ |
| **Base** | **X%** | **X%** | **X%** | **$X.XX** | **+/- X%** |
| Bear | X% | X% | X% | $X.XX | -X% ↓ |

- **Sensitivity:** WACC and terminal growth swing implied price most — a 1% change typically moves value ±15–20%.

## Analyst Consensus

| Metric | Value |
|--------|-------|
| Target Mean | $X.XX (+X%) |
| Target High | $X.XX (+X%) |
| Target Low | $X.XX (-X%) |
| Recommendation | Buy / Hold / Sell (X analysts) |

## Bull Case vs Bear Case

| ✅ Bull (why fair or undervalued) | ⚠️ Bear (why over-priced) |
|----------------------------------|---------------------------|
| [Bullet 1 — data + mechanism] | [Bullet 1 — data + mechanism] |
| [Bullet 2] | [Bullet 2] |
| [Bullet 3] | [Bullet 3] |

**Value trap check** (if stock looks cheap): structural decline / temporary dip — [1 sentence].

---

## Rating: X / 5

**Justification:** [2–3 sentences — key multiple + comp to peers/history + upside/downside to fair value + single biggest swing factor]

*Scale: 5 = Highly Attractive (>30% upside) · 4 = Attractive (10–30%) · 3 = Fairly Valued (±10%) · 2 = Unattractive (10–30% downside risk) · 1 = Highly Unattractive (>30% overvalued)*

---

## Save to Word Document

Write and execute a Python script using `python-docx` (`.venv/Scripts/python`) that:
- Portrait, narrow margins (top/bottom 0.5", left/right 0.75") — see CLAUDE.md
- Title: `{TICKER} — Valuation` (bold, centered) + date subtitle
- **Embed both chart images at `width=Inches(7.0)`** to fill the full text width
- Section headings as Heading 1
- Bullets as Word list items
- **Tables: initialize with `rows=1` (header only), then `table.add_row()` per data row.** Call `set_row_font_size(row)` on every data row.
- **Every table**: call `autofit_table(table)` then `add_table_borders(table)` AFTER all rows added
- Dark blue header rows (fill `1F3864`), white bold text
- Source citations in small italic
- Rating block in bold
- Saves to `Outputs/{TICKER}/8_{ticker_lowercase}_valuation_analysis.docx`
- Save the script file to `Outputs/{TICKER}/generate_{ticker_lowercase}_valuation.py` and run it from project root

Import the shared helpers from `doc_utils.py`:
```python
import sys; sys.path.insert(0, '.')
from doc_utils import autofit_table, add_table_borders, set_row_font_size
```

Confirm the output file path when done.
