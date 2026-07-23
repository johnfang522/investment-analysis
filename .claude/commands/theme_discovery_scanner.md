---
description: >
  A systematic scanning process for professional investors to *discover* candidate investment themes before they reach market consensus — the step that comes BEFORE theme analysis. Use this skill whenever the user asks how to find trends, wants to know "what's trending", "what themes are emerging", "what should I be watching", "where is smart money going", asks to run a market scan, wants to build or refresh a theme watchlist, or says they don't have a specific theme in mind. Also trigger for questions like "how do I get ahead of the market", "what's pre-consensus right now", or "scan for new opportunities". This skill discovers and ranks candidate themes; once a candidate is promoted, hand off to `/emerging_industry_trend` for full signal scoring and value chain mapping. Always use this skill for theme discovery — do not rely on ad-hoc responses.
---

# Theme Discovery Scanner

A repeatable scanning process that surfaces candidate investment themes *before* they become consensus, maintains a ranked watchlist, and promotes candidates into deep diligence via `/emerging_industry_trend`.

This is the **Stage 2 entry point** in the workflow — the step that runs *before* `/emerging_industry_trend`. Use it when the user has no specific theme in mind and needs the funnel to generate candidates; use `/emerging_industry_trend` once a candidate is chosen and needs full 5-signal scoring + value chain mapping.

**Relationship to other skills in the library:**
- This skill = **discovery** (generate and rank candidate themes)
- `/emerging_industry_trend` = **diligence** (5-signal convergence scoring + 6-layer value chain / bottleneck map of a chosen theme)
- `/industry_trend_analysis` = **value chain mapping** (investable stocks at every layer of a confirmed theme)
- `/multibagger_screener` / `/single_stock_quick_research` = **security selection** within a mapped theme

**House style — buy-side, for the PM.** Write this as a hedge-fund analyst hunting pre-consensus themes for the book — not a trend report. The deliverable is actionable: a ranked watchlist with explicit **promotion calls** and a directional **scan posture** (how much of the watchlist is act-ready vs. watch-only). The entire edge here is being early; lead with what is *not* yet
consensus and say so plainly. If the scan surfaces nothing genuinely pre-consensus, say that too — a manufactured candidate is a bias, not an edge.

---

## Instructions

The user has invoked `/theme_discovery_scanner` with the following argument: `$ARGUMENTS`

### Argument resolution — do this before anything else

- **Empty argument (the common case):** Run a full ad-hoc five-channel live scan and present the ranked watchlist. This is the default behavior.
- **A channel name or focus hint** (e.g., "capital flows", "cost curves", "science"): Emphasize that channel but still run all five for convergence context.
- **A sector/domain hint** (e.g., "energy", "biotech", "defense"): Scope the scan to that domain across all five channels.

In all cases, **always begin with Step 0 live web research** before ranking — trends move faster than any knowledge cutoff.

---

## Step 0 — Always Search First

Use `WebSearch` aggressively across all five channels. Search **recent (last 1–3 months)** sources: VC deal roundups, funding trend reports, conference coverage, earnings-call commentary, lobbying/regulatory news, and cost-curve data.

**Prefer primary and trade sources over mainstream media** — mainstream coverage of a theme is a *late* signal, not a discovery signal.

Run several of these in parallel:
- `venture capital funding roundup [current quarter] [current year]`
- `[sector] startup funding cluster [current year]`
- `notable engineers executives leaving [big company] founding startup [current year]`
- `earnings call new competitive threat [current year]`
- `lobbying spend spike [sector] [current year]`
- `[input] cost per unit decline [current year]` (e.g., compute cost per token, battery $/kWh, launch $/kg, sequencing $/genome)

---

## Part 1 — The Five Scanning Channels

Run all five channels each scan. Each channel maps to one of the five convergence signals used in `/emerging_industry_trend`, so a candidate appearing in multiple channels is already showing early convergence.

### Channel 1: Follow the Capital (→ Capital Flow signal)
- Scan VC deal roundups (PitchBook / Crunchbase / trade reports) for **clustering**: 3+ quality funds hitting the same *narrow* sub-sector within a quarter.
- Ignore what is biggest (already consensus). Look for what is *newly repeating* — a sub-sector name that appears in deal flow this quarter but not two quarters ago.
- Weight **concentration over volume**: one top-quartile fund making repeated bets in a niche outweighs broad diffuse activity.
- Also flag: strategic M&A by incumbents, corporate VC arms entering a space, sovereign wealth fund participation, government co-investment (a geopolitical/strategic tell).
- Reminder: smart private capital leads public-market recognition by **12–36 months** — this channel defines the discovery window.

### Channel 2: Follow the Talent (→ Narrative Momentum, leading edge)
- Track where senior engineers, scientists, and executives from top companies are moving *to*. Talent migrates **1–2 years before revenue**.
- Watch: new startup founding announcements by notable operators, lab poaching patterns, senior-hire flows into a sector.
- A cluster of respected people leaving stable positions for the same unproven space is one of the strongest early signals that exists.

