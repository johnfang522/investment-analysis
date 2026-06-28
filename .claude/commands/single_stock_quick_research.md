---
name: single_stock_research
description: >
  A disciplined bottom-up framework for initiating coverage on a single stock — the buy-side "should I own this?" workflow. Use whenever the user asks you to research, analyze, evaluate, or deep-dive a specific company or ticker; build an investment thesis on a named stock; write an initiation-of-coverage note; assess whether a stock is a buy/hold/sell; check if it's cheap or expensive; compare a company to peers; or pressure-test the bull/bear case on a name they own. Trigger on phrases like "what do you think of $TICKER", "is X a good investment", "should I buy Y", "analyze this company", "write a research note on Z", "is this stock overvalued", or "what's the downside here". This is the single-name, fundamentals-first complement to the top-down investor-trend-framework — use THIS skill when the unit of analysis is one company, not a theme. Always use it for single-stock research rather than answering ad hoc, and always pull live data (price, multiples, filings, news) rather than relying on memory.
---

# Single-Stock Research

A buy-side framework for deciding whether to put capital behind one company. The job is not to describe a stock — it is to build a falsifiable thesis, stress-test it against the bear case, and decide whether the price pays you to take the risk.

Operate like a portfolio manager writing an internal initiation note for the investment committee: opinionated, evidence-based, and honest about what you don't know. The output is a recommendation you'd stake capital and reputation on, not a balanced encyclopedia entry.

---

## Data Fetch

**Always re-download Yahoo Finance data before reading any JSON.** Run this first:

`.venv/Scripts/python -c "from yahoo_finance_data import fetch_all; fetch_all(['{TICKER}'])"`

This overwrites any stale cached files. Only then read `Outputs/{TICKER}/{ticker_lowercase}_*.json` for quantitative metrics (financials, price history, balance sheet, cash flows). Use `WebSearch` only for qualitative or forward-looking information (analyst targets, news, insider activity, guidance) — not for numbers available in the JSON.

---

## Operating Principles

Apply these throughout — they separate research from a data dump.

1. **Pull live data; never trust memory for numbers.** After the data fetch above, read all quantitative metrics — revenue, margins, EPS, balance sheet, cash flows, price history — from the Yahoo Finance JSON files in `Outputs/{TICKER}/`. Use `WebSearch` for analyst targets, forward guidance, recent news, and insider activity. Cite the source and as-of date for all web-sourced figures. If a number can't be verified, say so rather than inventing it.
2. **Everything is relative.** A 25× P/E means nothing alone. Anchor every metric to (a) the company's own history and (b) direct peers and the industry. Build comp tables, not lone figures.
3. **Separate fact from judgment.** Clearly distinguish what the filings say from what you infer. Label your variant perception — where and why you differ from consensus — explicitly.
4. **Always state the bear case.** If you can't argue the short side convincingly, you don't understand the stock well enough to be long it.
5. **A great company can be a bad investment.** Quality and price are separate questions. Decide both, then decide whether to act.
6. **End with a decision.** Buy / Hold / Avoid (or Long / Pass / Short), a conviction level, a position-size implication, and the specific evidence that would change your mind.
7. **Not investment advice.** This is research and analysis for the user's own decision-making, not a personalized recommendation. Note this in the output.

---

## The Seven Pillars

Work through all seven in order. Each pillar ends with a verdict, not just facts.

### Pillar 1 — The Business: Know What You Own
The two-sentence test: if you can't explain how the company makes money in two plain sentences, you're not ready to risk capital. Dig until you can.

Establish:
- **What it does and how it earns.** Revenue by segment / geography / customer type from income statement JSON and `WebSearch`. Unit economics — what is one unit of demand, and what does it earn?
- **Position in its value chain.** Leader, disruptor, or niche player? Where does it sit relative to suppliers and customers (pricing power flows from this).
- **Customers and concentration.** Who pays, how sticky are they, and is revenue dangerously concentrated in a few accounts?
- **The moat.** Classify it, don't just assert it. Sources of durable advantage: intangibles (brand/patents), switching costs, network effects, cost advantage / scale, efficient scale, regulatory licenses, and data advantages. Rate moat strength wide / narrow / none and say *why it persists*.
- **Management & capital allocation.** Track record, insider ownership and incentives, and how they spend a dollar of free cash flow (reinvest, acquire, buy back, dividend). Capital allocation is where most long-run value is made or destroyed.

**Verdict:** one-line bull thesis, one-line bear thesis, and a moat rating.

