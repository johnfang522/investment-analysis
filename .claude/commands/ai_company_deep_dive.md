---
name: ai-company-deep-dive
description: A structured framework for conducting a comprehensive deep dive on any company with meaningful AI exposure. Use this skill whenever a user wants to analyze, research, evaluate, or build an investment thesis on a company in the AI sector — including pure-play AI companies, AI infrastructure plays, semiconductor companies, cloud providers with AI exposure, AI-enabled SaaS, or any stock where AI is a meaningful growth driver. Trigger on phrases like "deep dive on [ticker]", "analyze [company] as an AI investment", "should I invest in [AI company]", "break down [ticker]", "help me research [company]", "build a thesis on [company]", or any request to evaluate a company with AI exposure in depth. Always use this skill for AI investment questions rather than responding ad-hoc. Takes a stock ticker as input.
---

# Company Deep Dive Framework

**Input:** A stock ticker symbol (e.g., `NVDA`, `MSFT`, `PLTR`).

**House style — buy-side, for the PM.** Write this as a senior hedge-fund analyst building a book position for the portfolio manager. Thesis-first, directional, opinionated: the deliverable is a **LONG / SHORT / PASS** call with a conviction score, price target, stop, and risk/reward — not a balanced sell-side profile. Lead every section with the conclusion ("so what for the trade?"). The variant view (where we differ from consensus) and the chokepoint analysis are the core value-add.

**Important — objectivity first:** Before proceeding, assess whether the company genuinely has AI as a core revenue driver or structural moat. If AI is a peripheral feature, marketing language, or has no measurable revenue impact, say so clearly and note that AI narrative may not apply. Do not force an AI thesis onto names that do not warrant it — an "AI-washing" short or PASS is a perfectly valid output.

---

## Data Setup

Always re-fetch fresh Yahoo Finance data before reading any JSON files:

1. Run the following to force-refresh all data for the ticker:
   ```python
   from yahoo_finance_data import fetch_all
   fetch_all(["TICKER"])
   ```
   Execute this via `.venv/Scripts/python -c "from yahoo_finance_data import fetch_all; fetch_all(['TICKER'])"` before reading any JSON.

2. After fetching, read the following files from `Outputs/{TICKER}/`:
   - `{ticker_lower}_quick_metrics.json` — key ratios and price data
   - `{ticker_lower}_income_statement_ttm.json` — TTM income statement
   - `{ticker_lower}_income_statement_annual.json` — annual income statements
   - `{ticker_lower}_balance_sheet_quarterly.json` — balance sheet
   - `{ticker_lower}_cash_flow_statement_ttm.json` — TTM cash flows
   - `{ticker_lower}_price_history.json` — price history for technical context

3. Use `WebSearch` only to supplement what is not available in the JSON — e.g., segment-level AI revenue breakdowns, RPO, NRR, backlog, insider transactions, and recent news.

---

## Step 1: Classify the Company

First, identify which layer of the AI stack the company occupies — this shapes every subsequent lens. If the company does not clearly fit any layer, say so and note it may not be an AI investment.

| Type | Examples | Key Focus |
|---|---|---|
| **Pure-play AI software** | Palantir, C3.ai, Scale AI | Revenue quality, ACV growth, path to profitability |
| **AI infrastructure / cloud** | AWS, Azure, GCP, CoreWeave | CapEx trajectory, AI workload share, margin impact |
| **Semiconductors** | NVIDIA, AMD, Broadcom, Marvell | Chip cycle, data center revenue mix, next-gen roadmap |
| **AI-enabled enterprise SaaS** | Salesforce, ServiceNow, Workday | AI attach rate, pricing power, NRR, churn risk |
| **Picks-and-shovels** | TSMC, ASML, Vertiv, Eaton | Capacity expansion, customer concentration, lead times |
| **Consumer AI** | Google, Meta, Apple | Monetization of AI features, regulatory risk, moat depth |
| **AI agents / autonomy** | Emerging players | ACV, enterprise adoption pace, model dependency risk |

A company can span multiple layers — note where the **majority of revenue and growth** comes from. If AI revenue is not separately disclosed or is below ~10% of total revenue with no credible near-term ramp, flag that the AI thesis may be speculative or premature.

---

## Step 2: AI Ecosystem Position & Chokepoint Analysis

**The most important structural question: does this company hold a key chokepoint in the AI supply chain — something every AI winner must buy from them, and that cannot be easily replicated or substituted?**

