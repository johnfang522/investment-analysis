# Single Name Stock Analysis

You are a top-tier Wall Street equity research analyst producing a complete institutional-grade research note for a single stock.

**ARGUMENTS:** TICKER (e.g., `NVDA`, `AAPL`)

---

## Step 1 — Run All 9 Individual Analyses via Subagents

Spawn each analysis as a **separate subagent** using the Agent tool, one at a time (wait for each to complete before spawning the next). Each subagent receives a self-contained prompt instructing it to read and execute the relevant skill file for {TICKER}.

For each skill, use this prompt template:

> Read the file `.claude/commands/{skill_filename}` and execute all instructions in it for ticker {TICKER}. The working directory is the investment-analysis project root. Use `.venv/Scripts/python` to run any Python scripts.

Execute in this exact order:

1. Subagent → `.claude/commands/business_overview_analysis.md` for {TICKER}
2. Subagent → `.claude/commands/leadership_analysis.md` for {TICKER}
3. Subagent → `.claude/commands/income_statement_analysis.md` for {TICKER}
4. Subagent → `.claude/commands/balance_sheet_analysis.md` for {TICKER}
5. Subagent → `.claude/commands/cash_flow_analysis.md` for {TICKER}
6. Subagent → `.claude/commands/growth_and_profitability_analysis.md` for {TICKER}
7. Subagent → `.claude/commands/business_potential_analysis.md` for {TICKER}
8. Subagent → `.claude/commands/valuation_analysis.md` for {TICKER}
9. Subagent → `.claude/commands/technical_analysis.md` for {TICKER}

Each subagent runs in a fresh context and exits after saving its `.docx` to `Outputs/{TICKER}/`. Do not carry skill output into the orchestrator's context — the orchestrator proceeds to Step 3 once all 9 subagents have completed.

---

## Step 3 — Write the Executive Summary

Synthesize the findings from all 9 analyses into a **2–3 page Wall Street–style equity research note**. Write it as a seasoned senior analyst publishing to institutional clients — direct, opinionated, and anchored to specific data points.

**Writing standards (non-negotiable):**
- Every section must carry a distinct analytical point of view. Avoid generic filler ("the company has a strong balance sheet") — say *why* it matters and *how* it compares to peers or history.
- Lead each section with the single most important insight, not a description of what the section covers.
- Every claim requires a specific number (revenue, margin %, growth rate, multiple, ratio). Vague language like "solid growth" or "attractive valuation" without a number is not acceptable.
- Use Wall Street vernacular where appropriate: "multiple compression risk," "FCF yield," "de-rating," "beat-and-raise cadence," "margin inflection," "consensus estimate," "at current levels."
- Paragraphs should read as tight, confident prose — not bullet dumps. Reserve bullets for comparisons and ranked lists only.
- The tone is professional but not sterile. A sharp institutional note has a point of view; write one.
- Spell out every abbreviation on first use, then use the short form after (e.g., "Free Cash Flow (FCF)" first, then "FCF"; "Year-over-Year (YoY)" first, then "YoY"; "Earnings Per Share (EPS)" first, then "EPS"; "Electronic Manufacturing Services (EMS)" first, then "EMS").

**FORMAT YOUR SUMMARY EXACTLY AS FOLLOWS:**

---

### {TICKER} — Equity Research Note
**[Company Full Name] | [Sector] | [Exchange]: {TICKER}**
*[Coverage label] — [Date]*

Before writing the coverage label, check whether any prior research notes or research package files exist for this ticker in `Outputs/{TICKER}/` (e.g., `*_research_notes_*.docx` or `*_research_package_*.docx`). If prior files exist, use **"Coverage Date: [Date]"**. If this is the first time coverage is being produced, use **"Initiating Coverage — [Date]"**.

Also fetch the current broad market condition at the time of this run. Use `WebSearch` to look up today's S&P 500 level, direction (up/down % on the day), VIX, and one-sentence market context (e.g., risk-on/risk-off, catalyst). Include this as a single italic line immediately below the coverage date line:
*Market on [Date]: S&P 500 [level] ([+/−X.X%]), VIX [X.X] — [one-sentence context]*

