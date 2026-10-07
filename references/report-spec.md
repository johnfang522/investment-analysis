# Writing a report spec (shared by every skill that saves a report)

Skills do **not** write python-docx or HTML code. They write the document's content as a JSON spec and run the shared renderer, which produces the house-style `.docx`, an offline interactive `.html` twin (charts drawn from the `.chart.json` files the `chart_*.py` scripts save next to their PNGs), a `_summary.json` for `/single_stock_deep_research`, and a refreshed `Outputs/index.html` library page.

```
PYTHONIOENCODING=utf-8 .venv/Scripts/python report_renderer.py Outputs/{TICKER}/{n}_{ticker}_{skill}_spec.json
```

On a `ValueError` (unknown block, missing key, ragged row) fix the spec and re-run — never fall back to a hand-written script. The full schema is the `report_renderer.py` docstring; read it only if something below is unclear.

## Spec skeleton

```json
{"ticker": "NVDA", "skill": "balance_sheet", "title": "NVDA — Balance Sheet",
 "subtitle": "Buy-side balance sheet read · October 7, 2026 · Data as of: Q2 FY2027 (quarter ended July 26, 2026)",
 "output": "Outputs/NVDA/4_nvda_balance_sheet_analysis.docx",
 "blocks": [ ... ],
 "summary": {"as_of": "...", "thesis_bias": "LONG|SHORT|PASS",
             "key_figures": [{"label": "...", "value": "...", "source": "..."}], "red_flags": ["..."]}}
```

## Blocks

| Block | Shape | Notes |
|---|---|---|
| heading | `{"type": "heading", "text": "At a Glance"}` | each `##` section of the skill's outline; `"level": 2` for a sub-heading |
| paragraph | `{"type": "paragraph", "text": "..."}` | rare — house style is bullets |
| bullets | `{"type": "bullets", "items": ["**Label:** text", ...]}` | |
| table | `{"type": "table", "headers": [...], "rows": [[...]], "source": "...", "bold_rows": [i], "fills": [[row, col, "C6EFCE"]], "sortable": true}` | every table has a `source`; fills: `C6EFCE` good / `FFEB9C` watch / `FFC7CE` bad / `F2F2F2` estimate; `sortable` only for peer/screen tables |
| chart | `{"type": "chart", "path": "Outputs/NVDA/nvda_cash_flow_trend.png", "source": "SEC EDGAR"}` | interactive in HTML automatically when the chart script wrote a sidecar |
| source | `{"type": "source", "text": "..."}` | standalone citation line |
| variant_view | `{"type": "variant_view", "rows": [[debate, consensus, our_read]], "source": "...", "edge": "...", "note": "..."}` | renders its own heading — mandatory in every note |
| read_through | `{"type": "read_through", "signal": "BULLISH|NEUTRAL|BEARISH", "dimension": "Cash-Flow-Quality", "conviction": 6, "so_what": "...", "what_flips": "..."}` | component skills; renders its own heading |
| verdict | `{"type": "verdict", "bias": "LONG|SHORT|PASS|AVOID", "conviction": 7, "rows": [["Current Price", "$X.XX"], ...], "bullets": ["**Justification:** ..."], "source": "..."}` | full-call skills; 2-column rows = the skill's Verdict table; renders its own heading and the colored bias line |
| income_trend | `{"type": "income_trend", "cadence": "annual|quarterly", "source": "..."}` | income-statement trend table built from the chart's own rows — never re-type them |
| page_break | `{"type": "page_break"}` | |

## Rules

- Follow the skill's outline in order; `variant_view`, `read_through` and `verdict` replace the matching `##` sections (no extra heading block).
- Paste figures exactly as `digest.py` / `compute_metrics()` print them; don't recompute or reformat a figure a script already gives. Format any other dollar amount like `fmt_value()` (`$1.23B`, `$45.6M`).
- Text formatting: `**bold**`, `*italic*`; a `\n` escape inside a JSON string is a line break in a table cell. Status icons (✅ ⚠️ 🔴 ↑ ↓ →) go straight into the text.
- Every quantitative figure carries a source — in the table's `source`, a `source` block, or inline.
- `summary.key_figures`: the 5–8 numbers `/single_stock_deep_research` most needs from this dimension, each with its source. The first three also appear as header tiles on the web page, so keep values short (put context in parentheses: `"$21.40B (+58.9% YoY)"`).
- `summary.thesis_bias` mirrors the skill's Thesis Bias row; signal and conviction are taken from the `read_through` / `verdict` block automatically.

## Final reply

The documents are the deliverable. Reply with only: the `.html` and `.docx` paths, `Signal · Conviction X/10 · Thesis bias`, the so-what (component) or justification (full-call) line, and the 3 most important key figures with sources. When invoked by `/single_stock_deep_research`, follow the reply shape in its prompt instead.
