# Quick Stock Metrics

Generate a side-by-side fundamental analysis spreadsheet for one or more tickers. Income statement, balance sheet, and cash flow data come from SEC EDGAR (`sec_edgar_data.py`) rather than Yahoo Finance, since Yahoo is often stale for weeks after an earnings release; market-quote data with no SEC EDGAR equivalent (price, market cap, P/E, dividend yield, etc.) still comes from Yahoo Finance's quick metrics.

**House style — buy-side quick-filter (Stage 3).** This is the triage screen a hedge-fund analyst runs before committing to deep diligence: a side-by-side read to decide which names are long candidates, which are short/avoid candidates, and which warrant a full single-name workup. The Excel is the data plus a **Summary** sheet carrying the directional screen read, and the **chat output must end with the same screen read** (see "Buy-Side Screen Read" below). Keep it decisive — the point of a screen is to kill names quickly.

## Inputs

- One or more ticker symbols (e.g. `AAPL`, `MSFT GOOGL NVDA`), **or**
- No arguments — in which case load tickers from `tickers.txt` in the project root by calling `load_tickers()` from `get_financial_data.py`

## Required JSON files (per ticker, lowercase)

For each `{ticker}`:
- `Outputs/{TICKER}/{ticker}_income_statement_quarterly.json`
- `Outputs/{TICKER}/{ticker}_income_statement_annual.json`
- `Outputs/{TICKER}/{ticker}_income_statement_ttm.json`
- `Outputs/{TICKER}/{ticker}_balance_sheet_quarterly.json`
- `Outputs/{TICKER}/{ticker}_cash_flow_statement_quarterly.json`
- `Outputs/{TICKER}/{ticker}_cash_flow_statement_annual.json`
- `Outputs/{TICKER}/{ticker}_cash_flow_statement_ttm.json`
- `Outputs/{TICKER}/{ticker}_quick_metrics.json`

## Data fetch — always re-download

**Always re-fetch fresh data before computing metrics**, regardless of whether JSON files already exist.

1. Call `fetch_all(tickers)` from `get_financial_data.py` for all tickers being processed — this fetches income statement / balance sheet / cash flow from SEC EDGAR (`sec_edgar_data.py`), plus quick_metrics and the 5-year price history from Yahoo Finance (the RSI input). Call it **once** with the full ticker list; `compute_metrics()` only reads the resulting JSON and never re-downloads price history.
2. If a ticker fetch fails, print an error and skip it (do not include it in the Excel output).
3. After fetching, verify the files exist before proceeding.

Do this **before** writing any Excel output.

## Your task

Run `quick_stock_metrics.py` (located in the project root) to compute the metrics below for each ticker, then output an Excel file `Outputs/quick_stock_metrics_YYYYMMDD.xlsx` where YYYYMMDD is today's date. If some tickers failed to fetch, pass the surviving tickers explicitly: `.venv/Scripts/python quick_stock_metrics.py T1 T2 ...`, since the no-argument run reads `tickers.txt` and stops on the first missing file.

### Data sourcing rules

