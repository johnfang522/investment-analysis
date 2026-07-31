"""
Plots 5-year time series for the 7 market sentiment indicators plus
Treasury yields, the US fiscal picture, and margin debt (10 charts total).
Saves individual PNGs to Outputs/ and a combined summary PNG.
Run from project root: .venv/Scripts/python plot_market_sentiment_history.py
"""
import sys, os, warnings, re, json, io
warnings.filterwarnings("ignore")
sys.path.insert(0, '.')

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import requests
from datetime import datetime, timedelta

OUT = "Outputs"
os.makedirs(OUT, exist_ok=True)

END       = datetime(2026, 7, 31)
START     = END - timedelta(days=5 * 365 + 5)
START_STR = START.strftime("%Y-%m-%d")
END_STR   = END.strftime("%Y-%m-%d")

STYLE = {
    "figure.facecolor": "white",
    "axes.facecolor":   "white",
    "axes.edgecolor":   "#444444",
    "axes.labelcolor":  "#222222",
    "axes.titlesize":   13,
    "axes.titleweight": "bold",
    "axes.titlepad":    10,
    "xtick.color":      "#444444",
    "ytick.color":      "#444444",
    "grid.color":       "#dddddd",
    "grid.linestyle":   "--",
    "grid.linewidth":   0.6,
    "lines.linewidth":  1.8,
    "font.family":      "sans-serif",
}
plt.rcParams.update(STYLE)

C_BLUE   = "#1f77b4"
C_ORANGE = "#ff7f0e"
C_RED    = "#d62728"
C_GREEN  = "#2ca02c"
C_PURPLE = "#9467bd"

HDR = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

def fmt_xaxis(ax):
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_minor_locator(mdates.MonthLocator(bymonth=[4, 7, 10]))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.tick_params(axis="x", which="minor", length=3)

def add_current(ax, series, fmt="{:.1f}", color=C_RED, offset=(8, 8)):
    if series.empty:
        return
    last_val = series.dropna().iloc[-1]
    last_idx = series.dropna().index[-1]
    ax.axhline(last_val, color=color, lw=0.8, ls=":", alpha=0.7)
    ax.annotate(
        f"Now: {fmt.format(last_val)}",
        xy=(last_idx, last_val), xytext=(offset[0], offset[1]),
        textcoords="offset points", fontsize=9, color=color, fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.2", fc="white", ec=color, lw=0.8),
    )

def fetch_fred(series_id, rename=None, timeout=60, start=None):
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
    try:
        r = requests.get(url, headers=HDR, timeout=timeout)
        r.raise_for_status()
        text = r.text.strip()
        # Parse CSV robustly — FRED uses "DATE" as first column but may vary
        df = pd.read_csv(io.StringIO(text))
        # Normalise column names
        df.columns = [c.strip() for c in df.columns]
        date_col = next((c for c in df.columns if "DATE" in c.upper() or "date" in c.lower()), df.columns[0])
        val_col  = next((c for c in df.columns if c != date_col), None)
        if val_col is None:
            return pd.DataFrame()
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
        df = df.dropna(subset=[date_col]).set_index(date_col)
        col = rename or series_id
        df = df[[val_col]].rename(columns={val_col: col})
        df[col] = pd.to_numeric(df[col], errors="coerce")
        return df[df.index >= (start or START_STR)]
    except Exception as e:
        print(f"  FRED fetch failed ({series_id}): {e}")
        return pd.DataFrame()

