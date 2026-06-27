# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Environment

Always use the project's virtual environment:
```
.venv/Scripts/python   # run scripts
.venv/Scripts/pip      # install packages
```

Key dependencies: `yfinance`, `openpyxl`, `python-docx`, `matplotlib`, `numpy`.

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
- `compute_metrics(ticker)`, `_short_comment(key, val, metrics)`, `METRICS`, and `color_current_price(metrics)` are imported by the `/single_stock_deep_research` skill's generated Word scripts — treat these as a shared library, not just a CLI script

**`chart_*.py`** — standalone chart generators (one per analysis domain)
- Scripts: `chart_income_statement.py`, `chart_balance_sheet.py`, `chart_cash_flow.py`, `chart_growth_profitability.py`, `chart_valuation.py`, `chart_technical.py`
- Each takes a single `TICKER` positional argument and saves PNG(s) to `Outputs/{TICKER}/`; e.g. `.venv/Scripts/python chart_technical.py NVDA`
- Skills call these scripts rather than generating matplotlib code inline; if a chart needs updating, edit the corresponding `chart_*.py`
- Each script reads its required JSON files from `Outputs/{TICKER}/` directly — run `yahoo_finance_data.py` first if JSON is missing

**`plot_market_sentiment_history.py`** — persistent market sentiment chart generator
- Fetches 5-year time-series data for all 7 sentiment indicators and saves PNGs to `Outputs/`
- Run from the project root: `.venv/Scripts/python plot_market_sentiment_history.py`
- Unlike the ephemeral `generate_*.py` / `assemble_*.py` scripts in `Outputs/`, this lives at the project root and is tracked in git
- Update the `END` date constant at the top before each run
- **External data source gotchas baked into this script** (see also the External Data Sources section below)

**`doc_utils.py`** — shared python-docx helpers
- Provides `autofit_table(table)`, `add_table_borders(table)`, `set_row_font_size(row, size=12)`, `add_footnote(doc)`, and `fmt_value(v, prefix='$')`
- All skill-generated Word scripts import from here; see the Word Document Generation section for the required import pattern
- When adding a new helper needed by multiple skills, add it here rather than inline in each skill

## Tickers

Edit `tickers.txt` to add/remove tickers (one per line, `#` for comments). Currently tracking: ABBV, CLX, ES, JNJ, KMB, KVUE, MCD, O, PG, SJM.

## Slash Commands (Skills)

The intended workflow runs in four stages:

**Stage 1 — Market Conditions:** Assess broad market sentiment and risk before deploying capital.

**Stage 2 — Theme Discovery:** Identify the value chain for a macro trend and surface candidate stocks at each layer.

**Stage 3 — Quick Filter:** Screen candidates on financial quality before committing to deep research.

**Stage 4 — Individual Stock Analysis:** Deep-dive on specific names across all dimensions, culminating in a research note.

| Stage | Skill | Argument | Output |
|---|---|---|---|
| 1 | `/market_sentiment_analysis` | _(none)_ | Word: `Outputs/market_sentiment_{YYYYMMDD}.docx` + 7 PNGs + dashboard PNG |
| 2 | `/emerging_industry_trend` | THEME, TICKER, or _(none)_ | Word: `Outputs/emerging_industry_trends_{theme}_{YYYYMMDD}.docx` |
| 2 | `/industry_trend_analysis` | THEME or TICKER | Word: `Outputs/industry_trend_analysis_{theme}_{YYYYMMDD}.docx` |
| 2 | `/industry_deep_dive` | THEME or TICKER | Word: `Outputs/industry_deep_dive_{theme}_{YYYYMMDD}.docx` |
| 2 | `/ai_company_deep_dive` | TICKER | Word: `Outputs/{TICKER}/{ticker}_company_deep_dive_{YYYYMMDD}.docx` |
| 3 | `/key_stock_metrics` | _(none — reads `tickers.txt`)_ | Excel: `Outputs/key_stock_metrics_YYYYMMDD.xlsx` |
| 4 | `/business_overview_analysis` | TICKER | Word: `Outputs/{TICKER}/1_{ticker}_business_overview_analysis.docx` |
| 4 | `/leadership_analysis` | TICKER | Word: `Outputs/{TICKER}/2_{ticker}_leadership_analysis.docx` |
| 4 | `/income_statement_analysis` | TICKER | Word: `Outputs/{TICKER}/3_{ticker}_income_statement_analysis.docx` |
| 4 | `/balance_sheet_analysis` | TICKER | Word: `Outputs/{TICKER}/4_{ticker}_balance_sheet_analysis.docx` |
| 4 | `/cash_flow_analysis` | TICKER | Word: `Outputs/{TICKER}/5_{ticker}_cash_flow_analysis.docx` |
| 4 | `/growth_and_profitability_analysis` | TICKER | Word: `Outputs/{TICKER}/6_{ticker}_growth_and_profitability_analysis.docx` |
| 4 | `/business_potential_analysis` | TICKER | Word: `Outputs/{TICKER}/7_{ticker}_business_potential_analysis.docx` |
| 4 | `/valuation_analysis` | TICKER | Word: `Outputs/{TICKER}/8_{ticker}_valuation_analysis.docx` |
| 4 | `/technical_analysis` | TICKER | Word: `Outputs/{TICKER}/9_{ticker}_technical_analysis.docx` |
| 4 | `/single_stock_deep_research` | TICKER | Word: `Outputs/{TICKER}/{ticker}_stock_deep_research_YYYYMMDD.docx` (package) + `{ticker}_stock_deep_research_notes_YYYYMMDD.docx` (note) |
| 4 | `/single_stock_quick_research` | TICKER | Word: `Outputs/{TICKER}/{ticker}_stock_quick_research_YYYYMMDD.docx` |

