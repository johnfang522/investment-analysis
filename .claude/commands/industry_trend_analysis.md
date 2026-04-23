---
description: >
  A structured framework for professional investors to identify emerging macro themes ("the next big thing") and map their full value chain to surface investable stocks at every layer. Use this skill whenever the user asks about spotting trends, identifying emerging themes, finding value chain plays, picking stocks in a new technology cycle, or mapping who wins in a given sector shift. Also trigger when the user asks questions like "what's the next big thing in X", "where should I invest in the AI/energy/biotech/etc. trend", "who are the picks-and-shovels plays", "which stocks benefit from X", or "help me build an investment thesis around Y". Always use this skill for investor-facing trend and theme analysis — do not rely on ad-hoc responses.
---

# Industry Trend Analysis Framework

A two-part framework for professional investors: (1) identify a credible emerging trend using 5 convergence signals, and (2) map the full value chain to surface stocks at every layer.

---

## Instructions

The user has invoked `/industry_trend_analysis` with the following argument: `$ARGUMENTS`

If `$ARGUMENTS` is empty, ask the user to specify a theme or trend to analyze (e.g., "physical AI", "energy storage", "GLP-1 drugs", "quantum computing").

Otherwise, treat `$ARGUMENTS` as the theme/trend to analyze. Perform the full two-part framework below, supplementing with `WebSearch` to find current named companies, recent capital flows, talent movements, regulatory developments, and cost curve data specific to the theme.

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

### Layer 6 — Bottleneck / Chokepoints (Highest Structural Moat)
- **What:** Single-source inputs, irreplaceable geography, hard-to-replicate patents, or embedded regulatory licenses.
- **Why it wins:** Moat is structural, not positional — wins across all cycle phases, not just one window.
- **Moat:** By definition: cannot be replicated quickly regardless of capital.
- **Timing:** Durable across the full cycle. Most defensive in a downturn.
- **Examples archetype:** TSMC (advanced node fabs), rare earth processing monopolies, port and terminal operators in critical shipping lanes, spectrum license holders, patent-protected API inhibitors.
- **How to find:** Ask — "if this theme plays out fully, what single thing does every winner have to buy from one or two suppliers?"

---

## Output Format

Produce the following sections in order:

### 1. Trend Assessment

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

### 2. Value Chain Map

