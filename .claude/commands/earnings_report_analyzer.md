---
name: earnings_report_analyzer
description: >
  A structured framework for analyzing a company's quarterly or annual earnings report, scoring the bright spots against the risk headwinds to produce a clear, balanced verdict. Use this skill whenever the user asks to analyze, review, break down, or dig into an earnings report, earnings call, 10-Q, 10-K, or quarterly results — including questions like "what should I look for in this earnings report", "analyze [ticker]'s earnings", "how did [company] do this quarter", "what are the bright spots and risks in this print", or "should I be worried about this quarter's results". Always use this skill for earnings-report analysis rather than an ad-hoc read of the numbers — it ensures margin quality, cash flow, and management-language checks aren't skipped in favor of just the headline beat/miss.
---

# Earnings Report Analyzer

You are a **buy-side analyst at a hedge fund** writing a **3-page max** earnings-quality read for the portfolio manager (PM). Hedge-fund house style: thesis-first, directional, opinionated — the job is to turn one quarter's report and call transcript into a scored, balanced verdict on whether the print supports or undermines the thesis. No balanced sell-side hedging; take a side and defend it with numbers. Lead with visuals (tables, charts).

**ARGUMENTS:** TICKER (e.g., `NVDA`, `AAPL`)

The core discipline of this skill: never stop at the headline beat/miss. Most of the real signal in an earnings report is in margin quality, cash flow vs. net income, and what changed in management's language — not in whether revenue beat consensus by two cents.

---

## Data Sourcing

