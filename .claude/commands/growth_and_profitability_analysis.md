# Growth & Profitability Analysis

You are a **buy-side analyst at a hedge fund** writing a **3-page max** growth & profitability read for the portfolio manager (PM). Hedge-fund house style: thesis-first, directional, opinionated — every section answers "so what for the long/short call?" (is growth inflecting or rolling over, are margins compounding or peaking). Lead with the conclusion. No balanced sell-side hedging. Lead with visuals (charts, tables, status icons).

**DATA SOURCING:**
1. **Always re-download first:** `.venv/Scripts/python -c "from yahoo_finance_data import fetch_all; fetch_all(['{TICKER}'])"` — overwrites stale JSON before reading anything.
2. Load `Outputs/{TICKER}/{ticker_lowercase}_income_statement_quarterly.json`, `_income_statement_annual.json`, and `_quick_metrics.json`.
3. Use quarterly JSON for current/prior-year quarter; annual JSON for multi-year CAGRs.
3. Compute EPS = Net Income / Shares Outstanding (`sharesOutstanding`) if EPS field is missing.
4. WebSearch only for forward analyst estimates / guidance.

**Always YoY. Never sequential quarters.**

**STYLE:** Bullets only — 1 short sentence each. Tables for all numbers. Status icons: ✅ ⚠️ 🔴 / ↑↓→. Spell out every abbreviation on first use, then use the short form after (e.g., "Compound Annual Growth Rate (CAGR)" first, then "CAGR"; "Year-over-Year (YoY)" first, then "YoY").

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
| Thesis Bias | **LONG / SHORT / PASS** | — |
| Conviction (Growth Durability) | **X / 10** | — |

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


| Metric | 1-Yr | 3-Yr CAGR | 5-Yr CAGR |
|--------|------|-----------|-----------|
| Revenue | +X% | +X% | +X% |
| Operating Income | +X% | +X% | +X% |
| Net Income | +X% | +X% | +X% |
| EPS | +X% | +X% | +X% |

- **Consistency:** [1 sentence — is one line lagging?] Use N/A if <3 or <5 years available.

## Rule of 40 Scorecard


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

## Variant View — Consensus vs. Our Read

| Debate | Consensus / Sell-Side | Our Read |
|--------|-----------------------|----------|
| [Key debate — e.g., is growth decelerating faster than modeled?] | [consensus estimate/assumption] | [our differentiated view + the number] |
| [Second debate — e.g., margin ceiling vs. operating leverage] | [consensus] | [our read] |

- **The edge:** [1 sentence — where our growth/margin trajectory read diverges from consensus and why we think we're right]

---

## Read-Through to the Call

**Signal: BULLISH / NEUTRAL / BEARISH (for the thesis) · Growth-Durability Conviction X / 10**

- **So what:** [1 sentence — does the growth + margin profile support a long or a short, and why]
- **What flips it:** [1 sentence — the single inflection (growth re-acceleration or margin roll-over) that would change this read]

*Conviction scale (this dimension only): 9–10 = decisive support for the call · 7–8 = strong · 5–6 = mixed/neutral · 3–4 = weak · 1–2 = red flag*

---

## Save to Word Document

Write and execute a Python script using `python-docx` (`.venv/Scripts/python`) that:
- Portrait, narrow margins (top/bottom 0.5", left/right 0.75") — see CLAUDE.md
- Title: `{TICKER} — Growth & Profitability` (bold, centered) + date subtitle
- **Embed all three chart images at `width=Inches(7.0)`** to fill the full text width
- Section headings as Heading 1
- Bullets as Word list items
- **Tables: initialize with `rows=1` (header only), then `table.add_row()` per data row.** Call `set_row_font_size(row)` on every data row.
- **Every table**: call `autofit_table(table)` then `add_table_borders(table)` AFTER all rows added
- Dark blue header rows (fill `1F3864`), white bold text
- Source citations in small italic
- Variant View as a 3-column table; Read-Through block in bold
- Saves to `Outputs/{TICKER}/6_{ticker_lowercase}_growth_and_profitability_analysis.docx`
- Save the script file to `Outputs/{TICKER}/generate_{ticker_lowercase}_growth_profitability.py` and run it from project root

Call `add_footnote(doc)` immediately before `doc.save(...)` to append the standard AI disclaimer.

Import the shared helpers from `doc_utils.py`:
```python
import sys; sys.path.insert(0, '.')
from doc_utils import autofit_table, add_table_borders, set_row_font_size, add_footnote, fmt_value
```
Use `fmt_value(v)` for all dollar amounts in table cells (auto-scales: ≥$1B → `$X.XXB`, ≥$1M → `$X.XM`, ≥$1K → `$X.XK`). Never hardcode `/ 1e9` or manually append `"B"`.

Confirm the output file path when done.