---

**RATING: BUY / HOLD / SELL**
**Price Target: $X.XX** *(12-month)*
**Current Price: $X.XX**
**Implied Upside/Downside: +X% / −X%**

---

#### Investment Thesis *(3–5 sentences)*
State the single most important reason to own or avoid this stock. Lead with the dominant theme (e.g., AI infrastructure monopoly, financial fortress, deteriorating moat). Name the key metric that anchors the thesis.

---

#### Business & Competitive Position
- **What the company does** in one sentence.
- **Moat:** What makes it hard to compete with? (network effects, switching costs, IP, scale)
- **Key risk to the moat:** Name the single biggest structural threat.

#### Financial Snapshot

Compute all metric values by calling `compute_metrics("{TICKER}")` from `key_stock_metrics.py` (project root). This function reads `_quick_metrics.json` first for every field, and falls back to the detailed TTM/quarterly/annual JSON files automatically — do not re-derive the formulas inline. Generate the comment label for each metric using `_short_comment(key, val, metrics)` from the same file.

To extract the values, run a short inline Python script:
```python
import sys; sys.path.insert(0, '.')
from key_stock_metrics import compute_metrics, _short_comment, METRICS
m = compute_metrics("{TICKER}")
for metric in METRICS:
    val = m.get(metric["key"])
    comment = _short_comment(metric["key"], val, m)
    print(metric["label"], "|", val, "|", comment)
```

The table has **4 columns only**: Metric, Value, Description (formula + benchmark thresholds), and Comments. Do NOT include a YoY Change column.

For the Comments column: go beyond the mechanical label. Write a one-sentence analyst take that names the actual computed value, compares it to the relevant industry/sector benchmark, and draws a clear conclusion (e.g., "At 42% gross margin, well above the ~25% hardware-sector median, the company demonstrates pricing power and a software-like mix."). For rows 2, 3, 5, 6 (52-wk low/high, market cap, revenue TTM), write a brief contextual note rather than leaving it blank.

