---
description: >
  Builds a professional Word document (.docx) market sentiment report for any industry theme (e.g. edge AI compute, optical interconnect, power infrastructure) or the broad stock market. Use this skill whenever the user asks to measure, score, or report on market sentiment, investor positioning, or theme-level sentiment signals. Also trigger for requests like "how bullish is the market on X", "what's the sentiment for Y theme", "build me a sentiment report", "score the setup for Z sector", "analyze investor sentiment for [theme]", or "save sentiment analysis to a Word doc". Always use this skill even if the user doesn't explicitly say "sentiment framework" — any request to gauge or document market mood, positioning, or investor enthusiasm for a theme qualifies.
---

# Market Sentiment Framework — Word Document Output

You produce a **plain-English, visual-heavy** sentiment report (Word .docx) that answers three questions any everyday investor cares about:

1. **Is the market bullish, neutral, or bearish right now?**
2. **Are we in a bull market or a bear market?**
3. **Are we in bubble territory?**

Lead with verdicts and visuals (charts, scorecards, status icons). Bullets only — no prose paragraphs. Define every acronym the first time you use it (e.g., "VIX — the market's 'fear index'").

---

## Instructions

The user invoked `/market_sentiment_framework` with: `$ARGUMENTS`.

If `$ARGUMENTS` is empty, ask the user for a theme, sector, or "broad market".

Otherwise, treat `$ARGUMENTS` as the theme. Use `WebSearch` to gather **current** signals for each pillar before scoring (do not rely on training data for valuations, flows, or sentiment readings — these change weekly). For unfamiliar themes or thin data, set the pillar to 50 and label "Insufficient data".

---

## The Three Big Questions (lead the report with these)

For **every** report, give clear verdicts:

| Question | Verdict | Key Evidence (1 phrase each) |
|---------|---------|-------------------------------|
| **1. Sentiment right now?** | 🟢 Bullish / 🟡 Neutral / 🔴 Bearish | [composite score, fear/greed reading] |
| **2. Bull market or bear market?** | 🐂 Bull / ↔ Range-bound / 🐻 Bear | [price vs 200-day moving average, drawdown from highs, breadth] |
| **3. Bubble territory?** | ✅ Not Bubble / ⚠️ Frothy / 🔴 Bubble | [valuation extremes, speculation excess, leverage] |

**Bull vs Bear thresholds:**
- 🐂 Bull market = index >5% above its 200-day moving average AND less than 10% below the 52-week high
- 🐻 Bear market = index >20% below the 52-week high (the textbook definition)
- ↔ Range-bound = anything in between

**Bubble territory thresholds:**
- 🔴 Bubble = ≥3 of these flags trip: Shiller P/E (a 10-year inflation-adjusted price-to-earnings ratio) >35 · Buffett Indicator (total US stock market value ÷ US economy size) >180% · IPO/SPAC frenzy (new public listings well above historical norms) · margin debt at 5-year high · top 10 stocks make up >30% of S&P 500 (concentration) · CNN Fear & Greed >80 (Extreme Greed)
- ⚠️ Frothy = 1–2 flags trip
- ✅ Not Bubble = 0 flags

---

## The Five Sentiment Pillars (the engine for the composite score)

Score each pillar 0–100 (0 = max bearish, 50 = neutral, 100 = max bullish).

| Pillar | What it measures (plain English) | Key data |
|---|---|---|
| **Where the money is moving** (Positioning & Flows) | Are investors buying or selling? | Fund flows (Investment Company Institute), institutional positioning, short interest, margin debt |
| **Price action** (Momentum & Breadth) | Are prices rising broadly or only in a few names? | % of stocks above their 200-day moving average, advance/decline line, 52-week highs vs lows, relative strength |
| **Valuation** (price vs fundamentals) | How expensive is it relative to earnings and sales? | Forward P/E (price-to-earnings using next year estimate), P/S (price-to-sales), EV/EBITDA (enterprise value to operating cash earnings), free cash flow yield, equity risk premium |
| **Macro environment** (the backdrop) | Does the broader economy support or threaten gains? | Yield curve (10-year minus 2-year US Treasury), credit spreads (junk bonds vs Treasuries), financial conditions index, jobless claims, capex guidance |
| **Narrative** (the story) | What is the prevailing story in the news? | News sentiment, Google Trends, analyst upgrades vs downgrades, earnings call mention frequency |