**Statement-derived metrics** (revenue, growth, margins, ROE, D/E, interest coverage, current ratio, FCF margin, Rule of 40, payout ratio) source primarily from the SEC EDGAR statement JSON files, falling back to `_quick_metrics.json` only if the SEC-derived value is unavailable (e.g. a filer doesn't use the expected XBRL tag).

**Hybrid metrics** (Trailing P/E, Price/Sales) combine SEC EDGAR fundamentals with Yahoo's current price, since SEC filings report historical financial statements, not trading prices — there is no SEC EDGAR substitute for "current price" at all.

**Market-quote metrics** (price, 52-week range, market cap, Forward P/E, PEG, dividend yield, sector) have no SEC EDGAR equivalent and always source from `_quick_metrics.json`. Forward P/E and PEG specifically can *never* be computed from SEC EDGAR, even partially — both require forward-looking consensus analyst estimates (next-FY EPS, expected growth rate), and SEC filings only ever contain actual reported historicals.

#### Statement-derived metrics — primary source (SEC EDGAR JSON)

| Metric | Primary source | Fallback (quick metrics field) |
|---|---|---|
| Revenue (TTM) | `Total Revenue` from `_income_statement_ttm.json` | `totalRevenue` |
| Revenue Growth Rate | Two most recent annual periods in `_income_statement_annual.json` | `revenueGrowth` |
| Gross Margin | `(Total Revenue - Cost Of Revenue) / Total Revenue` (TTM) | `grossMargins` |
| Operating Margin | `Operating Income / Total Revenue` (TTM) | `operatingMargins` |
| Net Income Margin | `Net Income / Total Revenue` (TTM) | `profitMargins` |
| ROE | `Net Income (TTM) / Stockholders Equity` (most recent quarter) | `returnOnEquity` |
| D/E | `Total Debt / Stockholders Equity` (most recent quarter) | `debtToEquity` (Yahoo returns a **percentage**, e.g. `173` = 173%; divide by 100 — do not double-divide) |
| Interest Coverage | `Operating Income (TTM) / abs(Interest Expense (TTM))` | — (N/A if Interest Expense is zero or missing) |
| Current Ratio | `Current Assets / Current Liabilities` (most recent quarter) | `currentRatio` |
| FCF Margin | `Free Cash Flow (TTM) / Total Revenue (TTM)` | `freeCashflow / totalRevenue` |
| Rule of 40 | Computed from Revenue Growth Rate + Operating Margin above | — |
| Payout Ratio | `abs(Cash Dividends Paid (TTM)) / Net Income (TTM)` | `payoutRatio` |

#### Hybrid metrics — SEC EDGAR fundamentals + Yahoo price

| Metric | Primary source | Fallback (quick metrics field) |
|---|---|---|
| Trailing P/E | `currentPrice / Diluted EPS (TTM)` — only when Diluted EPS > 0 | `trailingPE` |
| Price / Sales | `(currentPrice × Shares Outstanding) / Total Revenue (TTM)` — Shares Outstanding from the balance sheet JSON's `"Shares Outstanding"` field (SEC's `dei:EntityCommonStockSharesOutstanding`, filing cover page) | `priceToSalesTrailing12Months` |

#### Market-quote metrics — always from quick metrics

