---
name: market-sentiment
description: >
  Comprehensive broad market sentiment analysis tool. Use this skill whenever the user asks about: market sentiment, whether the market is bullish or bearish, bubble territory, market health, investor fear or greed, credit stress, equity valuation, market risk, or any combination of indicators like VIX, CNN Fear & Greed, put/call ratio, market breadth, credit spreads, Shiller PE / CAPE, or Buffett indicator. Also trigger when user asks "is the market overvalued", "should I be worried about a crash", "what does the bond market say about stocks", or "give me a market dashboard". Always use this skill — never try to answer market sentiment questions from memory alone.
---

# Market Sentiment Analysis Skill

**House style — buy-side, for the PM.** This is the top-down risk-posture overlay for a hedge-fund book. The deliverable is a directional **net-exposure call** (Risk-On / Neutral / Risk-Off) with a conviction score and an explicit variant view — not a neutral market summary. Lead with the call; the indicators justify it.

## What this skill produces

- **10 time-series chart PNGs** saved to `Outputs/` — 5-year history for each of the 7 sentiment indicators, plus Treasury yields, the US fiscal picture, and margin debt
- **A combined dashboard PNG** — `Outputs/sentiment_dashboard_{YYYYMMDD}.png`
- **A Word document** saved to `Outputs/market_sentiment_analysis_{YYYYMMDD}.docx` containing:
  1. **A risk-posture verdict** — Risk-On / Neutral / Risk-Off net-exposure call, conviction X/10, and a suggested gross/hedge tilt
  2. **A composite sentiment score** (0–100, very bearish → very bullish) synthesized from all 7 indicators
  3. **An indicator summary table** — all 7 indicators with current value, score, and signal
  4. **Per-indicator sections** — current reading, trend, interpretation, and embedded 5-year chart for each indicator
  5. **A Macro & Policy Outlook** — Fed commentary, interest-rate guidance, US fiscal deficit, and Treasury yields, each rated Tailwind / Neutral / Headwind for risk assets over the next 3–6 months, with embedded yield and fiscal charts
  6. **A Market Leverage (Margin Debt) analysis** — margin debt level, margin debt / GDP over time, YoY growth rate, and the historical record of crashes that followed critical margin levels, with embedded margin debt chart
  7. **A variant view** — where our read diverges from consensus positioning
  8. **A bubble/crash risk verdict** — Low / Moderate / Elevated / Extreme, with reasoning
  9. **Overall market opinion** — 2–4 paragraphs of analytical prose *(closing section)*

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

Then search for the **macro & policy overlay** inputs (used in Step 3.5 — not part of the composite score):

```
8.  "FOMC statement Fed chair press conference latest 2026"     ← most recent meeting + tone shift
9.  "Fed officials speeches rate outlook recent"                ← notable speaker commentary since the meeting
10. "Fed dot plot rate cut expectations CME FedWatch 2026"      ← market-implied path vs Fed guidance
11. "10 year 2 year treasury yield current 2026"                ← levels + 3-month trend
12. "US federal deficit treasury issuance auction demand 2026"  ← run-rate, refunding, bid-to-cover
13. "FINRA margin debt latest reading level year over year"     ← level, YoY growth, margin debt / GDP
```

For these, collect the *forward-looking* picture: the date and expected outcome of the next FOMC meeting, how many cuts/hikes the market is pricing over the next 6 months, whether recent Fed commentary shifted hawkish or dovish versus the prior meeting, the deficit run-rate and any signs of weak auction demand (tails, falling bid-to-cover), and the direction of the 10Y since the last FOMC.

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

## Step 3.5 — Macro & Policy Overlay (next 3–6 months)

The 7 indicators measure where sentiment **is**; this overlay assesses where it is likely to **go** over the next few months. Using the Step 1 searches (items 8–12), analyze four factors:

