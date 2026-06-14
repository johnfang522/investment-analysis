# Key Stock Metrics

Generate a side-by-side fundamental analysis spreadsheet for one or more tickers using pre-generated Yahoo Finance JSON outputs.

**House style — buy-side quick-filter (Stage 3).** This is the triage screen a hedge-fund analyst runs before committing to deep diligence: a side-by-side read to decide which names are long candidates, which are short/avoid candidates, and which warrant a full single-name workup. The Excel is the data; the **chat output must end with a directional screen read** (see "Buy-Side Screen Read" below). Keep it decisive — the point of a screen is to kill names quickly.

## Inputs

- One or more ticker symbols (e.g. `AAPL`, `MSFT GOOGL NVDA`), **or**
- No arguments — in which case load tickers from `tickers.txt` in the project root by calling `load_tickers()` from `yahoo_finance_data.py`

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

1. Call `fetch_all(tickers)` from `yahoo_finance_data.py` for all tickers being processed.
2. If a ticker fetch fails, print an error and skip it (do not include it in the Excel output).
3. After fetching, verify the files exist before proceeding.

Do this **before** writing any Excel output.

## Your task

Run `key_stock_metrics.py` (located in the project root) to compute the metrics below for each ticker, then output an Excel file `Outputs/key_stock_metrics_YYYYMMDD.xlsx` where YYYYMMDD is today's date.

### Data sourcing rules

For **every metric**, always attempt to source values from `_quick_metrics.json` first. Only fall back to the detailed financial statement files if the field is absent or null in quick metrics.

#### Quick metrics fields to try first (per metric)

| Metric | Quick metrics field(s) |
|---|---|
| Revenue (TTM) | `totalRevenue` |
| Revenue Growth Rate | `revenueGrowth` (already a ratio, use directly) |
| Gross Margin | `grossMargins` (already a decimal ratio, use directly) |
| Operating Margin | `operatingMargins` (already a ratio, use directly) |
| Net Income Margin | `profitMargins` (already a decimal ratio, use directly) |
| ROE | `returnOnEquity` |
| D/E | `debtToEquity` (already a ratio; use directly, divide by 100 if >10 to normalize) |
| Interest Coverage | `ebitda` (numerator) — fallback to income statement; denominator from income statement |
| Current Ratio | `currentRatio` |
| FCF Margin | `freeCashflow` (numerator) + `totalRevenue` (denominator) |
| Revenue Growth Rate (for Rule of 40) | `revenueGrowth` (already a ratio, use directly) |
| Operating Margin (for Rule of 40) | `operatingMargins` (same as above) |
| Current Price | `currentPrice`, fallback `regularMarketPrice` |
| 52-Week Low | `fiftyTwoWeekLow` |
| 52-Week High | `fiftyTwoWeekHigh` |
| Market Cap | `marketCap` |
| Trailing P/E | `trailingPE` |
| Forward P/E | `forwardPE` |
| PEG Ratio | `pegRatio`, fallback to `trailingPegRatio` |
| Price / Sales | `priceToSalesTrailing12Months` |
| Dividend Yield | `trailingAnnualDividendYield` |

#### Fallback: detailed financial statements

Only used when a quick metrics field is missing or null:

- **Income statement fallback**: use TTM figures from `_income_statement_ttm.json`
- **Balance sheet fallback**: use most recent quarter (first column) from `_balance_sheet_quarterly.json`
- **Cash flow fallback**: use TTM figures from `_cash_flow_statement_ttm.json`
- **Revenue growth fallback**: compute from two most recent annual periods in `_income_statement_annual.json`
- **Interest Coverage fallback**: compute `EBIT / Interest Expense` from TTM income statement; EBIT = Operating Income TTM; Interest Expense field is `InterestExpense` or `Interest Expense` (use absolute value as denominator)
- **Current Ratio fallback**: `Current Assets / Current Liabilities` from most recent quarter balance sheet
- **Gross Margin fallback**: `(Total Revenue - Cost of Revenue) / Total Revenue` from TTM income statement

