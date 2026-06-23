---
description: >
  A structured framework for deep-diving the internal mechanics of an industry — competitive dynamics, Porter's Five Forces, business models, margin structure, barriers to entry, and key players. Use this skill whenever the user asks how an industry works, wants to understand competitive dynamics, asks about margin structure or business models in a sector, or wants an industry primer before doing stock-level research. Also trigger for questions like "how does the X industry make money", "who are the key players in Y", "what are the barriers to entry in Z", "how competitive is this space", "what's the margin profile of this industry", or "give me an industry overview for [sector]". Accept either a theme/sector name or a stock ticker as input — if a ticker is given, derive the industry from it first.
---

# Industry Deep Dive Framework

A structural analysis of how an industry actually works — its competitive mechanics, business model economics, key players, and moat sources. Designed as an industry primer that complements `/emerging_industry_trend` (bottleneck hunting) and `/industry_trend_analysis` (value chain stock mapping).

**House style — buy-side, for the PM.** Write this as a hedge-fund analyst, not a textbook. Every structural finding must ladder up to "so what for the book" — is this industry structurally attractive to be long or to short, where do the economics concentrate, and which incumbents hold the moat. End with a directional **industry posture** (conviction + how to express) and a mandatory **variant view** on where consensus is wrong about the industry's structure.

---

## Instructions

The user has invoked `/industry_deep_dive` with the following argument: `$ARGUMENTS`

**If `$ARGUMENTS` is a stock ticker** (all-caps, 1–5 letters, e.g. `NVDA`, `AAPL`):
- Use `WebSearch` to identify the ticker's primary industry/sector before proceeding.
- Set `{theme}` to the derived industry name (e.g., `gpu_compute`, `cloud_infrastructure`) for the output filename.

**If `$ARGUMENTS` is a theme or sector name:**
- Treat it directly as the industry to analyze.
- Set `{theme}` to the argument lowercased, spaces replaced with underscores.

**If `$ARGUMENTS` is empty:**
- Ask the user which industry or ticker they want to deep-dive.

In all cases, **always begin with Step 0 web research** before writing any analysis.

---

## Step 0 — Always Search First

Before applying the framework, use `WebSearch` to pull current, grounded data.
Do not rely on training data alone — industry dynamics, margins, and competitive positions shift.

**Run 4–6 of these queries in parallel:**
- `[industry] competitive landscape key players market share [current year]`
- `[industry] gross margin operating margin benchmarks [current year]`
- `[industry] barriers to entry moat analysis`
- `[industry] Porter's Five Forces analysis`
- `[industry] business model revenue model how companies make money`
- `[industry] recent M&A consolidation [current year]`
- `[industry] growth drivers headwinds outlook [current year]`

Look for: analyst reports, industry association data, earnings call transcripts naming competitive dynamics, margin disclosures, and any recent structural shifts.

---

## Section 0 — Industry Summary

Write a concise **3–5 sentence prose overview** of the industry before any deep-dive analysis. Cover:
- What the industry does and its current market size
- The core value it delivers and to whom
- Why it is strategically relevant or interesting right now

This section sets context for everything that follows. Keep it punchy — no bullet points, just clear prose.

---

## Section 1 — Industry Structure: Porter's Five Forces

Score each force and provide grounded evidence.

| Force | Intensity | Key Evidence |
|---|---|---|
| Threat of New Entrants | High / Medium / Low | One-line rationale with specific data or examples |
| Bargaining Power of Suppliers | High / Medium / Low | … |
| Bargaining Power of Buyers | High / Medium / Low | … |
| Threat of Substitutes | High / Medium / Low | … |
| Competitive Rivalry | High / Medium / Low | … |

Follow the table with a single bold bullet: **Overall structural attractiveness:** one sentence verdict (e.g., "High rivalry + strong buyer power compress margins structurally; supplier power is the key lever for incumbents").

---

## Section 2 — Business Model & Economics

Cover in bullet-point form under the following sub-headings:

