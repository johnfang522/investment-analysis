"""
chart_balance_sheet.py TICKER

Generates two charts saved to Outputs/{TICKER}/:
  1. {ticker}_balance_sheet_composition.png — Stacked bar (most recent quarter)
  2. {ticker}_balance_sheet_trend.png       — Grouped bars, every bar labeled (last 8 quarters)
"""
import json, sys, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

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


def sfmt(v, div, suffix, dec=1):
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


def B(v, div=1e9, suffix='B'):
    return sfmt(v, div, suffix) if v is not None else ""


# ── Chart 1: Balance sheet composition stacked bar ────────────────────────

def chart_composition(ticker, data, out_path):
    t = ticker.upper()

    total_assets_s  = get_series(data, "Total Assets")
    cur_assets_s    = get_series(data, "Current Assets", "Total Current Assets")
    cur_liab_s      = get_series(data, "Current Liabilities", "Total Current Liabilities Net Minority Interest")
    lt_debt_s       = get_series(data, "Long Term Debt")
    total_liab_s    = get_series(data, "Total Liabilities Net Minority Interest", "Total Liabilities")
    equity_s        = get_series(data, "Stockholders Equity", "Total Equity Gross Minority Interest",
                                 "Common Stock Equity")

    ta  = latest(total_assets_s)
    ca  = latest(cur_assets_s)
    cl  = latest(cur_liab_s)
    ltd = latest(lt_debt_s)
    tl  = latest(total_liab_s)
    eq  = latest(equity_s)

    if ta is None:
        print(f"  [bs composition] Missing Total Assets for {ticker}"); return

    nca = (ta - ca) if ca is not None else None
    other_lt = max(0, (tl - cl - (ltd or 0))) if (tl and cl) else None
    period = period_label(total_assets_s[0][0]) if total_assets_s else "MRQ"

    all_vals = [ta, ca, nca, cl, ltd, other_lt, eq]
    div, axis_label, suffix = smart_scale(all_vals)

    fig, ax = plt.subplots(figsize=(16, 8))

    bar_w = 0.4
    # Assets bar
    bottoms_a, labels_a, colors_a = [], [], []
    if ca  is not None: bottoms_a.append(ca / div);  labels_a.append(f"Current Assets\n{B(ca, div, suffix)}");     colors_a.append("#4285F4")
    if nca is not None: bottoms_a.append(nca / div); labels_a.append(f"Non-Current Assets\n{B(nca, div, suffix)}"); colors_a.append("#4A90D9")

    # Funding bar
    bottoms_f, labels_f, colors_f = [], [], []
    if cl       is not None: bottoms_f.append(cl / div);       labels_f.append(f"Current Liabilities\n{B(cl, div, suffix)}");        colors_f.append("#EA4335")
    if ltd      is not None: bottoms_f.append(ltd / div);      labels_f.append(f"Long-term Debt\n{B(ltd, div, suffix)}");             colors_f.append("#F4A460")
    if other_lt is not None: bottoms_f.append(other_lt / div); labels_f.append(f"Other LT Liabilities\n{B(other_lt, div, suffix)}"); colors_f.append("#FA8072")
    if eq       is not None: bottoms_f.append(eq / div);       labels_f.append(f"Equity\n{B(eq, div, suffix)}");                     colors_f.append("#34A853")

    def draw_stack(x, segments, labels, colors):
        bottom = 0
        for seg, lbl, col in zip(segments, labels, colors):
            bar = ax.bar(x, seg, bottom=bottom, width=bar_w, color=col)
            mid = bottom + seg / 2
            ax.text(x, mid, lbl, ha="center", va="center", fontsize=13, fontweight="bold",
                    color="white" if col not in ("#FA8072", "#F4A460") else "#333333")
            bottom += seg

    draw_stack(0, bottoms_a, labels_a, colors_a)
    draw_stack(1, bottoms_f, labels_f, colors_f)

    ax.set_xticks([0, 1])
    ax.set_xticklabels(["Assets", "Funding (Liabilities + Equity)"], fontsize=17)
    ax.set_ylabel(axis_label, fontsize=17)
    ax.tick_params(axis="y", labelsize=15)
    ax.set_title(f"{t} Balance Sheet Composition ({period})", fontsize=22, fontweight="bold")
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {out_path}")


# ── Chart 2: Balance sheet trend line ─────────────────────────────────────

