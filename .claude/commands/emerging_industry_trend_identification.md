---
description: >
  A structured framework for identifying emerging industry trends and locating their structural bottlenecks before the market fully prices them in. Use this skill whenever the user asks about spotting the next big thing, finding the next CPU/GPU-style narrative, identifying upcoming chokepoints, mapping who wins in a new technology cycle, or asking "what should I invest in next?" Also trigger for questions like "what's the next narrative after X?", "where are the upcoming bottlenecks?", "what trend can I capitalize on?", "who are the picks-and-shovels plays for X?", "what's underpriced in the AI buildout?", or any request to identify investable themes early. Always use this skill for trend-spotting and bottleneck analysis — do not rely on ad-hoc responses. This skill combines proactive web research with a structured analytical framework to surface real, current signals.
---

# Emerging Trends & Bottlenecks Framework

A three-part framework for finding the next big investment narrative:
(1) scan for live signals using web research,
(2) score convergence across 5 dimensions, and
(3) map the value chain to find the structural bottleneck — the single chokepoint every winner has to buy through.

The CPU narrative (2022–2024) is the archetype: technology inflection + capital concentration fired first, bottleneck (TSMC, NVIDIA/CUDA) was identifiable before mainstream coverage. The power/grid narrative (2025–2026) followed the same pattern.
The goal is always to find the *next* one of these before the public market prices it in.

---

## Instructions

The user has invoked `/emerging_industry_trend_identification` with the following argument: `$ARGUMENTS`

If `$ARGUMENTS` is empty, ask the user whether they want to:
(a) scan broadly for the most promising emerging trends right now, or
(b) evaluate a specific theme they have in mind.

Otherwise, treat `$ARGUMENTS` as the theme or question to investigate and run the full three-part framework below.

In either case, **always begin with Step 0 web research** before scoring the signals.

---

## Step 0 — Always Search First

Before applying the framework, use `WebSearch` to pull current signals.
Do not rely on training data alone — trends move faster than knowledge cutoffs.

**Run 3–5 of these queries in parallel:**
- `"next bottleneck" AI infrastructure [current year]`
- `emerging investment trend [sector] [current year]`
- `venture capital concentration [sector] [current year]`
- `[specific theme] supply constraint shortage`
- `[specific theme] lead time backlog orders`

Look for: earnings call language about backlogs, VC deal clustering, CEO quotes naming constraints, analyst reports flagging supply/demand mismatches.

---

## Part 1 — The 5 Convergence Signals

A trend becomes investable when **2 or more** of these fire simultaneously.
Score each: ✅ Firing / ⚠️ Partial / ❌ Not yet.

### Signal 1: Technology Inflection
- A key input cost curve breaks non-linearly (compute, battery, sequencing, bandwidth, materials, energy density).
- A new capability crosses the threshold from "impressive demo" to "deployable at scale and at a price that makes economic sense."
- Watch: patent filings clustering around a specific year, academic citation spikes, startup founding dates concentrating, cost-per-unit charts inflecting.
- **The question:** What becomes newly possible or 10× cheaper this cycle?

### Signal 2: Regulatory Shift
- A door opens: new approvals, deregulation, new market structure.
- A door closes on incumbents: mandates, bans, compliance costs.
- **Key tell:** Incumbent lobbying spend spiking = they feel threatened.
  Watch congressional testimony, EU/FDA/FCC rulemaking calendars.
- **The question:** Who benefits from the new rules, and who is exposed?

### Signal 3: Behavioral Change
- Consumer or enterprise habits shift at scale and show signs of irreversibility.
- **Key test:** Did behavior revert after the forcing event ended?
  COVID → remote work partially reverted. EV adoption did not.
- Proxy metrics: cohort retention, reorder rates, enterprise renewal rates.
- **The question:** Is this a permanent new baseline or a temporary spike?

### Signal 4: Capital Flow Signal
- Concentration matters more than total volume. One top-tier fund making 10 bets in a theme > 50 funds making 1 each.
- Smart capital leads public market recognition by **12–36 months**.
- Watch: PitchBook/Crunchbase deal clustering, LP letters, strategic M&A by incumbents (buying rather than building = late but confident).
- **The question:** Are the best-informed allocators concentrating here?

### Signal 5: Narrative Momentum
- Talent migration: where are top engineers, scientists, executives moving?
  (LinkedIn senior-hire data is a leading indicator.)
- Conference inflection: theme moves from breakout session → keynote = crossed the chasm.
- Media inflection: trade press (early, specific) vs. mainstream (later, often peak hype). You want to be in during the trade press phase.
- **The question:** Is the talent and attention flywheel accelerating?

