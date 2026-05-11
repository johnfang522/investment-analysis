# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Environment

Always use the project's virtual environment:
```
.venv/Scripts/python   # run scripts
.venv/Scripts/pip      # install packages
```

Key dependencies: `yfinance`, `openpyxl`, `python-docx`.

## Project Overview

This is an investment analysis toolkit that fetches financial data from Yahoo Finance and runs structured equity research analyses via Claude Code slash commands (skills).

**Data flow:**
1. `yahoo_finance_data.py` fetches raw data from Yahoo Finance → saves JSON files to `Outputs/`
2. `key_stock_metrics.py` reads those JSON files → produces an Excel workbook in `Outputs/`
3. Claude Code skills (`.claude/commands/`) perform web-searched qualitative analysis → produce Word documents in `Outputs/`

## Core Scripts

**`yahoo_finance_data.py`** — data fetching library
- `fetch_all(tickers)` — fetches all data types for a list of tickers; call this to pre-populate data
- `load_tickers()` — reads `tickers.txt` (ignores `#` comments and blank lines)
- Individual getters: `get_income_statements()`, `get_balance_sheets()`, `get_cash_flow_statements()`, `get_quick_metrics()`, `get_price_history(ticker, years=3)`
- JSON output path: `Outputs/{TICKER}/` (e.g., `Outputs/NVDA/`) — one subfolder per ticker, created automatically
- `{ticker_lower}` means `ticker.lower()` (e.g., `NVDA` → `nvda`); used in all JSON filenames
- JSON filenames within the folder: `{ticker_lower}_quick_metrics.json`, `{ticker_lower}_balance_sheet_quarterly.json`, `{ticker_lower}_price_history.json`, and `{ticker_lower}_{income_statement|cash_flow_statement}_{quarterly|annual|ttm}.json`
- Income statements and cash flow statements produce three files each (quarterly, annual, ttm); balance sheet produces only quarterly
- `get_price_history()` returns a `{"YYYY-MM-DD": price}` dict; used by technical analysis charts
- To re-fetch all tickers: `.venv/Scripts/python yahoo_finance_data.py` (reads `tickers.txt`); to force-refresh a single ticker, delete `Outputs/{TICKER}/` then re-run the skill or call `fetch_all([ticker])` from a script

