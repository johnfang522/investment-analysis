# Growth & Profitability Analysis

You are a financial analyst writing a plain-English growth and profitability analysis for a general investor. Be concise — lead with numbers, skip filler, one or two bullets per section maximum.

**DATA SOURCING (follow this order):**
1. Load `Outputs/{TICKER}/{ticker_lowercase}_income_statement_quarterly.json`, `Outputs/{TICKER}/{ticker_lowercase}_income_statement_annual.json`, and `Outputs/{TICKER}/{ticker_lowercase}_quick_metrics.json`. If files are missing, run `yahoo_finance_data.py` to fetch.
2. Use quarterly JSON for all current/prior-year-quarter metrics. Use annual JSON only for multi-year CAGRs.
3. Compute EPS as Net Income / Shares Outstanding (`sharesOutstanding` from quick_metrics) if the EPS field in the JSON is zero or missing.
4. Only use WebSearch for analyst estimates and forward guidance — not for anything available locally.
5. Leave as N/A if still not found.

**Always compare year-over-year. Never compare sequential quarters.**

**SOURCE CITATIONS:** `Source: URL` indented below any web-sourced value. No citation needed for local JSON.

---

FORMAT YOUR RESPONSE EXACTLY AS FOLLOWS:

**Data as of**: [Fiscal Quarter] [Year]

## Charts

Run the chart script to generate all three charts:

```
.venv/Scripts/python chart_growth_profitability.py {TICKER}
```

This produces:
- `Outputs/{TICKER}/{ticker_lowercase}_gp_revenue_trend.png` — Revenue & Gross Profit grouped bar + Gross Margin % line (last 5 quarters)
- `Outputs/{TICKER}/{ticker_lowercase}_margin_trend.png` — Gross / Operating / Net Margin trend lines (last 5 quarters)
- `Outputs/{TICKER}/{ticker_lowercase}_yoy_growth.png` — Annual YoY Revenue & Net Income growth bars

---

## 1. Revenue Growth

*Revenue = total sales. Growing revenue means the business is expanding.*

| Period | Revenue | YoY Growth | Gross Profit | Gross Margin |
|--------|---------|------------|--------------|--------------|
| [Current Quarter] | $XX.XB | +X.X% | $XX.XB | XX.X% |
| [Prior Year Quarter] | $XX.XB | — | $XX.XB | XX.X% |

- Is growth accelerating or decelerating? Name the primary driver.
- Gross margin direction: expanding = pricing power or scale; compressing = rising costs.

## 2. Profitability

*Margins show how much of each revenue dollar becomes profit at each level.*

| Period | Gross Margin | Op. Margin | Net Margin | Op. Leverage* |
|--------|-------------|------------|------------|---------------|
| [Current Quarter] | XX.X% | XX.X% | XX.X% | X.Xx |
| [Prior Year Quarter] | XX.X% | XX.X% | XX.X% | X.Xx |

*Op. leverage = Operating Income growth ÷ Revenue growth. Above 1x means costs are scaling slower than revenue.*

- Are all three margins moving in the same direction? Divergence (e.g., gross up but net down) signals a specific cost problem worth naming.

## 3. Bottom-Line Growth

*EPS (earnings per share) is the profit allocated to each share you own.*

| Period | Operating Income | Op. Margin | Net Income | Net Margin | EPS | YoY EPS Growth |
|--------|-----------------|------------|------------|------------|-----|----------------|
| [Current Quarter] | $XX.XB | XX.X% | $XX.XB | XX.X% | $X.XX | +X.X% |
| [Prior Year Quarter] | $XX.XB | XX.X% | $XX.XB | XX.X% | $X.XX | — |

- Is net income growing faster or slower than revenue? Faster = real operating leverage.
- Is EPS growth matching net income growth? If EPS grows much faster, it's buyback-driven, not earnings quality.

## 4. Multi-Year Scorecard

*CAGR = the steady annual rate that would produce the same result over the period. Computed from annual JSON.*

| Metric | 1-Year | 3-Year CAGR | 5-Year CAGR |
|--------|--------|-------------|-------------|
| Revenue | +X% | +X% | +X% |
| Gross Profit | +X% | +X% | +X% |
| Operating Income | +X% | +X% | +X% |
| Net Income | +X% | +X% | +X% |
| EPS | +X% | +X% | +X% |

Use N/A if fewer than 3 or 5 years of annual data are available.

- One sentence: is growth consistent across all lines, or is one lagging?

## 5. Forward Estimates

Search WebSearch for consensus analyst estimates.

| Metric | Next Quarter Est. | Full Year Est. | Company Guidance |
|--------|-------------------|----------------|------------------|
| Revenue | $XX.XB | $XX.XB | $XX–XXB |
| EPS | $X.XX | $X.XX | $X.XX–X.XX |
| Revenue Growth (YoY) | +X% | +X% | — |

- One sentence: is the market expecting growth to accelerate or slow down?

---

## Strengths

3 bullet points, numbers required.

## Risks

3 bullet points, numbers required.

---

## Rule of 40 Summary

*The Rule of 40 is a quick health check for a business: add its revenue growth rate and its operating profit margin. A score above 40 means the company is balancing growth and profitability well. Below 40 is a warning sign.*

**Formula: Revenue Growth % (YoY) + Operating Margin %**

| Period | Revenue Growth | Operating Margin | Rule of 40 Score | Assessment |
|--------|---------------|-----------------|-----------------|------------|
| [Current Quarter] | +X.X% | XX.X% | XX | ✅ Healthy / ⚠️ Watch / ❌ Concern |
| [Prior Year Quarter] | +X.X% | XX.X% | XX | ✅ / ⚠️ / ❌ |

Thresholds: **≥40 = healthy** · **30–39 = watch** · **<30 = concern**

Also compute using FCF margin in place of operating margin as an alternative view (read FCF and revenue from `_cash_flow_statement_quarterly.json`):

| Period | Revenue Growth | FCF Margin | Rule of 40 (FCF) | Assessment |
|--------|---------------|------------|-----------------|------------|
| [Current Quarter] | +X.X% | XX.X% | XX | ✅ / ⚠️ / ❌ |
| [Prior Year Quarter] | +X.X% | XX.X% | XX | ✅ / ⚠️ / ❌ |

**Overall Rating: X/5**

Scale: 5 = exceptional (Rule of 40 ≥ 60, expanding margins, consistent multi-year growth) · 4 = strong (40–59) · 3 = average (Rule of 40 30–39 or growth slowing) · 2 = weak · 1 = poor

[2 sentences: Rule of 40 score, margin trend direction, and biggest growth risk.]

---

## Save to Word Document

Write and execute a Python script using `python-docx` (`.venv/Scripts/python`) that:
- Narrow margins (0.5 inch all sides)
- Title: `{TICKER} — Growth & Profitability Analysis` (bold heading) + date subtitle
- Embeds all three chart images after the title
- Section headings as Heading 1; bullets as Word list items
- **Tables: initialize with `rows=1` (header only), then `table.add_row()` per data row**
- Dark blue header rows (fill `1F3864`), white bold text; source citations in small italic
- Rating block in bold
- Saves to `Outputs/{TICKER}/{ticker_lowercase}_growth_and_profitability_analysis.docx`

Confirm the output file path when done.