| Metric | Quick metrics field(s) |
|---|---|
| Current Price | `currentPrice`, fallback `regularMarketPrice` |
| 52-Week Low | `fiftyTwoWeekLow` |
| 52-Week High | `fiftyTwoWeekHigh` |
| Market Cap | `marketCap` |
| Forward P/E | `forwardPE` |
| PEG Ratio | `pegRatio`, fallback to `trailingPegRatio` |
| Dividend Yield | `trailingAnnualDividendYield`, fallback `dividendYield` (Yahoo's forward-estimate field, sometimes a percentage — divide by 100) |

#### Notes on normalization

- `returnOnEquity`, `operatingMargins`, `grossMargins`, `profitMargins`, `revenueGrowth`, `currentRatio`: already decimal ratios — use as-is
- `debtToEquity`: Yahoo returns this as a **percentage** (e.g. `173` = 173%) — `quick_stock_metrics.py` always divides by 100 to convert to a ratio; do not divide again
- SEC EDGAR `Cost Of Revenue`, `Operating Income`, `Free Cash Flow`, and `Total Debt` may be derived (not directly tagged) by `sec_edgar_data.py` when a filer doesn't use the expected XBRL tag — see that script's backfill logic; treat them the same as directly-tagged values

### Metrics to compute

For each ticker compute the following. Apply the comment/benchmark alongside each value.

#### 1. Current Price
`currentPrice` (fallback `regularMarketPrice`) — display as `$X.XX`; color green if closer to 52-week low, pink if closer to 52-week high

#### 2. 52-Week Low
`fiftyTwoWeekLow` — display as `$X.XX`; no coloring

#### 3. 52-Week High
`fiftyTwoWeekHigh` — display as `$X.XX`; no coloring

#### 4. RSI (14-Day)
Compute from `{ticker}_price_history.json` using Wilder's smoothed 14-day RSI.
- Green ≤30 (oversold) | Yellow 30–70 (neutral) | Red ≥70 (overbought)

#### 5. Market Cap
`Market Cap = marketCap from quick metrics`
- Display in billions: `$X.XXB`
- Comments: no threshold coloring — informational context only

#### 6. Revenue (TTM)
`Revenue = Total Revenue from TTM income statement (SEC EDGAR), fallback totalRevenue from quick metrics`
- Display in billions: `$X.XXB`
- Comments: no threshold coloring — informational context only (leave cell uncolored)

#### 7. Revenue Growth Rate (YoY)
`Revenue Growth = revenueGrowth from quick metrics (or compute from two most recent annual periods)`
- Comments: >20% → Strong | 10–20% → Solid | <10% → Slow

#### 8. Gross Margin
`Gross Margin = (Total Revenue - Cost of Revenue) / Total Revenue (TTM)`
- Comments: >60% → High quality | 40–60% → Decent | <40% → Watch for pricing pressure

#### 9. Operating Margin
`Operating Margin = Operating Income (TTM) / Total Revenue (TTM)`
- Comments: >30% → Strong pricing power | 15–30% → Decent | <15% → Watch for cost pressure

#### 10. Net Income Margin
`Net Income Margin = Net Income (TTM) / Total Revenue (TTM)`
- Comments: >20% → Strong | 10–20% → Decent | <10% → Thin

#### 11. Return on Equity (ROE)
`ROE = Net Income (TTM) / Stockholders Equity (most recent quarter)`
- Comments: ≥20% → Ideal | ≥15% → Good | <15% → Below threshold

#### 12. Debt-to-Equity (D/E)
`D/E = Total Debt (most recent quarter) / Stockholders Equity (most recent quarter)`
- Total Debt = Short Long Term Debt + Long Term Debt (sum whichever fields are present; use `Total Debt` if available directly)
- Comments: <0.5 → Very conservative | 0.5–1.0 → Healthy | 1.0–2.0 → Moderate leverage | >2.0 → High risk

#### 13. Interest Coverage
`Interest Coverage = EBIT (TTM) / Interest Expense (TTM)`
- EBIT = Operating Income (TTM); use absolute value of Interest Expense as denominator
- If Interest Expense is zero or missing, display `N/A`
- Comments: >10× → Very safe | 5–10× → Adequate | 3–5× → Watch | <3× → At risk

#### 14. Current Ratio
`Current Ratio = Current Assets (MRQ) / Current Liabilities (MRQ)`
- Comments: >2.0 → Very liquid | 1.5–2.0 → Healthy | 1.0–1.5 → Adequate | <1.0 → Potential liquidity risk

#### 15. Free Cash Flow (FCF) Margin
`FCF Margin = (Operating Cash Flow (TTM) - Capital Expenditure (TTM)) / Total Revenue (TTM)`
- Capital Expenditure may be negative in the JSON; use its absolute value.
- Comments: >20% → High quality | 10–20% → Solid | <10% → Low

#### 16. Rule of 40 Score
`Rule of 40 = Revenue Growth Rate (YoY annual) + Operating Margin (TTM)`
- Revenue Growth Rate = (Most Recent Annual Revenue - Prior Annual Revenue) / Prior Annual Revenue
- Both expressed as percentages before summing.
- Comments: >40 → Healthy/investible | 30–40 → Borderline | <30 → Warning zone

#### 17. Valuation
Pull directly from `_quick_metrics.json`:
- `Trailing P/E` (field: `trailingPE`)
- `Forward P/E` (field: `forwardPE`)
- `PEG Ratio` (field: `pegRatio`)
- `Price / Sales` (field: `priceToSalesTrailing12Months`)
- Comments: PEG <1 → Potentially undervalued | PEG 1–2 → Fair | PEG >2 → Expensive relative to growth
- P/S Comments: <3 → Cheap | 3–6 → Fair | >6 → Expensive

#### 18. Dividend Yield
`Dividend Yield = trailingAnnualDividendYield from quick metrics`
- Display as a percentage (e.g. `1.5%`)
- Only shown when available; display `N/A` if missing
- No color applied

### Output format (Excel)

#### Per-ticker sheets
Each ticker gets its own sheet named by ticker symbol. Layout the metrics as a **flat table** with four columns: `Metric | Value | Comment | Source`.

- **Metric**: bold numbered metric name (e.g. `1. Return on Equity (ROE)`)
- **Value**: the computed value, color-coded (green/yellow/red); also carries an Excel comment (hover-note) citing its source, same text as the Source column
- **Comment**: short benchmark qualifier (e.g. `Ideal (≥20%)`)
- **Source**: where this metric's value actually came from for this ticker — `SEC EDGAR`, `Yahoo Finance`, `Hybrid (SEC EDGAR + Yahoo Finance)`, `Computed (Yahoo Finance price history)`, or `N/A (no data available)`. Get this from `compute_metrics(ticker, with_sources=True)`, which returns `(results, sources)` — never hardcode a metric's source, since fallback means the actual source can differ by ticker even for the same metric.

No description or benchmark rows on ticker sheets — those live only on the Comparison sheet.

Color the **value cell** only:
- Green fill if the value meets the "ideal/good" threshold
- Yellow fill if borderline
- Red fill if below threshold / warning zone

#### Summary sheet (the screen read)
- Named `Summary`, placed as the **first** sheet; added after the workbook is built (see "Buy-Side Screen Read" below)
- Title "Screen read (screen-level only; a full call needs a research skill)" and an as-of date
- Table: `Ticker | Tilt | Conviction | Why`, dark-blue header row; the Tilt cell is filled green for Long-lean, yellow for Neutral, pink for Short-lean / Avoid
- Below the table: **Top long candidate**, **Top short / avoid candidate**, **Next step**, and **Data notes** (excluded or substituted tickers, and metrics that are wrong or meaningless for a ticker, with the reason)

#### Summary Comparison sheet
- Named `Comparison`, placed second (right after `Summary`)
- **Top section**: flat comparison table — tickers as columns, metrics as rows, values only with green/yellow/red coloring for quick side-by-side review. Each value cell carries an Excel comment (hover-note) citing its source, since sources can differ by ticker for the same metric — there isn't room for a visible per-ticker Source column here without doubling the sheet width.
- **Middle section**: hierarchical metric descriptions and benchmarks — for each metric, list its description and benchmark thresholds. This is the only place descriptions and benchmarks appear.
- **Bottom section**: a "Data Source Legend" explaining each of the five source labels (SEC EDGAR / Yahoo Finance / Hybrid / Computed / N/A), plus a note to hover over any value cell for its specific source.

- Format all ratio/margin cells as percentages where appropriate
- Use `openpyxl` for Excel generation (already available in the project venv); use `openpyxl.comments.Comment` for the hover-note source citations

### Error handling

- If a JSON field is missing or null within a file, fill the cell with `N/A` and skip coloring
- Print a warning to stdout for any missing field
- Do not confuse a missing JSON field (within an existing file) with a missing file — missing files must trigger the auto-fetch described above

## REIT Handling (apply to any ticker that is a REIT)

Definitions are in `references/reit-framework.md`. Detect: `_quick_metrics.json` `industry` starts with `REIT` (or `sector` is `Real Estate`). Equity REITs follow this block; mortgage REITs (`REIT - Mortgage`) are financials, so flag it and use book value, price/book and net interest spread instead. Not a REIT: ignore this block.

- The Excel is built by `compute_metrics()` and stays GAAP-based, so for a REIT several columns (Trailing/Forward P/E, PEG, Payout Ratio, ROE, Interest Coverage, Current Ratio, FCF Margin, Rule of 40) are **not meaningful** and must not be used to rank it against operating companies; do not change the Excel metrics, but flag each REIT in the chat output.
- In the Buy-Side Screen Read, mark every REIT and screen it on REIT measures instead: AFFO per share and payout ratio (non-GAAP, from the latest release), dividend yield and its spread to the 10-year, and net debt/EBITDAre. Source these via `WebSearch` with date and label them non-GAAP; mark them N/A if not found.
- Recommend the full single-name workup for REITs that pass the screen, since the deep-research and quick-research skills apply this framework.

## Buy-Side Screen Read (Summary sheet + chat, after the Excel is saved)

After the workbook is saved, write a concise buy-side triage of the screened set — this is what makes the screen actionable for the PM. Derive it from the computed metrics and their green/yellow/red coloring (plus any WebSearch facts, e.g. REIT measures, cited with source and date); `compute_metrics()` does not produce it.

Before writing it, sanity-check the numbers you will lean on: negative book equity makes ROE and D/E meaningless; a huge one-quarter GAAP loss or gain distorts net margin, ROE and trailing P/E; an FCF margin far below the net margin usually means capex came back untagged and the metric fell back to Yahoo's narrower FCF; a very low forward P/E on a cyclical (memory, commodities) usually means peak earnings. Put each such finding in the Data notes rather than ranking on it.

- **Screen tilt per ticker:** a one-line directional lean for each name — **Long-lean / Neutral / Short-lean / Avoid** — with a one-clause reason anchored to the metrics (e.g., "Long-lean — Rule of 40 = 48, FCF margin 24%, net cash; quality compounder at a reasonable multiple").
- **Quick-filter conviction X/10** per name (screen-level only — a full call requires `/single_stock_quick_research` or `/single_stock_deep_research`).
- **Top long candidate** and **top short/avoid candidate** from the set, one sentence each on why.
- **Next step:** name the 1–2 tickers that most warrant a full `/single_stock_deep_research` (or lighter `/single_stock_quick_research`) workup and why.

**Write it into the workbook.** Save the screen read as JSON to `Outputs/quick_stock_metrics_summary_YYYYMMDD.json`:

```json
{
  "title": "Screen read (screen-level only; a full call needs a research skill)",
  "as_of": "YYYY-MM-DD",
  "rows": [
    {"ticker": "AVGO", "tilt": "Long-lean", "conviction": "7/10", "reason": "18.3x forward P/E, PEG 0.35, 48% operating margin ..."}
  ],
  "top_long": "AVGO: one sentence on why.",
  "top_short": "INTC: one sentence on why.",
  "next_step": ["/single_stock_deep_research AVGO: why.", "/single_stock_quick_research MU: why."],
  "notes": ["Excluded / substituted tickers and data caveats, one per item."]
}
```

Order `rows` from most long-leaning to most short-leaning. Then add the sheet with
`PYTHONIOENCODING=utf-8 .venv/Scripts/python quick_stock_metrics.py --summary Outputs/quick_stock_metrics_summary_YYYYMMDD.json` (it defaults to today's workbook; pass the `.xlsx` path as a third argument otherwise). This loads the workbook, adds or replaces the `Summary` sheet as the first sheet, and saves it in place, then rewrites the interactive web page `Outputs/quick_stock_metrics_YYYYMMDD.html` (screen read + a sortable, benchmark-colored comparison grid; the plain run writes the grid-only version) and refreshes `Outputs/index.html` — re-run it after editing the JSON.

**Then report the same read in chat** as a compact table plus the top long / top short / next-step lines and the data notes; the Excel carries the metric detail.

## Example invocation

The user may say:
- `/quick_stock_metrics` — load tickers from `tickers.txt`
- `/quick_stock_metrics AAPL` — single ticker
- `/quick_stock_metrics MSFT GOOGL NVDA` — explicit list
- "Run quick metrics for AAPL"
- "Compare AAPL and TSLA using quick metrics"

If no tickers are provided in the message, call `load_tickers()` from `get_financial_data.py` to read `tickers.txt`. If the file is empty or missing, print an error and stop.

Parse the tickers, run the script, add the Summary sheet, and report the output file path and the screen read when done.
