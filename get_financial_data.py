"""
Generic financial data module — the single entry point every skill should
use to pre-populate `Outputs/{TICKER}/` JSON before reading it.

Combines two underlying sources:
  - sec_edgar_data.py    — income statement, balance sheet, cash flow
                            statement (SEC EDGAR XBRL; not subject to
                            Yahoo Finance's multi-week post-earnings lag)
  - yahoo_finance_data.py — quick_metrics and price history (market
                            cap, P/E, dividend yield, beta, analyst
                            targets, price series — quote/market data
                            with no SEC EDGAR equivalent)

Skills and scripts should call `fetch_all()` / `load_tickers()` from here
rather than importing yahoo_finance_data.py or sec_edgar_data.py directly.

Usage:
    .venv/Scripts/python get_financial_data.py            # reads tickers.txt
    .venv/Scripts/python get_financial_data.py AAPL MSFT  # explicit tickers
"""

import os
import sys

from sec_edgar_data import fetch_edgar_statements
from yahoo_finance_data import get_quick_metrics, get_price_history


def load_tickers(path: str = None) -> list[str]:
    """
    Read ticker symbols from a file, one per line. Lines starting with '#'
    and blank lines are ignored.

    Args:
        path (str): Path to the tickers file. Defaults to tickers.txt in the
                    same directory as this script.

    Returns:
        list[str]: Uppercased ticker symbols.
    """
    if path is None:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tickers.txt")
    with open(path) as f:
        return [
            line.strip().upper()
            for line in f
            if line.strip() and not line.strip().startswith("#")
        ]


def fetch_all(tickers: list[str]) -> dict:
    """
    Pre-generate all available data for a list of tickers: income statement,
    balance sheet, and cash flow statement from SEC EDGAR
    (sec_edgar_data.fetch_edgar_statements), plus quick_metrics and
    price_history from Yahoo Finance (yahoo_finance_data.py).

    Args:
        tickers (list[str]): List of ticker symbols.

    Returns:
        dict: Keyed by ticker symbol, each value is a dict with keys
              'sec_statements', 'quick_metrics', and 'price_history'
              (or {'error': str} if fetching failed for that ticker).
    """
    results = {}
    for ticker in tickers:
        print(f"Fetching {ticker}...")
        try:
            results[ticker] = {
                "sec_statements": fetch_edgar_statements(ticker),
                "quick_metrics": get_quick_metrics(ticker),
                "price_history": get_price_history(ticker),
            }
            print(f"  {ticker} done.")
        except Exception as e:
            print(f"  {ticker} failed: {e}")
            results[ticker] = {"error": str(e)}
    return results


if __name__ == "__main__":
    tickers = [t.upper() for t in sys.argv[1:]] if len(sys.argv) > 1 else load_tickers()
    if not tickers:
        print("No tickers found in tickers.txt.")
    else:
        print(f"Loaded {len(tickers)} ticker(s): {', '.join(tickers)}")
        fetch_all(tickers)
