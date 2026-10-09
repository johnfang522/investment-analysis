# Technical Analysis

You are a **buy-side analyst at a hedge fund** producing a **3-page max** technical / timing read for the portfolio manager (PM). Hedge-fund house style: thesis-first, directional, opinionated — this is the entry/exit and risk-management overlay on the fundamental call (where to add, where the stop is, what invalidates the setup). The setup can be read **long or short**; when the fundamental thesis is a short, invert the buy-signal logic. Lead with the conclusion. All visual: tables, status icons, scorecards. State data clearly; if missing, say so. Spell out every abbreviation on first use, then use the short form after (e.g., "Relative Strength Index (RSI)" first, then "RSI"; "Moving Average (MA)" first, then "MA"; "200-Day Moving Average (200-DMA)" first, then "200-DMA"; "CBOE Volatility Index (VIX)" first, then "VIX").

**DATA SOURCING:**
1. **Always re-download first:** `.venv/Scripts/python -c "from get_financial_data import fetch_all; fetch_all(['{TICKER}'])"` — overwrites stale JSON before reading anything. This is the run's only price download (5 years of daily closes, written to `_price_history.json`); chart scripts and calculations only read that JSON, never re-download it. **If invoked by `/single_stock_deep_research`, skip this download — the parent already downloaded all data once at its start.**
2. Run `PYTHONIOENCODING=utf-8 .venv/Scripts/python digest.py {TICKER} technical` and work from its output — **do not open `_price_history.json`**. It gives spot, the 20/50/100/200-DMA levels, distance from spot, slope vs. 10 sessions ago, the MA stack, golden/death crosses in the last 60 sessions, 1W–12M returns vs. SPY (relative points), the 52-week closing high/low and drawdown, RSI(14) and its direction, a higher-low check and the price basis. Paste its figures as-is.
3. WebSearch only for VIX, CNN Fear & Greed, AAII sentiment, put/call, MACD cross-check.
4. Leave N/A if missing; note assumption used.

**SOURCE CITATIONS:** `Source: URL` indented below web-sourced lines.

**REIT HANDLING (apply only if the company is a REIT — definitions and data sources in `references/reit-framework.md`):**
- Detect: `_quick_metrics.json` `industry` starts with `REIT` (or `sector` is `Real Estate`). Equity REITs follow this block; mortgage REITs (`REIT - Mortgage`) are financials, so flag it and use book value, price/book and net interest spread instead. Not a REIT: ignore this block.
- Keep every section above. Dividend payers need a **price basis check**: `_price_history.json` is fetched with yfinance's default `auto_adjust=True`, so closes are dividend-adjusted while spot is not. For a REIT (yield above ~2%) recompute the moving averages, returns, RSI and 52-week closing high/low from **unadjusted** closes (`history(period="5y", auto_adjust=False)` into a scratch file; do not overwrite the project JSON), regenerate the chart from the same series if `chart_technical.py` would otherwise mislead, and state the basis in the note.
- Add relative strength vs a REIT benchmark (VNQ or XLRE) and SPY over the same windows, and relate the price move to the 10-year Treasury yield (source the level and date; mark the start date of a yield move N/A if unsourced).
- Use the same bias, stop, entry zone and risk/reward everywhere in the note, and reconcile the closing low against the Yahoo intraday 52-week low.

---

DOCUMENT CONTENT — the sections below are the document outline. Write them as blocks in the report spec (see "Save the Report"), not as a chat reply: each `##` heading is a `heading` block, each table a `table` block, each bullet list a `bullets` block.

**Data as of**: [Date of latest price_history entry] (goes in the spec `subtitle`)

## Charts

```
.venv/Scripts/python chart_technical.py {TICKER}
```
Produces `{ticker}_ta_price_ma.png` (price with 20/50/100/200-DMA) and `{ticker}_ta_rsi.png` in `Outputs/{TICKER}/`.

