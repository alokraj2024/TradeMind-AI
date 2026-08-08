import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ✅ IMPORT ROUTES
from routes.analyze import router as analyze_router

# ✅ NEW IMPORTS (ADD THIS 👇)
import pandas as pd
from fastapi.responses import FileResponse

app = FastAPI(title="TradeMind AI", version="0.1.0")

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ INCLUDE ROUTES
app.include_router(analyze_router)

@app.get("/")
def root():
    return {"message": "TradeMind AI Backend Running 🚀"}

@app.get("/health")
def health_check():
    return {"status": "ok"}


# =========================================================
# ✅ 🚀 ADD THIS EXPORT FEATURE (PASTE BELOW)
# =========================================================

@app.get("/export/{symbol}")
def export_summary(symbol: str):

    from datetime import datetime
    import os
    import pandas as pd
    from fastapi.responses import FileResponse

    # 🔹 TODO: Replace with real data from your analysis
    data = {
        "symbol": symbol,
        "signal": "BUY",
        "confidence": 0.82,
        "rsi": 28,
        "sma": 150,
        "sentiment": "Positive"
    }

    # ✅ Compute summary
    summary = {
        "Symbol": symbol,
        "Signal": data["signal"],
        "Confidence": data["confidence"],
        "RSI": data["rsi"],
        "SMA": data["sma"],
        "Sentiment": data["sentiment"],
        "Flag": "Oversold" if data["rsi"] < 30 else "Normal",
        "Recommendation": "Buy (Strong momentum)",
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # ✅ NEW
    }

    df = pd.DataFrame([summary])

    # ✅ ONE GLOBAL HISTORY FILE
    file_name = "signals_history.csv"

    # ✅ APPEND MODE (🔥 IMPORTANT CHANGE)
    if os.path.exists(file_name):
        df.to_csv(file_name, mode='a', header=False, index=False)
    else:
        df.to_csv(file_name, index=False)

    # ✅ RETURN FULL HISTORY FILE
    return FileResponse(
        path=file_name,
        media_type="text/csv",
        filename=file_name
    )

# =========================================================


# ✅ AI COPILOT FUNCTION
def generate_signal_explanation(df):
    latest = df.iloc[-1]
    prev = df.iloc[-2]

    signals = []

    # Trend
    if latest["close"] > latest["sma_20"]:
        trend = "bullish"
        signals.append("price is trading above the 20-day moving average")
    else:
        trend = "bearish"
        signals.append("price is trading below the 20-day moving average")

    # Momentum (MACD)
    if latest["macd"] > latest["macd_signal"]:
        momentum = "strong"
        signals.append("momentum is strengthening (MACD bullish crossover)")
    else:
        momentum = "weak"
        signals.append("momentum is weakening (MACD bearish crossover)")

    # Volume
    if latest["volume"] > prev["volume"]:
        signals.append("volume is increasing, confirming the move")
    else:
        signals.append("volume is declining, indicating weak conviction")

    # Final signal
    if trend == "bullish" and momentum == "strong":
        signal = "BUY"
    else:
        signal = "SELL"

    explanation = f"The model suggests a {signal} signal because " + ", ".join(signals) + "."

    return {
        "signal": signal,
        "confidence": 0.7,
        "explanation": explanation
    }