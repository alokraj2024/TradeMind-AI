import pandas as pd


def add_indicators(df):
    df = df.copy()

    # =========================
    # 📊 MOVING AVERAGES
    # =========================
    df["SMA_20"] = df["Close"].rolling(window=20).mean()
    df["SMA_50"] = df["Close"].rolling(window=50).mean()
    df["EMA_50"] = df["Close"].ewm(span=50, adjust=False).mean()
    df["EMA_200"] = df["Close"].ewm(span=200, adjust=False).mean()

    # =========================
    # ⚡ RSI (Improved)
    # =========================
    delta = df["Close"].diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()

    rs = avg_gain / avg_loss
    df["RSI"] = 100 - (100 / (1 + rs))

    # =========================
    # 🚀 MACD (VERY IMPORTANT)
    # =========================
    ema12 = df["Close"].ewm(span=12, adjust=False).mean()
    ema26 = df["Close"].ewm(span=26, adjust=False).mean()

    df["MACD"] = ema12 - ema26
    df["MACD_SIGNAL"] = df["MACD"].ewm(span=9, adjust=False).mean()

    # =========================
    # 📉 VOLATILITY (RISK)
    # =========================
    df["Returns"] = df["Close"].pct_change()
    df["Volatility"] = df["Returns"].rolling(window=20).std()
    df["VOL_AVG"] = df["Volume"].rolling(window=20).mean()
    df["VOL_SPIKE"] = df["Volume"] > (1.5 * df["VOL_AVG"])

    return df