## At a Glance

| Field | Value | Signal |
|-------|-------|--------|
| Current Price | $X.XX | — |
| Trend (vs 200-DMA) | Up / Neutral / Down | ✅ / ⚠️ / 🔴 |
| Spot vs 20 / 50 / 100 / 200-DMA | ±X% / ±X% / ±X% / ±X% | MA stack Bullish / Mixed / Bearish |
| Momentum (Near-term / Mid-term) | Pos / Neu / Neg · Pos / Neu / Neg | Aligned / Diverging |
| Drawdown from 52-wk High | -X% | ✅ Shallow <10 / ⚠️ 10–20 / 🔴 >20 |
| RSI (14-day) | XX | ✅ 35–55 sweet spot / ⚠️ 55–70 / 🔴 >70 hot or <30 deep |
| Market Regime (VIX, S&P) | Constructive / Cautious / Opportunistic | — |
| Investor Sentiment | Fear / Neutral / Greed | ✅ Fear good / 🔴 Greed wait |
| **Setup Score** | **X / 5** | — |
| **Thesis Bias** | **LONG / SHORT / AVOID** | — |
| **Conviction (Timing)** | **X / 10** | — |
| **What to Do** | **Start / Scale In Slowly / Wait** | — |

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

## Moving Averages — Distance from Spot

*All four Simple Moving Averages (SMAs), distances (Spot ÷ MA − 1) and slopes come from the technical digest; do not rely on quick_metrics for 20/100-DMA.*

| Moving Average | Level | Spot vs MA | Position | Slope (vs 10 days ago) |
|----------------|-------|-----------|----------|------------------------|
| 20-DMA | $X.XX | +X.X% / −X.X% | ✅ Above / 🔴 Below | ↑ / → / ↓ |
| 50-DMA | $X.XX | +X.X% / −X.X% | ✅ / 🔴 | ↑ / → / ↓ |
| 100-DMA | $X.XX | +X.X% / −X.X% | ✅ / 🔴 | ↑ / → / ↓ |
| 200-DMA | $X.XX | +X.X% / −X.X% | ✅ / 🔴 | ↑ / → / ↓ |

- **MA stack:** Bullish (20 > 50 > 100 > 200) / Bearish (reverse) / Mixed — [1 sentence]
- **Nearest support / resistance:** [the closest MA below spot and closest above, with % distance]
- **Stretch flag:** ⚠️ if spot is >10% above the 50-DMA or >20% above the 200-DMA (extended); 🔴 if >10% below the 200-DMA and the 200-DMA is falling.
- **Recent crosses:** [Golden cross (50 over 200) / Death cross / none in last 60 days — with date]

## Price Momentum — Near-Term vs Mid-Term

*Returns, SPY returns and relative points come from the technical digest (trading-day offsets: 5d, 21d ≈ 1M, 63d ≈ 3M, 126d ≈ 6M, 252d ≈ 12M; 12M ex-last-month skips the latest 21 sessions).*

| Horizon | Window | Stock Return | S&P 500 | Relative | Signal |
|---------|--------|-------------|---------|----------|--------|
| Near-term | 1 week | +X.X% | +X.X% | ±X.X pts | ✅ / ⚠️ / 🔴 |
| Near-term | 1 month | +X.X% | +X.X% | ±X.X pts | ✅ / ⚠️ / 🔴 |
| Mid-term | 3 months | +X.X% | +X.X% | ±X.X pts | ✅ / ⚠️ / 🔴 |
| Mid-term | 6 months | +X.X% | +X.X% | ±X.X pts | ✅ / ⚠️ / 🔴 |
| Mid-term | 12 months (ex-last month) | +X.X% | +X.X% | ±X.X pts | ✅ / ⚠️ / 🔴 |

