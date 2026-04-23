import json
import os
import yfinance as yf


def _df_to_dict(df) -> dict:
    df = df.copy()
    df.columns = [col.strftime("%Y-%m-%d") if hasattr(col, "strftime") else str(col) for col in df.columns]
    return json.loads(df.to_json(orient="index"))


def get_income_statements(ticker: str) -> dict:
    """
    Retrieve income statement data for a publicly traded stock.

    Fetches quarterly and annual income statements from Yahoo Finance and
    computes a trailing twelve months (TTM) figure by summing the four most
    recent quarters. Results are also saved as JSON files in the Outputs/
    directory alongside this script.

    Args:
        ticker (str): The stock ticker symbol (e.g., "AAPL", "MSFT"). Case-insensitive.

    Returns:
        dict: A dictionary with three keys:
            - "quarterly" (dict): Income statement line items keyed by metric name,
              each containing a dict of date strings ("YYYY-MM-DD") to values.
            - "annual" (dict): Same structure as quarterly but for annual periods.
            - "ttm" (dict): Same structure with a single "TTM" column representing
              the sum of the four most recent quarters.

    Raises:
        ValueError: If fewer than four quarters of data are available to compute TTM.

    Output files:
        Outputs/{ticker}_income_statement_quarterly.json
        Outputs/{ticker}_income_statement_annual.json
        Outputs/{ticker}_income_statement_ttm.json
    """
    ticker = ticker.upper()
    stock = yf.Ticker(ticker)
    base_path = os.path.dirname(os.path.abspath(__file__))

    quarterly = stock.quarterly_income_stmt
    annual = stock.income_stmt

    if quarterly.empty or quarterly.shape[1] < 4:
        raise ValueError("Not enough quarterly data to calculate TTM.")
    ttm = quarterly.iloc[:, :4].sum(axis=1).to_frame(name="TTM")

    results = {
        "quarterly": _df_to_dict(quarterly),
        "annual": _df_to_dict(annual),
        "ttm": _df_to_dict(ttm),
    }

    output_path = os.path.join(base_path, "Outputs", ticker.upper())
    os.makedirs(output_path, exist_ok=True)

    for period, data in results.items():
        output_file = os.path.join(output_path, f"{ticker.lower()}_income_statement_{period}.json")
        with open(output_file, "w") as f:
            json.dump(data, f, indent=4)

    return results


def get_balance_sheets(ticker: str) -> dict:
    """
    Retrieve the most recent quarterly balance sheet data for a publicly traded stock.

    Fetches quarterly balance sheet data from Yahoo Finance. Results are also
    saved as a JSON file in the Outputs/ directory alongside this script.

    Args:
        ticker (str): The stock ticker symbol (e.g., "AAPL", "MSFT"). Case-insensitive.

    Returns:
        dict: Balance sheet line items keyed by metric name, each containing a dict
            of date strings ("YYYY-MM-DD") to values. Covers the most recent quarters
            available from Yahoo Finance (typically up to 4).

    Output files:
        Outputs/{ticker}_balance_sheet_quarterly.json
    """
    ticker = ticker.upper()
    stock = yf.Ticker(ticker)
    base_path = os.path.dirname(os.path.abspath(__file__))

    quarterly = stock.quarterly_balance_sheet

    output_path = os.path.join(base_path, "Outputs", ticker.upper())
    os.makedirs(output_path, exist_ok=True)

    data = _df_to_dict(quarterly)
    output_file = os.path.join(output_path, f"{ticker.lower()}_balance_sheet_quarterly.json")
    with open(output_file, "w") as f:
        json.dump(data, f, indent=4)

    return data


def get_cash_flow_statements(ticker: str) -> dict:
    """
    Retrieve cash flow statement data for a publicly traded stock.

    Fetches quarterly and annual cash flow statements from Yahoo Finance and
    computes a trailing twelve months (TTM) figure by summing the four most
    recent quarters. Results are also saved as JSON files in the Outputs/
    directory alongside this script.

    Args:
        ticker (str): The stock ticker symbol (e.g., "AAPL", "MSFT"). Case-insensitive.

    Returns:
        dict: A dictionary with three keys:
            - "quarterly" (dict): Cash flow line items keyed by metric name,
              each containing a dict of date strings ("YYYY-MM-DD") to values.
            - "annual" (dict): Same structure as quarterly but for annual periods.
            - "ttm" (dict): Same structure with a single "TTM" column representing
              the sum of the four most recent quarters.

    Raises:
        ValueError: If fewer than four quarters of data are available to compute TTM.

    Output files:
        Outputs/{ticker}_cash_flow_statement_quarterly.json
        Outputs/{ticker}_cash_flow_statement_annual.json
        Outputs/{ticker}_cash_flow_statement_ttm.json
    """
    ticker = ticker.upper()
    stock = yf.Ticker(ticker)
    base_path = os.path.dirname(os.path.abspath(__file__))

    quarterly = stock.quarterly_cashflow
    annual = stock.cashflow

    if quarterly.empty or quarterly.shape[1] < 4:
        raise ValueError("Not enough quarterly data to calculate TTM.")
    ttm = quarterly.iloc[:, :4].sum(axis=1).to_frame(name="TTM")

    results = {
        "quarterly": _df_to_dict(quarterly),
        "annual": _df_to_dict(annual),
        "ttm": _df_to_dict(ttm),
    }

    output_path = os.path.join(base_path, "Outputs", ticker.upper())
    os.makedirs(output_path, exist_ok=True)

    for period, data in results.items():
        output_file = os.path.join(output_path, f"{ticker.lower()}_cash_flow_statement_{period}.json")
        with open(output_file, "w") as f:
            json.dump(data, f, indent=4)

    return results



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
    data = {
        date.strftime("%Y-%m-%d"): round(float(close), 4)
        for date, close in hist["Close"].items()
    }

    output_path = os.path.join(base_path, "Outputs", ticker.upper())
    os.makedirs(output_path, exist_ok=True)

    output_file = os.path.join(output_path, f"{ticker.lower()}_price_history.json")
    with open(output_file, "w") as f:
        json.dump(data, f, indent=4)

    return data


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
    Pre-generate all available Yahoo Finance data for a list of tickers.

    Calls get_income_statements, get_balance_sheets, get_cash_flow_statements,
    get_quick_metrics, and get_price_history for each ticker and collects the results.

    Args:
        tickers (list[str]): List of ticker symbols.

    Returns:
        dict: Keyed by ticker symbol, each value is a dict with keys
              'income_statements', 'balance_sheet', 'cash_flow_statements',
              'quick_metrics', and 'price_history'.
    """
    results = {}
    for ticker in tickers:
        print(f"Fetching {ticker}...")
        try:
            results[ticker] = {
                "income_statements": get_income_statements(ticker),
                "balance_sheet": get_balance_sheets(ticker),
                "cash_flow_statements": get_cash_flow_statements(ticker),
                "quick_metrics": get_quick_metrics(ticker),
                "price_history": get_price_history(ticker),
            }
            print(f"  {ticker} done.")
        except Exception as e:
            print(f"  {ticker} failed: {e}")
            results[ticker] = {"error": str(e)}
    return results


if __name__ == "__main__":
    tickers = load_tickers()
    if not tickers:
        print("No tickers found in tickers.txt.")
    else:
        print(f"Loaded {len(tickers)} ticker(s): {', '.join(tickers)}")
        fetch_all(tickers)