**`key_stock_metrics.py`** — Excel report generator
- Reads `Outputs/{TICKER}/{ticker_lower}_quick_metrics.json` (via `load_quick()`); when a metric is missing from quick_metrics, `compute_metrics()` falls back to the TTM/quarterly/annual JSON files automatically
- `debtToEquity` from Yahoo Finance is already expressed as a percentage (e.g. `173` = 173%); the script always divides by 100 to convert to a ratio — do not double-divide
- `dividendYield` from Yahoo Finance is already a decimal (e.g. `0.0052` = 0.52%) when read as `trailingAnnualDividendYield`, but `dividendYield` (the forward estimate field) is sometimes returned as a percentage — the script divides `dividendYield` by 100 to normalize; do not double-divide
- RSI is computed directly from `{ticker_lower}_price_history.json` (Wilder's 14-day method) inside `_calc_rsi()` — not sourced from Yahoo Finance
- Produces `Outputs/key_stock_metrics_YYYYMMDD.xlsx` with per-ticker sheets + a `Comparison` sheet (placed first)
- Can be run directly: `.venv/Scripts/python key_stock_metrics.py [TICKER ...]`

**`chart_*.py`** — standalone chart generators (one per analysis domain)
- Scripts: `chart_income_statement.py`, `chart_balance_sheet.py`, `chart_cash_flow.py`, `chart_growth_profitability.py`, `chart_valuation.py`, `chart_technical.py`
- Each takes a single `TICKER` positional argument and saves PNG(s) to `Outputs/{TICKER}/`; e.g. `.venv/Scripts/python chart_technical.py NVDA`
- Skills call these scripts rather than generating matplotlib code inline; if a chart needs updating, edit the corresponding `chart_*.py`
- Each script reads its required JSON files from `Outputs/{TICKER}/` directly — run `yahoo_finance_data.py` first if JSON is missing

**`doc_utils.py`** — shared python-docx helpers
- Provides `autofit_table(table)`, `add_table_borders(table)`, and `set_row_font_size(row, size=12)`
- All skill-generated Word scripts import from here; see the Word Document Generation section for the required import pattern
- When adding a new helper needed by multiple skills, add it here rather than inline in each skill

## Tickers

Edit `tickers.txt` to add/remove tickers (one per line, `#` for comments). Currently tracking: AAPL, AMZN, ASML, AVGO, COHR, GOOG, ISRG, META, MSFT, MRVL, NVDA, ORCL, TSLA, TSM.

## Slash Commands (Skills)

The intended workflow runs in three stages:

**Stage 1 — Theme Discovery:** Identify the value chain for a macro trend and surface candidate stocks at each layer.

**Stage 2 — Quick Filter:** Screen candidates on financial quality before committing to deep research.

**Stage 3 — Individual Stock Analysis:** Deep-dive on specific names across all dimensions, culminating in a research note.

| Stage | Skill | Argument | Output |
|---|---|---|---|
| 1 | `/emerging_industry_trend_identification` | THEME or _(none)_ | Chat output (signal scorecard, value chain map, bottleneck analysis, positioning) |
| 1 | `/industry_trend_analysis` | THEME | Word: `Outputs/industry_trend_analysis_{theme}_{YYYYMMDD}.docx` |
| 1 | `/market_sentiment_framework` | THEME or "broad market" | Word: `Outputs/market_sentiment_{theme}_{YYYYMMDD}.docx` |
| 2 | `/key_stock_metrics` | _(none — reads `tickers.txt`)_ | Excel: `Outputs/key_stock_metrics_YYYYMMDD.xlsx` |
| 3 | `/business_overview_analysis` | TICKER | Word: `Outputs/{TICKER}/1_{ticker}_business_overview_analysis.docx` |
| 3 | `/leadership_analysis` | TICKER | Word: `Outputs/{TICKER}/2_{ticker}_leadership_analysis.docx` |
| 3 | `/income_statement_analysis` | TICKER | Word: `Outputs/{TICKER}/3_{ticker}_income_statement_analysis.docx` |
| 3 | `/balance_sheet_analysis` | TICKER | Word: `Outputs/{TICKER}/4_{ticker}_balance_sheet_analysis.docx` |
| 3 | `/cash_flow_analysis` | TICKER | Word: `Outputs/{TICKER}/5_{ticker}_cash_flow_analysis.docx` |
| 3 | `/growth_and_profitability_analysis` | TICKER | Word: `Outputs/{TICKER}/6_{ticker}_growth_and_profitability_analysis.docx` |
| 3 | `/business_potential_analysis` | TICKER | Word: `Outputs/{TICKER}/7_{ticker}_business_potential_analysis.docx` |
| 3 | `/valuation_analysis` | TICKER | Word: `Outputs/{TICKER}/8_{ticker}_valuation_analysis.docx` |
| 3 | `/technical_analysis` | TICKER | Word: `Outputs/{TICKER}/9_{ticker}_technical_analysis.docx` |
| 3 | `/single_name_stock_analysis` | TICKER | Word: `Outputs/{TICKER}/{ticker}_research_package_YYYYMMDD.docx` (+ individual note + appendices) |

- `/emerging_industry_trend_identification` scans for live bottleneck signals before the market prices them in — outputs directly to chat (no Word doc); use it before `/industry_trend_analysis` when you want to surface *what* to research, not just map a known theme
- `/market_sentiment_framework` scores investor sentiment across 5 pillars (positioning, momentum, valuation, macro, narrative) and saves a Word report; pass a theme name or "broad market"
- `/key_stock_metrics` with no args reads from `tickers.txt`; all other skills require a TICKER or THEME argument
- `/key_stock_metrics` always re-fetches fresh data via `fetch_all()` before computing metrics, even if JSON files already exist
- Skills read local JSON from `Outputs/` first, run `yahoo_finance_data.py` if missing, then supplement with `WebSearch` for analyst estimates, guidance, and any N/A values
- Each analysis skill generates matplotlib charts (saved as PNGs to `Outputs/`), then writes and executes a `python-docx` script inline to embed the charts and produce the `.docx`
- `/single_name_stock_analysis` always re-fetches fresh Yahoo Finance data and re-runs all 9 individual analyses in sequence (including `/leadership_analysis`), then synthesizes a 2–3 page Wall Street–style research note (BUY/HOLD/SELL with price target), and finally assembles all documents into a single `_research_package_` Word file with page numbers

## Word Document Generation

When writing `python-docx` table code in any skill or script:
- **Always initialize tables with `rows=1`** (header only), then call `table.add_row()` for each data row — do NOT use `rows=1+len(data)` upfront, which creates blank rows between the header and data
- **Every table must call `autofit_table(table)` then `add_table_borders(table)` AFTER all rows are added** — calling before rows are added means new rows won't inherit the settings. Never call them at table creation time; always call them after the last `table.add_row()`.
  - `autofit_table` — sets `tblW`/`tblLayout` to autofit and strips all fixed `w:tcW` cell widths; never use `table.columns[i].width` or any fixed-width assignment
  - `add_table_borders` — applies a thin single border (`sz=4`, `val="single"`, `color="000000"`) to all four sides of every cell via `w:tcBorders`
- **All non-header table cell text must use font size 12.** Call `set_row_font_size(row)` on every data row immediately after `table.add_row()`. Do **not** call it on the header row.
- All three helpers live in `doc_utils.py` at the project root — generated scripts import them with:
  ```python
  import sys; sys.path.insert(0, '.')
  from doc_utils import autofit_table, add_table_borders, set_row_font_size
  ```
  The `sys.path.insert(0, '.')` is required because scripts are saved under `Outputs/{TICKER}/` but run from the project root.
- **Every skill must set portrait orientation and narrow margins** immediately after `doc = Document()`:
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

## Adding a New Skill

To add a new analysis skill:
1. Create `.claude/commands/{skill_name}.md` — write it as instructions Claude will follow at execution time (not Python code itself)
2. If the skill generates charts, add a `chart_{name}.py` at the project root following the existing chart script pattern (reads JSON from `Outputs/{TICKER}/`, saves PNG to the same folder)
3. If the skill generates a Word document, instruct it to: run the relevant `chart_*.py` → write a `generate_*.py` script to `Outputs/{TICKER}/` (or `Outputs/` root for non-ticker skills) → execute it → confirm the `.docx` path
4. All generated Word scripts must import helpers from `doc_utils.py` (see Word Document Generation section)
5. Ad-hoc one-off Python scripts should be saved to `Outputs/{TICKER}/`, not the project root

## Outputs Directory

- **Ticker-specific files** (JSON, PNG, Word) → `Outputs/{TICKER}/` (e.g., `Outputs/NVDA/`) — created automatically by `yahoo_finance_data.py` and each analysis skill
- **Cross-ticker files** (Excel) → `Outputs/` root — e.g., `key_stock_metrics_YYYYMMDD.xlsx`
- JSON files are the persistent data cache — delete and re-fetch if data is stale; Word/PNG files are overwritten on each run
- `generate_*.py`, `assemble_*.py`, and `compute_*.py` scripts generated by skills are saved to `Outputs/{TICKER}/` (not the project root) — safe to delete at any time
