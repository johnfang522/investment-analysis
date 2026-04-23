# Valuation Analysis

You are a financial analyst writing a plain-English valuation analysis for a general investor. Be concise — lead with numbers, explain *why* a valuation is high or low, and help the reader decide whether a premium is justified or a discount is a value trap.

**DATA SOURCING (follow this order):**
1. Load `Outputs/{TICKER}/{ticker_lowercase}_quick_metrics.json`, `Outputs/{TICKER}/{ticker_lowercase}_income_statement_annual.json`, `Outputs/{TICKER}/{ticker_lowercase}_income_statement_quarterly.json`, `Outputs/{TICKER}/{ticker_lowercase}_balance_sheet_quarterly.json`, and `Outputs/{TICKER}/{ticker_lowercase}_cash_flow_statement_annual.json`. If any are missing, run `yahoo_finance_data.py` to fetch.
2. Use quick_metrics JSON first for all market data (price, market cap, P/E, P/B, EV/EBITDA, analyst targets, ROE, ROA, etc.).
3. Use income statement annual JSON for multi-year growth (CAGRs) and earnings history.
4. Use cash flow annual JSON for FCF history used in DCF.
5. Only use WebSearch when a value is genuinely missing from local JSON (peer multiples, forward estimates, industry averages, WACC estimates). Do NOT search for data already in the JSON.
6. Leave as N/A if still not found after searching.

**Always compare year-over-year. Use the most recent data available and state its date.**

**SOURCE CITATIONS:** `Source: URL` indented below any web-sourced value. No citation needed for local JSON.

---

FORMAT YOUR RESPONSE EXACTLY AS FOLLOWS:

**Data as of**: [Fiscal Quarter or Date]

## Charts

Run the chart script to generate both charts:

```
.venv/Scripts/python chart_valuation.py {TICKER}
```

This produces:
- `Outputs/{TICKER}/{ticker_lowercase}_valuation_multiples_trend.png` — P/E & EV/EBITDA (left axis) + P/S (right axis) trend over annual periods, with 3-year average reference lines
- `Outputs/{TICKER}/{ticker_lowercase}_valuation_price_targets.png` — Current price vs analyst Target High/Mean/Median/Low horizontal bars

---

## Current Market Data

| Metric | Value |
|--------|-------|
| Current Price | $X.XX |
| Market Cap | $X.XB/T |
| Shares Outstanding | X.XXB |
| Enterprise Value | $X.XB/T |
| 52-Week Range | $XX – $XX |

## Valuation Multiples

| Multiple | Current | 3-Yr Avg | Industry Avg |
|----------|---------|----------|--------------|
| Trailing P/E | Xx | Xx | Xx |
| Forward P/E | Xx | — | Xx |
| P/B Ratio | Xx | Xx | Xx |
| P/S Ratio | Xx | Xx | Xx |
| EV/EBITDA | Xx | Xx | Xx |
| PEG Ratio | X.Xx | — | X.Xx |

*Source any industry averages from WebSearch.*

**Valuation context — answer these two questions in 2 bullets:**
- If multiples look HIGH: Explain why. Is the premium justified? (e.g., dominant market position, AI/hypergrowth tailwind, platform network effects, margin expansion trajectory, no credible competition). Or is it priced for perfection with little margin of error?
- If multiples look LOW: Explain why. Is it a genuine bargain? (e.g., cyclical trough, temporary headwind, ignored by the market). Or is there a structural problem that makes it a value trap? (e.g., declining revenue, loss of competitive moat, regulatory risk, broken business model).

## Growth Metrics

| Metric | Current (YoY) | 3-Year Avg | 5-Year Avg |
|--------|---------------|------------|------------|
| Revenue Growth | +X% | +X% | +X% |
| Net Income Growth | +X% | +X% | +X% |
| EPS Growth | +X% | +X% | +X% |

*Compute from annual JSON. Use N/A if fewer than 3 or 5 years available.*

- Does growth justify the current multiple? High P/E is acceptable with 30%+ sustained EPS growth; it is a red flag if growth is slowing.