def save_fig(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved {path}")

# ─────────────────────────── 1. VIX ─────────────────────────────────────────
print("Fetching VIX...")
vix = yf.download("^VIX", start=START_STR, end=END_STR, progress=False)["Close"].squeeze().dropna()

fig, ax = plt.subplots(figsize=(11, 4.5))
ax.fill_between(vix.index, vix, alpha=0.15, color=C_BLUE)
ax.plot(vix.index, vix, color=C_BLUE, lw=1.6)
ax.axhline(15, color=C_GREEN,  lw=1.0, ls="--", label="15 — complacency threshold")
ax.axhline(20, color=C_ORANGE, lw=1.0, ls="--", label="20 — caution zone")
ax.axhline(30, color=C_RED,    lw=1.0, ls="--", label="30 — fear zone")
add_current(ax, vix)
ax.set_title("VIX — CBOE Volatility Index (5-Year)")
ax.set_ylabel("VIX Level")
ax.legend(fontsize=9, loc="upper right")
fmt_xaxis(ax)
fig.tight_layout()
save_fig(fig, "sentiment_vix.png")

# ──────────────────── 2. Market Breadth: RSP vs SPY ─────────────────────────
print("Fetching RSP & SPY...")
rsp = yf.download("RSP", start=START_STR, end=END_STR, progress=False)["Close"].squeeze().dropna()
spy = yf.download("SPY", start=START_STR, end=END_STR, progress=False)["Close"].squeeze().dropna()

common  = rsp.index.intersection(spy.index)
rsp_idx = (rsp.loc[common] / rsp.loc[common].iloc[0]) * 100
spy_idx = (spy.loc[common] / spy.loc[common].iloc[0]) * 100
spread  = rsp_idx - spy_idx

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 7), sharex=True,
                                gridspec_kw={"height_ratios": [2, 1]})
ax1.plot(rsp_idx.index, rsp_idx, color=C_GREEN, lw=1.8, label="RSP (Equal-Weight S&P 500)")
ax1.plot(spy_idx.index, spy_idx, color=C_BLUE,  lw=1.8, label="SPY (Cap-Weight S&P 500)")
ax1.set_ylabel("Indexed (100 = 5yr ago)")
ax1.set_title("Market Breadth — RSP vs SPY (5-Year, Indexed)")
ax1.legend(fontsize=9)

ax2.fill_between(spread.index, spread, where=(spread >= 0), color=C_GREEN, alpha=0.35, label="RSP leading (bullish breadth)")
ax2.fill_between(spread.index, spread, where=(spread <  0), color=C_RED,   alpha=0.35, label="SPY leading (narrow rally)")
ax2.plot(spread.index, spread, color="#333333", lw=1.0)
ax2.axhline(0,  color="#666666", lw=0.8)
ax2.axhline(-5, color=C_RED,   lw=0.9, ls="--", alpha=0.7, label="-5pp warning threshold")
ax2.axhline( 5, color=C_GREEN, lw=0.9, ls="--", alpha=0.7, label="+5pp healthy threshold")
ax2.set_ylabel("RSP − SPY (pp)")
ax2.legend(fontsize=8, loc="lower left")
fmt_xaxis(ax2)
fig.tight_layout()
save_fig(fig, "sentiment_breadth.png")

# ─────────────────────── 3. HY OAS Spread ───────────────────────────────────
print("Fetching HY OAS from FRED...")
hy_df = fetch_fred("BAMLH0A0HYM2", rename="HY_OAS")
hy    = hy_df["HY_OAS"].dropna() if not hy_df.empty else pd.Series(dtype=float)

if not hy.empty:
    # FRED BAMLH0A0HYM2 is expressed in percentage points (e.g. 2.78 = 278 bps)
    # Convert to basis points for display
    hy_bps = hy * 100
    fig, ax = plt.subplots(figsize=(11, 4.5))
    ax.fill_between(hy_bps.index, hy_bps, alpha=0.15, color=C_ORANGE)
    ax.plot(hy_bps.index, hy_bps, color=C_ORANGE, lw=1.6)
    ax.axhline(300, color=C_GREEN,  lw=1.0, ls="--", label="300 bps — complacency threshold")
    ax.axhline(500, color=C_ORANGE, lw=1.0, ls="--", label="500 bps — neutral zone")
    ax.axhline(700, color=C_RED,    lw=1.0, ls="--", label="700 bps — stress zone")
    add_current(ax, hy_bps, fmt="{:.0f} bps", color=C_RED)
    ax.set_title("ICE BofA HY OAS Spread (5-Year)")
    ax.set_ylabel("Option-Adjusted Spread (bps)")
    ax.legend(fontsize=9)
    fmt_xaxis(ax)
    fig.tight_layout()
    save_fig(fig, "sentiment_hy_oas.png")