If the company does not appear to hold a chokepoint, state that clearly before proceeding. Not every company in the AI space holds a structural moat — many are beneficiaries, not bottlenecks.

### The AI Stack Chokepoint Map

```
[ Data & Compute Layer ]
  → Raw silicon design         — NVIDIA, AMD, custom ASICs (Google TPU, AWS Trainium)
  → Advanced fab & lithography — TSMC, ASML (EUV monopoly), Tokyo Electron
  → Packaging & memory         — SK Hynix, Samsung (HBM), OSAT providers
  → Power & cooling            — Vertiv, Eaton, Schneider Electric
  → Physical space             — Data center REITs, fiber backbone

[ Model & Training Layer ]
  → Foundation model providers — Anthropic, OpenAI, Google DeepMind, Meta
  → Training data & labeling   — Scale AI, proprietary dataset holders
  → Cloud compute brokers      — CoreWeave, Lambda Labs, hyperscalers

[ Orchestration & Tooling Layer ]
  → MLOps / observability      — Weights & Biases, Datadog, Arize
  → Vector databases           — Pinecone, Weaviate, pgvector
  → Developer APIs & SDKs      — Anthropic, OpenAI, LangChain

[ Application Layer ]
  → Vertical AI software       — Harvey (legal), Abridge (health), Glean (enterprise)
  → AI-enabled SaaS            — Salesforce, ServiceNow, Adobe
  → Consumer AI products       — Google, Meta, Apple, Perplexity
```

### Chokepoint Scoring

For each dimension, score **High / Medium / Low** based on evidence — not narrative:

| Dimension | Question to Answer | Score |
|---|---|---|
| **Supply scarcity** | Is this product/service in short supply relative to demand? Can supply be quickly expanded? | |
| **Substitutability** | Can customers switch to an alternative without significant cost, time, or performance loss? | |
| **Capital barrier** | How much capital, time, and expertise would it take for a new entrant to replicate this? | |
| **Customer dependency** | Do customers build critical workflows *on top of* this company's product, creating deep lock-in? | |
| **Pricing power evidence** | Has the company raised prices without meaningful customer loss? Are margins expanding? | |
| **Single-source risk** | Is this company one of only 1-3 suppliers globally for this input? | |

**Chokepoint verdict:**
- **5-6 High** → Structural chokepoint. Durable pricing power across the full AI cycle.
- **3-4 High** → Strong positional moat. Pricing power likely but not immune to disruption.
- **1-2 High** → Competitive position, not a chokepoint. Moat must come from execution or distribution.
- **0 High** → Commodity supplier or AI beneficiary without moat. Flag explicitly.

### The One Chokepoint Question
*"If the AI buildout plays out fully over the next 10 years, what single input does every winner have to buy from this company — and what would happen to the industry if this company disappeared tomorrow?"*

If there is no compelling answer, say so — that is itself an important finding.

### Historical Chokepoint Analogies

| Company | Chokepoint | Why It Held |
|---|---|---|
| **ASML** | Only supplier of EUV lithography machines globally | 20+ years of R&D, physics-limited replication, TSMC/Samsung dependent |
| **TSMC** | Leading-edge fab at 3nm/2nm | Decades of process know-how, geographic concentration, customer co-development |
| **SK Hynix / Samsung** | HBM memory for AI accelerators | Yield expertise, packaging integration, NVIDIA qualification lock-in |
| **Veeva Systems** | Life sciences CRM/data | Regulatory data formats, FDA submission workflows, 15+ year customer relationships |

---

## Step 3: Business Model Analysis

### Revenue Quality
Pull from `{ticker_lower}_income_statement_ttm.json` and `{ticker_lower}_quick_metrics.json` for quantitative figures. Supplement with `WebSearch` for ARR, NRR, ACV, and segment breakdowns not available in JSON.

- What % of revenue is **recurring** (ARR/SaaS) vs. one-time, transactional, or hardware?
- Is pricing **subscription** (predictable) or **consumption-based** (powerful in growth, vulnerable in downturns)?
- Who are the **top customers**? What is customer concentration risk?
- What is **net revenue retention (NRR)**? Above 120% is strong; above 130% is exceptional for AI SaaS.
- Is the AI product **core to the business** or a bolted-on feature? If the latter, flag it as AI-washing risk.

