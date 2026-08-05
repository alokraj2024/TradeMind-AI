import yfinance as yf
import pandas as pd

def fetch_stock_data(symbol: str):
    try:
        stock = yf.Ticker(symbol)
        df = stock.history(period="3mo", interval="1d")

        if df.empty:
            raise ValueError("No data returned")

        df.reset_index(inplace=True)

        return df

    except Exception as e:
        print("❌ Error fetching stock data:", e)
        return pd.DataFrame()