### Channel 3: Follow the Incumbents' Fear (→ Regulatory + Behavioral signals)
- Read large-cap earnings-call transcripts: what *new* competitive threat or opportunity has management started naming this quarter that they didn't a year ago? Track mention frequency across companies.
- Watch lobbying disclosures: a sudden spike in industry lobbying spend against (or for) something means incumbents believe it is real.
- Watch rulemaking calendars (FDA, FCC, EU, DOE, etc.) for doors opening or closing.

### Channel 4: Follow the Science (→ Technology Inflection, leading edge)
- Skim flagship conference agendas year-over-year (NeurIPS, RSS, JPM Healthcare, CERAWeek, DAC, ASCO, etc.). When a topic jumps from breakout session to keynote, that is a measurable inflection.
- Track preprint/citation momentum: which topics show accelerating paper counts and citation velocity?
- Note startup founding-date clustering around a specific enabling result.

### Channel 5: Follow the Cost Curves (→ Technology Inflection, hard data)
- Maintain a standing shortlist of key input costs and flag any that break trend (non-linear improvement). Examples: compute cost per token, battery $/kWh, launch $/kg, sequencing $/genome, electrolyzer $/kW, actuator cost, bandwidth $/Gbps.
- A ~10× cost improvement in an input almost always spawns a theme within 1–3 years. Ask: **what becomes newly possible or newly economical?**

---

## Part 2 — Candidate Qualification Filter

Before a scan finding becomes a watchlist candidate, it must pass **all three** filters:

1. **Specificity** — A nameable sub-sector or capability, not a broad category. "AI" fails; "on-prem inference infrastructure for regulated enterprises" passes.
2. **Pre-consensus** — It must NOT already dominate mainstream financial media or absorb the largest share of capital in its category. If it is the headline trade, it belongs in crowding analysis, not discovery.
3. **Public-market path** — There must be a plausible route to investable public equities within 1–3 years (existing listed players in the value chain, credible IPO pipeline, or listed adjacent beneficiaries).

---

## Part 3 — Watchlist Management

Maintain a ranked watchlist of **5–10 candidate themes**. For each, track:

| Field | Content |
|---|---|
| Theme name | Specific, nameable sub-sector |
| Channels detected | Which of the 5 scanning channels surfaced it (list) |
| First detected | Date first added to watchlist |
| Momentum | Rising / flat / fading since last scan |
| Early signal count | How many of the 5 convergence signals show at least partial evidence |
| Public-market path | Named tickers or company types already investable |
| One-line risk | The single most likely reason this fizzles |

**Ranking rule:** Rank by (a) number of independent channels detecting it, then (b) momentum, then (c) quality of public-market path.

**Lifecycle rules:**
- **Add** when a finding passes all three qualification filters.
- **Promote** to deep diligence when 2+ convergence signals show clear evidence → hand off to `/emerging_industry_trend` for full 5-signal scoring and 6-layer value chain / bottleneck mapping.
- **Demote/remove** when momentum fades for two consecutive scans, or when the theme crosses into consensus (mainstream saturation, extreme capital concentration) without the user holding a position — at that point it is a crowding question, not a discovery question.

---

## Part 4 — Scan Cadence

- **Monthly:** Full five-channel scan; refresh watchlist ranks; check promote/demote triggers.
- **Quarterly:** Earnings-transcript sweep (Channel 3) and cost-curve checkpoint (Channel 5) in depth.
- **Ad hoc:** Any time the user asks "what's emerging right now", run a compressed live scan (Channels 1, 2, and 4 via web search) and present the updated watchlist.

---

## Output Format

Always produce all sections below in order. Use **tables** and **bullet points** throughout — no dense prose paragraphs.

### 0. Scan Posture (lead with the call)

Open with the buy-side "so what": a bold **Scan Posture** line stating how act-ready the current watchlist is — e.g., *"Act-ready: 1 promotion call (data-center power delivery). Watch: 4. No investable pre-consensus theme in biotech this scan."* Follow with a one-line **The edge:** naming what is genuinely pre-consensus right now and why the market hasn't caught it. Keep it to 3–4 sentences of prose, no bullets.

### 1. Scan Summary (by channel)

For each of the five channels: what was searched, the 2–4 most notable findings, and which findings passed the qualification filter (with a one-line reason for any rejects worth mentioning). Present as a table:

| Channel | What Was Searched | Notable Findings | Passed Filter? |
|---|---|---|---|
| 1. Capital | … | … | Candidate: [theme] / Reject: [reason] |
| 2. Talent | … | … | … |
| 3. Incumbents' Fear | … | … | … |
| 4. Science | … | … | … |
| 5. Cost Curves | … | … | … |

### 2. Ranked Watchlist

Present as a table using the Part 3 structure, all current candidates ranked. Bold any candidate whose rank changed or that is newly added.

| Rank | Theme | Channels Detected | Momentum | Early Signal Count | Public-Market Path | One-Line Risk |
|---|---|---|---|---|---|---|
| 1 | … | … | Rising / Flat / Fading | X / 5 | … | … |

