print("✅ ANALYZE ROUTE FILE LOADED")

from fastapi import APIRouter
from utils.stock_api import fetch_stock_data
from services.indicators import add_indicators
from services.strategy import generate_signal

router = APIRouter(prefix="/analyze")

@router.get("/{symbol}")
def analyze_stock(symbol: str):
    data = fetch_stock_data(symbol)
    data = add_indicators(data)

    signal = generate_signal(data)

    return {
        "trend": signal.get("trend"),
        "confidence": signal.get("confidence"),
        "risk": signal.get("risk"),
        "explanation": signal.get("explanation"),
        "technical": signal.get("technical"),
        "sentiment": signal.get("sentiment"),
    }