else:
    print("  Skipping HY OAS chart — data unavailable")

# ──────────────────────── 4. Shiller CAPE ───────────────────────────────────
print("Fetching Shiller CAPE from multpl.com...")
cape_series = pd.Series(dtype=float)
try:
    r = requests.get(
        "https://www.multpl.com/shiller-pe/table/by-month",
        headers=HDR, timeout=30,
    )
    for tbl in pd.read_html(io.StringIO(r.text)):
        if tbl.shape[1] >= 2:
            tbl.columns  = ["Date", "Value"] + list(tbl.columns[2:])
            tbl["Date"]  = pd.to_datetime(tbl["Date"], errors="coerce")
            tbl["Value"] = pd.to_numeric(
                tbl["Value"].astype(str).str.replace(",", ""), errors="coerce"
            )
            tbl = tbl.dropna(subset=["Date", "Value"])
            if len(tbl) > 10:
                cape_series = tbl.set_index("Date")["Value"].sort_index()
                cape_series = cape_series[cape_series.index >= START_STR]
                break
except Exception as e:
    print(f"  multpl.com fetch failed: {e}")

if not cape_series.empty:
    fig, ax = plt.subplots(figsize=(11, 4.5))
    ax.fill_between(cape_series.index, cape_series, alpha=0.15, color=C_PURPLE)
    ax.plot(cape_series.index, cape_series, color=C_PURPLE, lw=1.8)
    ax.axhline(35, color=C_RED,    lw=1.0, ls="--", label="35 — bubble warning threshold")
    ax.axhline(25, color=C_ORANGE, lw=1.0, ls="--", label="25 — expensive")
    ax.axhline(17, color=C_GREEN,  lw=1.0, ls="--", label="17 — long-run average")
    add_current(ax, cape_series, fmt="{:.1f}", color=C_RED, offset=(8, 10))
    ax.set_title("Shiller CAPE Ratio (5-Year)")
    ax.set_ylabel("CAPE (Cyclically Adjusted P/E)")
    ax.legend(fontsize=9)
    fmt_xaxis(ax)
    fig.tight_layout()
    save_fig(fig, "sentiment_cape.png")
else:
    print("  Skipping CAPE chart — data unavailable")

# ──────────────────────── 5. Buffett Indicator ──────────────────────────────
print("Fetching Buffett Indicator (FTW5000 / GDP proxy)...")
buffett = pd.Series(dtype=float)

# Wilshire 5000 was removed from FRED in June 2024; use ^FTW5000 from Yahoo Finance
# GDP (quarterly) from FRED — normalise ratio to known anchor: ~233% on 2026-05-22
ftw_raw = yf.download("^FTW5000", start=START_STR, end=END_STR, progress=False)
if not ftw_raw.empty:
    ftw_col = ftw_raw["Close"]
    ftw = (ftw_col.iloc[:, 0] if hasattr(ftw_col, "columns") else ftw_col).dropna()
    gdp_df = fetch_fred("GDP", rename="GDP")
    if not gdp_df.empty:
        gdp_ff = gdp_df["GDP"].resample("D").ffill()
        common = ftw.index.intersection(gdp_ff.index)
        if len(common) > 20:
            raw_ratio = ftw.loc[common] / gdp_ff.loc[common]
            # Scale to % using known anchor: Buffett ≈ 233% on 2026-05-22
            anchor_date = pd.Timestamp("2026-05-22")
            anchor_raw  = raw_ratio.asof(anchor_date)
            if pd.notna(anchor_raw) and anchor_raw > 0:
                scale   = 233.0 / anchor_raw
                buffett = (raw_ratio * scale).clip(lower=0)
                buffett = buffett[buffett.index >= START_STR]
                print(f"  Buffett: {len(buffett)} rows, current={buffett.iloc[-1]:.1f}%")
    else:
        print("  GDP fetch failed — skipping Buffett chart")
else:
    print("  ^FTW5000 unavailable — skipping Buffett chart")

