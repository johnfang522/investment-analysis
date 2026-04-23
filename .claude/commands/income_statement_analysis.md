# Income Statement Analysis

You are an expert equity research analyst writing a concise 2–3 page income statement analysis for a general investor audience. Be clear, data-driven, and accessible — avoid jargon where possible.

**DATA SOURCING (follow this order):**
1. Load `Outputs/{TICKER}/{ticker_lowercase}_income_statement_quarterly.json` and `Outputs/{TICKER}/{ticker_lowercase}_quick_metrics.json`. Focus on the most recent quarter (first column). If files are missing, run `yahoo_finance_data.py` to fetch.
2. Only use WebSearch for values genuinely missing from the JSON (analyst estimates, guidance). Do not search for data already available locally.
3. For any value still not found, leave as N/A.

**CRITICAL: Always compare year-over-year (e.g., Q4 2025 vs Q4 2024). Never compare sequential quarters.**

**WRITING STYLE:**
- Max 2–3 bullet points per section. Be specific — cite actual numbers.
- Use tables for all multi-metric data. Show margins alongside dollar figures in the same row.
- Bold key metrics. No filler or repetition.
- Plain English: explain what each metric means in one phrase if it's not obvious (e.g., "gross margin — how much revenue the company keeps after production costs").

**SOURCE CITATIONS:** When using WebSearch data, put `Source: URL` on an indented new line below the content. No inline URLs. Yahoo Finance / local JSON needs no citation.

---

FORMAT YOUR RESPONSE EXACTLY AS FOLLOWS:

**Data as of**: [Fiscal Quarter] [Year] (Earnings reported: [Date])

## Income Statement Charts

Run the chart script to generate both charts:

```
.venv/Scripts/python chart_income_statement.py {TICKER}
```

This produces:
- `Outputs/{TICKER}/{ticker_lowercase}_income_statement_flow.png` — Sankey-style income flow for the most recent quarter
- `Outputs/{TICKER}/{ticker_lowercase}_income_statement_trend.png` — Quarterly trend line (Revenue, Gross Profit, Operating Income, Net Income)

---

## Revenue

*Revenue is the total sales a company generates — the "top line."*

Search for revenue analyst estimates (WebSearch) before creating this table.

| Period | Revenue | Analyst Est. | Beat/Miss | YoY Growth |
|--------|---------|--------------|-----------|------------|
| [Current Quarter] | $XX.XB | $XX.XB | +/-$X.XB | +X.X% |
| [Prior Year Quarter] | $XX.XB | $XX.XB | +/-$X.XB | +X.X% |

- Beat/miss vs expectations and what drove it
- Top revenue segments or geographies (include a pie chart if segment data is available)

## Profitability Snapshot

*This table shows how much of each revenue dollar the company keeps at each level — gross profit (after production costs), operating income (after all operating expenses), and net income (the final "bottom line").*

Search for gross profit, operating income, and net income analyst estimates (WebSearch) before creating this table.

| Period | Gross Profit | Gross Margin | Operating Income | Op. Margin | Net Income | Net Margin | EPS | EPS Est. | Beat/Miss |
|--------|--------------|--------------|-----------------|------------|------------|------------|-----|----------|-----------|
| [Current Quarter] | $XX.XB | XX.X% | $XX.XB | XX.X% | $XX.XB | XX.X% | $X.XX | $X.XX | +/-$X.XX |
| [Prior Year Quarter] | $XX.XB | XX.X% | $XX.XB | XX.X% | $XX.XB | XX.X% | $X.XX | $X.XX | +/-$X.XX |

- Whether margins expanded or compressed YoY and why
- EPS beat/miss significance and earnings quality (recurring vs one-time items)

## Operating Expenses

*Operating expenses are the costs of running the business beyond production — R&D, sales, and administrative costs.*

| Period | R&D | % Rev | SG&A | % Rev | Total OpEx | % Rev |
|--------|-----|-------|------|-------|------------|-------|
| [Current Quarter] | $XX.XB | XX% | $XX.XB | XX% | $XX.XB | XX% |
| [Prior Year Quarter] | $XX.XB | XX% | $XX.XB | XX% | $XX.XB | XX% |

- Key expense trends and whether the company is gaining or losing operating leverage

## Outlook & Guidance

Search for forward estimates and guidance (WebSearch) before creating this table.

| Metric | Next Quarter Est. | Full Year Est. | Company Guidance | vs. Consensus |
|--------|-------------------|----------------|------------------|---------------|
| Revenue | $XX.XB | $XX.XB | $XX–XXB | In-line/Above/Below |
| EPS | $X.XX | $X.XX | $X.XX–X.XX | In-line/Above/Below |
| Gross Margin | XX% | XX% | XX–XX% | — |

- Key guidance takeaways and analyst sentiment

## Strengths & Risks

**Strengths:**
- [2–3 specific positives — e.g., revenue beat, margin expansion, strong operating leverage]

**Risks:**
- [2–3 specific concerns — e.g., margin compression, rising costs, guidance cut, competitive pressure]

---

## Income Statement Rating

**Rating Scale:** 5 = exceptional (>20% YoY growth, expanding margins, consistent beats) · 4 = strong (10–20%) · 3 = average (5–10%) · 2 = below average (<5%) · 1 = poor (decline/losses)

**Rating: X/5**
**Justification**: [2–3 sentences with specific evidence: revenue growth rate, margin trend, EPS beat/miss]

---

## Save to Word Document

Write and execute a Python script using `python-docx` (`.venv/Scripts/python`) that:
- Narrow margins (0.5 inch all sides)
- Title: `{TICKER} — Income Statement Analysis` (large bold heading) + date subtitle
- Embeds both chart images after the title
- Section headings as Heading 1
- Bullets as actual Word list items
- Tables as Word tables with header row formatting. **CRITICAL: initialize tables with `rows=1` (header only), then call `table.add_row()` for each data row — do NOT pass `rows=1+len(data)` upfront or blank rows will appear between the header and data.**
- Source citations in small italic font
- Rating block in bold
- Saves to `Outputs/{TICKER}/{ticker_lowercase}_income_statement_analysis.docx`

Confirm the output file path when done.
