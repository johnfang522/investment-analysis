---
description: >
  Builds a professional Word document (.docx) market sentiment report for any industry theme (e.g. edge AI compute, optical interconnect, power infrastructure) or the broad stock market. Use this skill whenever the user asks to measure, score, or report on market sentiment, investor positioning, or theme-level sentiment signals. Also trigger for requests like "how bullish is the market on X", "what's the sentiment for Y theme", "build me a sentiment report", "score the setup for Z sector", "analyze investor sentiment for [theme]", or "save sentiment analysis to a Word doc". Always use this skill even if the user doesn't explicitly say "sentiment framework" — any request to gauge or document market mood, positioning, or investor enthusiasm for a theme qualifies.
---

# Market Sentiment Framework — Word Document Output

This skill produces a professionally formatted `.docx` sentiment report scored across five signal pillars.

---

## Instructions

The user has invoked `/market_sentiment_framework` with the following argument: `$ARGUMENTS`

If `$ARGUMENTS` is empty, ask the user to specify a theme, sector, or "broad market" to analyze.

Otherwise, treat `$ARGUMENTS` as the theme to analyze. Use `WebSearch` to gather current signals for each pillar before scoring. If the theme is well-known (edge AI compute, optical interconnect, power infrastructure, broad market S&P 500), weight the searched data heavily and be specific. If you lack sufficient data for a confident score on any pillar, set it to 50 and note "Insufficient data" in that pillar's signals.

---

## The Five Pillars

Score each pillar 0–100 (0 = maximally bearish, 50 = neutral, 100 = maximally bullish).

| Pillar | What it measures | Key data sources |
|---|---|---|
| **Positioning & Flows** | Where money is actually moving | Fund flows (ICI), CFTC net futures, margin debt, short interest, ETF inflows, 13F filings |
| **Price Momentum & Breadth** | Are prices rising broadly or narrowly? | % above 200-day MA, advance/decline, 52-wk highs/lows, relative strength, estimate revisions |
| **Valuation & Earnings** | How expensive vs. fundamentals? | Fwd P/E, P/S, EV/EBITDA vs. medians, equity risk premium, EPS revisions, FCF yield |
| **Macro & Conditions** | External environment supporting the theme? | Credit spreads, financial conditions, yield curve, capex guidance, policy tailwinds, supply chain |
| **Narrative & Media Sentiment** | What's the prevailing story? | NLP news scoring, Google Trends, analyst upgrades/downgrades, conference tone, earnings mentions |

## Composite Score Formula

```
Composite = (Positioning × 20%) + (Momentum × 25%) + (Valuation × 20%) + (Macro × 20%) + (Narrative × 15%)
```

Interpretation:
- 75–100 → Extreme Greed
- 60–74 → Greed / Bullish
- 45–59 → Neutral
- 30–44 → Fear / Cautious
- 0–29  → Extreme Fear

---

## Pillar Scoring Guide

For each pillar, determine scores by searching for current evidence and surfacing **3 concrete signals**:
- **Bullish** — a specific data point supporting the bull case
- **Mixed / Watch** — a nuanced or conflicting signal
- **Bearish / Risk** — a specific downside or caution flag

Also score **4 sub-signals per pillar** on the same 0–100 scale; average them to arrive at the pillar score.

### Positioning & Flows sub-signals
1. ETF/fund flows (net inflows = bullish; outflows = bearish)
2. CFTC or institutional net futures positioning
3. Short interest trend (falling = bullish; rising = bearish)
4. Margin debt / leverage level

### Price Momentum & Breadth sub-signals
1. % of theme stocks above 200-day MA
2. Advance/decline or 52-wk high/low ratio
3. Relative strength vs. benchmark (S&P 500 or sector index)
4. EPS / revenue estimate revision breadth

### Valuation & Earnings sub-signals
1. Forward P/E vs. 5-year median
2. P/S or EV/EBITDA vs. sector median
3. EPS revision trend (up = bullish)
4. FCF yield or equity risk premium

### Macro & Conditions sub-signals
1. Credit spreads (tight = bullish; wide = bearish)
2. Financial conditions index
3. Capex guidance trend for key customers / suppliers
4. Policy / regulatory tailwinds or headwinds

### Narrative & Media Sentiment sub-signals
1. News sentiment score (positive vs. negative coverage volume)
2. Google Trends search interest (rising = bullish)
3. Analyst upgrade/downgrade ratio (last 30 days)
4. Earnings call mention frequency trend

---

## Research Process

Before scoring, use `WebSearch` to gather current evidence for each pillar:

1. Search for recent fund flows, ETF inflows/outflows, and short interest data for the theme.
2. Search for current price performance, breadth statistics, and estimate revision trends.
3. Search for current valuation multiples and analyst earnings estimates.
4. Search for macro data: credit spreads, policy developments, capex guidance from major players.
5. Search for news sentiment, analyst upgrades/downgrades, and earnings call tone in the last 30–60 days.

Cite specific data points, dates, and sources inline. Do not rely on training data alone for flows, valuations, or analyst actions — these change rapidly.

---

## Output Format

Produce the following sections in order, then save as a Word document.

### 1. Cover Block
- Report title: "[Theme Name] — Market Sentiment Report"
- Subtitle: "Five-Pillar Sentiment Framework"
- Date: today's date
- Composite score (large, bold)
- One-line sentiment label (e.g., "Bullish · 64 / 100")

### 2. Executive Summary (1 paragraph)
Composite reading, key takeaway, strongest bullish pillar, biggest risk pillar, one specific data point to watch.

