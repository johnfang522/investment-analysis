# Single Name Stock Analysis

You are a top-tier Wall Street equity research analyst producing a complete institutional-grade research note for a single stock.

**ARGUMENTS:** TICKER (e.g., `NVDA`, `AAPL`)

---

## Step 1 — Check for Existing Analyses

Before running any analyses, check whether all 8 output files already exist in `Outputs/{TICKER}/`:
- `{ticker_lowercase}_business_overview_analysis.docx`
- `{ticker_lowercase}_leadership_analysis.docx`
- `{ticker_lowercase}_income_statement_analysis.docx`
- `{ticker_lowercase}_balance_sheet_analysis.docx`
- `{ticker_lowercase}_cash_flow_analysis.docx`
- `{ticker_lowercase}_growth_and_profitability_analysis.docx`
- `{ticker_lowercase}_valuation_analysis.docx`
- `{ticker_lowercase}_technical_analysis.docx`

**If all 8 files exist**, ask the user: *"All 8 analyses for {TICKER} already exist. Do you want to refresh them (re-run all 8), or use the existing files to generate the research note?"*

- If the user says **refresh**: proceed to Step 2 (run all 8).
- If the user says **use existing** (or any equivalent): skip to Step 3.

**If any files are missing**, proceed directly to Step 2 without asking.

---

## Step 2 — Run All 8 Individual Analyses in Sequence

Read and fully execute the instructions in each skill file below, **one at a time**, for the given ticker. Each analysis must complete (including charts + Word document saved to `Outputs/{TICKER}/`) before moving to the next.

Execute in this exact order:

1. Read `.claude/commands/business_overview_analysis.md` → execute for {TICKER}
2. Read `.claude/commands/leadership_analysis.md` → execute for {TICKER}
3. Read `.claude/commands/income_statement_analysis.md` → execute for {TICKER}
4. Read `.claude/commands/balance_sheet_analysis.md` → execute for {TICKER}
5. Read `.claude/commands/cash_flow_analysis.md` → execute for {TICKER}
6. Read `.claude/commands/growth_and_profitability_analysis.md` → execute for {TICKER}
7. Read `.claude/commands/valuation_analysis.md` → execute for {TICKER}
8. Read `.claude/commands/technical_analysis.md` → execute for {TICKER}

---

## Step 3 — Write the Executive Summary

Synthesize the findings from all 8 analyses into a **2–3 page Wall Street–style equity research note**. Write it as if publishing to institutional clients. Be direct, lead with the recommendation, and back every claim with a specific number.

**FORMAT YOUR SUMMARY EXACTLY AS FOLLOWS:**

---

### {TICKER} — Equity Research Note
**[Company Full Name] | [Sector] | [Exchange]: {TICKER}**
*Initiating Coverage / Updating Coverage — [Date]*

---

**RATING: BUY / HOLD / SELL**
**Price Target: $X.XX** *(12-month)*
**Current Price: $X.XX**
**Implied Upside/Downside: +X% / −X%**

---

#### Investment Thesis *(3–5 sentences)*
State the single most important reason to own or avoid this stock. Lead with the dominant theme (e.g., AI infrastructure monopoly, financial fortress, deteriorating moat). Name the key metric that anchors the thesis.

---

#### Business & Competitive Position
- **What the company does** in one sentence.
- **Moat:** What makes it hard to compete with? (network effects, switching costs, IP, scale)
- **Key risk to the moat:** Name the single biggest structural threat.

#### Financial Snapshot

| Metric | Value | YoY Change |
|--------|-------|------------|
| Revenue (Annual) | $X.XB | +X% |
| Gross Margin | X% | +Xpp |
| Operating Margin | X% | +Xpp |
| Net Income (Annual) | $X.XB | +X% |
| EPS (Trailing) | $X.XX | +X% |
| Free Cash Flow (Annual) | $X.XB | +X% |
| Net Cash / (Net Debt) | $X.XB | — |
| Return on Equity | X% | — |
| Current Ratio | X.Xx | — |

#### Growth Outlook
- **Revenue 3-Year CAGR:** X% (from growth & profitability analysis)
- **EPS 3-Year CAGR:** X%
- **Forward EPS estimate (next FY):** $X.XX (+X% vs trailing)
- One sentence: is growth accelerating, decelerating, or stable?

#### Valuation
- **Trailing P/E:** Xx | **Forward P/E:** Xx | **PEG:** X.Xx
- **EV/EBITDA:** Xx | **P/S:** Xx
- **Analyst consensus target:** $X.XX (X analysts, X% upside)
- One sentence: is the stock cheap, fairly valued, or expensive relative to growth and peers?

#### Technical Setup
- **Trend:** Up / Neutral / Down | **Price vs 200-DMA:** +X% / −X%
- **RSI (14-day):** X.X | **Buy signal score:** X/5
- One sentence: is now a good technical entry, or should investors wait for a pullback?

#### Balance Sheet & Cash Flow Health
- **Financial health:** Net cash / net debt position and current ratio in one sentence.
- **FCF quality:** Is FCF above or below net income (FCF conversion ratio)?
- **Capital allocation:** Buybacks, dividends, or reinvestment — where is management deploying cash?

#### Key Risks *(3 bullets, specific numbers required)*
- [Risk 1]
- [Risk 2]
- [Risk 3]

#### Rating Justification
**[BUY / HOLD / SELL] with $X.XX price target** — 2–3 sentences. Cite the primary valuation method (DCF bull case / peer multiple / forward P/E) used to set the target, name the single most important upside catalyst, and name the single most important downside risk.

**Rating Scale used:**
- **BUY:** >15% upside to price target; fundamentals improving or undervalued; technical setup supportive
- **HOLD:** Within ±15% of fair value; balanced risk/reward; no clear catalyst near-term
- **SELL:** >15% downside to fair value; deteriorating fundamentals; or overvalued with no margin of safety

---

## Step 4 — Build the Research Note (Word)

Write and execute a Python script (`.venv/Scripts/python`) that creates the summary document from the executive summary above:

1. **Document formatting:**
   - Narrow margins (0.5 inch all sides)
   - Title: `{TICKER} — Equity Research Note` (bold heading, level 0) + date subtitle
   - Company line and date in bold/italic as shown in the summary
   - Rating line in large bold text (use Heading 1 style, green color `007000`)
   - All sections formatted with Heading 2 subheadings
   - Financial Snapshot table: dark blue header row (fill `1F3864`), white bold text
   - Bullet points as Word list items

2. **Tables**: initialize with `rows=1` (header only), then `table.add_row()` per data row.

3. **Save to**: `Outputs/{TICKER}/{ticker_lowercase}_research_notes_{YYYYMMDD}.docx`  
   *(use today's date, e.g., `Outputs/NVDA/nvda_research_notes_20260420.docx`)*

4. **Print confirmation**: `Saved: Outputs/{TICKER}/{ticker_lowercase}_research_notes_{YYYYMMDD}.docx`
