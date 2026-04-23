"""
chart_technical.py TICKER

Generates two charts saved to Outputs/{TICKER}/:
  1. {ticker}_ta_price_ma.png — Price & Moving Averages (last 18 months)
  2. {ticker}_ta_rsi.png      — RSI (14-day, last 18 months)
"""
import json, sys, os
from datetime import datetime, timedelta
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def load_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except Exception:
        return {}


def compute_rsi(prices, period=14):
    """Wilder's RSI."""
    deltas = np.diff(prices)
    gains  = np.where(deltas > 0, deltas, 0.0)
    losses = np.where(deltas < 0, -deltas, 0.0)
    avg_gain = np.mean(gains[:period])
    avg_loss = np.mean(losses[:period])
    rsi = []
    for i in range(period, len(gains)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period
        rs = avg_gain / avg_loss if avg_loss != 0 else float("inf")
        rsi.append(100 - 100 / (1 + rs))
    # Pad with NaN for the first `period` prices
    return [float("nan")] * (period + 1) + rsi


def moving_average(prices, window):
    result = [float("nan")] * len(prices)
    for i in range(window - 1, len(prices)):
        result[i] = np.mean(prices[i - window + 1: i + 1])
    return result


def main():
    if len(sys.argv) < 2:
        print("Usage: chart_technical.py TICKER")
        sys.exit(1)
    ticker = sys.argv[1].upper()
    base = f"Outputs/{ticker}"
    os.makedirs(base, exist_ok=True)
    t = ticker.lower()

    price_data = load_json(f"{base}/{t}_price_history.json")
    if not price_data:
        print(f"Missing price history for {ticker}"); sys.exit(1)

    # Sort all dates ascending
    items = sorted([(datetime.strptime(d, "%Y-%m-%d"), v)
                    for d, v in price_data.items() if v is not None])
    if len(items) < 200:
        print(f"  Insufficient price history for {ticker} ({len(items)} days)")

    all_dates  = [d for d, _ in items]
    all_prices = np.array([v for _, v in items])

    # Restrict display to last 18 months
    cutoff = all_dates[-1] - timedelta(days=548)
    display_mask = [d >= cutoff for d in all_dates]
    disp_dates  = [d for d, m in zip(all_dates, display_mask) if m]
    disp_prices = all_prices[display_mask]

    # MAs computed on full history, then sliced
    ma50  = np.array(moving_average(all_prices.tolist(), 50))[display_mask]
    ma100 = np.array(moving_average(all_prices.tolist(), 100))[display_mask]
    ma200 = np.array(moving_average(all_prices.tolist(), 200))[display_mask]

    # ── Chart 1: Price & Moving Averages ──────────────────────────────────
    fig, ax = plt.subplots(figsize=(18, 8))

    # Background shading vs 200-DMA
    for i in range(1, len(disp_dates)):
        p, m = disp_prices[i], ma200[i]
        if np.isnan(m): continue
        color = "#34A853" if p > m else "#EA4335"
        ax.axvspan(disp_dates[i - 1], disp_dates[i], alpha=0.08, color=color, linewidth=0)

    ax.plot(disp_dates, disp_prices, color="#4285F4", linewidth=2.5, label="Price")
    ax.plot(disp_dates, ma50,  color="#F4B400", linewidth=2, label="50-DMA")
    ax.plot(disp_dates, ma100, color="#8F5DB7", linewidth=2, label="100-DMA")
    ax.plot(disp_dates, ma200, color="#EA4335", linewidth=2, label="200-DMA")

    last_price = disp_prices[-1]
    ax.axhline(last_price, color="#4285F4", linestyle="--", linewidth=1, alpha=0.6)
    ax.text(disp_dates[-1], last_price, f" ${last_price:.2f}", va="center", fontsize=14,
            color="#4285F4", fontweight="bold")

    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", fontsize=14)
    ax.tick_params(axis="y", labelsize=14)
    ax.set_ylabel("Price (USD)", fontsize=17)
    ax.set_title(f"{ticker} Price & Moving Averages", fontsize=22, fontweight="bold")
    ax.legend(fontsize=15)
    ax.grid(alpha=0.3)
    plt.tight_layout()
    out1 = f"{base}/{t}_ta_price_ma.png"
    plt.savefig(out1, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {out1}")

    # ── Chart 2: RSI ──────────────────────────────────────────────────────
    rsi_full = compute_rsi(all_prices.tolist(), period=14)
    rsi_disp = np.array(rsi_full)[display_mask]

    fig, ax = plt.subplots(figsize=(18, 6))
    ax.plot(disp_dates, rsi_disp, color="steelblue", linewidth=2.5)

    ax.axhline(70, color="#EA4335", linestyle="--", linewidth=1.5)
    ax.axhline(30, color="#34A853", linestyle="--", linewidth=1.5)

    # Shade zones
    ax.fill_between(disp_dates, 30, rsi_disp,
                    where=[r < 30 if not np.isnan(r) else False for r in rsi_disp],
                    color="#34A853", alpha=0.25)
    ax.fill_between(disp_dates, rsi_disp, 70,
                    where=[r > 70 if not np.isnan(r) else False for r in rsi_disp],
                    color="#EA4335", alpha=0.25)

    # Label current RSI
    valid_rsi = [(d, r) for d, r in zip(disp_dates, rsi_disp) if not np.isnan(r)]
    if valid_rsi:
        last_d, last_r = valid_rsi[-1]
        ax.annotate(f"RSI: {last_r:.1f}", xy=(last_d, last_r),
                    xytext=(-60, 10), textcoords="offset points",
                    fontsize=15, fontweight="bold", color="steelblue",
                    arrowprops=dict(arrowstyle="->", color="steelblue", lw=1.2))

    ax.set_ylim(0, 100)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", fontsize=14)
    ax.tick_params(axis="y", labelsize=14)
    ax.set_ylabel("RSI", fontsize=17)
    ax.set_title(f"{ticker} RSI (14) — Oversold <30 · Overbought >70",
                 fontsize=22, fontweight="bold")
    ax.grid(alpha=0.3)
    plt.tight_layout()
    out2 = f"{base}/{t}_ta_rsi.png"
    plt.savefig(out2, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {out2}")


if __name__ == "__main__":
    main()
