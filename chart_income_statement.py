"""
chart_income_statement.py TICKER

Generates charts saved to Outputs/{TICKER}/:
  1. {ticker}_income_statement_flow.png             — Sankey-style flow (most recent quarter)
  2. {ticker}_income_statement_annual_trend.png     — Annual $ bars (amount, YoY, margins) + share price: last 5 FYs + TTM + consensus FYs
  3. {ticker}_income_statement_quarterly_trend.png  — Quarterly $ bars, same format: last 8 quarters + up to 4 consensus quarters
Consensus comes from {ticker}_consensus_estimates.json (written by /income_statement_analysis from
WebSearch); without it, charts 2-3 show actuals only.
annual_trend_rows() / quarterly_trend_rows() are imported by the skill's Word script for the tables.
"""
import json, re, sys, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.lines import Line2D
from matplotlib.path import Path


def load_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except Exception:
        return {}


def get_series(data, *keys, n=8, exclude_ttm=True):
    """Return list of (date_str, value) sorted newest-first from a quarterly JSON."""
    for k in keys:
        raw = data.get(k)
        if raw and isinstance(raw, dict):
            items = [(d, v) for d, v in raw.items()
                     if v is not None and (not exclude_ttm or d != "TTM")]
            items.sort(key=lambda x: x[0], reverse=True)
            return items[:n]
    return []


def latest(series):
    return series[0][1] if series else None


def smart_scale(values):
    """Return (divisor, axis_label, suffix) based on max absolute value across all series."""
    flat = [v for v in values if v is not None]
    max_abs = max((abs(v) for v in flat), default=0)
    if max_abs >= 1e9: return 1e9, 'Billions USD', 'B'
    if max_abs >= 1e6: return 1e6, 'Millions USD', 'M'
    if max_abs >= 1e3: return 1e3, 'Thousands USD', 'K'
    return 1, 'USD', ''


def sfmt(v, div, suffix, dec=2):
    """Format a dollar value given a pre-determined scale divisor."""
    if v is None: return ''
    sign = '-' if v < 0 else ''
    return f"{sign}${abs(v)/div:.{dec}f}{suffix}"


def quarter_label(date_str):
    from datetime import datetime
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return f"Qtr Ended {dt.strftime('%b %Y')}"
    except Exception:
        return date_str

def period_label(date_str):
    """Return 'Quarter Ended Mon YYYY' — avoids calendar-vs-fiscal quarter mismatch."""
    from datetime import datetime
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return f"Quarter Ended {dt.strftime('%b %Y')}"
    except Exception:
        return date_str


# ── Chart 1: Income statement flow — Sankey (profitable) or waterfall (loss) ─

def chart_flow(ticker, data, out_path):
    t = ticker.upper()
    rev_s   = get_series(data, "Total Revenue")
    cogs_s  = get_series(data, "Cost Of Revenue", "Cost of Revenue")
    gp_s    = get_series(data, "Gross Profit")
    oi_s    = get_series(data, "Operating Income", "Total Operating Income As Reported", "EBIT")
    ni_s    = get_series(data, "Net Income", "Net Income Common Stockholders")
    opex_s  = get_series(data, "Operating Expense", "Total Operating Expenses")

    rev  = latest(rev_s)
    cogs = latest(cogs_s)
    gp   = latest(gp_s)
    oi   = latest(oi_s)
    ni   = latest(ni_s)

    if rev is None:
        print(f"  [income flow] Missing Revenue for {ticker}"); return

    # Derive missing values. Note: when both cogs and gp are missing (e.g. a
    # filer that stopped tagging Cost of Revenue/Gross Profit in XBRL with
    # no successor, like ORCL since FY2018), the gp = rev * 0.5 fallback
    # below is a rough placeholder, not a real figure — cogs must still be
    # re-derived from it afterward, or it stays None and crashes _chart_flow_sankey/_waterfall's abs(cogs).
    if cogs is None and gp is not None: cogs = rev - gp
    if gp   is None and cogs is not None: gp = rev - cogs
    if gp   is None: gp = rev * 0.5
    if cogs is None: cogs = rev - gp
    opex = latest(opex_s)
    if opex is None: opex = gp - oi if oi is not None else None
    if oi   is None: oi = gp - (opex or 0)
    if ni   is None: ni = oi * 0.7
    interest_tax = oi - ni
    period = period_label(rev_s[0][0]) if rev_s else "MRQ"

    div, _, suffix = smart_scale([rev, cogs, gp, oi, ni, interest_tax])
    def B(v): return sfmt(v, div, suffix)

    # Route to waterfall when the company is loss-making (opex > gp → oi < 0)
    if oi < 0 or ni < 0:
        _chart_flow_waterfall(t, rev, cogs, gp, opex, oi, ni, interest_tax,
                              period, div, suffix, out_path)
    else:
        _chart_flow_sankey(t, rev, cogs, gp, opex, oi, ni, interest_tax,
                           period, div, suffix, B, out_path)


