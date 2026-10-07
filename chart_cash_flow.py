"""
chart_cash_flow.py TICKER

Generates two charts saved to Outputs/{TICKER}/:
  1. {ticker}_cash_flow_waterfall.png — Waterfall bar (most recent quarter)
  2. {ticker}_cash_flow_trend.png     — Grouped bars, every bar labeled (last 8 quarters); Free CF bars also show FCF / net income
"""
import json, sys, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from chart_data import save_chart_data


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
    save_chart_data(out_path, {"kind": "waterfall", "title": f"{t} Cash Flow Waterfall ({period})", "unit": "usd",
                               "steps": [{"label": "Operating CF", "value": ocf, "total": True},
                                         {"label": "CapEx", "value": capex_bridge, "total": False},
                                         {"label": "Free CF", "value": fcf, "total": True}]})
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

    series = [([v / div if v is not None else None for v in raw_ni], "Net Income", "#F4B400"),
              ([v / div for v in raw_ocf], "Operating CF", "#34A853"),
              ([v / div if v is not None else None for v in raw_fcf], "Free CF", "#4285F4")]
    n = len(series)
    w, step, sp = 0.5, 0.55, 2.0  # bar width, spacing within a quarter group, spacing between groups
    fig, ax = plt.subplots(figsize=(24, 8))
    xs = [i * sp for i in range(len(dates))]
    for j, (vals, label, color) in enumerate(series):
        offs = (j - (n - 1) / 2) * step
        valid = [(k, x + offs, v) for k, (x, v) in enumerate(zip(xs, vals)) if v is not None]
        if not valid: continue
        ax.bar([x for _, x, _ in valid], [v for _, _, v in valid], width=w, color=color, label=label, zorder=2)
        for k, x, v in valid:  # label every bar; Free CF also shows its conversion of net income
            text = f"{'-' if v < 0 else ''}${abs(v):.2f}{suffix}"
            if label == "Free CF":
                ni = raw_ni[k]
                text += ("\n" + f"({raw_fcf[k] / ni:.1f}x NI)") if ni and ni > 0 and raw_fcf[k] / ni < 10 else "\n" + "(n/m)"
            ax.annotate(text, xy=(x, max(v, 0)), xytext=(0, 4), textcoords="offset points",
                        ha="center", va="bottom", fontsize=10.5, fontweight="bold", color=color, zorder=6)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_ylim(top=ax.get_ylim()[1] * 1.1)

    ax.set_xticks(xs); ax.set_xticklabels(dates, rotation=45, ha="right", fontsize=14)
    ax.tick_params(axis="y", labelsize=14)
    ax.set_ylabel(axis_label, fontsize=17)
    ax.set_title(f"{t} Quarterly Cash Flow Trend", fontsize=22, fontweight="bold")
    ax.legend(fontsize=15, loc="upper left")
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()
    fcf_notes = [(f"{f / n:.1f}x NI" if n and n > 0 and f is not None and f / n < 10 else "n/m")
                 for f, n in zip(raw_fcf, raw_ni)]
    save_chart_data(out_path, {"kind": "bar", "title": f"{t} Quarterly Cash Flow Trend", "unit": "usd",
                               "categories": [d for d, _ in ocf_s],
                               "series": [{"name": "Net Income", "values": raw_ni},
                                          {"name": "Operating CF", "values": raw_ocf},
                                          {"name": "Free CF", "values": raw_fcf, "notes": fcf_notes}]})
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