**Revenue Model**
- How companies in this industry charge customers (subscription, transaction, license, hardware, services, etc.)
- Pricing dynamics — who sets price, and what drives pricing power

**Margin Profile**
- Typical gross margin range and what drives it
- Typical operating margin range and key cost drivers (COGS, R&D, S&M, G&A)
- Where operating leverage or compression comes from

**Capital Intensity**
- Capex vs. opex profile — is this asset-heavy or asset-light?
- Working capital dynamics (inventory, receivables, deferred revenue)
- Typical return on invested capital (ROIC) range for leaders vs. laggards

---

## Section 3 — Competitive Landscape

Present as a table:

| Company | Public/Private | Market Position | Key Differentiation | Strengths | Weaknesses |
|---|---|---|---|---|---|
| … | … | Leader / Challenger / Niche | … | … | … |

Follow the table with bullet points:
- **Share dynamics:** Who is gaining share and why; who is under pressure
- **Recent M&A:** Notable deals in the last 2–3 years and what they signal about industry consolidation
- **Disruption watch:** Any emerging competitor or technology threatening incumbents

---

## Section 4 — Key Industry Dynamics

**Growth Drivers** (3–5 bullet points):
- Specific, evidence-backed drivers with data where available

**Headwinds & Risks** (3–5 bullet points):
- Structural, regulatory, cyclical, or competitive risks

**Secular Trends** (2–3 bullet points):
- Long-duration shifts reshaping the industry over the next 5–10 years

---

## Section 5 — Barriers to Entry & Moat Sources

Present as a table:

| Barrier Type | Strength (High/Med/Low) | Examples / Evidence |
|---|---|---|
| Intellectual property / patents | … | … |
| Regulatory licenses / approvals | … | … |
| Network effects | … | … |
| Switching costs | … | … |
| Scale / cost advantages | … | … |
| Geographic / physical constraints | … | … |
| Brand / trust | … | … |

Follow the table with a single bold bullet: **Primary moat source:** identify the 1–2 barriers that matter most and which incumbents hold them.

---

## Section 6 — Variant View & Industry Posture

**Variant View — Consensus vs. Our Read** (table):

| Debate | Consensus View | Our Read |
|---|---|---|
| [The structural debate that matters most — e.g., is rivalry permanently compressing margins?] | [what the Street/consensus believes] | [our differentiated read + evidence] |
| [Second debate — e.g., is the moat durable or eroding?] | [consensus] | [our read] |

Then a bold **Industry Posture** verdict:
- **Structural attractiveness:** Attractive / Mixed / Unattractive — **Conviction X/10**
- **How to express it:** one line — e.g., "long the bottleneck/moat holders, short the commoditized integrators," or "avoid until rivalry resolves"
- **The edge:** one sentence — what the market misunderstands about this industry's structure and why we think we're right

---

## Output Format

Produce all sections in chat first (Summary through Variant View & Posture + Sources). Use **tables** and **bullet points** throughout — no dense prose paragraphs except Section 0.

Then save as a Word document.

---

## Document Output

After producing the full analysis in chat, save it as a Word document using `python-docx`.

- **Output path:** `Outputs/industry_deep_dive_{theme}_{yyyymmdd}.docx`
  - Replace `{theme}` with the industry name lowercased, spaces replaced with underscores (e.g., `gpu_compute`, `optical_interconnect`).
  - Replace `{yyyymmdd}` with today's date in YYYYMMDD format.

Write and execute a Python script (save it to `Outputs/generate_industry_deep_dive_{theme}.py`) using `.venv/Scripts/python` that:

1. Creates the document with a title heading matching the industry name.
2. **Sets portrait orientation and narrow page margins** immediately after `Document()`:
   ```python
   from docx.shared import Inches
   for section in doc.sections:
       section.orientation = 0  # WD_ORIENT.PORTRAIT
       section.page_width = Inches(8.5)
       section.page_height = Inches(11)
       section.top_margin = Inches(0.5)
       section.bottom_margin = Inches(0.5)
       section.left_margin = Inches(0.75)
       section.right_margin = Inches(0.75)
   ```
