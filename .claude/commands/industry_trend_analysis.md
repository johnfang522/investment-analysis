---
description: >
  A structured framework for professional investors to identify emerging macro themes ("the next big thing"), map their full value chain to surface investable stocks at every layer, and define the conditions under which the theme is peaking or reversing. Use this skill whenever the user asks about spotting trends, identifying emerging themes, finding value chain plays, picking stocks in a new technology cycle, or mapping who wins in a given sector shift. Also trigger when the user asks questions like "what's the next big thing in X", "where should I invest in the AI/energy/biotech/etc. trend", "who are the picks-and-shovels plays", "which stocks benefit from X", or "help me build an investment thesis around Y". Also trigger for the exit side of a theme: "is this theme peaking", "is the X trade over", "when should I sell out of this theme", "how do I know this trend is reversing", "what would break this thesis", "is this a bubble", or "what are the warning signs for X". Always use this skill for investor-facing trend and theme analysis — do not rely on ad-hoc responses.
---

# Industry Trend Analysis Framework

A three-part framework for professional investors: (1) identify a credible emerging trend using 5 convergence signals, (2) map the full value chain to surface stocks at every layer, and (3) define in advance the conditions under which the theme is peaking or reversing — the exit discipline.

**House style — buy-side, for the PM.** Write this as a hedge-fund analyst building a thematic book, not a strategist publishing a survey. The deliverable is actionable: a directional **theme posture** (theme conviction X/10 + how to express it — long basket, pair trade, or underweight), an explicit **variant view** on where consensus is wrong, layer-level overweight/underweight calls, and **pre-committed exit tripwires**. Lead with the conclusion; the signals and value chain justify it.

**Entry logic and exit logic are separate disciplines.** A theme that clears the convergence test is not thereby safe to hold indefinitely — most thematic capital is lost not by picking the wrong theme but by holding the right theme past its peak. Part 3 is therefore mandatory in every run, including when the theme scores 4–5/5 on convergence. The strongest themes generate the most complacency.

---

## Instructions

The user has invoked `/industry_trend_analysis` with the following argument: `$ARGUMENTS`

### Argument resolution — do this before anything else

**Step A — Classify the argument:**

1. **Empty argument:** Ask the user to specify a theme or trend to analyze (e.g., "physical AI", "energy storage", "GLP-1 drugs", "quantum computing"). Do not proceed until they answer.

2. **Looks like a stock ticker** (1–5 uppercase letters, or a recognisable company name like "nvts", "nvda", "tsmc", "arm"): Do NOT run the analysis on the company — run it on the industry theme the company represents.
   - First, use `WebSearch` to identify what sector/theme the ticker is primarily known for (e.g., `NVTS` → GaN/SiC wide-bandgap power semiconductors; `NVDA` → AI accelerator / GPU compute; `ARM` → CPU/SoC IP licensing; `LLY` → GLP-1 / obesity drugs).
   - Derive a clear, descriptive theme name from that research (e.g., "GaN/SiC Wide-Bandgap Power Semiconductors", "AI GPU Compute & Accelerator Infrastructure").
   - State the mapping explicitly before proceeding: *"Argument detected as ticker [X]. Mapping to theme: [Theme Name]. Running analysis on the theme, not the individual stock."*
   - The input ticker's company **will appear** in the value chain map at the appropriate layer alongside all other relevant companies — it does not get special treatment or a dedicated focus section.

3. **Looks like a theme or descriptive phrase** (e.g., "humanoid robotics", "nuclear energy", "quantum computing", "edge AI inference"): Treat it directly as the theme and proceed.

In all non-empty cases, perform the full framework below, supplementing with `WebSearch` to find current named companies, recent capital flows, talent movements, regulatory developments, and cost curve data specific to the theme.

### Theme-first, ticker-neutral rule

Regardless of whether the argument was a ticker or a theme name, the entire analysis must be **theme-first and ticker-neutral**:
- Every value chain layer lists **all materially relevant companies** — not just the input ticker's company.
- No section of the analysis focuses exclusively on the input ticker.
- The input ticker's company is listed where it belongs in the value chain alongside its peers, with the same level of detail.
- The document filename uses the **derived theme name**, not the ticker (e.g., `gan_sic_wbg`, not `nvts`).
- The document title reflects the theme, with a subtitle noting the triggering argument if it was a ticker (e.g., "Triggered by: NVTS — mapped to GaN/SiC WBG theme").

---

## Part 1 — Trend Identification: The 5 Convergence Signals

A trend becomes investable when **2 or more** of these signals converge simultaneously. Evaluate each signal independently, then assess convergence.

### Signal 1: Technology Inflection
- A key input cost curve breaks non-linearly (compute, battery, sequencing, bandwidth, materials).
- A new capability emerges that was previously impossible or uneconomical.
- Watch: patent filings, academic citations, startup founding dates clustering around a specific year, cost-per-unit charts turning the corner.
- **Question to answer:** What becomes newly possible or 10× cheaper?

