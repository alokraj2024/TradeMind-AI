print("✅ ANALYZE ROUTE FILE LOADED")

from fastapi import APIRouter, HTTPException
import pandas as pd
from engines.sentiment import analyze_sentiment
from services.news_service import get_news
from utils.stock_api import fetch_stock_data
from services.indicators import add_indicators
from services.strategy import generate_signal

router = APIRouter(prefix="/analyze")


def build_chart_data(data: pd.DataFrame) -> list[dict]:
    """Create the latest 100 OHLC candles, indicators, and RSI markers."""
    chart = []

    for _, row in data.tail(100).iterrows():
        rsi = row.get("RSI")
        signal = "HOLD"
        if pd.notna(rsi) and rsi < 20:
            signal = "STRONG BUY"
        elif pd.notna(rsi) and rsi < 30:
            signal = "BUY"
        elif pd.notna(rsi) and rsi > 80:
            signal = "STRONG SELL"
        elif pd.notna(rsi) and rsi > 70:
            signal = "SELL"

        chart.append(
            {
                "time": pd.Timestamp(row["Date"]).strftime("%Y-%m-%d"),
                "open": round(float(row["Open"]), 2),
                "high": round(float(row["High"]), 2),
                "low": round(float(row["Low"]), 2),
                "close": round(float(row["Close"]), 2),
                "sma_20": (
                    round(float(row["SMA_20"]), 2)
                    if pd.notna(row["SMA_20"])
                    else None
                ),
                "rsi": round(float(rsi), 2) if pd.notna(rsi) else None,
                "signal": signal,
            }
        )

    return chart


@router.get("/{symbol}")
def analyze_stock(symbol: str):
    # 🔹 Step 1: Fetch Data
    data = fetch_stock_data(symbol)

    if data is None or data.empty:
        raise HTTPException(
            status_code=404,
            detail="Invalid stock symbol or no data available"
        )

    try:
        # 🔹 Step 2: Add Indicators
        data = add_indicators(data)
        chart = build_chart_data(data)

        # 🔹 Step 3: Generate Signal
        signal = generate_signal(data)

        headlines = get_news(symbol)
        sentiment_score = analyze_sentiment(headlines)
        if sentiment_score > 0.05:
            sentiment = "Positive"
        elif sentiment_score < -0.05:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"

        if not isinstance(signal, dict):
            raise ValueError("Signal generation failed")

        # 🔹 Step 4: Return Clean Response
        return {
            "symbol": symbol.upper(),
            "price": chart[-1]["close"],
            "action": signal.get("action"),
            "score": signal.get("score"),
            "trend": signal.get("trend"),
            "confidence": signal.get("confidence"),
            "risk": signal.get("risk"),
            "explanation": signal.get("explanation"),
            "technical": signal.get("technical"),
            "sentiment": sentiment,
            "sentiment_score": sentiment_score,
            "signals": {
                "technical": signal.get("technical"),
                "sentiment": sentiment,
                "risk": signal.get("risk"),
            },
            "chart": chart,
        }

    except Exception as e:
        print("❌ ANALYSIS ERROR:", e)
        raise HTTPException(
            status_code=500,
            detail="Error analyzing stock"
        )