def _chart_flow_waterfall(t, rev, cogs, gp, opex, oi, ni, interest_tax,
                          period, div, suffix, out_path):
    def B(v): return sfmt(v, div, suffix)
    """Waterfall P&L chart — used when operating income or net income is negative."""
    opex_val = opex if opex is not None else (gp - oi)

    # Stages: label, delta from previous running total, bar color
    stages = [
        ("Revenue",        rev,            "#4285F4"),
        ("− COGS",        -cogs,           "#EA4335"),
        ("Gross Profit",   None,           "#34A853" if gp >= 0 else "#EA4335"),
        ("− OpEx",        -opex_val,       "#EA4335"),
        ("Op. Income",     None,           "#34A853" if oi >= 0 else "#EA4335"),
        ("− Int. & Tax",  -interest_tax,   "#EA4335" if interest_tax > 0 else "#34A853"),
        ("Net Income",     None,           "#34A853" if ni >= 0 else "#EA4335"),
    ]
    subtotals = {"Gross Profit": gp, "Op. Income": oi, "Net Income": ni}

    fig, ax = plt.subplots(figsize=(16, 9))
    running = 0
    bar_bottoms, bar_heights, bar_colors = [], [], []
    xs_pos = list(range(len(stages)))

    for label, delta, color in stages:
        if label in subtotals:
            val = subtotals[label]
            bar_bottoms.append(min(0, val) / div)
            bar_heights.append(abs(val) / div)
            bar_colors.append(color)
            running = val
        else:
            prev = running
            running += delta
            lo = min(prev, running) / div
            hi = max(prev, running) / div
            bar_bottoms.append(lo)
            bar_heights.append(hi - lo)
            bar_colors.append(color)

    bars = ax.bar(xs_pos, bar_heights, bottom=bar_bottoms, color=bar_colors,
                  width=0.55, alpha=0.88, zorder=2)

    # Connector lines between adjacent bars (dashed)
    running2 = 0
    levels = []
    for label, delta, _ in stages:
        if label in subtotals:
            levels.append(subtotals[label] / div)
            running2 = subtotals[label]
        else:
            running2 += delta
            levels.append(running2 / div)

    for i in range(len(xs_pos) - 1):
        # connect top of current bar to bottom of next if going down, else bottom to top
        y = levels[i]
        ax.plot([xs_pos[i] + 0.28, xs_pos[i + 1] - 0.28], [y, y],
                color="#888888", linestyle="--", linewidth=1.2, zorder=3)

    ax.axhline(0, color="#333333", linewidth=1.2, zorder=1)

    # Value labels above/below each bar
    BBOX = dict(boxstyle="round,pad=0.3", facecolor="white",
                edgecolor="#cccccc", alpha=0.9, linewidth=0.8)
    for i, (bar, (label, delta, color), level) in enumerate(zip(bars, stages, levels)):
        val_str = B(subtotals[label]) if label in subtotals else B(abs(delta) if delta is not None else 0)
        y_pos = level + (0.02 * (max(levels) - min(levels)) or 0.5)
        if label in subtotals and subtotals[label] < 0:
            y_pos = level - (0.05 * (max(levels) - min(levels)) or 0.5)
        if label in subtotals and rev:
            tag = {"Gross Profit": "GM", "Op. Income": "OM", "Net Income": "NM"}[label]
            val_str += f"\n({tag}: {subtotals[label] / rev * 100:.1f}%)"
        ax.text(i, y_pos, f"{label}\n{val_str}",
                ha="center", va="bottom" if level >= 0 else "top",
                fontsize=13, fontweight="bold", color="#111111", bbox=BBOX)

    ax.set_xticks(xs_pos)
    ax.set_xticklabels([s[0] for s in stages], fontsize=14)
    ax.tick_params(axis="y", labelsize=13)
    y_unit = f" ({suffix[0] if suffix else 'USD'})" if suffix else " (USD)"
    ax.set_ylabel(f"{'Millions' if suffix == 'M' else 'Billions' if suffix == 'B' else 'Thousands'} USD", fontsize=16)
    ax.set_title(f"{t} Quarterly Income Statement ({period})", fontsize=22, fontweight="bold", pad=16)
    ax.grid(axis="y", alpha=0.3, zorder=0)
    plt.tight_layout()
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {out_path}")