### AI Moat Assessment
- Does the company have **proprietary training data** that compounds defensibility over time?
- Is the AI built **in-house** (more durable) or on top of third-party models like OpenAI or Anthropic (dependency risk)?
- Are there **switching costs** — workflow integration, retraining costs, data gravity — that lock customers in?
- What is the **threat from hyperscalers** (AWS, Azure, Google) building native equivalents at lower cost?
- Is the moat **positional** (first-mover, distribution) or **structural** (data, compute, proprietary architecture)?
- **Does the chokepoint analysis (Step 2) support or undermine the moat claim?**
- If the moat is weak or speculative, say so plainly.

### Go-To-Market
- Is the sales motion **enterprise top-down**, **product-led growth (PLG)**, **channel/partner**, or **API/developer**?
- What is the **average contract value (ACV)** and sales cycle length — and how are they trending?
- How efficient is sales? Reference **magic number** or **CAC payback period** if available.

---

## Step 4: Financial Deep Dive

Use the local JSON files as the primary data source for all financial metrics below. Read `{ticker_lower}_income_statement_annual.json` and `{ticker_lower}_income_statement_ttm.json` for revenue and margin data; `{ticker_lower}_balance_sheet_quarterly.json` for balance sheet items; `{ticker_lower}_cash_flow_statement_ttm.json` for FCF.

### Growth Metrics
- **Revenue growth YoY** — from annual JSON; is it accelerating, stable, or decelerating?
- **Gross profit and gross margin** — compute from revenue and cost of goods sold in the JSON
- For semis/hardware: note any **data center revenue %** from `WebSearch` if not in JSON
- **AI-specific revenue** — search for management disclosures; note if not separately reported

### Profitability & Margins
- **Gross margin** — AI software: 70%+; semis: 50–75%; infrastructure: lower due to CapEx
- **Operating margin** — from income statement JSON
- **Free cash flow (FCF) margin** — operating cash flow minus capex from cash flow JSON
- **Stock-based compensation (SBC)** — from cash flow JSON; strip it out to get "true" FCF
- Is there a clear and credible **path to profitability**, or is burn accelerating?
- **For chokepoints**: are gross margins *expanding* as demand outstrips supply? That is the clearest financial confirmation of pricing power.

### Balance Sheet
- Cash and investments vs. total debt — from balance sheet JSON
- **Runway** — for unprofitable companies, estimate quarters of cash remaining using burn rate from cash flow JSON
- **CapEx intensity** — from cash flow JSON; critical for semiconductor, cloud, and infrastructure plays
- Any convertible notes or dilutive instruments — supplement with `WebSearch`

### Key Ratios
Compute directly from JSON data where possible; use `{ticker_lower}_quick_metrics.json` for market cap and price:

- **EV/Revenue (forward)** — compare to peers at similar growth rates
- **EV/Gross Profit** — normalizes for business model differences
- **Rule of 40** = Revenue Growth % + FCF Margin % (40+ is healthy; 60+ is exceptional)
- **Price/FCF** if profitable
- **PEG ratio** — supplement with consensus EPS growth from `WebSearch`

---

## Step 5: Competitive Landscape

- Who are the **top 2-3 direct competitors**? How does market share break down?
- Is the company **gaining or losing share**, and what evidence supports that?
- What is the **hyperscaler threat** — can AWS/Azure/Google replicate this at zero marginal cost to existing customers?
- Is there an **open-source threat** — e.g., Meta's Llama or Mistral commoditizing what was once a paid product?
- What is the **realistic AI TAM** for this company, and what share is achievable in 5–10 years?
- **Does the chokepoint position insulate the company from competitive pressure, or is it exposed?**

---

## Step 6: Management & Narrative Quality

- Is the **CEO a founder** or hired operator?
- Track record: Has management **consistently hit or beaten guidance**?
- Are executives **buying or selling stock**? Search OpenInsider or SEC Form 4 via `WebSearch`.
- Is the AI narrative **authentic** — is AI core to the product and revenue — or is it **superficial AI-washing**? Be direct.
- Read the last **2-3 earnings call transcripts** — what questions is management deflecting?
- Has the company **changed its key metrics or guidance methodology**? Yellow flag.

---

## Step 7: Valuation & Scenarios

### Chokepoint Premium Logic

Structural scarcity with expanding margins justifies a higher multiple than a commodity supplier growing at the same rate.

**Rough AI sector multiple benchmarks:**

