# REIT Framework

Shared guidance for every single-stock skill when the company is an equity Real Estate Investment Trust (REIT). Generic operating-company templates (GAAP EPS, P/E, free cash flow, Debt/Equity, current ratio, Rule of 40) mislead for a REIT, so each skill keeps its normal format and swaps in the REIT-standard equivalents below. Every skill's own `REIT HANDLING` block points here for the definitions.

## 1. Detect the company type

- Read `Outputs/{TICKER}/{ticker_lowercase}_quick_metrics.json`: treat the company as a REIT if `industry` starts with `REIT` or `sector` is `Real Estate` (SIC code 6798 on the SEC filing is a second check).
- **Equity REITs** (net lease, retail, office, industrial, residential, healthcare, data center, tower, self-storage, timber, diversified) follow this framework.
- **Mortgage REITs** (`industry` = `REIT - Mortgage`) are financials, not property owners: FFO/AFFO, occupancy and cap rates do not apply. Say so explicitly, and use book value per share, price/book, net interest spread, leverage and dividend coverage by distributable earnings instead. Flag it to the user rather than forcing this framework.
- If the company is not a REIT, ignore this file and every `REIT HANDLING` block.

## 2. Metric substitutions

| Generic metric | Why it misleads for a REIT | Use instead |
|---|---|---|
| GAAP EPS, trailing/forward P/E, PEG | Net income is burdened by real-estate depreciation and amortization and by impairments; gains on sale distort it the other way | **FFO** and **AFFO per share** (non-GAAP); **P/FFO**, **P/AFFO** |
| Dividend payout ratio (dividends / net income) | Often above 100% purely because of depreciation | **AFFO payout ratio** (dividends per share / AFFO per share); operating-cash-flow dividend coverage |
| Free cash flow / FCF margin | Growth capex is acquisitions and development, often not in a "capex" line | Operating cash flow, then investing and financing flows; **AFFO** as the recurring cash-earnings measure |
| Debt/Equity | Book equity is depreciated and merger-distorted | **Net debt / annualized adjusted EBITDAre**; fixed-charge coverage; debt maturity ladder, weighted-average maturity and rate, fixed vs floating share, unsecured vs secured; liquidity; credit ratings |
| Interest coverage (GAAP operating income / interest) | Operating income is depreciation-burdened | EBITDAre-based interest or fixed-charge coverage |
| Current ratio, quick ratio, cash ratio | REITs report an unclassified balance sheet | **Liquidity** = cash + undrawn revolver, against near-term maturities |
| ROE | Book equity and depreciation distort it | Total return; AFFO per share growth; spread of acquisition yield over cost of capital |
| Rule of 40 | Software metric | Mark **not applicable** |
| Gross margin | Net-lease tenants pay property costs, so it is structurally high | Same-store NOI growth and NOI/EBITDAre margin where disclosed |
| DCF on free cash flow | Ignores acquisitions and cost-of-capital sensitivity | **Dividend discount model** or AFFO-growth total-return build; implied cap rate and NAV cross-check |

## 3. Definitions (use as the company defines them)

- **FFO (Funds From Operations, non-GAAP)** = GAAP net income + real-estate depreciation and amortization ± gains/losses on property sales ± impairments (per the NAREIT definition).
- **AFFO (Adjusted FFO, non-GAAP)** = FFO adjusted for items such as straight-line rent, amortization of above/below-market leases, stock-based compensation and recurring capital expenditures. Definitions vary by company, so quote the company's own reconciliation and label it non-GAAP.
- **EBITDAre** = earnings before interest, taxes, depreciation, amortization, adjusted for real-estate gains/losses and impairments.
- **Same-store NOI (or rent) growth** = growth in net operating income from properties owned in both periods; the organic-growth measure.
- **Implied cap rate** = the market-implied yield on the property portfolio after adding net debt to equity value; compare with the initial cash yield on acquisitions.
- **Investment spread** = initial cash yield on acquisitions minus the company's cost of capital.
- **WALT** = weighted-average lease term.

## 4. Where the data lives

