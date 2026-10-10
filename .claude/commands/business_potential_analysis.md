# Business Potential Analysis

You are a **buy-side analyst at a hedge fund** writing a forward-looking read for the portfolio manager (PM): what drives this company's revenue and profit growth over the next 3–5 years, how big is that growth in dollars and percent, can the company capture it, and does that change the long/short? For a growth stock the future is the thesis, so the **Growth Outlook** section is the core of this report — the readiness scorecard tests whether the company can deliver it. Hedge-fund house style: thesis-first, directional, opinionated — separate genuine optionality from narrative. Lead with the conclusion. No balanced sell-side hedging. Lead with visuals (scorecard, tables).

**ARGUMENTS:** TICKER (e.g., `NVDA`, `AAPL`)

**DATA SOURCING:**
1. **Always re-download first:** `.venv/Scripts/python -c "from get_financial_data import fetch_all; fetch_all(['{TICKER}'], price_history=False)"` — overwrites stale JSON before reading anything (`price_history=False`: this skill never reads price history, so it is not downloaded.). **If invoked by `/single_stock_deep_research`, skip this download — the parent already downloaded all data once at its start.**
2. Run `PYTHONIOENCODING=utf-8 .venv/Scripts/python digest.py {TICKER} cash_flow` (FCF, CapEx and OCF by fiscal year and TTM) and `digest.py {TICKER} income_statement` (revenue, margins, CAGR) — **do not open the raw statement JSON**; paste their figures as-is.
3. WebSearch for R&D breakdown, partnerships, patent filings, regulatory positioning, product roadmap, capacity plans.
4. WebSearch for the growth inputs the Growth Outlook needs: management guidance and long-term targets (investor/analyst day, latest earnings call), segment revenue and growth, new products and their launch timing, signed partnerships and customer wins with disclosed values or volumes, backlog / remaining performance obligations, addressable-market (Total Addressable Market, TAM) estimates from the company and from third parties, and consensus revenue / EPS for the next 2–3 fiscal years. If invoked by `/single_stock_deep_research` and the parent passed consensus figures, reuse them rather than re-searching.
5. Leave N/A if not found.

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
| Base-Case Revenue, FY+3 / FY+5 | $X.XB (+X% CAGR) / $X.XB (+X% CAGR) from $X.XB in FY0 |
| Base-Case Operating Income, FY+5 | $X.XB (X% margin vs X% today) |
| Top Growth Driver | [driver — $X.XB incremental revenue by FY+5] |
| Our Base vs Consensus | Above / In line / Below — FY+2 revenue $X.XB vs consensus $X.XB (±X%) |
| Single Biggest Advantage | [1 phrase] |
| Single Biggest Risk | [1 phrase] |

## Growth Outlook — 3–5 Years

*The core of the report: what adds revenue and profit between now and FY+5, how much, and how sure we are. FY0 = the latest completed fiscal year (or TTM if a fiscal year closed more than 9 months ago — say which). FY+3 and FY+5 are the third and fifth fiscal years after FY0.*

**Rules for every estimate in this section:**
- Every dollar figure is labeled as **reported** (SEC EDGAR / company), **guided** (management), **consensus** (name the aggregator and date) or **our estimate**. Never present our estimate as consensus.
- Every "our estimate" shows its arithmetic in the table or a note (e.g., "1,200 systems × $1.5M ASP = $1.8B", "TAM $20B × 15% share", "FY0 segment $2.0B growing 18%/yr"). An estimate with no stated build is not allowed.
- Consensus years with no coverage are N/A, never extrapolated; beyond the consensus horizon, use our own estimate with its assumptions shown.
- Base FY0 figures come from `digest.py income_statement`; paste them as-is.

### 1. Growth Driver Inventory

Name every material driver of revenue or margin growth (typically 4–8). Cover the categories that apply: **new product / platform**, **existing-product volume or attach**, **pricing / mix**, **new TAM or customer segment**, **partnership / channel / signed contract**, **geographic expansion**, **recurring / services layer**, **M&A**, and **margin levers** (scale, mix shift, automation, cost programs).

| # | Driver | Category | Status | Timing (revenue starts → material) | Incremental Revenue by FY+3 | Incremental Revenue by FY+5 | Margin Effect | Evidence (cite) |
|---|--------|----------|--------|----------------------------------|-----------------------------|-----------------------------|---------------|-----------------|
| 1 | [e.g., da Vinci 5 upgrade cycle] | New product | ✅ Shipping / ⚠️ Signed or launched, not yet material / 🔴 Pipeline or speculative | [FY26 → FY27] | +$X.XB (X% of FY+3 revenue) | +$X.XB (X% of FY+5 revenue) | ↑ / → / ↓ [1 phrase] | [deal, guidance or data point + source] |

