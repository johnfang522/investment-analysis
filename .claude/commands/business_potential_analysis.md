# Business Potential Analysis

You are a **buy-side analyst at a hedge fund** writing a **3-page max** forward-looking read for the portfolio manager (PM): can this company capitalize on the next major paradigm shift, and does that change the long/short? Hedge-fund house style: thesis-first, directional, opinionated — separate genuine optionality from narrative. Lead with the conclusion. No balanced sell-side hedging. Lead with visuals (scorecard, tables).

**ARGUMENTS:** TICKER (e.g., `NVDA`, `AAPL`)

**DATA SOURCING:**
1. **Always re-download first:** `.venv/Scripts/python -c "from get_financial_data import fetch_all; fetch_all(['{TICKER}'], price_history=False)"` — overwrites stale JSON before reading anything (`price_history=False`: this skill never reads price history, so it is not downloaded.). **If invoked by `/single_stock_deep_research`, skip this download — the parent already downloaded all data once at its start.**
2. Run `PYTHONIOENCODING=utf-8 .venv/Scripts/python digest.py {TICKER} cash_flow` (FCF, CapEx and OCF by fiscal year and TTM) and `digest.py {TICKER} income_statement` (revenue, margins, CAGR) — **do not open the raw statement JSON**; paste their figures as-is.
3. WebSearch for R&D breakdown, partnerships, patent filings, regulatory positioning, product roadmap, capacity plans.
4. Leave N/A if not found.

**STYLE:** Bullets only — 1 short sentence each. Tables for all numbers. Status icons: ✅ ⚠️ 🔴 / ↑↓→. Spell out every abbreviation on first use, then use the short form after (e.g., "Free Cash Flow (FCF)" first, then "FCF"; "Research & Development (R&D)" first, then "R&D"; "Capital Expenditures (CapEx)" first, then "CapEx").

**SOURCE CITATIONS:** `Source: URL` indented below web-sourced lines.

**REIT HANDLING (apply only if the company is a REIT — definitions and data sources in `references/reit-framework.md`):**
- Detect: `_quick_metrics.json` `industry` starts with `REIT` (or `sector` is `Real Estate`). Equity REITs follow this block; mortgage REITs (`REIT - Mortgage`) are financials, so flag it and use book value, price/book and net interest spread instead. Not a REIT: ignore this block.
- Keep every section above. Identify the REIT's emerging opportunity from sourced evidence: acquisition pipeline and addressable market, development, geographic expansion, new asset classes, and private-capital funds or joint ventures (capital-light, fee-generating growth).
- Financial runway = liquidity (cash + undrawn revolver), credit ratings, net debt/EBITDAre and the spread of acquisition yield over cost of capital; ecosystem control = tenant relationships and sourcing pipeline. R&D and headcount rows are generally not applicable.
- NBT Spend Ratio = trend-related deployment (for example a data-center joint venture or a new fund) over operating cash flow or AFFO; if trend-specific amounts are unsourced, use total investment as a labeled proxy or mark N/A. Cite each figure and show source disagreements as a range.

---

DOCUMENT CONTENT — the sections below are the document outline. Write them as blocks in the report spec (see "Save the Report"), not as a chat reply: each `##` heading is a `heading` block, each table a `table` block, each bullet list a `bullets` block.

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

## Save the Report (Word + interactive HTML)

Do not write a python-docx script. Write the content as a JSON spec and render it, following `references/report-spec.md` (block types, rules, final reply):

- Spec: `Outputs/{TICKER}/6_{ticker_lowercase}_business_potential_spec.json` with `"skill": "business_potential"`, `"title": "{TICKER} — Business Potential"`, `"output": "Outputs/{TICKER}/6_{ticker_lowercase}_business_potential_analysis.docx"`
- NBT Readiness Scorecard: `bold_rows` on the Total row and a `fills` entry on its score cell — `C6EFCE` for 17–20, `FFEB9C` for 9–16, `FFC7CE` for ≤8.
- Close with a `read_through` block (dimension: `NBT-Readiness`) — it replaces the Read-Through section above.
- Render: `PYTHONIOENCODING=utf-8 .venv/Scripts/python report_renderer.py Outputs/{TICKER}/6_{ticker_lowercase}_business_potential_spec.json` — writes the `.docx`, the interactive `.html`, `6_{ticker_lowercase}_business_potential_summary.json` and refreshes `Outputs/index.html`
