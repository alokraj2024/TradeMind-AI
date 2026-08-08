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


# 🧠 AI COPILOT FUNCTION
def generate_signal_explanation(data: pd.DataFrame):
    latest = data.iloc[-1]
    prev = data.iloc[-2]

    signals = []

    # Trend (SMA)
    if pd.notna(latest["SMA_20"]) and latest["Close"] > latest["SMA_20"]:
        trend = "bullish"
        signals.append("price is trading above the 20-day moving average")
    else:
        trend = "bearish"
        signals.append("price is trading below the 20-day moving average")

    # RSI Momentum
    rsi = latest.get("RSI")
    if pd.notna(rsi) and rsi > 60:
        momentum = "strong"
        signals.append("momentum is strong (RSI above 60)")
    elif pd.notna(rsi) and rsi < 40:
        momentum = "weak"
        signals.append("momentum is weakening (RSI below 40)")
    else:
        momentum = "neutral"
        signals.append("momentum is neutral")

    # Volume
    if latest["Volume"] > prev["Volume"]:
        signals.append("volume is increasing, confirming the move")
    else:
        signals.append("volume is declining, indicating weak conviction")

    # Final signal
    if trend == "bullish" and momentum == "strong":
        signal = "BUY"
        confidence = 0.75
    elif trend == "bearish" and momentum == "weak":
        signal = "SELL"
        confidence = 0.75
    else:
        signal = "HOLD"
        confidence = 0.55

    explanation = f"The model suggests a {signal} signal because " + ", ".join(signals) + "."

    return {
        "signal": signal,
        "confidence": confidence,
        "explanation": explanation
    }


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

        if "time" not in raw_data.columns:
            raw_data = raw_data.reset_index()

        if "index" in raw_data.columns:
            raw_data.rename(columns={"index": "time"}, inplace=True)

        if "time" not in raw_data.columns:
            raise HTTPException(status_code=500, detail="Missing time column")

        raw_data["time"] = pd.to_datetime(raw_data["time"], errors="coerce", utc=True)

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

        # 🔹 Add indicators
        data = add_indicators(raw_data)

        # 🧠 GENERATE AI EXPLANATION HERE
        ai_output = generate_signal_explanation(data)

        if MODEL is None:
            raise RuntimeError("ML model is not available")

        # 🔹 ML Features
        feature_data = raw_data.rename(
            columns={
                "Date": "time",
                "Open": "open",
                "High": "high",
                "Low": "low",
                "Close": "close",
                "Volume": "volume",
            }
        )

        feature_data = feature_data[["time", "open", "high", "low", "close", "volume"]]

        feature_data = compute_features(feature_data)
        feature_data = feature_data.replace([float("inf"), float("-inf")], None)
        feature_data = feature_data.dropna()

        if feature_data.empty:
            raise RuntimeError("No valid feature data after cleaning")

        latest_row = feature_data.tail(1)

        prediction_result = make_prediction(MODEL, FEATURE_COLUMNS, latest_row)

        chart = build_chart_data(data)

        # 🔹 Sentiment
        headlines = get_news(symbol)
        sentiment_score = analyze_sentiment(headlines)

        sentiment = (
            "Positive" if sentiment_score > 0.05
            else "Negative" if sentiment_score < -0.05
            else "Neutral"
        )

        response = {
            "symbol": symbol.upper(),
            "interval": interval,
            "source": source,
            "price": chart[-1]["close"],

            # 🔥 ORIGINAL ML OUTPUT
            "signal": prediction_result["signal"],
            "confidence": prediction_result["confidence"],

            # 🧠 NEW AI COPILOT
            "ai": ai_output,

            "trend": "BULLISH" if prediction_result["signal"] == "BUY" else "BEARISH",
            "risk": "LOW" if prediction_result["signal"] == "BUY" else "HIGH",

            "sentiment": sentiment,
            "sentiment_score": sentiment_score,

            "chart": chart,
        }

        return response

    except Exception as e:
        print("❌ ANALYSIS ERROR:", e)
        raise HTTPException(status_code=500, detail=str(e))


# =========================================================
# 🔐 ROLE-BASED FINANCIAL RECORDS API
# =========================================================

DEMO_FINANCIAL_RECORDS = [
    {
        "id": 1,
        "title": "Quarterly Audit Grant",
        "amount": 24500.0,
        "role": "admin",
        "status": "Approved",
        "note": "Verified by lead auditor"
    },
    {
        "id": 2,
        "title": "Portfolio Dividend Payout",
        "amount": 3200.5,
        "role": "user",
        "status": "Pending",
        "note": "Awaiting settlement confirmation"
    },
    {
        "id": 3,
        "title": "Regulatory Compliance Fee",
        "amount": 15400.0,
        "role": "authority",
        "status": "Approved",
        "note": "Clearance certificate issued"
    },
    {
        "id": 4,
        "title": "High Volatility Stock Trade",
        "amount": 8900.75,
        "role": "reviewer",
        "status": "Flagged",
        "note": "Anomalous price spike flagged for inspection"
    },
    {
        "id": 5,
        "title": "Risk Review Clearance",
        "amount": 6750.0,
        "role": "reviewer",
        "status": "Resolved",
        "note": "Risk mitigation protocol accepted"
    },
    {
        "id": 6,
        "title": "Personal Portfolio Deposit",
        "amount": 1200.0,
        "role": "user",
        "status": "Approved",
        "note": "Standard user transfer"
    },
    {
        "id": 7,
        "title": "Institutional Transfer Fund",
        "amount": 45000.0,
        "role": "authority",
        "status": "Flagged",
        "note": "High value transfer requiring admin authorization"
    }
]

@router.get("/records/{role}")
def get_records_by_role(role: str):
    role_clean = role.strip().lower()

    if role_clean == "all":
        filtered = DEMO_FINANCIAL_RECORDS
    else:
        filtered = [
            r for r in DEMO_FINANCIAL_RECORDS
            if r.get("role", "").lower() == role_clean
        ]

    return {
        "role": role_clean,
        "count": len(filtered),
        "data": filtered
    }