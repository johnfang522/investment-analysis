---
name: multibagger_screener
description: >
  An idea-generation funnel for finding stocks with outsized future return potential (5x, 10x, 100x "multi-baggers") — from hunting ground to scored shortlist. Use this skill whenever the user asks to find, discover, screen for, or generate ideas for high-return stocks; asks "which stocks could 10x", "find me the next NVIDIA/Monster/Amazon", "what small caps
  have big upside", "screen for multi-baggers", "where are outsized returns", or "give me stock ideas in theme X"; or wants a shortlist of candidates rather than analysis of one named stock. This skill takes the user from hunting ground to a scored, ranked shortlist with explicit return math. Always use this skill for idea generation rather than listing stocks ad hoc, and always pull live data (market caps, financials, coverage) rather than relying on memory.
---

# Multibagger Screener

A disciplined funnel for surfacing stocks with genuine outsized-return potential. The premise: multi-baggers are not found by predicting the future better — they are found by fishing where the structural odds are best and filtering hard for a specific, well-documented trait set.

**Qualifying bar: 5x+ over the holding period.** A name does not need 10x or 100x DNA to make the shortlist — genuine, evidence-backed 5x potential is a sufficient outcome for this mandate. Treat 10x-100x candidates as the top of the distribution, not the entry requirement.

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

**Note on the 5x bar specifically:** the base rates above describe the extreme (10x-100x) end of the distribution — smaller, longer, more painful, more ignored than a 5x needs to be. A 5x candidate can be larger, faster, and better-covered than a 100-bagger's starting profile and still clear this mandate. Don't force a 5x candidate to meet 100-bagger-grade extremity on every trait — score it on its own merits against the thresholds below, which are already calibrated to the 5x bar.

---

## The Funnel

### Stage 1 — Define the Hunting Ground

Pick one (or run several in parallel):

1. **Theme-driven:** Identify a credible secular theme, then map its value chain and fish in the least-crowded, highest-moat layers: raw infrastructure suppliers ("picks & shovels"), adjacent beneficiaries (incumbents with a new tailwind but no theme label — least crowded), and bottleneck/chokepoint assets (single-source inputs everyone must buy — highest structural moat). Avoid end-user application names: they are usually crowded and fully priced by the time a theme is visible.
   (Use `/industry_trend_analysis` — or `/emerging_industry_trend` for undiscovered themes — for this step when a full value chain map is needed; otherwise apply the heuristic above directly.)
2. **Neglect-driven:** Small/mid-caps with < 15 analysts, recent spin-offs, post-IPO busts trading below IPO price with improving fundamentals, "boring" industries with a consolidator.
3. **Quality-screen-driven:** Universe screen on the quantitative gate below, theme-agnostic.

State explicitly which hunting ground is being used and why.

### Stage 2 — Quantitative Gate (hard filters)

Pull live data. For any candidate ticker, source market cap, growth, margins, ROIC, balance sheet, and share count from Yahoo Finance first — run `fetch_all([tickers])` (from `yahoo_finance_data.py`) and read the resulting `Outputs/{TICKER}/` JSON files (`{ticker_lower}_quick_metrics.json`, income/balance/cash-flow statements). Only fall back to `WebSearch` for fields Yahoo Finance doesn't carry (analyst coverage counts, insider ownership %, spin-off/IPO context) or for names not yet in `tickers.txt`/`Outputs/`.

A candidate must clear most of these to advance:

| Filter | Threshold | Rationale |
|---|---|---|
| Market cap | < $15B, prefer < $5B | Room to 5x; a 5x from a larger base is still plausible, unlike a 10x-100x |
| Revenue growth | > 10% (3-yr CAGR or clear acceleration) | The growth engine exists — doesn't need to be explosive to compound to 5x over 5-10 yrs |
| Gross margin | > 35% (or top-quartile for its industry) | Pricing power headroom |
| ROIC | > 12%, or clearly inflecting toward it | Reinvestment creates value |
| Balance sheet | Net cash or net debt/EBITDA < 2.5x | Survives the inevitable drawdown |
| Dilution | Share count growth < 4%/yr | Growth is mostly self-funded |
| Analyst coverage | < 20 analysts | Some rerating room still available; doesn't need to be totally undiscovered for a 5x |

Thresholds above are calibrated to the 5x qualifying bar (looser than a 10x-100x screen would require). Exceptions are still allowed with justification (e.g., a chokepoint asset may carry more debt), but every exception must be named as a risk.

### Stage 3 — Multi-Bagger DNA Score

Score survivors on ten traits, 0 (absent) / 1 (partial) / 2 (strong), citing evidence for each:

