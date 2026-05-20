# Technical Analysis

You are an equity research analyst producing a **3-page max** technical setup scorecard for institutional investors. All visual: tables, status icons, scorecards. State data clearly; if missing, say so.

**DATA SOURCING:**
1. Load `Outputs/{TICKER}/{ticker_lowercase}_quick_metrics.json` (price, 50/200-DMA, 52-wk range, beta) and `_price_history.json` (DMA + RSI computation). Run `yahoo_finance_data.py` if missing.
2. WebSearch only for VIX, CNN Fear & Greed, AAII sentiment, put/call, MACD cross-check.
3. Leave N/A if missing; note assumption used.

**SOURCE CITATIONS:** `Source: URL` indented below web-sourced lines.

---

**Data as of**: [Date of latest price_history entry]

## Charts

```
.venv/Scripts/python chart_technical.py {TICKER}
```
Produces `{ticker}_ta_price_ma.png` and `{ticker}_ta_rsi.png` in `Outputs/{TICKER}/`.

## At a Glance

| Field | Value | Signal |
|-------|-------|--------|
| Current Price | $X.XX | — |
| Trend (vs 200-DMA) | Up / Neutral / Down | ✅ / ⚠️ / 🔴 |
| Drawdown from 52-wk High | -X% | ✅ Shallow <10 / ⚠️ 10–20 / 🔴 >20 |
| RSI (14-day) | XX | ✅ 35–55 sweet spot / ⚠️ 55–70 / 🔴 >70 hot or <30 deep |
| Market Regime (VIX, S&P) | Constructive / Cautious / Opportunistic | — |
| Investor Sentiment | Fear / Neutral / Greed | ✅ Fear good / 🔴 Greed wait |
| **Buy Signal Score** | **X / 5** | — |
| **Verdict** | **Start Buying / Scale In Slowly / Wait** | — |

## Buy Signal Scorecard

*5-factor checklist. Each ✅ = 1 point.*

| # | Factor | Status | Pts |
|---|--------|--------|-----|
| 1 | Stock above rising 200-DMA | ✅ / ❌ | 1 / 0 |
| 2 | Meaningful pullback to support (10–20%, near key MA) | ✅ / ❌ | 1 / 0 |
| 3 | Sentiment shows fear (F&G <40, AAII bulls <35%) | ✅ / ❌ | 1 / 0 |
| 4 | Momentum stabilizing (RSI 35–55 and rising) | ✅ / ❌ | 1 / 0 |
| 5 | Market not in freefall (VIX <30, S&P above 200-DMA) | ✅ / ❌ | 1 / 0 |
| | **Total** | — | **X / 5** |

**Interpretation:** 4–5 = Strong Buy Signal · 2–3 = Moderate (start small) · 0–1 = Wait

## Trend & Pullback

| Signal | Value | Meaning |
|--------|-------|---------|
| Price vs 50-DMA | $X.XX vs $X.XX | Above / Below |
| Price vs 200-DMA | $X.XX vs $X.XX | Above / Below |
| 200-DMA slope | Rising / Flat / Falling | Trend strengthening / weakening |
| 52-wk High → Now | -X% | Shallow / Meaningful / Deep |
| 52-wk Low → Now | +X% | — |
| 52-wk Return | +X% | vs S&P 500 +X% |

## Momentum & Sentiment

| Indicator | Value | Signal |
|-----------|-------|--------|
| RSI (14-day) | XX | ✅ 35–55 / ⚠️ <30 or 55–70 / 🔴 >70 |
| RSI direction | ↑ / → / ↓ | Recovering / Deteriorating |
| Higher lows in price? | Yes / No | Stabilizing / Still falling |
| Price back above 50-DMA? | Yes / No | Confirmed / Not yet |
| MACD (daily) | Bullish cross / Flattening / Bearish | — |
| VIX | XX | ✅ <20 / ⚠️ 20–30 / 🔴 >30 |
| S&P 500 vs 200-DMA | Above / Below | Bull / Correction |
| CNN Fear & Greed | XX/100 | ✅ <40 / ⚠️ 40–60 / 🔴 >60 |
| AAII Bulls / Bears | X% / X% | ✅ Bulls <30 or Bears >45 |
| Put/Call Ratio | X.XX | ✅ >1 (fear) / 🔴 <0.7 (complacency) |

## Staged Accumulation Framework

| When | Trigger | Suggested Sizing |
|------|---------|-----------------|
| **Tranche 1** | Score ≥3 or extreme fear reading | 25–33% of intended position |
| **Tranche 2** | Reclaims 50-DMA; RSI back above 50 | Another 33% |
| **Tranche 3** | Breakout to new high on volume | Remaining 33% |

- If the stock advances 15%+ before Tranche 2 trigger, stand down and reassess — avoid chasing momentum into an extended move.

## What Could Go Wrong

| Risk | Watch For | Action |
|------|-----------|--------|
| Trend break | Closes below 200-DMA for 2+ weeks | Pause adding; reassess |
| Business deterioration | Revenue/EPS miss, guidance cut | Re-check fundamental thesis |
| Macro shock | VIX >40, S&P -20% | Size down; wait for stability |

- **Soft stop:** sustained close below 200-DMA = pause accumulation and reassess the technical thesis.

---

## Final Verdict

| | Answer |
|---|--------|
| Trend | Up / Neutral / Down |
| Market Regime | Constructive / Cautious / Opportunistic |
| Sentiment | Fear / Neutral / Greed |
| Buy Signal Score | **X / 5** |
| **What to Do** | **Start Buying / Scale In Slowly / Wait** |

**Position sizing:** [1–2 sentences — specific tranche sizes given the regime + score]

**Biggest risk to watch:** [1 sentence]

**Summary:** [2 sentences max — technical thesis and primary risk to watch]

---

## Save to Word Document

Write and execute a Python script using `python-docx` (`.venv/Scripts/python`) that:
- Portrait, narrow margins (top/bottom 0.5", left/right 0.75") — see CLAUDE.md
- Title: `{TICKER} — Technical Analysis` (bold, centered) + date subtitle
- **Embed both chart images at `width=Inches(7.0)`** to fill the full text width
- Section headings as Heading 1
- Bullets as Word list items
- **Tables: initialize with `rows=1` (header only), then `table.add_row()` per data row.** Call `set_row_font_size(row)` on every data row.
- **Every table**: call `autofit_table(table)` then `add_table_borders(table)` AFTER all rows added
- Dark blue header rows (fill `1F3864`), white bold text
- Source citations in small italic
- Final Verdict block in bold
- Saves to `Outputs/{TICKER}/9_{ticker_lowercase}_technical_analysis.docx`
- Save the script file to `Outputs/{TICKER}/generate_{ticker_lowercase}_technical.py` and run it from project root

Call `add_footnote(doc)` immediately before `doc.save(...)` to append the standard AI disclaimer.

Import the shared helpers from `doc_utils.py`:
```python
import sys; sys.path.insert(0, '.')
from doc_utils import autofit_table, add_table_borders, set_row_font_size, add_footnote
```

Confirm the output file path when done.
