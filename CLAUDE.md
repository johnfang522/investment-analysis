# CLAUDE.md

Guidance for Claude Code (claude.ai/code) when working in this repository.

## What This Project Does

An investment research toolkit that turns a few commands into hedge-fund-style research reports.

- **What you get**
  - A structured, opinionated analysis written for a portfolio manager: a directional call (LONG / SHORT / PASS, or Risk-On / Risk-Off for markets), a conviction score, and the reasoning behind it
  - Reports open in a browser as interactive HTML pages (Word on request), collected in one searchable library: `Outputs/index.html`
- **How it works**
  - You run a slash command (a "skill") such as `/single_stock_deep_research NVDA`
  - The skill pulls financial statements from SEC EDGAR and quotes/prices from Yahoo Finance, searches the web for estimates, guidance and news, then writes the report
  - Every number cites its source
- **Quick start**
  - Market backdrop first: `/market_sentiment_analysis`
  - Find ideas: `/theme_discovery_scanner` → `/emerging_industry_trend` → `/industry_trend_analysis`
  - Screen names: `/quick_stock_metrics`
  - Go deep on a name: `/single_stock_deep_research TICKER` (or the lighter `/single_stock_quick_research TICKER`)
  - Check a single quarter: `/earnings_report_analyzer TICKER`

### The 4-stage workflow
- **Stage 1 — Market Conditions:** assess broad market sentiment and risk before deploying capital
- **Stage 2 — Theme Discovery:** identify the value chain for a macro trend and surface candidate stocks at each layer
- **Stage 3 — Quick Filter:** screen candidates on financial quality before committing to deep research
- **Stage 4 — Individual Stock Analysis:** deep-dive on specific names across all dimensions, ending in a research note

### All skills at a glance

**Stage 1 — Market Conditions**
- `/market_sentiment_analysis` — *Is the market healthy or frothy?*
  - Scores 7 indicators (VIX, Fear & Greed, put/call, breadth, credit spreads, Shiller CAPE, Buffett Indicator)
  - Adds a 3–6 month macro outlook (Fed, rates, deficit, Treasury yields) and a margin-debt leverage check
  - Ends with a Risk-On / Neutral / Risk-Off posture and a bubble-risk verdict