| Revenue Growth | Gross Margin | Chokepoint? | Typical Forward EV/Revenue |
|---|---|---|---|
| 50%+ | 70%+ | Yes | 20–35x |
| 50%+ | 70%+ | No | 15–25x |
| 25–50% | 70%+ | Yes | 12–20x |
| 25–50% | 70%+ | No | 8–15x |
| 25–50% | 50–70% | Either | 5–10x |
| 10–25% | Any | Either | 3–6x |
| Profitable + growing | — | Yes | 35–60x P/FCF |

### Build 3 Scenarios

| Scenario | Assumptions | Implied Target |
|---|---|---|
| **Bull** | AI adoption accelerates, chokepoint holds, pricing power expands | $ |
| **Base** | Consensus estimates met, competitive pressure manageable | $ |
| **Bear** | Chokepoint erodes (new entrant, substitute, hyperscaler), deceleration, multiple compression | $ |

### Key Valuation Questions
- What is the **current price implying** about future growth? (reverse DCF logic)
- What is the **margin of safety** at the current price?
- What **catalyst** is needed for the stock to rerate higher?
- How did the stock behave in the **2022 rate-hike selloff** and the **2025 DeepSeek shock**? Stress tests reveal true beta. Use `{ticker_lower}_price_history.json` for historical price context.

---

## Step 8: Risk Factors

Always explicitly identify and weigh:

- **Chokepoint erosion risk** — can a new entrant, open-source alternative, or hyperscaler invest their way around this moat?
- **Valuation risk** — already pricing in a perfect AI buildout?
- **Hyperscaler commoditization** — can AWS/Azure/Google replicate this with existing customer relationships?
- **Open-source disruption** — are open-weight models eroding the pricing power of the core product?
- **Model dependency risk** — if built on OpenAI/Anthropic APIs, what happens when those providers go direct?
- **Customer concentration** — what if the top 1-3 customers reduce AI spend or build in-house?
- **AI capex cycle risk** — exposed to a potential pause or digestion phase in hyperscaler spending?
- **Regulatory risk** — data privacy, EU AI Act, export controls (especially for semis), antitrust scrutiny
- **Execution risk** — does management have a track record of shipping product and hitting numbers?
- **Dilution risk** — high SBC from AI talent retention, future equity raises, convertible notes
- **No AI moat risk** — if the AI narrative is not supported by revenue data, state this as a primary risk

---

## Step 9: Synthesis, Verdict & Investment Thesis

### Verdict

**Conviction X / 10 · LONG / SHORT / PASS**

| | |
|---|---|
| Bias | **LONG / SHORT / PASS** |
| Conviction | **X / 10** |
| Current Price | $X.XX |
| Price Target (12-mo, base case) | **$X.XX (+/- X%)** |
| Stop / Invalidation | $X.XX (−X%) — name the thesis-breaking level or event |
| Risk/Reward (Bull vs. Bear from Step 7) | X.X : 1 |
| Sizing | Core (chokepoint confirmed) / Starter (beneficiary with optionality) / Tactical / Avoid |

*Conviction scale: 9–10 = highest-conviction book position · 7–8 = high · 5–6 = moderate/starter · 3–4 = low/watchlist · 1–2 = avoid or short candidate*

### Variant View — Consensus vs. Our Read

The core value-add. State precisely where we diverge from consensus, backed by a specific number. If the data aligns with consensus, say so — market alignment is not a failure, and a forced differentiated view is a bias, not an edge.

| Debate | Consensus / Sell-Side | Our View |
|--------|-----------------------|----------|
| [The chokepoint / moat debate that decides the stock] | [what consensus assumes — cite multiple or estimate] | [our differentiated read + the number] |
| [Second debate — e.g., AI revenue durability, hyperscaler threat] | [consensus] | [our view] |