| # | Trait | What "strong" looks like |
|---|---|---|
| 1 | Small starting size | Market cap under ~$1–5B; a 5x from here is plausible without needing micro-cap extremity |
| 2 | High ROIC | ROIC > 12–15%, above cost of capital |
| 3 | Reinvestment runway | Can redeploy most cash flow at those returns for 5–10 yrs (TAM penetration < ~30%) |
| 4 | Twin-engine setup | Entry multiple at or below market/peers, so growth AND rerating can both work |
| 5 | Owner-operator | Founder-led or manager with 5%+ ownership; skin in the game |
| 6 | Under-followed | < 15–20 analysts; some rerating room still available |
| 7 | Gross-margin strength | High and stable/rising gross margin = pricing power headroom |
| 8 | Self-funding | Growth financed mostly internally, not by heavy serial dilution or debt |
| 9 | Moat that scales | Advantage strengthens with size (network effects, data, unit cost) |
| 10 | Long secular tailwind | Rides a multi-year theme with segment-level revenue proof |

**Interpretation (recalibrated to the 5x qualifying bar):**

| Score | Read |
|---|---|
| 16–20 | Rare — 10x-100x-grade DNA; top of the shortlist |
| 8–15 | **Qualifies — credible 5x+ case; advances.** Name which missing traits are fixable vs. structural |
| 4–7 | Ordinary — may be a fine stock, but the 5x case isn't well-supported yet |
| 0–3 | Pass for this mandate |

Rank the shortlist by score. Names scoring **8+** advance (this is the 5x-calibrated bar — reserve the 16–20 "rare" band for genuine 10x-100x candidates, but don't require it for the shortlist).

### Stage 4 — The Twin-Engine Check (per finalist)

For each finalist, show the return decomposition explicitly:

- Entry multiple today vs. history/peers
- Plausible earnings/FCF growth rate for 5–10 years (tie to runway evidence, not hope)
- Plausible exit multiple (what does this business trade at if it works?)
- **Implied multiple-of-money** = growth compounding × multiple change

| Scenario | EPS/FCF CAGR | Exit multiple | 5–10-yr multiple of money |
|---|---|---|---|
| Engine works, rerates | | | |
| Engine works, no rerate | | | |
| Engine stalls | | | |

The bar to clear is **5x, not 10x** — a scenario that lands at ~4-6x on a 5-10 year horizon is a pass, not a near-miss. If the "no rerate" row still produces at least ~5x, the setup is resilient. If the thesis *requires* rerating to reach 5x, say so — that is a narrower, riskier bet, but can still qualify if the rerate assumption is well-evidenced.

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
- **Already-crowded theme darlings** — > 30 analysts, meme status, or valuation already pricing the bull case (the rerating engine is spent)
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

**Always produce the `.docx` memo — this is not optional and does not depend on whether any name qualifies.** Build it with `python-docx` per this project's Word Document Generation conventions (import helpers from `doc_utils.py`, portrait/narrow-margin sections, `add_footnote(doc)` before save), saved to `Outputs/multibagger_screener_{theme_or_date}_{YYYYMMDD}.docx`, structured as: hunting-ground rationale → funnel summary (how many screened → gated → scored) → quantitative gate table → shortlist table → per-name hooks with DNA scorecards → twin-engine tables (for names that scored 8+) → anti-pattern exclusions worth noting → handoff recommendation.

**A null result (zero names clearing the 8+ DNA threshold) still gets the full memo**, not just a chat message. State plainly in the Shortlist section that no names qualify, why (cite the specific gate/DNA failures), and the recommended next step (broaden the hunting ground, or revisit a name once its fundamentals inflect). Reporting "nothing qualifies" with evidence is a valid, complete deliverable — never force a pick to avoid an empty shortlist.

In chat, always confirm the saved `.docx` path after generating it. You may also give a short in-chat summary (shortlist table + hooks, or the null-result explanation) alongside the file, but the file itself is mandatory on every run.

---

## Optional Integrations

This skill is fully standalone. If the following happen to be installed, use them where noted — but never require them:

- `/industry_trend_analysis` (or `/emerging_industry_trend` for undiscovered themes) — for the theme-driven hunting ground in Stage 1.
- `/single_stock_quick_research` (or `/single_stock_deep_research` for the full suite) — for the post-shortlist handoff.
- `python-docx` via `doc_utils.py` — for the memo deliverable, following this project's Word Document Generation conventions.

---

## Disclaimer

Every output must include a brief note that the analysis is for informational and educational purposes, is not personalized investment advice, and that outsized-return investing carries a materially elevated risk of permanent capital loss — placed at the end, unobtrusive, once.
