"""
Shared python-docx helpers used by all skill-generated Word document scripts.

Scripts are saved to Outputs/{TICKER}/ and run from the project root, so they
must add '.' to sys.path before importing:

    import sys; sys.path.insert(0, '.')
    from doc_utils import setup_document, autofit_table, add_table_borders, set_row_font_size

House format (applied by setup_document() and re-enforced by add_footnote()):
landscape Letter, narrow 0.5" margins, Arial throughout, 10pt for all text
except headings (Title / Heading N styles keep their larger sizes).
"""

from docx.enum.section import WD_ORIENT
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.shared import Inches, Pt, RGBColor

FONT_NAME = "Arial"
BODY_PT = 10
HEADING_MIN_PT = 14          # explicit run sizes at or above this are treated as headings
CHART_WIDTH = Inches(9.5)    # full text width on landscape Letter with 0.5" margins


def _set_rfonts(rPr, name=FONT_NAME):
    """Point every script slot of a w:rPr at `name`, dropping theme-font overrides."""
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts')
        rPr.insert(0, rFonts)
    for attr in ('w:asciiTheme', 'w:hAnsiTheme', 'w:eastAsiaTheme', 'w:cstheme'):
        rFonts.attrib.pop(qn(attr), None)
    for attr in ('w:ascii', 'w:hAnsi', 'w:eastAsia', 'w:cs'):
        rFonts.set(qn(attr), name)


def _is_heading(paragraph):
    name = paragraph.style.name if paragraph.style is not None else ''
    return name == 'Title' or name.startswith('Heading')


def _iter_paragraphs(container):
    """Yield every paragraph in a document/cell/header, descending into (nested) tables."""
    for p in container.paragraphs:
        yield p
    for table in getattr(container, 'tables', []):
        for row in table.rows:
            for cell in row.cells:
                yield from _iter_paragraphs(cell)


def setup_document(doc):
    """
    Apply the house page layout and fonts. Call immediately after `doc = Document()`:
    landscape Letter (11" x 8.5"), narrow 0.5" margins on all sides, Arial everywhere,
    10pt body text. Heading/Title styles keep their sizes but switch to Arial.
    """
    for section in doc.sections:
        section.orientation = WD_ORIENT.LANDSCAPE
        section.page_width = Inches(11)
        section.page_height = Inches(8.5)
        for side in ('top_margin', 'bottom_margin', 'left_margin', 'right_margin'):
            setattr(section, side, Inches(0.5))

    # Document-wide defaults (covers table styles and anything without an explicit style font)
    rPrDefault = doc.styles.element.find(qn('w:docDefaults'))
    if rPrDefault is not None:
        rPr = rPrDefault.find(qn('w:rPrDefault') + '/' + qn('w:rPr'))
        if rPr is not None:
            _set_rfonts(rPr)
            sz = rPr.find(qn('w:sz'))
            if sz is None:
                sz = OxmlElement('w:sz')
                rPr.append(sz)
            sz.set(qn('w:val'), str(BODY_PT * 2))

    for style in doc.styles:
        if not hasattr(style, 'font'):
            continue
        rPr = style.element.get_or_add_rPr()
        _set_rfonts(rPr)
    doc.styles['Normal'].font.size = Pt(BODY_PT)
    return doc


def apply_house_style(doc):
    """
    Enforce the house format on a finished document: re-applies setup_document(),
    centers every table on the page, and normalizes every run to Arial, forcing any
    explicit non-heading size below HEADING_MIN_PT down to BODY_PT. add_footnote() calls
    this, so every skill's output conforms even if its generated script hardcoded Pt(12)
    somewhere or skipped autofit_table().
    """
    setup_document(doc)
    for tbl in doc.element.body.iter(qn('w:tbl')):
        _center_table(tbl)
    containers = [doc]
    for section in doc.sections:
        containers += [section.header, section.footer]
    for container in containers:
        for p in _iter_paragraphs(container):
            heading = _is_heading(p)
            for run in p.runs:
                _set_rfonts(run._r.get_or_add_rPr())
                size = run.font.size
                if not heading and size is not None and size.pt < HEADING_MIN_PT:
                    run.font.size = Pt(BODY_PT)
    return doc


def _separate_from_previous_table(table):
    """
    Word merges two tables that sit directly next to each other into one table, forcing
    the second onto the first's column grid (columns collapse to one character wide).
    Insert an empty paragraph between them so each keeps its own grid.
    """
    tbl = table._tbl
    prev = tbl.getprevious()
    if prev is not None and prev.tag == qn('w:tbl'):
        spacer = OxmlElement('w:p')
        tbl.addprevious(spacer)


def _center_table(tbl):
    """Center a table horizontally on the page (w:jc=center, no left indent)."""
    tblPr = tbl.tblPr
    tblPr.alignment = WD_TABLE_ALIGNMENT.CENTER
    ind = tblPr.find(qn('w:tblInd'))
    if ind is not None:
        tblPr.remove(ind)


