---
name: market-sentiment
description: >
  Comprehensive broad market sentiment analysis tool. Use this skill whenever the user asks about: market sentiment, whether the market is bullish or bearish, bubble territory, market health, investor fear or greed, credit stress, equity valuation, market risk, or any combination of indicators like VIX, CNN Fear & Greed, put/call ratio, market breadth, credit spreads, Shiller PE / CAPE, or Buffett indicator. Also trigger when user asks "is the market overvalued", "should I be worried about a crash", "what does the bond market say about stocks", or "give me a market dashboard". Always use this skill — never try to answer market sentiment uestions from memory alone.
---

# Market Sentiment Analysis Skill

**House style — buy-side, for the PM.** This is the top-down risk-posture overlay for a hedge-fund book. The deliverable is a directional **net-exposure call** (Risk-On / Neutral / Risk-Off) with a conviction score and an explicit variant view — not a neutral market summary. Lead with the call; the indicators justify it.

## What this skill produces

- **7 time-series chart PNGs** saved to `Outputs/` — one per indicator, 5-year history
- **A combined dashboard PNG** — `Outputs/sentiment_dashboard_{YYYYMMDD}.png`
- **A Word document** saved to `Outputs/market_sentiment_{YYYYMMDD}.docx` containing:
  1. **A risk-posture verdict** — Risk-On / Neutral / Risk-Off net-exposure call, conviction X/10, and a suggested gross/hedge tilt
  2. **A composite sentiment score** (0–100, very bearish → very bullish) synthesized from all 7 indicators
  3. **An indicator summary table** — all 7 indicators with current value, score, and signal
  4. **Per-indicator sections** — current reading, trend, interpretation, and embedded 5-year chart for each indicator
  5. **A bubble/crash risk verdict** — Low / Moderate / Elevated / Extreme, with reasoning
  6. **A variant view** — where our read diverges from consensus positioning
  7. **Overall market opinion** — 2–4 paragraphs of analytical prose

---

## Step 1 — Web-search for current data

Before building anything, search for fresh readings on **all 7 indicators**. Run these searches:

```
1. "VIX current level today 2026"
2. "CNN Fear and Greed Index current reading 2026"
3. "put call ratio CBOE current 2026"
4. "RSP vs SPY performance YTD 2026"   ← market breadth proxy
5. "ICE BofA high yield OAS spread current 2026"
6. "Shiller CAPE ratio current 2026"
7. "Buffett indicator market cap GDP ratio current 2026"
```

Collect: current value, direction (rising/falling), and brief context for each.

---

## Step 2 — Score each indicator (0–100)

Convert each raw reading into a sentiment score where **0 = extreme bear / maximum stress** and **100 = extreme bull / maximum complacency**.

Read the scoring tables in `references/scoring-tables.md` to convert each raw value.

Key inversion rules:
- VIX: HIGH vix = fear = LOW score. LOW vix = calm = HIGH score.
- HY spread: WIDE spread = stress = LOW score. TIGHT spread = bullish = HIGH score.
- Shiller CAPE: HIGH cape = overvalued = LOW score (valuation bearish).
- Buffett indicator: HIGH ratio = overvalued = LOW score (valuation bearish).
- CNN F&G: score maps directly (0=extreme fear → 0, 100=extreme greed → 100).
- Put/call ratio: HIGH ratio (lots of puts) = fear = LOW score.
- Breadth (RSP vs SPY YTD gap): RSP outperforming = broad participation = HIGH score.

Apply weights from `references/scoring-tables.md` to compute composite score.

---

## Step 3 — Assess bubble risk

Read `references/bubble-framework.md` for the full assessment framework.

In brief, flag bubble risk when **3 or more** of these conditions are simultaneously true:
- Shiller CAPE > 35
- Buffett indicator > 160%
- HY spread < 300 bps (extreme complacency in credit)
- CNN F&G > 70 (greed or extreme greed)
- VIX < 15 (extreme calm)
- Breadth diverging (SPY outperforming RSP by > 5pp — narrow rally)

Write a verdict: **Low / Moderate / Elevated / Extreme** bubble risk, with 2–3 sentences of reasoning citing the specific indicators that are flashing.

---

## Step 4 — Present findings in chat

Write a concise summary in chat covering:
- **Risk-posture verdict up front:** Risk-On / Neutral / Risk-Off, conviction X/10, and the suggested tilt (e.g., "raise gross," "trim and hedge," "stay defensive")
- Composite score and zone label
- Which 1–2 indicators are most concerning and why
- The bond market / credit spread signal specifically
- **Variant view:** one line on where this read differs from consensus positioning

Keep this to 3–5 short bullet points, lead with the posture call.

---

## Step 4.5 — Generate 5-year time-series charts

Before writing the Word document, generate historical time-series charts for all 7 indicators by running the chart script:

```
.venv/Scripts/python plot_market_sentiment_history.py
```

**If the script does not exist yet**, write it to `plot_market_sentiment_history.py` using the template below, then run it. The script fetches 5 years of data and saves 7 PNGs plus a combined dashboard to `Outputs/`:

| File | Indicator | Source |
|---|---|---|
| `sentiment_vix.png` | VIX | yfinance `^VIX` |
| `sentiment_breadth.png` | Market Breadth (RSP vs SPY) | yfinance RSP + SPY |
| `sentiment_hy_oas.png` | HY OAS Spread | FRED `BAMLH0A0HYM2` |
| `sentiment_cape.png` | Shiller CAPE | multpl.com scrape |
| `sentiment_buffett.png` | Buffett Indicator | yfinance `^FTW5000` + FRED GDP, normalised to current known value |
| `sentiment_fear_greed.png` | CNN Fear & Greed | CNN dataviz API (`production.dataviz.cnn.io`) |
| `sentiment_putcall.png` | CBOE SKEW Index (put-demand proxy) | yfinance `^SKEW` — the CBOE equity P/C ratio is not freely available historically post-2019; SKEW measures the same underlying demand for downside protection |
| `sentiment_dashboard_{YYYYMMDD}.png` | Combined dashboard | assembled from the 7 individual PNGs |