### Pillar 2 — Financial Health: Trust but Verify
Read 3–5 years of history and the latest quarter from the Yahoo Finance JSON files (`{ticker_lowercase}_income_statement_annual.json`, `_quarterly.json`, `_ttm.json`; `_balance_sheet_quarterly.json`; `_cash_flow_statement_*.json`; `_quick_metrics.json`). Look for the *trend and the direction of the second derivative*, not a single snapshot.

- **Growth.** Revenue and earnings CAGR over 3–5 years from annual income statement JSON. Is it accelerating or decelerating? Organic vs. acquired? For software, check the Rule of 40 (growth % + FCF margin % ≥ 40).
- **Margins & operating leverage.** Gross margin (pricing power), operating margin (efficiency / leverage), net margin, and their direction over time from income statement JSON. Watch stock-based compensation as a % of revenue (it's a real cost).
- **Quality of earnings.** Does cash back the profits? Compare FCF (cash flow JSON) to net income (income statement JSON); persistent divergence (rising receivables, inventory builds, aggressive accruals) is a red flag.
- **Balance sheet & survival.** Net debt / EBITDA, interest coverage, current ratio, and the debt maturity wall from balance sheet JSON. The test: can it survive a bad year without diluting holders or breaching covenants?
- **Returns on capital.** ROIC vs. WACC is the truest test of business quality — a company earning below its cost of capital destroys value while it grows. Decompose ROE (DuPont: margin × turnover × leverage) to see whether returns are earned or borrowed.
- **Peer comparison.** Put every metric above into a comp table against 3–5 direct competitors and the industry average. Peer figures come from `WebSearch` — Yahoo Finance JSON covers only the target ticker.

**Verdict:** is this a high-, average-, or low-quality business financially, and is it getting better or worse?

### Pillar 3 — Valuation: Are You Overpaying?
Price is what you pay; value is what you get. Triangulate — never rely on one multiple. Source current price and market cap from `{ticker_lowercase}_quick_metrics.json`; derive EV, EV/EBITDA, P/FCF from income statement and cash flow JSONs.

- **Multiples in context.** P/E, EV/EBITDA, EV/Sales, P/B, P/FCF and FCF yield — each vs. the company's own 5-year range (compute from historical JSON data) AND vs. peers (via `WebSearch`). Premium or discount, and is it justified by growth, margins, or returns?
- **Growth-adjusted.** PEG (P/E ÷ growth rate) to compare across different growth profiles. Use historical revenue/earnings growth from JSON; forward growth estimates from `WebSearch`.
- **What's priced in (reverse DCF).** Back out the growth and margin the current price implies, then ask: is that achievable, conservative, or heroic? "What does the market have to believe?" is the most useful valuation question on the buy side.
- **Scenario-weighted target.** Build bull / base / bear fair-value cases with rough probabilities → a probability-weighted expected value and an implied up/down skew. Asymmetry matters more than the point estimate.
- **Analyst targets** via `WebSearch` as a sanity check on the range — useful for spread and revision direction, never gospel.

**Verdict:** cheap / fair / expensive vs. the quality and growth on offer, with a margin-of-safety read.

### Pillar 4 — News, Sentiment & Catalysts: What's the Market Missing?
This pillar is time-sensitive — it MUST be built from live, recent sources.

- **Recent developments.** Material news, management changes, M&A, litigation, regulatory actions over the last 6–12 months.
- **Catalyst calendar.** Upcoming earnings, product launches, capital-markets days, regulatory decisions, lock-up expiries — anything that re-rates the stock.
- **Sell-side posture.** Rating distribution, target dispersion, and — most useful — the *direction of estimate revisions*. Estimate momentum often leads price.
- **Positioning & sentiment.** Short interest and trend, insider transactions (cluster buying by insiders is a stronger signal than selling), and unusual options activity if available.
- **Variant perception.** State plainly where your view differs from consensus and the specific reason the market may be wrong. No edge = no trade.

**Verdict:** is sentiment a tailwind, a headwind, or the opportunity itself?

### Pillar 5 — Risk & The Pre-Mortem: Don't Skip the Downside
Run a pre-mortem: assume it's two years later and the position is down 50% — write the story of what went wrong *before* you buy.

- **Map the key risks.** Competition / disruption, balance-sheet and refinancing, regulation, secular decline, customer or key-person concentration, cyclicality, governance.
- **Thesis-breakers (kill criteria).** Name the specific, observable data points that would prove the thesis wrong — the metrics you'll watch and the triggers that make you sell. A thesis you can't falsify is a hope, not a thesis.
- **Margin of safety & sizing.** Does the price compensate for the downside? Size the position to conviction and to the bear-case loss, not the bull-case gain.

**Verdict:** the single biggest risk, and whether the price pays you to bear it.

### Pillar 6 — Business Potential: Can It Win the Next Paradigm?
Don't conflate narrative with optionality. The question is not whether the trend is real — it's whether *this company* is structurally wired to capture it. Work through four tests:

- **Value alignment.** Does the trend extend the core business, or require reinventing it? Do existing moats (data, brand, IP, distribution) transfer, or become liabilities? Is legacy revenue sticky enough to fund the pivot?
- **Operational agility.** R&D as a % of revenue and its trajectory vs. revenue growth. Time-to-market evidence. Capacity expansion plans. Name signed contracts, customer wins, or JVs — no growth claims without specific deals.
- **Financial runway.** Annual FCF vs. estimated trend capex/R&D: can it self-fund, or does it need outside capital? Net cash / debt position and interest coverage as the guardrails.
- **Ecosystem control.** Does it own a toll booth — critical infrastructure, a platform standard, key IP? Is it open or closed? Is it shaping the rules, or reacting to them?

Score each dimension 0–5 and sum to an **NBT Readiness Score (X/20)**: Dominant (17–20) · Strong (13–16) · Capable (9–12) · At Risk (5–8) · Ill-Positioned (≤4). Name the single biggest structural advantage and the single biggest execution risk.

**Verdict:** does this readiness add real upside optionality to a long, or expose a vulnerability — and what one proof point (signed deal, capacity commitment, product launch) would change the read?

### Pillar 7 — Synthesis: The Investment Decision
Connect the dots — story, numbers, price, and mood — into one call. If the case isn't clear and data-backed, the answer is "pass." Capital deserves conviction, not hope.

Deliver:
- **Recommendation:** Buy / Hold / Avoid (or Long / Pass / Short).
- **Conviction:** low / medium / high, with the reasoning.
- **Position-size implication** consistent with conviction and downside.
- **Scenario price targets** (bull / base / bear) and implied skew.
- **Exit triggers** — what would make you sell, on either the upside or the thesis breaking.

---

## Scorecard

Summarize the seven pillars in a scannable table before the write-up:

| Pillar | Read | Notes |
|---|---|---|
| Business & moat | Strong / Mixed / Weak | one line |
| Financial health | Strong / Mixed / Weak | one line |
| Valuation | Cheap / Fair / Expensive | one line |
| Sentiment & catalysts | Tailwind / Neutral / Headwind | one line |
| Risk / margin of safety | Adequate / Thin / None | one line |
| Business potential | Dominant / Strong / Capable / At Risk / Ill-Positioned | one line |
| **Overall** | **Buy / Hold / Avoid** | **conviction + one-line thesis** |

And close with the research checklist:

| Step | The question | The discipline |
|---|---|---|
| Business model | Can I explain it in two sentences? | If not, dig deeper |
| Financials | Are growth, margins, and returns solid — vs. peers? | Always compare |
| Valuation | Premium or discount, and is it justified? | Triangulate multiples |
| News & sentiment | What's the hidden risk or catalyst? | Scan live headlines |
| Risk | What's my downside and what breaks the thesis? | Always plan the exit |
| Business potential | Is the company positioned to win the next paradigm? | NBT Readiness Score |

---

## Output Format

Default deliverable: polished **quick research notes as a `.docx`** saved to `Outputs/{TICKER}/{ticker}_stock_quick_research_{YYYYMMDD}.docx`. Follow the Word Document Generation conventions in CLAUDE.md: use `doc_utils.py` helpers, call `add_footnote(doc)` before saving, set portrait orientation and narrow margins.

For a quick "what do you think of $X" with no request for a document, a tight in-chat note is fine — lead with the scorecard and recommendation, then the supporting pillars. Offer the `.docx` as a follow-up.

Structure the note in this order:

1. **Header** — company, ticker, current price & date, market cap, and the one-line recommendation + conviction.
2. **Investment thesis** — 3–5 sentences: what we own, why it wins, and the variant perception.
3. **Scorecard** (the table above).
4. **The seven pillars**, each with its facts and its verdict.
5. **Bull / Base / Bear** scenarios with price targets and probabilities.
6. **Risks & thesis-breakers.**
7. **Recommendation & exit triggers.**
8. **Sources & disclaimer** — cite data sources with as-of dates; note this is research, not personalized investment advice.

Write in a professional, decisive buy-side voice. Use tables for comps, multiples, and scenarios so they're scannable. Bold the recommendation. Never pad — every paragraph should move the decision forward.
