"""
chart_income_statement.py TICKER

Generates two charts saved to Outputs/{TICKER}/:
  1. {ticker}_income_statement_flow.png  — Sankey-style flow (most recent quarter)
  2. {ticker}_income_statement_trend.png — Quarterly trend line (last 8 quarters)
"""
import json, sys, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
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

    # Derive missing values
    if cogs is None and gp is not None: cogs = rev - gp
    if gp   is None and cogs is not None: gp = rev - cogs
    if gp   is None: gp = rev * 0.5
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

    ax.text(lx0, BASE + rev_h / 2, f"Revenue\n{B(rev)}", **lkw)
    place_label(ax, lx1, BASE + cogs_h + gp_h / 2,  f"Gross Profit\n{B(gp)}", gp_h)
    place_label(ax, lx1, BASE + cogs_h / 2,          f"Cost of Revenue\n{B(cogs)}", cogs_h, above=False)
    place_label(ax, lx2, BASE + opex_h + oi_h / 2,   f"Operating Income\n{B(oi)}", oi_h)
    place_label(ax, lx2, BASE + opex_h / 2,           f"Operating Expenses\n{B(opex_val)}", opex_h, above=False)
    place_label(ax, lx3, BASE + it_h + ni_h / 2,      f"Net Income\n{B(ni)}", ni_h)
    place_label(ax, lx3, BASE + it_h / 2,             f"Interest & Tax\n{B(interest_tax)}", it_h, above=False)

    plt.tight_layout()
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {out_path}")


# ── Chart 2: Quarterly trend line ─────────────────────────────────────────

def chart_trend(ticker, data, out_path):
    t = ticker.upper()
    rev_s = get_series(data, "Total Revenue")
    gp_s  = get_series(data, "Gross Profit")
    oi_s  = get_series(data, "Operating Income", "Total Operating Income As Reported", "EBIT")
    ni_s  = get_series(data, "Net Income", "Net Income Common Stockholders")

    if not rev_s:
        print(f"  [income trend] Missing Revenue for {ticker}"); return

    rev_s = list(reversed(rev_s))   # oldest → newest (left → right)
    dates = [quarter_label(d) for d, _ in rev_s]

    def align(series):
        smap = {d: v for d, v in series}
        return [smap.get(d, None) for d, _ in rev_s]

    raw_rev = [v for _, v in rev_s]
    raw_gp  = align(gp_s)
    raw_oi  = align(oi_s)
    raw_ni  = align(ni_s)
    div, axis_label, suffix = smart_scale(raw_rev + raw_gp + raw_oi + raw_ni)

    rev_v = [v / div for v in raw_rev]
    gp_v  = [v / div if v is not None else None for v in raw_gp]
    oi_v  = [v / div if v is not None else None for v in raw_oi]
    ni_v  = [v / div if v is not None else None for v in raw_ni]

    fig, ax = plt.subplots(figsize=(18, 8))
    xs = list(range(len(dates)))

    def plot_line(vals, label, color):
        valid = [(i, v) for i, v in zip(xs, vals) if v is not None]
        if not valid: return
        xi, yi = zip(*valid)
        ax.plot(xi, yi, color=color, linewidth=2.5, marker="o", markersize=7, label=label)
        for idx in [0, -1]:
            ax.annotate(f"${yi[idx]:.1f}{suffix}", xy=(xi[idx], yi[idx]),
                        xytext=(8, 6), textcoords="offset points",
                        fontsize=15, fontweight="bold", color=color)

    plot_line(rev_v, "Revenue",          "#4285F4")
    plot_line(gp_v,  "Gross Profit",     "#34A853")
    plot_line(oi_v,  "Operating Income", "#F4B400")
    plot_line(ni_v,  "Net Income",       "#EA4335")

    ax.set_xticks(xs); ax.set_xticklabels(dates, rotation=45, ha="right", fontsize=14)
    ax.tick_params(axis="y", labelsize=14)
    ax.set_ylabel(axis_label, fontsize=17)
    ax.set_title(f"{t} Quarterly Income Statement Trend", fontsize=22, fontweight="bold")
    ax.legend(fontsize=15)
    ax.grid(axis="y", alpha=0.3)
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
    chart_flow(ticker,  data, f"{base}/{t}_income_statement_flow.png")
    chart_trend(ticker, data, f"{base}/{t}_income_statement_trend.png")


if __name__ == "__main__":
    main()