### Composite formula

```
Composite = Momentum 25% + Positioning 20% + Valuation 20% + Macro 20% + Narrative 15%
```

| Score | Label | What it means |
|-------|-------|---------------|
| 75–100 | Extreme Greed | Bullish, but watch for crowding/froth |
| 60–74 | Greed / Bullish | Broadly positive |
| 45–59 | Neutral | Mixed signals |
| 30–44 | Fear / Cautious | Bearish lean |
| 0–29  | Extreme Fear | Deep pessimism — historically a contrarian buy zone |

Each pillar averages **4 sub-signals** (each on the same 0–100 scale).

---

## Sub-signals (use these to score each pillar)

**Where the money is moving:** ETF/fund flows · institutional/CFTC positioning · short interest trend · margin debt level

**Price action:** % of theme stocks above their 200-day moving average · 52-week high vs low ratio · relative strength vs S&P 500 · earnings estimate revisions (rising or falling)

**Valuation:** Forward P/E vs 5-year median · P/S or EV/EBITDA vs sector median · earnings revision direction · free cash flow yield or equity risk premium

**Macro environment:** Credit spreads (tight = bullish, wide = bearish) · financial conditions · capex guidance from large players · policy/regulatory tailwinds vs headwinds

**Narrative:** News sentiment volume (positive vs negative) · Google Trends · analyst upgrade/downgrade ratio (last 30 days) · earnings call mention frequency

---

## Macro Health Dashboard (always include)

These are the indicators a Wall Street analyst would check first to size up the regime. Use plain English captions for every term.

| Indicator | Plain English | Current | Status |
|-----------|---------------|---------|--------|
| S&P 500 vs 200-day moving average | Long-term trend of the broad market | +X% / -X% | 🟢 Bull / 🟡 Mixed / 🔴 Bear |
| Drawdown from 52-week high | How far we've fallen from the top | -X% | 🟢 <10% / 🟡 10–20% / 🔴 >20% |
| % of S&P 500 stocks above their 200-day MA | How broad the rally is (breadth) | X% | 🟢 >60% / 🟡 40–60% / 🔴 <40% |
| Yield curve (10-year minus 2-year US Treasury) | Negative = recession warning historically | +/-X bps | 🟢 Normal / 🟡 Flat / 🔴 Inverted |
| Credit spreads (high-yield bond yield minus Treasury) | Wide = stress, tight = risk-on | XXX bps | 🟢 <400 / 🟡 400–600 / 🔴 >600 |
| VIX (the "fear index" — expected S&P volatility) | High = fear, low = complacency | XX | 🟢 <16 calm / 🟡 16–25 nervous / 🔴 >25 fearful |
| CNN Fear & Greed Index | Composite retail sentiment (0 = panic, 100 = euphoria) | XX | 🟢 25–55 / 🟡 / 🔴 <25 panic or >75 greed |
| AAII Bulls minus Bears (American Assn. of Individual Investors weekly survey) | Retail bull/bear spread | +/-X% | Contrarian: extreme bullish = caution; extreme bearish = opportunity |
| Shiller P/E (10-year inflation-adjusted P/E) | Long-term valuation gauge | XX | 🟢 <22 / 🟡 22–30 / 🔴 >30 stretched |
| Buffett Indicator (US market cap / US GDP) | "Best single measure" per Warren Buffett | XX% | 🟢 <120% / 🟡 120–180% / 🔴 >180% bubble territory |
| Forward P/E of S&P 500 | Price relative to next 12 months earnings | Xx | 🟢 <17 / 🟡 17–20 / 🔴 >20 |
| US 10-year Treasury yield | The risk-free benchmark — high yields pressure stock valuations | X.X% | — |

