import pandas as pd
import numpy as np

# ================================
# 📊 INDICATORS
# ================================

def add_indicators(df):
    df = df.copy()

    # Moving Averages
    df["SMA_20"] = df["Close"].rolling(window=20).mean()
    df["EMA_50"] = df["Close"].ewm(span=50, adjust=False).mean()
    df["EMA_200"] = df["Close"].ewm(span=200, adjust=False).mean()

    # RSI
    delta = df["Close"].diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = (-delta.clip(upper=0)).rolling(14).mean()
    rs = gain / loss
    df["RSI"] = 100 - (100 / (1 + rs))

    # MACD
    ema12 = df["Close"].ewm(span=12, adjust=False).mean()
    ema26 = df["Close"].ewm(span=26, adjust=False).mean()
    df["MACD"] = ema12 - ema26
    df["MACD_SIGNAL"] = df["MACD"].ewm(span=9, adjust=False).mean()

    # Volume Spike
    df["VOL_AVG"] = df["Volume"].rolling(20).mean()
    df["VOL_SPIKE"] = df["Volume"] > 1.5 * df["VOL_AVG"]

    return df


# ================================
# 🧠 STRATEGY ENGINE
# ================================

def generate_signal(df):
    latest = df.iloc[-1]
    prev = df.iloc[-2]

    score = 0
    signals = []

    # ======================
    # 📈 TREND ANALYSIS
    # ======================
    if latest["Close"] > latest["EMA_200"]:
        trend = "BULLISH"
        score += 2
    else:
        trend = "BEARISH"
        score -= 2

    # ======================
    # ⚡ MOMENTUM (RSI)
    # ======================
    if latest["RSI"] < 30:
        score += 2
        signals.append("RSI indicates oversold (potential reversal)")
    elif latest["RSI"] > 70:
        score -= 2
        signals.append("RSI indicates overbought (pullback risk)")

    # ======================
    # 🔁 MACD CROSSOVER
    # ======================
    if prev["MACD"] < prev["MACD_SIGNAL"] and latest["MACD"] > latest["MACD_SIGNAL"]:
        score += 3
        signals.append("Bullish MACD crossover")
    elif prev["MACD"] > prev["MACD_SIGNAL"] and latest["MACD"] < latest["MACD_SIGNAL"]:
        score -= 3
        signals.append("Bearish MACD crossover")

    # ======================
    # 📊 MOVING AVERAGE CONFIRMATION
    # ======================
    if latest["Close"] > latest["EMA_50"]:
        score += 1
    else:
        score -= 1

    # ======================
    # 📢 VOLUME CONFIRMATION
    # ======================
    if latest["VOL_SPIKE"]:
        score += 1
        signals.append("High volume confirms move")

    # ======================
    # 🎯 FINAL DECISION
    # ======================
    if score >= 5:
        action = "STRONG BUY"
    elif score >= 3:
        action = "BUY"
    elif score >= 1:
        action = "HOLD"
    elif score <= -5:
        action = "STRONG SELL"
    elif score <= -3:
        action = "SELL"
    else:
        action = "HOLD"

    # ======================
    # ⚠️ RISK ANALYSIS
    # ======================
    risk = "LOW"

    if trend == "BEARISH" and action in ["BUY", "STRONG BUY"]:
        risk = "HIGH"

    if latest["RSI"] > 75 or latest["RSI"] < 25:
        risk = "HIGH"

    # ======================
    # 💬 EXPLANATION
    # ======================
    explanation = f"""
    Trend: {trend}
    Score: {score}

    Signals:
    - {'; '.join(signals) if signals else 'No strong signals'}

    Risk Level: {risk}
    """

    return {
        "action": action,
        "score": score,
        "confidence": min(95, 50 + abs(score) * 10),
        "trend": trend,
        "risk": risk,
        "explanation": explanation.strip(),
        "technical": "; ".join(signals) if signals else "No strong technical signals",
        "sentiment": "News sentiment is not available yet",
    }