if not buffett.empty:
    fig, ax = plt.subplots(figsize=(11, 4.5))
    ax.fill_between(buffett.index, buffett, alpha=0.15, color=C_RED)
    ax.plot(buffett.index, buffett, color=C_RED, lw=1.8)
    ax.axhline(160, color=C_RED,    lw=1.0, ls="--", label="160% — bubble warning threshold")
    ax.axhline(120, color=C_ORANGE, lw=1.0, ls="--", label="120% — overvalued")
    ax.axhline(100, color=C_GREEN,  lw=1.0, ls="--", label="100% — fair value (approx)")
    add_current(ax, buffett, fmt="{:.0f}%", color=C_RED, offset=(8, 10))
    ax.set_title("Buffett Indicator — Market Cap / GDP (5-Year)")
    ax.set_ylabel("Market Cap as % of GDP")
    ax.legend(fontsize=9)
    fmt_xaxis(ax)
    fig.tight_layout()
    save_fig(fig, "sentiment_buffett.png")
else:
    print("  Skipping Buffett chart — data unavailable")

# ──────────────────── 6. CNN Fear & Greed ───────────────────────────────────
print("Fetching CNN Fear & Greed historical data...")
fg_series = pd.Series(dtype=float)

# Primary: CNN dataviz API
try:
    r = requests.get(
        "https://production.dataviz.cnn.io/index/fearandgreed/graphdata",
        headers={**HDR, "Referer": "https://www.cnn.com/markets/fear-and-greed"},
        timeout=30,
    )
    if r.status_code == 200:
        data = r.json()
        rows = data.get("fear_and_greed_historical", {}).get("data", [])
        if not rows:
            rows = data.get("data", [])
        if rows:
            df_fg = pd.DataFrame(rows)
            # x = ms timestamp, y = score
            df_fg["date"]  = pd.to_datetime(df_fg["x"], unit="ms")
            df_fg["score"] = pd.to_numeric(df_fg["y"], errors="coerce")
            fg_series = df_fg.set_index("date")["score"].sort_index().dropna()
            fg_series = fg_series[fg_series.index >= START_STR]
            print(f"  CNN F&G: {len(fg_series)} rows via dataviz API")
except Exception as e:
    print(f"  CNN F&G dataviz API failed: {e}")

# Fallback: finhacker.cz table
if fg_series.empty:
    try:
        r = requests.get(
            "https://www.finhacker.cz/en/fear-and-greed-index-historical-data-and-chart/",
            headers=HDR, timeout=30,
        )
        for tbl in pd.read_html(io.StringIO(r.text)):
            if tbl.shape[1] >= 2:
                tbl.columns = ["Date", "Score"] + list(tbl.columns[2:])
                tbl["Date"]  = pd.to_datetime(tbl["Date"],  errors="coerce")
                tbl["Score"] = pd.to_numeric(tbl["Score"].astype(str).str.extract(r"(\d+)")[0], errors="coerce")
                tbl = tbl.dropna(subset=["Date", "Score"])
                if len(tbl) > 20:
                    fg_series = tbl.set_index("Date")["Score"].sort_index()
                    fg_series = fg_series[fg_series.index >= START_STR]
                    print(f"  CNN F&G: {len(fg_series)} rows via finhacker.cz")
                    break
    except Exception as e:
        print(f"  finhacker.cz fallback failed: {e}")

if not fg_series.empty:
    fig, ax = plt.subplots(figsize=(11, 4.5))
    ax.fill_between(fg_series.index, fg_series,
                    where=(fg_series >= 50), color=C_GREEN, alpha=0.20, label="Greed (≥50)")
    ax.fill_between(fg_series.index, fg_series,
                    where=(fg_series <  50), color=C_RED,   alpha=0.20, label="Fear (<50)")
    ax.plot(fg_series.index, fg_series, color="#333333", lw=1.4)
    ax.axhline(75, color=C_RED,    lw=1.0, ls="--", label="75 — extreme greed")
    ax.axhline(50, color="#888888", lw=0.8, ls="-")
    ax.axhline(25, color=C_GREEN,  lw=1.0, ls="--", label="25 — extreme fear")
    add_current(ax, fg_series, fmt="{:.0f}", color=C_RED, offset=(8, 5))
    ax.set_ylim(0, 100)
    ax.set_title("CNN Fear & Greed Index (5-Year)")
    ax.set_ylabel("Score (0 = Extreme Fear, 100 = Extreme Greed)")
    ax.legend(fontsize=9)
    fmt_xaxis(ax)
    fig.tight_layout()
    save_fig(fig, "sentiment_fear_greed.png")