| Metric | Value | Description | Comments |
|--------|-------|-------------|----------|
| 1. Current Price | $X.XX | Most recent market price. Benchmark: position within the 52-week range — closer to low implies potential value entry; closer to high implies momentum but compressed margin of safety. | [e.g., "At $X.XX, the stock sits X% above its 52-week low and X% below its high, suggesting mid-range positioning with neither distressed-entry appeal nor extended momentum risk."] |
| 2. 52-Week Low | $X.XX | Lowest closing price over trailing 52 weeks; marks the lower technical support reference for the current trading range. | [e.g., "The $X.XX low was established during [brief context]; serves as a key technical floor and downside reference."] |
| 3. 52-Week High | $X.XX | Highest closing price over trailing 52 weeks; marks the upper resistance level and peak recent investor sentiment. | [e.g., "The $X.XX high reflected peak optimism around [catalyst]; the current X% discount to that level implies sentiment has moderated."] |
| 4. RSI (14-Day) | X.X | Wilder's smoothed 14-day RSI = 100 − [100 / (1 + avg gain / avg loss)]. Benchmark: ≤30 = oversold; 30–70 = neutral; ≥70 = overbought. | [e.g., "RSI of X.X sits in neutral territory, consistent with orderly price action rather than speculative excess or forced selling."] |
| 5. Market Cap | $X.XB | Price x diluted shares outstanding. Determines index eligibility, institutional capacity, and float-driven liquidity profile. | [e.g., "At $X.XB, the company is a [large/mid/small]-cap name with [broad institutional ownership / sufficient float for large institutional positions]."] |
| 6. Revenue (TTM) | $X.XB | Sum of four most recent quarters of total revenue. Establishes absolute scale and operating leverage base relative to sector peers. | [e.g., "TTM revenue of $X.XB places the company [among the top X in its peer set / at scale to absorb fixed-cost leverage], with [growing / stable / declining] top-line trajectory."] |
| 7. Revenue Growth Rate (YoY) | X% | Formula: (Most recent annual revenue − prior year) / prior year. Benchmark: >20% = Strong; 10–20% = Solid; <10% = Slow. Compare to sector peer median for context. | [e.g., "X% YoY revenue growth [outpaces / trails] the peer-group median of ~X%, pointing to [market share gains / cyclical softness / pricing headwinds]."] |
| 8. Gross Margin | X% | Formula: (Revenue − COGS) / Revenue (TTM). Measures pricing power and input cost discipline. Benchmark: >60% = High quality; 40–60% = Decent; <40% = Watch for pricing pressure. | [e.g., "Gross margin of X% [exceeds / is in line with / trails] the sector median of ~X%, reflecting [strong IP monetization / commodity input exposure / product mix shift toward lower-margin lines]."] |
| 9. Operating Margin | X% | Formula: Operating Income / Revenue (TTM). Captures core profitability before financing costs and taxes. Benchmark: >30% = Strong pricing power; 15–30% = Decent; <15% = Watch for cost pressure. | [e.g., "Operating margin of X% [demonstrates / has yet to demonstrate] operating leverage at scale; [elevated R&D/SG&A as a % of revenue / scale benefits compounding] is the primary driver."] |
| 10. Net Income Margin | X% | Formula: Net Income / Revenue (TTM). Bottom-line profitability after all costs, interest, and taxes. Benchmark: >20% = Strong; 10–20% = Decent; <10% = Thin. | [e.g., "Net margin of X% [leads / is roughly in line with / trails] peers; [tax benefits / high interest expense / one-time charges] are distorting the headline figure vs. underlying operating performance."] |
| 11. Return on Equity (ROE) | X% | Formula: Net Income (TTM) / Stockholders' Equity (MRQ). Measures management's efficiency in generating profit from shareholder capital. Benchmark: ≥20% = Ideal; ≥15% = Good; <15% = Below threshold. Note: very high ROE can reflect elevated financial leverage — cross-check D/E. | [e.g., "ROE of X% [comfortably clears / falls short of] the ≥20% ideal threshold; [driven by superior margins / amplified by a leveraged balance sheet — verify sustainability against D/E]."] |
| 12. Debt-to-Equity (D/E) | X.Xx | Formula: Total Debt (MRQ) / Stockholders' Equity (MRQ). Benchmark: <0.5 = Very conservative; 0.5–1.0 = Healthy; 1.0–2.0 = Moderate leverage; >2.0 = High risk. Note: capital-intensive sectors (utilities, telecom, REITs) routinely carry 1–3× as normal. | [e.g., "D/E of X.Xx is [conservative relative to / in line with / elevated vs.] the sector median of ~X×; [the company funds growth organically / leverage is a deliberate capital-efficiency tool / rising debt warrants monitoring against FCF generation]."] |
| 13. Interest Coverage | X.Xx× | Formula: EBIT (TTM) / Interest Expense (TTM); use absolute value of interest expense. Benchmark: >10× = Very safe; 5–10× = Adequate; 3–5× = Watch; <3× = At risk. | [e.g., "Interest coverage of X.Xx× [provides a wide safety margin / clears the minimum threshold / raises solvency concerns]; debt service is [well-covered / manageable / a material risk in a revenue-slowdown scenario]."] |
| 14. Current Ratio | X.Xx | Formula: Current Assets (MRQ) / Current Liabilities (MRQ). Benchmark: >2.0 = Very liquid; 1.5–2.0 = Healthy; 1.0–1.5 = Adequate; <1.0 = Potential liquidity risk. | [e.g., "Current ratio of X.Xx signals [ample / adequate / tight] near-term liquidity; [the above-2.0 reading partly reflects strategic cash reserves / a sub-1.0 ratio is offset by a committed revolving credit facility]."] |
| 15. FCF Margin | X% | Formula: (Operating Cash Flow − CapEx) (TTM) / Revenue (TTM). Benchmark: >20% = High quality; 10–20% = Solid; <10% = Low. FCF margin above net income margin signals high earnings quality. | [e.g., "FCF margin of X% [exceeds / approximates / falls short of] the net income margin of X%, [confirming strong cash conversion / suggesting working capital build or elevated maintenance CapEx is consuming reported earnings]."] |
| 16. Rule of 40 | XX | Formula: Revenue Growth % + Operating Margin %. Benchmark (software/SaaS-primary): >40 = Healthy/investible; 30–40 = Borderline; <30 = Warning zone. Less relevant for mature industrials or capital-intensive businesses. | [e.g., "Rule of 40 score of XX [comfortably clears / narrowly clears / misses] the threshold; [growth / profitability] is carrying the heavier load, and [the balance is improving / deteriorating] as the business matures."] |
| 17a. Trailing P/E | Xx.X | Formula: Current Price / Trailing EPS (last 12 months). Benchmark: <15 = Cheap; 15–25 = Fair; >25 = Expensive. Growth stocks routinely trade >25×; compare to sector median and the stock's own 5-year average. | [e.g., "Trailing P/E of Xx.X [represents a premium to / is in line with / is a discount to] the sector median of ~X×; [the premium is justified by superior growth / a concern given earnings deceleration]."] |
| 17b. Forward P/E | Xx.X | Formula: Current Price / Next-FY consensus EPS estimate. Benchmark: <15 = Cheap; 15–25 = Fair; >25 = Expensive. Forward P/E discounts expected earnings growth; compare to trailing P/E to gauge earnings trajectory. | [e.g., "Forward P/E of Xx.X [implies contraction from / is in line with / implies expansion from] the trailing multiple, signaling the market is pricing in [accelerating / stable / decelerating] earnings."] |
| 17c. PEG Ratio | X.Xx | Formula: Trailing P/E / EPS growth rate (%). Normalizes valuation for growth. Benchmark: <1 = Potentially undervalued; 1–2 = Fair value; >2 = Expensive relative to growth. | [e.g., "PEG of X.Xx [suggests the stock is attractively priced on a growth-adjusted basis / implies fair compensation for growth / indicates the market is pricing in flawless execution with limited margin for error]."] |
| 17d. Price / Sales (TTM) | X.Xx | Formula: Market Cap / Revenue (TTM). Benchmark: <3 = Cheap; 3–6 = Fair; >6 = Expensive. P/S is most informative when margins are thin or earnings are cyclical. | [e.g., "P/S of X.Xx [is elevated relative to / is consistent with / is a discount to] peer comps; [justified by superior margin profile / a concern if revenue growth decelerates and multiple compression follows]."] |
| 18. Dividend Yield | X% or N/A | Formula: Annual dividend per share / Current price. Benchmark: >4% = High yield; 2–4% = Moderate; <2% = Low / growth-oriented; N/A = no dividend paid. | [e.g., "Yield of X% [is competitive with investment-grade bonds and suggests mature capital return discipline / is modest, consistent with a growth-reinvestment posture / is not applicable as the company retains all earnings for reinvestment]."] |
| 19. Dividend Payout Ratio | X% or N/A | Formula: Total dividends paid (TTM) / Net Income (TTM). Benchmark: <50% = Sustainable; 50–75% = Moderate; 75–100% = High; >100% = Unsustainable (paying from reserves or borrowings). | [e.g., "Payout ratio of X% [leaves substantial retained earnings for reinvestment and buybacks / is elevated and may constrain future dividend growth if earnings disappoint / is unsustainable without a recovery in net income]."] |