def _chart_flow_sankey(t, rev, cogs, gp, opex, oi, ni, interest_tax,
                       period, div, suffix, B, out_path):
    """Sankey-style flow chart — used when operating income AND net income are both positive."""
    opex_val = opex if opex is not None else (gp - oi)

    # Normalize to max absolute value so no bar can overflow the chart area
    max_scale = max(abs(v) for v in [rev, cogs, gp, opex_val, oi, ni, interest_tax] if v is not None)

    CHART_H = 0.80
    BASE = 0.10
    NODE_W = 0.035
    xs = [0.03, 0.27, 0.54, 0.78]

    def norm(v): return (abs(v) / max_scale) * CHART_H

    rev_h  = norm(rev)
    gp_h   = norm(gp)
    cogs_h = norm(cogs)
    oi_h   = norm(oi)
    opex_h = norm(opex_val)
    ni_h   = norm(ni)
    it_h   = norm(interest_tax)

    fig, ax = plt.subplots(figsize=(16, 9))
    ax.set_xlim(0, 1.0); ax.set_ylim(0, 1.0)
    ax.axis("off")
    ax.set_title(f"{t} Quarterly Income Statement ({period})",
                 fontsize=22, fontweight="bold", pad=16)

    # Draw bars
    ax.add_patch(patches.Rectangle((xs[0], BASE), NODE_W, rev_h,
                 transform=ax.transAxes, color="#4285F4", zorder=2))
    ax.add_patch(patches.Rectangle((xs[1], BASE + cogs_h), NODE_W, gp_h,
                 transform=ax.transAxes, color="#34A853", zorder=2))
    ax.add_patch(patches.Rectangle((xs[1], BASE), NODE_W, cogs_h,
                 transform=ax.transAxes, color="#EA4335", zorder=2))
    ax.add_patch(patches.Rectangle((xs[2], BASE + opex_h), NODE_W, oi_h,
                 transform=ax.transAxes, color="#34A853", zorder=2))
    ax.add_patch(patches.Rectangle((xs[2], BASE), NODE_W, opex_h,
                 transform=ax.transAxes, color="#EA4335", zorder=2))
    ax.add_patch(patches.Rectangle((xs[3], BASE + it_h), NODE_W, ni_h,
                 transform=ax.transAxes, color="#34A853", zorder=2))
    ax.add_patch(patches.Rectangle((xs[3], BASE), NODE_W, it_h,
                 transform=ax.transAxes, color="#EA4335", zorder=2))

    def bezier_band(ax, x0, y0_bot, y0_top, x1, y1_bot, y1_top, color="#DADADA", alpha=0.55):
        mx = (x0 + x1) / 2
        verts = [
            (x0, y0_bot), (mx, y0_bot), (mx, y1_bot), (x1, y1_bot),
            (x1, y1_top), (mx, y1_top), (mx, y0_top), (x0, y0_top),
            (x0, y0_bot),
        ]
        codes = [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4,
                 Path.LINETO, Path.CURVE4, Path.CURVE4, Path.CURVE4,
                 Path.CLOSEPOLY]
        path = Path(verts, codes)
        ax.add_patch(patches.PathPatch(path, facecolor=color, edgecolor="none",
                                       alpha=alpha, zorder=1,
                                       transform=ax.transAxes))

    x0e = xs[0] + NODE_W
    x1e = xs[1] + NODE_W
    x2e = xs[2] + NODE_W

    bezier_band(ax, x0e, BASE + cogs_h, BASE + rev_h, xs[1], BASE + cogs_h, BASE + cogs_h + gp_h)
    bezier_band(ax, x0e, BASE, BASE + cogs_h, xs[1], BASE, BASE + cogs_h)
    bezier_band(ax, x1e, BASE + cogs_h + opex_h, BASE + cogs_h + gp_h,
                xs[2], BASE + opex_h, BASE + opex_h + oi_h)
    bezier_band(ax, x1e, BASE + cogs_h, BASE + cogs_h + opex_h,
                xs[2], BASE, BASE + opex_h)
    bezier_band(ax, x2e, BASE + opex_h + it_h, BASE + opex_h + oi_h,
                xs[3], BASE + it_h, BASE + it_h + ni_h)
    bezier_band(ax, x2e, BASE + opex_h, BASE + opex_h + it_h,
                xs[3], BASE, BASE + it_h)

    BBOX = dict(boxstyle="round,pad=0.35", facecolor="white",
                edgecolor="#cccccc", alpha=0.92, linewidth=0.8)
    lkw = dict(transform=ax.transAxes, va="center", ha="left",
               fontsize=16, fontweight="bold", color="#111111",
               linespacing=1.5, bbox=BBOX)

    def place_label(ax, x, y, text, small_h, above=True):
        if small_h < 0.07:
            y_off = y + 0.10 if above else y - 0.08
            ax.annotate("", xy=(x, y), xytext=(x + 0.01, y_off),
                        xycoords="axes fraction", textcoords="axes fraction",
                        arrowprops=dict(arrowstyle="-", color="#888888", lw=1.0))
            ax.text(x + 0.012, y_off, text, **lkw)
        else:
            ax.text(x, y, text, **lkw)

    lx0 = xs[0] + NODE_W + 0.012
    lx1 = xs[1] + NODE_W + 0.012
    lx2 = xs[2] + NODE_W + 0.012
    lx3 = xs[3] + NODE_W + 0.012

    def pct(v, tag): return f"({tag}: {v / rev * 100:.1f}%)"

    ax.text(lx0, BASE + rev_h / 2, f"Revenue\n{B(rev)}", **lkw)
    place_label(ax, lx1, BASE + cogs_h + gp_h / 2,  f"Gross Profit\n{B(gp)}\n{pct(gp, "GM")}", gp_h)
    place_label(ax, lx1, BASE + cogs_h / 2,          f"Cost of Revenue\n{B(cogs)}", cogs_h, above=False)
    place_label(ax, lx2, BASE + opex_h + oi_h / 2,   f"Operating Income\n{B(oi)}\n{pct(oi, "OM")}", oi_h)
    place_label(ax, lx2, BASE + opex_h / 2,           f"Operating Expenses\n{B(opex_val)}", opex_h, above=False)
    place_label(ax, lx3, BASE + it_h + ni_h / 2,      f"Net Income\n{B(ni)}\n{pct(ni, "NM")}", ni_h)
    place_label(ax, lx3, BASE + it_h / 2,             f"Interest & Tax\n{B(interest_tax)}", it_h, above=False)

    plt.tight_layout()
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {out_path}")