def chart_trend(ticker, data, out_path):
    t = ticker.upper()

    total_assets_s = get_series(data, "Total Assets")
    equity_s       = get_series(data, "Stockholders Equity", "Total Equity Gross Minority Interest", "Common Stock Equity")
    total_liab_s   = get_series(data, "Total Liabilities Net Minority Interest", "Total Liabilities")
    total_debt_s   = get_series(data, "Total Debt")
    cash_s         = get_series(data, "Cash And Cash Equivalents",
                                "Cash Cash Equivalents And Short Term Investments",
                                "Cash And Short Term Investments")

    if not total_assets_s:
        print(f"  [bs trend] Missing Total Assets for {ticker}"); return

    total_assets_s = list(reversed(total_assets_s))  # oldest → newest (left → right)
    dates = [quarter_label(d) for d, _ in total_assets_s]

    def align(series):
        smap = {d: v for d, v in series}
        return [smap.get(d, None) for d, _ in total_assets_s]

    raw_ta = [v for _, v in total_assets_s]
    raw_eq = align(equity_s)
    raw_tl = align(total_liab_s)
    raw_td = align(total_debt_s)
    raw_ca = align(cash_s)
    div, axis_label, suffix = smart_scale(raw_ta + raw_eq + raw_tl + raw_td + raw_ca)

    def to_scaled(vals):
        return [v / div if v else None for v in vals]

    ta_v  = [v / div for v in raw_ta]
    eq_v  = to_scaled(raw_eq)
    tl_v  = to_scaled(raw_tl)
    td_v  = to_scaled(raw_td)
    ca_v  = to_scaled(raw_ca)

    series = [(ta_v, "Total Assets",      "#4285F4"),
              (eq_v, "Total Equity",      "#34A853"),
              (tl_v, "Total Liabilities", "#EA4335"),
              (td_v, "Total Debt",        "#F4B400"),
              (ca_v, "Cash",              "#8F5DB7")]
    n = len(series)
    w, step, sp = 0.2, 0.21, 1.3  # bar width, spacing within a quarter group, spacing between groups
    fig, ax = plt.subplots(figsize=(24, 8))
    xs = [i * sp for i in range(len(dates))]
    for j, (vals, label, color) in enumerate(series):
        offs = (j - (n - 1) / 2) * step
        valid = [(x + offs, v) for x, v in zip(xs, vals) if v is not None]
        if not valid: continue
        ax.bar([x for x, _ in valid], [v for _, v in valid], width=w, color=color, label=label, zorder=2)
        for x, v in valid:  # label every bar
            ax.annotate(f"{'-' if v < 0 else ''}${abs(v):.1f}{suffix}", xy=(x, max(v, 0)), xytext=(0, 4),
                        textcoords="offset points", ha="center", va="bottom",
                        fontsize=10, fontweight="bold", color=color, zorder=6)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_ylim(top=ax.get_ylim()[1] * 1.08)

    ax.set_xticks(xs); ax.set_xticklabels(dates, rotation=45, ha="right", fontsize=14)
    ax.tick_params(axis="y", labelsize=14)
    ax.set_ylabel(axis_label, fontsize=17)
    ax.set_title(f"{t} Balance Sheet Trend", fontsize=22, fontweight="bold")
    ax.legend(fontsize=15, loc="upper left")
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()
    save_chart_data(out_path, {"kind": "bar", "title": f"{t} Balance Sheet Trend", "unit": "usd",
                               "categories": [d for d, _ in total_assets_s],
                               "series": [{"name": name, "values": [v if v else None for v in raw]}
                                          for name, raw in (("Total Assets", raw_ta), ("Total Equity", raw_eq),
                                                            ("Total Liabilities", raw_tl), ("Total Debt", raw_td),
                                                            ("Cash", raw_ca))]})
    print(f"  Saved: {out_path}")


def main():
    if len(sys.argv) < 2:
        print("Usage: chart_balance_sheet.py TICKER")
        sys.exit(1)
    ticker = sys.argv[1].upper()
    base = f"Outputs/{ticker}"
    os.makedirs(base, exist_ok=True)
    t = ticker.lower()
    data = load_json(f"{base}/{t}_balance_sheet_quarterly.json")
    if not data:
        print(f"Missing quarterly balance sheet for {ticker}"); sys.exit(1)
    chart_composition(ticker, data, f"{base}/{t}_balance_sheet_composition.png")
    chart_trend(ticker,       data, f"{base}/{t}_balance_sheet_trend.png")


if __name__ == "__main__":
    main()
