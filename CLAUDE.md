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
- JSON filenames within the folder: `{ticker_lower}_quick_metrics.json`, `{ticker_lower}_balance_sheet_quarterly.json`, `{ticker_lower}_price_history.json`, and `{ticker_lower}_{income_statement|cash_flow_statement}_{quarterly|annual|ttm}.json`
- Income statements and cash flow statements produce three files each (quarterly, annual, ttm); balance sheet produces only quarterly
- `get_price_history()` returns a `{"YYYY-MM-DD": price}` dict; used by technical analysis charts

**`key_stock_metrics.py`** — Excel report generator
- Reads only `Outputs/{TICKER}/{ticker_lower}_quick_metrics.json` (via `load_quick()`); the detailed statement fallback logic lives in the `/key_stock_metrics` skill prompt, not this script
- `debtToEquity` from Yahoo Finance is already expressed as a percentage (e.g. `173` = 173%); the script always divides by 100 to convert to a ratio — do not double-divide
- Produces `Outputs/key_stock_metrics_YYYYMMDD.xlsx` with per-ticker sheets + a `Comparison` sheet (placed first)
- Can be run directly: `.venv/Scripts/python key_stock_metrics.py [TICKER ...]`

**`chart_*.py`** — standalone chart generators (one per analysis domain)
- Scripts: `chart_income_statement.py`, `chart_balance_sheet.py`, `chart_cash_flow.py`, `chart_growth_profitability.py`, `chart_valuation.py`, `chart_technical.py`
- Each takes a single `TICKER` argument and saves PNG(s) to `Outputs/{TICKER}/`
- Skills call these scripts rather than generating matplotlib code inline; if a chart needs updating, edit the corresponding `chart_*.py`
- Each script reads its required JSON files from `Outputs/{TICKER}/` directly — run `yahoo_finance_data.py` first if JSON is missing

## Tickers

Edit `tickers.txt` to add/remove tickers (one per line, `#` for comments). Currently tracking: AAPL, AMZN, ASML, AVGO, COHR, GOOG, ISRG, META, MSFT, MRVL, NVDA, ORCL, TSLA, TSM.

## Slash Commands (Skills)

The intended workflow runs in three stages:

**Stage 1 — Theme Discovery:** Identify the value chain for a macro trend and surface candidate stocks at each layer.

**Stage 2 — Quick Filter:** Screen candidates on financial quality before committing to deep research.

**Stage 3 — Individual Stock Analysis:** Deep-dive on specific names across all dimensions, culminating in a research note.

| Stage | Skill | Argument | Output |
|---|---|---|---|
| 1 | `/industry_trend_analysis` | THEME | Word: `Outputs/industry_trend_analysis_{theme}_{YYYYMMDD}.docx` |
| 2 | `/key_stock_metrics` | _(none — reads `tickers.txt`)_ | Excel: `Outputs/key_stock_metrics_YYYYMMDD.xlsx` |
| 3 | `/business_overview_analysis` | TICKER | Word: `Outputs/{ticker}_business_overview_analysis.docx` |
| 3 | `/leadership_analysis` | TICKER | Word: `Outputs/{ticker}_leadership_analysis.docx` |
| 3 | `/income_statement_analysis` | TICKER | Word: `Outputs/{ticker}_income_statement_analysis.docx` |
| 3 | `/balance_sheet_analysis` | TICKER | Word: `Outputs/{ticker}_balance_sheet_analysis.docx` |
| 3 | `/cash_flow_analysis` | TICKER | Word: `Outputs/{ticker}_cash_flow_analysis.docx` |
| 3 | `/growth_and_profitability_analysis` | TICKER | Word: `Outputs/{ticker}_growth_and_profitability_analysis.docx` |
| 3 | `/business_potential_analysis` | TICKER | Word: `Outputs/{ticker}_business_potential_analysis.docx` |
| 3 | `/valuation_analysis` | TICKER | Word: `Outputs/{ticker}_valuation_analysis.docx` |
| 3 | `/technical_analysis` | TICKER | Word: `Outputs/{ticker}_technical_analysis.docx` |
| 3 | `/single_name_stock_analysis` | TICKER | Word: `Outputs/{ticker}_research_notes_YYYYMMDD.docx` |

- `/key_stock_metrics` with no args reads from `tickers.txt`; all other skills require a TICKER or THEME argument
- `/key_stock_metrics` always re-fetches fresh data via `fetch_all()` before computing metrics, even if JSON files already exist
- Skills read local JSON from `Outputs/` first, run `yahoo_finance_data.py` if missing, then supplement with `WebSearch` for analyst estimates, guidance, and any N/A values
- Each analysis skill generates matplotlib charts (saved as PNGs to `Outputs/`), then writes and executes a `python-docx` script inline to embed the charts and produce the `.docx`
- `/single_name_stock_analysis` always re-fetches fresh Yahoo Finance data and re-runs all 9 individual analyses in sequence, then synthesizes a 2–3 page Wall Street–style research note (BUY/HOLD/SELL with price target)

## Word Document Generation

When writing `python-docx` table code in any skill or script:
- **Always initialize tables with `rows=1`** (header only), then call `table.add_row()` for each data row
- Do NOT use `rows=1+len(data)` upfront — this creates blank rows between the header and data

## Outputs Directory

- **Ticker-specific files** (JSON, PNG, Word) → `Outputs/{TICKER}/` (e.g., `Outputs/NVDA/`) — created automatically by `yahoo_finance_data.py` and each analysis skill
- **Cross-ticker files** (Excel) → `Outputs/` root — e.g., `key_stock_metrics_YYYYMMDD.xlsx`
- JSON files are the persistent data cache — delete and re-fetch if data is stale; Word/PNG files are overwritten on each run
