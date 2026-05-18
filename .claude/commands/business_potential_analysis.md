# Business Potential Analysis

You are an equity research analyst writing a **3-page max** forward-looking analysis: can this company capitalize on the next major paradigm shift? Lead with visuals (scorecard, tables). Plain English.

**ARGUMENTS:** TICKER (e.g., `NVDA`, `AAPL`)

**DATA SOURCING:**
1. Load `Outputs/{TICKER}/{ticker_lowercase}_quick_metrics.json`, `_income_statement_annual.json`, `_cash_flow_statement_annual.json`. Run `yahoo_finance_data.py` if missing.
2. WebSearch for R&D breakdown, partnerships, patent filings, regulatory positioning, product roadmap, capacity plans.
3. Leave N/A if not found.

**STYLE:** Bullets only — 1 short sentence each. Tables for all numbers. Status icons: ✅ ⚠️ 🔴 / ↑↓→

**SOURCE CITATIONS:** `Source: URL` indented below web-sourced lines.

---

FORMAT YOUR RESPONSE EXACTLY AS FOLLOWS:

**Data as of**: [Most Recent Fiscal Year]

## At a Glance

| Field | Value |
|-------|-------|
| Primary Emerging Opportunity | [e.g., "AI inference at the edge"] |
| NBT Readiness Score | **X / 20** |
| Readiness Rating | **X / 5** — Dominant / Strong / Capable / At Risk / Ill-Positioned |
| Single Biggest Advantage | [1 phrase] |
| Single Biggest Risk | [1 phrase] |

## NBT Readiness Scorecard

*NBT = "Next Big Thing." Four dimensions test whether the company has the DNA, Engine, Oxygen, and Gravity to win the trend.*

| Dimension | Score | Key Evidence (1 phrase) |
|-----------|-------|-------------------------|
| 1. Value Alignment (DNA) — does the trend extend the business? | X/5 | [e.g., "Trend solves a core problem for top customers"] |
| 2. Operational Agility (Engine) — can it pivot resources fast? | X/5 | [e.g., "R&D up X%; 12-mo time-to-market"] |
| 3. Solvency & Buffer (Oxygen) — can it survive the trough? | X/5 | [e.g., "FCF $X.XB covers 3x trend capex"] |
| 4. Ecosystem Power (Gravity) — will it own infrastructure? | X/5 | [e.g., "Owns the standard platform; key patent"] |
| **Total** | **X/20** | |

## DNA — Value Alignment

| Question | Verdict | Evidence (1 phrase) |
|----------|---------|---------------------|
| Does the trend solve a core problem for existing customers? | ✅ / ⚠️ / 🔴 | [phrase] |
| Do current moats extend (data, brand, IP, distribution)? | ✅ / ⚠️ / 🔴 | [phrase] |
| Is the legacy business sticky enough to fund the pivot? | ✅ / ⚠️ / 🔴 | [phrase] |

## Engine — Operational Agility

| Metric | Value | Notes |
|--------|-------|-------|
| R&D Spend (annual) | $X.XB | X% of revenue |
| R&D Growth (YoY) | +X% | vs revenue +X% |
| Recent time-to-market | X months | [Product name] |
| Capacity Expansion | [signed deals / new fabs / etc.] | [evidence] |

- **Talent & infrastructure:** [1 sentence — generalists vs siloed specialists, scale-up readiness]
- **Forward-looking proof:** name signed contracts, customer wins, JVs, capex commitments — no growth claims without specific deals.

## Oxygen — Solvency & Financial Buffer

| Metric | Value |
|--------|-------|
| Annual Free Cash Flow | $X.XB |
| Estimated Trend Capex / R&D | $X.XB |
| **NBT Spend Ratio** | **X.Xx** (✅ <0.5 self-funding · ⚠️ 0.5–1.0 manageable · 🔴 >1.0 reliant on outside capital) |
| FCF Margin | X% |
| Net Cash / (Net Debt) | $X.XB |
| Interest Coverage | X.Xx |

- **Legacy revenue drag:** X% of revenue tied to disrupted segments — [1 sentence]

## Gravity — Positioning & Ecosystem Power

| Question | Verdict | Evidence (1 phrase) |
|----------|---------|---------------------|
| Toll booth — owns critical infrastructure? | ✅ / ⚠️ / 🔴 | [e.g., "Standard CUDA platform"] |
| Open ecosystem or closed niche? | ✅ Open / ⚠️ Mixed / 🔴 Closed | [phrase] |
| Helping write the rules (regulatory engagement)? | ✅ / ⚠️ / 🔴 | [phrase] |

## Strengths vs Risks

| ✅ Structural Advantages | ⚠️ Execution Risks |
|--------------------------|---------------------|
| [Advantage 1 — specific evidence] | [Risk 1 — specific evidence] |
| [Advantage 2] | [Risk 2] |
| [Advantage 3] | [Risk 3] |

---

## Readiness Rating: X / 5

**Justification:** [2–3 sentences — name the specific trend + single biggest structural advantage + single biggest execution risk]

*Scale: 5 = Dominant (17–20 pts) · 4 = Strong (13–16) · 3 = Capable (9–12) · 2 = At Risk (5–8) · 1 = Ill-Positioned (≤4)*

---

## Save to Word Document

Write and execute a Python script using `python-docx` (`.venv/Scripts/python`) that:
- Portrait, narrow margins (top/bottom 0.5", left/right 0.75") — see CLAUDE.md
- Title: `{TICKER} — Business Potential` (bold, centered) + date subtitle
- Section headings as Heading 1
- Bullets as Word list items
- **Tables: initialize with `rows=1` (header only), then `table.add_row()` per data row.** Call `set_row_font_size(row)` on every data row.
- **Every table**: call `autofit_table(table)` then `add_table_borders(table)` AFTER all rows added
- Dark blue header rows (fill `1F3864`), white bold text
- NBT Readiness Scorecard table: bold the Total row; color score cell green (`007000`) for 4–5, orange (`FF8C00`) for 3, red (`C00000`) for 1–2
- Source citations in small italic
- Rating block in bold
- Saves to `Outputs/{TICKER}/7_{ticker_lowercase}_business_potential_analysis.docx`
- Save the script file to `Outputs/{TICKER}/generate_{ticker_lowercase}_business_potential.py` and run it from project root

Call `add_footnote(doc)` immediately before `doc.save(...)` to append the standard AI disclaimer.

Import the shared helpers from `doc_utils.py`:
```python
import sys; sys.path.insert(0, '.')
from doc_utils import autofit_table, add_table_borders, set_row_font_size, add_footnote
```

Confirm the output file path when done.
