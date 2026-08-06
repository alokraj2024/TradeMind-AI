import yfinance as yf
import pandas as pd

def fetch_data():
    # Example: Apple stock (you can change later)
    df = yf.download(
        "AAPL",          # stock symbol
        interval="5m",   # 1m, 5m, 15m etc.
        period="5d"      # last 5 days
    )

    df.reset_index(inplace=True)

    # Rename columns to match your ML pipeline
    df.rename(columns={
        "Datetime": "time",
        "Open": "open",
        "High": "high",
        "Low": "low",
        "Close": "close",
        "Volume": "volume"
    }, inplace=True)

    # Keep only required columns
    df = df[["time", "open", "high", "low", "close", "volume"]]

    df.to_csv("data/training_data.csv", index=False)
    print("✅ Data saved to data/training_data.csv")
    print(df.head())

if __name__ == "__main__":
    fetch_data()