### Convergence Table
| Signals Firing | Interpretation | Action |
|---|---|---|
| 1 | Interesting — watch | Monitor, don't act |
| 2 | Emerging | Begin deep diligence |
| 3 | Credible trend | Build initial positions |
| 4–5 | Strong conviction | Size up; also check for crowding |

---

## Part 2 — Value Chain Map (6 Layers)

Once a theme is confirmed, map every layer. The bottleneck is almost always found at Layer 1 or Layer 6 — but you need to see the whole stack to find it.

### Layer 1 — Infrastructure ("Picks & Shovels")
- Raw input suppliers: chips, materials, energy, physical space, bandwidth.
- **Why it wins early:** Demand exceeds supply before anyone knows the application winners. You don't need to pick the winner.
- **Moat:** Physical scarcity, capex barriers, long lead times.
- **Timing:** Outperforms years 1–5; compresses when supply catches up.

### Layer 2 — Enablers ("Platforms & Tools")
- Software, APIs, developer tooling, cloud services that make the tech usable.
- **Moat:** Developer lock-in, ecosystem network effects, switching costs.
- **Timing:** Peaks mid-cycle (years 3–8) as application companies proliferate.

### Layer 3 — Integrators ("System Builders")
- Companies that combine Layers 1+2 into a deployable, complete solution.
- **Moat:** Brand, distribution, execution, systems integration expertise.
- **Timing:** Early to mid-cycle (years 2–6); watch for commoditization risk.

### Layer 4 — Applications ("End-Use Products")
- Direct consumer or enterprise value delivery.
- **Risk:** Valuations catch up fastest here; moats can be thin if the underlying tech is commoditized.
- **Timing:** Mid to late cycle (years 4–10); highest outcome dispersion.

### Layer 5 — Adjacent Beneficiaries
- Incumbents whose TAM expands or cost structure permanently improves.
- **Why it wins:** Most overlooked layer. No theme label, so trades at lower multiples with less crowding. Productivity benefit shows up in margins with a 2–4 year lag.
- **Moat:** Existing distribution + brand + regulatory relationships + new tailwind.

### Layer 6 — Bottleneck / Chokepoints ⭐ ("Highest Structural Moat")
- Single-source inputs, irreplaceable geography, hard-to-replicate IP, or embedded regulatory licenses.
- **Why it wins:** Moat is structural, not positional — wins across all cycle phases, not just one window. Most defensive in a downturn.
- **How to find:** Ask — *"If this theme plays out fully, what single thing does every winner have to buy from one or two suppliers?"*
- **Real examples:**
  - GPU era → TSMC (advanced node fabs) + NVIDIA (CUDA ecosystem)
  - Power/grid era → Large transformer manufacturers (2yr+ lead times), grid interconnection queue positions
  - Physical AI → Simulation platforms (NVIDIA Isaac/Omniverse), specialized actuator IP, sensor supply chains

---

## Part 3 — Bottleneck Identification Checklist

Run this checklist specifically to find the Layer 6 chokepoint:

1. **Lead time test:** Is there a component with >12 month lead time?
   Long lead times = structural scarcity = pricing power.

2. **Backlog test:** Are order backlogs expanding faster than revenue?
   Expanding backlog at margin improvement = demand-constrained, not supply-constrained on the earnings side.

3. **Single-source test:** Is there a supplier/geography/platform that >60% of the value chain depends on? (TSMC for cutting-edge nodes, China for 90% of robotics components, grid interconnection queues for data center power.)

4. **CEO quote test:** Are multiple CEOs of large companies publicly naming the same constraint in earnings calls? When Amazon, Microsoft, and Google CEOs all say "power is the bottleneck" in the same quarter — that's the signal. Search for these quotes.

5. **Capex-before-revenue test:** Are companies spending capex now for revenue 2–4 years out? This creates a window where the input supplier wins before the application layer does.

6. **Substitution difficulty test:** Can the bottleneck be substituted quickly?
   If not (transformer manufacturing takes years to scale, grid permitting takes a decade) — the moat is durable.

---

## Output Format

Always produce all four sections below. Use **tables** and **bullet points** throughout — no dense prose paragraphs.

---

### 1. Signal Scorecard

Present as a table:

| Signal | Status | Evidence |
|---|---|---|
| 1. Technology Inflection | ✅ / ⚠️ / ❌ | One-line rationale with specific data point, quote, or source |
| 2. Regulatory Shift | ✅ / ⚠️ / ❌ | … |
| 3. Behavioral Change | ✅ / ⚠️ / ❌ | … |
| 4. Capital Flow | ✅ / ⚠️ / ❌ | … |
| 5. Narrative Momentum | ✅ / ⚠️ / ❌ | … |