### 3. Promotion Calls

Explicitly state which candidates (if any) now meet the **2+ signal** promotion threshold, and offer to run `/emerging_industry_trend` on them. If none qualify, say so plainly.

### 4. Variant View — Consensus vs. Our Read

**Mandatory.** A small 3-column table contrasting the current consensus trade with our pre-consensus read, followed by a one-line **The edge:** bullet.

| Debate | Consensus / What's Priced | Our Read |
|---|---|---|
| What is the headline trade right now? | [consensus theme] | [why it's late / crowded] |
| What is genuinely pre-consensus? | [what the market ignores] | [our earlier read + evidence] |

**The edge:** one line naming what the market is mispricing and why we think we are right. **If the scan confirms the consensus is correctly positioned and nothing is genuinely early, say so — a forced variant view is a bias, not an edge.**

---

## Document Output

After producing the full analysis in chat, save it as a Word document using `python-docx`.

- **Output path:** `Outputs/theme_discovery_scan_{yyyymmdd}.docx` (this is a cross-theme, non-ticker skill → save to the `Outputs/` root, not a ticker subfolder). Replace `{yyyymmdd}` with today's date in YYYYMMDD format.

Write and execute a Python script using `.venv/Scripts/python` that:

1. Creates the document with a title heading "Theme Discovery Scan — [Month YYYY]".
2. **Set portrait orientation and narrow page margins** immediately after creating the document:
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
3. Renders all output sections (Scan Posture, Scan Summary, Ranked Watchlist, Promotion Calls, Variant View) with appropriate headings, paragraphs, tables, and bullet points.
4. For all tables, uses `python-docx` table objects. **Always initialize tables with `rows=1` (header only), then call `table.add_row()` for each data row.** Never pass a pre-sized `rows` count.
5. **Every table must call `autofit_table(table)` then `add_table_borders(table)` AFTER all rows are added:**
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
   from doc_utils import autofit_table, add_table_borders, set_row_font_size, add_footnote, fmt_value
   ```
   Use `fmt_value(v)` for any dollar amounts in table cells (auto-scales: ≥$1B → `$X.XXB`, ≥$1M → `$X.XM`, ≥$1K → `$X.XK`). Never hardcode `/ 1e9` or manually append `"B"`.
6. **All non-header table cell text must use font size 12.** Call `set_row_font_size(row)` on every data row immediately after `table.add_row()` — never on the header row.
7. **Apostrophe pitfall:** when writing string literals containing apostrophes (e.g. `"Incumbents' Fear"`), use double-quoted Python strings — never single-quoted — to avoid `SyntaxError: unterminated string literal`.
8. Ends with a **Sources** section listing all URLs cited during the analysis as bullet points (title + URL).
9. Calls `add_footnote(doc)` immediately before `doc.save(...)` to append the standard AI disclaimer.
10. Saves the file to the output path above and prints the path.

Keep the in-chat response to a concise summary of the top-ranked candidates and any promotion calls, then link the saved document.

---

## Final Step — Offer next step

After delivering the full output, ask the user:

> "Would you like to promote one of these candidates and kick off `/emerging_industry_trend` for full signal scoring and value chain / bottleneck mapping?"

If the user says yes, ask which theme they want to go deeper on (if more than one qualifies), then invoke `/emerging_industry_trend` with that theme as the argument.

---

## Example Application (abbreviated)

**Ad hoc scan, mid-2026 context:**

- Channel 1 finding: Vertical AI deals clustering in law, finance, construction, biotech; fusion/geothermal drawing largest single-day deals; defense-industrial seed rounds with a Pentagon path. Consensus check: frontier-lab mega-rounds (~3/4 of Q1 venture dollars) = consensus, excluded from discovery.
- Channel 3 finding: Utilities and grid operators newly discussing data-center interconnection queues on earnings calls → "data-center power delivery" candidate.
- Channel 5 finding: If actuator and force-sensor costs continue breaking trend → supports the existing "physical AI" watchlist candidate.

**Resulting watchlist top 3 (illustrative):** data-center power delivery (3 channels), vertical AI in regulated industries (2 channels), defense-industrial new entrants (2 channels). Promotion call: data-center power delivery meets the 2+ signal threshold → hand off to `/emerging_industry_trend`.

---

## Common Mistakes to Avoid

- **Acting on mainstream coverage.** By the time CNBC runs a segment on a theme, the discovery window has usually closed. Mainstream coverage is a demote trigger, not an add trigger.
- **Confusing broad category with nameable sub-sector.** "AI" or "energy" fails the specificity filter. Force the candidate down to a specific bottleneck or capability.
- **Volume over concentration in Channel 1.** Fifty funds making one bet each is noise; one top-quartile fund making ten bets in a niche is signal.
- **Manufacturing a candidate to fill the watchlist.** If nothing passes all three filters this scan, report a shorter list. A forced candidate wastes diligence.
- **Skipping the anti-consensus check.** Always name the current consensus trade for context, then confirm watchlist candidates are genuinely earlier than it.
