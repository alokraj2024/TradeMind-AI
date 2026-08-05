import pandas as pd

def add_indicators(df):
    # Moving Average (Simple)
    df["SMA_20"] = df["Close"].rolling(window=20).mean()

    # RSI
    delta = df["Close"].diff()
    
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    
    rs = gain / loss
    df["RSI"] = 100 - (100 / (1 + rs))

    return df