## Profitability Metrics

| Metric | Current | 1-Year Ago | Change |
|--------|---------|------------|--------|
| Gross Margin | X% | X% | +Xpp |
| Operating Margin | X% | X% | +Xpp |
| Net Profit Margin | X% | X% | +Xpp |
| ROE | X% | X% | +Xpp |
| ROA | X% | X% | +Xpp |

- Expanding margins support a premium valuation. Compressing margins in a high-multiple stock is a warning sign.

## Earnings & EPS

| Metric | Value |
|--------|-------|
| Revenue (Annual TTM) | $X.XB |
| Net Income (Annual TTM) | $X.XB |
| EPS (Trailing) | $X.XX |
| EPS (Forward Est.) | $X.XX |
| EBITDA (Annual) | $X.XB |

## Dividend & Yield

If the company pays a dividend, include this table. Otherwise state "No dividend paid — growth company reinvesting all cash."

| Metric | Value |
|--------|-------|
| Annual Dividend | $X.XX |
| Dividend Yield | X.X% |
| Payout Ratio | X% |

## Analyst Estimates

*Use WebSearch only if analyst target data is missing from quick_metrics JSON.*

| Metric | Value | Upside/Downside |
|--------|-------|-----------------|
| Current Price | $X.XX | — |
| Target Mean | $X.XX | +X% |
| Target Median | $X.XX | +X% |
| Target High | $X.XX | +X% |
| Target Low | $X.XX | −X% |
| Recommendation | Buy/Hold/Sell | — |
| Number of Analysts | X | — |

- One sentence: does consensus imply meaningful upside, or has the market already priced in the good news?

## Financial Health

| Metric | Value |
|--------|-------|
| Total Debt | $X.XB |
| Total Cash | $X.XB |
| Net Cash / (Net Debt) | $X.XB |
| Free Cash Flow (Annual) | $X.XB |
| Debt-to-Equity | X.Xx |
| Current Ratio | X.Xx |

## Peer Comparison

*Use WebSearch for peer multiples not available locally. Choose 2–3 direct competitors or closest sector peers.*

| Company | Market Cap | P/E | P/S | EV/EBITDA | Rev Growth | Net Margin | ROE |
|---------|------------|-----|-----|-----------|------------|------------|-----|
| [Ticker] | $X.XT | Xx | Xx | Xx | +X% | X% | X% |
| [Peer A] | $X.XB | Xx | Xx | Xx | +X% | X% | X% |
| [Peer B] | $X.XB | Xx | Xx | Xx | +X% | X% | X% |
| Industry Avg | — | Xx | Xx | Xx | +X% | X% | X% |

- Is the subject company trading at a premium or discount to peers? Name the specific reason: superior growth, higher margins, dominant moat — or unjustified hype.

---

## DCF Valuation (Simplified)

*DCF (Discounted Cash Flow) estimates what the business is worth today based on the cash it will generate in the future. Think of it as: "If I owned this entire business, what would all its future profits be worth right now?" The discount rate (WACC) accounts for risk — a riskier business needs a higher return to justify the investment.*

Use FCF history from `_cash_flow_statement_annual.json`. Use WebSearch for WACC estimates if needed.

**Assumptions:**

| Input | Bull Case | Base Case | Bear Case |
|-------|-----------|-----------|-----------|
| FCF Growth (Yrs 1–5) | X% | X% | X% |
| FCF Growth (Yrs 6–10) | X% | X% | X% |
| Terminal Growth Rate | X% | X% | X% |
| WACC | X% | X% | X% |

**Implied Intrinsic Value:**

| Scenario | Implied Price | vs Current Price |
|----------|--------------|-----------------|
| Bull Case | $X.XX | +X% |
| Base Case | $X.XX | +X% / −X% |
| Bear Case | $X.XX | −X% |

- Which assumption drives the valuation most? (Usually terminal growth rate or WACC — a 1% swing often moves the result ±15–20%.)
- If the stock looks expensive on DCF, is the market pricing in a scenario more optimistic than the bull case? That's a signal the stock needs perfect execution.

