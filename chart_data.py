"""
Sidecar chart data for the interactive HTML reports.

Each chart_*.py script calls save_chart_data() next to every PNG it writes, so
report_renderer.py can draw the same chart interactively in the HTML version
(hover tooltips, legend toggles, data table) while the .docx keeps the PNG.
The sidecar for `x.png` is `x.chart.json`.

Schemas (values are raw numbers in the `unit`, None for a missing point):
  bar / line: {"kind": "bar"|"line", "title": str, "unit": "usd"|"pct"|"x"|"num",
               "categories": [str, ...],
               "series": [{"name": str, "values": [...], "notes": [str|None, ...]}, ...]}
               `notes` (optional) are per-point annotations shown in the tooltip (e.g. "1.6x NI")
               series options: "slot": 1-8 (borrow that palette slot's color), "faded": true (consensus /
               estimates), "dashed": true, "width": px (lines)
               chart options: "category_notes": [str|None, ...] (tooltip header + data-table column),
               "refs": [{"value": 70, "label": "Overbought"}, ...] (dashed reference lines),
               "y_min" / "y_max" (fixed axis bounds),
               "overlay" (bar charts only): a line on its own right-hand axis, lifted above the bars —
               {"name": str, "unit": "price", "slot": int, "points": [per-category value|None] (diamond markers,
               labeled), "daily": {"x": [fractional category index], "y": [...], "last_label": str} (optional)}
               units: "usd" ($ auto-scaled B/M/K), "price" ($X.XX), "pct", "x" (multiples), "num"
  waterfall:  {"kind": "waterfall", "title": str, "unit": "usd",
               "steps": [{"label": str, "value": num, "total": bool}, ...]}
               a `total` step is drawn from zero; other steps float from the running total
"""
import json
import math


def _clean(v):
    if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
        return None
    return v


def chart_data_path(png_path):
    return png_path[:-4] + ".chart.json" if png_path.endswith(".png") else png_path + ".chart.json"


def save_chart_data(png_path, data):
    def walk(o):
        if isinstance(o, dict):
            return {k: walk(v) for k, v in o.items()}
        if isinstance(o, list):
            return [walk(v) for v in o]
        return _clean(o)
    with open(chart_data_path(png_path), "w", encoding="utf-8") as f:
        json.dump(walk(data), f, ensure_ascii=False)