- **SEC EDGAR JSON is GAAP only** and often incomplete for REITs: `Total Debt` may be untagged, and capex/free-cash-flow, dividends paid, debt issued/repaid and equity issued lines can be missing. Say so instead of fabricating them, and reconcile debt against the latest 10-Q balance sheet (notes payable + term loans + credit facility + mortgages) stating which figure was used.
- **FFO, AFFO, occupancy, WALT, same-store growth, leverage, maturity ladder, acquisitions and guidance** come from the earnings release (8-K Exhibit 99.1), the supplemental package and the call transcript via `WebSearch`/`WebFetch`. Cite the filing and date.
- **Yahoo `payoutRatio`** is GAAP-based and misleading for a REIT (it can exceed 200%); `key_stock_metrics._short_comment` already warns about this. Do not use it as the dividend-safety test.
- **Sources disagree.** Where the release, call and supplemental give different values (for example initial cash yield, acquisition volume on a 100% vs pro-rata basis, fixed-rate share), show the range and label it unreconciled rather than picking one silently. State which basis (100%, pro-rata, consolidated) each figure uses.

## 5. Valuation and the rate link

- Value on **P/AFFO** (and P/FFO) against peers and the company's own history, **dividend yield and its spread to the 10-year Treasury** (source the current yield and date), **implied cap rate versus acquisition yields**, and **NAV premium/discount** where analyst NAV is sourced (else N/A). Build a dividend discount model or AFFO-growth total-return case with explicit assumptions and a sensitivity table on the required return.
- REITs are rate-sensitive: state where the 10-year yield sits and how each 50 bp move in the required return changes value per share. The house verdict rules are unchanged: LONG needs more than 15% upside with risk/reward of at least 1.5:1; PASS is within about 15% of fair value or has unclear risk/reward.
- Total return = dividend yield + AFFO-per-share growth ± multiple change. Show it on price alone and including dividends.
- Peer multiples: mark N/A unless the multiple itself is sourced (a peer's AFFO guidance is not a P/AFFO multiple).

## 6. Growth and capital allocation

- Growth is AFFO per share (CAGR from company filings, cited by year), same-store NOI/rent growth, occupancy, acquisition and development volume at what yield spread, and share-count dilution. Explain any gap between revenue growth and AFFO-per-share growth (issuance, financing cost, dilution).
- Capital allocation: acquisition funding mix (public equity vs debt vs retained cash flow vs dispositions), equity issued above or below NAV, leverage discipline, dividend growth record, and any private capital fund or joint-venture (fee-generating, capital-light) strategy. Mark computed residuals (for example "debt and other") as computed, not reported.

## 7. Sub-type checklist (test only what applies)

- **Net lease:** WALT, tenant and industry concentration (top 10/20 tenants as % of rent), rent coverage, investment spread, retail vs industrial mix.
- **Office / retail / industrial:** occupancy, leasing spreads, tenant improvement and leasing commissions (recurring capex), lease expirations, same-store NOI.
- **Residential:** same-store NOI, rent growth on new vs renewal leases, turnover, supply in key markets.
- **Healthcare:** operator rent coverage, operator credit, government reimbursement exposure.
- **Data center:** contracted and installed megawatts, utilization, pre-leasing, power availability, development yield, hyperscaler tenant concentration, cost of capital.
- **Tower / infrastructure:** tenant churn, escalators, lease terms, carrier concentration.
- **Self-storage:** occupancy, street rates, same-store revenue growth, supply.
- **Office specifically:** treat occupancy and lease-expiry risk as first-order; NAV and leverage matter more than AFFO growth.

## 8. Technical analysis for dividend payers

- The project's `_price_history.json` comes from `yf.Ticker(t).history()` with yfinance's default `auto_adjust=True`, so the saved closes are **dividend-adjusted** while the spot price and Yahoo 52-week range are unadjusted. For any material dividend payer (yield above about 2%) this understates older prices, the moving averages and the closing low. Recompute from unadjusted closes, for example `history(period="3y", auto_adjust=False)` saved to a scratch file (do not overwrite the project JSON), and state the basis. Regenerate the chart from the same series if `chart_technical.py` (which reads the adjusted JSON) would otherwise mislead.
- Add relative strength against a REIT benchmark (VNQ or XLRE) and SPY over the same windows, and relate price moves to the 10-year yield (date the move from a source, or mark N/A).

## 9. Presentation conventions

- Label FFO, AFFO, EBITDAre, same-store NOI and adjusted leverage as **non-GAAP**, and give the company's definition once.
- Where a standard table row is not meaningful for a REIT (GAAP P/E, PEG, Rule of 40, current ratio, FCF margin, GAAP payout, ROE, GAAP interest coverage), keep the row but write **"not meaningful for a REIT"** with the REIT equivalent in the comment, and do not color-code it.
- Spell out REIT abbreviations on first use (Funds From Operations (FFO), Adjusted Funds From Operations (AFFO), Earnings Before Interest, Taxes, Depreciation, Amortization for real estate (EBITDAre), Net Asset Value (NAV), Weighted-Average Lease Term (WALT), Net Operating Income (NOI)).