1. **Fed commentary** — the most recent FOMC statement/minutes/press conference plus notable Fed speakers since. Did the tone shift hawkish or dovish versus the prior meeting? Quote or paraphrase the one line that matters most.
2. **Interest-rate guidance** — the Fed's dot plot / stated path versus the market-implied path (CME FedWatch). How many cuts or hikes are priced over the next 6 months? A wide gap between Fed guidance and market pricing is repricing risk in whichever direction the gap closes.
3. **US fiscal deficit** — trailing-12M deficit run-rate, upcoming Treasury issuance/refunding calendar, auction demand (bid-to-cover, tails), and the net interest burden. Heavy supply into weak demand pushes term premium and long yields up regardless of Fed policy.
4. **Treasury yields** — 10Y and 2Y levels, the 3-month trend, and curve shape. The 10Y is the discount rate for equities: a sustained move above ~4.5% pressures the multiples that CAPE and the Buffett Indicator already flag as stretched; a falling 10Y can rescue an expensive market.

For each factor, assign a rating — **Tailwind / Neutral / Headwind** for risk assets over the next 3–6 months — with one line of reasoning citing the specific number (e.g., "10Y at 4.8% and rising into a $2T deficit run-rate = Headwind").

**Interplay check** — flag the dangerous and benign combinations explicitly:
- Rising 10Y + heavy issuance + hawkish Fed = multiple-compression risk even when VIX is calm and the composite score looks fine
- Dovish pivot + falling yields can sustain an expensive market longer than valuation indicators alone suggest
- Rate cuts driven by *deteriorating growth* are not the same tailwind as cuts into a resilient economy — say which one this is

**Posture adjustment rule:** the overlay does **not** enter the composite score (it is forward-looking policy, not coincident sentiment), but it may adjust the final call:
- 3+ of 4 factors are Headwinds → cap the posture at Neutral and/or reduce conviction by 1
- 3+ of 4 factors are Tailwinds → add 1 conviction, or upgrade a borderline Neutral to Risk-On
- Otherwise → no adjustment; the composite stands
- Whatever the outcome, state the net overlay (Tailwind / Neutral / Headwind) and any adjustment applied explicitly in the Risk Posture section

Close with **dated upcoming catalysts** — the next FOMC meeting, the next CPI/PCE print, and the next quarterly refunding announcement, each with its date and what would move the posture.

---

## Step 3.7 — Market Leverage (Margin Debt) Analysis

Margin debt measures how much of the market's buying is funded with borrowed money — it is the purest gauge of speculative leverage, and it *amplifies* whatever the market does next. Using the Step 1 search (item 13), analyze **three dimensions, not just the level**:

1. **Level** — the current FINRA margin debt reading in $B/$T, and whether it is at/near a record. A record nominal level alone is weak evidence (nominal records are common in rising markets).
2. **Margin debt / GDP over time** — the level normalized by the economy. This is the structural gauge: cyclical peaks near **~2.8% (2000)**, **~2.6% (2007)**, and **~3.8–4.0% (2021)** each marked major tops. Compare today's ratio against those peaks explicitly.
3. **YoY growth rate** — the timing gauge. YoY growth **> +40–50%** has occurred in only a few clusters since 1997 — **late 1999–early 2000, mid-2007, and spring 2021** — every one a late-cycle environment that preceded a major drawdown within ~1–2 years. Sharp *contraction* in margin debt is the confirmation signal of a deleveraging spiral already underway (1929, 1987, 2000, 2008, 2020 all saw forced-selling margin contractions accelerate the decline).

**Critical-level crash record — cite this table in the report:**

| Episode | Margin signal at the peak | What followed |
|---|---|---|
| 1929 | Broker loans ≈ 12% of NYSE market cap; call-loan rates spiking | −89% Dow peak-to-trough; margin calls drove the cascade |
| Mar 2000 | Margin/GDP ~2.8% record; YoY growth >+50% | Dot-com crash, S&P −49%; margin debt fell ~50% |
| Jul 2007 | Margin/GDP ~2.6%; YoY growth >+50% mid-2007 | GFC, S&P −57%; margin contraction amplified the decline |
| Oct 2021 | Margin/GDP ~3.8–4.0% record; YoY growth >+70% (spring 2021) | 2022 bear market, S&P −25% |