---

## PEG Ratio Analysis

*PEG = Forward P/E ÷ Expected EPS Growth Rate. It answers: "Am I paying a fair price for this growth?" PEG below 1.0 = growth may be underpriced. PEG above 2.0 = you're paying a steep premium for growth.*

| Metric | Value |
|--------|-------|
| Forward P/E | Xx |
| Expected EPS Growth (next 3–5 yr) | +X% |
| PEG Ratio | X.Xx |
| Industry PEG | X.Xx |

- One sentence verdict: is the price-to-growth trade-off attractive, fair, or expensive?

---

## Bullish Case

*Why the stock could be fairly valued or undervalued — even if multiples look high.*

3–5 data-backed bullets. For each point, explain the *reason* behind it:
- [e.g., Forward P/E of Xx looks high, but EPS is growing +X% — PEG of X.Xx is below the industry's X.Xx, meaning you're getting faster growth at a lower relative price]
- [e.g., Premium to peers is earned: X% net margin vs industry X%, and ROE of X% vs peers at X%]
- [e.g., Analyst consensus of $XXX implies +X% upside — X of X analysts rated Buy]
- [e.g., Dominant position in [AI/cloud/semiconductor/etc.] — a secular trend that could sustain elevated multiples for years]
- [e.g., DCF base case of $XXX suggests stock is fairly valued; bull case of $XXX implies meaningful upside if growth holds]

## Bearish Case

*Why the stock could be overvalued — and what could go wrong.*

3–5 data-backed bullets. For each point, explain the *mechanism* of the risk:
- [e.g., Trading at Xx EV/EBITDA vs peers at Xx — the premium leaves no room for execution misses; a single earnings miss could compress multiples sharply]
- [e.g., Revenue growth decelerating from +X% to +X% — if the slowdown continues, today's P/E of Xx becomes tomorrow's expensive multiple]
- [e.g., DCF bear case of $XXX implies −X% downside if growth assumptions prove optimistic]
- [e.g., [Specific risk]: export controls / competition / customer concentration / regulatory pressure — explain how it would directly reduce earnings or multiples]
- [e.g., High P/S of Xx requires sustained margin expansion to be justified — if margins plateau, the stock could re-rate lower]

**Value trap check** (include this paragraph if the stock looks cheap): If the stock is trading at a discount to peers or historical averages, state plainly whether this is likely a temporary opportunity or a structural problem. A value trap typically shows declining revenue, an eroding competitive moat, or a business model disrupted by new technology or competition.

---

## Valuation Analysis Rating

**Rating Scale:**
- **5/5 — Highly Attractive**: Significantly undervalued (>30% upside to fair value), low PEG, compelling margin of safety
- **4/5 — Attractive**: Modestly undervalued (10–30% upside), multiples reasonable relative to growth and quality
- **3/5 — Fairly Valued**: Trading near fair value (within ~10%), multiples in line with history and peers
- **2/5 — Unattractive**: Modestly overvalued (10–30% downside risk), premium not fully justified by fundamentals
- **1/5 — Highly Unattractive**: Significantly overvalued (>30% downside), extreme multiples unsupported by fundamentals

**Rating: X/5**
**Justification**: [2–3 sentences: cite the key multiple(s), compare to peers/history, state the upside/downside to fair value, and name the single biggest factor that would change this rating.]

---

## Save to Word Document

Write and execute a Python script using `python-docx` (`.venv/Scripts/python`) that:
- Narrow margins (0.5 inch all sides)
- Title: `{TICKER} — Valuation Analysis` (bold heading) + date subtitle
- Embeds both chart images after the title
- Section headings as Heading 1; bullets as Word list items
- **Tables: initialize with `rows=1` (header only), then `table.add_row()` per data row**
- Dark blue header rows (fill `1F3864`), white bold text; source citations in small italic
- Rating block in bold
- Saves to `Outputs/{TICKER}/{ticker_lowercase}_valuation_analysis.docx`

Confirm the output file path when done.