**Stage 2 — Theme Discovery**
- `/theme_discovery_scanner` — *What themes are emerging that I should be watching?* Scans five channels (capital flows, talent, incumbents' fear, science, cost curves) and keeps a ranked watchlist
- `/emerging_industry_trend` — *Where are the bottlenecks before the market prices them in?* Signal scorecard, value chain map, positioning
- `/industry_trend_analysis` — *Who wins in this theme, and when do I get out?* Maps the full value chain with stocks at every layer, TAM expansion, a variant view, and pre-committed exit tripwires
- `/industry_deep_dive` — *How does this industry actually work?* Porter's Five Forces, economics, competitors, barriers to entry
- `/ai_company_deep_dive` — *Is this company's AI story real?* Places it in the AI stack, scores chokepoint strength and revenue quality, and builds a 3-scenario thesis
- `/multibagger_screener` — *Which stocks could 5x–100x?* Screens a theme or quality universe into a scored 3–7 name shortlist (no Buy/Sell calls)

**Stage 3 — Quick Filter**
- `/quick_stock_metrics` — *Which names deserve a deeper look?* Side-by-side Excel and HTML grid of 22 financial metrics for all tickers in `tickers.txt`, with a long/short screen read

**Stage 4 — Individual Stock Analysis**
- Eight component analyses (each ends with a Bullish / Neutral / Bearish read and a variant view)
  - `/business_overview_analysis` — what the company does and how it competes
  - `/leadership_analysis` — management quality, ownership and capital allocation
  - `/income_statement_analysis` — growth, margins, what drove the quarter, and consensus outlook
  - `/balance_sheet_analysis` — leverage, liquidity and off-balance-sheet risks
  - `/cash_flow_analysis` — free cash flow quality and conversion
  - `/business_potential_analysis` — readiness to capture its next big opportunity
  - `/valuation_analysis` — what the stock is worth (DCF, multiples, peers) with a price target
  - `/technical_analysis` — trend, moving averages, momentum and entry levels
- `/single_stock_deep_research` — *The full research package.* Runs all 8 analyses, then writes a 2–3 page note with LONG / SHORT / PASS, conviction, price target, stop and risk/reward
- `/single_stock_quick_research` — *A faster initiation note.* Seven-pillar single-stock read; the default for "should I buy X?"
- `/earnings_report_analyzer` — *Was the quarter actually good?* Scores one earnings report across 7 dimensions, going beyond the headline beat/miss

### Outputs by skill
- Every report is **HTML by default** (`.html`); a `.docx` is written only on request (add `--docx` or `--both`)
- Paths show the base name; swap the extension as needed

| Stage | Skill | Argument | Output |
|---|---|---|---|
| 1 | `/market_sentiment_analysis` | _(none)_ | `Outputs/market_sentiment_analysis_{YYYYMMDD}.html` + 10 PNGs + dashboard PNG |
| 2 | `/theme_discovery_scanner` | CHANNEL/SECTOR hint or _(none)_ | `Outputs/theme_discovery_scan_{YYYYMMDD}.html` |
| 2 | `/emerging_industry_trend` | THEME, TICKER, or _(none)_ | `Outputs/emerging_industry_trends_{theme}_{YYYYMMDD}.html` |
| 2 | `/industry_trend_analysis` | THEME or TICKER | `Outputs/industry_trend_analysis_{theme}_{YYYYMMDD}.html` |
| 2 | `/industry_deep_dive` | THEME or TICKER | `Outputs/industry_deep_dive_{theme}_{YYYYMMDD}.html` |
| 2 | `/ai_company_deep_dive` | TICKER | `Outputs/{TICKER}/{ticker}_company_deep_dive_{YYYYMMDD}.html` |
| 2 | `/multibagger_screener` | THEME or _(none)_ | `Outputs/multibagger_screener_{theme_or_date}_{YYYYMMDD}.html` |
| 3 | `/quick_stock_metrics` | _(none — reads `tickers.txt`)_ | Excel `Outputs/quick_stock_metrics_YYYYMMDD.xlsx` (Summary sheet = screen read) + `.html` |
| 4 | `/business_overview_analysis` | TICKER | `Outputs/{TICKER}/1_{ticker}_business_overview_analysis.html` |
| 4 | `/leadership_analysis` | TICKER | `Outputs/{TICKER}/2_{ticker}_leadership_analysis.html` |
| 4 | `/income_statement_analysis` | TICKER | `Outputs/{TICKER}/3_{ticker}_income_statement_analysis.html` |
| 4 | `/balance_sheet_analysis` | TICKER | `Outputs/{TICKER}/4_{ticker}_balance_sheet_analysis.html` |
| 4 | `/cash_flow_analysis` | TICKER | `Outputs/{TICKER}/5_{ticker}_cash_flow_analysis.html` |
| 4 | `/business_potential_analysis` | TICKER | `Outputs/{TICKER}/6_{ticker}_business_potential_analysis.html` |
| 4 | `/valuation_analysis` | TICKER | `Outputs/{TICKER}/7_{ticker}_valuation_analysis.html` |
| 4 | `/technical_analysis` | TICKER | `Outputs/{TICKER}/8_{ticker}_technical_analysis.html` |
| 4 | `/single_stock_deep_research` | TICKER | Note `Outputs/{TICKER}/{ticker}_stock_deep_research_notes_YYYYMMDD.html` (the hub); with Word, also the merged `{ticker}_stock_deep_research_YYYYMMDD.docx` package |
| 4 | `/single_stock_quick_research` | TICKER | `Outputs/{TICKER}/{ticker}_stock_quick_research_YYYYMMDD.html` |
| 4 | `/earnings_report_analyzer` | TICKER | `Outputs/{TICKER}/{ticker}_earnings_analysis_YYYYMMDD.html` |

---

# Technical Reference

Everything below is for working on the code and the skills.

## Environment

- **Always use the project's virtual environment**
  - Run scripts: `.venv/Scripts/python`
  - Install packages: `.venv/Scripts/pip`
- **Key dependencies:** `yfinance`, `openpyxl`, `python-docx`, `matplotlib`, `numpy`
- **No test suite, linter or build step**
  - Verification = run the relevant script and inspect the file it writes to `Outputs/`
- **Prefix every Python invocation that prints to the console with `PYTHONIOENCODING=utf-8`**
  - Example: `PYTHONIOENCODING=utf-8 .venv/Scripts/python quick_stock_metrics.py AAPL`
  - Why
    - The default Windows console codec is cp1252
    - Printed output contains non-Latin-1 characters (`Oversold (≤30)`, `Very safe (>10×)`, `—`, `·`)
  - Failure mode
    - `UnicodeEncodeError: 'charmap' codec can't encode character` raised **partway through** the output
    - A diagnostic loop prints a few rows then dies, which looks like a data problem
  - Writing to files is unaffected; only stdout is affected
- **Git**
  - Gitignored: `Outputs/`, `.venv/`, `__pycache__/` (generated JSON, PNG, HTML, Word and Excel are never committed)
  - Tracked: Python libraries at the project root, `.claude/commands/`, `references/`, `tickers.txt`, this file

## Project Overview

- **What it is:** an investment analysis toolkit
  - Fetches financial data from SEC EDGAR and Yahoo Finance
  - Runs structured equity research via Claude Code slash commands (skills)
- **Data flow**
  1. `get_financial_data.py` fetches raw data and saves JSON to `Outputs/`
     - Statements (income, balance sheet, cash flow): SEC EDGAR
     - Quote data and price history: Yahoo Finance
  2. `quick_stock_metrics.py` reads that JSON and writes an Excel workbook to `Outputs/`
  3. Skills (`.claude/commands/`) add web-searched qualitative analysis and write reports to `Outputs/` (HTML by default)

## Core Scripts

### `get_financial_data.py` — data fetching entry point
- Skills and scripts call this, **not** `yahoo_finance_data.py` or `sec_edgar_data.py` directly
- `fetch_all(tickers, price_history=True)` — fetches all data types for a list of tickers
  - Combines `sec_edgar_data.fetch_edgar_statements()` with `yahoo_finance_data.get_quick_metrics()` and `get_price_history()`
  - Per-ticker failures are caught and printed, not fatal
  - Recent IPOs: TTM needs ≥4 quarters, so they raise `ValueError` and land in the results as `{"error": ...}`
  - **Price history is downloaded once, at the start of a skill run** (5 years of daily closes)
    - Skills that read `_price_history.json` use the default
      - `/technical_analysis`, `/income_statement_analysis`, `/earnings_report_analyzer`, `/quick_stock_metrics`, `/ai_company_deep_dive`, `/single_stock_quick_research`
      - `/single_stock_deep_research` via its Step 0
    - Skills that never use it pass `price_history=False`
      - business overview, leadership, balance sheet, cash flow, business potential, valuation, multibagger
    - Subagents spawned by `/single_stock_deep_research` skip the download (the parent already did it)
    - Chart scripts and `compute_metrics()` only read the JSON
- `load_tickers()` — reads `tickers.txt` (ignores `#` comments and blank lines)
- Re-fetching
  - All tickers: `.venv/Scripts/python get_financial_data.py` (reads `tickers.txt`, or pass tickers as args)
  - One ticker: delete `Outputs/{TICKER}/`, then re-run the skill or call `fetch_all([ticker])`

### `sec_edgar_data.py` — statement fetcher (SEC EDGAR XBRL "company facts" API)
- Why: Yahoo Finance is stale for weeks after an earnings release
- `fetch_edgar_statements(ticker)`
  - Saves JSON with Yahoo-style line-item names (`"Total Revenue"`, `"Operating Income"`, …) at the same paths the old Yahoo fetchers used
  - So `chart_*.py` and `quick_stock_metrics.py` need no field-name changes
  - Run directly: `.venv/Scripts/python sec_edgar_data.py TICKER`
  - Every SEC request needs the descriptive `User-Agent` with a contact email (`USER_AGENT`)
- **When numbers look inconsistent** (a metric stuck on a stale date, Revenue − Cost ≠ Gross Profit), suspect one of three things before a one-off ticker quirk
  1. A filer retired or switched an XBRL tag
     - Tag selection is freshness-based (`_extract_tag_series()`), never "first tag in the list"
  2. The filer reports cumulative year-to-date facts
     - Discrete quarters are derived by diffing within a fiscal year; Q4 = FY total − 9-month YTD
  3. The concept is never tagged at all
     - The field comes back `{}` or `0`, not wrong-looking
- **A `0` or empty debt figure on a company you know carries debt is missing data, not deleveraging**
  - Examples: SWKS `Total Debt` = 0 after retiring notes; AKAM leaves debt, PP&E and goodwill untagged
  - Fall back to `_quick_metrics.json` or the 10-Q, and cite the fallback
  - Distrust any leverage ratio (D/E, net debt/EBITDA) computed from the untagged line
  - Line items a filer stopped tagging (no successor) are cleared by `_drop_stale_line_items()`
- Balance sheet extras
  - `"Temporary Equity"` so `Assets − Liabilities − Equity` reconciles
  - `"Shares Outstanding"` from the `dei` namespace (in shares, not USD)
- TTM: `_best_ttm()` anchors every line item to the same four quarter-end dates
- **Full mechanics:** `references/data-layer.md`

### `yahoo_finance_data.py` — quote/market data (only data with no SEC equivalent)
- Do **not** import it directly from skills; go through `get_financial_data.py`
- `get_quick_metrics()` — market cap, P/E, dividend yield, beta, analyst targets, sector (the `stock.info` dict)
- `get_price_history(ticker, years=5)` — returns `{"YYYY-MM-DD": price}`; used by technical charts and RSI
  - **Closes are dividend-adjusted** (`auto_adjust=True`); `current_price` and the 52-week range are not
  - For material dividend payers (yield above ~2%, e.g. REITs), older prices, moving averages and closing highs/lows are understated
  - The technical skill recomputes from unadjusted closes (`auto_adjust=False`) for those names
- File conventions
  - Output path: `Outputs/{TICKER}/` (one subfolder per ticker, created automatically)
  - `{ticker_lower}` = `ticker.lower()` (e.g. `nvda`), used in all JSON filenames
  - Written by this module: `{ticker_lower}_quick_metrics.json` and `{ticker_lower}_price_history.json` only
  - Written by `sec_edgar_data.py`: `{ticker_lower}_balance_sheet_quarterly.json` and `{ticker_lower}_{income_statement|cash_flow_statement}_{quarterly|annual|ttm}.json`

### `quick_stock_metrics.py` — Excel generator and shared metrics library
- `compute_metrics(ticker, with_sources=True)` returns `(results, sources)`
  - `sources` labels each metric's *actual* source: `SRC_SEC`, `SRC_YAHOO`, `SRC_HYBRID`, `SRC_COMPUTED`, `SRC_NA`
  - It can differ by ticker: read it, never infer it from the key name
  - Plain `compute_metrics(ticker)` returns just `results`
- Where metrics come from
  - Statement-derived: SEC EDGAR JSON, falling back to `_quick_metrics.json`
  - Trailing P/E and Price/Sales: hybrids (SEC fundamentals × Yahoo price)
  - Forward P/E and PEG: Yahoo-only (they need consensus estimates)
  - Price, 52-week range, market cap, dividend yield, sector: always Yahoo
  - RSI: computed from `_price_history.json` (`_calc_rsi()`, Wilder 14-day)
- Shared library imported by `/single_stock_deep_research`
  - `compute_metrics()`, `_short_comment()`, `METRICS` (22 snake_case keys, render order), `color_current_price()`
  - Iterate `METRICS` instead of hardcoding keys
  - Ratio-style keys are plain multiples; margin-style keys are decimals needing `×100`
  - `dividend_yield` is `None` for non-payers, while `payout_ratio` is `0.0`
  - There is no EV/EBITDA key
- Unit traps
  - Yahoo `debtToEquity` is already a percentage; the script divides by 100 (don't double-divide)
  - The forward `dividendYield` can come back as a percentage and is divided by 100
- **A metric can be valid arithmetic and still meaningless**
  - `de` is `-10.1x` for negative book equity (SMG) and `_short_comment` calls it "Very conservative"
  - `roe` goes negative on negative equity
  - `trailing_pe` can diverge from Yahoo's with discontinued operations
  - Check the balance sheet's sign before repeating a label
- Output: `Outputs/quick_stock_metrics_YYYYMMDD.xlsx`
  - Sheets: `Summary` (buy-side screen read) → `Comparison` (per-cell hover-note sources + legend) → per-ticker sheets (with a "Source" column)
  - Run: `.venv/Scripts/python quick_stock_metrics.py [TICKER ...]`
  - Add the Summary: `.venv/Scripts/python quick_stock_metrics.py --summary Outputs/quick_stock_metrics_summary_YYYYMMDD.json`
    - Uses `write_summary_sheet()` on the screen-read JSON the `/quick_stock_metrics` skill writes
- **Full detail:** `references/data-layer.md`

### `chart_*.py` — standalone chart generators (one per analysis domain)
- Scripts: `chart_income_statement.py`, `chart_balance_sheet.py`, `chart_cash_flow.py`, `chart_valuation.py`, `chart_technical.py`
- Usage
  - Each takes a single `TICKER` argument and saves PNG(s) to `Outputs/{TICKER}/`
  - Example: `.venv/Scripts/python chart_technical.py NVDA`
  - Each reads its JSON from `Outputs/{TICKER}/`; run `get_financial_data.py` first if missing
- Skills call these scripts rather than writing matplotlib inline; to change a chart, edit the script
- `chart_income_statement.py`
  - Annual trend: last 5 FYs + TTM + consensus FYs
  - Quarterly trend: last 8 quarters + up to 4 consensus quarters
  - Grouped bars of revenue / gross profit / operating income / net income
    - Every bar labeled with amount, YoY and gross/operating/net margin
    - Consensus is revenue-only hatched bars
    - Share price (from `_price_history.json`) on a right axis: close on or before each period-end date, including TTM
    - Periods older than the cached 5-year history get no price point
  - No separate margin charts
  - Consensus comes from `{ticker_lower}_consensus_estimates.json`, written by `/income_statement_analysis` from WebSearch
    - Without it, the trends show actuals only
  - `annual_trend_rows()` / `quarterly_trend_rows()` are shared library functions (like `compute_metrics()`)
- `chart_balance_sheet.py`
  - Latest-quarter composition stack + grouped-bar trend of the last 8 quarters (total assets, equity, liabilities, debt, cash)
- `chart_cash_flow.py`
  - Latest-quarter OCF → CapEx → FCF waterfall + grouped-bar trend of the last 8 quarters (net income, operating cash flow, free cash flow)
  - Free CF bars also show FCF ÷ net income
  - The cash flow JSON has no net income; the trend takes it from `_income_statement_quarterly.json`
- `chart_technical.py`
  - Price with 20/50/100/200-day moving averages (`_ta_price_ma.png`) + Wilder RSI chart (`_ta_rsi.png`)

### `plot_market_sentiment_history.py` — persistent market sentiment charts
- What it does
  - Fetches 5 years of data for the 7 sentiment indicators
  - Plus: Treasury yields (FRED `DGS10`/`DGS2`, with a 10Y−2Y curve panel)
  - Plus: US fiscal picture (FRED `MTSDS133FMS` trailing-12M deficit + `A091RC1Q027SBEA` net interest)
  - Plus: margin debt (FRED `BOGZ1FL663067003Q` quarterly Z.1 margin loans, level + % of GDP)
  - 10 charts total, saved as PNGs to `Outputs/`
- Run from the project root: `.venv/Scripts/python plot_market_sentiment_history.py`
- Lives at the project root and is tracked in git (unlike the ephemeral `generate_*.py` / `assemble_*.py` scripts in `Outputs/`)
- `END` defaults to today; pass a `YYYY-MM-DD` CLI arg for a reproducible historical run
- **Update `BUFFETT_ANCHOR_VALUE` (top of file) before each run**
  - Use the current Buffett Indicator from a web search; there is no free live API
  - A stale anchor silently drifts the Buffett chart and current reading
- Wilshire proxy: uses `^FTW5000`, with an automatic fallback to `^W5000` when it returns no data
- See the External Data Sources section for the API gotchas baked into this script

### `report_renderer.py` — the report renderer every skill uses
- Skills write content (a JSON spec), **never** python-docx or HTML code
- `report_renderer.py SPEC_JSON`
  - Builds the self-contained, offline **interactive HTML** (and a house-style `.docx` on request) from one spec
  - Writes the skill's `_summary.json` (signal, conviction, key figures, variant view) — the return contract `/single_stock_deep_research` synthesizes from
  - Rebuilds `Outputs/index.html` (`--index` rebuilds it alone)
  - Skill-facing rules: `references/report-spec.md`; full schema: the module docstring
- **Output format is selectable; default is HTML only**
  - `report_renderer.py SPEC --format html|docx|both`, or env `REPORT_FORMAT`
  - Precedence: flag > env > spec `formats` > html
  - If the user adds `--docx` / `--both` (or says "word"), the skill appends `--format docx|both`
  - `/single_stock_deep_research` runs `assemble_package.py` only when Word was requested
- **`Outputs/index.html` (Investment Research Library)**
  - Organised by the 4 workflow stages
    - `STAGES` / `_stage_of()` in `report_renderer.py` map a report's `skill` to a stage
    - Single-stock reports default to Stage 4, grouped per ticker (cards collapsed by default)
    - To place a new skill in Stage 1–3, add its skill-name key to `STAGES`
  - Left navigation of stages and tickers
  - One instance per report: rebuilding the index deletes older dated copies (`<name>_YYYYMMDD.html` plus its `.docx`, `_spec.json`, `_summary.json`) when a later date exists (`prune_superseded()`), so a re-run replaces the earlier report
  - Every line shows its date and time; reports under 7 days old carry a "New" tag
  - Every report page has a floating, draggable "← Back" button (`.back-fab`)
    - Component reports go back to their research package page
    - Other pages go back to the library
- Blocks
  - Core: heading, paragraph (optional `color` for verdict lines), bullets (`numbered`), table (`fills`, `bold_rows`, `sortable`), chart, source, variant_view, read_through, verdict, page_break
  - Macro blocks (expanded before rendering)
    - `income_trend` — trend tables from `chart_income_statement`'s own rows
    - `metrics_snapshot` — deep-research Financial Snapshot (values, sources, colors from `compute_metrics()`; the spec supplies only comments)
    - `appendix_index` — HTML-only hub linking the 8 component pages
  - Add new block types here, not in skills
- HTML is self-contained, no CDN; publish it to GitHub Pages with `publish_reports.py` (see below)
  - `report_assets/report.css` + `report.js` are inlined
  - `.venv/Scripts/python publish_reports.py` copies only the `Outputs/**/*.html` files to the `gh-pages` branch (disclaimer banner and `noindex` added to the copies, force-pushed, never touches `master`); site: https://johnfang522.github.io/investment-analysis/ — public if the repo is public; `--dry-run` stages without pushing
  - Features: light/dark theme, contents sidebar, SVG charts with hover / legend toggles / data tables, opt-in sortable tables, print styles
- Charts
  - Every `chart_*.py` and `plot_market_sentiment_history.py` call `chart_data.save_chart_data(png_path, data)`
    - Writes a `.chart.json` sidecar next to each PNG (schemas in `chart_data.py`)
  - The HTML draws from the sidecar; it falls back to the embedded PNG when none exists
    - Income-statement flow, balance-sheet composition and Buffett charts have no sidecar
  - Colors follow the categorical palette in `report.css`
  - Every bar and line point carries a value label like the PNGs
    - Labels turn vertical when bars are narrow
    - Dense daily lines label a thinned set, or only end values when there are several series
  - The only second y-axis is a bar chart's `overlay` (the income trend's share price, matching the .docx)
  - The multiples chart puts all three multiples on one axis

### `digest.py` — compact, pre-computed, source-labeled JSON digest
- Usage: `digest.py TICKER SECTION` (so skills don't read raw JSON or do arithmetic by hand)
- Sections
  - `cash_flow`, `income_statement`
  - `balance_sheet` — with `data_flags` for an EDGAR `Total Debt` that is missing or under half of Yahoo's, negative equity, temporary equity
  - `technical` — MAs, slopes, crosses, returns vs SPY, RSI, 52-week range (downloads SPY)
  - `metrics` — `compute_metrics()` with source labels

### `assemble_package.py` — Word package merge
- Usage: `assemble_package.py TICKER YYYYMMDD`
- Merges the deep-research note and the 8 component `.docx` files into one package
  - Bookmarked appendix headings on new pages, linked appendix index, "Page X of Y" footers
- Edit this script, not the skill, to change the merge
- Only relevant when Word output was requested

### `doc_utils.py` — shared python-docx helpers
- Provides
  - `setup_document(doc)` / `apply_house_style(doc)` (landscape, narrow margins, Arial 10pt, centered tables)
  - `autofit_table(table)`, `add_table_borders(table)`, `set_row_font_size(row, size=10)`
  - `add_footnote(doc)`, `fmt_value(v, prefix='$')`
  - `add_source_note(paragraph_or_cell, source)` (per-figure source citations)
- Used by `report_renderer.py`, `assemble_package.py` and any one-off script
- Add new helpers needed by multiple skills here, not inline in each skill

## Tickers

- Edit `tickers.txt` to add/remove tickers (one per line, `#` for comments)
- Currently tracking: AMD, AVGO, COHR, INTC, LITE, MU, MRVL, NVDA, QCOM

## Skill Details

- Overview, workflow stages and the outputs table are at the top of this file
- Below: how each skill behaves and what to keep consistent when editing it

### Stage 1 — Market Conditions
- **`/market_sentiment_analysis`**
  - Scores investor sentiment across 7 indicators: VIX, CNN F&G, put/call, breadth, HY OAS, Shiller CAPE, Buffett Indicator
  - Applies a forward-looking **Macro & Policy Overlay**
    - Factors: Fed commentary, rate guidance vs market-implied path, US fiscal deficit/issuance, Treasury yields
    - Each rated Tailwind / Neutral / Headwind for the next 3–6 months
    - Can cap or boost the final posture but does not enter the composite score
  - Applies a **Market Leverage (margin debt) analysis**
    - Level, margin/GDP vs the 2000/2007/2021 peaks, YoY growth vs historical crash clusters
    - Rated Low / Elevated / Critical
  - Runs `plot_market_sentiment_history.py` for 5-year charts and embeds them in the report
  - Overall Market Opinion is the closing section; saves a combined dashboard PNG
  - On completion, prompts the user to kick off `/emerging_industry_trend`

### Stage 2 — Theme Discovery
- **`/theme_discovery_scanner`** — the Stage 2 entry point
  - Systematic five-channel scan: capital flows, talent migration, incumbents' fear, science, cost curves
  - *Discovers* pre-consensus candidate themes and maintains a ranked watchlist
  - Runs *before* `/emerging_industry_trend`
  - Use when the user has no specific theme ("what's emerging right now", "what should I be watching", "scan for new opportunities", "build a theme watchlist")
  - Each finding must pass a three-part filter: specificity, pre-consensus, public-market path
  - Candidates with 2+ convergence signals are flagged as **promotion calls** handing off to `/emerging_industry_trend`
  - Runs standalone (full ad-hoc scan) or with a channel/sector hint; offers to promote a candidate on completion
- **`/emerging_industry_trend`**
  - Scans for live bottleneck signals before the market prices them in
  - Produces signal scorecard, value chain map, bottleneck analysis and positioning
  - Use before `/industry_trend_analysis` to surface *what* to research; prompts the user to kick off `/industry_trend_analysis` on completion
  - **Accepts a ticker** (e.g. `/emerging_industry_trend NVTS`)
    - Detects the ticker via `WebSearch`, maps it to its industry theme, states the mapping explicitly, then runs on that theme
    - The ticker's company appears in the value chain with its peers, with no special focus
    - Output filename uses the derived theme slug, never the ticker (e.g. `gan_sic_wbg`, not `nvts`)
- **`/industry_trend_analysis`**
  - Maps a known macro theme across its full value chain
    - Layers: infrastructure, enablers, integrators, applications, adjacent beneficiaries, bottlenecks
    - Output: thesis, value chain tables, TAM expansion analysis, stock shortlist, risks
  - **Also accepts a ticker** with the same mapping logic; the title reflects the derived theme with a "Triggered by: [TICKER]" subtitle
  - **Three-part framework**
    - Part 1: 5 convergence signals (entry)
    - Part 2: 6-layer value chain map
    - Part 3 / output Section 6: **Peak & Reversal Watch** (exit)
  - Part 3 scores 6 exhaustion signals (mirror of the entry signals)
    - Signal inversion; supply catch-up/capacity overshoot; valuation & crowding extremes; unit-economics erosion; demand-side funding stress; macro/policy regime shift
    - 2+ firing is the warning threshold
    - Renders pre-committed tripwires, a dated watch calendar, a false-alarm test (structural vs cyclical) and the closest historical analogue
  - Section 6 is **mandatory in every run**, including at 5/5 convergence
  - Consistency rules when editing
    - The peak verdict must reconcile with the Section 2 cycle stage
    - Section 5 layer weightings must square with the peak verdict
    - Section 6a's status colors are deliberately **inverted** versus Section 2 (a firing signal there is bad news)
  - Output has 7 sections; Key Diligence Questions is Section 7
- **`/industry_deep_dive`**
  - Analyzes the structural mechanics of an industry: Porter's Five Forces, business model economics, competitive landscape, barriers to entry
  - Use to understand *how* an industry works, not just which stocks benefit
  - Accepts a theme name or a ticker
- **`/ai_company_deep_dive`**
  - Multi-dimensional deep dive on a ticker with AI exposure
    - Classifies its position in the AI stack, scores chokepoint strength, analyzes revenue quality and moat
    - Builds a 3-scenario investment thesis; explicitly flags names where the AI narrative isn't supported by the data
  - Always re-fetches fresh data via `fetch_all()` before reading JSON
  - Output titled "{TICKER} — Company Deep Dive"
- **`/multibagger_screener`**
  - Idea-generation funnel (not a single-name analysis) for stocks with 5x/10x/100x potential
  - Screens a theme-driven or quality-screen-driven hunting ground against multi-bagger base rates
    - Small, long holding period, painful drawdowns, twin-engined growth + multiple expansion, under-covered
  - Output: scored 3–7 name shortlist with hooks and DNA scorecards
  - Issues no Buy/Hold/Sell calls; hands names to `/single_stock_quick_research` or `/single_stock_deep_research`
  - Runs standalone or chains from `/industry_trend_analysis` / `/emerging_industry_trend`

### Stage 3 — Quick Filter
- **`/quick_stock_metrics`**
  - With no args, reads `tickers.txt`
  - Always re-fetches fresh data via `fetch_all()` before computing, even if JSON exists
  - Writes the Excel workbook (Summary sheet = screen read) and a `quick_stock_metrics_YYYYMMDD.html` next to it

### Stage 4 — Individual Stock Analysis
- **Component analyses** (all take a TICKER)
  - `/balance_sheet_analysis` includes an **Off-Balance-Sheet (OBS) Analysis**
    - 7-category scored checklist (leases, SPEs/VIEs, guarantees, JV/equity-method, pensions, purchase obligations, SBC dilution; 0–2 each, total /14)
    - Plus an OBS-adjusted vs reported leverage table
    - SEC EDGAR JSON has no footnote data, so it is sourced from 10-K/10-Q footnotes via `WebSearch`, cited by filing and date
  - `/income_statement_analysis` also covers growth & profitability (the former `/growth_and_profitability_analysis` was merged in)
    - Latest-quarter YoY snapshot
    - A **drivers section**: sourced explanations of what moved revenue, gross profit, operating income and net income (press release / MD&A / call), plus revenue vs pre-print consensus and guidance
    - Annual (5 FYs + TTM + consensus) and quarterly (8 quarters + up to 4 consensus) trend charts with matching tables
    - Rule of 40
    - A **Consensus Outlook** for the next 2–3 fiscal years (revenue, margins, EPS, analyst count) from WebSearch; out-years with no coverage are N/A, never extrapolated
  - `/technical_analysis`
    - **Moving Averages — Distance from Spot**: 20/50/100/200-day levels, % distance, slope, MA stack, crosses
    - **Price Momentum — Near-Term vs Mid-Term**: 1W–12M returns vs the S&P 500, aligned/diverging call
    - MAs and returns come from `_price_history.json`, not `_quick_metrics.json`
- **`/single_stock_deep_research`**
  - Always re-fetches fresh data via `fetch_all()`
  - Re-runs all 8 component analyses in sequence (including `/leadership_analysis`; output prefixes 1–8)
  - Synthesizes a 2–3 page hedge-fund research note (conviction score + LONG/SHORT/PASS with price target)
  - The note's HTML page is the hub linking the 8 component pages
  - Assembles the single `_stock_deep_research_` Word package (`assemble_package.py`) only when Word is requested
- **`/single_stock_quick_research`**
  - Lighter, self-contained initiation note across seven pillars: business, financial health, valuation, news/catalysts, risk, business potential, synthesis
  - Re-fetches data via `get_financial_data.py`, then uses `WebSearch` for peer comps, analyst targets and news
  - Use for quick coverage where the full 9-analysis suite is overkill
  - Default skill for "what do you think of $TICKER" or "should I buy X"
- **`/earnings_report_analyzer`**
  - Scores one quarter's report and call across 7 dimensions, each −2 to +2
    - Headline quality, margin trajectory, growth durability, balance sheet/cash flow quality, management commentary shift, headwinds/red flags, valuation reality check
    - Net score classifies the quarter from "Strong quality beat" to "Red flag quarter"
  - Re-fetches JSON via `get_financial_data.py` and reuses `chart_income_statement.py` for charts
  - Uses `WebSearch` for the press release, call transcript and prior guidance
  - Use when the ask is about one specific print, not a full initiation note

### Common behaviors
- Skills read local JSON from `Outputs/` first, run `get_financial_data.py` if missing, then supplement with `WebSearch` (analyst estimates, guidance, N/A values)
- Each analysis skill
  - Runs its `chart_*.py` (PNGs + `.chart.json` sidecars)
  - Writes a JSON report spec and runs `report_renderer.py`
  - Produces the interactive `.html` (and a `.docx` if requested)
- Open `Outputs/index.html` to browse everything
- All skills except `/quick_stock_metrics` require a TICKER or THEME argument

## Hedge-Fund House Style

- All skills are written for a **buy-side portfolio manager (PM)**, not a sell-side client
- When editing or adding a skill, conform to the points below
- **Persona**
  - A buy-side analyst at a hedge fund writing for the PM
  - Thesis-first, directional, opinionated
  - Lead each section with the conclusion ("so what for the long/short")
  - No balanced sell-side hedging: take a side and defend it with numbers
- **Verdict — three templates by skill type**
  - **Full-call skills** (`single_stock_deep_research`, `ai_company_deep_dive`, `valuation_analysis`, `technical_analysis`): a **Verdict** block with
    - Directional bias (**LONG / SHORT / PASS**) and **Conviction X/10**
    - Current price, **12-month price target (+%)**, **stop / invalidation (−%)**
    - **Risk/reward ratio** and **sizing** (Core / Starter / Tactical / Avoid)
  - **Component skills** (`business_overview`, `leadership`, `income_statement`, `balance_sheet`, `cash_flow`, `business_potential`): a **Read-Through to the Call** block with
    - **Signal** (BULLISH / NEUTRAL / BEARISH for the thesis) and **dimension conviction X/10**
    - A one-line "so what" for the long/short
    - A one-line "what flips it"
  - **Theme/macro skills** (`emerging_industry_trend`, `industry_trend_analysis`, `industry_deep_dive`, `market_sentiment_analysis`): a directional **posture** call
    - Themes: conviction X/10 plus how to express it (long basket / pair trade / underweight)
    - Market sentiment: Risk-On / Neutral / Risk-Off net-exposure posture with conviction X/10
- **Conviction scale (X/10)**
  - 9–10 highest-conviction book position · 7–8 high · 5–6 moderate/starter · 3–4 low/watchlist · 1–2 avoid or short candidate
  - Replaces the old X/5 "Rating" blocks: no skill should emit an "Overall Rating X/5"
- **Variant View — mandatory in every note**
  - A "Variant View — Consensus vs. Our Read" section
  - A 3-column table: debate | consensus / sell-side view | our differentiated read with the number behind it
  - Followed by a one-line **"The edge:"** bullet naming what the market is mispricing and why we're right
  - Non-negotiable: this is the buy-side value-add
- **Word rendering**
  - The Verdict / Read-Through block is bold
  - Full-call verdicts use a colored Heading-1-style line: green `007000` for LONG / Risk-On, red `C00000` for SHORT / Risk-Off, neutral for PASS
  - The Variant View table follows the standard table rules below

## Word Document Generation

- Skills no longer write python-docx code
  - `report_renderer.py` and `doc_utils.py` implement these rules
  - They matter when editing the renderer, `assemble_package.py` or a one-off script
- **Tables**
  - Always initialize with `rows=1` (header only), then `table.add_row()` for each data row
    - Never use `rows=1+len(data)` upfront: it creates blank rows between the header and data
  - Call `autofit_table(table)` then `add_table_borders(table)` **after** all rows are added
    - Never at table creation time: rows added later won't inherit the settings
    - `autofit_table`
      - Sets `tblW`/`tblLayout` to autofit and strips fixed `w:tcW` cell widths
      - Centers the table on the page
      - Never use `table.columns[i].width` or fixed widths; don't set `table.alignment` yourself
      - `apply_house_style()` (run by `add_footnote()`) re-centers every table as a backstop
    - `add_table_borders`
      - Thin single border (`sz=4`, `val="single"`, `color="000000"`) on all four sides plus inner dividers (`insideH`/`insideV`) via `w:tcBorders`
  - All non-header cell text is size 10 Arial
    - Call `set_row_font_size(row)` on every data row right after `table.add_row()`
    - Do **not** call it on the header row
  - **Never place two tables back to back**
    - Word merges adjacent tables and the columns collapse
    - `autofit_table()` inserts a spacer paragraph automatically; still put a heading, caption or source line between tables
- **Imports in generated scripts**
  - Scripts are saved under `Outputs/{TICKER}/` but run from the project root
    ```python
    import sys; sys.path.insert(0, '.')
    from doc_utils import setup_document, autofit_table, add_table_borders, set_row_font_size, add_footnote, fmt_value
    ```
  - The `sys.path.insert(0, '.')` is required
- **Formatting values**
  - Always use `fmt_value(v)` for dollar amounts in Word table cells
    - Never hardcode `/ 1e9` or append `"B"`
    - Auto-scales: ≥$1B → `$X.XXB`, ≥$1M → `$X.XM`, ≥$1K → `$X.XK`, else raw dollars
    - Pass `prefix=''` for non-dollar values
  - `smart_scale(values)` is defined locally in each `chart_*.py` (not in `doc_utils`)
    - Returns `(divisor, axis_label, suffix)` to pick a shared Y-axis scale
    - Copy an existing implementation when writing a new chart script
- **Apostrophe pitfall in generated Python**
  - Use double-quoted strings for literals containing apostrophes (`"Tesla's"`)
  - Single-quoted strings with an apostrophe raise `SyntaxError: unterminated string literal`
  - The most common bug in skill-generated `generate_*.py` scripts
- **Footnote:** every skill calls `add_footnote(doc)` immediately before `doc.save(...)` (standard AI-generated disclaimer and "not investment advice" notice)
- **Source citations: every quantitative figure must cite where it came from**
  - Sources: SEC EDGAR, Yahoo Finance, a hybrid of both, or a WebSearch source
  - Figures from `compute_metrics()`
    - Call with `with_sources=True` for the per-metric label (`SRC_SEC`, `SRC_YAHOO`, `SRC_HYBRID`, `SRC_COMPUTED`, `SRC_NA`)
    - Read the label; never assume it from the metric name
    - Cite with `add_source_note()` inline, or as a trailing small-print line under a snapshot table
  - Figures read directly from JSON
    - Statements → "SEC EDGAR"; quick_metrics / price_history → "Yahoo Finance"
  - Figures from `WebSearch` (estimates, guidance, news, peer comps)
    - Cite the source name/publication and date
  - Reference implementation: `quick_stock_metrics.py`'s Excel output
    - Visible "Source" column on ticker sheets
    - Hover-note per cell plus a legend on the Comparison sheet
    - Every value cell also carries the hover-note as the literal footnote
- **House format**
  - Landscape Letter (11" × 8.5"), 0.5" margins on all sides, Arial throughout, 10pt for all text except headings
  - Call `setup_document(doc)` right after `doc = Document()`
    ```python
    setup_document(doc)  # landscape Letter, 0.5" margins, Arial 10pt body text
    ```
  - Don't set explicit run sizes on body text, table cells, citations or captions
  - `add_footnote(doc)` re-applies the format via `apply_house_style(doc)`
    - Forces any explicit non-heading run size below 14pt down to 10pt, so a stray `Pt(12)` can't break the style
  - Embed full-width charts at `width=Inches(9.5)` (`doc_utils.CHART_WIDTH`)

## External Data Sources

### FRED (St. Louis Fed)
- Fetch URL: `https://fred.stlouisfed.org/graph/fredgraph.csv?id={SERIES_ID}`
- CSV format
  - First row is the header
  - Some responses prepend a disclaimer line: find the row starting with `DATE` before `pd.read_csv`
- `BAMLH0A0HYM2` (ICE BofA HY OAS)
  - Values are in **percentage points** (`2.78` = 278 bps)
  - Always multiply by 100 before plotting or comparing against bps thresholds
- `WILL5000IND` / `WILL5000INDFC` (Wilshire 5000)
  - **Removed from FRED in June 2024**
  - Use `^FTW5000` from yfinance, falling back to `^W5000` (the sentiment script does this automatically)
- Reliability
  - FRED occasionally rate-limits or times out
  - The HY OAS and GDP fetches are the most reliable
  - Retry with a 60-second timeout before giving up

### Yahoo Finance (yfinance)
- `^VIX`, `^SKEW`, `RSP`, `SPY` work reliably
- `^FTW5000` can return no data; `^W5000` is the working Wilshire 5000 series
- `^CPCE` / `^CPC` (CBOE put/call) are not available: use `^SKEW` as the put-demand proxy
- `yf.download()` returns a MultiIndex with `progress=False`: call `.squeeze()` on the `Close` column to get a plain Series

### CNN Fear & Greed
- Endpoint: `https://production.dataviz.cnn.io/index/fearandgreed/graphdata`
  - Send a browser-like `User-Agent` and a `Referer: https://www.cnn.com/markets/fear-and-greed` header; some requests are rejected without them
- Response JSON: `data.fear_and_greed_historical.data`
  - Each element has `x` (ms timestamp) and `y` (score 0–100)
- Returns only the ~250 most recent days, not a full 5-year history

### CBOE Put/Call CSV
- Available at `https://cdn.cboe.com/resources/options/volume_and_call_put_ratios/equitypc.csv`
- Covers **November 2006 through October 2019 only**: not usable for recent 5-year charts
- Use the CBOE SKEW Index (`^SKEW` via yfinance) as the substitute

### `pandas_datareader`
- Incompatible with Python 3.14+ (imports `distutils`, removed in 3.12)
- Do not use it here; fetch FRED data directly via `requests`

### `references/` directory
- `references/scoring-tables.md`
  - Per-indicator 0–100 conversion bands, composite weights (credit heaviest at 20%), composite zone labels for `/market_sentiment_analysis`
  - If an indicator is unavailable, drop it and renormalize the weights
- `references/bubble-framework.md`
  - The six bubble warning conditions, the conditions-firing → Low/Moderate/Elevated/Extreme mapping, historical analogues
- Both are read by `/market_sentiment_analysis` Steps 2–3; keep thresholds here and in the skill's inline summary consistent
- `references/data-layer.md`
  - Full mechanics of `sec_edgar_data.py` (tag selection, discrete-quarter derivation, backfills, stale-item dropping, TTM anchoring)
  - And `quick_stock_metrics.py` (sourcing rules per metric, unit traps, the `METRICS` contract)
  - CLAUDE.md keeps the summary and traps; read this before editing either module or debugging a statement number
- `references/report-spec.md`
  - Skill-facing rules for writing a report spec (blocks, output-format rule, market/theme report conventions, final reply)
- `references/reit-framework.md`
  - REIT detection
    - `industry` starts with `REIT` or `sector` = `Real Estate`
    - Mortgage REITs are excluded
  - Generic-to-REIT metric substitutions
    - AFFO/FFO for EPS, P/AFFO, AFFO payout, net debt/EBITDAre, dividend-yield spread to the 10-year, implied cap rate/NAV, dividend discount model
  - Data-source caveats: SEC EDGAR is GAAP-only and often lacks Total Debt/capex/dividend lines for REITs
  - The unadjusted-price rule for dividend payers
  - Every single-stock skill carries a short `REIT HANDLING` block pointing here
    - `business_overview`, `leadership`, `income_statement`, `balance_sheet`, `cash_flow`, `business_potential`, `valuation`, `technical`, `single_stock_deep_research`, `single_stock_quick_research`, `earnings_report_analyzer`, `ai_company_deep_dive`, `quick_stock_metrics`
    - The block applies only when the company is a REIT; keep it and the reference consistent when editing either

## Adding a New Skill

1. Create `.claude/commands/{skill_name}.md`
   - Write it as instructions Claude follows at execution time, not Python code
2. If it generates charts for a single ticker
   - Add `chart_{name}.py` at the project root (reads JSON from `Outputs/{TICKER}/`, saves PNG to the same folder)
   - Have it call `chart_data.save_chart_data()` next to each PNG so the HTML is interactive
3. If it needs statement figures
   - Add a `digest.py` section instead of telling the skill to read raw JSON
4. To produce a report
   - Instruct the skill to write a JSON spec and run `report_renderer.py`
   - Point it at `references/report-spec.md` and list only the skill's own placement rules (which chart goes where, which table is sortable, which cells get fills)
   - Never instruct a skill to write a python-docx script
5. Add it to `STAGES` in `report_renderer.py` if it belongs in Stage 1–3 of the library
6. Save ad-hoc one-off Python scripts to `Outputs/{TICKER}/`, not the project root

## Outputs Directory

- **Ticker-specific files** → `Outputs/{TICKER}/`
  - JSON, PNG + `.chart.json`, HTML (and Word if requested), `_spec.json` / `_summary.json`
  - Created automatically by `get_financial_data.py` and each analysis skill
- **Cross-ticker files** → `Outputs/` root
  - Excel and market/theme reports (e.g. `quick_stock_metrics_YYYYMMDD.xlsx` / `.html`)
  - `Outputs/index.html` is the library page over every HTML report
- **Caching**
  - JSON is the persistent data cache: delete and re-fetch if stale
  - HTML/Word/PNG files are overwritten on each run
- **Report specs (`*_spec.json`)** are the editable source of each report
  - Fix a typo in the spec and re-run `report_renderer.py` instead of regenerating the analysis
- Older `generate_*.py` / `assemble_*.py` scripts in `Outputs/` are leftovers from before the renderer: safe to delete
