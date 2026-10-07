# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Environment

Always use the project's virtual environment:
```
.venv/Scripts/python   # run scripts
.venv/Scripts/pip      # install packages
```

Key dependencies: `yfinance`, `openpyxl`, `python-docx`, `matplotlib`, `numpy`.

There is no test suite, linter, or build step — verification means running the relevant script and inspecting the file it writes to `Outputs/`.

**Prefix every Python invocation that prints to the console with `PYTHONIOENCODING=utf-8`:**
```
PYTHONIOENCODING=utf-8 .venv/Scripts/python quick_stock_metrics.py AAPL
```
The default Windows console codec is cp1252, and much of this project's printed output contains non-Latin-1 characters — `_short_comment()` in `quick_stock_metrics.py` returns benchmark labels like `Oversold (≤30)` and `Very safe (>10×)`, and the skills use `—` and `·` throughout. Without the prefix these raise `UnicodeEncodeError: 'charmap' codec can't encode character` **partway through the output**, so a diagnostic loop prints its first few rows and then dies, which reads like a data problem rather than an encoding one. Writing to files is unaffected; this only bites on stdout.

`Outputs/`, `.venv/`, and `__pycache__/` are gitignored: generated artifacts (JSON, PNG, Word, Excel) are never committed. The tracked surface is the Python libraries at the project root, `.claude/commands/`, `references/`, `tickers.txt`, and this file.

## Project Overview

This is an investment analysis toolkit that fetches financial data from SEC EDGAR and Yahoo Finance and runs structured equity research analyses via Claude Code slash commands (skills).

**Data flow:**
1. `get_financial_data.py` fetches raw data — income statement / balance sheet / cash flow from SEC EDGAR, quote/market data and price history from Yahoo Finance — → saves JSON files to `Outputs/`
2. `quick_stock_metrics.py` reads those JSON files → produces an Excel workbook in `Outputs/`
3. Claude Code skills (`.claude/commands/`) perform web-searched qualitative analysis → produce Word documents in `Outputs/`

## Core Scripts

**`get_financial_data.py`** — the data fetching entry point; skills and scripts should call this, not `yahoo_finance_data.py` or `sec_edgar_data.py` directly
- `fetch_all(tickers, price_history=True)` — fetches all data types for a list of tickers; call this to pre-populate data. **Price history is downloaded once, at the start of a skill run** (5 years of daily closes): skills that read `_price_history.json` (`/technical_analysis`, `/income_statement_analysis`, `/earnings_report_analyzer`, `/quick_stock_metrics`, `/ai_company_deep_dive`, `/single_stock_quick_research`, and `/single_stock_deep_research` via its Step 0) call it with the default; skills that never use it (business overview, leadership, balance sheet, cash flow, business potential, valuation, multibagger) pass `price_history=False`; and subagents spawned by `/single_stock_deep_research` skip the download entirely because the parent already did it. Chart scripts and `compute_metrics()` only read the JSON. Combines `sec_edgar_data.fetch_edgar_statements()` (income statement, balance sheet, cash flow) with `yahoo_finance_data.get_quick_metrics()` and `get_price_history()`. Per-ticker failures are caught and printed, not fatal. TTM computation requires ≥4 quarters of history, so recent IPOs raise `ValueError` and land in the results dict as `{"error": ...}`
- `load_tickers()` — reads `tickers.txt` (ignores `#` comments and blank lines)
- To re-fetch all tickers: `.venv/Scripts/python get_financial_data.py` (reads `tickers.txt`, or pass tickers as args); to force-refresh a single ticker, delete `Outputs/{TICKER}/` then re-run the skill or call `fetch_all([ticker])` from a script

**`sec_edgar_data.py`** — income statement, balance sheet, cash flow fetcher (SEC EDGAR XBRL "company facts" API); used because Yahoo Finance is stale for weeks after an earnings release
- `fetch_edgar_statements(ticker)` saves JSON with Yahoo-style line-item names (`"Total Revenue"`, `"Operating Income"`, …) at the same paths the old Yahoo fetchers used, so `chart_*.py` / `quick_stock_metrics.py` need no field-name changes. Run directly: `.venv/Scripts/python sec_edgar_data.py TICKER`. Every SEC request needs the descriptive `User-Agent` with a contact email (`USER_AGENT`).
- **When numbers look inconsistent (a metric stuck on a stale date, Revenue − Cost ≠ Gross Profit), suspect one of three things before a one-off ticker quirk:** (1) a filer retired/switched an XBRL tag — tag selection is freshness-based (`_extract_tag_series()`), never "first tag in the list"; (2) the filer reports cumulative year-to-date facts — discrete quarters are derived by diffing within a fiscal year, with Q4 = FY total − 9-month YTD; (3) the concept is never tagged at all — the field comes back `{}` or `0`, not wrong-looking.
- **A `0` or empty debt figure on a company you know carries debt is missing data, not deleveraging** (SWKS `Total Debt` = 0 after retiring notes; AKAM leaves debt, PP&E and goodwill untagged). Fall back to `_quick_metrics.json` or the 10-Q, cite the fallback, and distrust any leverage ratio (D/E, net debt/EBITDA) computed from the untagged line. Line items a filer stopped tagging (no successor) are cleared by `_drop_stale_line_items()` rather than left stale.
- Balance sheet also carries `"Temporary Equity"` (so `Assets − Liabilities − Equity` reconciles) and `"Shares Outstanding"` (from the `dei` namespace, in shares, not USD). TTM (`_best_ttm()`) anchors every line item to the same four quarter-end dates.
- **Full mechanics (backfills, stale-item dropping, TTM anchoring, tag examples): `references/data-layer.md`.**