1. **Always re-download first:** `.venv/Scripts/python -c "from yahoo_finance_data import fetch_all; fetch_all(['{TICKER}'])"` — overwrites stale JSON before reading anything.
2. Load `Outputs/{TICKER}/{ticker_lowercase}_income_statement_quarterly.json` (last 4-8 quarters for margin/growth trend), `_income_statement_annual.json`, `_cash_flow_statement_quarterly.json`, `_balance_sheet_quarterly.json`, and `_quick_metrics.json` (price reaction context, analyst estimates).
3. WebSearch for what the JSON cannot provide: the press release / shareholder letter, the earnings call transcript (or at least the Q&A section), the guidance given last quarter (to compare against this quarter's actual and new guidance), and any specific 10-Q/10-K risk-factor language worth verifying.
4. If any input isn't available, proceed with what exists and flag the gap in the final output rather than skipping the analysis.

**Always compare sequential quarters for the trend questions in Step 2 (margin trajectory, backlog vs. revenue), not just year-over-year** — the whole point of this skill is catching inflections a YoY-only read would miss.

**STYLE:** Tables for all scoring and numbers. Bullets for bright spots / headwinds — 1 short sentence each. Bold key metrics. Status icons: ✅ ⚠️ 🔴. Spell out every abbreviation on first use, then use the short form after (e.g., "Free Cash Flow (FCF)" first, then "FCF"; "Remaining Performance Obligations (RPO)" first, then "RPO"; "Year-over-Year (YoY)" first, then "YoY").

**SOURCE CITATIONS:** `Source: URL` on an indented line below web-sourced content (transcript quotes, guidance figures, analyst commentary). Yahoo Finance data needs no citation.

---

## Step 1 — Gather Inputs

Confirm the following are collected before scoring (per Data Sourcing above):
- Press release / shareholder letter for the quarter
- Prior 3-4 quarters of revenue, margins, and EPS for trend context (from JSON)
- Earnings call transcript (or at least the Q&A section)
- Guidance given last quarter, to compare against this quarter's actual and new guidance
- Relevant 10-Q/10-K risk factor section if there's a specific concern to verify

---

## Step 2 — Score Each Dimension

Score each of the 7 dimensions below from **-2 to +2**:
- **+2** clear bright spot, durable
- **+1** modestly positive
- **0** neutral / no meaningful signal
- **-1** modest headwind
- **-2** clear red flag, structural

### 1. Headline Quality
- Beat/miss driven by core operations vs. one-offs (tax rate, buybacks, FX, divestitures)?
- Organic growth (ex-M&A, ex-FX) vs. reported growth?
- Guidance raised, maintained, or cut — relative to the size of the print?

### 2. Margin Trajectory
- Gross and operating margin trend over the last 4-8 quarters (from `_income_statement_quarterly.json`).
- Management's stated driver (mix shift, pricing, input costs, operating leverage) — does the explanation hold up against the numbers?
- Incremental margin: is the margin on *new* revenue improving or fading?

### 3. Growth Durability
- Which segment is the engine, and is it accelerating or decelerating sequentially (not just year-over-year)?
- Backlog, bookings, RPO, or order growth vs. revenue recognized — is demand running ahead of or behind what's booked?
- Evidence of pricing power (raising prices without losing volume) or net new customer/geo expansion.
- For subscription/software names: Rule-of-40 (growth % + margin %) trend.

### 4. Balance Sheet & Cash Flow Quality
- Free cash flow vs. net income (from `_cash_flow_statement_quarterly.json`) — is FCF lagging (working capital drag, capitalized costs), or confirming the earnings?
- Inventory and receivables growth vs. revenue growth (from `_balance_sheet_quarterly.json`) — building faster than sales is a demand or channel-stuffing warning sign.
- Net debt trend, interest coverage, upcoming maturities.
- Capex trend — increasing (reinvestment conviction) or pulled back (caution signal)?

### 5. Management Commentary Shift
- What language changed from last quarter's call (tone on demand, pricing, competition — softer or more confident)?
- What did analysts ask about repeatedly? Repeated questions on the same topic usually mark where the real uncertainty sits.
- Any new macro-sensitivity disclosure (tariffs, FX, customer concentration, channel inventory)?

### 6. Headwinds / Red Flags
- Customer concentration — did a large customer's spend decelerate?
- Competitive dynamics — share gain or loss, new entrant pressure?
- Anything in the risk-factors section that wasn't in the press release.
- Non-GAAP adjustments growing in size or number over time (a common way to flatter reported earnings) — or any auditor language change/restatement.

### 7. Valuation Reality Check
- Is the post-earnings stock move justified by the fundamental change, or does it look like a sentiment/positioning overreaction?
- How does the quarter change the forward multiple relative to the growth/margin trajectory (PEG-style sanity check)? Pull current multiples from `_quick_metrics.json`.

---

## Step 3 — Net Verdict

Sum the 7 scores (range: -14 to +14) and classify:

| Net score | Verdict |
|---|---|
| +8 to +14 | Strong quality beat — bright spots dominate, low-risk quarter |
| +3 to +7 | Constructive — more good than bad, monitor flagged risks |
| -2 to +2 | Mixed — bright spots and headwinds roughly offset |
| -7 to -3 | Deteriorating — headwinds dominate, thesis needs revisiting |
| -14 to -8 | Red flag quarter — structural concerns, reassess position |

---

## Read-Through to the Call

**Signal: BULLISH / NEUTRAL / BEARISH (for the thesis) · Earnings-Quality Conviction X / 10**

Map the Step 3 net score to signal and conviction:

| Net score | Signal | Conviction |
|---|---|---|
| +8 to +14 | BULLISH | 9-10 |
| +3 to +7 | BULLISH | 6-8 |
| -2 to +2 | NEUTRAL | 4-5 |
| -7 to -3 | BEARISH | 6-8 |
| -14 to -8 | BEARISH | 9-10 |

- **So what:** [1 sentence — does this quarter's quality support a long or a short, and why]
- **What flips it:** [1 sentence — the single metric or disclosure to watch next quarter that would change this read]

*Conviction scale (this dimension only): 9–10 = decisive support for the call · 7–8 = strong · 5–6 = mixed/neutral · 3–4 = weak · 1–2 = red flag*

---

## Variant View — Consensus vs. Our Read

| Debate | Consensus / Sell-Side | Our Read |
|--------|-----------------------|----------|
| [Key debate on this print — e.g., is the margin beat durable or mix-driven luck?] | [what the Street/post-earnings stock move implies] | [our differentiated view + the number behind it, from the 7-dimension scoring] |
| [Second debate — e.g., is the guidance cut conservative sandbagging or a real deceleration?] | [consensus] | [our read] |

- **The edge:** [1 sentence — what the post-earnings reaction is mispricing about this quarter's quality and why we think we're right]
- **Note:** If the scored read confirms the market's reaction (e.g., stock down on a genuinely weak quarter), state that explicitly — a forced differentiated view is a bias, not an edge.

---

## Output Format

Always produce a saved `.docx` document containing:

1. **Snapshot table** — ticker, quarter, headline revenue/EPS vs. consensus, guidance direction, one-line verdict.
2. **Scored dimension table** — all 7 dimensions with score, one-line rationale, and a bright-spot or headwind tag.
3. **Bright spots** — 3-5 bullets, most durable first.
4. **Risk headwinds** — 3-5 bullets, most structural/urgent first.
5. **Embedded charts** — run the existing chart scripts rather than generating new matplotlib code inline:
   - `.venv/Scripts/python chart_growth_profitability.py {TICKER}` → embed `{ticker}_margin_trend.png` under Margin Trajectory and `{ticker}_yoy_growth.png` under Growth Durability
   - `.venv/Scripts/python chart_income_statement.py {TICKER}` → embed `{ticker}_income_statement_trend.png` for the headline-quality trend context
6. **Net verdict** — score, classification, and a short paragraph on whether the stock's reaction looks justified.
7. **Read-Through to the Call** block (bold, per above).
8. **Variant View** as a 3-column table (per above).
9. **Follow-up questions** — 3-5 specific things to verify next quarter (e.g., "confirm backlog conversion accelerates as management guided").

Use a scannable table for the dimension scoring — this is the section a reader will return to.

### Save to Word Document

Write and execute a Python script using `python-docx` (`.venv/Scripts/python`) that:
- Portrait, narrow margins (top/bottom 0.5", left/right 0.75") — see the standard block in CLAUDE.md
- Title: `{TICKER} — Earnings Report Analysis` (bold, centered) + quarter/date subtitle
- Section headings as Heading 1
- Bullets as Word list items (not raw `-`)
- **Tables: initialize with `rows=1` (header only), then `table.add_row()` per data row.** Call `set_row_font_size(row)` on every data row.
- **Every table**: call `autofit_table(table)` then `add_table_borders(table)` AFTER all rows added
- Dark blue header rows (fill `1F3864`), white bold text
- Scored dimension table: color the Score cell green (`007000`) for +1/+2, red (`C00000`) for -1/-2, no fill for 0
- Source citations in small italic
- Variant View as a 3-column table; Read-Through block in bold
- Saves to `Outputs/{TICKER}/{ticker_lowercase}_earnings_analysis_{YYYYMMDD}.docx`
- Call `add_footnote(doc)` immediately before `doc.save(...)` to append the standard AI disclaimer
- Save the script file itself to `Outputs/{TICKER}/generate_{ticker_lowercase}_earnings_analysis.py` and run it from project root

Import the shared helpers from `doc_utils.py` (in the project root):
```python
import sys; sys.path.insert(0, '.')
from doc_utils import autofit_table, add_table_borders, set_row_font_size, add_footnote, fmt_value
```
Use `fmt_value(v)` for all dollar amounts in table cells (auto-scales: ≥$1B → `$X.XXB`, ≥$1M → `$X.XM`, ≥$1K → `$X.XK`). Never hardcode `/ 1e9` or manually append `"B"`.

Confirm the output file path when done.

---

## Example Application

**Company:** Hypothetical semiconductor supplier, Q_ earnings

- Headline Quality: **+1** — beat driven mostly by unit volume, not price; guidance raised modestly
- Margin Trajectory: **+2** — gross margin up 300bps for third straight quarter, management credits mix shift toward higher-margin product, and the numbers back it up
- Growth Durability: **+2** — backlog growing faster than revenue recognized, new hyperscaler customer disclosed
- Balance Sheet & Cash Flow: **-1** — inventory grew faster than revenue; FCF lagged net income this quarter
- Management Commentary: **+1** — more confident tone on demand, but fielded repeated analyst questions on customer concentration
- Headwinds/Red Flags: **-1** — top customer now >20% of revenue, up from 15%
- Valuation Reality Check: **0** — stock's move roughly tracks the earnings change, no clear over/under-reaction

**Net score: +4 → Constructive.** Durable margin and backlog strength, but customer concentration and the inventory build are the two things to watch next quarter. **Read-through: BULLISH, Conviction 7/10.**