# ── Trend data: actuals + TTM + consensus, shared by charts and Word tables ──

LINE_ITEMS = [
    ("revenue",          "Revenue",          ("Total Revenue",),                                                 "gross_margin"),
    ("gross_profit",     "Gross Profit",     ("Gross Profit",),                                                  "gross_margin"),
    ("operating_income", "Operating Income", ("Operating Income", "Total Operating Income As Reported", "EBIT"), "operating_margin"),
    ("net_income",       "Net Income",       ("Net Income", "Net Income Common Stockholders"),                   "net_margin"),
]
LINE_COLORS = {"revenue": "#4285F4", "gross_profit": "#34A853",
               "operating_income": "#F4B400", "net_income": "#EA4335"}


def _series(data, keys):
    for k in keys:
        raw = data.get(k)
        if raw and isinstance(raw, dict):
            return {d: v for d, v in raw.items() if v is not None and d != "TTM"}
    return {}


def _ttm_value(data, keys):
    for k in keys:
        raw = data.get(k)
        if raw and isinstance(raw, dict) and raw.get("TTM") is not None:
            return raw["TTM"]
    return None


def _month_label(date_str):
    from datetime import datetime
    return datetime.strptime(date_str, "%Y-%m-%d").strftime("%b %Y")


def _estimate_values(e):
    """Dollar values from a consensus entry; falls back to revenue × margin when only a margin is given."""
    rev = e.get("revenue")
    out = {"revenue": rev}
    for key, _, _, margin_key in LINE_ITEMS[1:]:
        v = e.get(key)
        if v is None and rev is not None and e.get(margin_key) is not None:
            v = rev * e[margin_key]
        out[key] = v
    return out


