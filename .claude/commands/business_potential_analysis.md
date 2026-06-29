# Business Potential Analysis

You are a **buy-side analyst at a hedge fund** writing a **3-page max** forward-looking read for the portfolio manager (PM): can this company capitalize on the next major paradigm shift, and does that change the long/short? Hedge-fund house style: thesis-first, directional, opinionated — separate genuine optionality from narrative. Lead with the conclusion. No balanced sell-side hedging. Lead with visuals (scorecard, tables).

**ARGUMENTS:** TICKER (e.g., `NVDA`, `AAPL`)

**DATA SOURCING:**
1. **Always re-download first:** `.venv/Scripts/python -c "from yahoo_finance_data import fetch_all; fetch_all(['{TICKER}'])"` — overwrites stale JSON before reading anything.
2. Load `Outputs/{TICKER}/{ticker_lowercase}_quick_metrics.json`, `_income_statement_annual.json`, `_cash_flow_statement_annual.json`.
3. WebSearch for R&D breakdown, partnerships, patent filings, regulatory positioning, product roadmap, capacity plans.
3. Leave N/A if not found.

**STYLE:** Bullets only — 1 short sentence each. Tables for all numbers. Status icons: ✅ ⚠️ 🔴 / ↑↓→. Spell out every abbreviation on first use, then use the short form after (e.g., "Free Cash Flow (FCF)" first, then "FCF"; "Research & Development (R&D)" first, then "R&D"; "Capital Expenditures (CapEx)" first, then "CapEx").

**SOURCE CITATIONS:** `Source: URL` indented below web-sourced lines.

---

FORMAT YOUR RESPONSE EXACTLY AS FOLLOWS:

**Data as of**: [Most Recent Fiscal Year]

## At a Glance

| Field | Value |
|-------|-------|
| Primary Emerging Opportunity | [e.g., "AI inference at the edge"] |
| Next Big Thing (NBT) Readiness Score | **X / 20** — Dominant / Strong / Capable / At Risk / Ill-Positioned |
| Thesis Bias | **LONG / SHORT / PASS** |
| Conviction (Optionality) | **X / 10** |
| Single Biggest Advantage | [1 phrase] |
| Single Biggest Risk | [1 phrase] |

## NBT Readiness Scorecard

*NBT = "Next Big Thing." Four dimensions test whether the company is structurally positioned to capture the trend. Each score (0–5) must be accompanied by a specific, cited data point from the JSON or WebSearch — a score without evidence is not valid.*

| Dimension | Score | Key Evidence (must cite source) |
|-----------|-------|----------------------------------|
| 1. Value Alignment — does the trend extend the core business? | X/5 | [e.g., "Trend revenue = X% of total; moats transfer directly — source: earnings call"] |
| 2. Operational Agility — can it pivot resources fast? | X/5 | [e.g., "R&D up X% YoY from JSON; signed deal XYZ — source: press release"] |
| 3. Financial Runway — can it self-fund the transition? | X/5 | [e.g., "FCF $X.XB vs. trend capex $X.XB; net debt $X.XB — source: cash flow JSON"] |
| 4. Ecosystem Control — does it own a toll booth? | X/5 | [e.g., "Controls X% of market; NVLink Fusion partnership — source: WebSearch"] |
| **Total** | **X/20** | |

## Value Alignment

| Question | Verdict | Evidence (1 phrase) |
|----------|---------|---------------------|
| Does the trend solve a core problem for existing customers? | ✅ / ⚠️ / 🔴 | [phrase] |
| Do current moats extend (data, brand, IP, distribution)? | ✅ / ⚠️ / 🔴 | [phrase] |
| Is the legacy business sticky enough to fund the pivot? | ✅ / ⚠️ / 🔴 | [phrase] |

## Operational Agility

| Metric | Value | Notes |
|--------|-------|-------|
| R&D Spend (annual) | $X.XB | X% of revenue |
| R&D Growth (YoY) | +X% | vs revenue +X% |
| Recent time-to-market | X months | [Product name] |
| Capacity Expansion | [signed deals / new fabs / etc.] | [evidence] |

- **Talent & infrastructure:** [1 sentence — generalists vs siloed specialists, scale-up readiness]
- **Forward-looking proof:** name signed contracts, customer wins, JVs, capex commitments — no growth claims without specific deals.

## Financial Runway

| Metric | Value |
|--------|-------|
| Annual Free Cash Flow | $X.XB |
| Estimated Trend Capex / R&D | $X.XB |
| **NBT Spend Ratio** | **X.Xx** (✅ <0.5 self-funding · ⚠️ 0.5–1.0 manageable · 🔴 >1.0 reliant on outside capital) |
| FCF Margin | X% |
| Net Cash / (Net Debt) | $X.XB |
| Interest Coverage | X.Xx |

- **Legacy revenue drag:** X% of revenue tied to disrupted segments — [1 sentence]

## Ecosystem Control

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

## Variant View — Consensus vs. Our Read

| Debate | Consensus / Sell-Side | Our Read |
|--------|-----------------------|----------|
| [Key debate — e.g., is the optionality real or AI-washing?] | [what the Street is paying for] | [our differentiated view — does the data support it?] |
| [Second debate — e.g., can they self-fund the pivot?] | [consensus] | [our read + the number] |

- **The edge:** [1 sentence — what the market over- or under-credits in this company's future optionality and why we think we're right]
- **Note:** If the NBT readiness data aligns with how the market prices the optionality, state that explicitly — a forced differentiated view is a bias, not an edge. The score is anchored to cited evidence; let the evidence lead the conclusion.

---

## Read-Through to the Call

**Signal: BULLISH / NEUTRAL / BEARISH (for the thesis) · Optionality Conviction X / 10**

- **So what:** [1 sentence — does the company's readiness for the next trend add upside optionality to a long, or expose it as a short, and why]
- **What flips it:** [1 sentence — the single proof point (signed deal, capacity, product) that would change this read]

*Conviction scale (this dimension only): 9–10 = decisive support for the call · 7–8 = strong · 5–6 = mixed/neutral · 3–4 = weak · 1–2 = red flag (narrative not supported by data)*
*NBT readiness reference: Dominant (17–20 pts) · Strong (13–16) · Capable (9–12) · At Risk (5–8) · Ill-Positioned (≤4)*

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
- NBT Readiness Scorecard table: bold the Total row; color score cell green (`007000`) for 17–20, orange (`FF8C00`) for 9–16, red (`C00000`) for ≤8
- Source citations in small italic
- Variant View as a 3-column table; Read-Through block in bold
- Saves to `Outputs/{TICKER}/7_{ticker_lowercase}_business_potential_analysis.docx`
- Save the script file to `Outputs/{TICKER}/generate_{ticker_lowercase}_business_potential.py` and run it from project root

Call `add_footnote(doc)` immediately before `doc.save(...)` to append the standard AI disclaimer.

Import the shared helpers from `doc_utils.py`:
```python
import sys; sys.path.insert(0, '.')
from doc_utils import autofit_table, add_table_borders, set_row_font_size, add_footnote, fmt_value
```
Use `fmt_value(v)` for all dollar amounts in table cells (auto-scales: ≥$1B → `$X.XXB`, ≥$1M → `$X.XM`, ≥$1K → `$X.XK`). Never hardcode `/ 1e9` or manually append `"B"`.

Confirm the output file path when done.
