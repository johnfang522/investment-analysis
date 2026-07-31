# Bubble / Crash Risk Framework

Used by `/market_sentiment_analysis` Step 3. Bubble risk is assessed on **simultaneity** — any one condition alone is common; several firing together is what precedes major drawdowns.

## The Six Warning Conditions

| # | Condition | Threshold | What it captures |
|---|---|---|---|
| 1 | Shiller CAPE | > 35 | Valuation stretched vs. a century of history |
| 2 | Buffett Indicator | > 160% | Market cap outrunning the real economy |
| 3 | HY OAS | < 300 bps | Credit priced for perfection — no compensation for default risk |
| 4 | CNN Fear & Greed | > 70 | Retail/positioning greed |
| 5 | VIX | < 15 | Volatility complacency — hedging demand collapsed |
| 6 | Breadth divergence | SPY − RSP > 5pp YTD | Narrow leadership carrying the index |

## Verdict Mapping

| Conditions true | Verdict |
|---|---|
| 0–1 | **Low** |
| 2 | **Moderate** |
| 3–4 | **Elevated** |
| 5–6 | **Extreme** |

Always name the specific conditions firing in the verdict reasoning, with their current readings.

## Interpretation Discipline

- **Valuation alone is not a timing signal.** CAPE and the Buffett Indicator can stay in warning territory for *years* (both spent most of 2017–2021 above threshold). They set the size of the eventual drawdown, not its date.
- **Credit + volatility are the trigger conditions.** Historically, the transition from "expensive" to "dangerous" shows up first as HY spreads widening off the lows and VIX regime-shifting above ~20 — watch the *change*, not just the level.
- **Breadth divergence is the fragility tell.** A narrow rally means the index is one or two earnings misses away from losing its leadership; broad participation absorbs shocks.
- An **Elevated/Extreme verdict is a risk-budget statement, not a short signal** — the actionable output is reduced gross, tighter stops, and hedges, per the Risk Posture section.

## Historical Analogues (for calibration in the write-up)

| Episode | Conditions at peak | What followed |
|---|---|---|
| 2000 dot-com | CAPE ~44, Buffett ~140%, narrow tech leadership | S&P −49% over 2.5 yrs; CAPE never revisited 44 until the 2020s |
| 2007 pre-GFC | HY OAS ~240 bps, VIX low-teens, CAPE ~27 | Credit was the tell — spreads doubled before equities peaked-to-troughed −57% |
| Jan 2018 "vol-mageddon" | VIX ~10, F&G extreme greed, valuations elevated | −10% in 9 days — complacency conditions without credit stress produced a correction, not a crash |
| 2021–22 | CAPE ~38, Buffett ~200%, spreads ~300 bps, meme-stock froth | −25% over 10 months as the rate regime changed |
| 2000 & 2007 common thread | 4+ conditions simultaneously true | The only two episodes with 5–6 conditions firing preceded the two >45% drawdowns |

Use the closest analogue explicitly in the Bubble Risk Assessment section ("current conditions most resemble [episode] because ...") — and say where the analogy breaks down.