### Signal 2: Regulatory Shift
- A door opens: new approvals, deregulation, new market structure (spectrum auctions, crypto frameworks, drug approvals, energy mandates).
- A door closes on incumbents: bans, compliance mandates, carbon pricing.
- Watch: congressional testimony, EU/FDA/FCC rulemaking calendars, lobbying spend by incumbents (high spend = they feel threatened).
- **Question to answer:** Who benefits from the new rules, and who is exposed?

### Signal 3: Behavioral Change
- Consumer or enterprise habits shift at scale and show signs of irreversibility.
- Proxy metrics: NPS scores, cohort retention, reorder rates, time-on-platform.
- Key test: did behavior revert after the forcing event ended? (COVID → remote work, telehealth, e-commerce — partial reversion signals vs. permanent shifts)
- **Question to answer:** Is this a permanent new baseline or a temporary spike?

### Signal 4: Capital Flow Signal
- Top-tier VC firms, sovereign wealth funds, corporate venture arms concentrate bets in a sector.
- Signal quality: concentration matters more than total volume. One fund making 10 bets in a theme outweighs 50 funds making 1 each.
- Watch: PitchBook/Crunchbase deal clustering, LP letters from top-quartile managers, strategic M&A by incumbents (buying rather than building = late but confident).
- Lead time: smart capital typically leads public market recognition by 12–36 months.
- **Question to answer:** Are the best-informed allocators concentrating here?

### Signal 5: Narrative Momentum
- Talent migration: where are the best engineers, scientists, and executives moving? LinkedIn senior-hire data is a leading indicator.
- Conference agenda shift: when a theme moves from a breakout session to a keynote, it has crossed the chasm.
- Media inflection: distinguish between trade press coverage (early, specific) and mainstream coverage (later, often peak hype).
- **Question to answer:** Is the talent and attention flywheel accelerating?

### Convergence Assessment
| Signals firing | Interpretation |
|---|---|
| 1 signal | Interesting — monitor, do not act |
| 2 signals | Emerging — begin deep diligence |
| 3 signals | Credible trend — build initial positions |
| 4–5 signals | Strong conviction — size up; also check for crowding |

---

## Part 2 — Value Chain Map: Where the Money Is Made

Once a theme is identified, map the full value chain across 6 layers.
For each layer provide: definition, named companies or company types relevant to the specific theme, moat characteristics, and cycle timing.

### Layer 1 — Infrastructure ("Picks & Shovels")
- **What:** Raw input suppliers — chips, materials, energy, bandwidth, physical space.
- **Why it wins early:** Demand exceeds supply before anyone knows who the application winners will be. You don't need to pick the winner.
- **Moat:** Physical scarcity, capex barriers, long lead times.
- **Timing:** Outperforms in years 1–5 of a cycle; can compress when supply catches up.
- **Examples archetype:** Semiconductor fabs, rare earth miners, data center REITs, fiber backbone operators.

### Layer 2 — Enablers (Platforms & Tools)
- **What:** Software, APIs, developer tooling, cloud services that make the technology usable at scale.
- **Why it wins:** Every application company buys from this layer. High revenue visibility, often recurring.
- **Moat:** Developer lock-in, ecosystem network effects, switching costs.
- **Timing:** Peaks mid-cycle (years 3–8) as application companies proliferate.
- **Examples archetype:** Cloud hyperscalers in mobile era, model API providers in AI era, orchestration platforms, data infrastructure.

### Layer 3 — Integrators (System Builders)
- **What:** Companies that combine layers 1 and 2 into a deployable, complete product or service.
- **Why it wins:** First visible winners — customers pay for a solution, not components. Often the first large-cap to emerge.
- **Moat:** Brand, distribution, execution, systems integration expertise.
- **Timing:** Early to mid-cycle (years 2–6); watch for commoditization risk as the stack matures.
- **Examples archetype:** EV manufacturers buying cells + software, autonomous vehicle platforms, turnkey industrial AI systems.

### Layer 4 — Applications (End-Use Products)
- **What:** Direct consumer or enterprise value delivery. Revenue model is clearest here — subscription, usage, transactional.
- **Why it wins:** Largest addressable markets; narrative is easiest to communicate to generalist investors.
- **Risk:** Valuations catch up fastest here; competitive moats can be thin if the underlying tech is commoditized.
- **Moat:** Brand, data network effects, distribution, regulatory moats.
- **Timing:** Mid to late cycle (years 4–10); high dispersion of outcomes.
- **Examples archetype:** Fintech apps, digital health platforms, SaaS on top of AI models, consumer genomics.