**Key implementation notes for the chart script:**
- FRED `WILL5000IND` was removed in June 2024 — use `^FTW5000` from yfinance instead
- FRED CSV responses have `DATE` as the first column but may include a disclaimer header; parse robustly by finding the line starting with `DATE`
- **HY OAS unit conversion:** FRED `BAMLH0A0HYM2` returns values in percentage points (e.g. `2.78`), not basis points. Always multiply by 100 before plotting so the y-axis and reference lines (`300`, `500`, `700`) are in bps and match the data
- For the Buffett Indicator, normalise the `^FTW5000 / GDP` ratio to the current known Buffett Indicator value (~233% as of May 2026) using an anchor point on the most recent date
- CNN Fear & Greed: fetch from `https://production.dataviz.cnn.io/index/fearandgreed/graphdata` (JSON, `fear_and_greed_historical.data`, `x` = ms timestamp, `y` = score)
- SKEW chart: annotate that it is used as a put/call proxy

The script template is in `plot_market_sentiment_history.py` from the prior session — update the `END` date to today before running.

---

## Step 5 — Save to Word Document

Write and execute a Python script using `python-docx` (`.venv/Scripts/python`) that saves the full analysis to `Outputs/market_sentiment_{YYYYMMDD}.docx`.

Save the script itself to `Outputs/generate_market_sentiment_{YYYYMMDD}.py` and run it from the project root.

### Document structure

**Portrait, narrow margins** (top/bottom 0.5", left/right 0.75") — see the standard block in CLAUDE.md.

**Title block**
- Title: `Market Sentiment Analysis` (bold, centered, 18pt)
- Subtitle: date (centered, italic)

**Section 1 — Risk Posture (Verdict)** *(place first, right after the title block)*
- Heading 1: `Risk Posture`
- Large bold text colored by call: `Risk-On` (green `007000`) / `Neutral` (neutral dark) / `Risk-Off` (red `C00000`), followed by `· Conviction X/10`
- A small 2-column table: `Posture | …`, `Conviction | X/10`, `Composite Score | XX/100`, `Suggested tilt | e.g. "trim gross, add hedges"`, `Key swing factor | [1 phrase]`
- One sentence stating the net-exposure implication for the book

**Section 2 — Composite Score**
- Heading 1: `Composite Sentiment Score`
- Large bold text: score number + zone label (e.g. `67 — Bullish`)
- One sentence on what the zone means

**Section 3 — Indicator Summary Table**
- Heading 1: `Indicator Dashboard`
- Table with columns: `Indicator | Current Value | Score (0–100) | Signal | Trend`
- Signal values: `Bearish` / `Neutral` / `Bullish`
- Initialize with `rows=1` (header only), then `table.add_row()` per indicator row
- Call `set_row_font_size(row)` on every data row
- Call `autofit_table(table)` then `add_table_borders(table)` after all rows are added

**Section 4 — Per-Indicator Detail**
- Heading 1: `Indicator Detail`
- For each of the 7 indicators, a Heading 2 with the indicator name, then:
  - A short table: `Current Value | Score | Trend | Signal` (single data row)
  - A bullet or two of interpretation
  - **Embed the corresponding time-series chart PNG** using `doc.add_picture(chart_path, width=Inches(6.5))` immediately after the table — use the filenames from the table in Step 4.5
- Same table rules: `rows=1`, `add_row()`, `set_row_font_size()`, `autofit_table()`, `add_table_borders()`

**Section 5 — Bubble / Crash Risk**
- Heading 1: `Bubble Risk Assessment`
- Bold verdict label: `Risk Level: Low / Moderate / Elevated / Extreme`
- 3–5 bullet points listing which indicators are in warning zones and why
- 2–3 sentences of analytical reasoning

**Section 6 — Variant View**
- Heading 1: `Variant View — Consensus vs. Our Read`
- A 3-column table: `Debate | Consensus / Positioning | Our Read` (e.g., debate over whether tight credit spreads are complacency or justified; whether narrow breadth is a warning or normal late-cycle leadership)
- One bold bullet: `The edge:` — what consensus positioning is mispricing right now and why our posture differs

**Section 7 — Market Opinion**
- Heading 1: `Overall Market Opinion`
- 2–4 paragraphs of analytical prose covering:
  - What the composite score means in context
  - The most concerning indicators and why
  - The bond market / credit spread signal specifically
  - Overall verdict: cautious / neutral / confident

**Footer**
- Call `add_footnote(doc)` immediately before `doc.save(...)` to append the standard AI disclaimer

### Import the shared helpers

```python
import sys; sys.path.insert(0, '.')
from doc_utils import autofit_table, add_table_borders, set_row_font_size, add_footnote
```

Confirm the output file path when done.

---

## Step 6 — Offer next step

After confirming the output file path, ask the user:

> "Would you like to kick off `/emerging_industry_trend` to identify the next market trend or investment theme worth researching?"

If the user says yes (or provides a theme), invoke the `/emerging_industry_trend` skill with their input (or with no argument if they want a broad scan).

---

## Reference files

- `references/scoring-tables.md` — exact conversion tables for each indicator
- `references/bubble-framework.md` — bubble risk framework and historical analogues

Read both before scoring the indicators.