#### Notes on quick metrics normalization

- `returnOnEquity`: already a decimal ratio (e.g. 0.45 = 45%) — use as-is
- `debtToEquity`: Yahoo returns this as a plain ratio (e.g. 1.73) — use as-is, no division needed
- `operatingMargins`: already a decimal ratio — use as-is
- `grossMargins`: already a decimal ratio — use as-is
- `profitMargins`: already a decimal ratio — use as-is
- `revenueGrowth`: already a decimal ratio — use as-is
- `freeCashflow`: raw dollar value — divide by `totalRevenue` from quick metrics (also raw dollars) to get FCF margin
- `totalRevenue`: raw dollar value — display in billions (divide by 1,000,000,000), formatted as `$X.XXB`
- `currentRatio`: already a plain ratio — use as-is

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
`Revenue = totalRevenue from quick metrics (or Total Revenue from TTM income statement)`
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
Each ticker gets its own sheet named by ticker symbol. Layout the metrics as a **flat table** with three columns: `Metric | Value | Comment`.

- **Metric**: bold numbered metric name (e.g. `1. Return on Equity (ROE)`)
- **Value**: the computed value, color-coded (green/yellow/red)
- **Comment**: short benchmark qualifier (e.g. `Ideal (≥20%)`)

No description or benchmark rows on ticker sheets — those live only on the Comparison sheet.

Color the **value cell** only:
- Green fill if the value meets the "ideal/good" threshold
- Yellow fill if borderline
- Red fill if below threshold / warning zone

#### Summary Comparison sheet
- Named `Comparison`, placed as the first sheet
- **Top section**: flat comparison table — tickers as columns, metrics as rows, values only with green/yellow/red coloring for quick side-by-side review
- **Bottom section**: hierarchical metric descriptions and benchmarks — for each metric, list its description and benchmark thresholds. This is the only place descriptions and benchmarks appear.

- Format all ratio/margin cells as percentages where appropriate
- Use `openpyxl` for Excel generation (already available in the project venv)

### Error handling

- If a JSON field is missing or null within a file, fill the cell with `N/A` and skip coloring
- Print a warning to stdout for any missing field
- Do not confuse a missing JSON field (within an existing file) with a missing file — missing files must trigger the auto-fetch described above

## Buy-Side Screen Read (report in chat after the Excel is saved)

After confirming the output file path, end your chat response with a concise buy-side triage of the screened set — this is what makes the screen actionable for the PM. Do **not** modify the Excel/Python pipeline to produce this; derive it from the computed metrics and their green/yellow/red coloring.

- **Screen tilt per ticker:** a one-line directional lean for each name — **Long-lean / Neutral / Short-lean / Avoid** — with a one-clause reason anchored to the metrics (e.g., "Long-lean — Rule of 40 = 48, FCF margin 24%, net cash; quality compounder at a reasonable multiple").
- **Quick-filter conviction X/10** per name (screen-level only — a full call requires `/single_name_stock_analysis`).
- **Top long candidate** and **top short/avoid candidate** from the set, one sentence each on why.
- **Next step:** name the 1–2 tickers that most warrant a full `/single_name_stock_analysis` deep dive and why.

Keep this to a compact bulleted block; the Excel carries the detail.

## Example invocation

The user may say:
- `/key_stock_metrics` — load tickers from `tickers.txt`
- `/key_stock_metrics AAPL` — single ticker
- `/key_stock_metrics MSFT GOOGL NVDA` — explicit list
- "Run key metrics for AAPL"
- "Compare AAPL and TSLA using key metrics"

If no tickers are provided in the message, call `load_tickers()` from `yahoo_finance_data.py` to read `tickers.txt`. If the file is empty or missing, print an error and stop.

Parse the tickers, generate the script, execute it, and report the output file path when done.
