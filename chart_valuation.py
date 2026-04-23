"""
chart_valuation.py TICKER

Generates two charts saved to Outputs/{TICKER}/:
  1. {ticker}_valuation_multiples_trend.png — P/E, EV/EBITDA (left), P/S (right) over annual periods
  2. {ticker}_valuation_price_targets.png   — Current price vs analyst targets (horizontal bars)
"""
import json, sys, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


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
            items.sort(key=lambda x: x[0])
            return items[-n:]
    return []


def fiscal_year(date_str):
    try:
        return str(__import__("datetime").datetime.strptime(date_str, "%Y-%m-%d").year)
    except Exception:
        return date_str


# ── Chart 1: Valuation multiples trend ────────────────────────────────────

def chart_multiples(ticker, ann_data, q_data, quick, out_path):
    t = ticker.upper()

    # Approximate P/E from EPS: annual net income / shares
    # We use what's available; for historical P/E we rely on priceToEarningsRatio if in JSON,
    # or estimate from EPS fields.
    # Quick metrics has current values; annual JSON has EPS history if available.

    eps_s  = get_series(ann_data, "Diluted EPS", "Basic EPS", "EPS")
    rev_s  = get_series(ann_data, "Total Revenue")
    ebitda_s = get_series(ann_data, "EBITDA", "Normalized EBITDA")

    # Current market cap / price for computing multiples — from quick metrics
    mkt_cap = quick.get("marketCap")
    ev       = quick.get("enterpriseValue")
    cur_pe   = quick.get("trailingPE")
    cur_ps   = quick.get("priceToSalesTrailing12Months", quick.get("priceToBook"))
    cur_ev_ebitda = quick.get("enterpriseToEbitda")

    # Build years list from revenue series
    if not rev_s:
        print(f"  [multiples] Insufficient annual data for {ticker}"); return

    years   = [fiscal_year(d) for d, _ in rev_s]
    rev_vals = [v for _, v in rev_s]

    # P/S approximation: if mkt_cap available, compute historical P/S = mkt_cap / rev
    # For trend we can only approximate using current market cap vs historical revenue
    ps_vals = [mkt_cap / r if mkt_cap and r else None for r in rev_vals]

    # EV/EBITDA approximation: use current EV vs historical EBITDA
    ev_ebitda_vals = []
    ebitda_map = {d: v for d, v in ebitda_s}
    for d, _ in rev_s:
        eb = ebitda_map.get(d)
        ev_ebitda_vals.append(ev / eb if ev and eb else None)

    # P/E approximation: use current mkt_cap vs historical net income
    ni_s = get_series(ann_data, "Net Income", "Net Income Common Stockholders")
    ni_map = {d: v for d, v in ni_s}
    pe_vals = []
    for d, _ in rev_s:
        ni = ni_map.get(d)
        pe_vals.append(mkt_cap / ni if mkt_cap and ni and ni > 0 else None)

    # Override last point with current reported multiples from quick_metrics if available
    if cur_pe:        pe_vals[-1]       = cur_pe
    if cur_ev_ebitda: ev_ebitda_vals[-1] = cur_ev_ebitda

    # 3-year averages for reference lines
    def avg3(vals):
        v = [x for x in vals[-3:] if x is not None]
        return sum(v) / len(v) if v else None

    pe_avg       = avg3(pe_vals)
    ev_eb_avg    = avg3(ev_ebitda_vals)
    ps_avg       = avg3(ps_vals)

    fig, ax1 = plt.subplots(figsize=(18, 8))
    ax2 = ax1.twinx()
    xs = list(range(len(years)))

    def plot_left(vals, label, color):
        valid = [(i, v) for i, v in enumerate(vals) if v is not None]
        if not valid: return
        xi, yi = zip(*valid)
        ax1.plot(xi, yi, color=color, linewidth=2.5, marker="o", markersize=7, label=label)
        for idx in [0, -1]:
            ax1.annotate(f"{yi[idx]:.1f}x", xy=(xi[idx], yi[idx]),
                         xytext=(8, 6), textcoords="offset points",
                         fontsize=15, fontweight="bold", color=color)

    def plot_right(vals, label, color):
        valid = [(i, v) for i, v in enumerate(vals) if v is not None]
        if not valid: return
        xi, yi = zip(*valid)
        ax2.plot(xi, yi, color=color, linewidth=2.5, linestyle="--",
                 marker="s", markersize=7, label=label)
        for idx in [0, -1]:
            ax2.annotate(f"{yi[idx]:.1f}x", xy=(xi[idx], yi[idx]),
                         xytext=(8, -14), textcoords="offset points",
                         fontsize=15, fontweight="bold", color=color)

    plot_left(pe_vals,       "Trailing P/E",  "#4285F4")
    plot_left(ev_ebitda_vals, "EV/EBITDA",    "#009B9F")
    plot_right(ps_vals,      "P/S",           "#F4B400")

    if pe_avg:     ax1.axhline(pe_avg,    color="#4285F4", linestyle=":", alpha=0.5, linewidth=1)
    if ev_eb_avg:  ax1.axhline(ev_eb_avg, color="#009B9F", linestyle=":", alpha=0.5, linewidth=1)
    if ps_avg:     ax2.axhline(ps_avg,    color="#F4B400", linestyle=":", alpha=0.5, linewidth=1)

    ax1.set_xticks(xs); ax1.set_xticklabels(years, fontsize=15)
    ax1.tick_params(axis="y", labelsize=14); ax2.tick_params(axis="y", labelsize=14)
    ax1.set_ylabel("P/E  ·  EV/EBITDA", fontsize=17)
    ax2.set_ylabel("P/S", fontsize=17)
    ax1.set_title(f"{t} Valuation Multiples Trend", fontsize=22, fontweight="bold")
    lines1, lbl1 = ax1.get_legend_handles_labels()
    lines2, lbl2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, lbl1 + lbl2, fontsize=15)
    ax1.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {out_path}")