#### Growth Outlook
- **Revenue 3-Year CAGR:** X% (from growth & profitability analysis)
- **EPS 3-Year CAGR:** X%
- **Forward EPS estimate (next FY):** $X.XX (+X% vs trailing)
- One sentence: is growth accelerating, decelerating, or stable?

#### Valuation
- **Trailing P/E:** Xx | **Forward P/E:** Xx | **PEG:** X.Xx
- **EV/EBITDA:** Xx | **P/S:** Xx
- **Analyst consensus target:** $X.XX (X analysts, X% upside)
- One sentence: is the stock cheap, fairly valued, or expensive relative to growth and peers?

#### Technical Setup
- **Trend:** Up / Neutral / Down | **Price vs 200-DMA:** +X% / −X%
- **RSI (14-day):** X.X | **Buy signal score:** X/5
- One sentence: is now a good technical entry, or should investors wait for a pullback?

#### Balance Sheet & Cash Flow Health
- **Financial health:** Net cash / net debt position and current ratio in one sentence.
- **FCF quality:** Is FCF above or below net income (FCF conversion ratio)?
- **Capital allocation:** Buybacks, dividends, or reinvestment — where is management deploying cash?

#### Business Potential — Next Big Thing (NBT) Readiness

*This section evaluates the company's structural capacity to capitalize on its primary emerging opportunity — its "Next Big Thing" (NBT) — before it becomes the industry standard.*

