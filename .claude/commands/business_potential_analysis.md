# Business Potential Analysis

You are a strategic equity research analyst evaluating a company's structural capacity to capitalize on the next major paradigm shift — technological, regulatory, or behavioral. This is a forward-looking, qualitative-first analysis backed by quantitative checks. Be direct, lead with evidence, skip filler.

**ARGUMENTS:** TICKER (e.g., `NVDA`, `AAPL`)

**DATA SOURCING (follow this order):**
1. Load `Outputs/{TICKER}/{ticker_lowercase}_quick_metrics.json`, `Outputs/{TICKER}/{ticker_lowercase}_income_statement_annual.json`, and `Outputs/{TICKER}/{ticker_lowercase}_cash_flow_statement_annual.json`. If files are missing, run `yahoo_finance_data.py` to fetch.
2. Use WebSearch for R&D spend breakdown, strategic partnership announcements, patent filings, regulatory positioning, product roadmap, and management commentary on growth initiatives.
3. Leave as N/A if still not found.

**SOURCE CITATIONS:** `Source: URL` indented below any web-sourced value. No citation needed for local JSON.

---

FORMAT YOUR RESPONSE EXACTLY AS FOLLOWS:

**Data as of**: [Most Recent Fiscal Year]

---

## 1. Value Alignment — The "DNA" Check

*Determines if the next big trend is a natural extension of the company or a threat to its existence.*

**The Utility Gap:** Does the trend solve a core problem for the company's existing customer base?
- [1–2 sentences with supporting evidence]

**The Moat Extension:** Can the company apply its current competitive advantages (data, brand, distribution, IP) to the new trend, or are those advantages rendered obsolete?
- [1–2 sentences with supporting evidence]

**Market Share Elasticity:** Is the legacy business "sticky" enough to provide a stable foundation while the company pivots resources toward the new trend?
- [1–2 sentences; cite retention rates, switching costs, or revenue concentration if available]

**Alignment Score: X/5** — [One sentence verdict]

---

## 2. Operational Agility — The "Engine" Check

*Measures the company's ability to pivot resources without internal collapse.*

**R&D Velocity:** How quickly has the company historically moved from proof-of-concept to global production?

| Metric | Value | Notes |
|--------|-------|-------|
| R&D Spend (Annual) | $X.XB | X% of revenue |
| R&D YoY Growth | +X% | vs. revenue growth of X% |
| Time-to-Market (recent major product) | X months | [Product name] |

- [1 sentence: is R&D spend rising or declining relative to revenue?]

**Talent Density:** Does the workforce consist of generalist problem-solvers who can be reassigned, or siloed specialists tied to legacy tech?
- [1–2 sentences based on hiring trends, workforce composition, or management commentary]

**Infrastructure Elasticity:** Can the digital or physical supply chain scale 10x in 12 months if the trend hits an inflection point?
- [1–2 sentences; cite capacity expansion plans, cloud/manufacturing partnerships, or capex trajectory]

**Agility Score: X/5** — [One sentence verdict]

---

## 3. Solvency & Financial Buffer — The "Oxygen" Check

*Analyzes the ability to survive the "Trough of Disillusionment" when a trend isn't yet profitable.*

**FCF Coverage (NBT Spend Ratio):**

Formula: NBT Spend Ratio = Projected Trend Capex / Annual Free Cash Flow

| Metric | Value |
|--------|-------|
| Annual Free Cash Flow | $X.XB |
| Estimated Trend-Related Capex / R&D | $X.XB |
| NBT Spend Ratio | X.Xx |
| FCF Margin | X% |

- Ratio < 0.5x = self-funding capacity; 0.5–1.0x = manageable; > 1.0x = reliant on debt or equity

**Legacy Revenue Drag:** What percentage of revenue is tied to the industry the trend disrupts?
- [1–2 sentences; estimate legacy vs. growth segment mix if reported]

**Interest Coverage:**

| Metric | Value |
|--------|-------|
| EBIT | $X.XB |
| Interest Expense | $X.XB |
| Interest Coverage Ratio | X.Xx |
| Net Cash / (Net Debt) | $X.XB |

- [1 sentence: can the company service debt while scaling R&D simultaneously?]

**Solvency Score: X/5** — [One sentence verdict]

---

## 4. Positioning & Ecosystem Power — The "Gravity" Check

*Assesses whether the company will control the new industry or simply participate in it.*

**The Toll Booth Factor:** Does the company own a critical, non-negotiable part of the new infrastructure (e.g., a standard platform, a unique patent, or a distribution bottleneck)?
- [1–2 sentences with specific examples]

**Strategic Partnerships:** Is the company building an open ecosystem that gains mass adoption, or a closed system that risks becoming a niche player?
- [1–2 sentences citing key partnerships, alliances, or platform integrations]

**Regulatory Foresight:** Is the company helping to write the new rules of the game, or waiting to be told how to operate?
- [1–2 sentences on regulatory engagement, lobbying posture, or standards-body participation]

**Positioning Score: X/5** — [One sentence verdict]

---

## NBT Readiness Scorecard

*NBT = Next Big Thing. Scores reflect the company's capacity to capitalize on its primary emerging opportunity.*

| Dimension | Score | Key Evidence |
|-----------|-------|--------------|
| 1. Value Alignment (DNA) | X/5 | [One-phrase summary] |
| 2. Operational Agility (Engine) | X/5 | [One-phrase summary] |
| 3. Solvency & Buffer (Oxygen) | X/5 | [One-phrase summary] |
| 4. Ecosystem Power (Gravity) | X/5 | [One-phrase summary] |
| **Overall NBT Readiness** | **X/20** | |

**Readiness Rating: X/5**

Scale: 5 = Dominant (17–20 pts, multiple structural advantages) · 4 = Strong (13–16 pts) · 3 = Capable (9–12 pts) · 2 = At Risk (5–8 pts) · 1 = Ill-Positioned (≤4 pts)

[2–3 sentences: name the specific trend being evaluated, the company's single biggest structural advantage, and the single biggest execution risk.]

---

## Strengths

3 bullet points, specific evidence required.

## Risks

3 bullet points, specific evidence required.

---

## Save to Word Document

Write and execute a Python script using `python-docx` (`.venv/Scripts/python`) that:
- Narrow margins (0.5 inch all sides)
- Title: `{TICKER} — Business Potential Analysis` (bold heading) + date subtitle
- Section headings as Heading 1; sub-dimension labels as Heading 2; bullets as Word list items
- **Tables: initialize with `rows=1` (header only), then `table.add_row()` per data row**
- Dark blue header rows (fill `1F3864`), white bold text; source citations in small italic
- NBT Readiness Scorecard table: bold the Overall row; color the score cell based on rating (green `007000` for 4–5, orange `FF8C00` for 3, red `C00000` for 1–2)
- Rating block in bold
- Saves to `Outputs/{TICKER}/{ticker_lowercase}_business_potential_analysis.docx`

Confirm the output file path when done.