else:
    print("  CNN F&G historical data unavailable — skipping chart")

# ──────────────────── 7. CBOE SKEW Index (tail-risk / put-demand proxy) ──────
# The CBOE equity P/C ratio is not available historically beyond 2019 via free sources.
# The SKEW Index (^SKEW) measures the perceived tail risk of the S&P 500 as reflected
# in options pricing — high SKEW = elevated demand for downside protection (puts).
print("Fetching CBOE SKEW Index (put-demand / tail-risk proxy)...")
skew_raw = yf.download("^SKEW", start=START_STR, end=END_STR, progress=False)
skew = skew_raw["Close"].squeeze().dropna() if not skew_raw.empty else pd.Series(dtype=float)

if not skew.empty:
    skew_smooth = skew.rolling(20, min_periods=5).mean()
    fig, ax = plt.subplots(figsize=(11, 4.5))
    ax.plot(skew.index, skew, color="#cccccc", lw=0.8, label="Daily")
    ax.plot(skew_smooth.index, skew_smooth, color=C_BLUE, lw=1.8, label="20-day avg")
    ax.axhline(150, color=C_RED,    lw=1.0, ls="--", label="150 — elevated tail risk")
    ax.axhline(135, color=C_ORANGE, lw=1.0, ls="--", label="135 — caution zone")
    ax.axhline(115, color=C_GREEN,  lw=1.0, ls="--", label="115 — complacency")
    add_current(ax, skew_smooth.dropna(), fmt="{:.1f}", color=C_RED, offset=(8, 5))
    ax.set_title("CBOE SKEW Index — Tail-Risk / Put-Demand Proxy (5-Year)")
    ax.set_ylabel("SKEW Level")
    ax.legend(fontsize=9)
    ax.annotate(
        "Note: SKEW > 130 indicates elevated put-buying for tail protection.\n"
        "Used here as a proxy for put/call demand (P/C ratio not freely available post-2019).",
        xy=(0.01, 0.03), xycoords="axes fraction", fontsize=8, color="#666666",
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#cccccc", lw=0.8),
    )
    fmt_xaxis(ax)
    fig.tight_layout()
    save_fig(fig, "sentiment_putcall.png")
    print(f"  SKEW: {len(skew)} rows, current={skew.iloc[-1]:.1f}")
else:
    print("  SKEW data unavailable — skipping chart")

# ──────────────── 8. Treasury Yields (10Y, 2Y, curve) ───────────────────────
print("Fetching Treasury yields from FRED...")
d10 = fetch_fred("DGS10", rename="Y10")
d02 = fetch_fred("DGS2",  rename="Y2")

if not d10.empty and not d02.empty:
    y10 = d10["Y10"].dropna()
    y2  = d02["Y2"].dropna()
    common = y10.index.intersection(y2.index)
    curve  = y10.loc[common] - y2.loc[common]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 7), sharex=True,
                                   gridspec_kw={"height_ratios": [2, 1]})
    ax1.plot(y10.index, y10, color=C_BLUE,   lw=1.8, label="10-Year")
    ax1.plot(y2.index,  y2,  color=C_ORANGE, lw=1.8, label="2-Year")
    ax1.axhline(4.5, color=C_ORANGE, lw=1.0, ls="--", label="4.5% — equity valuation headwind")
    ax1.axhline(5.0, color=C_RED,    lw=1.0, ls="--", label="5.0% — danger zone")
    add_current(ax1, y10, fmt="{:.2f}%", color=C_RED)
    ax1.set_ylabel("Yield (%)")
    ax1.set_title("US Treasury Yields — 10Y vs 2Y (5-Year)")
    ax1.legend(fontsize=9)

    ax2.fill_between(curve.index, curve, where=(curve >= 0), color=C_GREEN, alpha=0.35, label="Normal (10Y > 2Y)")
    ax2.fill_between(curve.index, curve, where=(curve <  0), color=C_RED,   alpha=0.35, label="Inverted")
    ax2.plot(curve.index, curve, color="#333333", lw=1.0)
    ax2.axhline(0, color="#666666", lw=0.8)
    ax2.set_ylabel("10Y − 2Y (pp)")
    ax2.legend(fontsize=8, loc="lower right")
    fmt_xaxis(ax2)
    fig.tight_layout()
    save_fig(fig, "sentiment_treasury_yields.png")
    print(f"  Yields: 10Y={y10.iloc[-1]:.2f}%, 2Y={y2.iloc[-1]:.2f}%, curve={curve.iloc[-1]:+.2f}pp")