Follow the table with two bullet points:
- **Convergence verdict:** X of 5 signals firing → [Monitor / Begin diligence / Build position / Size up]
- **Cycle stage:** Early / Mid / Late — one sentence of reasoning

---

### 2. Value Chain Map

Present as a table:

| Layer | Layer Name | Representative Companies | Moat Strength | Cycle Timing | Key Risk |
|---|---|---|---|---|---|
| 1 | Infrastructure | … | … | … | … |
| 2 | Enablers | … | … | … | … |
| 3 | Integrators | … | … | … | … |
| 4 | Applications | … | … | … | … |
| 5 | Adjacent Beneficiaries | … | … | … | … |
| 6 ⭐ | Bottleneck / Chokepoints | … | … | … | … |

Follow the table with a single bullet: **Highest-conviction layer right now:** [Layer X] — one sentence of reasoning.

---

### 3. Bottleneck Analysis

Present the checklist as a table:

| # | Test | Answer | Implication |
|---|---|---|---|
| 1 | Lead time (>12 months?) | Yes / No / Partial | … |
| 2 | Backlog expanding faster than revenue? | … | … |
| 3 | Single-source dependency (>60%)? | … | … |
| 4 | CEO quote test | … | … |
| 5 | Capex-before-revenue? | … | … |
| 6 | Substitution difficulty? | … | … |

Follow the table with bullets:
- **Top structural chokepoint(s):** Name 1–2 specific companies or asset types
- **Key CEO/executive quotes** (if found via web search — high-signal, include source)

---

### 4. Positioning & Diligence

**Layer weighting given current cycle stage:**

| Layer | Weight | Rationale |
|---|---|---|
| 1 — Infrastructure | Overweight / Neutral / Underweight | … |
| 2 — Enablers | … | … |
| 3 — Integrators | … | … |
| 4 — Applications | … | … |
| 5 — Adjacent | … | … |
| 6 — Bottleneck | … | … |

**Risk flags** (bullet points):
- Crowding check: [crowded / not yet crowded] — reasoning
- Valuation risk: …
- Any other flags

**Diligence questions before committing capital** (3–5 bullet points):
- …
- …
- …

---

## Worked Examples

### Example A — GPU / Compute (2022, now late cycle)
- **Bottleneck found:** TSMC advanced nodes + NVIDIA CUDA lock-in
- **Lead time signal:** H100 allocation waitlists 12+ months in 2023
- **CEO quote signal:** Every hyperscaler CEO named GPU availability as the constraint in Q3 2022 earnings calls
- **Lesson:** By the time mainstream media ran "GPU shortage" stories (mid-2023), the infrastructure layer had already re-rated. The signal was in the trade press and earnings calls 12 months earlier.

### Example B — AI Power Infrastructure (2025–2026, early-mid cycle)
- **Bottleneck found:** Large power transformers (2yr+ lead time), grid interconnection queue positions, SMR/nuclear baseload
- **Lead time signal:** Transformer lead times extending to 24–36 months; GE Vernova book-to-bill near 2.5× in early 2026
- **CEO quote signal:** Jensen Huang: "Energy is the bottleneck." Amazon CEO: "The single biggest constraint is power."
- **Lesson:** The shift from "silicon story" to "power story" was telegraphed in CEO language and equipment company backlogs a full year before mainstream investor rotation.

### Example C — Physical AI / Humanoid Robotics (2026, early cycle)
- **Bottleneck candidates:** Simulation-to-reality platforms (NVIDIA Isaac), precision actuators and force-torque sensors, US-sourced robotics components (geopolitical bottleneck: 90% of components currently from China)
- **Capital signal:** €38.5B VC into robotics in 2025 (9% of all VC)
- **Lesson:** Still early — the bottleneck layer hasn't fully emerged. Monitor actuator/sensor supply chains and sim platform lock-in.

---

## Common Mistakes to Avoid

- **Confusing "interesting theme" with "investable bottleneck."** A trend needs 2+ signals AND an identifiable chokepoint to act on.
- **Acting at mainstream coverage.** By the time CNBC runs a segment on "the GPU shortage," the infrastructure layer has often already re-rated.
- **Ignoring Layer 5.** Adjacent beneficiaries are chronically underowned because they don't carry the theme label. Often the best risk/reward.
- **Crowding check.** At 4–5 signals, always ask: is the trade already consensus? High signal convergence + crowded positioning = risk of disappointment even if the thesis is right.
- **Geopolitical supply chain blindspot.** Always ask whether the bottleneck is in a geopolitically exposed supply chain (e.g., rare earths, robotics components). A US-sourced alternative to a China-dependent bottleneck is itself an investable theme.