- **The edge:** [1 sentence — what the market is mispricing, why we're right, and the catalyst that closes the gap]

### Investment Thesis

Write a 3–5 sentence thesis that answers:

1. **What does this company do, and does AI genuinely make it more valuable over time — or is that narrative overstated?**
2. **Does it hold a chokepoint in the AI stack?** If yes, how durable is it and what would break it? If no, say so.
3. **What is the expected return and over what time horizon**, and how does it map to the conviction score above?
4. **What would make you wrong, and what is the exit trigger** (tie to the stop / invalidation level)?

---

## Useful Data Sources

- Local JSON in `Outputs/{TICKER}/` — primary source for all quantitative metrics
- Latest **10-K / 10-Q** (SEC EDGAR) via `WebSearch`
- Most recent **earnings call transcript** (Seeking Alpha, Motley Fool, or company IR site)
- **Investor Day presentation** if one exists
- **Sell-side consensus estimates** (Yahoo Finance, Macrotrends)
- **Insider transactions** (OpenInsider, SEC Form 4)
- Recent news: partnerships, model releases, customer wins, hyperscaler commentary
- **Short interest data** — elevated short interest can signal risk or a squeeze setup
- **Competitor earnings calls** — hyperscalers' CapEx guidance moves the whole sector

---

## Save to Word Document

After completing all 9 steps above, write and execute a Python script using `python-docx` (`.venv/Scripts/python`) that saves the full analysis to `Outputs/{TICKER}/{ticker_lowercase}_company_deep_dive_{YYYYMMDD}.docx`.

Save the script to `Outputs/{TICKER}/generate_{ticker_lowercase}_company_deep_dive.py` and run it from the project root.

**Document structure:**
- Portrait orientation, narrow margins (top/bottom 0.5", left/right 0.75") — see CLAUDE.md
- Title: use `doc.add_heading('{TICKER} — Company Deep Dive', 0)` (Heading 0 style, NOT a custom-sized run) + `doc.add_paragraph(date_label)` as plain subtitle
- Each Step becomes a `doc.add_heading('Step N: ...', 1)` section; sub-headings use level 2
- All body narrative text: `doc.add_paragraph()` with an explicit 12pt run — do NOT leave font size unset; always call `run.font.size = Pt(12)` on every body paragraph run
- **Use bullet points liberally.** Any time content is a list — advantages, observations, risks, factors, named items — use `bullet()` instead of embedding it as "(1)...(2)...(3)..." inside a prose paragraph. Never inline numbered items like "(1) ... (2) ... (3) ..." inside a single `body()` call; always split each into its own `bullet()` call. Lead with a short `body()` intro line (e.g. `body(doc, 'Key observations:')`) then follow with individual `bullet()` calls.
- Bullet points: use `doc.add_paragraph(style='List Bullet')` + `p.add_run(text)` with `run.font.size = Pt(12)`
- All tables use dark blue header rows (fill `1F3864`, white bold text), 12pt data rows
- Chokepoint scoring table: color the Score column cell green (`007000`) for High, orange (`FF8C00`) for Medium, red (`C00000`) for Low
- Valuation scenario table: color Bull row green, Base row neutral, Bear row red
- **Verdict block (Step 9):** render the Bias line as a colored Heading-1-style line — green `007000` for LONG, red `C00000` for SHORT, neutral for PASS — followed by the Verdict table
- **Variant View table (Step 9):** render with the dark-blue header row (fill `1F3864`, white bold text); this section is mandatory
- Source citations: `doc.add_paragraph()` with `run.italic = True; run.font.size = Pt(10)`

**Required table rules (from CLAUDE.md):**
- Initialize every table with `rows=1` (header only), then call `table.add_row()` for each data row — never use `rows=1+len(data)` upfront
- Call `set_row_font_size(row)` on every data row immediately after `table.add_row()`
- Call `autofit_table(table)` then `add_table_borders(table)` **after all rows are added**
- Never use fixed column widths

**Import shared helpers from `doc_utils.py`:**
```python
import sys; sys.path.insert(0, '.')
from doc_utils import autofit_table, add_table_borders, set_row_font_size, add_footnote, fmt_value
```
Use `fmt_value(v)` for all dollar amounts in table cells (auto-scales: ≥$1B → `$X.XXB`, ≥$1M → `$X.XM`, ≥$1K → `$X.XK`). Never hardcode `/ 1e9` or manually append `"B"`.

**Set portrait orientation and narrow margins immediately after `doc = Document()`:**
```python
from docx.shared import Inches
for section in doc.sections:
    section.orientation = 0
    section.page_width = Inches(8.5)
    section.page_height = Inches(11)
    section.top_margin = Inches(0.5)
    section.bottom_margin = Inches(0.5)
    section.left_margin = Inches(0.75)
    section.right_margin = Inches(0.75)
```

Call `add_footnote(doc)` immediately before `doc.save(...)` to append the standard AI disclaimer.

Confirm the output file path when done.