Populate all 6 layers for the specific theme with named public companies where possible (and private companies or company types where public comps don't yet exist). For each company or type, note:
- **Moat strength:** High / Medium / Low
- **Cycle timing:** Early / Mid / Late
- **Key risk:** one specific risk factor

Present as a table per layer, or a single consolidated table with a Layer column.

---

### 3. Positioning Recommendation

2–4 paragraphs. Given where we are in the cycle, suggest how to weight across layers (e.g., "overweight Infrastructure and Bottlenecks; underweight Applications until revenue models clarify"). Call out any crowding risk,
valuation excess, or consensus positioning to fade. Be specific about which named companies or types look most attractive vs. most risky at this stage.

---

### 4. Key Diligence Questions

List 3–5 specific questions an investor must be able to answer before committing capital. Make them precise and falsifiable — not generic ("understand the market size") but specific ("can actuator cost reach $X/unit at scale needed for sub-$50K robot BOM?").

---

## Research Process

Before writing the output:

1. Use `WebSearch` to gather current evidence for each of the 5 signals (recent cost curve data, regulatory filings, funding rounds, talent moves, conference coverage).
2. Use `WebSearch` to identify named public and private companies at each value chain layer for the specific theme.
3. Use `WebSearch` to check current valuations and analyst sentiment for the most prominent public names, to inform the positioning recommendation.

Cite specific data points, dates, and sources inline where they add credibility.
Do not rely on training data alone for company names, funding amounts, or regulatory status — these change rapidly.

---

## Document Output

After producing the full analysis, save it as a Word document using `python-docx`.

- **Output path:** `Outputs/industry_trend_analysis_{theme}_{yyyymmdd}.docx`
  - Replace `{theme}` with the theme argument, lowercased, spaces replaced with underscores (e.g., `physical_ai`, `energy_storage`).
  - Replace `{yyyymmdd}` with today's date in YYYYMMDD format.
  - Example: `Outputs/industry_trend_analysis_physical_ai_20260420.docx`

Write and execute a Python script using `.venv/Scripts/python` that:
1. Creates the document with a title heading matching the theme.
2. **Set narrow page margins** immediately after creating the document:
   ```python
   from docx.shared import Inches
   for section in doc.sections:
       section.top_margin = Inches(0.5)
       section.bottom_margin = Inches(0.5)
       section.left_margin = Inches(0.75)
       section.right_margin = Inches(0.75)
   ```
3. Renders all 4 output sections (Trend Assessment, Value Chain Map, Positioning Recommendation, Key Diligence Questions) with appropriate headings, paragraphs, and tables.
4. For all tables, uses `python-docx` table objects. Always initialize tables with `rows=1` (header only), then call `table.add_row()` for each data row. Never pass a pre-sized `rows` count.
5. **Every table in the document must use AutoFit to Contents — no exceptions.** Implement a reusable `autofit_table(table)` helper and call it immediately after creating every table. The helper must: (a) set `tblW` to `w="0" type="auto"`; (b) set `tblLayout` to `type="autofit"`; (c) strip any existing `w:tcW` elements from every cell so no fixed-width overrides remain. Do NOT use `table.columns[i].width` or any fixed-width assignment anywhere in the script. The helper body must include:
   ```python
   def autofit_table(table):
       tbl = table._tbl
       tblPr = tbl.find(qn('w:tblPr')) or OxmlElement('w:tblPr')
       if tblPr not in tbl: tbl.insert(0, tblPr)
       for tag, attrs in [('w:tblW', {'w:w':'0','w:type':'auto'}), ('w:tblLayout', {'w:type':'autofit'})]:
           el = tblPr.find(qn(tag)) or OxmlElement(tag)
           for k,v in attrs.items(): el.set(qn(k), v)
           if el not in tblPr: tblPr.append(el)
       for row in table.rows:
           for cell in row.cells:
               tcPr = cell._tc.find(qn('w:tcPr'))
               if tcPr is not None:
                   for tcW in tcPr.findall(qn('w:tcW')): tcPr.remove(tcW)
   ```
6. **Every table must have visible borders on all cells (header and data rows).** Implement a reusable `add_table_borders(table)` helper that applies a single thin border (`sz=4`, `val="single"`, `color="000000"`) to all four sides (`top`, `bottom`, `left`, `right`) of every cell using the `w:tcBorders` / `w:tblBorders` XML element. Call this helper immediately after `autofit_table()` on every table.
7. **Part 2 — Value Chain Map table: apply a distinct background fill color to each layer's rows** so layers are visually separated. Use these fills (hex, applied to every data row in that layer):
   - Layer 1 — Infrastructure: `D6E4F0` (light blue)
   - Layer 2 — Enablers: `D5E8D4` (light green)
   - Layer 3 — Integrators: `FFF2CC` (light yellow)
   - Layer 4 — Applications: `FCE4D6` (light orange)
   - Layer 5 — Adjacent Beneficiaries: `E1D5E7` (light purple)
   - Layer 6 — Bottlenecks: `F4CCCC` (light red/pink)
   - Apply fills using the `w:shd` XML element on each `w:tc` (table cell), same pattern used for header rows.
8. **Use bullet points (Word List Bullet style) throughout the document wherever content is list-like**: signal rationale sub-points, positioning recommendation action items, key risks, diligence sub-questions, and any enumerated observations. Reserve prose paragraphs only for flowing narrative (introductions, verdicts, and multi-sentence analytical conclusions).
9. Saves the file to the output path above.

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