**Overall NBT Readiness: X/20 (X/5)** — [Readiness rating label: Dominant / Strong / Capable / At Risk / Ill-Positioned]

| Dimension | Score | Key Evidence |
|-----------|-------|--------------|
| Value Alignment (DNA) | X/5 | [One-phrase summary] |
| Operational Agility (Engine) | X/5 | [One-phrase summary] |
| Solvency & Buffer (Oxygen) | X/5 | [One-phrase summary] |
| Ecosystem Power (Gravity) | X/5 | [One-phrase summary] |

- **Primary emerging opportunity:** [Name the specific trend — e.g., AI inference at the edge, robotic surgery expansion, autonomous vehicles]
- **Biggest structural advantage:** [One sentence on the single dimension where the company leads and why it is defensible]
- **NBT Spend Ratio:** X.Xx (Trend Capex / Annual FCF) — [self-funding / manageable / reliant on external capital]
- **Biggest execution risk:** [One sentence on the structural or operational gap most likely to prevent full capture of the opportunity]

#### Key Risks *(3 bullets, specific numbers required)*
- [Risk 1]
- [Risk 2]
- [Risk 3]

#### Rating Justification
**[BUY / HOLD / SELL] with $X.XX price target** — 2–3 sentences. Cite the primary valuation method (DCF bull case / peer multiple / forward P/E) used to set the target, name the single most important upside catalyst, and name the single most important downside risk.

**Rating Scale used:**
- **BUY:** >15% upside to price target; fundamentals improving or undervalued; technical setup supportive
- **HOLD:** Within ±15% of fair value; balanced risk/reward; no clear catalyst near-term
- **SELL:** >15% downside to fair value; deteriorating fundamentals; or overvalued with no margin of safety

---

## Step 4 — Build the Research Note (Word)

Write and execute a Python script (`.venv/Scripts/python`) that creates the summary document from the executive summary above:

