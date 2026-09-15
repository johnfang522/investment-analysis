import json
import os
import yfinance as yf

# Income statement, balance sheet, and cash flow data now come from SEC
# EDGAR (sec_edgar_data.py) instead of Yahoo Finance, since Yahoo is often
# several weeks stale after an earnings release. This module is retained
# only for price history and quick_metrics (market cap, P/E, dividend
# yield, beta, analyst targets — quote/market data with no SEC EDGAR
# equivalent).
#
# Skills should not import from this module directly — use
# get_financial_data.py, which combines this module with sec_edgar_data.py
# behind a single fetch_all() / load_tickers() entry point.


def get_quick_metrics(ticker: str) -> dict:
    """
    Retrieve quick metrics for a publicly traded stock.

    Fetches the info dictionary from Yahoo Finance and saves it as a JSON file
    in the Outputs/ directory alongside this script.

    Args:
        ticker (str): The stock ticker symbol (e.g., "AAPL", "MSFT"). Case-insensitive.

    Returns:
        dict: A flat dictionary of stock fields (e.g., sector, industry,
              market cap, trailing P/E, revenue, analyst targets, etc.).

    Output files:
        Outputs/{ticker}_quick_metrics.json
    """
    ticker = ticker.upper()
    stock = yf.Ticker(ticker)
    base_path = os.path.dirname(os.path.abspath(__file__))

    data = stock.info

    output_path = os.path.join(base_path, "Outputs", ticker.upper())
    os.makedirs(output_path, exist_ok=True)

    output_file = os.path.join(output_path, f"{ticker.lower()}_quick_metrics.json")
    with open(output_file, "w") as f:
        json.dump(data, f, indent=4)

    return data


def get_price_history(ticker: str, years: int = 3) -> dict:
    """
    Retrieve daily closing price history for a stock.

    Fetches adjusted closing prices from Yahoo Finance for the last `years`
    years and saves the result as a JSON file in the Outputs/ directory.

    Args:
        ticker (str): The stock ticker symbol (e.g., "AAPL", "MSFT"). Case-insensitive.
        years (int): Number of years of history to fetch. Defaults to 3.

    Returns:
        dict: Date strings ("YYYY-MM-DD") mapped to adjusted closing prices.

    Output files:
        Outputs/{ticker}_price_history.json
    """
    ticker = ticker.upper()
    stock = yf.Ticker(ticker)
    base_path = os.path.dirname(os.path.abspath(__file__))

    hist = stock.history(period=f"{years}y")
    # yfinance can return a NaN close for the most recent row when a trading
    # day is still in progress / not yet fully settled — drop it rather than
    # writing "NaN" into the JSON (invalid JSON strictly, and it propagates
    # into RSI/technical-chart calculations as a NaN).
    data = {
        date.strftime("%Y-%m-%d"): round(float(close), 4)
        for date, close in hist["Close"].items()
        if close == close  # NaN != NaN
    }

    output_path = os.path.join(base_path, "Outputs", ticker.upper())
    os.makedirs(output_path, exist_ok=True)

    output_file = os.path.join(output_path, f"{ticker.lower()}_price_history.json")
    with open(output_file, "w") as f:
        json.dump(data, f, indent=4)

    return data