else:
    print("  Treasury yield data unavailable — skipping chart")

# ──────────────── 9. US Fiscal — Deficit & Net Interest ─────────────────────
print("Fetching fiscal data from FRED...")
# MTSDS133FMS is monthly, $ millions, deficit months negative. Fetch extra
# history so the 12-month rolling window is complete at the chart's left edge.
fiscal_start = (START - timedelta(days=400)).strftime("%Y-%m-%d")
mts_df = fetch_fred("MTSDS133FMS", rename="DEFICIT", start=fiscal_start)
int_df = fetch_fred("A091RC1Q027SBEA", rename="INTEREST")

if not mts_df.empty:
    deficit_12m = (-mts_df["DEFICIT"].rolling(12, min_periods=12).sum() / 1e6).dropna()
    deficit_12m = deficit_12m[deficit_12m.index >= START_STR]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 7), sharex=True,
                                   gridspec_kw={"height_ratios": [2, 1]})
    ax1.fill_between(deficit_12m.index, deficit_12m, alpha=0.15, color=C_RED)
    ax1.plot(deficit_12m.index, deficit_12m, color=C_RED, lw=1.8)
    ax1.axhline(1.0, color=C_ORANGE, lw=1.0, ls="--", label="$1T")
    ax1.axhline(2.0, color=C_RED,    lw=1.0, ls="--", label="$2T — heavy issuance zone")
    add_current(ax1, deficit_12m, fmt="${:.2f}T", color=C_RED)
    ax1.set_ylabel("Trailing 12M Deficit ($T)")
    ax1.set_title("US Federal Deficit (Trailing 12M) & Net Interest Outlays (5-Year)")
    ax1.legend(fontsize=9)

    if not int_df.empty:
        interest = int_df["INTEREST"].dropna()  # quarterly, SAAR, $B
        ax2.fill_between(interest.index, interest, alpha=0.15, color=C_PURPLE)
        ax2.plot(interest.index, interest, color=C_PURPLE, lw=1.8)
        add_current(ax2, interest, fmt="${:.0f}B", color=C_PURPLE)
        ax2.set_ylabel("Net Interest (SAAR, $B)")
    else:
        ax2.text(0.5, 0.5, "Net interest data unavailable", ha="center", va="center",
                 transform=ax2.transAxes, fontsize=10, color="#888888")
    fmt_xaxis(ax2)
    fig.tight_layout()
    save_fig(fig, "sentiment_fiscal.png")
    print(f"  Fiscal: trailing-12M deficit=${deficit_12m.iloc[-1]:.2f}T")
else:
    print("  Fiscal deficit data unavailable — skipping chart")

# ──────────────── 10. Margin Debt (level + % of GDP) ────────────────────────
print("Fetching margin debt from FRED...")
# Z.1 quarterly margin loans (broker-dealer receivables from customers), $ millions.
# FINRA's monthly series is more current but has no free CSV endpoint.
md_df  = fetch_fred("BOGZ1FL663067003Q", rename="MARGIN")
gdp_md = fetch_fred("GDP", rename="GDP")

