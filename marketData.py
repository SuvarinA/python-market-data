import yfinance as yf
import pandas as pd
import datetime as dt

# This function fetches historical market data for a given ticker or list of tickers.
def get_historical_data(tickers, start_date=None, end_date=None, interval='1d'):
    """
    Downloads historical market data from Yahoo Finance.

    Args:
        tickers (str or list): The ticker symbol(s) for the stock(s) you want to download.
        start_date (str, optional): The start date for the data in 'YYYY-MM-DD' format.
                                    Defaults to 1 year ago.
        end_date (str, optional): The end date for the data in 'YYYY-MM-DD' format.
                                  Defaults to today.
        interval (str, optional): The data interval (e.g., '1d', '1wk', '1mo').
                                  Defaults to '1d'.

    Returns:
        pd.DataFrame: A pandas DataFrame containing the historical market data.
    """
    if start_date is None:
        start_date = (dt.date.today() - dt.timedelta(days=365)).strftime('%Y-%m-%d')
    if end_date is None:
        end_date = dt.date.today().strftime('%Y-%m-%d')

    print(f"Downloading historical data for {tickers} from {start_date} to {end_date}...")
    try:
        data = yf.download(tickers, start=start_date, end=end_date, interval=interval)
        if data.empty:
            print("No data found. Please check the ticker symbol(s) or date range.")
        else:
            print("Data downloaded successfully.")
        return data
    except Exception as e:
        print(f"An error occurred: {e}")
        return pd.DataFrame()

# This function fetches a Ticker object for a single ticker.
def get_ticker_info(ticker):
    """
    Creates a yfinance Ticker object to access more detailed information.

    Args:
        ticker (str): The ticker symbol for the stock.

    Returns:
        yf.Ticker: A yfinance Ticker object.
    """
    print(f"Fetching information for ticker: {ticker}...")
    try:
        ticker_obj = yf.Ticker(ticker)
        return ticker_obj
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# --- Example Usage ---
if __name__ == "__main__":
    # Example 1: Download historical data for a single stock (Apple)
    apple_data = get_historical_data('AAPL', start_date='2023-01-01', end_date='2024-01-01')
    if not apple_data.empty:
        print("\n--- Apple Historical Data (First 5 rows) ---")
        print(apple_data.head())
        print("\n--- Apple Historical Data (Last 5 rows) ---")
        print(apple_data.tail())

    # Example 2: Download historical data for multiple stocks (Microsoft and Google)
    stock_list = ['MSFT', 'GOOGL']
    multi_stock_data = get_historical_data(stock_list, interval='1mo')
    if not multi_stock_data.empty:
        print("\n--- Multiple Stocks Historical Data (First 5 rows) ---")
        print(multi_stock_data.head())

    # Example 3: Get detailed info for a single ticker (Tesla)
    tesla_ticker = get_ticker_info('TSLA')
    if tesla_ticker:
        print("\n--- Tesla Company Info ---")
        # Accessing various attributes from the ticker object
        info = tesla_ticker.info
        print(f"Company Name: {info.get('longName')}")
        print(f"Sector: {info.get('sector')}")
        print(f"Current Price: {info.get('currentPrice')}")
        print(f"Market Cap: {info.get('marketCap')}")
        print(f"Dividend Rate: {info.get('dividendRate')}")
