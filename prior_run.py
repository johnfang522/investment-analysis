"""
Find the previous run of a report so a skill can say what changed since then.

Usage:
    .venv/Scripts/python prior_run.py PREFIX [YYYYMMDD]

PREFIX is the report's output path without the date and extension, exactly as the skill names it,
e.g. `Outputs/NVDA/8_nvda_technical_analysis` or `Outputs/market_sentiment_analysis`
(the `emerging_industry_trends_{theme}` style prefixes include the theme, so only the same theme
is compared). The optional date is today's run date (default: today); only runs dated strictly
before it count, so a same-day re-run compares against the last earlier day.

Prints one JSON object: `{"prior": null}` when there is no earlier run (this is initial coverage),
otherwise `{"prior": {"date", "spec", "summary_path", "summary", "key_figures_by_label"}}`.
"""

import glob
import json
import os
import re
import sys
from datetime import date


def find_prior(prefix: str, today: str = None) -> dict | None:
    today = today or date.today().strftime("%Y%m%d")
    pat = re.compile(re.escape(os.path.basename(prefix)) + r"_(\d{8})_summary\.json$")
    best = None
    for path in glob.glob(prefix + "_*_summary.json"):
        m = pat.fullmatch(os.path.basename(path))
        if m and m.group(1) < today and (best is None or m.group(1) > best[0]):
            best = (m.group(1), path)
    if not best:
        return None
    d, path = best
    with open(path, encoding="utf-8") as f:
        summary = json.load(f)
    spec = path.replace("_summary.json", "_spec.json")
    figs = summary.get("key_figures") or []
    return {"date": d, "spec": spec if os.path.exists(spec) else None, "summary_path": path,
            "summary": summary,
            "key_figures_by_label": {k.get("label"): k.get("value") for k in figs if isinstance(k, dict)}}


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    prior = find_prior(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
    print(json.dumps({"prior": prior}, indent=2, ensure_ascii=False))
