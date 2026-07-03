---
name: multibagger_screener
description: >
  An idea-generation funnel for finding stocks with outsized future return potential (5x, 10x, 100x "multi-baggers") — from hunting ground to scored shortlist. Use this skill whenever the user asks to find, discover, screen for, or generate ideas for high-return stocks; asks "which stocks could 10x", "find me the next NVIDIA/Monster/Amazon", "what small caps
  have big upside", "screen for multi-baggers", "where are outsized returns", or "give me stock ideas in theme X"; or wants a shortlist of candidates rather than analysis of one named stock. This skill takes the user from hunting ground to a scored, ranked shortlist with explicit return math. Always use this skill for idea generation rather than listing stocks ad hoc, and always pull live data (market caps, financials, coverage) rather than relying on memory.
---

# Multibagger Screener

A disciplined funnel for surfacing stocks with genuine outsized-return potential. The premise: multi-baggers are not found by predicting the future better — they are found by fishing where the structural odds are best and filtering hard for a specific, well-documented trait set.

The output is a **scored shortlist of 3–7 names**, each with a one-paragraph hook, ready to hand to the single_stock_quick_research (or single_stock_deep_research) skill for further deep dive. This skill generates and ranks ideas; it does not issue Buy/Hold/Sell calls.

---

## The Base Rates (why the funnel is shaped this way)

Ground every screen in what the historical population of 10x–100x stocks actually looked like at the *start* of their runs:

- **Small:** The median 100-bagger started as a small-cap (most under ~$500M–$1B). Mega-caps almost never 10x — the law of large numbers is the single biggest enemy of outsized returns.
- **Long:** The average 100-bagger took ~20–25 years; even 10-baggers typically need 5–10 years. This is a holding-period game, not a timing game.
- **Painful:** Nearly all suffered at least one 50%+ drawdown mid-run. Volatility is the toll, not the signal.
- **Twin-engined:** The biggest winners compounded earnings growth AND multiple expansion together. Buying growth cheaply matters as much as finding growth.
- **Ignored at first:** Most were under-covered and under-owned by institutions when the run began. Popularity is a late-cycle trait.

**Calibration anchors** (traits at the start of the run, not today):

| Company | At the start | The engine |
|---|---|---|
| Monster Beverage | Micro-cap, no coverage, founder-run | Category creation + national distribution runway |
| NVIDIA (pre-2016) | Mid-cap, seen as "PC gaming chips" | Optionality (CUDA) repriced as a new market emerged |
| Old Dominion | Small trucker in a "bad" industry | Relentless unit-cost advantage + share gains for 20 yrs |
| Heico | Small family-run aerospace parts | Niche dominance + disciplined serial acquisition |
| Constellation Software | Ignored at IPO | High-ROIC capital recycling machine, founder-led |
| Copart | Small-cap "junkyard" | Network effects + land moat nobody modeled |

The lesson: the winners rarely looked glamorous. They looked small, profitable, founder-driven, and structurally advantaged in a market that could grow for decades.

---

## The Funnel

### Stage 1 — Define the Hunting Ground

Pick one (or run several in parallel):

1. **Theme-driven:** Identify a credible secular theme, then map its value chain and fish in the least-crowded, highest-moat layers: raw infrastructure suppliers ("picks & shovels"), adjacent beneficiaries (incumbents with a new tailwind but no theme label — least crowded), and bottleneck/chokepoint assets (single-source inputs everyone must buy — highest structural moat). Avoid end-user application names: they are usually crowded and fully priced by the time a theme is visible.
   (If an investor-trend-framework skill is installed, use it for this step; otherwise apply the heuristic above directly.)
2. **Neglect-driven:** Small-caps with < 5 analysts, recent spin-offs, post-IPO busts trading below IPO price with improving fundamentals, "boring" industries with a consolidator.
3. **Quality-screen-driven:** Universe screen on the quantitative gate below, theme-agnostic.

State explicitly which hunting ground is being used and why.

### Stage 2 — Quantitative Gate (hard filters)

Pull live data. For any candidate ticker, source market cap, growth, margins, ROIC, balance sheet, and share count from Yahoo Finance first — run `fetch_all([tickers])` (from `yahoo_finance_data.py`) and read the resulting `Outputs/{TICKER}/` JSON files (`{ticker_lower}_quick_metrics.json`, income/balance/cash-flow statements). Only fall back to `WebSearch` for fields Yahoo Finance doesn't carry (analyst coverage counts, insider ownership %, spin-off/IPO context) or for names not yet in `tickers.txt`/`Outputs/`.

A candidate must clear most of these to advance:

| Filter | Threshold | Rationale |
|---|---|---|
| Market cap | < $5B, prefer < $1.5B | Room to 10x; survivable size |
| Revenue growth | > 15% (3-yr CAGR or clear acceleration) | The growth engine exists |
| Gross margin | > 40% (or top-quartile for its industry) | Pricing power headroom |
| ROIC | > 15%, or clearly inflecting toward it | Reinvestment creates value |
| Balance sheet | Net cash or net debt/EBITDA < 2x | Survives the inevitable drawdown |
| Dilution | Share count growth < 3%/yr | Growth is self-funded |
| Analyst coverage | < 10 analysts | Rerating engine not yet fired |

Exceptions are allowed with justification (e.g., a chokepoint asset may carry more debt), but every exception must be named as a risk.

### Stage 3 — Multi-Bagger DNA Score