**Interpretation rules:**
- Margin debt is an **amplifier and a sentiment thermometer, not a timing trigger** — peaks in margin debt *coincide with or slightly lead* market peaks, but the lag can be months.
- The dangerous combination is **record margin/GDP + YoY growth in the historical crash-cluster zone (>+40–50%) + a hawkish/tightening rate backdrop** — leverage built at low rates meets a rising cost of carry.
- Rate the margin picture — **Low / Elevated / Critical** — and state explicitly which historical episode today's readings most resemble. This rating feeds the Bubble Risk section (a Critical margin reading argues for bumping the bubble verdict up one notch if it is borderline) and belongs in the chat summary.

Chart data note: the 5-year history chart uses the quarterly Fed Z.1 margin-loans series (FRED `BOGZ1FL663067003Q`); FINRA's monthly statistics are more current — use the web-searched FINRA number for the current reading and the chart for the trend.

---

## Step 4 — Present findings in chat

Write a concise summary in chat covering:
- **Risk-posture verdict up front:** Risk-On / Neutral / Risk-Off, conviction X/10, and the suggested tilt (e.g., "raise gross," "trim and hedge," "stay defensive")
- Composite score and zone label
- Which 1–2 indicators are most concerning and why
- The bond market / credit spread signal specifically
- **Macro overlay:** one line — net Tailwind / Neutral / Headwind from Fed commentary + rate path + fiscal + Treasury yields over the next 3–6 months, and whether it adjusted the posture
- **Margin debt:** one line — Low / Elevated / Critical, the level, margin/GDP vs. the 2000/2007/2021 peaks, and the YoY growth rate
- **Variant view:** one line on where this read differs from consensus positioning

Keep this to 5–7 short bullet points, lead with the posture call.

---

## Step 4.5 — Generate 5-year time-series charts

Before writing the Word document, generate historical time-series charts for all 10 indicators by running the chart script:

```
.venv/Scripts/python plot_market_sentiment_history.py
```

**If the script does not exist yet**, write it to `plot_market_sentiment_history.py` using the template below, then run it. The script fetches 5 years of data and saves 10 PNGs plus a combined dashboard to `Outputs/`:

| File | Indicator | Source |
|---|---|---|
| `sentiment_vix.png` | VIX | yfinance `^VIX` |
| `sentiment_breadth.png` | Market Breadth (RSP vs SPY) | yfinance RSP + SPY |
| `sentiment_hy_oas.png` | HY OAS Spread | FRED `BAMLH0A0HYM2` |
| `sentiment_cape.png` | Shiller CAPE | multpl.com scrape |
| `sentiment_buffett.png` | Buffett Indicator | yfinance `^FTW5000` + FRED GDP, normalised to current known value |
| `sentiment_fear_greed.png` | CNN Fear & Greed | CNN dataviz API (`production.dataviz.cnn.io`) |
| `sentiment_putcall.png` | CBOE SKEW Index (put-demand proxy) | yfinance `^SKEW` — the CBOE equity P/C ratio is not freely available historically post-2019; SKEW measures the same underlying demand for downside protection |
| `sentiment_treasury_yields.png` | Treasury Yields — 10Y, 2Y + 10Y−2Y curve panel | FRED `DGS10`, `DGS2` |
| `sentiment_fiscal.png` | US Fiscal — trailing-12M deficit + net interest outlays | FRED `MTSDS133FMS`, `A091RC1Q027SBEA` |
| `sentiment_margin_debt.png` | Margin Debt — level ($B) + margin debt / GDP panel | FRED `BOGZ1FL663067003Q` (Z.1 margin loans) + FRED GDP |
| `sentiment_dashboard_{YYYYMMDD}.png` | Combined dashboard | assembled from the 10 individual PNGs |