WebSearch each indicator (don't rely on training data). Cite sources.

---

## Bubble Watch Checklist

| Flag | Triggered? | Evidence (1 phrase) |
|------|-----------|---------------------|
| Shiller P/E >35 | ✅ / ❌ | [number] |
| Buffett Indicator >180% | ✅ / ❌ | [number] |
| IPO / SPAC issuance well above 10-yr norm | ✅ / ❌ | [data point] |
| Margin debt at multi-year high | ✅ / ❌ | [latest FINRA reading] |
| Top 10 S&P 500 stocks >30% of index (concentration) | ✅ / ❌ | [%] |
| CNN Fear & Greed >80 (Extreme Greed) | ✅ / ❌ | [reading] |

**Total flags tripped: X / 6** → Bubble verdict above

---

## Charts (always include)

Generate these charts inline in the Python script (no separate chart_*.py file). Use `yfinance` + `matplotlib`. Save PNGs to `Outputs/` root with filenames `sentiment_{slug}_{chart_name}.png` where slug = the lowercased theme with spaces → underscores.

1. **`sentiment_{slug}_sp500_trend.png`** — S&P 500 (^GSPC) with 50-day and 200-day moving averages over the last 2 years. Shade green when price > 200-DMA, red when below. Title: "S&P 500 — Bull/Bear Regime."
2. **`sentiment_{slug}_vix_trend.png`** — VIX (^VIX) over the last 3 years. Shade green <20, yellow 20–30, red >30. Title: "VIX (Fear Index) — Last 3 Years."
3. **`sentiment_{slug}_yield_curve.png`** — 10-year minus 2-year Treasury yield (^TNX minus ^FVX as fallback if 2Y unavailable; otherwise WebSearch FRED for `T10Y2Y` series). Shade red when negative (inverted = recession warning). Title: "Yield Curve (10-Year minus 2-Year Treasury)." If data is hard to fetch from yfinance, embed a clear note in the doc instead.
4. **`sentiment_{slug}_pillar_scorecard.png`** — Horizontal bar chart of the 5 pillar scores (0–100). Color each bar by score (green ≥60, yellow 45–59, red <45). Title: "Sentiment Scorecard."

For theme-specific reports (anything other than "broad market"), **also** add:
- **`sentiment_{slug}_theme_etf_trend.png`** — Theme ETF price + 200-DMA, last 2 years. Title: "[Theme] — Price vs 200-Day MA."

Embed every chart at `width=Inches(7.0)` to keep them compact.

---

## Research Process

Before scoring, use WebSearch to gather current evidence — be specific and cite dates/sources:

1. Recent fund flows, ETF inflows/outflows, short interest, margin debt (FINRA monthly).
2. Current price performance, breadth (% above 200-DMA), estimate revision trends.
3. Current valuation multiples (Shiller P/E, Buffett Indicator, S&P 500 forward P/E).
4. Macro: yield curve, credit spreads, jobless claims, financial conditions.
5. News sentiment, analyst upgrades/downgrades (last 30–60 days), Google Trends.

Cite sources inline as `Source: URL` on an indented line below the relevant content. Do not rely on training data for any number that can change weekly.

---

## Output Format (in this exact order)

### 1. Cover Block
- Heading 1: "[Theme Name] — Market Sentiment Report"
- Bold paragraph: "Five-Pillar Sentiment Framework"
- Date: YYYY-MM-DD
- **Composite Score: XX / 100** (large bold)
- **Sentiment Label: 🟢 Bullish / 🟡 Neutral / 🔴 Bearish**

### 2. The Three Big Questions
- Heading 1: "The Three Big Questions"
- Render the verdict table from above (Sentiment / Bull or Bear / Bubble territory)
- Below the table, 3 bullets explaining each verdict in 1 sentence each — plain English, like you're talking to a friend

### 3. How to Read This Report
- Heading 1: "How to Read This Report"
- 1 sentence of context: "Each pillar and sub-signal is scored 0–100. The composite is a weighted average across all five pillars."
- 3-column table: **Score Range | Label | What It Means**, with these rows and Score-Range cell fills:

| Score Range | Label | Fill | What It Means |
|---|---|---|---|
| 75 – 100 | Extreme Greed | `C6EFCE` (green) | Strong bullish momentum; risk of crowding |
| 60 – 74 | Greed / Bullish | `C6EFCE` (green) | Broadly positive |
| 45 – 59 | Neutral | `FFEB9C` (yellow) | Mixed signals |
| 30 – 44 | Fear / Cautious | `FFC7CE` (red) | Bearish lean |
| 0 – 29 | Extreme Fear | `FFC7CE` (red) | Deep pessimism — contrarian opportunity |

- 1 sentence noting the composite formula: "Composite = Momentum 25% + Positioning 20% + Valuation 20% + Macro 20% + Narrative 15%."

### 4. Quick Summary (bullets)
- Heading 1: "Quick Summary"
- 5–7 bullets covering: composite reading and what it means in plain English · the strongest bullish pillar · the biggest risk · whether we're in a bull or bear regime · whether bubble flags are tripping · one specific data point to watch

### 5. Macro Health Dashboard
- Heading 1: "Macro Health Dashboard"
- Render the dashboard table above
- 2-3 plain-English bullets summarizing what the dashboard tells you (e.g., "The S&P 500 is well above its 200-day moving average — long-term trend is up.")

### 6. Bubble Watch
- Heading 1: "Bubble Watch"
- Render the bubble checklist table
- 2-3 bullets explaining the verdict in plain English, e.g.: "Top-10 stock concentration is XX% — historically high but not yet at dot-com extremes."

### 7. Charts
- Heading 1: "Charts"
- Embed all 4 (or 5) charts described above, each at `width=Inches(7.0)`, with a 1-sentence caption underneath each in italic

### 8. Composite Score Scorecard
- Heading 1: "Composite Score Scorecard"
- 3-column table: Pillar | Score | Reading
- Score cell shaded by score range (use the same color rules as Section 3)
- Final row (Composite) is bold

### 9. Price Snapshot
- Heading 1: "Price Snapshot"
- Fetch each ticker via `yfinance` (`yf.Ticker(symbol).history(period="1y")`); skip empties
- Columns: **Ticker | Price | 52W Low | 52W High | 50-DMA | 200-DMA | RSI (14)**
- Format prices/MAs to 2 decimals; RSI to 1 decimal
- Color rules:
  - Price cell: green if > 200-DMA, red if < 200-DMA
  - RSI cell: green if <30 (oversold), red if >70 (overbought), yellow otherwise
  - 200-DMA cell: green if price within +5% of 200-DMA, red if price >5% below, yellow otherwise
- 1 sentence interpretation below the table

**Ticker selection rules:**
- **Broad market**: `[("SPY", "S&P 500 ETF"), ("QQQ", "Nasdaq-100 ETF"), ("IWM", "Russell 2000 ETF"), ("DIA", "Dow Jones ETF"), ("XLK", "Technology"), ("XLE", "Energy"), ("XLF", "Financials"), ("XLV", "Health Care"), ("XLU", "Utilities")]`
- **Any other theme**: identify 5–7 representative stocks for the theme + the most liquid theme ETF (e.g., `SOXX` for semiconductors, `XLE` for energy, `ARKK` for disruptive innovation)

**RSI calculation** — Wilder's exponential smoothing (matches `_calc_rsi()` in `key_stock_metrics.py`):
```python
delta = closes.diff()
gain = delta.clip(lower=0)
loss = -delta.clip(upper=0)
avg_gain = gain.ewm(alpha=1/14, min_periods=14).mean()
avg_loss = loss.ewm(alpha=1/14, min_periods=14).mean()
rsi = (100 - 100 / (1 + avg_gain / avg_loss)).iloc[-1]
```

### 10. Pillar Deep Dives (one section per pillar)
For each of 5 pillars:
- Heading 1: "[Pillar Name] — [Score] / 100"
- Sub-signal table (2 columns: Sub-Signal | Score), Score cell shaded by score range
- 3 bullets labeled **🟢 Bullish:**, **🟡 Mixed / Watch:**, **🔴 Bearish / Risk:** — each with a specific cited data point

### 11. Key Signals to Watch (next 30–90 days)
- Heading 1: "Key Signals to Watch"
- 4–6 bullets. Each names a specific metric, threshold, or event date

### 12. Methodology Note
- Heading 1: "Methodology"
- 1 short paragraph (3 sentences max) explaining: the five-pillar framework + composite weighting + that scores are point-in-time

---

## Document Output

After completing the analysis, save it as a Word document using `python-docx`.

- **Output path:** `Outputs/market_sentiment_{theme}_{yyyymmdd}.docx`
  - `{theme}` = lowercased theme, spaces replaced with underscores (e.g., `edge_ai_compute`, `broad_market`)
  - `{yyyymmdd}` = today's date

Write and execute a Python script saved as `Outputs/generate_market_sentiment_{theme}_{yyyymmdd}.py` and run with `.venv/Scripts/python`. The script must:

1. Create the document with title heading matching the theme.
2. **Set portrait orientation and narrow page margins** immediately after `Document()`:
   ```python
   from docx.shared import Inches
   for section in doc.sections:
       section.orientation = 0  # WD_ORIENT.PORTRAIT
       section.page_width = Inches(8.5)
       section.page_height = Inches(11)
       section.top_margin = Inches(0.5)
       section.bottom_margin = Inches(0.5)
       section.left_margin = Inches(0.75)
       section.right_margin = Inches(0.75)
   ```
3. **Generate all 4 (or 5) charts inline using yfinance + matplotlib** before building the body. Save each PNG to `Outputs/sentiment_{slug}_<chart>.png`. Use `matplotlib.use("Agg")`. Embed each at `width=Inches(7.0)` in Section 7.
4. Render all 12 output sections with appropriate headings, paragraphs, tables, and bullet points.
5. **Tables:** initialize with `rows=1` (header only), then `table.add_row()` per data row. **Every table** must call `autofit_table(table)` then `add_table_borders(table)` AFTER all rows are added.
6. **Font size 12 on every data row** — call `set_row_font_size(row)` immediately after `table.add_row()` (don't call on header).
7. **Color-shade Score cells** in Sections 3, 8, 10 using the `w:shd` XML element (color rules per section).

Import shared helpers (script lives in `Outputs/` and runs from project root):
```python
import sys; sys.path.insert(0, '.')
from doc_utils import autofit_table, add_table_borders, set_row_font_size
```

**Helpful chart snippet** — use this pattern for the S&P 500 trend chart and adapt for VIX / yield curve / theme ETF:
```python
import yfinance as yf
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def chart_price_with_ma(symbol, title, out_path, period="2y"):
    hist = yf.Ticker(symbol).history(period=period)
    if hist.empty:
        return False
    closes = hist['Close']
    ma50 = closes.rolling(50).mean()
    ma200 = closes.rolling(200).mean()
    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.plot(closes.index, closes, label="Price", color="#222", linewidth=1.5)
    ax.plot(ma50.index, ma50, label="50-Day MA", color="#4285F4", linewidth=1.2)
    ax.plot(ma200.index, ma200, label="200-Day MA", color="#EA4335", linewidth=1.5)
    ax.fill_between(closes.index, closes, ma200,
                    where=(closes >= ma200), color="#34A853", alpha=0.12)
    ax.fill_between(closes.index, closes, ma200,
                    where=(closes <  ma200), color="#EA4335", alpha=0.12)
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.legend(loc="upper left", fontsize=10)
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()
    return True
```

If a chart's data fetch fails (e.g., ^TNX or ^FVX returns empty), skip that chart and add a small italic note in the doc instead of crashing.

---

## Post-Document Prose Summary (chat output, after saving)

After saving the file, write 4–6 short bullets (no prose paragraph) covering:
- The composite reading and what it means in plain English
- Bull or bear market verdict + 1-sentence reason
- Bubble territory verdict + 1-sentence reason
- Strongest bullish pillar
- Biggest risk / bearish signal
- One specific data point or event to watch most closely
