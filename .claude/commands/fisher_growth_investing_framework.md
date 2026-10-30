---
name: fisher_growth_investing_framework
description: Analyze any publicly traded stock through Philip Fisher's growth investing lens (Common Stocks and Uncommon Profits). Given a ticker, runs scuttlebutt-style research, scores the company on Fisher's 15 Points, applies a management-integrity knockout gate, adds modern overlays (ROIC, FCF per share, dilution, durability of advantage), stress-tests valuation with an EPS-growth vs multiple-compression return model, defines sell and thesis-break rules, and produces a scored interactive HTML report (Word on request) with a verdict, saved under Outputs/{TICKER}/. Use whenever the user gives a ticker and asks for a Fisher analysis, growth stock analysis, scuttlebutt research, "is this a great growth company", the 15 points, or whether a growth stock is worth holding long term, even if they never mention Fisher by name.
---

# Fisher Growth Investing Framework

You are a **buy-side analyst at a hedge fund** writing for the portfolio manager (PM): thesis-first, directional, opinionated, every number sourced. Lead with tables.

**ARGUMENTS:** TICKER (e.g., `NVDA`, `AAPL`), or none. Add `--docx` / `--both` for a Word file as well (see `references/report-spec.md`).

Turn a ticker into a Fisher-style long-term growth analysis: first decide whether the business is truly outstanding, then how long it can keep compounding, and only then whether the current price is worth paying. A great company is not automatically a great stock.

## Core philosophy (keep in mind throughout)

- Fisher looked for outstanding businesses that can compound earnings for decades, not statistical bargains (that is Graham).
- Most of the money is made by a few exceptional companies held a very long time. Concentration in things you understand deeply beats diversification into things you barely know.
- Qualitative evidence from people around the company (scuttlebutt) matters as much as the financial statements.
- Management integrity is non-negotiable. A company can fail a few points and still qualify; it cannot fail on integrity.
- The opportunity is the gap between how good the company really is and how good the market believes it is.
- Sell only for three reasons: the original analysis was wrong, the business has deteriorated, or a clearly better opportunity exists. Never sell just because the price rose.

## Inputs

- **Ticker:** confirm the exchange and company name if the ticker is ambiguous or foreign-listed.
  - **No ticker given:** read the list with `.venv/Scripts/python -c "from get_financial_data import load_tickers; print(load_tickers())"` (`tickers.txt`, skipping `#` comments and blank lines), show it to the user, and **ask before running** — run all of them, a subset they name, or a different ticker. Do not start any analysis until they answer. Each confirmed ticker gets the full workflow (see "several tickers" under Output).
- **Optional:** the user's intended holding period, current position/cost basis, a price they are considering, or a specific concern. If absent, assume a 5 to 10 year horizon and do not ask; state the assumption in the report.

## Data rules

