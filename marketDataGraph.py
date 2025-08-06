import yfinance as yf
import pandas as pd
import datetime as dt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import mplfinance as mpf

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
        pd.DataFrame or dict: A pandas DataFrame if a single ticker is provided,
                                or a dictionary of DataFrames if a list of tickers is provided.
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
            return pd.DataFrame() if isinstance(tickers, str) else {}
        else:
            print("Data downloaded successfully.")

        # If multiple tickers were requested, split the data into a dictionary of individual DataFrames
        if isinstance(tickers, list) and len(tickers) > 1:
            data_dict = {ticker: data.xs(ticker, axis=1, level=1) for ticker in tickers}
            return data_dict
        else:
            return data
            
    except Exception as e:
        print(f"An error occurred: {e}")
        return pd.DataFrame() if isinstance(tickers, str) else {}

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

# This function creates a candlestick chart.
def create_candlestick_chart(data, ticker):
    """
    Generates and displays a candlestick chart using mplfinance.

    Args:
        data (pd.DataFrame): The DataFrame containing OHLCV data.
        ticker (str): The ticker symbol for the stock.
    """
    if data.empty:
        print("No data to plot.")
        return

    print(f"Creating candlestick chart for {ticker}...")
    try:
        # IMPORTANT: Clean the data to ensure columns are of numeric type
        required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        
        # Check if the required columns exist before trying to access them
        if not all(col in data.columns for col in required_cols):
            print(f"Error: Missing one or more required columns for plotting: {required_cols}")
            print(f"Available columns: {data.columns.tolist()}")
            return
            
        plot_data = data[required_cols].copy()
        
        for col in plot_data.columns:
            plot_data[col] = pd.to_numeric(plot_data[col], errors='coerce')
        
        plot_data.dropna(inplace=True)

        # Create a title for the plot
        title_text = f"{ticker} Candlestick Chart"
        
        # Use mplfinance to plot the cleaned data
        # Save the chart instead of displaying
        save_path = f"{ticker}_candlestick_chart.png"
        mpf.plot(
            plot_data,
            type='candle',
            style='charles',
            title=title_text,
            ylabel='Price',
            volume=True,
            show_nontrading=False,
            figscale=1.5,
            savefig=save_path
        )
        print(f"Chart saved as {save_path}")
    except Exception as e:
        print(f"An error occurred while plotting: {e}")


# --- Example Usage ---
if __name__ == "__main__":
    # Example 1: Download historical data for a single stock (Apple)
    apple_data = get_historical_data('AAPL', start_date='2023-01-01', end_date='2024-01-01')
    if not apple_data.empty:
        print("\n--- Apple Historical Data (First 5 rows) ---")
        print(apple_data.head())
        print("\n--- Apple Historical Data (Last 5 rows) ---")
        print(apple_data.tail())
        create_candlestick_chart(apple_data, 'AAPL')

    # Example 2: Download historical data for multiple stocks (Microsoft and Google)
    stock_list = ['MSFT', 'GOOGL']
    multi_stock_data = get_historical_data(stock_list, interval='1mo')
    if multi_stock_data:
        print("\n--- Multiple Stocks Historical Data ---")
        for ticker, data in multi_stock_data.items():
            print(f"\n--- {ticker} Historical Data (First 5 rows) ---")
            print(data.head())
            create_candlestick_chart(data, ticker)
