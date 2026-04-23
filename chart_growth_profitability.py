"""
chart_growth_profitability.py TICKER

Generates three charts saved to Outputs/{TICKER}/:
  1. {ticker}_gp_revenue_trend.png — Revenue & Gross Profit grouped bar + Gross Margin % line
  2. {ticker}_margin_trend.png     — Gross / Operating / Net Margin trend lines
  3. {ticker}_yoy_growth.png       — Annual YoY Revenue & Net Income growth bars
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
            items.sort(key=lambda x: x[0], reverse=True)
            return items[:n]
    return []


def quarter_label(date_str):
    from datetime import datetime
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        q = (dt.month - 1) // 3 + 1
        return f"Q{q} {dt.year}"
    except Exception:
        return date_str


def fiscal_year(date_str):
    from datetime import datetime
    try:
        return str(datetime.strptime(date_str, "%Y-%m-%d").year)
    except Exception:
        return date_str


# ── Chart 1: Revenue & Gross Profit grouped bar + Gross Margin line ────────

def chart_gp_revenue(ticker, q_data, out_path):
    t = ticker.upper()
    rev_s = get_series(q_data, "Total Revenue", n=5)
    gp_s  = get_series(q_data, "Gross Profit",  n=5)

    if not rev_s:
        print(f"  [gp_revenue] Missing Revenue for {ticker}"); return

    rev_s = list(reversed(rev_s))  # oldest → newest (left → right)
    dates = [quarter_label(d) for d, _ in rev_s]
    xs = np.arange(len(dates))
    width = 0.35

    def align(series):
        smap = {d: v for d, v in series}
        return [smap.get(d, None) for d, _ in rev_s]

    rev_v = [v / 1e9 for _, v in rev_s]
    gp_v  = [v / 1e9 if v else None for v in align(gp_s)]
    gm_v  = [gp / rev * 100 if gp and rev else None
             for gp, rev in zip(gp_v, rev_v)]

    fig, ax1 = plt.subplots(figsize=(18, 8))
    ax2 = ax1.twinx()

    bars1 = ax1.bar(xs - width/2, rev_v, width, color="#4285F4", label="Revenue")
    gp_vals = [v if v else 0 for v in gp_v]
    bars2 = ax1.bar(xs + width/2, gp_vals, width, color="#009B9F", label="Gross Profit")

    # Label most recent bars
    for bar in [bars1[-1], bars2[-1]]:
        h = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width() / 2, h + 0.3, f"${h:.1f}B",
                 ha="center", fontsize=15, fontweight="bold")

    valid_gm = [(i, v) for i, v in enumerate(gm_v) if v is not None]
    if valid_gm:
        xi, yi = zip(*valid_gm)
        ax2.plot(xi, yi, color="#34A853", linewidth=2.5, linestyle="--",
                 marker="o", markersize=8, label="Gross Margin %")

    ax1.set_xticks(xs); ax1.set_xticklabels(dates, rotation=45, ha="right", fontsize=14)
    ax1.tick_params(axis="y", labelsize=14); ax2.tick_params(axis="y", labelsize=14)
    ax1.set_ylabel("Billions USD", fontsize=17); ax2.set_ylabel("Gross Margin %", fontsize=17)
    ax1.set_title(f"{t} Revenue & Gross Profit Trend", fontsize=22, fontweight="bold")
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, fontsize=15)
    ax1.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {out_path}")


# ── Chart 2: Margin trend lines ────────────────────────────────────────────

def chart_margins(ticker, q_data, out_path):
    t = ticker.upper()
    rev_s = get_series(q_data, "Total Revenue", n=5)
    gp_s  = get_series(q_data, "Gross Profit",  n=5)
    oi_s  = get_series(q_data, "Operating Income", "Total Operating Income As Reported", "EBIT", n=5)
    ni_s  = get_series(q_data, "Net Income", "Net Income Common Stockholders", n=5)

    if not rev_s:
        print(f"  [margins] Missing Revenue for {ticker}"); return

    rev_s = list(reversed(rev_s))  # oldest → newest (left → right)
    dates = [quarter_label(d) for d, _ in rev_s]
    xs = list(range(len(dates)))

    def align(series):
        smap = {d: v for d, v in series}
        return [smap.get(d, None) for d, _ in rev_s]

    rev_v = [v for _, v in rev_s]

    def margin(num_vals):
        return [n / r * 100 if n and r else None
                for n, r in zip(num_vals, rev_v)]

    gm_v  = margin(align(gp_s))
    om_v  = margin(align(oi_s))
    nm_v  = margin(align(ni_s))

    fig, ax = plt.subplots(figsize=(18, 8))

    def plot_line(vals, label, color):
        valid = [(i, v) for i, v in zip(xs, vals) if v is not None]
        if not valid: return
        xi, yi = zip(*valid)
        ax.plot(xi, yi, color=color, linewidth=2.5, marker="o", markersize=7, label=label)
        for idx in [0, -1]:
            ax.annotate(f"{yi[idx]:.1f}%", xy=(xi[idx], yi[idx]),
                        xytext=(8, 6), textcoords="offset points",
                        fontsize=15, fontweight="bold", color=color)

    plot_line(gm_v, "Gross Margin",     "#009B9F")
    plot_line(om_v, "Operating Margin", "#4285F4")
    plot_line(nm_v, "Net Margin",       "#F4B400")

    ax.set_xticks(xs); ax.set_xticklabels(dates, rotation=45, ha="right", fontsize=14)
    ax.tick_params(axis="y", labelsize=14)
    ax.set_ylabel("Margin (%)", fontsize=17)
    ax.set_title(f"{t} Margin Trend", fontsize=22, fontweight="bold")
    ax.legend(fontsize=15)
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {out_path}")


# ── Chart 3: Annual YoY growth rates grouped bar ───────────────────────────

def chart_yoy_growth(ticker, ann_data, out_path):
    t = ticker.upper()
    rev_s = get_series(ann_data, "Total Revenue", n=6)
    ni_s  = get_series(ann_data, "Net Income", "Net Income Common Stockholders", n=6)

    if len(rev_s) < 2:
        print(f"  [yoy growth] Insufficient annual Revenue data for {ticker}"); return

    # Compute YoY growth for each available year (need current and prior)
    rev_by_date = {d: v for d, v in rev_s}
    ni_by_date  = {d: v for d, v in ni_s}

    dates_sorted = sorted(rev_by_date.keys())
    years, rev_growths, ni_growths = [], [], []
    for i in range(1, len(dates_sorted)):
        cur_d, prv_d = dates_sorted[i], dates_sorted[i - 1]
        yr = fiscal_year(cur_d)
        rv_cur = rev_by_date.get(cur_d); rv_prv = rev_by_date.get(prv_d)
        ni_cur = ni_by_date.get(cur_d);  ni_prv = ni_by_date.get(prv_d)
        rg = (rv_cur - rv_prv) / abs(rv_prv) * 100 if rv_cur and rv_prv else None
        ng = (ni_cur - ni_prv) / abs(ni_prv) * 100 if ni_cur and ni_prv else None
        years.append(yr); rev_growths.append(rg); ni_growths.append(ng)

    xs = np.arange(len(years))
    width = 0.35
    fig, ax = plt.subplots(figsize=(18, 8))

    def color_bar(v): return "#34A853" if (v or 0) >= 0 else "#EA4335"

    for i, (yr, rg, ng) in enumerate(zip(years, rev_growths, ni_growths)):
        if rg is not None:
            b = ax.bar(i - width/2, rg, width, color=color_bar(rg), label="Revenue Growth" if i == 0 else "")
            ax.text(i - width/2, rg + (1 if rg >= 0 else -3), f"{rg:.1f}%",
                    ha="center", fontsize=15, fontweight="bold")
        if ng is not None:
            ax.bar(i + width/2, ng, width, color=color_bar(ng),
                   alpha=0.65, label="Net Income Growth" if i == 0 else "")
            ax.text(i + width/2, ng + (1 if ng >= 0 else -3), f"{ng:.1f}%",
                    ha="center", fontsize=15, fontweight="bold")

    ax.axhline(0, color="#333333", linewidth=1, linestyle="--")
    ax.set_xticks(xs); ax.set_xticklabels(years, fontsize=15)
    ax.tick_params(axis="y", labelsize=14)
    ax.set_ylabel("Growth (%)", fontsize=17)
    ax.set_title(f"{t} Annual YoY Growth Rates", fontsize=22, fontweight="bold")

    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color="#34A853", label="Revenue Growth"),
                        Patch(color="#34A853", alpha=0.65, label="Net Income Growth")],
              fontsize=15)
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {out_path}")


def main():
    if len(sys.argv) < 2:
        print("Usage: chart_growth_profitability.py TICKER")
        sys.exit(1)
    ticker = sys.argv[1].upper()
    base = f"Outputs/{ticker}"
    os.makedirs(base, exist_ok=True)
    t = ticker.lower()
    q_data   = load_json(f"{base}/{t}_income_statement_quarterly.json")
    ann_data = load_json(f"{base}/{t}_income_statement_annual.json")
    if not q_data:
        print(f"Missing quarterly income statement for {ticker}"); sys.exit(1)
    chart_gp_revenue(ticker, q_data,   f"{base}/{t}_gp_revenue_trend.png")
    chart_margins(ticker,    q_data,   f"{base}/{t}_margin_trend.png")
    chart_yoy_growth(ticker, ann_data, f"{base}/{t}_yoy_growth.png")


if __name__ == "__main__":
    main()