def _year_ago(dates, d):
    from datetime import datetime
    dt = datetime.strptime(d, "%Y-%m-%d")
    for c in dates:
        if 350 <= (dt - datetime.strptime(c, "%Y-%m-%d")).days <= 380:
            return c
    return None


def _load(ticker):
    base, t = f"Outputs/{ticker.upper()}", ticker.lower()
    return (load_json(f"{base}/{t}_income_statement_quarterly.json"),
            load_json(f"{base}/{t}_income_statement_annual.json"),
            load_json(f"{base}/{t}_income_statement_ttm.json"),
            load_json(f"{base}/{t}_consensus_estimates.json"))


def annual_trend_rows(ticker, n_years=5):
    """Last n fiscal years (SEC EDGAR) + TTM (if newer than the last FY) + consensus fiscal years.

    Each row: {period, kind ('actual'|'ttm'|'estimate'), revenue, gross_profit,
    operating_income, net_income, rev_yoy}. Values are raw dollars or None.
    """
    q, ann, ttm, est = _load(ticker)
    ann_s = {key: _series(ann, keys) for key, _, keys, _ in LINE_ITEMS}
    years = sorted(ann_s["revenue"])[-n_years:]
    rows = []
    for d in years:
        row = {"period": f"FY{d[:4]}", "kind": "actual", "end": d}
        row.update({key: ann_s[key].get(d) for key, *_ in LINE_ITEMS})
        rows.append(row)

    q_rev = _series(q, LINE_ITEMS[0][2])
    q_dates = sorted(q_rev)
    if q_dates and years and q_dates[-1] > years[-1] and ttm:
        row = {"period": f"TTM {_month_label(q_dates[-1])}", "kind": "ttm", "end": q_dates[-1]}
        row.update({key: _ttm_value(ttm, keys) for key, _, keys, _ in LINE_ITEMS})
        prior = q_dates[-8:-4]
        if len(prior) == 4 and row["revenue"]:
            row["rev_yoy"] = row["revenue"] / sum(q_rev[d] for d in prior) - 1
        rows.append(row)

    last_year = int(years[-1][:4]) if years else 0
    for e in est.get("estimates", []):
        m = re.search(r"\d{4}", e.get("label", ""))
        if not m or int(m.group()) <= last_year or e.get("revenue") is None:
            continue
        row = {"period": e["label"], "kind": "estimate"}
        row.update(_estimate_values(e))
        rows.append(row)

    prev = None
    for row in rows:
        if row["kind"] == "ttm":
            continue
        if prev and prev["revenue"] and row["revenue"] is not None:
            row["rev_yoy"] = row["revenue"] / prev["revenue"] - 1
        prev = row
    for row in rows:
        row.setdefault("rev_yoy", None)
    return rows


