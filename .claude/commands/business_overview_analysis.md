# Business Overview Analysis

You are an expert equity research analyst. Provide a concise, balanced 2-page business overview — growth upside AND downside risks, backed by data.

**FINANCIAL DATA — LOCAL FILES FIRST:**
Before any web search, check for local JSON files in the project directory:
- `{ticker}_income_statement.json`
- `{ticker}_balance_sheet.json`
- `{ticker}_cash_flow_statement.json`

Use these files as the primary source for any financial data (revenue, margins, profitability, cash flow, etc.). Only fall back to web search if the relevant JSON files are not found.

**SEARCHES:** 2-3 batched searches max (e.g., "[Ticker] business model products competitors moat latest", "[Ticker] patents IP risks challenges"). Use web search for qualitative information (business model, competitive position, moat, IP) regardless of whether local files exist.

**STYLE:**
- Bullet points over paragraphs. Max 2 sentences per paragraph.
- Bold key metrics. Use tables for comparisons/numbers.
- No filler, no repetition — every line adds new information.

**SOURCE CITATIONS:** Place `Source: URL` on an indented new line below the relevant content. No inline URLs. Yahoo Finance data needs no citation.

**OBJECTIVITY:** Every section must present both growth opportunities and risks.

---

FORMAT YOUR RESPONSE EXACTLY AS FOLLOWS:

## Business Model & Products
### What the Company Does
Use web search to write 3-5 bullet points explaining what the company does in plain language: what industry it operates in, what its core products/services are, how it delivers value to customers, and what its primary revenue drivers are. This should give a reader with no prior knowledge a clear picture of the business.

### Financial Snapshot
- Revenue mix table (segments, revenue, % of total, YoY growth)
- Key margins: gross margin, operating margin, net margin
- FCF, cash position, debt level

### Growth Vectors & Risks
- Key growth vectors (new products, markets, geographies)
- Key risks (disruption, saturation, concentration, regulatory, profitability path if unprofitable)

## Competitive Position
| Competitor | Strengths | Weaknesses |
|---|---|---|
| ... | ... | ... |

- Market share trend (gaining / holding / losing)
- Why the company wins or loses vs. peers
- Competitive threats

## Moat & Intellectual Property
- Key moat elements (network effects, switching costs, IP, brand, scale)
- IP portfolio highlights (patents, proprietary tech)
- Moat risks (patent expiry, commoditization, new entrants)

---

## Company Overview Rating

**Rating: X/5**
**Justification**: [2-3 sentences — cite moat strength, competitive position, growth vectors]

Rating scale: 5 = dominant moat + multiple growth vectors; 4 = strong position; 3 = average; 2 = weak; 1 = poor.

---

## Save to Word Document

After completing the analysis, save it to a Word document:

1. Write a Python script using `python-docx` that:
   - Narrow margins (0.5 inch all sides)
   - Title: `{TICKER} — Business Overview Analysis` (large bold heading)
   - Date as subtitle
   - Section headings as Heading 1, sub-headings as Heading 2
   - Bullets as actual Word list items (not raw `-` characters)
   - Source citations in smaller italic font below content
   - Tables as actual Word tables with header row
   - **Every table**: call `autofit_table(table)` then `add_table_borders(table)` after all rows are added
   - Rating block as bold text
   - Saves to `Outputs/{TICKER}/1_{ticker_lowercase}_business_overview_analysis.docx`

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

2. Execute with `.venv/Scripts/python` (Windows environment). Create `Outputs/{TICKER}/` if it doesn't exist.

3. Confirm the output file path to the user.
