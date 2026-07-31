# Leadership Analysis

You are a **buy-side analyst at a hedge fund** writing a **2-page max** leadership scorecard for the portfolio manager (PM). Hedge-fund house style: thesis-first, directional, opinionated — judge management on whether they make the long/short work (capital allocation, execution, alignment). Lead with the conclusion. No balanced sell-side hedging. All visual: tables, bullets, status icons. No prose paragraphs.

**DATA FETCH — always re-download first:** Before any analysis, run:
`.venv/Scripts/python -c "from yahoo_finance_data import fetch_all; fetch_all(['{TICKER}'])"`
This ensures `Outputs/{TICKER}/` JSON files are current before reading any metrics.

**SEARCHES:** 2 batched WebSearch max — "[Ticker] CEO CFO leadership track record execution" and "[Ticker] insider ownership capital allocation M&A".

**STYLE:**
- Bullets only. 1 short sentence each.
- Tables for ownership/scoring. Status icons: ✅ ⚠️ 🔴
- Bold key facts and numbers.
- Spell out every abbreviation on first use, then use the short form after (e.g., "Mergers & Acquisitions (M&A)" first, then "M&A"; "Research & Development (R&D)" first, then "R&D").

**SOURCE CITATIONS:** `Source: URL` indented below the bullet.

---

FORMAT YOUR RESPONSE EXACTLY AS FOLLOWS:

## At a Glance

| Field | Value |
|-------|-------|
| CEO | [Name] (since YYYY) |
| CFO | [Name] (since YYYY) |
| Insider Ownership | X.X% ✅/⚠️/🔴 |
| Avg Exec Tenure | X.X years |
| Capital Allocation Style | Buybacks / Dividends / M&A / Reinvest |
| Thesis Bias | **LONG / SHORT / PASS** |
| Conviction (Management Quality) | **X / 10** |

## Leadership Scorecard

| Dimension | Score | Key Evidence (1 phrase) |
|-----------|-------|-------------------------|
| Execution Track Record | X/5 | [e.g., "Hit guidance 8 of last 10 quarters"] |
| Vision & Innovation | X/5 | [e.g., "Bet on AI early; R&D up 40%"] |
| Capital Allocation | X/5 | [e.g., "$10B buybacks at avg $XXX, smart"] |
| Transparency | X/5 | [e.g., "Owns mistakes on calls; clear guidance"] |
| Insider Alignment | X/5 | [e.g., "CEO holds 8% — high skin in the game"] |
| Team Depth | X/5 | [e.g., "Strong CFO bench; minimal turnover"] |

## Key Executives & Ownership

| Name | Role | Tenure | Stake | Recent Activity |
|------|------|--------|-------|-----------------|
| [Name] | CEO | X yr | X.X% | Buying / Selling / Holding |
| [Name] | CFO | X yr | X.X% | Buying / Selling / Holding |
| [Name] | [Role] | X yr | X.X% | — |

## Strengths vs Risks

| ✅ Strengths | ⚠️ Risks |
|-------------|----------|
| [Strength 1 — 1 short sentence with a number] | [Risk 1 — 1 short sentence with evidence] |
| [Strength 2] | [Risk 2] |
| [Strength 3] | [Risk 3] |

## Variant View — Consensus vs. Our Read

| Debate | Consensus / Sell-Side | Our Read |
|--------|-----------------------|----------|
| [Key debate on management — e.g., capital allocation discipline] | [what the Street assumes] | [our differentiated view + evidence] |
| [Second debate — e.g., succession / execution credibility] | [consensus] | [our read] |

- **The edge:** [1 sentence — what the market misjudges about this management team and why we think we're right]
- **Note:** If the data on management quality aligns with consensus, state that explicitly — a forced differentiated view is a bias, not an edge. Insider selling or weak ROIC is a fact, not a differentiated read.

---

## Read-Through to the Call

**Signal: BULLISH / NEUTRAL / BEARISH (for the thesis) · Management-Quality Conviction X / 10**

- **So what:** [1 sentence — does leadership + capital allocation support a long or a short, and why]
- **What flips it:** [1 sentence — the single event (departure, value-destructive M&A, insider selling) that would change this read]

*Conviction scale (this dimension only): 9–10 = decisive support for the call · 7–8 = strong · 5–6 = mixed/neutral · 3–4 = weak · 1–2 = red flag*

---

## Save to Word Document

Write and execute a Python script using `python-docx` (`.venv/Scripts/python`) that:
- Portrait, narrow margins (top/bottom 0.5", left/right 0.75") — see the standard block in CLAUDE.md
- Title: `{TICKER} — Leadership Analysis` (bold, centered) + date subtitle
- Section headings as Heading 1
- Bullets as Word list items
- **Tables: initialize with `rows=1` (header only), then `table.add_row()` per data row.** Call `set_row_font_size(row)` on every data row.
- **Every table**: call `autofit_table(table)` then `add_table_borders(table)` AFTER all rows added
- Dark blue header rows (fill `1F3864`), white bold text
- Source citations in small italic
- Variant View as a 3-column table; Read-Through block in bold
- Saves to `Outputs/{TICKER}/2_{ticker_lowercase}_leadership_analysis.docx`
- Save the script file to `Outputs/{TICKER}/generate_{ticker_lowercase}_leadership.py` and run it from project root

Call `add_footnote(doc)` immediately before `doc.save(...)` to append the standard AI disclaimer.

Import the shared helpers from `doc_utils.py` (in the project root):
```python
import sys; sys.path.insert(0, '.')
from doc_utils import autofit_table, add_table_borders, set_row_font_size, add_footnote, fmt_value
```
Use `fmt_value(v)` for all dollar amounts in table cells (auto-scales: ≥$1B → `$X.XXB`, ≥$1M → `$X.XM`, ≥$1K → `$X.XK`). Never hardcode `/ 1e9` or manually append `"B"`.

Confirm the output file path when done.