3. Imports the shared helpers from `doc_utils.py`:
   ```python
   import sys; sys.path.insert(0, '.')
   from doc_utils import autofit_table, add_table_borders, set_row_font_size, add_footnote, fmt_value
```
Use `fmt_value(v)` for all dollar amounts in table cells (auto-scales: ≥$1B → `$X.XXB`, ≥$1M → `$X.XM`, ≥$1K → `$X.XK`). Never hardcode `/ 1e9` or manually append `"B"`.
   ```
4. Renders all sections with appropriate headings, paragraphs, tables, and bullet points.
5. For all tables:
   - Always initialize with `rows=1` (header only), then `table.add_row()` per data row.
   - Call `autofit_table(table)` then `add_table_borders(table)` AFTER all rows are added.
   - Call `set_row_font_size(row, size=11)` on every non-header data row immediately after `table.add_row()`.
6. Applies color fills to the Porter's Five Forces table rows using `w:shd`:
   - Threat of New Entrants: `D6E4F0` (light blue)
   - Bargaining Power of Suppliers: `D5E8D4` (light green)
   - Bargaining Power of Buyers: `FFF2CC` (light yellow)
   - Threat of Substitutes: `FCE4D6` (light orange)
   - Competitive Rivalry: `F4CCCC` (light red/pink)
7. Renders **Section 6 — Variant View & Industry Posture**: the 3-column Variant View table (dark-blue header row), then the bold Industry Posture verdict (color the attractiveness label green `007000` for Attractive, neutral for Mixed, red `C00000` for Unattractive).
8. Ends with a **Sources** section (Heading 1) listing all URLs cited as bullet points.
9. Calls `add_footnote(doc)` immediately before `doc.save(...)` to append the standard AI disclaimer.
9. Saves the file to the output path and prints the path.

---

### Per-Section Formatting Rules

#### Section 0 — Industry Summary
- Heading 1: "Industry Summary"
- One paragraph (3–5 sentences): industry definition, market size, current relevance.
- No tables or bullet points in this section.

#### Section 1 — Porter's Five Forces
- Heading 1: "1. Industry Structure: Porter's Five Forces"
- One table: Force | Intensity | Key Evidence (3 columns). Color-fill each data row (colors above). Do not color the header row.
- After the table, one bold bullet: "Overall structural attractiveness:" with a one-sentence verdict.

#### Section 2 — Business Model & Economics
- Heading 1: "2. Business Model & Economics"
- Three sub-headings (Heading 2): "Revenue Model", "Margin Profile", "Capital Intensity"
- Each sub-heading followed by bullet points (Word List Bullet style).

#### Section 3 — Competitive Landscape
- Heading 1: "3. Competitive Landscape"
- One table: Company | Public/Private | Market Position | Key Differentiation | Strengths | Weaknesses (6 columns).
- After the table, three bold bullet points: share dynamics, recent M&A, disruption watch.

#### Section 4 — Key Industry Dynamics
- Heading 1: "4. Key Industry Dynamics"
- Three sub-headings (Heading 2): "Growth Drivers", "Headwinds & Risks", "Secular Trends"
- Each sub-heading followed by bullet points (Word List Bullet style).

#### Section 5 — Barriers to Entry & Moat Sources
- Heading 1: "5. Barriers to Entry & Moat Sources"
- One table: Barrier Type | Strength | Examples / Evidence (3 columns).
- After the table, one bold bullet: "Primary moat source:" with the 1–2 dominant barriers and which incumbents hold them.

#### Section 6 — Variant View & Industry Posture
- Heading 1: "6. Variant View & Industry Posture"
- One table: Debate | Consensus View | Our Read (3 columns), dark-blue header row.
- After the table, the bold **Industry Posture** verdict: structural attractiveness label + Conviction X/10, a "How to express it" line, and a bold "The edge:" bullet.

#### Section 7 — Sources
- Heading 1: "7. Sources"
- Bullet list of all URLs cited during the analysis (title + URL).