1. **Document formatting:**
   - Narrow margins (0.5 inch all sides)
   - Title: `{TICKER} — Equity Research Note` (bold heading, level 0) + date subtitle
   - Company line, coverage label, and date in bold/italic as shown in the summary. Coverage label logic: check `Outputs/{TICKER}/` for any prior `*_research_notes_*.docx` or `*_research_package_*.docx` files — if found, use "Coverage Date: [Date]"; if none, use "Initiating Coverage — [Date]".
   - Broad market condition line in italics immediately below the coverage label, as produced in Step 3 (e.g., *Market on [Date]: S&P 500 [level] ([+/−X.X%]), VIX [X.X] — [one-sentence context]*)
   - Rating line in large bold text (use Heading 1 style, green color `007000`)
   - All sections formatted with Heading 2 subheadings
   - Financial Snapshot table: **4 columns only** (Metric, Value, Description, Comments) — no YoY Change column; dark blue header row (fill `1F3864`), white bold text; populate values and analyst comments by importing `compute_metrics`, `_short_comment`, `METRICS`, and `color_current_price` from `key_stock_metrics` (already on `sys.path` via `sys.path.insert(0, '.')`).
     - **IMPORTANT — key names:** Before writing the generation script, run this diagnostic to discover the exact key names returned by `compute_metrics` for this ticker:
       ```python
       import sys; sys.path.insert(0, '.')
       from key_stock_metrics import compute_metrics
       m = compute_metrics("{TICKER}")
       print(list(m.keys()))
       ```
       Use only the keys that appear in this output. Do NOT invent key names from memory (e.g. do not assume `currentPrice`, `rsi14`, `marketCap` — the actual keys are snake_case such as `current_price`, `rsi`, `market_cap`). Every `m.get(...)` call in the generated script must use a key confirmed by this diagnostic.
     - **Description column**: populate with the formula + benchmark text from the Financial Snapshot table template in Step 3 (hardcode per metric — these are static reference descriptions, not computed values).
     - **Comments column**: populate with the analyst commentary you wrote in Step 3 (the actual one-sentence assessment for this ticker, not the bracketed template text). This is the substantive column — each cell must contain a specific, data-driven sentence, not a placeholder.
     - Apply background color to the **Value cell** (not Comments) using this logic:
       - Use `color_current_price(metrics)` for Current Price — **this function returns an openpyxl `PatternFill` object, not a plain hex string**. Extract the 6-digit hex from it with: `fill = color_current_price(m); hex_color = fill.fgColor.rgb[-6:]` (the `.rgb` attribute is an 8-char string like `'00C6EFCE'`; take the last 6 chars).
       - For all other metrics, use `_short_comment(key, val, metrics)` to get the label, then map: positive keywords (Strong, High quality, Ideal, Good, Very conservative, Very safe, Very liquid, Solid, Healthy, Undervalued, Cheap, High yield, Sustainable) → Green (`C6EFCE`); borderline keywords (Decent, Neutral, Moderate, Adequate, Borderline, Fair) → Yellow (`FFEB9C`); warning keywords (Watch, Slow, Thin, Below threshold, At risk, Liquidity risk, Overbought, Expensive, High risk, Low, Warning, Unsustainable) → Pink (`FFC7CE`); no fill for informational rows (52-Week Low, 52-Week High, Market Cap, Revenue TTM) and N/A values
   - Business Potential NBT Readiness table: dark blue header row (fill `1F3864`), white bold text; color the Overall NBT Readiness line bold; color the score cell green (`007000`) for 4–5, orange (`FF8C00`) for 3, red (`C00000`) for 1–2
   - Bullet points as Word list items

2. **Tables**: initialize with `rows=1` (header only), then `table.add_row()` per data row. **Every table**: call `autofit_table(table)` then `add_table_borders(table)` after all rows are added.

   Import the shared helpers from `doc_utils.py` and metric helpers from `key_stock_metrics.py` (both in the project root):
   ```python
   import sys; sys.path.insert(0, '.')
   from doc_utils import autofit_table, add_table_borders, set_row_font_size, add_footnote
   from key_stock_metrics import compute_metrics, _short_comment, METRICS, color_current_price
   ```