### 3. Composite Score Scorecard (table)
Summary table: all five pillars, their scores, and a one-line verdict each. Final row is the weighted composite.

| Pillar | Score | Reading |
|---|---|---|
| Positioning & Flows | XX | [one-line verdict] |
| Price Momentum & Breadth | XX | [one-line verdict] |
| Valuation & Earnings | XX | [one-line verdict] |
| Macro & Conditions | XX | [one-line verdict] |
| Narrative & Media Sentiment | XX | [one-line verdict] |
| **Composite** | **XX** | **[label]** |

### 4. Pillar Deep Dives (one section per pillar)
For each pillar:
- Heading: pillar name + score (e.g., "Positioning & Flows — 62 / 100")
- Sub-signal table: 4 sub-signals with their 0–100 scores
- Signal bullets: 3 bullets (Bullish / Mixed / Bearish) with specific cited data points

### 5. Key Signals to Watch
Bullet list of 4–6 specific data points or events the reader should monitor over the next 30–90 days. Be precise — include metric names, thresholds, or event dates where known.

### 6. Methodology Note
Short paragraph explaining the five-pillar framework, composite weighting, and that scores are point-in-time assessments based on available data at the time of generation.

---

## Document Output

After completing the analysis, save it as a Word document using `python-docx`.

- **Output path:** `Outputs/market_sentiment_{theme}_{yyyymmdd}.docx`
  - Replace `{theme}` with the theme argument, lowercased, spaces replaced with underscores (e.g., `edge_ai_compute`, `broad_market`).
  - Replace `{yyyymmdd}` with today's date in YYYYMMDD format.
  - Example: `Outputs/market_sentiment_edge_ai_compute_20260511.docx`

Write and execute a Python script using `.venv/Scripts/python` that:

1. Creates the document with a title heading matching the theme.
2. **Set portrait orientation and narrow page margins** immediately after creating the document:
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
3. Renders all 6 output sections with appropriate headings, paragraphs, tables, and bullet points as specified in the Per-Section Formatting Rules below.
4. For all tables, uses `python-docx` table objects. Always initialize tables with `rows=1` (header only), then call `table.add_row()` for each data row. Never pass a pre-sized `rows` count.
5. **Every table must use AutoFit to Contents and have visible borders — applied AFTER all rows are added.** The critical rule: `autofit_table` and `add_table_borders` must be called **after** all data rows have been added, not at creation time. Use this pattern for every table without exception:
   ```python
   table = doc.add_table(rows=1, cols=N)
   # ... populate header row ...
   # ... add all data rows with table.add_row() ...
   autofit_table(table)      # call AFTER all rows are added
   add_table_borders(table)  # call AFTER all rows are added
   ```

   Import the shared helpers from `doc_utils.py` (in the project root):
   ```python
   import sys; sys.path.insert(0, '.')
   from doc_utils import autofit_table, add_table_borders, set_row_font_size
   ```

6. **All non-header table cell text must use font size 12.** Call `set_row_font_size(row)` on every data row immediately after `table.add_row()`. Do **not** call it on the header row.
7. Saves the file to the output path above.

---

## Per-Section Formatting Rules

### Section 1 — Cover Block
- Heading 1: the report title (e.g., "Edge AI Compute — Market Sentiment Report")
- Below the title, add a bold paragraph: "Five-Pillar Sentiment Framework"
- Add a normal paragraph with the date: "Date: YYYY-MM-DD"
- Add a bold paragraph with the composite score displayed prominently: "Composite Score: XX / 100"
- Add a bold paragraph with the sentiment label: e.g., "Bullish · 64 / 100"

### Section 2 — Executive Summary
- Heading 1: "Executive Summary"
- Write as a single prose paragraph (4–6 sentences). Cover composite reading, strongest bullish pillar, biggest risk pillar, and one specific data point to watch.

### Section 3 — Composite Score Scorecard
- Heading 1: "Composite Score Scorecard"
- Table with 3 columns: Pillar | Score | Reading
- Apply score-based background shading to the Score cell of each data row using the `w:shd` XML element:
  - Score ≥ 65: `C6EFCE` (light green)
  - Score 50–64: `FFEB9C` (light yellow)
  - Score 35–49: `FFEB9C` (light yellow / amber)
  - Score < 35: `FFC7CE` (light red)
- The final row (Composite) should be bold in all cells.

### Section 4 — Pillar Deep Dives
For each of the 5 pillars:
- Heading 1: "[Pillar Name] — [Score] / 100" (e.g., "Positioning & Flows — 62 / 100")
- Sub-signal table with 2 columns: Sub-Signal | Score
  - Apply score-based background shading (same color rules as Section 3) to the Score cell of each row.
- After the table, write 3 bullet points labeled **Bullish:**, **Mixed / Watch:**, and **Bearish / Risk:** — each with a specific cited data point.

### Section 5 — Key Signals to Watch
- Heading 1: "Key Signals to Watch"
- Write 4–6 bullet points using Word List Bullet style. Each bullet must be specific: name the metric, threshold, or event date where possible.

### Section 6 — Methodology Note
- Heading 1: "Methodology"
- Write as a single prose paragraph (3–5 sentences) explaining the five-pillar framework, composite weighting, and the point-in-time nature of the scores.

---

## Post-Document Prose Summary

After saving the file, write 3–5 sentences in chat covering:
- The composite reading and what it means in plain English
- The strongest bullish pillar and why
- The most significant risk or bearish signal
- One specific data point or event to watch most closely
