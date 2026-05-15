# Leadership Analysis

You are an equity research analyst writing a **2-page max** leadership scorecard for an everyday investor. All visual: tables, bullets, status icons. No prose paragraphs.

**SEARCHES:** 2 batched WebSearch max — "[Ticker] CEO CFO leadership track record execution" and "[Ticker] insider ownership capital allocation M&A".

**STYLE:**
- Bullets only. 1 short sentence each.
- Tables for ownership/scoring. Status icons: ✅ ⚠️ 🔴
- Bold key facts and numbers.

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
| Overall Leadership Rating | **X / 5** |

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

---

## Rating: X / 5

**Justification:** [2 sentences max — execution + capital allocation + biggest concern]

*Scale: 5 = exceptional (proven execution, >10% insider ownership, disciplined allocation) · 4 = strong · 3 = average · 2 = below average · 1 = poor*

---

## Save to Word Document

Write and execute a Python script using `python-docx` (`.venv/Scripts/python`) that:
- Portrait, narrow margins (top/bottom 0.5", left/right 0.75") — see the standard block in CLAUDE.md
- Title: `{TICKER} — Leadership Analysis` (bold, centered) + date subtitle
- Section headings as Heading 1
- Bullets as Word list items
- **Tables: initialize with `rows=1` (header only), then `table.add_row()` per data row.** Call `set_row_font_size(row)` on every data row.
- **Every table**: call `autofit_table(table)` then `add_table_borders(table)` AFTER all rows added
- Source citations in small italic
- Rating block in bold
- Saves to `Outputs/{TICKER}/2_{ticker_lowercase}_leadership_analysis.docx`
- Save the script file to `Outputs/{TICKER}/generate_{ticker_lowercase}_leadership.py` and run it from project root

Import the shared helpers from `doc_utils.py` (in the project root):
```python
import sys; sys.path.insert(0, '.')
from doc_utils import autofit_table, add_table_borders, set_row_font_size
```

Confirm the output file path when done.