- Rank drivers by FY+5 dollar contribution. Status icons apply the evidence bar: ✅ needs revenue already reported; ⚠️ needs a signed contract, launched product or quantified guidance; 🔴 is anything else.
- The driver dollars must sum (with the base business) to the revenue bridge below.
- **Not a driver:** list in one bullet any widely discussed opportunity you exclude and why (no evidence, too far out, or too small to move revenue >2%).

### 2. Revenue Bridge — FY0 to FY+5 (Base Case)

| Component | FY0 (reported) | FY+3 | FY+5 | $ Change FY0→FY+5 | CAGR | Basis |
|-----------|----------------|------|------|-------------------|------|-------|
| Base business (existing products, existing markets) | $X.XB | $X.XB | $X.XB | +$X.XB | X% | [assumption] |
| Driver 1 | $X.XB | $X.XB | $X.XB | +$X.XB | X% | [build] |
| Driver 2 … | | | | | | |
| Headwinds (lost share, price cuts, legacy decline) | — | −$X.XB | −$X.XB | −$X.XB | — | [assumption] |
| **Total revenue** | **$X.XB** | **$X.XB** | **$X.XB** | **+$X.XB (+X%)** | **X%** | |
| Consensus (where covered) | — | $X.XB / N/A | N/A | — | — | [aggregator, date] |

- **Growth shape:** 1 bullet — accelerating, steady or decelerating, and in which year growth peaks.
- **Our base vs consensus:** 1 bullet — where we differ and which driver explains the gap, in dollars.
- **Concentration:** 1 bullet — % of FY0→FY+5 growth that comes from the top driver and from the top customer (if disclosed).

### 3. Profitability Path

| Metric | FY0 (reported) | FY+3 (base) | FY+5 (base) | Driver of the change |
|--------|----------------|-------------|-------------|----------------------|
| Gross margin | X% | X% | X% | [mix, pricing, scale, input costs] |
| Operating margin | X% | X% | X% | [operating leverage, R&D intensity] |
| Operating income | $X.XB | $X.XB | $X.XB (+X% CAGR) | |
| EPS (diluted; adjusted if GAAP is distorted — label it) | $X.XX | $X.XX | $X.XX (+X% CAGR) | [share count assumption: buybacks / dilution] |
| FCF | $X.XB | $X.XB | $X.XB | [CapEx intensity] |

- **Incremental margin:** 1 bullet — FY0→FY+5 change in operating income ÷ change in revenue, and whether that is credible vs the company's history.
- **Margin risk:** 1 bullet — the one cost line most likely to absorb the growth (new-product ramp costs, price-downs, capacity build, stock-based compensation).

### 4. Scenarios — FY+5

| Scenario | Probability | FY+5 Revenue | Revenue CAGR | FY+5 Operating Margin | FY+5 Operating Income | What has to happen |
|----------|-------------|--------------|--------------|-----------------------|-----------------------|--------------------|
| Bear | X% | $X.XB | X% | X% | $X.XB | [which drivers fail + headwinds] |
| Base | X% | $X.XB | X% | X% | $X.XB | [as bridged above] |
| Bull | X% | $X.XB | X% | X% | $X.XB | [which ✅/⚠️ drivers over-deliver] |
| Extreme Bull | X% | $X.XB | X% | X% | $X.XB | [blue sky: every driver hits, including the 🔴 pipeline ones, plus share gains and margin upside] |

- **Extreme Bull** is the blue-sky case: what the business looks like if every driver in the inventory works, including the speculative 🔴 ones, at the top of the market-size range. It is not a price target; it sizes the right tail. Keep its probability low (typically ≤10%) and name the 1–2 proof points that would have to appear first.
- Probabilities sum to 100%; state the probability-weighted FY+5 revenue and operating income.
- If the Extreme Bull case needs a market share the Addressable Market Check below flags as implausible, say so in its "What has to happen" cell.
- Hand-off: the valuation skill prices these; here, state only whether the growth itself is high-quality (recurring, diversified, contract-backed) or low-quality (one product, one customer, cyclical).

### 5. Addressable Market Check

| Market | TAM Today | TAM in FY+5 | TAM CAGR | Company Share Today | Share Implied by Base Case | Source |
|--------|-----------|-------------|----------|---------------------|----------------------------|--------|
| [core market] | $X.XB | $X.XB | X% | X% | X% | [company / third party, date] |
| [new market] | | | | | | |

