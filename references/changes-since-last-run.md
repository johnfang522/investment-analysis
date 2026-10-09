# Changes since the last run

Reports keep history (every filename ends in `_YYYYMMDD`). When a skill is re-run and an earlier run of the **same skill, same ticker/theme** exists, it is no longer initial coverage: the new report must say what changed, so the PM reads the delta first.

## Procedure (every skill that carries this block)

1. **Before writing the spec**, find the prior run (strictly earlier date than today's run date):
   `PYTHONIOENCODING=utf-8 .venv/Scripts/python prior_run.py {PREFIX} {YYYYMMDD}`
   `{PREFIX}` is the skill's spec path without `_{YYYYMMDD}_spec.json` (given in the skill's own block). It prints `{"prior": null}` or the prior run's date, `_summary.json` content (signal, conviction, key figures, variant view, red flags) and the path of its `_spec.json`.
2. **`prior` is null** → initial coverage. Add no section; use the skill's normal "Initiating Coverage" wording.
3. **`prior` exists** → label the report "Coverage Date" / "Update", and add a **"What Changed Since {prior date}"** section **immediately after the verdict / read-through / opening block**, before the rest of the analysis.
   - A `table` with headers `Item | Prior ({prior date}) | Now | What changed and why it matters`, one row per item in the skill's checklist (below) that moved materially. Colour the "Now" cell (`C6EFCE` improved / `FFC7CE` worsened / `FFEB9C` mixed) via `fills`.
   - Then `bullets`: **Net read** (thesis intact / strengthened / weakened, and whether signal or conviction moved: prior → now), **Driver** (the sourced event behind the move: filing, print, news; cite it), and **Prior triggers** (which of the prior run's "what flips it" / thesis-breakers / entry levels have since fired or not).
   - Read the prior spec (`prior.spec`) only when the summary lacks a figure you need to compare; never recompute a prior figure from today's data: quote it from the prior report and label it with the prior date.
   - Unchanged items are omitted. If nothing material moved, write one line saying so with the prior date. Do not pad.
4. Add to the spec's `summary`: `"changes_since": {"date": "{prior YYYY-MM-DD}", "net_read": "intact|strengthened|weakened", "headline": "one line"}` so a parent skill (e.g. `/single_stock_deep_research`) can roll it up.
5. Final reply: one extra line, the net read and the single biggest change.
