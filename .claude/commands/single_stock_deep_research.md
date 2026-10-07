# Single Name Stock Analysis

You are a senior **buy-side analyst at a hedge fund** producing a complete research note for the portfolio manager (PM) and investment committee on a single stock. The note is a directional **LONG / SHORT / PASS** recommendation with a conviction score, price target, stop, and risk/reward — written to be actioned, not just read.

**ARGUMENTS:** TICKER (e.g., `NVDA`, `AAPL`)

---

## REIT Handling (apply only when the company is a REIT)

Definitions, metric substitutions and data sources are in `references/reit-framework.md`. Detect: `_quick_metrics.json` `industry` starts with `REIT` (or `sector` is `Real Estate`). Equity REITs follow this block; mortgage REITs (`REIT - Mortgage`) are financials, so flag it and use book value, price/book and net interest spread instead. Not a REIT: ignore this block.

- **Pass REIT context to every subagent in Step 1:** append to each subagent prompt "This company is a REIT: follow the REIT HANDLING block in the skill file and `references/reit-framework.md`, use AFFO (non-GAAP) not GAAP EPS, and mark metrics that are not meaningful for a REIT." Also pass any established, sourced facts from earlier subagents (for example FFO/AFFO, guidance, leverage) and tell later subagents to reconcile, not restate, discrepancies.
- In Step 2, keep the 19-row Financial Snapshot but write **"not meaningful for a REIT"** in the value or comment for GAAP-based rows (trailing/forward P/E, PEG, payout ratio, ROE, GAAP interest coverage, current ratio, FCF margin, Rule of 40), and add the REIT read in the Comments column: P/AFFO, AFFO payout, net debt/EBITDAre, dividend yield spread to the 10-year, occupancy/WALT. In Step 3 color-code only metrics that are meaningful for a REIT.
- The Growth Outlook section uses AFFO-per-share CAGR and guidance (non-GAAP, labeled) instead of EPS CAGR; the Valuation section uses P/AFFO, yield spread, implied cap rate/NAV and a dividend discount model instead of EV/EBITDA and P/S; the Technical section must use unadjusted (price-only) closes (see the technical skill); the NBT section follows the REIT rules in the business potential skill.
- The Verdict still uses the standard LONG/PASS/SHORT rules; state total return both on price and including dividends, and show risk/reward consistently across the note. Where subagent documents disagree with each other, resolve the disagreement before writing the summary.

---

## Step 0 — Download All Data Once, Up Front

Before spawning any subagent, run once: `.venv/Scripts/python -c "from get_financial_data import fetch_all; fetch_all(['{TICKER}'])"`. This is the **only** download for the whole run — SEC EDGAR statements, Yahoo quote data and the **5-year** Yahoo price history (`_price_history.json`). Check the printed price-history line (`first date -> last date`): it should start about five years before today (a shorter span is fine only for a recently listed company). Subagents and the chart/Word scripts then read the JSON; none of them re-downloads anything, price history included. (The one exception is the REIT technical recompute on unadjusted closes, which writes a scratch file and must also request 5 years.)

## Step 1 — Run All 8 Individual Analyses via Subagents

Spawn each analysis as a **separate subagent** using the Agent tool, one at a time (wait for each to complete before spawning the next). Each subagent receives a self-contained prompt instructing it to read and execute the relevant skill file for {TICKER}.

For each skill, use this prompt template:

> Read the file `.claude/commands/{skill_filename}` and execute all instructions in it for ticker {TICKER}. The working directory is the investment-analysis project root. Use `.venv/Scripts/python` to run any Python scripts. All data (including the 5-year price history) was already downloaded by the parent in Step 0, so skip the skill's own "re-download first" / `fetch_all` step and read the existing JSON in `Outputs/{TICKER}/`. **Your final reply goes to the orchestrator, not the user — keep it under 200 words and in exactly this shape:** `.docx` path · `Signal: BULLISH/NEUTRAL/BEARISH · Conviction X/10` · one-line so-what · one-line what-flips-it · up to 6 key figures as `label: value [source]` · the Variant View edge in one line. Do not restate the document.

Execute in this exact order:

1. Subagent → `.claude/commands/business_overview_analysis.md` for {TICKER}
2. Subagent → `.claude/commands/leadership_analysis.md` for {TICKER}
3. Subagent → `.claude/commands/income_statement_analysis.md` for {TICKER}
4. Subagent → `.claude/commands/balance_sheet_analysis.md` for {TICKER}
5. Subagent → `.claude/commands/cash_flow_analysis.md` for {TICKER}
6. Subagent → `.claude/commands/business_potential_analysis.md` for {TICKER}
7. Subagent → `.claude/commands/valuation_analysis.md` for {TICKER}
8. Subagent → `.claude/commands/technical_analysis.md` for {TICKER}

