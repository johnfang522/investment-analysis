"""
chart_balance_sheet.py TICKER

Generates two charts saved to Outputs/{TICKER}/:
  1. {ticker}_balance_sheet_composition.png — Stacked bar (most recent quarter)
  2. {ticker}_balance_sheet_trend.png       — Trend line (last 8 quarters)
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


def latest(series):
    return series[0][1] if series else None


def quarter_label(date_str):
    from datetime import datetime
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        q = (dt.month - 1) // 3 + 1
        return f"Q{q} {dt.year}"
    except Exception:
        return date_str


def B(v):
    return f"${v/1e9:.1f}B" if v is not None else ""


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
    period = quarter_label(total_assets_s[0][0]) if total_assets_s else "MRQ"

    fig, ax = plt.subplots(figsize=(16, 8))

    bar_w = 0.4
    # Assets bar
    bottoms_a, labels_a, colors_a = [], [], []
    if ca  is not None: bottoms_a.append(ca / 1e9);  labels_a.append(f"Current Assets\n{B(ca)}");     colors_a.append("#4285F4")
    if nca is not None: bottoms_a.append(nca / 1e9); labels_a.append(f"Non-Current Assets\n{B(nca)}"); colors_a.append("#4A90D9")

    # Funding bar
    bottoms_f, labels_f, colors_f = [], [], []
    if cl       is not None: bottoms_f.append(cl / 1e9);       labels_f.append(f"Current Liabilities\n{B(cl)}");   colors_f.append("#EA4335")
    if ltd      is not None: bottoms_f.append(ltd / 1e9);      labels_f.append(f"Long-term Debt\n{B(ltd)}");        colors_f.append("#F4A460")
    if other_lt is not None: bottoms_f.append(other_lt / 1e9); labels_f.append(f"Other LT Liabilities\n{B(other_lt)}"); colors_f.append("#FA8072")
    if eq       is not None: bottoms_f.append(eq / 1e9);       labels_f.append(f"Equity\n{B(eq)}");                 colors_f.append("#34A853")

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
    ax.set_ylabel("Billions USD", fontsize=17)
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

    def to_b(vals):
        return [v / 1e9 if v else None for v in vals]

    ta_v  = [v / 1e9 for _, v in total_assets_s]
    eq_v  = to_b(align(equity_s))
    tl_v  = to_b(align(total_liab_s))
    td_v  = to_b(align(total_debt_s))
    ca_v  = to_b(align(cash_s))

    fig, ax = plt.subplots(figsize=(18, 8))
    xs = list(range(len(dates)))

    def plot_line(vals, label, color):
        valid = [(i, v) for i, v in zip(xs, vals) if v is not None]
        if not valid: return
        xi, yi = zip(*valid)
        ax.plot(xi, yi, color=color, linewidth=2.5, marker="o", markersize=7, label=label)
        for idx in [0, -1]:
            ax.annotate(f"${yi[idx]:.1f}B", xy=(xi[idx], yi[idx]),
                        xytext=(8, 6), textcoords="offset points",
                        fontsize=15, fontweight="bold", color=color)

    plot_line(ta_v, "Total Assets",      "#4285F4")
    plot_line(eq_v, "Total Equity",      "#34A853")
    plot_line(tl_v, "Total Liabilities", "#EA4335")
    plot_line(td_v, "Total Debt",        "#F4B400")
    plot_line(ca_v, "Cash",              "#8F5DB7")

    ax.set_xticks(xs); ax.set_xticklabels(dates, rotation=45, ha="right", fontsize=14)
    ax.tick_params(axis="y", labelsize=14)
    ax.set_ylabel("Billions USD", fontsize=17)
    ax.set_title(f"{t} Balance Sheet Trend", fontsize=22, fontweight="bold")
    ax.legend(fontsize=15)
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()
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