### Layer 5 — Adjacent Beneficiaries
- **What:** Incumbents whose total addressable market expands, or whose cost structure permanently improves, due to the new technology.
- **Why it wins:** Most overlooked layer. No thematic label, so often missed by thematic investors. Trades at lower multiples with less crowding.
- **Moat:** Existing distribution, brand, regulatory relationships — now paired with a new tailwind.
- **Timing:** Often lags the theme by 2–4 years as the productivity benefit shows up in margins.
- **Examples archetype:** Traditional logistics companies adopting autonomous routing, banks with AI fraud detection, pharma using ML in drug discovery.

### Layer 6 — Bottleneck (Highest Structural Moat)
- **What:** Single-source inputs, irreplaceable geography, hard-to-replicate patents, or embedded regulatory licenses.
- **Why it wins:** Moat is structural, not positional — wins across all cycle phases, not just one window.
- **Moat:** By definition: cannot be replicated quickly regardless of capital.
- **Timing:** Durable across the full cycle. Most defensive in a downturn.
- **Examples archetype:** TSMC (advanced node fabs), rare earth processing monopolies, port and terminal operators in critical shipping lanes, spectrum license holders, patent-protected API inhibitors.
- **How to find:** Ask — "if this theme plays out fully, what single thing does every winner have to buy from one or two suppliers?"

---

## Part 3 — Peak & Reversal Detection: The 6 Exhaustion Signals

Part 1 asks "is this trend real?" Part 3 asks "**when does being right stop paying?**" Define exit conditions *before* the position is on, so the exit is a rule, not a reaction. A theme rarely dies from one cause — watch for **2 or more** signals firing (the same convergence logic as Part 1, inverted).

### Exhaustion Signal 1: Convergence Signal Inversion
The 5 entry signals can roll over — recheck each for deterioration: tech cost curve flattens (<~20%/yr gains, node slips) · subsidies/mandates get clawed back or reversed · retention/reorder/pilot-to-production stalls · capital decelerates (down rounds, fewer deals but bigger size) · narrative saturates (media peak, theme ETFs launch, talent exits).
**Question:** Which of the 5 entry signals no longer hold?

### Exhaustion Signal 2: Supply Catch-Up & Capacity Overshoot
The most reliable killer of Layer 1 (Infrastructure) returns, and earliest visible in hard data: lead times shorten · book-to-bill falls below 1.0, backlog shrinks, cancellations appear · announced industry capacity (summed across all producers) exceeds credible demand growth · channel inventory builds as growth decelerates · spot pricing falls below contract pricing.
**Question:** Is the scarcity being engineered away, and on what timeline?

### Exhaustion Signal 3: Valuation & Crowding Extremes
Positioning risk, not fundamental risk — turns a modest miss into a 40% drawdown: multiple expansion outpaces estimate revisions (decompose the return) · thematic ETF/AUM inflows accelerate · short interest collapses, ratings cluster at Buy · issuance window opens (IPOs, secondaries, converts, SPACs priced into strength) · insider selling accelerates, lock-ups cluster · intra-basket correlation rises toward 1.
**Question:** What is priced in, and who is left to buy?

### Exhaustion Signal 4: Unit Economics & Margin Erosion
Growth continues but profitability doesn't: gross margins compress across *multiple* companies in the layer simultaneously (structural, not one-off execution) · ASPs fall faster than unit costs · competitor count rises, differentiation collapses to price · customers dual-source or in-source · incremental ROIC falls below cost of capital.
**Question:** Is growth still creating value, or is the layer competing the economics away?

### Exhaustion Signal 5: Demand-Side Funding Stress
Who actually pays, and with whose money? Demand not funded by the customer's own operating cash flow is the most fragile kind: end demand depends on venture/government/subsidy funding or one buyer · customer concentration rises · vendor financing or circular equity-for-revenue deals appear · backlog is weak-counterparty or non-binding · customers' own funding conditions deteriorate.
**Question:** If capital markets closed for 12 months, what share of demand disappears?

### Exhaustion Signal 6: Macro & Policy Regime Shift
Thematic equities are long-duration assets — the discount rate drives the multiple regardless of fundamentals: real rates rise materially · credit spreads widen, closing the financing window · the underwriting subsidy/policy regime faces election, expiry, or reconciliation risk · trade policy fragments the supply chain or TAM · input/energy/labor cost shocks break the cost curve.
**Question:** Does this theme require a specific macro/policy regime, and how durable is it?

### Peak Verdict Mapping
| Exhaustion signals firing | Verdict | Action |
|---|---|---|
| 0–1 | **Intact** — trend healthy | Hold / continue building on weakness |
| 2 | **Late-cycle** — first cracks | Stop adding; tighten stops; rotate toward Layer 6 (bottlenecks) and Layer 5 (adjacent) |
| 3 | **Peaking** — distribution underway | Trim into strength; cut the most crowded/highest-multiple layer first |
| 4+ | **Reversing** — regime change | Exit the theme basket; only structurally moated bottleneck names survive a full cycle down |

