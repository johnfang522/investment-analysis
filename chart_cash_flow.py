"""
chart_cash_flow.py TICKER

Generates two charts saved to Outputs/{TICKER}/:
  1. {ticker}_cash_flow_waterfall.png — Waterfall bar (most recent quarter)
  2. {ticker}_cash_flow_trend.png     — Trend line (last 8 quarters)
"""
import json, sys, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def load_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except Exception:
        return {}


def get_series(data, *keys, n=8):
    for k in keys:
        raw = data.get(k)
        if raw and isinstance(raw, dict):
            items = [(d, v) for d, v in raw.items() if v is not None and d != "TTM"]
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


# ── Chart 1: Cash flow waterfall ──────────────────────────────────────────

def chart_waterfall(ticker, cf_data, out_path):
    t = ticker.upper()
    ocf_s = get_series(cf_data, "Operating Cash Flow")
    fcf_s = get_series(cf_data, "Free Cash Flow")

    ocf = latest(ocf_s)
    fcf = latest(fcf_s)

    if ocf is None or fcf is None:
        print(f"  [cf waterfall] Missing OCF or FCF for {ticker}"); return

    capex_bridge = fcf - ocf  # negative number (steps down)
    period = period_label(ocf_s[0][0]) if ocf_s else "MRQ"

    div, axis_label, suffix = smart_scale([ocf, fcf, capex_bridge])

    fig, ax = plt.subplots(figsize=(16, 8))
    labels = ["Operating CF", "CapEx", "Free CF"]
    colors = ["#34A853", "#EA4335", "#4285F4"]

    # OCF: full bar from 0
    ax.bar(0, ocf / div, color="#34A853", width=0.5)
    # CapEx: floating bar starting at OCF, going down to FCF
    ax.bar(1, capex_bridge / div, bottom=ocf / div, color="#EA4335", width=0.5)
    # FCF: full bar from 0
    ax.bar(2, fcf / div, color="#4285F4", width=0.5)

    # Connector lines
    for x in [0.25, 1.25]:
        y = fcf / div if x > 1 else ocf / div
        ax.plot([x, x + 0.5], [y, y], color="#888888", linestyle="--", linewidth=1)

    # Value labels
    ax.text(0, ocf / div + abs(ocf) * 0.02 / div, sfmt(ocf, div, suffix),
            ha="center", fontsize=18, fontweight="bold")
    ax.text(1, (ocf + capex_bridge / 2) / div, sfmt(capex_bridge, div, suffix),
            ha="center", va="center", fontsize=18, fontweight="bold", color="white")
    fcf_offset = fcf / div + abs(ocf) * 0.02 / div
    ax.text(2, fcf_offset, sfmt(fcf, div, suffix),
            ha="center", fontsize=18, fontweight="bold")

    ax.set_xticks([0, 1, 2])
    ax.set_xticklabels(labels, fontsize=17)
    ax.set_ylabel(axis_label, fontsize=17)
    ax.tick_params(axis="y", labelsize=15)
    ax.set_title(f"{t} Cash Flow Waterfall ({period})", fontsize=22, fontweight="bold")
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {out_path}")


# ── Chart 2: Cash flow trend line ─────────────────────────────────────────

def chart_trend(ticker, cf_data, is_data, out_path):
    t = ticker.upper()
    ocf_s = get_series(cf_data, "Operating Cash Flow")
    fcf_s = get_series(cf_data, "Free Cash Flow")
    ni_s  = get_series(cf_data, "Net Income")
    if not ni_s:
        ni_s = get_series(is_data, "Net Income", "Net Income Common Stockholders")

    if not ocf_s:
        print(f"  [cf trend] Missing OCF for {ticker}"); return

    ocf_s = list(reversed(ocf_s))  # oldest → newest (left → right)
    dates = [quarter_label(d) for d, _ in ocf_s]

    def align(series):
        smap = {d: v for d, v in series}
        return [smap.get(d, None) for d, _ in ocf_s]

    raw_ocf = [v for _, v in ocf_s]
    raw_fcf = align(fcf_s)
    raw_ni  = align(ni_s)
    div, axis_label, suffix = smart_scale(raw_ocf + raw_fcf + raw_ni)

    ocf_v = [v / div for v in raw_ocf]
    fcf_v = [v / div if v is not None else None for v in raw_fcf]
    ni_v  = [v / div if v is not None else None for v in raw_ni]

    fig, ax = plt.subplots(figsize=(18, 8))
    xs = list(range(len(dates)))

    def plot_line(vals, label, color, offset=(8, 6)):
        valid = [(i, v) for i, v in zip(xs, vals) if v is not None]
        if not valid: return
        xi, yi = zip(*valid)
        ax.plot(xi, yi, color=color, linewidth=2.5, marker="o", markersize=8, label=label)
        for idx in [0, -1]:
            ax.annotate(f"${yi[idx]:.1f}{suffix}", xy=(xi[idx], yi[idx]),
                        xytext=offset, textcoords="offset points",
                        fontsize=15, fontweight="bold", color=color)

    plot_line(ocf_v, "Operating CF", "#34A853", offset=(8, 8))
    plot_line(fcf_v, "Free CF",      "#4285F4", offset=(8, -14))
    plot_line(ni_v,  "Net Income",   "#F4B400", offset=(8, 6))

    ax.set_xticks(xs); ax.set_xticklabels(dates, rotation=45, ha="right", fontsize=14)
    ax.tick_params(axis="y", labelsize=14)
    ax.set_ylabel(axis_label, fontsize=17)
    ax.set_title(f"{t} Quarterly Cash Flow Trend", fontsize=22, fontweight="bold")
    ax.legend(fontsize=15)
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {out_path}")


def main():
    if len(sys.argv) < 2:
        print("Usage: chart_cash_flow.py TICKER")
        sys.exit(1)
    ticker = sys.argv[1].upper()
    base = f"Outputs/{ticker}"
    os.makedirs(base, exist_ok=True)
    t = ticker.lower()
    cf_data = load_json(f"{base}/{t}_cash_flow_statement_quarterly.json")
    is_data = load_json(f"{base}/{t}_income_statement_quarterly.json")
    if not cf_data:
        print(f"Missing quarterly cash flow statement for {ticker}"); sys.exit(1)
    chart_waterfall(ticker, cf_data, f"{base}/{t}_cash_flow_waterfall.png")
    chart_trend(ticker, cf_data, is_data, f"{base}/{t}_cash_flow_trend.png")


if __name__ == "__main__":
    main()