Score survivors on ten traits, 0 (absent) / 1 (partial) / 2 (strong), citing evidence for each:

| # | Trait | What "strong" looks like |
|---|---|---|
| 1 | Small starting size | Market cap under ~$1–3B; big enough to survive, small enough to 10x |
| 2 | High ROIC | ROIC > 15–20%, well above cost of capital |
| 3 | Reinvestment runway | Can redeploy most cash flow at those returns for 10+ yrs (TAM penetration < ~20%) |
| 4 | Twin-engine setup | Entry multiple at or below market/peers, so growth AND rerating can both work |
| 5 | Owner-operator | Founder-led or manager with 5%+ ownership; skin in the game |
| 6 | Under-followed | < 10 analysts; low institutional ownership; no index crowding yet |
| 7 | Gross-margin strength | High and stable/rising gross margin = pricing power headroom |
| 8 | Self-funding | Growth financed internally, not by serial dilution or debt |
| 9 | Moat that scales | Advantage strengthens with size (network effects, data, unit cost) |
| 10 | Long secular tailwind | Rides a decade-plus theme with segment-level revenue proof |

**Interpretation:**

| Score | Read |
|---|---|
| 16–20 | Rare — genuine multi-bagger DNA; top of the shortlist |
| 11–15 | Promising — advances; name which missing traits are fixable vs. structural |
| 6–10 | Ordinary — may be a fine stock, but not an outsized-return candidate |
| 0–5 | Pass for this mandate |

Rank the shortlist by score. Only names scoring **11+** advance.

### Stage 4 — The Twin-Engine Check (per finalist)

For each finalist, show the return decomposition explicitly:

- Entry multiple today vs. history/peers
- Plausible earnings/FCF growth rate for 5–10 years (tie to runway evidence, not hope)
- Plausible exit multiple (what does this business trade at if it works?)
- **Implied multiple-of-money** = growth compounding × multiple change

| Scenario | EPS/FCF CAGR | Exit multiple | 10-yr multiple of money |
|---|---|---|---|
| Engine works, rerates | | | |
| Engine works, no rerate | | | |
| Engine stalls | | | |

If the "no rerate" row still produces a solid return, the setup is resilient. If the thesis *requires* rerating, say so — that is a narrower, riskier bet.

### Stage 5 — Shortlist Output

Deliver the final table:

| Ticker | Company | Mkt cap | Hunting ground | DNA score /20 | One-line hook | Biggest single risk |
|---|---|---|---|---|---|---|

Plus, for each name, a one-paragraph hook: what the market currently believes, what the multi-bagger case requires believing instead, and why that gap might close.

End with the handoff line: recommend a full bottom-up deep dive on the top 1–3 names (business quality, financial health, valuation with scenario targets, risks and thesis-breakers) before any capital is committed — using whatever single-stock research process or skill the user has.

---

## Anti-Patterns (screen these OUT)

- **Story stocks with no gross margin** — narrative without unit economics 
- **Serial diluters** — "growth" funded by your ownership shrinking
- **Binary outcomes** — single-drug biotechs, single-contract defense names (lottery tickets, not compounders — unless explicitly requested)
- **Already-crowded theme darlings** — > 20 analysts, meme status, or valuation already pricing the bull case (the rerating engine is spent)
- **Melting-ice-cube cheapness** — low multiple on declining revenue is a value trap, not a coiled spring
- **AI-washing** — theme exposure claimed in the deck but absent from the revenue mix; demand segment-level proof

---

## Operating Principles

1. **Live data only, Yahoo Finance first.** Market caps, growth rates, and multiples must be pulled fresh with as-of dates — via `fetch_all()`/`Outputs/{TICKER}/` JSON before any `WebSearch`. Reserve `WebSearch` for what Yahoo Finance can't provide (coverage counts, ownership, qualitative context). Never screen from memory.
2. **Base rates over stories.** Every shortlisted name should rhyme with the historical winner profile; every deviation is a named risk.
3. **Prefer boring-but-advantaged over exciting-but-contested.** 
4. **The shortlist is hypotheses, not picks.** No position without the full deep dive.
5. **Expect to be early and underwater.** State it in the output: the historical price of a 10x is sitting through a 50% drawdown.

---

## Output Format

Default deliverable: a **`.docx` idea-generation memo**, built with `python-docx` per this project's Word Document Generation conventions (import helpers from `doc_utils.py`, portrait/narrow-margin sections, `add_footnote(doc)` before save), saved to `Outputs/multibagger_screener_{theme_or_date}_{YYYYMMDD}.docx`, structured as: hunting-ground rationale → funnel summary (how many screened → gated → scored) → shortlist table → per-name hooks with DNA scorecards → twin-engine tables → anti-pattern exclusions worth noting → handoff recommendation.

For a quick take in chat: shortlist table + hooks only.

---

## Optional Integrations

This skill is fully standalone. If the following happen to be installed, use them where noted — but never require them:

- `/industry_trend_analysis` (or `/emerging_industry_trend` for undiscovered themes) — for the theme-driven hunting ground in Stage 1.
- `/single_stock_quick_research` (or `/single_stock_deep_research` for the full suite) — for the post-shortlist handoff.
- `python-docx` via `doc_utils.py` — for the memo deliverable, following this project's Word Document Generation conventions.

---

## Disclaimer

Every output must include a brief note that the analysis is for informational and educational purposes, is not personalized investment advice, and that outsized-return investing carries a materially elevated risk of permanent capital loss — placed at the end, unobtrusive, once.