**`yahoo_finance_data.py`** — quote/market data fetching library; retained only for data with no SEC EDGAR equivalent
- `get_quick_metrics()` — market cap, P/E, dividend yield, beta, analyst targets, sector, etc. (the `stock.info` dict)
- `get_price_history(ticker, years=5)` — returns a `{"YYYY-MM-DD": price}` dict; used by technical analysis charts and RSI. **Closes are dividend-adjusted** (yfinance's default `auto_adjust=True`) while `current_price` and the 52-week range from quick metrics are not, so for material dividend payers (yield above ~2%, e.g. REITs) older prices, moving averages and closing highs/lows are understated; the technical skill recomputes from unadjusted closes (`auto_adjust=False`) for those names
- JSON output path: `Outputs/{TICKER}/` (e.g., `Outputs/NVDA/`) — one subfolder per ticker, created automatically
- `{ticker_lower}` means `ticker.lower()` (e.g., `NVDA` → `nvda`); used in all JSON filenames
- JSON filenames written by this module: `{ticker_lower}_quick_metrics.json` and `{ticker_lower}_price_history.json` only. The statement files in the same folder — `{ticker_lower}_balance_sheet_quarterly.json` and `{ticker_lower}_{income_statement|cash_flow_statement}_{quarterly|annual|ttm}.json` — are all written by `sec_edgar_data.py`, not this module
- Do not import this module directly from skills — go through `get_financial_data.py`

**`quick_stock_metrics.py`** — Excel report generator and shared metrics library
- `compute_metrics(ticker, with_sources=True)` returns `(results, sources)`; `sources` labels each metric's *actual* source for that ticker (`SRC_SEC`, `SRC_YAHOO`, `SRC_HYBRID`, `SRC_COMPUTED`, `SRC_NA`) — it can differ by ticker, so read it, never infer it from the key name. Plain `compute_metrics(ticker)` returns just `results`.
- Statement-derived metrics come from the SEC EDGAR JSON, falling back to `_quick_metrics.json`. Trailing P/E and Price/Sales are hybrids (SEC fundamentals × Yahoo price); forward P/E and PEG are Yahoo-only (no SEC path — they need consensus estimates); price, 52-week range, market cap, dividend yield and sector are always Yahoo quote data. RSI is computed from `_price_history.json` (`_calc_rsi()`, Wilder 14-day).
- Imported by `/single_stock_deep_research`'s Word scripts as a shared library: `compute_metrics()`, `_short_comment()`, `METRICS` (22 snake_case keys, render order), `color_current_price()`. Iterate `METRICS` instead of hardcoding keys; ratio-style keys are plain multiples, margin-style keys are decimals needing `×100`; `dividend_yield` is `None` for non-payers while `payout_ratio` is `0.0`; there is no EV/EBITDA key.
- Unit traps: Yahoo `debtToEquity` is already a percentage and the script divides by 100 (don't double-divide); the forward `dividendYield` field can come back as a percentage and is divided by 100 to normalize.
- **A metric can be valid arithmetic and still meaningless** — `de` is `-10.1x` for a company with negative book equity (SMG) and `_short_comment` calls it "Very conservative"; `roe` goes negative on negative equity; `trailing_pe` can diverge from Yahoo's with discontinued operations. Check the balance sheet's sign before repeating a label.
- Output `Outputs/quick_stock_metrics_YYYYMMDD.xlsx` (`Summary` sheet first with the buy-side screen read, then `Comparison` with per-cell hover-note sources and a legend, then per-ticker sheets with a "Source" column). Run: `.venv/Scripts/python quick_stock_metrics.py [TICKER ...]`; then `.venv/Scripts/python quick_stock_metrics.py --summary Outputs/quick_stock_metrics_summary_YYYYMMDD.json` adds the `Summary` sheet (`write_summary_sheet()`) from the screen read the `/quick_stock_metrics` skill writes as JSON. **Full detail: `references/data-layer.md`.**

**`chart_*.py`** — standalone chart generators (one per analysis domain)
- Scripts: `chart_income_statement.py`, `chart_balance_sheet.py`, `chart_cash_flow.py`, `chart_valuation.py`, `chart_technical.py`
- Each takes a single `TICKER` positional argument and saves PNG(s) to `Outputs/{TICKER}/`; e.g. `.venv/Scripts/python chart_technical.py NVDA`
- `chart_income_statement.py` draws an annual trend (last 5 FYs + TTM + consensus FYs) and a quarterly trend (last 8 quarters + up to 4 consensus quarters) as grouped bars of revenue / gross profit / operating income / net income (every bar labeled with amount, YoY and gross/operating/net margin; consensus is revenue-only hatched bars; period-end dates on the x-axis; the share price from `_price_history.json` on a right axis — close on or before each period-end date, including TTM — so periods older than the cached 5-year history get no price point). There are no separate margin charts. Consensus comes from `{ticker_lower}_consensus_estimates.json`, written by `/income_statement_analysis` from WebSearch (not fetched); without it the trends show actuals only. Its `annual_trend_rows()` / `quarterly_trend_rows()` are imported by the skill's Word script to build the matching tables — treat them as shared library functions, like `compute_metrics()`
- `chart_balance_sheet.py` draws a latest-quarter composition stack plus a grouped-bar trend of the last 8 quarters (total assets, equity, liabilities, debt, cash — every bar labeled); `chart_cash_flow.py` draws a latest-quarter OCF→CapEx→FCF waterfall plus a grouped-bar trend of the last 8 quarters (net income, operating cash flow, free cash flow — in that order, every bar labeled, Free CF bars also show FCF ÷ net income). The cash flow JSON has no net income, so the trend takes it from `_income_statement_quarterly.json`
- `chart_technical.py` plots price with the 20/50/100/200-day moving averages (`_ta_price_ma.png`) plus a Wilder RSI chart (`_ta_rsi.png`)
- Skills call these scripts rather than generating matplotlib code inline; if a chart needs updating, edit the corresponding `chart_*.py`
- Each script reads its required JSON files from `Outputs/{TICKER}/` directly — run `get_financial_data.py` first if JSON is missing

**`plot_market_sentiment_history.py`** — persistent market sentiment chart generator
- Fetches 5-year time-series data for the 7 sentiment indicators plus Treasury yields (FRED `DGS10`/`DGS2` with a 10Y−2Y curve panel), the US fiscal picture (FRED `MTSDS133FMS` trailing-12M deficit + `A091RC1Q027SBEA` net interest), and margin debt (FRED `BOGZ1FL663067003Q` quarterly Z.1 margin loans, level + % of GDP) — 10 charts total — and saves PNGs to `Outputs/`
- Run from the project root: `.venv/Scripts/python plot_market_sentiment_history.py`
- Unlike the ephemeral `generate_*.py` / `assemble_*.py` scripts in `Outputs/`, this lives at the project root and is tracked in git
- `END` defaults to today (`datetime.now()`); pass a `YYYY-MM-DD` CLI arg to override for a reproducible historical run — no file edit needed
- `BUFFETT_ANCHOR_VALUE` (top of file) must be updated to the current Buffett Indicator reading (from a web search) before each run — there is no free live API for it, so a stale anchor silently drifts the Buffett chart and current-reading out of date
- **External data source gotchas baked into this script** (see also the External Data Sources section below)

**`report_renderer.py`** — spec-driven report renderer (being rolled out skill by skill; `/cash_flow_analysis` uses it first)
- `report_renderer.py SPEC_JSON` builds both the house-style `.docx` and a self-contained, offline **interactive HTML** twin (same base name) from one JSON content spec (heading / paragraph / bullets / table / chart / source / variant_view / read_through blocks — schema in the module docstring), so skills write content instead of a fresh python-docx script each run. It also writes `{n}_{ticker}_{skill}_summary.json` (signal, conviction, key figures, variant view), the subagent return contract `/single_stock_deep_research` synthesizes from, and rebuilds `Outputs/index.html` (searchable research library; `--index` rebuilds it alone). HTML is for personal use only — no hosting, no CDN: `report_assets/report.css` + `report.js` are inlined (light/dark theme, contents sidebar, SVG charts with hover / legend toggles / data tables, opt-in sortable tables). Add new block types here, not in skill-generated scripts.
- Charts: each `chart_*.py` calls `chart_data.save_chart_data(png_path, data)` to write a `.chart.json` sidecar next to every PNG (bar / line / waterfall schemas in `chart_data.py`); the HTML draws from it and falls back to the embedded PNG when a chart has no sidecar (so far only `chart_cash_flow.py` writes them). Chart colors follow the validated categorical palette in `report.css`; no dual-axis charts in HTML.

**`digest.py`** — `digest.py TICKER SECTION` prints a compact, pre-computed, source-labeled JSON digest of the cached statements (sections: `cash_flow`) so skills don't read raw JSON or do arithmetic by hand; flags an EDGAR `Total Debt` that is missing or under half of Yahoo's.

**`doc_utils.py`** — shared python-docx helpers
- Provides `setup_document(doc)` / `apply_house_style(doc)` (landscape, narrow margins, Arial 10pt, centered tables), `autofit_table(table)`, `add_table_borders(table)`, `set_row_font_size(row, size=10)`, `add_footnote(doc)`, `fmt_value(v, prefix='$')`, and `add_source_note(paragraph_or_cell, source)` (used for the per-figure source citations)
- All skill-generated Word scripts import from here; see the Word Document Generation section for the required import pattern
- When adding a new helper needed by multiple skills, add it here rather than inline in each skill

## Tickers

Edit `tickers.txt` to add/remove tickers (one per line, `#` for comments). Currently tracking: AMD, AVGO, COHR, INTC, LITE, MU, MRVL, NVDA, QCOM.

## Slash Commands (Skills)

The intended workflow runs in four stages:

**Stage 1 — Market Conditions:** Assess broad market sentiment and risk before deploying capital.

**Stage 2 — Theme Discovery:** Identify the value chain for a macro trend and surface candidate stocks at each layer.

**Stage 3 — Quick Filter:** Screen candidates on financial quality before committing to deep research.

**Stage 4 — Individual Stock Analysis:** Deep-dive on specific names across all dimensions, culminating in a research note.

| Stage | Skill | Argument | Output |
|---|---|---|---|
| 1 | `/market_sentiment_analysis` | _(none)_ | Word: `Outputs/market_sentiment_analysis_{YYYYMMDD}.docx` + 10 PNGs + dashboard PNG |
| 2 | `/theme_discovery_scanner` | CHANNEL/SECTOR hint or _(none)_ | Word: `Outputs/theme_discovery_scan_{YYYYMMDD}.docx` |
| 2 | `/emerging_industry_trend` | THEME, TICKER, or _(none)_ | Word: `Outputs/emerging_industry_trends_{theme}_{YYYYMMDD}.docx` |
| 2 | `/industry_trend_analysis` | THEME or TICKER | Word: `Outputs/industry_trend_analysis_{theme}_{YYYYMMDD}.docx` |
| 2 | `/industry_deep_dive` | THEME or TICKER | Word: `Outputs/industry_deep_dive_{theme}_{YYYYMMDD}.docx` |
| 2 | `/ai_company_deep_dive` | TICKER | Word: `Outputs/{TICKER}/{ticker}_company_deep_dive_{YYYYMMDD}.docx` |
| 2 | `/multibagger_screener` | THEME or _(none)_ | Word: `Outputs/multibagger_screener_{theme_or_date}_{YYYYMMDD}.docx` |
| 3 | `/quick_stock_metrics` | _(none — reads `tickers.txt`)_ | Excel: `Outputs/quick_stock_metrics_YYYYMMDD.xlsx` (Summary sheet = screen read) |
| 4 | `/business_overview_analysis` | TICKER | Word: `Outputs/{TICKER}/1_{ticker}_business_overview_analysis.docx` |
| 4 | `/leadership_analysis` | TICKER | Word: `Outputs/{TICKER}/2_{ticker}_leadership_analysis.docx` |
| 4 | `/income_statement_analysis` | TICKER | Word: `Outputs/{TICKER}/3_{ticker}_income_statement_analysis.docx` |
| 4 | `/balance_sheet_analysis` | TICKER | Word: `Outputs/{TICKER}/4_{ticker}_balance_sheet_analysis.docx` |
| 4 | `/cash_flow_analysis` | TICKER | Word: `Outputs/{TICKER}/5_{ticker}_cash_flow_analysis.docx` |
| 4 | `/business_potential_analysis` | TICKER | Word: `Outputs/{TICKER}/6_{ticker}_business_potential_analysis.docx` |
| 4 | `/valuation_analysis` | TICKER | Word: `Outputs/{TICKER}/7_{ticker}_valuation_analysis.docx` |
| 4 | `/technical_analysis` | TICKER | Word: `Outputs/{TICKER}/8_{ticker}_technical_analysis.docx` |
| 4 | `/single_stock_deep_research` | TICKER | Word: `Outputs/{TICKER}/{ticker}_stock_deep_research_YYYYMMDD.docx` (package) + `{ticker}_stock_deep_research_notes_YYYYMMDD.docx` (note) |
| 4 | `/single_stock_quick_research` | TICKER | Word: `Outputs/{TICKER}/{ticker}_stock_quick_research_YYYYMMDD.docx` |
| 4 | `/earnings_report_analyzer` | TICKER | Word: `Outputs/{TICKER}/{ticker}_earnings_analysis_YYYYMMDD.docx` |

- `/market_sentiment_analysis` scores investor sentiment across 7 indicators (VIX, CNN F&G, put/call, breadth, HY OAS, Shiller CAPE, Buffett Indicator), then applies a forward-looking **Macro & Policy Overlay** (Fed commentary, interest-rate guidance vs. market-implied path, US fiscal deficit/issuance, Treasury yields — each rated Tailwind / Neutral / Headwind for the next 3–6 months; the overlay can cap or boost the final posture but does not enter the composite score) and a **Market Leverage (margin debt) analysis** (level, margin/GDP vs. the 2000/2007/2021 peaks, YoY growth vs. historical crash clusters — rated Low / Elevated / Critical), runs `plot_market_sentiment_history.py` to generate 5-year time-series charts, embeds them in the Word report (Overall Market Opinion is the closing section), and saves a combined dashboard PNG; on completion it prompts the user to kick off `/emerging_industry_trend`
- `/theme_discovery_scanner` is the **Stage 2 entry point** — a systematic five-channel scan (capital flows, talent migration, incumbents' fear, science, cost curves) that *discovers* pre-consensus candidate themes and maintains a ranked watchlist, the step that runs *before* `/emerging_industry_trend`; use it when the user has no specific theme in mind ("what's emerging right now", "what should I be watching", "scan for new opportunities", "build a theme watchlist"). Each finding must pass a three-part qualification filter (specificity, pre-consensus, public-market path); candidates showing 2+ convergence signals are flagged as **promotion calls** that hand off to `/emerging_industry_trend`; runs standalone with no argument (full ad-hoc scan) or accepts a channel/sector hint; on completion it offers to promote a candidate into `/emerging_industry_trend`
- `/emerging_industry_trend` scans for live bottleneck signals before the market prices them in — produces a Word doc with signal scorecard, value chain map, bottleneck analysis, and positioning; use it before `/industry_trend_analysis` when you want to surface *what* to research, not just map a known theme; on completion it prompts the user to kick off `/industry_trend_analysis`. **Accepts a ticker as argument** (e.g. `/emerging_industry_trend NVTS`): the skill detects the ticker via `WebSearch`, maps it to its industry theme, states the mapping explicitly, then runs the full analysis on that theme — the ticker's company appears in the value chain map alongside all peers but receives no special focus. The output filename always uses the derived theme slug, never the raw ticker (e.g. `gan_sic_wbg`, not `nvts`).
- `/industry_trend_analysis` maps a known macro theme across its full value chain — identifies investable stocks at each layer (infrastructure, enablers, integrators, applications, adjacent beneficiaries, bottlenecks) and produces a Word doc with thesis, value chain table, TAM expansion analysis, stock shortlist, and risks. **Also accepts a ticker as argument** with the same ticker-to-theme mapping logic as `/emerging_industry_trend`; the document title reflects the derived theme with a "Triggered by: [TICKER]" subtitle when a ticker was the input. The skill is a **three-part framework** — 5 convergence signals (entry), the 6-layer value chain map, and **Part 3 / output Section 6: Peak & Reversal Watch** (exit). Part 3 scores 6 exhaustion signals as the mirror of the convergence signals — signal inversion, supply catch-up/capacity overshoot, valuation & crowding extremes, unit-economics erosion, demand-side funding stress, macro/policy regime shift — with 2+ firing as the warning threshold, and renders pre-committed tripwires, a dated watch calendar, a false-alarm test (structural vs. cyclical signals) and the closest historical analogue. Section 6 is **mandatory in every run**, including at 5/5 convergence. Two internal consistency rules when editing: the peak verdict must reconcile with the Section 2 cycle stage, and Section 5 layer weightings must square with the peak verdict; Section 6a's status colors are deliberately **inverted** versus Section 2 (a firing signal there is bad news). Output section count is 7 — Key Diligence Questions is Section 7, not 6.
- `/industry_deep_dive` analyzes the structural mechanics of an industry (Porter's Five Forces, business model economics, competitive landscape, barriers to entry) — use it when you want to understand *how* an industry works, not just which stocks benefit; accepts either a theme name or a ticker symbol
- `/ai_company_deep_dive` conducts a rigorous multi-dimensional deep dive on a specific ticker with AI exposure — classifies its position in the AI stack, scores its chokepoint strength, analyzes revenue quality and moat, and builds a 3-scenario investment thesis; always re-fetches fresh data via `fetch_all()` (from `get_financial_data.py`) before reading JSON; explicitly flags names where the AI narrative is not supported by the data; output titled "{TICKER} — Company Deep Dive"
- `/multibagger_screener` is an idea-generation funnel (not a single-name analysis) for surfacing stocks with outsized 5x/10x/100x return potential — screens a theme-driven or quality-screen-driven hunting ground against historical multi-bagger base rates (small, long holding period, painful drawdowns, twin-engined growth + multiple expansion, under-covered), producing a scored 3-7 name shortlist with hooks and DNA scorecards; issues no Buy/Hold/Sell calls — hands names off to `/single_stock_quick_research` or `/single_stock_deep_research` for the actual call; runs standalone but can optionally chain from `/industry_trend_analysis` or `/emerging_industry_trend` for the theme-driven hunting ground
- `/balance_sheet_analysis` includes an **Off-Balance-Sheet (OBS) Analysis** section: a 7-category scored checklist (leases, SPEs/VIEs, guarantees, JV/equity-method, pensions, purchase obligations, SBC dilution; 0–2 each, total /14) plus an OBS-adjusted vs. reported leverage table. SEC EDGAR JSON has no footnote data, so this section is sourced from 10-K/10-Q footnotes via `WebSearch`, cited by filing and date
- `/income_statement_analysis` also covers growth & profitability (the former `/growth_and_profitability_analysis` skill was merged into it): latest-quarter YoY snapshot, a **drivers section** (sourced explanations of what moved revenue, gross profit, operating income and net income from the press release / MD&A / call, plus revenue vs. pre-print consensus and guidance), annual (5 FYs + TTM + consensus) and quarterly (8 quarters + up to 4 consensus) trend charts with matching tables, Rule of 40, and a **Consensus Outlook** of the next 2–3 fiscal years (revenue, margins, EPS, analyst count) from WebSearch — out-years with no coverage are N/A, never extrapolated
- `/technical_analysis` includes a **Moving Averages — Distance from Spot** section (20/50/100/200-day levels, % distance, slope, MA stack, crosses) and a **Price Momentum — Near-Term vs Mid-Term** section (1W–12M returns vs. S&P 500, aligned/diverging call); MAs and returns are computed from `_price_history.json`, not `_quick_metrics.json`
- `/quick_stock_metrics` with no args reads from `tickers.txt`; all other skills require a TICKER or THEME argument
- `/quick_stock_metrics` always re-fetches fresh data via `fetch_all()` before computing metrics, even if JSON files already exist
- Skills read local JSON from `Outputs/` first, run `get_financial_data.py` if missing, then supplement with `WebSearch` for analyst estimates, guidance, and any N/A values
- Each analysis skill generates matplotlib charts (saved as PNGs to `Outputs/`), then writes and executes a `python-docx` script inline to embed the charts and produce the `.docx`
- `/single_stock_deep_research` always re-fetches fresh data via `fetch_all()` (from `get_financial_data.py`) and re-runs all 8 individual analyses in sequence (including `/leadership_analysis`; output prefixes are numbered 1–8), then synthesizes a 2–3 page hedge-fund research note (conviction score + LONG/SHORT/PASS with price target), and finally assembles all documents into a single `_stock_deep_research_` Word file with page numbers
- `/single_stock_quick_research` is a lighter-weight, self-contained single-stock initiation note — works through seven pillars (business, financial health, valuation, news/catalysts, risk, business potential, synthesis); re-fetches data via `get_financial_data.py` first, then supplements with `WebSearch` for peer comps, analyst targets, and news; produces a single polished `.docx`; use it for quick coverage initiation where the full 9-analysis suite is overkill; also serves as the default skill when the user asks "what do you think of $TICKER" or "should I buy X"
- `/earnings_report_analyzer` scores a single quarter's earnings report and call transcript across 7 dimensions (headline quality, margin trajectory, growth durability, balance sheet/cash flow quality, management commentary shift, headwinds/red flags, valuation reality check), each -2 to +2, summing to a net score that classifies the quarter from "Strong quality beat" to "Red flag quarter"; re-fetches JSON via `get_financial_data.py` for the quantitative trend data and reuses `chart_income_statement.py` for margin and growth charts rather than generating new ones, then supplements with `WebSearch` for the press release, call transcript, and prior guidance; use it whenever the ask is about one specific print rather than a full initiation note — it exists to stop analysis from stopping at the headline beat/miss

## Hedge-Fund House Style

Every analysis skill is written for a **buy-side portfolio manager (PM)** to digest — not a sell-side client. All skills share one consistent house style. When editing an existing skill or adding a new one, conform to this:

- **Persona:** the author is a **buy-side analyst at a hedge fund** writing for the PM. Thesis-first, directional, and opinionated. Lead each section with the conclusion ("so what for the long/short"), not a description of what the section covers. No balanced sell-side hedging — take a side and defend it with numbers.
- **Verdict — two templates depending on skill type:**
  - **Full-call skills** (`single_stock_deep_research`, `ai_company_deep_dive`, `valuation_analysis`, `technical_analysis`) render a **Verdict** block with: directional bias (**LONG / SHORT / PASS**), a **Conviction score X/10**, current price, **12-month price target (+%)**, **stop / invalidation level (−%)**, **risk/reward ratio**, and **sizing** (Core / Starter / Tactical / Avoid).
  - **Component skills** (`business_overview`, `leadership`, `income_statement`, `balance_sheet`, `cash_flow`, `business_potential`) render a **Read-Through to the Call** block: a directional **Signal (BULLISH / NEUTRAL / BEARISH for the thesis)**, a **dimension conviction X/10**, a one-line "so what" for the long/short, and a one-line "what flips it."
  - **Theme/macro skills** (`emerging_industry_trend`, `industry_trend_analysis`, `industry_deep_dive`, `market_sentiment_analysis`) render a directional **posture** call (e.g., theme conviction X/10 with how to express it — long basket / pair trade / underweight; or for market sentiment a Risk-On / Neutral / Risk-Off net-exposure posture with conviction X/10).
- **Conviction scale (X/10):** 9–10 = highest-conviction book position · 7–8 = high · 5–6 = moderate / starter · 3–4 = low / watchlist · 1–2 = avoid or short candidate. This **replaces the old X/5 "Rating" blocks** — no skill should still emit an "Overall Rating X/5."
- **Variant View — mandatory in every note.** Every skill must include a **"Variant View — Consensus vs. Our Read"** section: a small 3-column table (debate | consensus / sell-side view | our differentiated read with the number behind it), followed by a one-line **"The edge:"** bullet naming what the market is mispricing and why we think we are right. This is the buy-side value-add and is non-negotiable.
- **Word rendering:** the Verdict / Read-Through block is rendered in bold (full-call verdicts use a colored Heading-1-style line: green `007000` for LONG / Risk-On, red `C00000` for SHORT / Risk-Off, neutral for PASS). The Variant View table follows the standard table rules below.

## Word Document Generation

When writing `python-docx` table code in any skill or script:
- **Always initialize tables with `rows=1`** (header only), then call `table.add_row()` for each data row — do NOT use `rows=1+len(data)` upfront, which creates blank rows between the header and data
- **Every table must call `autofit_table(table)` then `add_table_borders(table)` AFTER all rows are added** — calling before rows are added means new rows won't inherit the settings. Never call them at table creation time; always call them after the last `table.add_row()`.
  - `autofit_table` — sets `tblW`/`tblLayout` to autofit, strips all fixed `w:tcW` cell widths, and centers the table on the page; never use `table.columns[i].width` or any fixed-width assignment, and don't set `table.alignment` yourself (`apply_house_style()`, run by `add_footnote()`, also re-centers every table as a backstop)
  - `add_table_borders` — applies a thin single border (`sz=4`, `val="single"`, `color="000000"`) to all four sides plus inner dividers (`insideH`/`insideV`) of every cell via `w:tcBorders`
- **All non-header table cell text must use font size 10 (Arial).** Call `set_row_font_size(row)` on every data row immediately after `table.add_row()`. Do **not** call it on the header row.
- All helpers live in `doc_utils.py` at the project root — generated scripts import them with:
  ```python
  import sys; sys.path.insert(0, '.')
  from doc_utils import setup_document, autofit_table, add_table_borders, set_row_font_size, add_footnote, fmt_value
  ```
  The `sys.path.insert(0, '.')` is required because scripts are saved under `Outputs/{TICKER}/` but run from the project root.
- **Always use `fmt_value(v)` from `doc_utils` to format all dollar amounts in Word table cells** — never hardcode `/ 1e9` or append `"B"` manually. `fmt_value` auto-scales: ≥$1B → `$X.XXB`, ≥$1M → `$X.XM`, ≥$1K → `$X.XK`, else raw dollars. Pass `prefix=''` for non-dollar values.
- **`smart_scale(values)` is defined locally in each `chart_*.py`** (not in `doc_utils`). It returns `(divisor, axis_label, suffix)` and is used to pick a shared Y-axis scale for all series on a chart. Copy the existing implementation from any `chart_*.py` when writing a new chart script.
- **Apostrophe pitfall in generated Python scripts:** when writing string literals that contain apostrophes (e.g. `"Tesla's"`, `"Comma.ai's"`), use double-quoted strings — never single-quoted. Single-quoted strings with an apostrophe inside cause `SyntaxError: unterminated string literal` at runtime. This is the most common bug in skill-generated `generate_*.py` scripts.
- **Every skill must call `add_footnote(doc)` immediately before `doc.save(...)`** — this appends the standard AI-generated disclaimer and "not investment advice" notice at the bottom of every Word document.
- **Every quantitative figure in every generated document must cite where it came from** — SEC EDGAR, Yahoo Finance, a hybrid of both, or a WebSearch source. This applies to Word docs as much as `quick_stock_metrics.py`'s Excel output. Mechanics:
  - When a figure comes from `quick_stock_metrics.compute_metrics()`, call it with `with_sources=True` to get the actual per-metric source label (`SRC_SEC`, `SRC_YAHOO`, `SRC_HYBRID`, `SRC_COMPUTED`, or `SRC_NA` — a metric's source can differ by ticker, so always read the label rather than assuming one from the metric name) and cite it with `add_source_note()` from `doc_utils.py` (import alongside the other helpers) — either inline after a stated figure or as a trailing small-print line under a financial-snapshot table.
  - When a figure is pulled directly from a JSON file (income statement / balance sheet / cash flow → "SEC EDGAR"; quick_metrics / price_history → "Yahoo Finance") rather than through `compute_metrics()`, cite it the same way using the matching plain-text label.
  - When a figure comes from `WebSearch` (analyst estimates, guidance, news, peer comps), cite the source name/publication and date, consistent with how skills already handle citations for qualitative claims — the source-citation requirement isn't new for WebSearch-derived figures, just now explicit that it applies to *every* number, not only web-sourced ones.
  - `quick_stock_metrics.py`'s Excel output is the reference implementation: ticker sheets get a visible "Source" column, the Comparison sheet uses an Excel comment/hover-note per cell plus a legend, and every value cell also carries the hover-note as the literal footnote.
- **House format — every Word document is landscape Letter (11" × 8.5"), narrow 0.5" margins on all sides, Arial throughout, 10pt for all text except headings** (Title / Heading N styles keep their sizes). Call `setup_document(doc)` immediately after `doc = Document()`:
  ```python
  setup_document(doc)  # landscape Letter, 0.5" margins, Arial 10pt body text
  ```
  Don't set explicit run sizes on body text, table cells, citations or captions — 10pt is the default. `add_footnote(doc)` re-applies the format via `apply_house_style(doc)`, which also forces any explicit non-heading run size below 14pt down to 10pt, so a stray `Pt(12)` can't break the house style. Embed full-width charts at `width=Inches(9.5)` (`doc_utils.CHART_WIDTH`).
- **Never place two tables back to back.** Word merges adjacent tables into one, putting the second table onto the first's column grid, so columns collapse to a character wide. `autofit_table()` now inserts a spacer paragraph automatically when a table directly follows another one. Still, put a heading, caption or source line between tables.

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
- `references/scoring-tables.md` — per-indicator 0–100 conversion bands, composite weights (credit heaviest at 20%), and composite zone labels for `/market_sentiment_analysis`; if an indicator is unavailable, drop it and renormalize the weights
- `references/bubble-framework.md` — the six bubble warning conditions, the conditions-firing → Low/Moderate/Elevated/Extreme verdict mapping, and historical analogues for calibration
- Both are read by `/market_sentiment_analysis` Steps 2–3; keep the thresholds here and in the skill's inline summary consistent when editing either
- `references/data-layer.md` — the full mechanics of `sec_edgar_data.py` (tag selection, discrete-quarter derivation, backfills, stale-item dropping, TTM anchoring) and `quick_stock_metrics.py` (sourcing rules per metric, unit traps, the `METRICS` contract); CLAUDE.md keeps the summary and traps — read this before editing either module or debugging a statement number
- `references/reit-framework.md` — REIT detection (`industry` starts with `REIT` / `sector` = `Real Estate`; mortgage REITs excluded), the generic-to-REIT metric substitutions (AFFO/FFO for EPS, P/AFFO, AFFO payout, net debt/EBITDAre, dividend-yield spread to the 10-year, implied cap rate/NAV, dividend discount model), data-source caveats (SEC EDGAR is GAAP-only and often lacks Total Debt/capex/dividend lines for REITs), and the unadjusted-price rule for dividend payers. Every single-stock skill (`business_overview`, `leadership`, `income_statement`, `balance_sheet`, `cash_flow`, `business_potential`, `valuation`, `technical`, `single_stock_deep_research`, `single_stock_quick_research`, `earnings_report_analyzer`, `ai_company_deep_dive`, `quick_stock_metrics`) carries a short `REIT HANDLING` block that points here and applies only when the company is a REIT; keep the block and the reference consistent when editing either

## Adding a New Skill

To add a new analysis skill:
1. Create `.claude/commands/{skill_name}.md` — write it as instructions Claude will follow at execution time (not Python code itself)
2. If the skill generates charts for a single ticker, add a `chart_{name}.py` at the project root (reads JSON from `Outputs/{TICKER}/`, saves PNG to same folder). Theme/market-level skills (e.g., `/market_sentiment_analysis`) generate charts inline inside the `generate_*.py` script using `yfinance` + `matplotlib` directly — no separate `chart_*.py` needed.
3. If the skill generates a Word document, instruct it to: run the relevant `chart_*.py` (or generate charts inline) → write a `generate_*.py` script to `Outputs/{TICKER}/` (or `Outputs/` root for non-ticker skills) → execute it → confirm the `.docx` path
4. All generated Word scripts must import helpers from `doc_utils.py` (see Word Document Generation section)
5. Ad-hoc one-off Python scripts should be saved to `Outputs/{TICKER}/`, not the project root

## Outputs Directory

- **Ticker-specific files** (JSON, PNG, Word) → `Outputs/{TICKER}/` (e.g., `Outputs/NVDA/`) — created automatically by `get_financial_data.py` and each analysis skill
- **Cross-ticker files** (Excel) → `Outputs/` root — e.g., `quick_stock_metrics_YYYYMMDD.xlsx`
- JSON files are the persistent data cache — delete and re-fetch if data is stale; Word/PNG files are overwritten on each run
- `generate_*.py`, `assemble_*.py`, and `compute_*.py` scripts generated by skills are saved to `Outputs/{TICKER}/` (not the project root) — safe to delete at any time