Growth and profitability (multi-year trend, CAGRs, Rule of 40, and 2–3 years of consensus estimates) is covered inside the income statement analysis — there is no separate growth subagent. Output filenames are numbered 1–8 consecutively.

Each subagent runs in a fresh context and exits after saving its `.docx` to `Outputs/{TICKER}/`, returning only the short reply above. Every component skill renders through `report_renderer.py`, so each also writes `Outputs/{TICKER}/{n}_{ticker_lowercase}_{skill}_summary.json` — the same contract in machine-readable form. Proceed to Step 2 once all 8 subagents have completed.

---

## Step 2 — Write the Executive Summary

**Inputs:** synthesize from the 8 subagent replies plus any `Outputs/{TICKER}/*_summary.json` files (prefer the JSON where both exist) — **do not open the 8 appendix `.docx` files**. If a figure the note needs is missing from them, run `digest.py` or a targeted read of that one figure, not a full document read.

Synthesize the findings from all 8 analyses into a **2–3 page hedge-fund research note**. Each of the 8 appendices now carries its own directional **Read-Through** (BULLISH / NEUTRAL / BEARISH) and a dimension conviction score — roll these up into a single house view, weighting the dimensions that actually drive this name. Write it as a seasoned buy-side analyst pitching the PM — direct, opinionated, anchored to specific data points, and explicit about the variant view and the risk/reward asymmetry.

**Writing standards (non-negotiable):**
- Every section must carry a distinct analytical point of view. Avoid generic filler ("the company has a strong balance sheet") — say *why* it matters and *how* it compares to peers or history.
- Lead each section with the single most important insight, not a description of what the section covers.
- Every claim requires a specific number (revenue, margin %, growth rate, multiple, ratio). Vague language like "solid growth" or "attractive valuation" without a number is not acceptable.
- Use buy-side vernacular where appropriate: "variant view," "risk/reward asymmetry," "multiple compression risk," "FCF yield," "de-rating," "beat-and-raise cadence," "margin inflection," "consensus estimate," "what's priced in," "position sizing," "at current levels."
- Paragraphs should read as tight, confident prose — not bullet dumps. Reserve bullets for comparisons and ranked lists only.
- The tone is professional but not sterile. A sharp institutional note has a point of view; write one.
- Spell out every abbreviation on first use, then use the short form after (e.g., "Free Cash Flow (FCF)" first, then "FCF"; "Year-over-Year (YoY)" first, then "YoY"; "Earnings Per Share (EPS)" first, then "EPS"; "Electronic Manufacturing Services (EMS)" first, then "EMS").

**FORMAT YOUR SUMMARY EXACTLY AS FOLLOWS:**

---

### {TICKER} — Comprehensive Investment Research Package
**[Company Full Name] | [Sector] | [Exchange]: {TICKER}**
*[Coverage label] — [Date]*

Before writing the coverage label, check whether any prior research notes or research package files exist for this ticker in `Outputs/{TICKER}/` (e.g., `*_research_notes_*.docx` or `*_research_package_*.docx`). If prior files exist, use **"Coverage Date: [Date]"**. If this is the first time coverage is being produced, use **"Initiating Coverage — [Date]"**.

Also fetch the current broad market condition at the time of this run. Use `WebSearch` to look up today's S&P 500 level, direction (up/down % on the day), VIX, and one-sentence market context (e.g., risk-on/risk-off, catalyst). Include this as a single italic line immediately below the coverage date line:
*Market on [Date]: S&P 500 [level] ([+/−X.X%]), VIX [X.X] — [one-sentence context]*

---

**VERDICT: LONG / SHORT / PASS · Conviction X / 10**
**Price Target (12-mo): $X.XX (+X%)**  |  **Current Price: $X.XX**  |  **Stop / Invalidation: $X.XX (−X%)**
**Risk/Reward: X.X : 1**  |  **Sizing: Core / Starter / Tactical / Avoid**

*Conviction scale: 9–10 = highest-conviction book position · 7–8 = high · 5–6 = moderate/starter · 3–4 = low/watchlist · 1–2 = avoid or short candidate*

---

#### Investment Thesis *(3–5 sentences)*
State the single most important reason to be long or short this stock. Lead with the dominant theme (e.g., AI infrastructure monopoly, financial fortress, deteriorating moat). Name the key metric that anchors the thesis.

---

#### Variant View — What the Market Is Getting Wrong *(2–4 sentences + table)*
The single most important section: state where our view diverges from consensus and the differentiated insight that justifies the position. Vague agreement with the Street is not a trade.