def autofit_table(table):
    """
    Set table layout to autofit and strip all fixed w:tcW cell-width overrides.
    Also centers the table on the page and inserts a spacer paragraph if this table
    directly follows another table, so Word does not merge the two.
    """
    _separate_from_previous_table(table)
    tbl = table._tbl
    tblPr = tbl.find(qn('w:tblPr'))
    if tblPr is None:
        tblPr = OxmlElement('w:tblPr')
        tbl.insert(0, tblPr)
    for tag, attrs in [('w:tblW', {'w:w': '0', 'w:type': 'auto'}), ('w:tblLayout', {'w:type': 'autofit'})]:
        el = tblPr.find(qn(tag))
        if el is None:
            el = OxmlElement(tag)
        for k, v in attrs.items():
            el.set(qn(k), v)
        if el not in list(tblPr):
            tblPr.append(el)
    look = tblPr.find(qn('w:tblLook'))
    if look is not None:
        tblPr.append(look)   # schema order: tblLook must stay last, after tblLayout
    _center_table(tbl)
    for row in table.rows:
        for cell in row.cells:
            tc = cell._tc
            tcPr = tc.find(qn('w:tcPr'))
            if tcPr is not None:
                for tcW in tcPr.findall(qn('w:tcW')):
                    tcPr.remove(tcW)


def add_table_borders(table):
    """Apply a thin single border to all four sides (and inner dividers) of every cell."""
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
            for side in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
                border = OxmlElement(f'w:{side}')
                border.set(qn('w:val'), 'single')
                border.set(qn('w:sz'), '4')
                border.set(qn('w:color'), '000000')
                tcBorders.append(border)


def set_row_font_size(row, size=BODY_PT):
    """Set Arial at `size` points (default 10) for all runs in all cells of a table row."""
    for cell in row.cells:
        for para in cell.paragraphs:
            for run in para.runs:
                run.font.size = Pt(size)
                _set_rfonts(run._r.get_or_add_rPr())


def fmt_value(v, prefix='$'):
    """Format a numeric value with smart scale: B ≥1B, M ≥1M, K ≥1K, else raw.
    Use this in all skill-generated Word table scripts instead of hardcoding / 1e9.
    Examples: fmt_value(1_500_000_000) → '$1.50B'
              fmt_value(42_000_000)    → '$42.0M'
              fmt_value(850_000)       → '$850.0K'
              fmt_value(-5_000_000)    → '-$5.0M'
              fmt_value(None)          → 'N/A'
    """
    if v is None:
        return "N/A"
    abs_v = abs(v)
    sign = '-' if v < 0 else ''
    if abs_v >= 1e9:
        return f"{sign}{prefix}{abs_v/1e9:.2f}B"
    if abs_v >= 1e6:
        return f"{sign}{prefix}{abs_v/1e6:.1f}M"
    if abs_v >= 1e3:
        return f"{sign}{prefix}{abs_v/1e3:.1f}K"
    return f"{sign}{prefix}{abs_v:.2f}"


def add_source_note(paragraph_or_cell, source):
    """
    Append a small italic gray "Source: ..." run citing where a figure or
    table came from — SEC EDGAR, Yahoo Finance, a hybrid of both, or a
    WebSearch citation. Accepts a docx Paragraph (appends inline, e.g. right
    after a stated figure) or a table cell (appends as that cell's own
    trailing run, e.g. a small note under a financial-snapshot table).
    Use the labels compute_metrics(ticker, with_sources=True) already
    returns (quick_stock_metrics.SRC_SEC / SRC_YAHOO / SRC_HYBRID /
    SRC_COMPUTED / SRC_NA) when citing a metrics-table figure, or a short
    plain-text citation (e.g. "WebSearch — Coherent Q4 FY2026 press
    release") for a qualitative figure pulled from web research.
    """
    para = paragraph_or_cell.paragraphs[0] if hasattr(paragraph_or_cell, "paragraphs") else paragraph_or_cell
    run = para.add_run(f"  [Source: {source}]")
    run.font.size = Pt(BODY_PT)
    run.font.italic = True
    run.font.color.rgb = RGBColor(0x80, 0x80, 0x80)


def add_footnote(doc):
    """
    Append a standard AI disclaimer footnote as the last paragraph of the document,
    then enforce the house format (landscape, narrow margins, Arial 10pt) on the
    whole document via apply_house_style(). Call immediately before doc.save().
    """
    doc.add_paragraph()  # spacer
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    run = p.add_run(
        "This analysis was generated by AI with human instructions. "
        "It is provided for informational purposes only and does not constitute investment advice. "
        "Past performance is not indicative of future results. "
        "Always conduct your own research and consult a qualified financial advisor before making any investment decisions."
    )
    run.font.size = Pt(BODY_PT)
    run.font.color.rgb = RGBColor(0x80, 0x80, 0x80)
    run.font.italic = True
    apply_house_style(doc)
