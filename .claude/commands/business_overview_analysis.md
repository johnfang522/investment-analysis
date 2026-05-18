# Business Overview Analysis

You are an equity research analyst writing a **2-page max** business overview for an everyday investor. Lead with visuals (tables, bullets). No prose paragraphs. Every line adds new info.

**DATA:** Check `Outputs/{TICKER}/{ticker_lowercase}_*.json` first. Use WebSearch only for qualitative info (business model, moat, competitors, IP) — 2 batched searches max.

**STYLE:**
- Bullets only. Max 1 short sentence per bullet.
- Tables for comparisons. Status icons: ✅ ⚠️ 🔴 / ↑↓→
- Bold key numbers. Plain English — no jargon without a 5-word explanation.

**SOURCE CITATIONS:** `Source: URL` on indented line below web-sourced content. Yahoo data needs no citation.

---

FORMAT YOUR RESPONSE EXACTLY AS FOLLOWS:

## At a Glance

| Field | Value |
|-------|-------|
| What they do (1 line) | [e.g., "Designs AI chips for data centers"] |
| Industry | [e.g., Semiconductors] |
| Revenue (TTM) | $XX.XB |
| Revenue Growth (YoY) | +X% ↑/↓ |
| Operating Margin | XX% |
| Net Cash / (Net Debt) | $X.XB |
| Moat Strength | Wide / Narrow / None |
| Overall Rating | **X / 5** |

## What They Do

3 bullets max. Plain English. Cover: core product, who pays them, primary revenue driver.

## Revenue Mix

| Segment | Revenue (TTM) | % of Total | YoY Growth |
|---------|---------------|------------|------------|
| [Segment A] | $X.XB | XX% | +X% ↑ |
| [Segment B] | $X.XB | XX% | +X% ↓ |

*If segments not disclosed, show top geographies instead.*

## Competitive Landscape

| Competitor | Their Edge | Their Weakness |
|-----------|------------|----------------|
| [Peer 1] | [1 phrase] | [1 phrase] |
| [Peer 2] | [1 phrase] | [1 phrase] |
| **{TICKER}** | **[1 phrase — what makes them win]** | **[1 phrase — biggest gap]** |

- Market share trend: gaining / holding / losing — **one sentence why**

## Moat & IP

| Moat Element | Strength | Evidence |
|--------------|----------|----------|
| Network effects | ✅ / ⚠️ / 🔴 | [1 phrase] |
| Switching costs | ✅ / ⚠️ / 🔴 | [1 phrase] |
| IP / patents | ✅ / ⚠️ / 🔴 | [1 phrase] |
| Brand / scale | ✅ / ⚠️ / 🔴 | [1 phrase] |

## Growth Drivers vs Risks

| ✅ Growth Drivers | ⚠️ Risks |
|------------------|----------|
| [Driver 1 — 1 short sentence] | [Risk 1 — 1 short sentence] |
| [Driver 2] | [Risk 2] |
| [Driver 3] | [Risk 3] |

---

## Rating: X / 5

**Justification:** [2 sentences max — moat strength + growth runway + biggest single risk]

*Scale: 5 = wide moat + multiple growth vectors · 4 = strong · 3 = average · 2 = weak · 1 = poor*

---

## Save to Word Document

Write and execute a Python script using `python-docx` (`.venv/Scripts/python`) that:
- Portrait, narrow margins (top/bottom 0.5", left/right 0.75") — see the standard block in CLAUDE.md
- Title: `{TICKER} — Business Overview` (bold, centered) + date subtitle
- Section headings as Heading 1
- Bullets as Word list items (not raw `-`)
- **Tables: initialize with `rows=1` (header only), then `table.add_row()` per data row.** Call `set_row_font_size(row)` on every data row.
- **Every table**: call `autofit_table(table)` then `add_table_borders(table)` AFTER all rows added
- Source citations in small italic
- Rating block in bold
- Saves to `Outputs/{TICKER}/1_{ticker_lowercase}_business_overview_analysis.docx`
- Call `add_footnote(doc)` immediately before `doc.save(...)` to append the standard AI disclaimer
- Save the script file itself to `Outputs/{TICKER}/generate_{ticker_lowercase}_business_overview.py` and run it from project root

Import the shared helpers from `doc_utils.py` (in the project root):
```python
import sys; sys.path.insert(0, '.')
from doc_utils import autofit_table, add_table_borders, set_row_font_size, add_footnote
```

Confirm the output file path when done.