| Debate | Consensus / Sell-Side | Our View |
|--------|-----------------------|----------|
| [The core debate that decides the stock] | [what consensus assumes — cite the estimate/multiple] | [our differentiated read + the number behind it] |
| [Second debate] | [consensus] | [our view] |

- **The edge:** [1 sentence — what the market is mispricing, why we think we're right, and what catalyst closes the gap]

---

#### Business & Competitive Position
- **What the company does** in one sentence.
- **Moat:** What makes it hard to compete with? (network effects, switching costs, IP, scale)
- **Key risk to the moat:** Name the single biggest structural threat.

#### Financial Snapshot

Rendered by a `metrics_snapshot` block (Step 3): it pulls every value from `compute_metrics("{TICKER}", with_sources=True)`, writes the formula + benchmark + per-metric source into the Description column, and colors the Value cell from `_short_comment()` (and `color_current_price()` for row 1). **You supply only the Comments column**, keyed by the snake_case metric key.

Run `PYTHONIOENCODING=utf-8 .venv/Scripts/python digest.py {TICKER} metrics` to see each key's value, source and benchmark label, then write one comment per key: a one-sentence analyst take that names the value, compares it to the sector/peer benchmark and draws a conclusion (e.g. "At 42% gross margin, well above the ~25% hardware-sector median, the company shows pricing power and a software-like mix."). For the informational rows (`week52_low`, `week52_high`, `market_cap`, `revenue`) write a brief context note rather than leaving them blank. Check the balance sheet's sign before repeating a label — negative equity makes `de` and `roe` arithmetic, not meaningful (see CLAUDE.md).

Keys: `current_price, week52_low, week52_high, rsi, market_cap, revenue, rev_growth, gross_margin, op_margin, ni_margin, roe, de, interest_cov, cur_ratio, fcf_margin, r40, trailing_pe, forward_pe, peg, price_to_sales, dividend_yield, payout_ratio`.

#### Growth Outlook
- **Revenue 3-Year CAGR:** X% (from income statement analysis)
- **EPS 3-Year CAGR:** X% (compute from `_income_statement_annual.json` Diluted EPS; cite SEC EDGAR)
- **Consensus revenue / EPS CAGR (next 2–3 FYs):** X% / X% (from income statement analysis)
- **Forward EPS estimate (next FY):** $X.XX (+X% vs trailing)
- One sentence: is growth accelerating, decelerating, or stable?

#### Valuation
- **Trailing P/E:** Xx | **Forward P/E:** Xx | **PEG:** X.Xx
- **EV/EBITDA:** Xx | **P/S:** Xx
- **Analyst consensus target:** $X.XX (X analysts, X% upside)
- One sentence: is the stock cheap, fairly valued, or expensive relative to growth and peers?

#### Technical Setup & Entry
- **Trend:** Up / Neutral / Down | **Price vs 200-DMA:** +X% / −X%
- **RSI (14-day):** X.X | **Setup score:** X/5 | **Timing bias:** LONG / SHORT / WAIT
- **Entry / add zone:** $X.XX–$X.XX | **Stop / invalidation:** $X.XX
- One sentence: do we initiate at current levels, scale in, or wait — and what level invalidates the entry?

#### Balance Sheet & Cash Flow Health
- **Financial health:** Net cash / net debt position and current ratio in one sentence.
- **FCF quality:** Is FCF above or below net income (FCF conversion ratio)?
- **Capital allocation:** Buybacks, dividends, or reinvestment — where is management deploying cash?

#### Business Potential — Next Big Thing (NBT) Readiness

*This section evaluates the company's structural capacity to capitalize on its primary emerging opportunity — its "Next Big Thing" (NBT) — before it becomes the industry standard.*

**Overall NBT Readiness: X/20** — [Readiness label: Dominant (17–20) / Strong (13–16) / Capable (9–12) / At Risk (5–8) / Ill-Positioned (≤4)] · **Read-through to the call: BULLISH / NEUTRAL / BEARISH**

| Dimension | Score | Key Evidence (must cite source) |
|-----------|-------|----------------------------------|
| Value Alignment | X/5 | [One-phrase summary + source] |
| Operational Agility | X/5 | [One-phrase summary + source] |
| Financial Runway | X/5 | [One-phrase summary + source] |
| Ecosystem Control | X/5 | [One-phrase summary + source] |

- **Primary emerging opportunity:** [Name the specific trend — e.g., AI inference at the edge, robotic surgery expansion, autonomous vehicles]
- **Biggest structural advantage:** [One sentence on the single dimension where the company leads and why it is defensible]
- **NBT Spend Ratio:** X.Xx (Trend Capex / Annual FCF) — [self-funding / manageable / reliant on external capital]
- **Biggest execution risk:** [One sentence on the structural or operational gap most likely to prevent full capture of the opportunity]

#### Key Risks *(3 bullets, specific numbers required)*
- [Risk 1]
- [Risk 2]
- [Risk 3]

#### Verdict & Conviction Rationale
**[LONG / SHORT / PASS], Conviction X/10, with $X.XX price target** — 2–3 sentences. Cite the primary valuation method (DCF bull case / peer multiple / forward P/E) used to set the target, state the risk/reward (e.g., "X.X:1 skew to upside"), name the single most important catalyst that closes the gap to target, and name the single most important risk that hits the stop. Close with the position-sizing logic (high-conviction core vs. starter vs. tactical).

**Conviction & bias scale used:**
- **LONG:** >15% upside to price target with favorable risk/reward (≥1.5:1); fundamentals improving or undervalued; variant view supported by data. Conviction 7–10 = core; 5–6 = starter.
- **PASS:** Within ±15% of fair value, or balanced/unclear risk/reward, or no variant edge vs. consensus; no near-term catalyst. Conviction 3–6.
- **SHORT:** >15% downside to fair value; deteriorating fundamentals or overvalued with no margin of safety; identifiable catalyst to re-rate lower. Conviction 7–10 = core short; 5–6 = tactical.

---

## Step 3 — Render the Research Note (Word + interactive HTML)

Do not write a python-docx script. Write the note from Step 2 as a JSON spec and render it, following `references/report-spec.md` (block types, rules):

- Spec: `Outputs/{TICKER}/{ticker_lowercase}_stock_deep_research_notes_{YYYYMMDD}_spec.json` with `"skill": "deep_research"`, `"title": "{TICKER} — Comprehensive Investment Research Package"`, `"output": "Outputs/{TICKER}/{ticker_lowercase}_stock_deep_research_notes_{YYYYMMDD}.docx"`, and `"subtitle"` = the company line, coverage label and the italic market line from Step 2 (separate them with ` · `, or `\n` for a line break).
- Blocks, in order:
  1. `verdict` — `bias`, `conviction`, `rows` = Current Price, Price Target (12-mo) (+%), Stop / Invalidation (−%), Risk/Reward, Sizing; `bullets` = the conviction-scale note is added automatically, so leave it out.
  2. `heading` "Investment Thesis" + `bullets` (or one `paragraph`).
  3. `variant_view` — the Variant View table rows, `edge`.
  4. `heading` + `bullets` for Business & Competitive Position.
  5. `heading` "Financial Snapshot" + `{"type": "metrics_snapshot", "comments": {"current_price": "...", ...}}`.
  6. `heading` + `bullets` for Growth Outlook, Valuation, Technical Setup & Entry, Balance Sheet & Cash Flow Health.
  7. `heading` "Business Potential — NBT Readiness" + `bullets` (overall line) + `table` (Dimension | Score | Key Evidence) with a `fills` entry on each score cell — `C6EFCE` for 4–5, `FFEB9C` for 3, `FFC7CE` for 1–2 — + `bullets`.
  8. `heading` "Key Risks" + `bullets`; `heading` "Verdict & Conviction Rationale" + `paragraph`.
  9. `heading` "Appendices" + `{"type": "appendix_index"}` — in the HTML note it is a hub table linking the 8 component pages with their signal and conviction; the Word package gets its linked appendix list from Step 4 instead.
- `summary`: `as_of`, `thesis_bias`, and `key_figures` (price target, upside, stop, risk/reward, plus the 3–4 numbers that anchor the thesis) — signal and conviction come from the `verdict` block.
- Render: `PYTHONIOENCODING=utf-8 .venv/Scripts/python report_renderer.py Outputs/{TICKER}/{ticker_lowercase}_stock_deep_research_notes_{YYYYMMDD}_spec.json`

## Step 4 — Assemble the Word Package

```
PYTHONIOENCODING=utf-8 .venv/Scripts/python assemble_package.py {TICKER} {YYYYMMDD}
```

It merges the research note with the 8 component documents as Appendices A–H (each on a new page with a bookmarked heading), adds the linked appendix index at the end of the note and "Page X of Y" footers, and saves `Outputs/{TICKER}/{ticker_lowercase}_stock_deep_research_{YYYYMMDD}.docx`. Edit `assemble_package.py` — not this skill — if the merge needs to change. The HTML needs no merge: the research note page is the hub.

## Final Reply

Reply with: the research note `.html` (the hub — open it in a browser) and the package `.docx` paths, the verdict line (bias · conviction · price target · stop · risk/reward), the edge in one line, and the one row of each appendix's signal/conviction that disagrees most with the house view.