1. **Always re-download first:** `.venv/Scripts/python -c "from get_financial_data import fetch_all; fetch_all(['{TICKER}'], price_history=False)"` — refreshes the SEC EDGAR statements and the Yahoo quote in `Outputs/{TICKER}/` before anything is read. **If invoked by `/single_stock_deep_research`, skip this download — the parent already did it.** A recent IPO (fewer than 4 quarters) comes back with `{"error": ...}`: source the statements by hand from the S-1 / 10-Qs and cite them.
2. Read the statements through the digests rather than raw JSON or hand arithmetic: `PYTHONIOENCODING=utf-8 .venv/Scripts/python digest.py {TICKER} income_statement` (also `cash_flow`, `balance_sheet`, `metrics`). These are SEC EDGAR figures (fresh after each filing); `metrics` labels each figure's source — read the label, never infer it. Paste figures as the digest prints them.
3. Use primary sources for everything the JSON lacks: latest 10-K/20-F and 10-Qs (segments, customers, risk factors), earnings call transcripts, the proxy statement (DEF 14A) for compensation, ownership and governance, and investor-relations materials, via WebSearch.
4. Yahoo Finance (`_quick_metrics.json`) is used only for the current price, market cap, multiples and analyst targets, labeled "Yahoo Finance", and cross-checked where it matters. Its `forwardEps` (behind forward P/E and PEG) can be off — recompute forward multiples from fiscal-year consensus EPS found by WebSearch before quoting them. A `0` or missing debt line on a company you know carries debt is missing data: fall back to the 10-Q and cite it (`digest.py balance_sheet` flags this in `data_flags`).
5. Date-stamp every figure (period and source). If a number could not be verified, mark it `UNVERIFIED` rather than estimating silently.
6. The valuation uses `_quick_metrics.json` `currentPrice` (Yahoo's live quote); state the price and its as-of date.
7. Keep quotes from sources under 15 words; paraphrase everything else.

**SOURCE CITATIONS:** every quantitative figure cites where it came from — SEC EDGAR, Yahoo Finance, or a WebSearch source (publication and date) — in the table's `source`, a `source` block, or inline as a `[title](url)` link.

## REIT Handling (apply only when the company is a REIT)

Definitions, metric substitutions and data sources are in `references/reit-framework.md`. Detect: `_quick_metrics.json` `industry` starts with `REIT` (or `sector` is `Real Estate`). Equity REITs follow this block; mortgage REITs (`REIT - Mortgage`) are financials, so flag it and use book value, price/book and net interest spread instead. Not a REIT: ignore this block.

- Score the 15 Points and overlays with REIT inputs: margins = same-store NOI margin and AFFO margin; Point 13 (dilution) = equity issuance and AFFO-per-share growth vs total AFFO growth; ROIC overlay = investment spread (acquisition/development yield vs cost of capital); FCF per share overlay = AFFO per share.
- The Step 6 return model uses AFFO per share and P/AFFO in place of EPS and P/E, plus the dividend (material for every REIT); label FFO/AFFO non-GAAP.

## Workflow

### Step 1: Business snapshot
In a short table: what the company sells, to whom, how it makes money, revenue by segment/geography, 5-year revenue and EPS growth, gross/operating/FCF margins, share count trend, net cash/debt, market cap, and the key customers and suppliers. End with one sentence: "This is a business that ___."

### Step 2: Scuttlebutt (digital edition)
Fisher talked to customers, suppliers, competitors, ex-employees, and experts. Approximate this with what is publicly retrievable. Search each channel separately, summarize the pattern across them, and note where sources conflict.

| Channel | What to look for | Example sources |
|---|---|---|
| Customers | Satisfaction, switching costs, repeat purchase, pricing pushback | Review sites (G2, Gartner Peer Insights, Trustpilot), customer earnings calls, forums |
| Suppliers / partners | Importance of the company to them, payment behavior, capacity commitments | Supplier filings and calls, partner announcements |
| Competitors | Share shifts, pricing pressure, who is catching up | Competitor 10-Ks and calls, industry reports |
| Employees | Culture, talent retention, engineering quality, morale | Glassdoor, Blind, LinkedIn headcount and departures, job postings |
| Industry experts | Technical standing, whether the R&D is real | Conference talks, patents, academic citations, trade press, GitHub activity where relevant |
| Management behavior | Candor in good and bad quarters | Earnings call history, guidance accuracy, how misses were handled |

Output a short "Scuttlebutt verdict" (Strong / Mixed / Weak) with 3 to 5 bullets of the most decision-relevant findings. If a channel yields nothing, say so rather than inventing.

### Step 3: Score the 15 Points
Score each point 0, 1, or 2 (0 = fails, 1 = partial or unproven, 2 = clearly passes). Each score needs one line of evidence with source and date. Maximum 30.

| # | Fisher's question | What to check |
|---|---|---|
| 1 | Does it have products or services with enough market potential to grow sales for years? | TAM, penetration, segment growth, runway of 5 to 10 years |
| 2 | Is management determined to keep developing new products once current growth drivers are exploited? | Product roadmap, new-product revenue share, history of launching the next leg |
| 3 | How effective is R&D relative to the company's size? | R&D as % of sales, revenue from products under 3 years old, peer comparison, patents |
| 4 | Does it have an above-average sales organization? | Sales efficiency, net revenue retention, customer acquisition cost, win rates |
| 5 | Is the profit margin worthwhile? | Gross, operating, and FCF margin vs peers and own history |
| 6 | What is it doing to maintain or improve margins? | Scale effects, mix shift, pricing power, cost programs, incremental margins |
| 7 | Is labor and personnel relations outstanding? | Retention, culture signals, strikes, key-talent departures |
| 8 | Are executive relations outstanding? | Stability of the leadership team, internal promotion, signs of infighting |
| 9 | Is there depth to management? | Bench beyond the CEO and founder, succession plan, key-person risk |
| 10 | Are cost analysis and accounting controls good? | Unit economics disclosure, audit quality, restatements, working-capital discipline |
| 11 | Are there industry-specific aspects that reveal competitive standing? | The metric that matters in this industry (e.g. design wins, backlog, NRR, same-store sales, yield, utilization) and how the company ranks |
| 12 | Short-range or long-range outlook on profits? | Willingness to sacrifice near-term earnings for long-term position, capex and R&D through downturns |
| 13 | Will growth require equity financing that dilutes shareholders? | Net share count change, SBC as % of revenue, cash runway, convertible debt, funded by internal cash flow? |
| 14 | Does management talk freely when things go well but clam up when they go badly? | Tone of calls after misses, guidance withdrawals, disclosure changes, Q&A candor |
| 15 | Is management's integrity beyond question? | Related-party transactions, insider selling vs buying, compensation structure, SEC actions, auditor changes, governance, track record of promises vs delivery |

### Step 4: Knockout gate
Regardless of total score, **disqualify or flag red** if any of these hold:
- Points 14 or 15 score 0.
- Credible evidence of accounting manipulation, undisclosed related-party dealings, or repeated broken promises.
- Point 13 scores 0 and the business cannot fund growth without heavy ongoing dilution.
- Points 1 and 2 both score 0 (no growth runway and no plan for one).

State the gate result explicitly: `PASS`, `FLAG`, or `FAIL`. A `FAIL` ends the investment case. Still complete the report so the user sees why.

### Step 5: Modern overlays (beyond Fisher)
These reflect lessons Fisher did not need to emphasize. Score each 0 to 2 (max 10).

| Overlay | Question | Evidence |
|---|---|---|
| ROIC vs cost of capital | Does growth earn returns above its cost, and are incremental returns holding up? | ROIC trend, incremental ROIC, vs estimated WACC |
| FCF per share growth | Does growth reach the shareholder after capex, SBC, and dilution? | 5-year FCF/share CAGR vs revenue CAGR |
| Durability of advantage | What specifically stops competitors from copying it, and is that moat widening or narrowing? | Switching costs, network effects, scale, IP, ecosystem; evidence of share shifts |
| Capital allocation | Are acquisitions, buybacks, and reinvestment creating per-share value? | Acquisition track record, buyback price vs intrinsic value, capex returns |
| Cyclicality and concentration | Could one customer, one product, or one cycle break the thesis? | Top-customer %, cyclic revenue history, geopolitical or regulatory exposure |

### Step 6: Valuation reality check
Fisher paid up for quality but not blindly. Show that the price embeds sensible expectations.

1. **Return model.** Annualized price return over N years (default 5):
   `((EPS_end x PE_end) / (EPS_now x PE_now))^(1/N) - 1`, plus dividends if material.
2. **Three scenarios** in a table: Bear / Base / Bull, each with EPS CAGR, exit P/E, resulting annualized return, and the evidence supporting that scenario's growth rate.
3. **Multiple compression test.** Hold EPS growth at the base case and show how returns change if the exit multiple is 25% and 50% lower than today's. Call out explicitly when great earnings growth still yields poor returns because of the starting multiple.
4. **Reverse check.** What EPS growth for how many years is the current price implying? Is that consistent with the Step 3 evidence?
5. **Peer context.** Compare P/E, EV/sales, and FCF yield against 3 to 5 true peers, adjusting for growth.

Do not give a single-point price target. Give ranges and the assumptions that drive them.

### Step 7: Thesis-break and sell rules
Fisher's three sell triggers, made specific to this company:
1. **Mistake in the analysis:** the 2 to 3 facts that, if false, mean the original thesis was wrong.
2. **Business deterioration:** measurable signals (e.g. margin falling below X for two quarters, share loss in segment Y, key executive departure, integrity red flag).
3. **Clearly better opportunity:** the bar a replacement must clear. Remind the user that rising price or high valuation alone is not a sell signal under Fisher, though extreme valuation should reduce position size or expected returns in the Step 6 model.

Also list what would make the user **buy more** (e.g. a market-driven price drop with no change in fundamentals, which Fisher saw as the real opportunity).

### Step 8: Verdict
Compute:
- Fisher score: Step 3 total out of 30.
- Overlay score: Step 5 total out of 10.
- Combined: out of 40.

| Combined score | Gate | Classification |
|---|---|---|
| 34 to 40 | PASS | **Fisher-grade compounder.** Outstanding business; valuation decides sizing and timing |
| 27 to 33 | PASS | **Strong candidate.** Good business with identifiable weaknesses; monitor the weak points |
| 20 to 26 | PASS or FLAG | **Watchlist.** Interesting but unproven or flawed; needs more evidence |
| Below 20 or gate FAIL | any | **Does not meet Fisher's standard.** Pass |

Then pair business quality with price in a 2-line summary:
- **Business quality:** classification above.
- **Price attractiveness:** Attractive / Fair / Demanding / Unattractive, based on the Step 6 base-case annualized return and multiple-compression sensitivity.

Final one-paragraph conclusion in plain language: what you would need to believe, the biggest risk, and what to monitor next. Offer research conclusions as analysis, not personalized advice.

### Step 9: The call
Translate the Fisher classification and the price rating into the house verdict:

| Classification | Price attractiveness | Bias | Conviction | Sizing |
|---|---|---|---|---|
| Fisher-grade compounder | Attractive / Fair | LONG | 8–10 | Core |
| Strong candidate | Attractive / Fair | LONG | 6–8 | Starter |
| Compounder or Strong candidate | Demanding / Unattractive | PASS (great business, wait for price) | 4–6 | Avoid for now; name the entry price |
| Watchlist | any | PASS | 3–5 | Avoid |
| Does not meet Fisher's standard, or gate FAIL | any | AVOID | 1–2 | Avoid |

Fisher is a long-only framework: never output SHORT. Keep Fisher's rule of no single-point target — the verdict gives the bear–bull price range at the end of the holding period and the base-case annualized return instead.

### Step 10: Variant View — Consensus vs. Our Read
A 3-column table (debate | consensus / sell-side view | our read with the number behind it) on the 2–3 debates the Fisher work most changes: usually runway length (Points 1–2), margin durability (Points 5–6), and what the multiple implies (Step 6 reverse check). End with one line, **"The edge:"** what the market is mispricing and why. If the work confirms consensus, say so — a forced variant view is a bias, not an edge.

## Fisher's "don'ts" to check against the conclusion
Before finalizing, confirm the analysis did not fall into these traps:
- Buying a promotional story or a not-yet-proven company because of a hot industry.
- Buying because the annual report or management presentation looked impressive, without outside corroboration.
- Over-diversifying into companies you cannot explain well.
- Following the crowd into a popular stock without independent evidence.
- Haggling over small price differences on a company that passes every other test (but not ignoring an extreme valuation).
- Assuming a fast-growing industry means every company in it rewards shareholders.

## Output

Do not write a python-docx script. Write the report as a JSON spec and render it, following `references/report-spec.md` (block types, output-format rule, final reply).

1. Spec: `Outputs/{TICKER}/{ticker_lowercase}_fisher_analysis_{YYYYMMDD}_spec.json` with `"output": "Outputs/{TICKER}/{ticker_lowercase}_fisher_analysis_{YYYYMMDD}.docx"` (the `.html` is written next to it; the `.docx` only if Word was requested).
2. `"ticker"`, `"skill": "fisher"`, `"title"`: "{TICKER} — Fisher Growth Analysis", `"subtitle"`: company name, price and as-of date, analysis date, holding-period assumption.
3. Blocks, in this order:
   1. **Verdict** — a `verdict` block: `bias` and `conviction` from Step 9; `rows` = Current Price (as-of date) · Combined Score (X/40: Fisher X/30 + Overlays X/10) · Knockout Gate · Business Quality · Price Attractiveness · Base-Case Annualized Return (N years) · Bear–Bull Price Range at Year N · Sizing; `bullets` = `**Justification:** ...` plus the buy-more price/condition.
   2. **Business Snapshot** — `table`, then the "This is a business that ___." line as a `paragraph`.
   3. **Scuttlebutt Findings** — `table` (Channel · What we found · Signal ✅ ⚠️ 🔴 · Source/date), then the verdict and 3–5 `bullets`.
   4. **How to Read the Scores** — one `bullets` block with parent items and `children`: the 0 / 1 / 2 point scale; the combined-score bands from Step 8; the gate outcomes (PASS / FLAG / FAIL).
   5. **Fisher 15 Points Scorecard** — `table` (# · Question · Score · Evidence · Source/date) with a bold subtotal row (`bold_rows`); `fills` on the Score cell: `C6EFCE` for 2, `FFEB9C` for 1, `FFC7CE` for 0.
   6. **Knockout Gate** — a colored `paragraph` (`007000` PASS · `BF8F00` FLAG · `C00000` FAIL) + reasoning `bullets`.
   7. **Modern Overlays** — `table` (Overlay · Score · Evidence · Source/date), same fills, bold subtotal row.
   8. **Valuation Reality Check** — scenario `table` (Bear / Base / Bull: EPS CAGR · exit P/E · annualized return · evidence), multiple-compression `table`, reverse-check `bullets`, peer `table` with `"sortable": true`.
   9. **Sell Rules and Add-More Triggers** — `bullets`, grouped by Fisher's three triggers, then the buy-more triggers.
   10. **Key Risks and What to Monitor** — two `bullets` blocks (top 3–5 risks; next-quarter monitors as `"numbered": true`).
   11. **Variant View** — a `variant_view` block (Step 10).
   12. **Sources** — `bullets` of `[title](url)` links with dates; list any `UNVERIFIED` figure here.
4. `summary`: `as_of`, `thesis_bias` (= Step 9 bias), and `key_figures` — Combined Score, Gate, Business Quality, Price Attractiveness, Base-Case Annualized Return, ROIC, FCF/share CAGR, each with its source.
5. Render: `PYTHONIOENCODING=utf-8 .venv/Scripts/python report_renderer.py Outputs/{TICKER}/{ticker_lowercase}_fisher_analysis_{YYYYMMDD}_spec.json` (append `--format docx|both` if Word was requested). It writes the `.html`, the `_summary.json`, and refreshes `Outputs/index.html`.

If the user asks about several tickers, run each through the full workflow (one report per ticker) and finish the chat reply with a ranked comparison table.

**Final reply:** per `references/report-spec.md` — the `.html` (and `.docx` if written) path, `Bias · Conviction X/10 · Combined X/40 · Gate`, the justification line, and the 3 most important key figures with sources. Do not repeat the report.

## Changes Since Last Run (when an earlier run exists)

Before writing the spec, run `PYTHONIOENCODING=utf-8 .venv/Scripts/python prior_run.py Outputs/{TICKER}/{ticker_lowercase}_fisher_analysis {YYYYMMDD}` (today's run date). If it returns `{"prior": null}` this is initial coverage and nothing below applies. Otherwise follow `references/changes-since-last-run.md` and add a **"What Changed Since {prior date}"** section straight after the Verdict. Items to compare for this skill: combined score and classification, each of the 15 Points and 5 overlay scores that moved, gate result, scuttlebutt verdict, base-case annualized return and price rating, and any sell rule or thesis-break trigger that has fired.

## Interaction with other skills (if available in the session)
- For a full DCF, price target and technical entry, hand off to `/single_stock_deep_research` (or `/valuation_analysis`).
- For the latest quarter's results, use `/earnings_report_analyzer` to feed Steps 3 and 7.
- For screening many tickers quickly before running this full analysis, use `/multibagger_screener` or `/quick_stock_metrics`.

## Quality checks before delivering
- Every score in Step 3 has evidence with a source and date.
- The knockout gate was evaluated explicitly, not skipped.
- Valuation uses a verified current price and states its date.
- The Verdict, Variant View and every table's `source` are present; the report rendered without a `ValueError`.
- Bear case is genuinely adverse, not a mild variation of the base case.
- No claim relies on training-data memory for numbers that change (prices, share counts, margins, guidance); those were retrieved and date-stamped.
- Report length is proportionate: scorecards and tables carry the content, prose is brief.