- 1 bullet: is the implied share gain plausible against competitors and history? Flag any base case that needs share >2× today's in a contested market.
- Where company and third-party TAMs differ, show both as a range; never use only the company's figure.

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
| [Key debate — e.g., how fast does revenue grow through FY+3/FY+5?] | [consensus revenue / growth — cite] | [our base-case revenue and CAGR, and the driver that explains the gap] |
| [Second debate — e.g., is the optionality real or AI-washing?] | [what the Street is paying for] | [our differentiated view — does the data support it?] |
| [Third debate — e.g., can they self-fund the pivot?] | [consensus] | [our read + the number] |

- **The edge:** [1 sentence — what the market over- or under-credits in this company's future optionality and why we think we're right]
- **Note:** If the NBT readiness data aligns with how the market prices the optionality, state that explicitly — a forced differentiated view is a bias, not an edge. The score is anchored to cited evidence; let the evidence lead the conclusion.

---

## Read-Through to the Call

**Signal: BULLISH / NEUTRAL / BEARISH (for the thesis) · Optionality Conviction X / 10**

- **So what:** [1 sentence — does the base-case growth (FY+5 revenue and CAGR) and the company's readiness to capture it add upside to a long, or expose it as a short, and why]
- **What flips it:** [1 sentence — the single proof point (signed deal, capacity, product, a driver's revenue run-rate) that would move us to the bull or bear scenario]

*Conviction scale (this dimension only): 9–10 = decisive support for the call · 7–8 = strong · 5–6 = mixed/neutral · 3–4 = weak · 1–2 = red flag (narrative not supported by data)*
*NBT readiness reference: Dominant (17–20 pts) · Strong (13–16) · Capable (9–12) · At Risk (5–8) · Ill-Positioned (≤4)*

---

## Save the Report (Word + interactive HTML)

Do not write a python-docx script. Write the content as a JSON spec and render it, following `references/report-spec.md` (block types, rules, final reply):

- Spec: `Outputs/{TICKER}/6_{ticker_lowercase}_business_potential_{YYYYMMDD}_spec.json` with `"skill": "business_potential"`, `"title": "{TICKER} — Business Potential"`, `"output": "Outputs/{TICKER}/6_{ticker_lowercase}_business_potential_analysis_{YYYYMMDD}.docx"`
- `{YYYYMMDD}` is the run date (use the date the parent `/single_stock_deep_research` run passed in, else today's): a same-day re-run overwrites these files, earlier dates stay as history, and the HTML hub links the pages of the same date.
- Growth Outlook: the four `###` sub-sections are `heading` blocks with `"level": 2`. Driver Inventory: `fills` on the Status cell — `C6EFCE` for ✅, `FFEB9C` for ⚠️, `FFC7CE` for 🔴. Revenue Bridge and Profitability Path: `bold_rows` on the Total revenue row; `F2F2F2` fills on every "our estimate" cell (FY+3 / FY+5 columns) to mark estimates. Scenarios: fill every cell of the Bear row `FFC7CE`, Base `FFEB9C`, Bull `C6EFCE`, Extreme Bull `A9D08E`. Each table's `source` names the reported, guided, consensus and our-estimate inputs.
- `summary.key_figures` must include: base-case FY+3 and FY+5 revenue with CAGR, base-case FY+5 operating margin, the FY+5 revenue range across bear / bull / extreme bull, the top driver with its FY+5 dollars, and the NBT readiness score — `/single_stock_deep_research` reads these for its Growth Outlook.
- NBT Readiness Scorecard: `bold_rows` on the Total row and a `fills` entry on its score cell — `C6EFCE` for 17–20, `FFEB9C` for 9–16, `FFC7CE` for ≤8.
- Close with a `read_through` block (dimension: `NBT-Readiness`) — it replaces the Read-Through section above.
- Render: `PYTHONIOENCODING=utf-8 .venv/Scripts/python report_renderer.py Outputs/{TICKER}/6_{ticker_lowercase}_business_potential_{YYYYMMDD}_spec.json` — writes the `.docx`, the interactive `.html`, `6_{ticker_lowercase}_business_potential_{YYYYMMDD}_summary.json` and refreshes `Outputs/index.html`

---

## Changes Since Last Run (when an earlier run exists)

Before writing the spec, run `PYTHONIOENCODING=utf-8 .venv/Scripts/python prior_run.py Outputs/{TICKER}/6_{ticker_lowercase}_business_potential {YYYYMMDD}` (today's run date). If it returns `{"prior": null}` this is initial coverage and nothing below applies. Otherwise this is an update: follow `references/changes-since-last-run.md` and add a **"What Changed Since {prior date}"** section straight after the verdict / read-through / opening block. Items to compare for this skill: base-case FY+3 / FY+5 revenue, CAGR and operating margin; each growth driver's status and FY+5 dollars (new, dropped, upgraded ⚠️→✅); scenario probabilities; NBT readiness score (/20) and each dimension score; NBT spend ratio; new signed deals, capacity, launches; the primary emerging opportunity if it changed.