### Layer Sequencing — What Breaks First
Layers do not peak simultaneously. Expect this order, and use it to decide what to cut first:
1. **Layer 4 (Applications)** and the most narrative-driven names de-rate first — highest multiples, thinnest moats, most retail ownership.
2. **Layer 3 (Integrators)** follows as commoditization compresses the systems-integration premium.
3. **Layer 1 (Infrastructure)** breaks when capacity catches up — often the most violent move, because the scarcity premium unwinds fast and capex commitments are already sunk.
4. **Layer 2 (Enablers)** holds longer on recurring revenue, but re-rates as customer growth slows.
5. **Layer 5 (Adjacent Beneficiaries)** and **Layer 6 (Bottlenecks)** are last and least — Layer 6 by definition survives the cycle, which is why it is the defensive core of a thematic book.

### The False-Alarm Test — Correction or Regime Change?
Most thematic drawdowns are not peaks. Before acting on exhaustion signals, run this discrimination test — selling a healthy theme into a mid-cycle correction is as costly as holding a dead one:
- **Are the fundamentals confirming?** A price drawdown with backlog, bookings, lead times and estimate revisions still rising is a positioning flush, not a peak. A drawdown *with* deteriorating order data is the real thing.
- **Is it theme-specific or market-wide?** Compare the basket to the broad index and to comparable long-duration baskets. A theme falling with everything else is a discount-rate event; a theme falling alone is a thesis event.
- **Which signals are firing?** Signals 2 and 4 (supply catch-up, margin erosion) are *structural* and hard to reverse. Signals 3 and 6 (crowding, macro) are *cyclical* and frequently reverse — crowding unwinds create the best entry points in an intact theme.
- **Has the end state changed?** Restate the Section 1 "end state" in one sentence. If it is still credible on the same timeline, the theme is intact and the drawdown is an entry. If the timeline has slipped by years or the end state now requires a technology or subsidy that is not arriving, the theme has changed.

### Historical Calibration
Use these as base rates for what a peak actually looked like in real time, and name the closest analogue for the theme under analysis:
- **Dot-com (2000):** narrative saturation plus an issuance window wide open; infrastructure (telecom/fiber) overbuilt by a factor of 10x and took a decade to absorb.
- **Solar (2008, 2011):** subsidy-dependent demand plus Chinese capacity overshoot — Signals 2, 5 and 6 firing together.
- **Shale (2014):** capital-markets-funded demand met an OPEC supply decision; the funding-stress signal was visible in negative free cash flow years before the break.
- **3D printing (2014), cannabis (2019), EV/SPAC (2021):** classic Signal 3 peaks — thematic ETF launches and issuance windows marked the top within quarters, with fundamentals rolling over later.
- **Crypto (2022):** macro regime shift (Signal 6) plus circular/vendor-financed demand (Signal 5).

---

## Output Format

Produce the following sections in order:

### 1. Introduction

Write a concise introduction using 4–6 bullet points. Each bullet should be one to two sentences. Cover:
- **What is this theme?** — Plain-language definition of the technology, behavior, or structural shift at the center of it.
- **Why now?** — The key recent change (cost curve break, regulatory milestone, scientific breakthrough, or behavioral shift) that makes this relevant today.
- **End state** — One concrete, specific picture of what the world looks like if this plays out (which industries disrupted, what disappears, what new behavior becomes normal).
- **Investment opportunity** — Magnitude of expected capital flows, rough timeline, and what distinguishes this from prior hype cycles (or why it may still be investable despite resembling one).
- 1–2 additional bullets for any critical context a new reader needs (e.g., a key enabling technology, a defining constraint, or a common misconception to dispel).

Use `WebSearch` to ground at least 2 bullets with current facts, statistics, or recent events.

---

### 2. Trend Assessment (5 Convergence Signals)

Score each of the 5 signals as one of: ✅ Firing / ⚠️ Partial / ❌ Not yet.
For each, write 1–3 sentences of rationale citing specific current evidence found via WebSearch (recent data points, named companies, regulatory events, cost curves, capital raises). Then give a convergence verdict with cycle stage.

Format as a table:

| Signal | Status | Rationale |
|---|---|---|
| Technology Inflection | ✅ / ⚠️ / ❌ | ... |
| Regulatory Shift | ✅ / ⚠️ / ❌ | ... |
| Behavioral Change | ✅ / ⚠️ / ❌ | ... |
| Capital Flow | ✅ / ⚠️ / ❌ | ... |
| Narrative Momentum | ✅ / ⚠️ / ❌ | ... |

**Convergence verdict:** X/5 signals firing — [Interesting / Emerging / Credible / Strong conviction]. Estimated cycle stage: [Early / Mid / Late].

---

### 3. Value Chain Map

