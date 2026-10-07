"""
digest.py TICKER SECTION

Prints a compact, pre-computed JSON digest of the cached statement JSON for one
skill, so a skill reads ~1-2K tokens of exact figures instead of 3-6 raw JSON
files (and never does the arithmetic by hand). Every figure carries its source.

    PYTHONIOENCODING=utf-8 .venv/Scripts/python digest.py TSLA cash_flow

Sections: cash_flow, income_statement, balance_sheet, technical, metrics
Reads Outputs/{TICKER}/ only (technical also downloads SPY closes for relative returns);
run get_financial_data.fetch_all() first if JSON is missing.
"""
import json
import os
import sys
from datetime import date

from doc_utils import fmt_value

SEC, YAHOO, HYBRID, COMPUTED = "SEC EDGAR", "Yahoo Finance", "SEC EDGAR × Yahoo Finance (hybrid)", "computed"


def _load(ticker, name):
    path = f"Outputs/{ticker}/{ticker.lower()}_{name}.json"
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _series(data, key):
    """{date: value} for one line item, TTM key dropped, oldest first."""
    raw = data.get(key) or {}
    return dict(sorted((d, v) for d, v in raw.items() if d != "TTM" and v is not None))


def _ttm(data, key):
    return (data.get(key) or {}).get("TTM")


def _prior_year_date(dates, latest):
    """The period end closest to one year before `latest` (within 20 days), or None."""
    y, m, d = map(int, latest.split("-"))
    target = date(y - 1, m, min(d, 28))
    best = min(dates, key=lambda s: abs((date(*map(int, s.split("-"))) - target).days), default=None)
    if best and abs((date(*map(int, best.split("-"))) - target).days) <= 20:
        return best
    return None


def _ratio(a, b):
    if a is None or b in (None, 0):
        return None
    return round(a / b, 2)


def _pct(a, b):
    """Margin or share in percent."""
    r = _ratio(a, b)
    return None if r is None else round(a / b * 100, 1)


def _yoy(a, b):
    """YoY % change; 'n/m' when the sign flips or the base is negative (quote the $ change instead)."""
    if a is None or b in (None, 0):
        return None
    if b < 0 or (a < 0) != (b < 0):
        return "n/m"
    return round((a - b) / b * 100, 1)


def _money(v):
    return {"value": v, "fmt": fmt_value(v)}