def quarterly_trend_rows(ticker, n_quarters=8, n_estimates=4):
    """Last n quarters (SEC EDGAR, including the latest) + up to n consensus quarters.

    Same row shape as annual_trend_rows; rev_yoy is vs. the same quarter a year earlier.
    """
    q, _, _, est = _load(ticker)
    q_s = {key: _series(q, keys) for key, _, keys, _ in LINE_ITEMS}
    all_dates = sorted(q_s["revenue"])
    dates = all_dates[-n_quarters:]
    rows = []
    for d in dates:
        row = {"period": _month_label(d), "kind": "actual", "end": d}
        row.update({key: q_s[key].get(d) for key, *_ in LINE_ITEMS})
        rows.append(row)

    last = dates[-1] if dates else ""
    future = sorted((e for e in est.get("quarterly_estimates", [])
                     if e.get("period_end", "") > last and e.get("revenue") is not None),
                    key=lambda e: e["period_end"])[:n_estimates]
    for e in future:
        row = {"period": f"{_month_label(e['period_end'])}E", "kind": "estimate", "end": e["period_end"]}
        row.update(_estimate_values(e))
        rows.append(row)

    for row in rows:
        ya = _year_ago(all_dates, row["end"])
        row["rev_yoy"] = (row["revenue"] / q_s["revenue"][ya] - 1
                          if ya and row["revenue"] is not None and q_s["revenue"][ya] else None)
        row["yoy"] = {}
        for key, *_ in LINE_ITEMS:
            p, c = q_s[key].get(ya) if ya else None, row[key]
            if p is not None and c is not None:
                row["yoy"][key] = (c / p - 1) if p > 0 else "n/m"
    return rows


def margin(row, key):
    """Line item ÷ revenue as a decimal, or None."""
    return row[key] / row["revenue"] if row[key] is not None and row["revenue"] else None


def _price_points(ticker, rows):
    """{row index: close} for the share-price overlay: close on/before each period end (fiscal year-end, quarter-end, TTM end).
    Fiscal years that predate the cached price history (5 years) are skipped."""
    hist = load_json(f"Outputs/{ticker.upper()}/{ticker.lower()}_price_history.json")
    if not hist:
        return {}
    days = sorted(hist)
    pts = {}
    for i, r in enumerate(rows):
        if r["kind"] != "estimate" and r.get("end") and r["end"] >= days[0]:
            prior = [d for d in days if d <= r["end"]]
            if prior:
                pts[i] = hist[prior[-1]]
    return pts


def _daily_price(ticker, rows, cx):
    """(x positions, closes, latest date as mm/dd/yyyy) for every trading day from the first period end to the
    latest cached close. The axis is categorical, so dates map to x by linear interpolation between each period's
    end date and its x center; consensus periods with no end date (annual) are placed one year apart."""
    from datetime import datetime, timedelta
    hist = load_json(f"Outputs/{ticker.upper()}/{ticker.lower()}_price_history.json")
    parse = lambda d: datetime.strptime(d, "%Y-%m-%d")
    anchors, last_end, last_year = [], None, None
    for r, x in zip(rows, cx):
        end = r.get("end")
        if end:
            end = parse(end)
            if r["kind"] != "estimate":
                last_end, last_year = end, end.year
        elif r["kind"] == "estimate" and last_end:
            m = re.search(r"\d{4}", r["period"])
            end = last_end + timedelta(days=365 * (int(m.group()) - last_year)) if m else None
        if end:
            anchors.append((end.toordinal(), x))
    if not hist or len(anchors) < 2:
        return None
    days = [d for d in sorted(hist) if parse(d).toordinal() >= anchors[0][0]]
    if not days:
        return None
    xs = np.interp([parse(d).toordinal() for d in days], [a[0] for a in anchors], [a[1] for a in anchors])
    return xs, [hist[d] for d in days], parse(days[-1]).strftime("%m/%d/%Y")


PRICE_COLOR = "#6A1B9A"
MARGIN_TAGS = {"gross_profit": "GM", "operating_income": "OM", "net_income": "NM"}


