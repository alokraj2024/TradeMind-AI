print("✅ ANALYZE ROUTE FILE LOADED")

from fastapi import APIRouter, HTTPException
import pandas as pd
from engines.sentiment import analyze_sentiment
from engines.prediction import load_model, make_prediction
from ml.features import compute_features
from services.news_service import get_news
from services.market_data import get_market_data
from services.indicators import add_indicators

router = APIRouter(prefix="/analyze")

MODEL = None
FEATURE_COLUMNS = []
try:
    MODEL, FEATURE_COLUMNS = load_model()
except Exception as exc:
    print(f"⚠️  Warning: ML model could not be loaded: {exc}")


def build_chart_data(data: pd.DataFrame) -> list[dict]:
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
def analyze_stock(symbol: str, interval: str = "1d"):
    try:
        # 🔹 Step 1: Fetch Data
        result = get_market_data(symbol, interval)

        if result.get("error"):
            raise HTTPException(status_code=404, detail=result["error"])

        source = result.get("source")
        data_rows = result.get("data", [])

        if not isinstance(data_rows, list) or not data_rows:
            raise HTTPException(
                status_code=404,
                detail="Invalid symbol or no data available"
            )

        raw_data = pd.DataFrame(data_rows)

        # ✅ Ensure time column exists
        if "time" not in raw_data.columns:
            raw_data = raw_data.reset_index()

        if "index" in raw_data.columns:
            raw_data.rename(columns={"index": "time"}, inplace=True)

        if "time" not in raw_data.columns:
            raise HTTPException(status_code=500, detail="Missing time column")

        # ✅ Normalize datetime
        raw_data["time"] = pd.to_datetime(raw_data["time"], errors="coerce", utc=True)

        # 🔹 Prepare OHLC format
        raw_data["Date"] = raw_data["time"]

        raw_data = raw_data.rename(
            columns={
                "open": "Open",
                "high": "High",
                "low": "Low",
                "close": "Close",
                "volume": "Volume",
            }
        )

        raw_data = raw_data[["Date", "Open", "High", "Low", "Close", "Volume"]]

        # ✅🔥 CRITICAL FIX: ADD TIME COLUMN HERE
        feature_data = raw_data.rename(
            columns={
                "Date": "time",   # ⭐ THIS WAS MISSING
                "Open": "open",
                "High": "high",
                "Low": "low",
                "Close": "close",
                "Volume": "volume",
            }
        )

        # ✅ Ensure correct structure
        feature_data = feature_data[["time", "open", "high", "low", "close", "volume"]]

        # 🔹 Add indicators (for chart only)
        data = add_indicators(raw_data)

        if MODEL is None:
            raise RuntimeError("ML model is not available")

        # 🔹 Compute ML features
        feature_data = compute_features(feature_data)

        # ✅ Clean data
        feature_data = feature_data.replace([float("inf"), float("-inf")], None)
        feature_data = feature_data.dropna()

        if feature_data.empty:
            raise RuntimeError("No valid feature data after cleaning")

        latest_row = feature_data.tail(1)

        # 🔹 Predict
        prediction_result = make_prediction(MODEL, FEATURE_COLUMNS, latest_row)

        chart = build_chart_data(data)

        # 🔹 Sentiment
        headlines = get_news(symbol)
        sentiment_score = analyze_sentiment(headlines)

        if sentiment_score > 0.05:
            sentiment = "Positive"
        elif sentiment_score < -0.05:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"

        # 🔹 Extract prediction
        signal = prediction_result["signal"]
        confidence_value = prediction_result["confidence"]
        features_used = prediction_result.get("features_used", [])
        error_info = prediction_result.get("error")

        # 🔹 Derived metrics
        trend = "BULLISH" if signal == "BUY" else "BEARISH" if signal == "SELL" else "NEUTRAL"
        risk = "LOW" if signal == "BUY" else "HIGH" if signal == "SELL" else "MEDIUM"
        score = round((confidence_value - 50) / 5, 2)

        explanation = f"AI model predicts {signal} with {confidence_value}% confidence."
        technical = "XGBoost model using price, trend, and volatility features."

        response = {
            "symbol": symbol.upper(),
            "interval": interval,
            "source": source,
            "price": chart[-1]["close"],
            "signal": signal,
            "confidence": confidence_value,
            "features_used": features_used,
            "action": signal,
            "score": score,
            "trend": trend,
            "risk": risk,
            "explanation": explanation,
            "technical": technical,
            "sentiment": sentiment,
            "sentiment_score": sentiment_score,
            "signals": {
                "technical": technical,
                "sentiment": sentiment,
                "risk": risk,
            },
            "chart": chart,
        }

        if error_info:
            response["error"] = error_info

        return response

    except Exception as e:
        print("❌ ANALYSIS ERROR:", e)
        raise HTTPException(status_code=500, detail=str(e))