def _compact(obj):
    """Collapse {"value", "fmt"} pairs to their fmt string (plus source when present) for printing."""
    if isinstance(obj, dict):
        if "fmt" in obj and "value" in obj:
            return f"{obj['fmt']} [{obj['source']}]" if "source" in obj else obj["fmt"]
        return {k: _compact(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_compact(v) for v in obj]
    return obj


def _period(cf, inc, when):
    """Cash-flow block for one period; `when` is a date string or 'TTM'."""
    get_cf = (lambda k: _ttm(cf["ttm"], k)) if when == "TTM" else (lambda k: _series(cf["q"], k).get(when))
    get_inc = (lambda k: _ttm(inc["ttm"], k)) if when == "TTM" else (lambda k: _series(inc["q"], k).get(when))
    rev, ni = get_inc("Total Revenue"), get_inc("Net Income")
    ocf, capex, fcf = get_cf("Operating Cash Flow"), get_cf("Capital Expenditure"), get_cf("Free Cash Flow")
    div = get_cf("Cash Dividends Paid")
    out = {
        "period": when,
        "revenue": _money(rev), "net_income": _money(ni),
        "operating_cash_flow": _money(ocf), "capex": _money(capex), "free_cash_flow": _money(fcf),
        "dividends_paid": _money(div),
        "ocf_margin_pct": _pct(ocf, rev), "fcf_margin_pct": _pct(fcf, rev),
        "ocf_to_net_income": _ratio(ocf, ni) if ni and ni > 0 else None,
        "fcf_to_net_income": _ratio(fcf, ni) if ni and ni > 0 else None,
    }
    if ni is not None and ni <= 0:
        out["conversion_note"] = "net income <= 0: conversion ratios not meaningful"
    return out


def cash_flow(ticker):
    cf = {"q": _load(ticker, "cash_flow_statement_quarterly"), "ttm": _load(ticker, "cash_flow_statement_ttm"),
          "a": _load(ticker, "cash_flow_statement_annual")}
    inc = {"q": _load(ticker, "income_statement_quarterly"), "ttm": _load(ticker, "income_statement_ttm")}
    bs = _load(ticker, "balance_sheet_quarterly")
    qm = _load(ticker, "quick_metrics")
    if not cf["q"]:
        sys.exit(f"No cash flow JSON for {ticker}: run get_financial_data.fetch_all(['{ticker}']) first")

    dates = list(_series(cf["q"], "Operating Cash Flow"))
    latest = dates[-1]
    prior = _prior_year_date(dates, latest)
    L, P, T = _period(cf, inc, latest), (_period(cf, inc, prior) if prior else None), _period(cf, inc, "TTM")

    yoy = {}
    if P:
        for k in ("operating_cash_flow", "capex", "free_cash_flow", "revenue", "net_income", "dividends_paid"):
            yoy[k + "_pct"] = _yoy(L[k]["value"], P[k]["value"])
        for k in ("ocf_margin_pct", "fcf_margin_pct"):
            if L[k] is not None and P[k] is not None:
                yoy[k.replace("_pct", "_change_pp")] = round(L[k] - P[k], 1)

    trend = []
    for d in dates[-8:]:
        p = _period(cf, inc, d)
        trend.append({"period": d, "net_income": p["net_income"]["fmt"], "ocf": p["operating_cash_flow"]["fmt"],
                      "fcf": p["free_cash_flow"]["fmt"], "fcf_to_ni": p["fcf_to_net_income"]})

    annual = []
    for d in list(_series(cf["a"], "Operating Cash Flow"))[-4:]:
        annual.append({"fiscal_year_end": d,
                       **{k: fmt_value(_series(cf["a"], src).get(d)) for k, src in
                          (("ocf", "Operating Cash Flow"), ("capex", "Capital Expenditure"), ("fcf", "Free Cash Flow"))}})

    # Coverage: SEC debt first, Yahoo fallback; a 0/missing SEC debt line is missing data, not zero debt.
    bs_date = list(_series(bs, "Total Assets"))[-1] if bs else None
    sec_debt = _series(bs, "Total Debt").get(bs_date) if bs_date else None
    debt, debt_src = sec_debt, SEC
    yahoo_debt = qm.get("totalDebt")
    if not sec_debt:
        debt, debt_src = yahoo_debt, f"{YAHOO} (SEC EDGAR Total Debt missing/0 — untagged, verify in 10-Q)"
    elif yahoo_debt and sec_debt < 0.5 * yahoo_debt:
        debt_src = (f"{SEC} — WARNING: under half of Yahoo totalDebt {fmt_value(yahoo_debt)}; the EDGAR tag is "
                    "likely incomplete (finance leases / other notes), confirm total debt in the 10-Q")
    cash = _series(bs, "Cash And Cash Equivalents").get(bs_date) if bs_date else None
    interest = _ttm(inc["ttm"], "Interest Expense")
    ocf_t, fcf_t, div_t = T["operating_cash_flow"]["value"], T["free_cash_flow"]["value"], T["dividends_paid"]["value"]
    mcap = qm.get("marketCap")

    industry, sector = qm.get("industry") or "", qm.get("sector") or ""
    return {
        "ticker": ticker,
        "company": qm.get("longName") or qm.get("shortName"),
        "industry": industry, "sector": sector,
        "is_reit": industry.startswith("REIT") or sector == "Real Estate",
        "units_note": "capex is a positive outflow; $ strings are fmt_value() output — paste as-is; pct = percent, pp = points",
        "sources": {"statements": SEC, "market_cap_price": YAHOO, "fcf_yield": HYBRID, "ratios": COMPUTED},
        "latest_quarter": L, "prior_year_quarter": P, "ttm": T, "yoy": yoy,
        "trend_8q": trend, "annual": annual,
        "coverage": {
            "balance_sheet_date": bs_date,
            "total_debt": {**_money(debt), "source": debt_src},
            "cash": {**_money(cash), "source": SEC},
            "interest_expense_ttm": {**_money(interest), "source": SEC},
            "ocf_to_interest": _ratio(ocf_t, abs(interest)) if interest else None,
            "ocf_to_total_debt": _ratio(ocf_t, debt),
            "fcf_to_dividends": _ratio(fcf_t, abs(div_t)) if div_t else None,
        },
        "market": {"price": qm.get("currentPrice"), "market_cap": _money(mcap),
                   "fcf_yield_ttm_pct": _pct(fcf_t, mcap)},
        "missing_from_sec": "no D&A, SBC, working-capital, buyback or debt repayment lines — WebSearch the 10-Q/10-K",
    }


def _quarter_pair(series_by_date):
    dates = list(series_by_date)
    if not dates:
        sys.exit("No quarterly statement data: run get_financial_data.fetch_all() first")
    latest = dates[-1]
    return latest, _prior_year_date(dates, latest)


def _cagr(first, last, years):
    if not first or not last or first <= 0 or last <= 0 or years <= 0:
        return None
    return round(((last / first) ** (1 / years) - 1) * 100, 1)


def income_statement(ticker):
    q, a, t = (_load(ticker, f"income_statement_{k}") for k in ("quarterly", "annual", "ttm"))
    qm = _load(ticker, "quick_metrics")
    rev_q = _series(q, "Total Revenue")
    L, P = _quarter_pair(rev_q)

    def block(when):
        get = (lambda k: _ttm(t, k)) if when == "TTM" else (lambda k: _series(q, k).get(when))
        rev = get("Total Revenue")
        out = {"period": when, "revenue": _money(rev)}
        for key, label in (("Gross Profit", "gross_profit"), ("Operating Income", "operating_income"),
                           ("Net Income", "net_income")):
            v = get(key)
            out[label] = _money(v)
            out[label.replace("_income", "").replace("_profit", "") + "_margin_pct"] = _pct(v, rev)
        out["diluted_eps"] = get("Diluted EPS")
        return out

    cur, prior, ttm = block(L), (block(P) if P else None), block("TTM")
    yoy = {}
    if prior:
        for k in ("revenue", "gross_profit", "operating_income", "net_income"):
            yoy[k + "_pct"] = _yoy(cur[k]["value"], prior[k]["value"])
        for k in ("gross_margin_pct", "operating_margin_pct", "net_margin_pct"):
            if cur[k] is not None and prior[k] is not None:
                yoy[k.replace("_pct", "_change_pp")] = round(cur[k] - prior[k], 1)
        if cur["diluted_eps"] is not None and prior["diluted_eps"]:
            yoy["diluted_eps_pct"] = _yoy(cur["diluted_eps"], prior["diluted_eps"])
        r, o = yoy.get("revenue_pct"), yoy.get("operating_income_pct")
        if isinstance(r, float) and isinstance(o, float) and r:
            yoy["operating_leverage_x"] = round(o / r, 2)

    ann_rev = _series(a, "Total Revenue")
    years = list(ann_rev)
    cagr3 = _cagr(ann_rev[years[-4]], ann_rev[years[-1]], 3) if len(years) >= 4 else None
    rev_growth = yoy.get("revenue_pct")
    rule40 = (round(rev_growth + cur["operating_margin_pct"], 1)
              if isinstance(rev_growth, float) and cur["operating_margin_pct"] is not None else None)
    return {
        "ticker": ticker, "company": qm.get("longName"), "sector": qm.get("sector"), "industry": qm.get("industry"),
        "is_reit": (qm.get("industry") or "").startswith("REIT") or qm.get("sector") == "Real Estate",
        "sources": {"statements": SEC, "ratios": COMPUTED},
        "latest_quarter": cur, "prior_year_quarter": prior, "ttm": ttm, "yoy": yoy,
        "revenue_3yr_cagr_pct": cagr3,
        "revenue_3yr_cagr_basis": f"FY{years[-4][:4]} → FY{years[-1][:4]}" if len(years) >= 4 else None,
        "rule_of_40_latest_q": rule40,
        "rule_of_40_basis": "latest-quarter revenue YoY % + latest-quarter operating margin %",
        "trend_tables": "use the income_trend report block (annual / quarterly) — do not re-type trend rows",
        "missing_from_sec": "drivers, guidance and consensus — WebSearch (see the skill's DATA SOURCING)",
    }


def balance_sheet(ticker):
    bs = _load(ticker, "balance_sheet_quarterly")
    qm = _load(ticker, "quick_metrics")
    L, P = _quarter_pair(_series(bs, "Total Assets"))
    keys = (("total_assets", "Total Assets"), ("current_assets", "Current Assets"),
            ("cash", "Cash And Cash Equivalents"), ("total_liabilities", "Total Liabilities"),
            ("current_liabilities", "Current Liabilities"), ("long_term_debt", "Long Term Debt"),
            ("total_debt", "Total Debt"), ("equity", "Stockholders Equity"), ("temporary_equity", "Temporary Equity"))

    def block(when):
        out = {"period": when}
        for k, src in keys:
            out[k] = _money(_series(bs, src).get(when))
        v = {k: out[k]["value"] for k, _ in keys}
        out["current_ratio"] = _ratio(v["current_assets"], v["current_liabilities"])
        out["debt_to_equity"] = _ratio(v["total_debt"], v["equity"])
        out["net_debt"] = _money(v["total_debt"] - v["cash"] if v["total_debt"] is not None and v["cash"] is not None else None)
        out["working_capital"] = _money(v["current_assets"] - v["current_liabilities"]
                                        if v["current_assets"] is not None and v["current_liabilities"] is not None else None)
        # dei share counts are dated at the 10-Q cover (weeks after quarter end): take the nearest within 60 days
        y, m, d = map(int, when.split("-"))
        sh = [(abs((date(*map(int, k.split("-"))) - date(y, m, d)).days), v)
              for k, v in _series(bs, "Shares Outstanding").items()]
        shares = min(sh)[1] if sh and min(sh)[0] <= 60 else None
        out["shares_outstanding"] = shares
        out["book_value_per_share"] = round(v["equity"] / shares, 2) if v["equity"] and shares else None
        return out

    cur, prior = block(L), (block(P) if P else None)
    yoy = {}
    if prior:
        for k, _ in keys:
            yoy[k + "_pct"] = _yoy(cur[k]["value"], prior[k]["value"])
        if cur["shares_outstanding"] and prior["shares_outstanding"]:
            yoy["shares_outstanding_pct"] = _yoy(cur["shares_outstanding"], prior["shares_outstanding"])
    flags = []
    sec_debt, yahoo_debt = cur["total_debt"]["value"], qm.get("totalDebt")
    if not sec_debt:
        flags.append(f"SEC EDGAR Total Debt missing/0 — untagged, not deleveraging; Yahoo totalDebt "
                     f"{fmt_value(yahoo_debt)}; verify in the 10-Q and distrust D/E and net debt here")
    elif yahoo_debt and sec_debt < 0.5 * yahoo_debt:
        flags.append(f"SEC EDGAR Total Debt {fmt_value(sec_debt)} is under half of Yahoo totalDebt "
                     f"{fmt_value(yahoo_debt)} — tag likely incomplete; confirm in the 10-Q")
    if cur["equity"]["value"] is not None and cur["equity"]["value"] < 0:
        flags.append("Negative stockholders' equity: D/E and ROE are arithmetic, not meaningful")
    if cur["temporary_equity"]["value"]:
        flags.append("Carries temporary (mezzanine) equity: Assets − Liabilities − Equity will not reconcile without it")
    return {
        "ticker": ticker, "company": qm.get("longName"), "sector": qm.get("sector"), "industry": qm.get("industry"),
        "is_reit": (qm.get("industry") or "").startswith("REIT") or qm.get("sector") == "Real Estate",
        "sources": {"statements": SEC, "ratios": COMPUTED},
        "note": "cash = cash & equivalents only (EDGAR line); short-term investments are not included",
        "latest_quarter": cur, "prior_year_quarter": prior, "yoy": yoy, "data_flags": flags,
        "missing_from_sec": "off-balance-sheet items (leases, VIEs, guarantees, purchase obligations) — 10-K/10-Q footnotes",
    }


def _rsi(prices, period=14):
    if len(prices) <= period:
        return []
    gains = [max(b - a, 0) for a, b in zip(prices, prices[1:])]
    losses = [max(a - b, 0) for a, b in zip(prices, prices[1:])]
    ag, al = sum(gains[:period]) / period, sum(losses[:period]) / period
    out = []
    for g, l in zip(gains[period:], losses[period:]):
        ag, al = (ag * (period - 1) + g) / period, (al * (period - 1) + l) / period
        out.append(100.0 if al == 0 else 100 - 100 / (1 + ag / al))
    return out


def _returns(closes, offsets):
    out = {}
    for name, (back, skip) in offsets.items():
        if len(closes) > back:
            end = closes[-1 - skip]
            out[name] = round((end / closes[-1 - back] - 1) * 100, 1)
        else:
            out[name] = None
    return out


def technical(ticker):
    ph = _load(ticker, "price_history")
    qm = _load(ticker, "quick_metrics")
    if not ph:
        sys.exit(f"No price history for {ticker}: run get_financial_data.fetch_all(['{ticker}']) first")
    dates = sorted(ph)
    closes = [ph[d] for d in dates]
    spot = closes[-1]

    def sma(n, end=None):
        seg = closes[:len(closes) - (end or 0)][-n:]
        return sum(seg) / n if len(seg) == n else None

    mas = {}
    for n in (20, 50, 100, 200):
        now, then = sma(n), sma(n, 10)
        slope = None if now is None or then is None else ("↑" if now > then * 1.002 else "↓" if now < then * 0.998 else "→")
        mas[f"{n}_dma"] = {"level": round(now, 2) if now else None,
                           "spot_vs_ma_pct": round((spot / now - 1) * 100, 1) if now else None,
                           "position": None if now is None else ("above" if spot > now else "below"),
                           "slope_vs_10d_ago": slope}
    lv = [mas[f"{n}_dma"]["level"] for n in (20, 50, 100, 200)]
    stack = ("bullish" if all(lv) and lv == sorted(lv, reverse=True)
             else "bearish" if all(lv) and lv == sorted(lv) else "mixed")

    crosses = []
    for i in range(max(200, len(closes) - 60), len(closes)):
        a50, a200 = sum(closes[i - 50:i]) / 50, sum(closes[i - 200:i]) / 200
        b50, b200 = sum(closes[i - 49:i + 1]) / 50, sum(closes[i - 199:i + 1]) / 200
        if a50 <= a200 and b50 > b200:
            crosses.append(f"golden cross {dates[i]}")
        elif a50 >= a200 and b50 < b200:
            crosses.append(f"death cross {dates[i]}")

    windows = {"1w": (5, 0), "1m": (21, 0), "3m": (63, 0), "6m": (126, 0), "12m_ex_last_month": (252, 21), "12m": (252, 0)}
    stock_ret = _returns(closes, windows)
    spy_ret, spy_note = {}, None
    try:
        import yfinance as yf
        spy = yf.download("SPY", period="2y", progress=False, auto_adjust=True)["Close"].squeeze()
        spy = [float(v) for v in spy.dropna().tolist()]
        spy_ret = _returns(spy, windows)
    except Exception as e:   # network or yfinance failure: leave S&P columns empty
        spy_note = f"SPY download failed ({type(e).__name__}); S&P 500 returns N/A"
    relative = {k: (round(stock_ret[k] - spy_ret[k], 1) if stock_ret.get(k) is not None and spy_ret.get(k) is not None
                    else None) for k in windows}

    last252 = closes[-252:]
    hi, lo = max(last252), min(last252)
    rsi = _rsi(closes)
    rsi_now = round(rsi[-1], 1) if rsi else None
    rsi_5d = round(rsi[-6], 1) if len(rsi) > 6 else None
    recent_low, prior_low = min(closes[-20:]), min(closes[-40:-20]) if len(closes) >= 40 else None
    yield_pct = qm.get("dividendYield")
    return {
        "ticker": ticker, "as_of": dates[-1], "spot_close": round(spot, 2),
        "yahoo_current_price": qm.get("currentPrice"),
        "sources": {"closes_mas_rsi_returns": "Yahoo Finance price history (computed)", "spy": "Yahoo Finance (SPY)"},
        "price_basis": ("dividend-adjusted closes (yfinance auto_adjust=True); yield "
                        f"{yield_pct}% — above ~2%: recompute on unadjusted closes per the skill"
                        if yield_pct and yield_pct > 2 else "dividend-adjusted closes (yfinance auto_adjust=True)"),
        "moving_averages": mas, "ma_stack": stack, "crosses_last_60_sessions": crosses or ["none"],
        "returns_pct": {"stock": stock_ret, "spy": spy_ret, "relative_pts": relative},
        "spy_note": spy_note,
        "range_52w_closing": {"high": round(hi, 2), "low": round(lo, 2),
                              "drawdown_from_high_pct": round((spot / hi - 1) * 100, 1),
                              "above_low_pct": round((spot / lo - 1) * 100, 1)},
        "range_52w_intraday_yahoo": {"high": qm.get("fiftyTwoWeekHigh"), "low": qm.get("fiftyTwoWeekLow")},
        "rsi_14": rsi_now, "rsi_14_5_sessions_ago": rsi_5d,
        "rsi_direction": None if rsi_now is None or rsi_5d is None else ("↑" if rsi_now > rsi_5d + 1 else "↓" if rsi_now < rsi_5d - 1 else "→"),
        "higher_low_last_20_vs_prior_20": None if prior_low is None else recent_low > prior_low,
        "beta": qm.get("beta"),
        "not_included": "VIX, CNN Fear & Greed, AAII, put/call, MACD — WebSearch",
    }


def metrics(ticker):
    from quick_stock_metrics import METRICS, compute_metrics, _short_comment
    m, src = compute_metrics(ticker, with_sources=True)
    rows = []
    for spec in METRICS:
        k = spec["key"]
        rows.append({"key": k, "label": spec["label"], "value": m.get(k), "source": src.get(k),
                     "benchmark_label": _short_comment(k, m.get(k), m)})
    return {"ticker": ticker, "note": "margin-style values are decimals (×100 for %); ratios are plain multiples",
            "metrics": rows}


SECTIONS = {"cash_flow": cash_flow, "income_statement": income_statement, "balance_sheet": balance_sheet,
            "technical": technical, "metrics": metrics}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in SECTIONS:
        sys.exit(__doc__)
    print(json.dumps(_compact(SECTIONS[sys.argv[2]](sys.argv[1].upper())), indent=1, ensure_ascii=False))