def chart_bars(ticker, rows, title, out_path, quarterly=False):
    """Grouped bar chart of trend rows: revenue, gross profit, operating income, net income, with the share
    price on a right axis. Every bar is labeled with amount, YoY growth and margin (annual TTM: no YoY).
    Consensus is drawn for revenue only (light, hatched). quarterly=True uses each row's precomputed "yoy"
    (vs. the same quarter a year earlier) and tighter spacing."""
    rows = [r for r in rows if any(r[k] is not None for k, *_ in LINE_ITEMS)]
    if not rows:
        print(f"  [income bars] No data for {ticker}"); return
    div, axis_label, suffix = smart_scale([r[k] for r in rows for k, *_ in LINE_ITEMS])

    # YoY vs. previous fiscal/consensus year (TTM skipped); n/m when the prior base is <= 0
    yoy, prev = [], None
    for r in rows:
        yoy.append({})
        if quarterly:
            yoy[-1] = r.get("yoy", {})
            continue
        if r["kind"] == "ttm":
            continue
        for key, *_ in LINE_ITEMS:
            p, c = (prev or {}).get(key), r[key]
            if p is not None and c is not None:
                yoy[-1][key] = (c / p - 1) if p > 0 else "n/m"
        prev = r

    light = {"revenue": "#A9C7F7"}
    n = len(LINE_ITEMS)
    # Layout: roomy spacing for the four-bar actual groups (horizontal labels need it), tight spacing for the
    # single-bar revenue consensus periods, with a modest gap before them.
    w, step, hist_sp = (0.5, 0.55, 2.5) if quarterly else (0.44, 0.5, 2.1)
    cx = []
    for i, r in enumerate(rows):
        if not cx:
            cx.append(0.0)
        else:
            was_est, is_est = rows[i - 1]["kind"] == "estimate", r["kind"] == "estimate"
            cx.append(cx[-1] + (1.0 if is_est and was_est else 1.5 if is_est else hist_sp))
    fig, ax = plt.subplots(figsize=(40 if quarterly else 34, 8))
    tops = []
    for i, r in enumerate(rows):
        est = r["kind"] == "estimate"
        for j, (key, name, *_) in enumerate(LINE_ITEMS):
            v = r[key]
            if v is None or (est and key != "revenue"):
                continue
            x = cx[i] + (0 if est else (j - (n - 1) / 2) * step)
            color = LINE_COLORS[key]
            ax.bar(x, v / div, width=w, color=light[key] if est else color,
                   hatch="//" if est else None, edgecolor="#1F3864" if est else color, zorder=2)
            label = f"${v / div:.1f}{suffix}" if v >= 0 else f"-${abs(v) / div:.1f}{suffix}"
            g = yoy[i].get(key)
            if g == "n/m" or (g is not None and abs(g) >= 10):
                label += "\n(n/m YoY)"
            elif g is not None:
                label += f"\n({g * 100:+.0f}% YoY)"
            if key in MARGIN_TAGS and margin(r, key) is not None:
                label += f"\n({MARGIN_TAGS[key]} {margin(r, key) * 100:.1f}%)"
            ax.annotate(label, xy=(x, max(v, 0) / div), xytext=(0, 4), textcoords="offset points",
                        ha="center", va="bottom", fontsize=10 if quarterly else 8, fontweight="bold", linespacing=1.15,
                        color=color if not est else "#1F3864", zorder=6)
            tops.append(v / div)
    lo, hi = min(tops + [0]), max(tops + [0])
    ax.set_ylim(lo - (hi - lo) * 0.15 if lo < 0 else 0, hi * (1.45 if quarterly else 1.3))
    ax.axhline(0, color="black", linewidth=0.8)
    est_idx = [i for i, r in enumerate(rows) if r["kind"] == "estimate"]
    if est_idx:
        k = min(est_idx)
        ax.axvline(cx[k] - 0.45 if k else cx[0] - 0.5, color="gray", linestyle=":", linewidth=1.5)
    ax.set_xlim(cx[0] - 1.2, cx[-1] + 0.8)
    ax.set_xticks(cx)
    def tick_label(r):
        if r.get("end"):  # fiscal year / quarter / TTM period end as mm/dd/yyyy
            from datetime import datetime
            head = "TTM" if r["kind"] == "ttm" else r["period"]
            return f"{head}\n({datetime.strptime(r['end'], '%Y-%m-%d').strftime('%m/%d/%Y')})"
        return r["period"]
    ax.set_xticklabels([tick_label(r) for r in rows], fontsize=13)
    ax.tick_params(axis="y", labelsize=14)
    ax.set_ylabel(axis_label, fontsize=17)
    ax.set_title(title, fontsize=22, fontweight="bold")
    px = _price_points(ticker, rows)
    daily = _daily_price(ticker, rows, cx)
    if px:
        ax2 = ax.twinx()
        if daily:  # daily closes: first period end -> latest close; dates are interpolated between period-end x positions
            dx, dy, last_day = daily
            ax2.plot(dx, dy, color=PRICE_COLOR, linewidth=1.3, alpha=0.8, zorder=7)
            ax2.plot(dx[-1], dy[-1], color=PRICE_COLOR, marker="o", markersize=8, zorder=8)
            ax2.annotate(f"Latest ${dy[-1]:,.2f}\n({last_day})", xy=(dx[-1], dy[-1]), xytext=(0, 10),
                         textcoords="offset points", ha="center", fontsize=11, fontweight="bold",
                         color="white", zorder=9,
                         bbox=dict(facecolor=PRICE_COLOR, edgecolor=PRICE_COLOR, boxstyle="round,pad=0.25"))
        xs, ys = [cx[i] for i in sorted(px)], [px[i] for i in sorted(px)]
        ax2.plot(xs, ys, color=PRICE_COLOR, linewidth=0, marker="D", markersize=8, zorder=8)
        for xi, yi in zip(xs, ys):
            ax2.annotate(f"${yi:,.2f}", xy=(xi, yi), xytext=(0, -24), textcoords="offset points", ha="center",
                         fontsize=11, fontweight="bold", color=PRICE_COLOR, zorder=9,
                         bbox=dict(facecolor="white", edgecolor=PRICE_COLOR, alpha=0.9, boxstyle="round,pad=0.25"))
        # negative floor lifts the price line into the empty band above the bars; hide the negative ticks
        allp = ys + (daily[1] if daily else [])
        top, bottom = max(allp) * 1.22, min(allp)
        floor = 0.66 if quarterly else 0.62  # share of axis height the lowest price sits at, above the bar labels
        ax2.set_ylim((bottom - floor * top) / (1 - floor), top)
        ax2.set_yticks([t for t in ax2.get_yticks() if 0 <= t <= top])
        ax2.set_ylabel("Share price (USD)", fontsize=17, color=PRICE_COLOR)
        ax2.tick_params(axis="y", labelsize=14, colors=PRICE_COLOR)
    handles = [patches.Patch(color=LINE_COLORS[k], label=name) for k, name, *_ in LINE_ITEMS]
    if est_idx:
        handles.insert(1, patches.Patch(facecolor=light["revenue"], edgecolor="#1F3864", hatch="//",
                                        label="Revenue (consensus)"))
    if px:
        handles.append(Line2D([0], [0], color=PRICE_COLOR, marker="D", linewidth=1.5,
                              label="Share price (daily close; diamonds = period-end close)"))
    ax.legend(handles=handles, fontsize=13, loc="upper center", bbox_to_anchor=(0.5, -0.1),
              ncol=len(handles), frameon=False)
    ax.grid(axis="y", alpha=0.3, zorder=0)
    plt.tight_layout()
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {out_path}")


def main():
    if len(sys.argv) < 2:
        print("Usage: chart_income_statement.py TICKER")
        sys.exit(1)
    ticker = sys.argv[1].upper()
    base = f"Outputs/{ticker}"
    os.makedirs(base, exist_ok=True)
    t = ticker.lower()
    data = load_json(f"{base}/{t}_income_statement_quarterly.json")
    if not data:
        print(f"Missing quarterly income statement for {ticker}"); sys.exit(1)
    chart_flow(ticker, data, f"{base}/{t}_income_statement_flow.png")
    q_rows = quarterly_trend_rows(ticker)
    a_rows = annual_trend_rows(ticker)
    chart_bars(ticker, a_rows, f"{ticker} Annual Income Statement Trend",
               f"{base}/{t}_income_statement_annual_trend.png")
    chart_bars(ticker, q_rows, f"{ticker} Quarterly Income Statement Trend",
               f"{base}/{t}_income_statement_quarterly_trend.png", quarterly=True)


if __name__ == "__main__":
    main()