**Key implementation notes for the chart script:**
- FRED `WILL5000IND` was removed in June 2024 — use `^FTW5000` from yfinance instead
- FRED CSV responses have `DATE` as the first column but may include a disclaimer header; parse robustly by finding the line starting with `DATE`
- **HY OAS unit conversion:** FRED `BAMLH0A0HYM2` returns values in percentage points (e.g. `2.78`), not basis points. Always multiply by 100 before plotting so the y-axis and reference lines (`300`, `500`, `700`) are in bps and match the data
- For the Buffett Indicator, normalise the `^FTW5000 / GDP` ratio to the current known Buffett Indicator value (~233% as of May 2026) using an anchor point on the most recent date
- CNN Fear & Greed: fetch from `https://production.dataviz.cnn.io/index/fearandgreed/graphdata` (JSON, `fear_and_greed_historical.data`, `x` = ms timestamp, `y` = score)
- SKEW chart: annotate that it is used as a put/call proxy
- **Treasury yields:** FRED `DGS10` / `DGS2` are in percent — plot directly; add a lower panel with the 10Y−2Y spread (shaded red below zero = inversion) and reference lines at 4.5% (equity valuation headwind) and 5.0% on the yield panel
- **Fiscal:** FRED `MTSDS133FMS` (monthly federal surplus/deficit) is in **$ millions with deficit months negative** — take the rolling 12-month sum, negate, and divide by 1e6 to plot the trailing-12M deficit in $T (positive = deficit); fetch it with a start date ~13 months before the chart window so the rolling window is complete at the left edge. `A091RC1Q027SBEA` (federal net interest outlays) is quarterly, SAAR, in $B — plot in a lower panel
- **Margin debt:** FRED `BOGZ1FL663067003Q` (Z.1 "security brokers and dealers; margin loans receivable") is **quarterly, in $ millions** — divide by 1e3 for $B on the level panel; divide by FRED `GDP` (in $B) and ×100 for the margin/GDP panel, with reference lines at 2.6% (2007 peak), 2.8% (2000 peak), and 3.8% (2021 peak). FINRA's monthly margin statistics are more current than the quarterly Z.1 series but have no free CSV endpoint — the current reading comes from the Step 1 web search, the chart from FRED

The script template is in `plot_market_sentiment_history.py` from the prior session — update the `END` date to today before running.

---

## Step 5 — Save to Word Document

Write and execute a Python script using `python-docx` (`.venv/Scripts/python`) that saves the full analysis to `Outputs/market_sentiment_analysis_{YYYYMMDD}.docx`.

Save the script itself to `Outputs/generate_market_sentiment_analysis_{YYYYMMDD}.py` and run it from the project root.

### Document structure

**Portrait, narrow margins** (top/bottom 0.5", left/right 0.75") — see the standard block in CLAUDE.md.

**Title block**
- Title: `Market Sentiment Analysis` (bold, centered, 18pt)
- Subtitle: date (centered, italic)

**Section 1 — Risk Posture (Verdict)** *(place first, right after the title block)*
- Heading 1: `Risk Posture`
- Large bold text colored by call: `Risk-On` (green `007000`) / `Neutral` (neutral dark) / `Risk-Off` (red `C00000`), followed by `· Conviction X/10`
- A small 2-column table: `Posture | …`, `Conviction | X/10`, `Composite Score | XX/100`, `Macro overlay (3–6 mo) | Tailwind / Neutral / Headwind [+ adjustment applied, if any]`, `Suggested tilt | e.g. "trim gross, add hedges"`, `Key swing factor | [1 phrase]`
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