- `/market_sentiment_analysis` scores investor sentiment across 7 indicators (VIX, CNN F&G, put/call, breadth, HY OAS, Shiller CAPE, Buffett Indicator), runs `plot_market_sentiment_history.py` to generate 5-year time-series charts, embeds them in the Word report, and saves a combined dashboard PNG; on completion it prompts the user to kick off `/emerging_industry_trend`
- `/emerging_industry_trend` scans for live bottleneck signals before the market prices them in — produces a Word doc with signal scorecard, value chain map, bottleneck analysis, and positioning; use it before `/industry_trend_analysis` when you want to surface *what* to research, not just map a known theme; on completion it prompts the user to kick off `/industry_trend_analysis`. **Accepts a ticker as argument** (e.g. `/emerging_industry_trend NVTS`): the skill detects the ticker via `WebSearch`, maps it to its industry theme, states the mapping explicitly, then runs the full analysis on that theme — the ticker's company appears in the value chain map alongside all peers but receives no special focus. The output filename always uses the derived theme slug, never the raw ticker (e.g. `gan_sic_wbg`, not `nvts`).
- `/industry_trend_analysis` maps a known macro theme across its full value chain — identifies investable stocks at each layer (infrastructure, enablers, integrators, applications, adjacent beneficiaries, bottlenecks) and produces a Word doc with thesis, value chain table, TAM expansion analysis, stock shortlist, and risks. **Also accepts a ticker as argument** with the same ticker-to-theme mapping logic as `/emerging_industry_trend`; the document title reflects the derived theme with a "Triggered by: [TICKER]" subtitle when a ticker was the input.
- `/industry_deep_dive` analyzes the structural mechanics of an industry (Porter's Five Forces, business model economics, competitive landscape, barriers to entry) — use it when you want to understand *how* an industry works, not just which stocks benefit; accepts either a theme name or a ticker symbol
- `/ai_company_deep_dive` conducts a rigorous multi-dimensional deep dive on a specific ticker with AI exposure — classifies its position in the AI stack, scores its chokepoint strength, analyzes revenue quality and moat, and builds a 3-scenario investment thesis; always re-fetches fresh Yahoo Finance data via `fetch_all()` before reading JSON; explicitly flags names where the AI narrative is not supported by the data; output titled "{TICKER} — Company Deep Dive"
- `/key_stock_metrics` with no args reads from `tickers.txt`; all other skills require a TICKER or THEME argument
- `/key_stock_metrics` always re-fetches fresh data via `fetch_all()` before computing metrics, even if JSON files already exist
- Skills read local JSON from `Outputs/` first, run `yahoo_finance_data.py` if missing, then supplement with `WebSearch` for analyst estimates, guidance, and any N/A values
- Each analysis skill generates matplotlib charts (saved as PNGs to `Outputs/`), then writes and executes a `python-docx` script inline to embed the charts and produce the `.docx`
- `/single_stock_deep_research` always re-fetches fresh Yahoo Finance data and re-runs all 9 individual analyses in sequence (including `/leadership_analysis`), then synthesizes a 2–3 page hedge-fund research note (conviction score + LONG/SHORT/PASS with price target), and finally assembles all documents into a single `_stock_deep_research_` Word file with page numbers
- `/single_stock_quick_research` is a lighter-weight, self-contained single-stock initiation note — works through six pillars (business, financial health, valuation, news/catalysts, risk, synthesis); re-fetches Yahoo Finance data first, then supplements with `WebSearch` for peer comps, analyst targets, and news; produces a single polished `.docx`; use it for quick coverage initiation where the full 9-analysis suite is overkill; also serves as the default skill when the user asks "what do you think of $TICKER" or "should I buy X"

## Hedge-Fund House Style

Every analysis skill is written for a **buy-side portfolio manager (PM)** to digest — not a sell-side client. All skills share one consistent house style. When editing an existing skill or adding a new one, conform to this:

- **Persona:** the author is a **buy-side analyst at a hedge fund** writing for the PM. Thesis-first, directional, and opinionated. Lead each section with the conclusion ("so what for the long/short"), not a description of what the section covers. No balanced sell-side hedging — take a side and defend it with numbers.
- **Verdict — two templates depending on skill type:**
  - **Full-call skills** (`single_stock_deep_research`, `ai_company_deep_dive`, `valuation_analysis`, `technical_analysis`) render a **Verdict** block with: directional bias (**LONG / SHORT / PASS**), a **Conviction score X/10**, current price, **12-month price target (+%)**, **stop / invalidation level (−%)**, **risk/reward ratio**, and **sizing** (Core / Starter / Tactical / Avoid).
  - **Component skills** (`business_overview`, `leadership`, `income_statement`, `balance_sheet`, `cash_flow`, `growth_and_profitability`, `business_potential`) render a **Read-Through to the Call** block: a directional **Signal (BULLISH / NEUTRAL / BEARISH for the thesis)**, a **dimension conviction X/10**, a one-line "so what" for the long/short, and a one-line "what flips it."
  - **Theme/macro skills** (`emerging_industry_trend`, `industry_trend_analysis`, `industry_deep_dive`, `market_sentiment_analysis`) render a directional **posture** call (e.g., theme conviction X/10 with how to express it — long basket / pair trade / underweight; or for market sentiment a Risk-On / Neutral / Risk-Off net-exposure posture with conviction X/10).
- **Conviction scale (X/10):** 9–10 = highest-conviction book position · 7–8 = high · 5–6 = moderate / starter · 3–4 = low / watchlist · 1–2 = avoid or short candidate. This **replaces the old X/5 "Rating" blocks** — no skill should still emit an "Overall Rating X/5."
- **Variant View — mandatory in every note.** Every skill must include a **"Variant View — Consensus vs. Our Read"** section: a small 3-column table (debate | consensus / sell-side view | our differentiated read with the number behind it), followed by a one-line **"The edge:"** bullet naming what the market is mispricing and why we think we are right. This is the buy-side value-add and is non-negotiable.
- **Word rendering:** the Verdict / Read-Through block is rendered in bold (full-call verdicts use a colored Heading-1-style line: green `007000` for LONG / Risk-On, red `C00000` for SHORT / Risk-Off, neutral for PASS). The Variant View table follows the standard table rules below.

## Word Document Generation

When writing `python-docx` table code in any skill or script:
- **Always initialize tables with `rows=1`** (header only), then call `table.add_row()` for each data row — do NOT use `rows=1+len(data)` upfront, which creates blank rows between the header and data
- **Every table must call `autofit_table(table)` then `add_table_borders(table)` AFTER all rows are added** — calling before rows are added means new rows won't inherit the settings. Never call them at table creation time; always call them after the last `table.add_row()`.
  - `autofit_table` — sets `tblW`/`tblLayout` to autofit and strips all fixed `w:tcW` cell widths; never use `table.columns[i].width` or any fixed-width assignment
  - `add_table_borders` — applies a thin single border (`sz=4`, `val="single"`, `color="000000"`) to all four sides of every cell via `w:tcBorders`
- **All non-header table cell text must use font size 12.** Call `set_row_font_size(row)` on every data row immediately after `table.add_row()`. Do **not** call it on the header row.
- All helpers live in `doc_utils.py` at the project root — generated scripts import them with:
  ```python
  import sys; sys.path.insert(0, '.')
  from doc_utils import autofit_table, add_table_borders, set_row_font_size, add_footnote, fmt_value
  ```
  The `sys.path.insert(0, '.')` is required because scripts are saved under `Outputs/{TICKER}/` but run from the project root.
- **Always use `fmt_value(v)` from `doc_utils` to format all dollar amounts in Word table cells** — never hardcode `/ 1e9` or append `"B"` manually. `fmt_value` auto-scales: ≥$1B → `$X.XXB`, ≥$1M → `$X.XM`, ≥$1K → `$X.XK`, else raw dollars. Pass `prefix=''` for non-dollar values.
- **`smart_scale(values)` is defined locally in each `chart_*.py`** (not in `doc_utils`). It returns `(divisor, axis_label, suffix)` and is used to pick a shared Y-axis scale for all series on a chart. Copy the existing implementation from any `chart_*.py` when writing a new chart script.
- **Apostrophe pitfall in generated Python scripts:** when writing string literals that contain apostrophes (e.g. `"Tesla's"`, `"Comma.ai's"`), use double-quoted strings — never single-quoted. Single-quoted strings with an apostrophe inside cause `SyntaxError: unterminated string literal` at runtime. This is the most common bug in skill-generated `generate_*.py` scripts.
- **Every skill must call `add_footnote(doc)` immediately before `doc.save(...)`** — this appends the standard AI-generated disclaimer and "not investment advice" notice at the bottom of every Word document.
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

## External Data Sources

Non-obvious facts about external APIs used by the market sentiment charts and skills:

**FRED (St. Louis Fed)**
- Fetch URL: `https://fred.stlouisfed.org/graph/fredgraph.csv?id={SERIES_ID}`
- CSV format: first row is the header; some responses prepend a disclaimer line — find the row starting with `DATE` before passing to `pd.read_csv`
- `BAMLH0A0HYM2` (ICE BofA HY OAS): values are in **percentage points**, not basis points (e.g. `2.78` = 278 bps). Always multiply by 100 before plotting or comparing against bps thresholds
- `WILL5000IND` / `WILL5000INDFC` (Wilshire 5000): **removed from FRED in June 2024** — use `^FTW5000` from yfinance instead
- FRED occasionally rate-limits or times out; the HY OAS and GDP fetches are the most reliable; retry with a 60-second timeout before giving up

**Yahoo Finance (yfinance)**
- `^VIX`, `^SKEW`, `^FTW5000`, `RSP`, `SPY` all work reliably
- `^CPCE` / `^CPC` (CBOE put/call) are not available — use `^SKEW` as the put-demand proxy
- `yf.download()` returns a MultiIndex when `progress=False`; always call `.squeeze()` on the `Close` column to get a plain Series

**CNN Fear & Greed**
- Endpoint: `https://production.dataviz.cnn.io/index/fearandgreed/graphdata`
- Response JSON: `data.fear_and_greed_historical.data` — each element has `x` (ms timestamp) and `y` (score 0–100)
- Returns ~250 most recent days only; not a full 5-year history

**CBOE Put/Call CSV**
- Available at `https://cdn.cboe.com/resources/options/volume_and_call_put_ratios/equitypc.csv`
- The file covers **November 2006 through October 2019 only** — not usable for recent 5-year charts
- Use the CBOE SKEW Index (`^SKEW` via yfinance) as the current-data substitute

**`pandas_datareader`**
- Incompatible with Python 3.14+ (imports `distutils`, which was removed in 3.12). Do not use it in this project; fetch FRED data directly via `requests` instead.

**`references/` directory**
- The files `references/scoring-tables.md` and `references/bubble-framework.md` are referenced in the `/market_sentiment_analysis` skill but **do not exist on disk**. The skill uses inline fallback scoring logic. If you create these files, the skill will read them; until then, scoring tables are embedded in the skill instructions themselves.

## Adding a New Skill

To add a new analysis skill:
1. Create `.claude/commands/{skill_name}.md` — write it as instructions Claude will follow at execution time (not Python code itself)
2. If the skill generates charts for a single ticker, add a `chart_{name}.py` at the project root (reads JSON from `Outputs/{TICKER}/`, saves PNG to same folder). Theme/market-level skills (e.g., `/market_sentiment_analysis`) generate charts inline inside the `generate_*.py` script using `yfinance` + `matplotlib` directly — no separate `chart_*.py` needed.
3. If the skill generates a Word document, instruct it to: run the relevant `chart_*.py` (or generate charts inline) → write a `generate_*.py` script to `Outputs/{TICKER}/` (or `Outputs/` root for non-ticker skills) → execute it → confirm the `.docx` path
4. All generated Word scripts must import helpers from `doc_utils.py` (see Word Document Generation section)
5. Ad-hoc one-off Python scripts should be saved to `Outputs/{TICKER}/`, not the project root

## Outputs Directory

- **Ticker-specific files** (JSON, PNG, Word) → `Outputs/{TICKER}/` (e.g., `Outputs/NVDA/`) — created automatically by `yahoo_finance_data.py` and each analysis skill
- **Cross-ticker files** (Excel) → `Outputs/` root — e.g., `key_stock_metrics_YYYYMMDD.xlsx`
- JSON files are the persistent data cache — delete and re-fetch if data is stale; Word/PNG files are overwritten on each run
- `generate_*.py`, `assemble_*.py`, and `compute_*.py` scripts generated by skills are saved to `Outputs/{TICKER}/` (not the project root) — safe to delete at any time