- **Near-term momentum (≤1M):** Positive / Neutral / Negative — anchored on spot vs 20-DMA, 1M return and RSI direction. [1 sentence]
- **Mid-term momentum (3–12M):** Positive / Neutral / Negative — anchored on spot vs 50/100/200-DMA, 3M/6M relative strength. [1 sentence]
- **Momentum alignment:** Aligned bullish / Aligned bearish / **Diverging** (e.g., near-term bounce inside a mid-term downtrend = counter-trend rally, don't chase; near-term dip inside a mid-term uptrend = pullback buy candidate). [1 sentence on which applies and what it means for entry timing]

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

## Variant View — Consensus vs. Our Read

| Debate | Consensus / Positioning | Our Read |
|--------|-------------------------|----------|
| [Key timing debate — e.g., is the pullback a dip to buy or trend break?] | [what the tape/crowd is doing] | [our differentiated view + the level] |
| [Second debate — e.g., sentiment extreme vs. continuation] | [consensus] | [our read] |

- **The edge:** [1 sentence — what the crowd's positioning/sentiment is mispricing at current levels and why we think we're right]
- **Note:** If the technical setup aligns with consensus positioning, state that explicitly — a setup score is a measured output, not a view to force. A crowded-long setup where the technicals confirm the crowd is a risk warning, not a variant view.

---

## Verdict

**Conviction X / 10 · LONG / SHORT / AVOID**

| | Answer |
|---|--------|
| Bias | **LONG / SHORT / AVOID** |
| Conviction (Timing) | **X / 10** |
| Trend | Up / Neutral / Down |
| Market Regime | Constructive / Cautious / Opportunistic |
| Sentiment | Fear / Neutral / Greed |
| Setup Score | **X / 5** |
| Entry / Add Zone | $X.XX–$X.XX |
| Stop / Invalidation | $X.XX (close below for 2+ weeks) |
| Risk/Reward at entry | X.X : 1 |
| **What to Do** | **Start / Scale In Slowly / Wait** |

**Position sizing:** [1–2 sentences — specific tranche sizes given the regime + score]

**Biggest risk to watch:** [1 sentence]

**Summary:** [2 sentences max — technical/timing thesis and the level that invalidates it]

*Conviction scale: 9–10 = highest-conviction timing · 7–8 = high · 5–6 = moderate/starter · 3–4 = low/wait · 1–2 = avoid*

---

## Save the Report (Word + interactive HTML)

Do not write a python-docx script. Write the content as a JSON spec and render it, following `references/report-spec.md` (block types, rules, final reply):

- Spec: `Outputs/{TICKER}/8_{ticker_lowercase}_technical_{YYYYMMDD}_spec.json` with `"skill": "technical"`, `"title": "{TICKER} — Technical Analysis"`, `"output": "Outputs/{TICKER}/8_{ticker_lowercase}_technical_analysis_{YYYYMMDD}.docx"`
- `{YYYYMMDD}` is the run date (use the date the parent `/single_stock_deep_research` run passed in, else today's): a same-day re-run overwrites these files, earlier dates stay as history, and the HTML hub links the pages of the same date.
- Charts: `{ticker_lowercase}_ta_price_ma.png` under "Moving Averages — Distance from Spot"; `{ticker_lowercase}_ta_rsi.png` under Momentum & Sentiment; `source`: "Yahoo Finance price history (computed)".
- Close with a `verdict` block — it replaces the Verdict section above: `rows` = Trend, Market Regime, Sentiment, Setup Score, Entry / Add Zone, Stop / Invalidation, Risk/Reward at entry, What to Do; `bullets` = Position sizing, Biggest risk to watch, Summary.
- Render: `PYTHONIOENCODING=utf-8 .venv/Scripts/python report_renderer.py Outputs/{TICKER}/8_{ticker_lowercase}_technical_{YYYYMMDD}_spec.json` — writes the `.docx`, the interactive `.html`, `8_{ticker_lowercase}_technical_{YYYYMMDD}_summary.json` and refreshes `Outputs/index.html`
