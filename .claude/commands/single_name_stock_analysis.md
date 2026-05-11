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

Synthesize the findings from all 9 analyses into a **2–3 page Wall Street–style equity research note**. Write it as if publishing to institutional clients. Be direct, lead with the recommendation, and back every claim with a specific number.

**FORMAT YOUR SUMMARY EXACTLY AS FOLLOWS:**

---

### {TICKER} — Equity Research Note
**[Company Full Name] | [Sector] | [Exchange]: {TICKER}**
*Initiating Coverage / Updating Coverage — [Date]*

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

| Metric | Value | YoY Change |
|--------|-------|------------|
| Revenue (Annual) | $X.XB | +X% |
| Gross Margin | X% | +Xpp |
| Operating Margin | X% | +Xpp |
| Net Income (Annual) | $X.XB | +X% |
| EPS (Trailing) | $X.XX | +X% |
| Free Cash Flow (Annual) | $X.XB | +X% |
| Net Cash / (Net Debt) | $X.XB | — |
| Return on Equity | X% | — |
| Current Ratio | X.Xx | — |

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

#### Business Potential — NBT Readiness

*This section evaluates the company's structural capacity to capitalize on its primary emerging opportunity before it becomes the industry standard.*

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
   - Company line and date in bold/italic as shown in the summary
   - Rating line in large bold text (use Heading 1 style, green color `007000`)
   - All sections formatted with Heading 2 subheadings
   - Financial Snapshot table: dark blue header row (fill `1F3864`), white bold text
   - Business Potential NBT Readiness table: dark blue header row (fill `1F3864`), white bold text; color the Overall NBT Readiness line bold; color the score cell green (`007000`) for 4–5, orange (`FF8C00`) for 3, red (`C00000`) for 1–2
   - Bullet points as Word list items

2. **Tables**: initialize with `rows=1` (header only), then `table.add_row()` per data row. **Every table**: call `autofit_table(table)` then `add_table_borders(table)` after all rows are added.

   Define these helpers in the script:
   ```python
   def autofit_table(table):
       from docx.oxml.ns import qn
       from docx.oxml import OxmlElement
       tbl = table._tbl
       tblPr = tbl.find(qn('w:tblPr')) or tbl.insert(0, OxmlElement('w:tblPr'))
       for tag, attrs in [('w:tblW', {'w:w':'0','w:type':'auto'}), ('w:tblLayout', {'w:type':'autofit'})]:
           el = tblPr.find(qn(tag)) or OxmlElement(tag)
           for k, v in attrs.items(): el.set(qn(k), v)
           if el not in list(tblPr): tblPr.append(el)
       for row in table.rows:
           for cell in row.cells:
               tc = cell._tc
               tcPr = tc.find(qn('w:tcPr'))
               if tcPr is not None:
                   for tcW in tcPr.findall(qn('w:tcW')): tcPr.remove(tcW)

   def add_table_borders(table):
       from docx.oxml.ns import qn
       from docx.oxml import OxmlElement
       for row in table.rows:
           for cell in row.cells:
               tc = cell._tc
               tcPr = tc.find(qn('w:tcPr'))
               if tcPr is None:
                   tcPr = OxmlElement('w:tcPr'); tc.insert(0, tcPr)
               tcBorders = tcPr.find(qn('w:tcBorders'))
               if tcBorders is None:
                   tcBorders = OxmlElement('w:tcBorders'); tcPr.append(tcBorders)
               for side in ('top','left','bottom','right','insideH','insideV'):
                   border = OxmlElement(f'w:{side}')
                   border.set(qn('w:val'), 'single')
                   border.set(qn('w:sz'), '4')
                   border.set(qn('w:color'), '000000')
                   tcBorders.append(border)
   ```

3. **Save to**: `Outputs/{TICKER}/{ticker_lowercase}_research_notes_{YYYYMMDD}.docx`  
   *(use today's date, e.g., `Outputs/NVDA/nvda_research_notes_20260420.docx`)*

4. **Print confirmation**: `Saved: Outputs/{TICKER}/{ticker_lowercase}_research_notes_{YYYYMMDD}.docx`

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
import copy

def append_doc(target, source_path, appendix_label, appendix_title):
    """Append a page break, appendix heading, then all body elements from source."""
    src = Document(source_path)

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

    # Copy all body-level XML elements from source (skip the last sectPr)
    for elem in src.element.body:
        if elem.tag.endswith('}sectPr'):
            continue
        target.element.body.append(deepcopy(elem))
```

Copy images: images embedded in the source document must be carried over. To handle this, after copying elements, copy all image parts from the source document's package into the target package using the relationship map:

```python
from docx.opc.constants import RELATIONSHIP_TYPE as RT

def copy_images(target_doc, source_doc):
    """Copy image blobs from source into target and re-map rId references in copied XML."""
    for rel in source_doc.part.rels.values():
        if "image" in rel.reltype:
            img_part = rel.target_part
            new_rId = target_doc.part.relate_to(img_part, rel.reltype)
            # Remap rId in the copied XML elements
            for elem in target_doc.element.body.iter():
                for attr in list(elem.attrib):
                    if elem.attrib[attr] == rel.rId:
                        elem.attrib[attr] = new_rId
```

Call `copy_images(target, src)` immediately after copying each source document's elements, before moving to the next source.

**Script structure:**

```python
from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.shared import RGBColor
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
    src = Document(path)
    append_doc(target, path, label, title)   # adds page break + heading + body elements
    copy_images(target, src)                 # re-maps image relationships

out_path = f"{base}/{t}_deep_research_{date}.docx"
target.save(out_path)
print(f"Saved: {out_path}")
```

**Save to**: `Outputs/{TICKER}/{ticker_lowercase}_deep_research_{YYYYMMDD}.docx`

**Print confirmation**: `Saved: Outputs/{TICKER}/{ticker_lowercase}_deep_research_{YYYYMMDD}.docx`