if not md_df.empty and not gdp_md.empty:
    margin_b  = (md_df["MARGIN"].dropna() / 1e3)          # $B
    gdp_ff    = gdp_md["GDP"].resample("D").ffill()       # $B
    common    = margin_b.index.intersection(gdp_ff.index)
    md_gdp    = (margin_b.loc[common] / gdp_ff.loc[common]) * 100

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 7), sharex=True,
                                   gridspec_kw={"height_ratios": [1, 1]})
    ax1.fill_between(margin_b.index, margin_b, alpha=0.15, color=C_PURPLE)
    ax1.plot(margin_b.index, margin_b, color=C_PURPLE, lw=1.8)
    add_current(ax1, margin_b, fmt="${:.0f}B", color=C_PURPLE)
    ax1.set_ylabel("Margin Loans ($B)")
    ax1.set_title("Margin Debt — Level & % of GDP (5-Year, quarterly Fed Z.1)")

    ax2.fill_between(md_gdp.index, md_gdp, alpha=0.15, color=C_RED)
    ax2.plot(md_gdp.index, md_gdp, color=C_RED, lw=1.8)
    ax2.axhline(2.6, color=C_GREEN,  lw=1.0, ls="--", label="2.6% — 2007 peak")
    ax2.axhline(2.8, color=C_ORANGE, lw=1.0, ls="--", label="2.8% — 2000 peak")
    ax2.axhline(3.8, color=C_RED,    lw=1.0, ls="--", label="3.8% — 2021 peak")
    add_current(ax2, md_gdp, fmt="{:.2f}%", color=C_RED)
    ax2.set_ylabel("Margin Debt / GDP (%)")
    ax2.legend(fontsize=9, loc="lower right")
    ax2.annotate(
        "Note: plotted line is the Fed Z.1 broker-dealer margin-loans series, a narrower measure than\n"
        "FINRA's monthly margin statistics (the basis for the 2000/2007/2021 peak reference lines).\n"
        "Compare the FINRA-basis current reading from the report text against those peaks, not this line.",
        xy=(0.01, 0.63), xycoords="axes fraction", fontsize=8, color="#666666",
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#cccccc", lw=0.8),
    )
    fmt_xaxis(ax2)
    fig.tight_layout()
    save_fig(fig, "sentiment_margin_debt.png")
    print(f"  Margin: ${margin_b.iloc[-1]:.0f}B, {md_gdp.iloc[-1]:.2f}% of GDP")
else:
    print("  Margin debt data unavailable — skipping chart")

# ──────────────── Combined Summary Dashboard ─────────────────────────────────
print("\nBuilding combined dashboard...")
chart_order = [
    ("sentiment_vix.png",        "VIX"),
    ("sentiment_fear_greed.png", "CNN Fear & Greed"),
    ("sentiment_putcall.png",    "Put/Call Ratio"),
    ("sentiment_breadth.png",    "Market Breadth (RSP vs SPY)"),
    ("sentiment_hy_oas.png",     "HY OAS Spread"),
    ("sentiment_cape.png",       "Shiller CAPE"),
    ("sentiment_buffett.png",    "Buffett Indicator"),
    ("sentiment_treasury_yields.png", "Treasury Yields"),
    ("sentiment_fiscal.png",     "US Fiscal"),
    ("sentiment_margin_debt.png", "Margin Debt"),
]
available = [(os.path.join(OUT, f), t) for f, t in chart_order if os.path.exists(os.path.join(OUT, f))]

if available:
    n    = len(available)
    cols = 2
    rows = (n + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(20, rows * 5.2))
    axes = axes.flatten()
    from matplotlib.image import imread
    for i, (path, title) in enumerate(available):
        axes[i].imshow(imread(path))
        axes[i].axis("off")
    for j in range(len(available), len(axes)):
        axes[j].axis("off")
    fig.suptitle(f"Market Sentiment Dashboard — {END.strftime('%B %d, %Y')}", fontsize=16, fontweight="bold", y=1.005)
    fig.tight_layout()
    save_fig(fig, f"sentiment_dashboard_{END.strftime('%Y%m%d')}.png")

print(f"\nDone. {len(available)}/{len(chart_order)} charts saved to Outputs/")