**Section 5 — Macro & Policy Outlook**
- Heading 1: `Macro & Policy Outlook (Next 3–6 Months)`
- A table with columns: `Factor | Current Reading | Expected Path (3–6 mo) | Market Impact | Signal` — one row each for `Fed commentary`, `Rate guidance`, `Fiscal deficit`, `Treasury yields`; Signal values: `Tailwind` / `Neutral` / `Headwind`
- Same table rules: `rows=1`, `add_row()`, `set_row_font_size()`, `autofit_table()`, `add_table_borders()`
- **Embed `sentiment_treasury_yields.png` and `sentiment_fiscal.png`** with `doc.add_picture(path, width=Inches(6.5))`
- One short paragraph per factor: what was said / what is priced, and how it feeds through to market sentiment over the next few months (per Step 3.5)
- A bold line: `Net macro overlay: Tailwind / Neutral / Headwind` — plus the posture adjustment applied, or "no adjustment; composite stands"
- A short bullet list of **dated upcoming catalysts** (next FOMC meeting, next CPI/PCE print, next quarterly refunding announcement) with what each could change

**Section 6 — Market Leverage (Margin Debt)**
- Heading 1: `Market Leverage — Margin Debt`
- Bold rating line: `Margin Picture: Low / Elevated / Critical`
- A table with columns: `Dimension | Current Reading | Historical Benchmark | Signal` — one row each for `Level ($B/$T)`, `Margin Debt / GDP`, `YoY Growth Rate` (benchmarks: the 2000/2007/2021 peaks per Step 3.7)
- **Embed `sentiment_margin_debt.png`** with `doc.add_picture(path, width=Inches(6.5))`
- The **critical-level crash record table** from Step 3.7 (`Episode | Margin signal at the peak | What followed`) rendered as a 3-column table
- One short paragraph: which historical episode today's readings most resemble, why margin debt is an amplifier rather than a timing trigger, and how this rating feeds the Bubble Risk verdict
- Same table rules: `rows=1`, `add_row()`, `set_row_font_size()`, `autofit_table()`, `add_table_borders()`

**Section 7 — Variant View**
- Heading 1: `Variant View — Consensus vs. Our Read`
- A 3-column table: `Debate | Consensus / Positioning | Our Read` (e.g., debate over whether tight credit spreads are complacency or justified; whether narrow breadth is a warning or normal late-cycle leadership; whether the market-implied rate path or the Fed's guidance is right)
- One bold bullet: `The edge:` — what consensus positioning is mispricing right now and why our posture differs. If the indicator readings confirm the market's current risk posture, state that explicitly — a forced contrarian view is a bias, not an edge.

**Section 8 — Bubble / Crash Risk**
- Heading 1: `Bubble Risk Assessment`
- Bold verdict label: `Risk Level: Low / Moderate / Elevated / Extreme`
- 3–5 bullet points listing which indicators are in warning zones and why
- 2–3 sentences of analytical reasoning, incorporating the margin debt rating from Section 6 (a Critical margin reading argues for bumping a borderline verdict up one notch)

**Section 9 — Market Opinion** *(closing section — always last, immediately before the footer)*
- Heading 1: `Overall Market Opinion`
- 2–4 paragraphs of analytical prose covering:
  - What the composite score means in context
  - The most concerning indicators and why
  - The bond market / credit spread signal specifically
  - How the Fed path, fiscal/issuance picture, Treasury yield trend, and margin leverage are likely to move sentiment over the next few months
  - Overall verdict: cautious / neutral / confident

**Footer**
- Call `add_footnote(doc)` immediately before `doc.save(...)` to append the standard AI disclaimer

### Import the shared helpers

```python
import sys; sys.path.insert(0, '.')
from doc_utils import autofit_table, add_table_borders, set_row_font_size, add_footnote, fmt_value
```
Use `fmt_value(v)` for all dollar amounts in table cells (auto-scales: ≥$1B → `$X.XXB`, ≥$1M → `$X.XM`, ≥$1K → `$X.XK`). Never hardcode `/ 1e9` or manually append `"B"`.

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
