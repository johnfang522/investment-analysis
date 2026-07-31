# Market Sentiment Scoring Tables

Conversion tables for the 7 indicators in `/market_sentiment_analysis`. Each raw reading maps to a 0–100 sentiment score where **0 = extreme bear / maximum stress** and **100 = extreme bull / maximum complacency**. Interpolate linearly within a band when the reading falls between band midpoints — the bands give the anchor score for the middle of each range.

## 1. VIX (inverted: high VIX = fear = low score)

| VIX level | Score |
|---|---|
| < 12 | 95 |
| 12–15 | 85 |
| 15–20 | 65 |
| 20–25 | 50 |
| 25–30 | 35 |
| 30–40 | 20 |
| > 40 | 5 |

## 2. CNN Fear & Greed (direct mapping)

Use the index value as the score directly (0 = extreme fear → 0; 100 = extreme greed → 100).

## 3. Put/Call Demand — CBOE SKEW proxy (inverted: high SKEW = put demand = fear = low score)

Use the 20-day average of `^SKEW`. If an actual CBOE equity put/call ratio reading is available from the web search, prefer it with the same logic (high ratio = fear = low score; P/C > 1.0 ≈ score 25, ~0.85 ≈ 50, < 0.70 ≈ 80).

| SKEW (20-day avg) | Score |
|---|---|
| < 115 | 90 (complacency) |
| 115–125 | 70 |
| 125–135 | 55 |
| 135–145 | 40 |
| 145–155 | 25 |
| > 155 | 10 |

## 4. Market Breadth — RSP minus SPY, YTD gap (direct: broad participation = high score)

| RSP − SPY (YTD, pp) | Score |
|---|---|
| > +5 | 85 (broad, healthy participation) |
| +2 to +5 | 70 |
| −2 to +2 | 50 |
| −5 to −2 | 35 |
| < −5 | 15 (narrow rally — warning) |

## 5. HY OAS Spread (inverted: wide spread = stress = low score)

Remember: FRED `BAMLH0A0HYM2` is in percentage points — multiply by 100 for bps.

| HY OAS (bps) | Score |
|---|---|
| < 275 | 90 (extreme credit complacency) |
| 275–350 | 75 |
| 350–450 | 55 |
| 450–550 | 40 |
| 550–700 | 25 |
| > 700 | 10 (credit stress) |

Note the double-edged read: a very high score here is *bullish sentiment* but a *bubble-risk input* — flag it in Step 3 when < 300 bps.

## 6. Shiller CAPE (inverted: high CAPE = overvalued = low score)

| CAPE | Score |
|---|---|
| < 17 | 90 |
| 17–22 | 75 |
| 22–27 | 60 |
| 27–32 | 45 |
| 32–37 | 30 |
| > 37 | 15 |

## 7. Buffett Indicator — Market Cap / GDP (inverted: high ratio = overvalued = low score)

| Ratio | Score |
|---|---|
| < 100% | 90 |
| 100–120% | 75 |
| 120–140% | 60 |
| 140–160% | 45 |
| 160–200% | 30 |
| > 200% | 15 |

## Composite Weights

| Indicator | Weight |
|---|---|
| VIX | 15% |
| CNN Fear & Greed | 15% |
| Put/Call (SKEW proxy) | 10% |
| Market Breadth (RSP vs SPY) | 15% |
| HY OAS Spread | 20% |
| Shiller CAPE | 15% |
| Buffett Indicator | 10% |

Credit gets the heaviest weight — the bond market is historically the earliest and least emotional of the seven signals. If an indicator is unavailable on a given run, drop it and renormalize the remaining weights to 100%; note the omission in the report.

## Composite Zones

| Composite | Zone label |
|---|---|
| 0–20 | Very Bearish — capitulation / maximum stress |
| 20–40 | Bearish — fear dominant |
| 40–60 | Neutral — mixed signals |
| 60–80 | Bullish — greed building, complacency risk |
| 80–100 | Very Bullish — extreme complacency, contrarian caution |

Interpretation discipline: extremes are contrarian at the tails (0–20 has historically been a better *buying* zone than 80–100). The composite describes *where sentiment is*, not where the market goes next — direction of change since the prior run matters as much as level.
