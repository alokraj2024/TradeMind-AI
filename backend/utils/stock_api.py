import yfinance as yf
import pandas as pd


def fetch_stock_data(symbol: str):
    try:
        stock = yf.Ticker(symbol)

        # Get last 3 months of data
        # Six months of daily data provides enough trading days for a
        # 100-point chart after calculating the technical indicators.
        df = stock.history(period="6mo", interval="1d")

        if df.empty:
            return None

        # Reset index for easier handling
        df.reset_index(inplace=True)

        return df

    except Exception as e:
        print("❌ Error fetching stock data:", e)
        return None