# ── Chart 2: Price vs analyst targets horizontal bar ──────────────────────

def chart_price_targets(ticker, quick, out_path):
    t = ticker.upper()
    cur_price   = quick.get("currentPrice") or quick.get("regularMarketPrice")
    target_mean = quick.get("targetMeanPrice")
    target_med  = quick.get("targetMedianPrice")
    target_high = quick.get("targetHighPrice")
    target_low  = quick.get("targetLowPrice")

    if cur_price is None:
        print(f"  [price targets] Missing current price for {ticker}"); return

    labels = ["Target High", "Target Mean", "Target Median", "Current Price", "Target Low"]
    values = [target_high, target_mean, target_med, cur_price, target_low]
    colors = ["#34A853", "#F4B400", "#4A90D9", "#4285F4", "#EA4335"]

    valid = [(l, v, c) for l, v, c in zip(labels, values, colors) if v is not None]
    if not valid:
        print(f"  [price targets] No price target data for {ticker}"); return

    labels_v, values_v, colors_v = zip(*valid)

    fig, ax = plt.subplots(figsize=(16, 7))
    ys = list(range(len(labels_v)))
    bars = ax.barh(ys, values_v, color=colors_v, height=0.5)

    for bar, val, lbl in zip(bars, values_v, labels_v):
        ax.text(val + max(values_v) * 0.01, bar.get_y() + bar.get_height() / 2,
                f"${val:.2f}", va="center", fontsize=15, fontweight="bold")

    # Vertical reference line at current price
    ax.axvline(cur_price, color="#4285F4", linestyle="--", linewidth=1.5, alpha=0.7)

    ax.set_yticks(ys); ax.set_yticklabels(labels_v, fontsize=15)
    ax.tick_params(axis="x", labelsize=14)
    ax.set_xlabel("Price (USD)", fontsize=17)
    ax.set_title(f"{t} Price vs Analyst Targets", fontsize=22, fontweight="bold")
    ax.grid(axis="x", alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {out_path}")


def main():
    if len(sys.argv) < 2:
        print("Usage: chart_valuation.py TICKER")
        sys.exit(1)
    ticker = sys.argv[1].upper()
    base = f"Outputs/{ticker}"
    os.makedirs(base, exist_ok=True)
    t = ticker.lower()
    ann_data = load_json(f"{base}/{t}_income_statement_annual.json")
    q_data   = load_json(f"{base}/{t}_income_statement_quarterly.json")
    quick    = load_json(f"{base}/{t}_quick_metrics.json")
    if not quick:
        print(f"Missing quick_metrics for {ticker}"); sys.exit(1)
    chart_multiples(ticker, ann_data, q_data, quick,
                    f"{base}/{t}_valuation_multiples_trend.png")
    chart_price_targets(ticker, quick, f"{base}/{t}_valuation_price_targets.png")


if __name__ == "__main__":
    main()