Populate all 6 layers for the specific theme with named public companies where possible (and private companies or company types where public comps don't yet exist). For each company or type, note:
- **Moat strength:** High / Medium / Low
- **Cycle timing:** Early / Mid / Late
- **Key risk:** one specific risk factor

Present as a table per layer, or a single consolidated table with a Layer column.

---

### 4. TAM Expansion Analysis

This section quantifies how the theme expands addressable markets and identifies which named companies capture the most vs. least of that expansion.

**4a. TAM Expansion Narrative (2–3 paragraphs)**

Describe how this theme creates net-new demand rather than merely redistributing existing spend. Address:
- What markets did not previously exist (or were economically inaccessible) that this theme unlocks?
- What is the order-of-magnitude expansion? (e.g., "legacy TAM was $X; this theme expands it to $Y by 20XX because...")
- Which demand drivers are structural (demographic, regulatory, physical constraints) vs. cyclical (adoption enthusiasm, cheap capital)?

Use `WebSearch` to find analyst TAM estimates, market sizing studies, or company-disclosed SAM/TAM figures. Cite sources and dates.

**4b. Primary Beneficiaries — High TAM Capture**

Identify 4–6 specific named companies most likely to capture disproportionate TAM expansion. For each, explain:
- **Why they capture it:** what structural advantage (moat, position, timing) lets them take share of the new market
- **TAM exposure:** what % of their current revenue or business mix is tied to the expanding TAM
- **Upside scenario:** what does revenue look like if TAM expands as projected?

Present as a table:

| Company | Ticker | Why High TAM Capture | TAM Exposure | Upside Scenario |
|---|---|---|---|---|

**4c. Limited Beneficiaries — Low TAM Capture or TAM Risk**

Identify 3–5 named companies that are in the value chain but will capture less TAM expansion than the market assumes — or that face TAM compression from the same trend. For each, explain:
- **Why they underperform:** commoditization pressure, addressable segment too small, displaced by the trend, or margin compression from new entrants
- **Common mistake:** why investors might initially lump them into the theme incorrectly
- **What to watch:** the signal that confirms or refutes this concern

Present as a table:

| Company | Ticker | Why Limited Capture | Common Investor Mistake | Signal to Watch |
|---|---|---|---|---|

---

### 5. Positioning Recommendation

**Open with the Variant View — Consensus vs. Our Read** (table). This is the buy-side value-add: where do we diverge from how the market is currently positioned on this theme?

| Debate | Consensus / Crowded View | Our Read |
|---|---|---|
| [The core debate on the theme — e.g., which layer captures the economics?] | [where the market is positioned + why] | [our differentiated read + evidence] |
| [Second debate — e.g., is the timing earlier/later than consensus thinks?] | [consensus] | [our read] |

**Theme posture:** state a directional verdict — **Theme Conviction X/10** and **how to express it** (e.g., "long a basket of Layer 1 + Layer 6 names; pair against crowded Layer 4 applications," or "monitor only — too early to size"). Add a one-line **The edge:** naming what consensus is mispricing. **If the structural analysis confirms the market's current positioning on this theme, state that explicitly — a forced variant view is a bias, not an edge.**

Then 2–4 paragraphs. Given where we are in the cycle, suggest how to weight across layers (e.g., "overweight Infrastructure and Bottlenecks; underweight Applications until revenue models clarify"). Call out any crowding risk,
valuation excess, or consensus positioning to fade. Be specific about which named companies or types look most attractive vs. most risky at this stage. Reference the TAM Expansion Analysis findings where relevant.

---

### 6. Peak & Reversal Watch — When to Be Concerned

The exit discipline. This section is **mandatory in every run**, including when convergence scores 4–5/5. Lead with the verdict, then the evidence.

**6a. Exhaustion Scorecard**

Score each of the 6 exhaustion signals as ✅ Firing / ⚠️ Early warning / ❌ Not yet, with specific current evidence found via `WebSearch` — lead times, book-to-bill, pricing data, ETF launches, funding rounds, policy calendars. Where a signal is not yet firing, still name the **specific metric and threshold** that would make it fire.

| Exhaustion Signal | Status | Evidence / What Would Trip It |
|---|---|---|
| 1. Convergence Signal Inversion | ✅ / ⚠️ / ❌ | ... |
| 2. Supply Catch-Up & Capacity Overshoot | ✅ / ⚠️ / ❌ | ... |
| 3. Valuation & Crowding Extremes | ✅ / ⚠️ / ❌ | ... |
| 4. Unit Economics & Margin Erosion | ✅ / ⚠️ / ❌ | ... |
| 5. Demand-Side Funding Stress | ✅ / ⚠️ / ❌ | ... |
| 6. Macro & Policy Regime Shift | ✅ / ⚠️ / ❌ | ... |

**Peak verdict:** X/6 signals firing — [Intact / Late-cycle / Peaking / Reversing]. Estimated time to peak: [quarters or years, with the reasoning]. This verdict must be **consistent with** the Section 2 cycle stage — if Section 2 says "early cycle" and this section says "peaking", resolve the contradiction explicitly rather than publishing both.

**6b. Tripwires — Pre-Committed Exit Triggers**

The core deliverable of this section: named, observable, falsifiable tripwires with the action attached. No vague language ("watch for slowing growth") — every tripwire needs a **number or event**, a **source where it is observable**, and the **portfolio action** it triggers. Produce 5–8 rows covering at least three different exhaustion signals.

| # | Tripwire (specific, measurable) | Signal | Where Observed | Action if Triggered |
|---|---|---|---|---|
| 1 | [e.g., "Lead times for [component] fall below X weeks, or book-to-bill prints <1.0 for two consecutive quarters"] | 2 | [e.g., quarterly earnings calls of named suppliers; SEMI/industry data] | [e.g., "Cut Layer 1 exposure by half"] |

**6c. Watch Calendar — Dated Catalysts**

List the specific dated or near-dated events over the next 12–18 months that could confirm or break the theme. Use `WebSearch` to find real dates. Each entry: date/window, event, and which way it cuts.

| Date / Window | Event | Bullish if... | Bearish if... |
|---|---|---|---|

**6d. False-Alarm Test**

Apply the four discrimination questions (fundamentals confirming, theme-specific vs. market-wide, structural vs. cyclical signals, has the end state changed) to this specific theme. Write 4 bullets, one per question, each naming the actual metric to check. State explicitly which exhaustion signals for *this* theme would be structural (act on) versus cyclical (likely a buying opportunity).

**6e. Closest Historical Analogue**

Name the single closest historical peak analogue for this theme in 2–4 sentences. State what marked that top in real time, what the drawdown was from peak to trough, how long it took to recover (or whether it did), and the one concrete way this theme differs from that analogue. Be honest where the comparison is unflattering — a forced reassurance is worth nothing to the PM.

---

### 7. Key Diligence Questions

List 3–5 specific questions an investor must be able to answer before committing capital. Make them precise and falsifiable — not generic ("understand the market size") but specific ("can actuator cost reach $X/unit at scale needed for sub-$50K robot BOM?").

At least one question must address the **downside/exit case** — the specific thing that would have to be true for the theme to peak within the investment horizon.

---

## Research Process

Before writing the output:

1. Use `WebSearch` to gather current evidence for each of the 5 signals (recent cost curve data, regulatory filings, funding rounds, talent moves, conference coverage).
2. Use `WebSearch` to identify named public and private companies at each value chain layer for the specific theme.
3. Use `WebSearch` to check current valuations and analyst sentiment for the most prominent public names, to inform the positioning recommendation.
4. Use `WebSearch` to gather current evidence for the 6 exhaustion signals — this is separate research from step 1, not a re-reading of it. Look specifically for: lead times and book-to-bill commentary from named suppliers' most recent earnings calls, announced capacity additions across the whole layer (sum them), average selling price and gross margin trends, thematic ETF launches and AUM flows, short interest and insider transactions, down rounds or flat rounds, customer concentration and vendor-financing arrangements, and the dated policy/subsidy/election calendar for the next 12–18 months.
5. Use `WebSearch` to confirm the facts of the historical analogue named in Section 6e — the actual peak date, drawdown magnitude, and recovery time. Do not rely on memory for these figures.

Cite specific data points, dates, and sources inline where they add credibility.
Do not rely on training data alone for company names, funding amounts, or regulatory status — these change rapidly.

---

## Document Output

After producing the full analysis, save it as a Word document using `python-docx`.

- **Output path:** `Outputs/industry_trend_analysis_{theme}_{yyyymmdd}.docx`
  - `{theme}` is always the **derived theme name**, lowercased with spaces replaced by underscores — never the raw ticker symbol (e.g., `gan_sic_wbg`, `physical_ai`, `energy_storage`). If the argument was a ticker, use the theme you mapped it to.
  - Replace `{yyyymmdd}` with today's date in YYYYMMDD format.
  - Example: `Outputs/industry_trend_analysis_physical_ai_20260420.docx`

Write and execute a Python script using `.venv/Scripts/python` that:
1. Creates the document with a title heading matching the **derived theme name** (never the raw ticker). If the argument was a ticker, add a subtitle line: `"Triggered by: [TICKER] — mapped to [Theme Name]"`.
2. **Set the house format (landscape, narrow margins, Arial 10pt)** immediately after creating the document:
   ```python
   setup_document(doc)  # landscape Letter, 0.5" margins, Arial 10pt body text
   ```
3. Renders all 7 output sections with appropriate headings, paragraphs, tables, and bullet points as specified below. Follow the per-section formatting rules exactly.
4. For all tables, uses `python-docx` table objects. Always initialize tables with `rows=1` (header only), then call `table.add_row()` for each data row. Never pass a pre-sized `rows` count.
5. **Every table must use AutoFit to Contents and have visible borders — applied AFTER all rows are added.** The critical rule: `autofit_table` and `add_table_borders` must be called **after** all data rows have been added to the table, not at creation time. Rows added after these helpers are called will not inherit the settings. Use this pattern for every table without exception:
   ```python
   table = doc.add_table(rows=1, cols=N)
   # ... populate header row ...
   # ... add all data rows with table.add_row() ...
   autofit_table(table)      # call AFTER all rows are added
   add_table_borders(table)  # call AFTER all rows are added
   ```

   Import the shared helpers from `doc_utils.py` (in the project root):
   ```python
   import sys; sys.path.insert(0, '.')
   from doc_utils import setup_document, autofit_table, add_table_borders, set_row_font_size, add_footnote, fmt_value
   ```
   Use `fmt_value(v)` for all dollar amounts in table cells (auto-scales: ≥$1B → `$X.XXB`, ≥$1M → `$X.XM`, ≥$1K → `$X.XK`). Never hardcode `/ 1e9` or manually append `"B"`.

6. **All non-header table cell text must use font size 10 (Arial).** Call `set_row_font_size(row)` (imported above) on every data row immediately after `table.add_row()`. Do **not** call it on the header row.
7. Calls `add_footnote(doc)` immediately before `doc.save(...)` to append the standard AI disclaimer.
8. Saves the file to the output path above.

---

### Per-Section Formatting Rules

#### Section 1 — Introduction
- Heading 1: "1. Introduction"
- Write 4–6 bullet points (no prose paragraphs). Each bullet is 1–2 sentences.

#### Section 2 — Trend Assessment
- Heading 1: "2. Trend Assessment: The 5 Convergence Signals"
- Open with a **summary table** (3 columns: Signal | Status | One-Line Verdict). Keep the One-Line Verdict to a single concise sentence — do not put long rationale in the table cell.
- After the table, write the **convergence verdict** as a bold paragraph: "Convergence Verdict: X/5 signals firing — [level]. Estimated cycle stage: [Early/Mid/Late]."
- Then add one **Heading 2 sub-section per signal** (e.g., "Technology Inflection — ✅ Firing"). Under each heading, write the detailed rationale as **3–5 bullet points**, each citing a specific data point, named company, date, or figure. Do not use prose paragraphs in these sub-sections.

#### Section 3 — Value Chain Map
- Heading 1: "3. Value Chain Map"
- For **each of the 6 layers**, emit:
  1. A **Heading 2** with the layer name and color label (e.g., "Layer 1 — Infrastructure ('Picks & Shovels')")
  2. A **one-sentence italicized definition** of what this layer means for the specific theme
  3. A **per-layer table** with columns: Company / Type | Ticker | Description | Moat Strength | Cycle Timing | Key Risk
     - **Description** is a 1–2 sentence plain-language summary of what the company does and why it is relevant to this theme
     - Apply the layer's background fill color to every data row (not the header row) using the `w:shd` XML element:
       - Layer 1 — Infrastructure: `D6E4F0` (light blue)
       - Layer 2 — Enablers: `D5E8D4` (light green)
       - Layer 3 — Integrators: `FFF2CC` (light yellow)
       - Layer 4 — Applications: `FCE4D6` (light orange)
       - Layer 5 — Adjacent Beneficiaries: `E1D5E7` (light purple)
       - Layer 6 — Bottlenecks: `F4CCCC` (light red/pink)
- Do **not** use a single consolidated table for all layers — each layer gets its own table.

#### Section 4 — TAM Expansion Analysis
- Heading 1: "4. TAM Expansion Analysis"
- **4a. TAM Expansion Narrative**
  - Heading 2: "4a. Market Size & Growth Drivers"
  - Write 1 short framing paragraph (2–3 sentences) explaining the net-new demand thesis.
  - Then emit a **bullet list of key TAM data points**: market size today, projected size, CAGR, source, and date — one bullet per data point/segment. Example: "• Global optical interconnect market: $15.4B (2025) → $43B (2034) at 12% CAGR (Mordor Intelligence, 2025)"
  - Then write a short paragraph (3–5 sentences) distinguishing structural demand drivers from cyclical ones.
- **4b. Primary Beneficiaries**
  - Heading 2: "4b. Primary Beneficiaries — High TAM Capture"
  - Table with columns: Company | Ticker | Why High TAM Capture | TAM Exposure | Upside Scenario
- **4c. Limited Beneficiaries**
  - Heading 2: "4c. Limited Beneficiaries — Low TAM Capture or TAM Risk"
  - Table with columns: Company | Ticker | Why Limited Capture | Common Investor Mistake | Signal to Watch

#### Section 5 — Positioning Recommendation
- Heading 1: "5. Positioning Recommendation"
- **Open with the Variant View table** (3 columns: Debate | Consensus / Crowded View | Our Read), dark-blue header row.
- Then a bold **Theme Posture** line: "Theme Conviction X/10 — [how to express it]", followed by a bold "The edge:" bullet.
- Then a **Layer Weighting Summary table** (3 columns: Layer | Weight | Rationale), where Weight is one of: Overweight / Neutral / Underweight. Keep Rationale to one short phrase.
- Then write **one bullet per named company or company type** you recommend acting on, formatted as: "**TICKER / Name** — [1-sentence action and reason]". Group bullets under bold sub-labels: **Overweight**, **Neutral**, **Underweight**.
- Close with 1–2 prose paragraphs covering crowding risk, valuation caution, or entry timing nuance. Reference the Section 6 peak verdict explicitly — the layer weightings must be consistent with it (a "Peaking" verdict cannot sit alongside an Overweight on Layer 4 Applications without a stated reason).

#### Section 6 — Peak & Reversal Watch
- Heading 1: "6. Peak & Reversal Watch — When to Be Concerned"
- Open with a bold **Peak Verdict** paragraph: "Peak Verdict: X/6 exhaustion signals firing — [Intact / Late-cycle / Peaking / Reversing]. Estimated time to peak: [...]." Color the verdict run: green `007000` for Intact, dark yellow `BF8F00` for Late-cycle, orange `FF8C00` for Peaking, red `C00000` for Reversing.
- **6a. Exhaustion Scorecard** — Heading 2. Table with columns: Exhaustion Signal | Status | Evidence / What Would Trip It. Dark-blue header row (`1F3864`), white bold text. Shade the **Status** cell of each data row: ✅ Firing → `FFC7CE` (pink), ⚠️ Early warning → `FFEB9C` (yellow), ❌ Not yet → `C6EFCE` (green). Note the inversion versus the Section 2 signal table — here a firing signal is *bad news*, so the color logic is deliberately reversed. Add a one-line italic note under the table stating this, so a reader flipping between the two tables is not misled.
- **6b. Tripwires** — Heading 2. Table with columns: # | Tripwire | Signal | Where Observed | Action if Triggered. 5–8 data rows. Dark-blue header row. Bold the text in the "Action if Triggered" column.
- **6c. Watch Calendar** — Heading 2. Table with columns: Date / Window | Event | Bullish if... | Bearish if... Dark-blue header row. Order rows chronologically.
- **6d. False-Alarm Test** — Heading 2. Four bullet points, one per discrimination question, each naming the specific metric to check. Follow with one bold line: "**Structural signals for this theme (act on):** ... · **Cyclical signals (likely buy the dip):** ..."
- **6e. Closest Historical Analogue** — Heading 2. One short prose paragraph (2–4 sentences), then a small 2-column table (Metric | Value) covering: Analogue, Peak date, Peak-to-trough drawdown, Recovery time, Key difference vs. this theme.

#### Section 7 — Key Diligence Questions
- Heading 1: "7. Key Diligence Questions"
- Write each question as a **numbered bullet** (Word List Number style). Each question must be specific and falsifiable — include concrete thresholds, named companies, or specific timeframes. No generic questions.

---

## Example Application (for reference — do not reproduce verbatim)

**Theme:** Physical AI / humanoid robotics (2024–2026)

**Signal check:**
- Technology inflection ✅ — transformer-based policy networks, cost of actuators falling, dexterous manipulation crossing threshold
- Regulatory shift ⚠️ — partial; OSHA frameworks lagging, liability unclear 
- Behavioral change ✅ — labor shortages in manufacturing and logistics forcing enterprise adoption
- Capital flow ✅ — concentration in Figure, Physical Intelligence, 1X, Apptronik; strategic bets from automotive OEMs
- Narrative momentum ✅ — talent exodus from FAANG to robotics; NeurIPS and RSS dominated by manipulation papers

**Verdict:** 4/5 signals — strong conviction, early cycle positioning.

**Layer priorities at this stage:** Infrastructure (actuator makers, force sensors, simulation software) and Bottlenecks (NVIDIA sim platforms, specialized motor controller IP) over Applications (too early, no established revenue model at scale).

**Peak & reversal check:**
- Convergence inversion ❌ — all four firing signals still intact; cost curves still breaking
- Supply catch-up ❌ — actuator and force-sensor lead times still extended; no credible capacity overshoot yet
- Crowding ⚠️ — humanoid-robotics ETFs launched and the issuance window is open; sell-side ratings clustering at Buy
- Unit economics ⚠️ — bill-of-materials falling, but no company yet demonstrates positive gross margin at volume
- Demand-side funding ✅ — demand is overwhelmingly venture- and OEM-subsidized pilots rather than customer operating budgets; this is the fragile link
- Macro/policy ❌ — no subsidy dependency; labor-shortage driver is demographic, not policy

**Peak verdict:** 1 firing + 2 early warnings — **Intact, with the funding-stress signal as the live risk.** The tripwire that matters most is not a price level but a conversion rate: if pilot-to-production conversion stalls below ~20% through two consecutive fiscal years while venture funding decelerates, the theme is a decade early rather than three years early. Closest analogue: 3D printing circa 2014 — same signature of real technology, genuine enterprise pilots, and demand that never crossed from innovation budgets into operating budgets.