3. **Save to**: `Outputs/{TICKER}/{ticker_lowercase}_research_notes_{YYYYMMDD}.docx`  
   *(use today's date, e.g., `Outputs/NVDA/nvda_research_notes_20260420.docx`)*

4. **Script file location**: Save the script itself to `Outputs/{TICKER}/generate_{ticker_lowercase}_research_notes.py` and run it with `.venv/Scripts/python Outputs/{TICKER}/generate_{ticker_lowercase}_research_notes.py`

5. Call `add_footnote(doc)` immediately before `doc.save(...)` to append the standard AI disclaimer.

6. **Print confirmation**: `Saved: Outputs/{TICKER}/{ticker_lowercase}_research_notes_{YYYYMMDD}.docx`

---

## Step 5 — Assemble the Complete Research Package (Word)

Write and execute a Python script (`.venv/Scripts/python`) that combines all documents into a single master file:

**Source documents** (in this exact order):
1. `Outputs/{TICKER}/{ticker_lowercase}_research_notes_{YYYYMMDD}.docx` — the research note (goes first, no appendix label)
2. `Outputs/{TICKER}/1_{ticker_lowercase}_business_overview_analysis.docx` — Appendix A
3. `Outputs/{TICKER}/2_{ticker_lowercase}_leadership_analysis.docx` — Appendix B
4. `Outputs/{TICKER}/3_{ticker_lowercase}_income_statement_analysis.docx` — Appendix C
5. `Outputs/{TICKER}/4_{ticker_lowercase}_balance_sheet_analysis.docx` — Appendix D
6. `Outputs/{TICKER}/5_{ticker_lowercase}_cash_flow_analysis.docx` — Appendix E
7. `Outputs/{TICKER}/6_{ticker_lowercase}_growth_and_profitability_analysis.docx` — Appendix F
8. `Outputs/{TICKER}/7_{ticker_lowercase}_business_potential_analysis.docx` — Appendix G
9. `Outputs/{TICKER}/8_{ticker_lowercase}_valuation_analysis.docx` — Appendix H
10. `Outputs/{TICKER}/9_{ticker_lowercase}_technical_analysis.docx` — Appendix I

**Merge logic:**

Use `python-docx` to copy elements across documents. Use this helper pattern to append one document's body into another:

```python
from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from copy import deepcopy

def append_doc(target, source_path, appendix_label, appendix_title):
    """Append a page break, appendix heading, then all body elements from source."""
    src = Document(source_path)

    # Register images into target first (deduplication by content hash)
    rId_map = {}
    for rel in src.part.rels.values():
        if "image" in rel.reltype:
            new_rId = _add_image_to_target(target, rel.target_part)
            rId_map[rel.rId] = new_rId

    # Page break before each appendix
    p = OxmlElement('w:p')
    r = OxmlElement('w:r')
    br = OxmlElement('w:br')
    br.set(qn('w:type'), 'page')
    r.append(br)
    p.append(r)
    target.element.body.append(p)

    # Appendix label heading (e.g. "Appendix A — Business Overview Analysis")
    heading = target.add_heading(f"{appendix_label} — {appendix_title}", level=1)
    heading.runs[0].font.color.rgb = RGBColor(0x1F, 0x38, 0x64)

    # Copy body elements, remapping image rIds only within the copied elements
    for elem in src.element.body:
        if elem.tag.endswith('}sectPr'):
            continue
        copied = deepcopy(elem)
        if rId_map:
            for node in copied.iter():
                for attr in list(node.attrib):
                    if node.attrib[attr] in rId_map:
                        node.attrib[attr] = rId_map[node.attrib[attr]]
        target.element.body.append(copied)
```

Copy images: images must be registered into the target package with unique partnames before copying elements, to avoid duplicate zip entries that corrupt the file. Use this approach — images are deduplicated by SHA-1 hash of their bytes, and each unique image gets a unique partname:

```python
import hashlib
from docx.parts.image import ImagePart
from docx.opc.packuri import PackURI

_image_registry = {}   # sha1 -> target ImagePart
_image_counter = [0]

def _add_image_to_target(target_doc, src_img_part):
    blob = src_img_part.blob
    sha1 = hashlib.sha1(blob).hexdigest()
    if sha1 not in _image_registry:
        _image_counter[0] += 1
        ext = src_img_part.partname.ext
        partname = PackURI(f"/word/media/img_merged_{_image_counter[0]}{ext}")
        _image_registry[sha1] = ImagePart(partname, src_img_part.content_type, blob)
    img_part = _image_registry[sha1]
    return target_doc.part.relate_to(img_part,
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/image")
```

Image rId remapping is handled inside `append_doc` — build the rId map from the source before copying, then remap only within the newly-copied elements (not the whole body).

**Script structure:**

```python
import hashlib
from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.shared import RGBColor
from docx.parts.image import ImagePart
from docx.opc.packuri import PackURI
from copy import deepcopy

# ... define append_doc and copy_images helpers above ...

ticker = "{TICKER}"
t = ticker.lower()
date = "{YYYYMMDD}"
base = f"Outputs/{ticker}"

target = Document(f"{base}/{t}_research_notes_{date}.docx")

appendices = [
    ("Appendix A", "Business Overview Analysis",        f"{base}/1_{t}_business_overview_analysis.docx"),
    ("Appendix B", "Leadership Analysis",               f"{base}/2_{t}_leadership_analysis.docx"),
    ("Appendix C", "Income Statement Analysis",         f"{base}/3_{t}_income_statement_analysis.docx"),
    ("Appendix D", "Balance Sheet Analysis",            f"{base}/4_{t}_balance_sheet_analysis.docx"),
    ("Appendix E", "Cash Flow Analysis",                f"{base}/5_{t}_cash_flow_analysis.docx"),
    ("Appendix F", "Growth & Profitability Analysis",   f"{base}/6_{t}_growth_and_profitability_analysis.docx"),
    ("Appendix G", "Business Potential Analysis",       f"{base}/7_{t}_business_potential_analysis.docx"),
    ("Appendix H", "Valuation Analysis",                f"{base}/8_{t}_valuation_analysis.docx"),
    ("Appendix I", "Technical Analysis",                f"{base}/9_{t}_technical_analysis.docx"),
]

for label, title, path in appendices:
    append_doc(target, path, label, title)   # adds page break + heading + body elements (images handled inside)

def add_page_numbers(doc):
    """Add 'Page X of Y' footer to every section in the document."""
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement

    def make_fldChar(fld_char_type):
        fldChar = OxmlElement('w:fldChar')
        fldChar.set(qn('w:fldCharType'), fld_char_type)
        return fldChar

    def make_instrText(text):
        instrText = OxmlElement('w:instrText')
        instrText.set(qn('xml:space'), 'preserve')
        instrText.text = text
        return instrText

    for section in doc.sections:
        section.different_first_page_header_footer = False
        footer = section.footer
        footer.is_linked_to_previous = False
        # Clear existing footer content
        for para in footer.paragraphs:
            para.clear()
        p = footer.paragraphs[0]
        p.alignment = 1  # center
        run = p.add_run()
        run.add_text('Page ')
        # PAGE field
        r1 = OxmlElement('w:r')
        r1.append(make_fldChar('begin'))
        p._p.append(r1)
        r2 = OxmlElement('w:r')
        r2.append(make_instrText(' PAGE '))
        p._p.append(r2)
        r3 = OxmlElement('w:r')
        r3.append(make_fldChar('end'))
        p._p.append(r3)
        run2 = p.add_run(' of ')
        # NUMPAGES field
        r4 = OxmlElement('w:r')
        r4.append(make_fldChar('begin'))
        p._p.append(r4)
        r5 = OxmlElement('w:r')
        r5.append(make_instrText(' NUMPAGES '))
        p._p.append(r5)
        r6 = OxmlElement('w:r')
        r6.append(make_fldChar('end'))
        p._p.append(r6)

add_page_numbers(target)

out_path = f"{base}/{t}_research_package_{date}.docx"
target.save(out_path)
print(f"Saved: {out_path}")
```

**Script file location**: Save the script itself to `Outputs/{TICKER}/assemble_{ticker_lowercase}_research_package.py` and run it with `.venv/Scripts/python Outputs/{TICKER}/assemble_{ticker_lowercase}_research_package.py`

**Save to**: `Outputs/{TICKER}/{ticker_lowercase}_research_package_{YYYYMMDD}.docx`

**Print confirmation**: `Saved: Outputs/{TICKER}/{ticker_lowercase}_research_package_{YYYYMMDD}.docx`
