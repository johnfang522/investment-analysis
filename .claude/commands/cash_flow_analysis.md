# Cash Flow Analysis

You are a financial analyst writing a **3-page max** cash flow review for institutional investors. Lead with visuals (charts, tables, status icons).

**DATA SOURCING:**
1. Load `Outputs/{TICKER}/{ticker_lowercase}_cash_flow_statement_quarterly.json` and `_quick_metrics.json`. Run `yahoo_finance_data.py` if missing.
2. WebSearch only for items genuinely missing (interest expense, dividend totals). Leave N/A if not found.

**Always YoY. Never sequential quarters.**

**STYLE:** Bullets only — 1 short sentence each. Tables for all numbers. Status icons: ✅ ⚠️ 🔴 / ↑↓→

---

FORMAT YOUR RESPONSE EXACTLY AS FOLLOWS:

**Data as of**: [Fiscal Quarter] [Year]

## Charts

```
.venv/Scripts/python chart_cash_flow.py {TICKER}
```
Produces `{ticker}_cash_flow_waterfall.png` and `{ticker}_cash_flow_trend.png` in `Outputs/{TICKER}/`.

## At a Glance

| Field | Value | Signal |
|-------|-------|--------|
| Operating Cash Flow | $X.XB | +X% YoY ↑/↓ |
| Free Cash Flow | $X.XB | +X% YoY ↑/↓ |
| FCF Margin | XX% | ✅ >15% / ⚠️ 5–15% / 🔴 <5% |
| FCF Conversion (FCF ÷ NI) | X.Xx | ✅ >1 / ⚠️ ~1 / 🔴 <1 |
| Capital Allocation Bias | Buybacks / Dividends / M&A / Reinvest | — |
| Overall Rating | **X / 5** | — |

## Cash Flow Snapshot (YoY)

*One table = OCF, FCF, CapEx and the key margins, current quarter vs prior-year quarter.*

| Metric | Latest Qtr | Prior-Yr Qtr | Δ |
|--------|-----------|--------------|---|
| Operating Cash Flow | $X.XB | $X.XB | +X% ↑ |
| OCF Margin | XX% | XX% | +X pp |
| CapEx | $X.XB | $X.XB | +X% |
| Free Cash Flow | $X.XB | $X.XB | +X% |
| FCF Margin | XX% | XX% | +X pp |
| FCF / Net Income | X.Xx | X.Xx | — |

- **What drove the change:** [1 sentence — working capital, CapEx surge, etc.]

## Capital Allocation


| Use of Cash | Latest Qtr | Prior-Yr Qtr | Δ |
|-------------|-----------|--------------|---|
| CapEx | $X.XB | $X.XB | +X% |
| Buybacks | $X.XB | $X.XB | +X% |
| Dividends | $X.XB | $X.XB | +X% |
| Debt Repayment | $X.XB | $X.XB | +X% |

- **Red flag check:** [e.g., "Buybacks rising while debt grows" — or "None identified"]

## Financial Safety

| Coverage Ratio | Latest | Plain English |
|----------------|--------|---------------|
| Interest Coverage (OCF ÷ interest) | X.Xx | Higher = safer |
| Dividend Coverage (FCF ÷ dividends) | X.Xx | >1 means dividend covered |
| Debt Coverage (OCF ÷ total debt) | X.Xx | Years to repay all debt from OCF |

- **Could the company self-fund through a bad year?** Yes / Tight / No — [1 sentence]

## Strengths vs Risks

| ✅ Strengths | ⚠️ Risks |
|-------------|----------|
| [e.g., FCF $X.XB at XX% margin — ahead of net income] | [e.g., CapEx +XX% YoY pressuring FCF margin] |
| [Strength 2] | [Risk 2] |
| [Strength 3] | [Risk 3] |

---

## Rating: X / 5

**Justification:** [2 sentences — FCF margin + OCF vs net income + biggest allocation flag]

*Scale: 5 = exceptional (>25% FCF margin, FCF >1x NI, disciplined) · 4 = strong (15–25%) · 3 = average (5–15%) · 2 = weak (<5%) · 1 = poor (negative)*

---

## Save to Word Document

Write and execute a Python script using `python-docx` (`.venv/Scripts/python`) that:
- Portrait, narrow margins (top/bottom 0.5", left/right 0.75") — see CLAUDE.md
- Title: `{TICKER} — Cash Flow` (bold, centered) + date subtitle
- **Embed both chart images at `width=Inches(7.0)`** to fill the full text width
- Section headings as Heading 1
- Bullets as Word list items
- **Tables: initialize with `rows=1` (header only), then `table.add_row()` per data row.** Call `set_row_font_size(row)` on every data row.
- **Every table**: call `autofit_table(table)` then `add_table_borders(table)` AFTER all rows added
- Dark blue header rows (fill `1F3864`), white bold text
- Source citations in small italic
- Rating block in bold
- Saves to `Outputs/{TICKER}/5_{ticker_lowercase}_cash_flow_analysis.docx`
- Save the script file to `Outputs/{TICKER}/generate_{ticker_lowercase}_cash_flow.py` and run it from project root

Call `add_footnote(doc)` immediately before `doc.save(...)` to append the standard AI disclaimer.

Import the shared helpers from `doc_utils.py`:
```python
import sys; sys.path.insert(0, '.')
from doc_utils import autofit_table, add_table_borders, set_row_font_size, add_footnote
```

Confirm the output file path when done.
