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

2–4 paragraphs. Given where we are in the cycle, suggest how to weight across layers (e.g., "overweight Infrastructure and Bottlenecks; underweight Applications until revenue models clarify"). Call out any crowding risk,
valuation excess, or consensus positioning to fade. Be specific about which named companies or types look most attractive vs. most risky at this stage. Reference the TAM Expansion Analysis findings where relevant.

---

### 6. Key Diligence Questions

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
2. **Set landscape orientation and narrow page margins** immediately after creating the document:
   ```python
   from docx.shared import Inches
   for section in doc.sections:
       section.orientation = 1  # WD_ORIENT.LANDSCAPE
       section.page_width = Inches(11)
       section.page_height = Inches(8.5)
       section.top_margin = Inches(0.5)
       section.bottom_margin = Inches(0.5)
       section.left_margin = Inches(0.75)
       section.right_margin = Inches(0.75)
   ```
3. Renders all 6 output sections with appropriate headings, paragraphs, tables, and bullet points as specified below. Follow the per-section formatting rules exactly.
4. For all tables, uses `python-docx` table objects. Always initialize tables with `rows=1` (header only), then call `table.add_row()` for each data row. Never pass a pre-sized `rows` count.
5. **Every table must use AutoFit to Contents and have visible borders — applied AFTER all rows are added.** The critical rule: `autofit_table` and `add_table_borders` must be called **after** all data rows have been added to the table, not at creation time. Rows added after these helpers are called will not inherit the settings. Use this pattern for every table without exception:
   ```python
   table = doc.add_table(rows=1, cols=N)
   # ... populate header row ...
   # ... add all data rows with table.add_row() ...
   autofit_table(table)      # call AFTER all rows are added
   add_table_borders(table)  # call AFTER all rows are added
   ```

   **`autofit_table` helper** — sets `tblW`/`tblLayout` to autofit and strips all `w:tcW` fixed-width overrides from every cell:
   ```python
   def autofit_table(table):
       tbl = table._tbl
       tblPr = tbl.find(qn('w:tblPr'))
       if tblPr is None:
           tblPr = OxmlElement('w:tblPr')
           tbl.insert(0, tblPr)
       for tag, attrs in [('w:tblW', {'w:w':'0','w:type':'auto'}), ('w:tblLayout', {'w:type':'autofit'})]:
           el = tblPr.find(qn(tag))
           if el is None:
               el = OxmlElement(tag)
           for k,v in attrs.items(): el.set(qn(k), v)
           if el not in tblPr: tblPr.append(el)
       for row in table.rows:
           for cell in row.cells:
               tcPr = cell._tc.find(qn('w:tcPr'))
               if tcPr is not None:
                   for tcW in tcPr.findall(qn('w:tcW')): tcPr.remove(tcW)
   ```

   **`add_table_borders` helper** — applies a single thin border (`sz=4`, `val="single"`, `color="000000"`) to all four sides of every cell in every row:
   ```python
   def add_table_borders(table):
       for row in table.rows:
           for cell in row.cells:
               tc = cell._tc
               tcPr = tc.find(qn('w:tcPr'))
               if tcPr is None:
                   tcPr = OxmlElement('w:tcPr')
                   tc.insert(0, tcPr)
               tcBorders = tcPr.find(qn('w:tcBorders'))
               if tcBorders is None:
                   tcBorders = OxmlElement('w:tcBorders')
                   tcPr.append(tcBorders)
               for side in ['top', 'left', 'bottom', 'right']:
                   border = OxmlElement(f'w:{side}')
                   border.set(qn('w:val'), 'single')
                   border.set(qn('w:sz'), '4')
                   border.set(qn('w:color'), '000000')
                   tcBorders.append(border)
   ```

6. **All non-header table cell text must use font size 12.** Implement a reusable helper and call it on every data row immediately after `table.add_row()`:
   ```python
   from docx.shared import Pt
   def set_row_font_size(row, size=12):
       for cell in row.cells:
           for para in cell.paragraphs:
               for run in para.runs:
                   run.font.size = Pt(size)
   ```
   Call `set_row_font_size(row)` on every data row (i.e., every row returned by `table.add_row()`). Do **not** call it on the header row.
7. Saves the file to the output path above.

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
- Open with a **Layer Weighting Summary table** (3 columns: Layer | Weight | Rationale), where Weight is one of: Overweight / Neutral / Underweight. Keep Rationale to one short phrase.
- Then write **one bullet per named company or company type** you recommend acting on, formatted as: "**TICKER / Name** — [1-sentence action and reason]". Group bullets under bold sub-labels: **Overweight**, **Neutral**, **Underweight**.
- Close with 1–2 prose paragraphs covering crowding risk, valuation caution, or entry timing nuance.

#### Section 6 — Key Diligence Questions
- Heading 1: "6. Key Diligence Questions"
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