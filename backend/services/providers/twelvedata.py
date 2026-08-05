import json
import os
from dotenv import load_dotenv
from typing import Any, Dict, List
from urllib import parse, request

load_dotenv()

from utils.interval_mapper import map_interval
from utils.normalizer import normalize_ohlcv

TWELVE_DATA_URL = os.getenv("TWELVE_DATA_URL", "https://api.twelvedata.com/time_series")
TWELVE_DATA_API_KEY = os.getenv("TWELVE_DATA_API_KEY", "").strip()


def _http_get(url: str, timeout: int = 20) -> str:
    req = request.Request(url, headers={"User-Agent": "TradeMindAI/1.0"})
    with request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8")


def fetch(symbol: str, interval: str, outputsize: int = 180) -> Dict[str, Any]:
    if not TWELVE_DATA_API_KEY:
        return {"error": "Missing TWELVE_DATA_API_KEY", "symbol": symbol}

    mapped_interval = map_interval("twelvedata", interval)
    params = {
        "symbol": symbol,
        "interval": mapped_interval,
        "outputsize": str(outputsize),
        "format": "JSON",
        "apikey": TWELVE_DATA_API_KEY,
    }
    url = f"{TWELVE_DATA_URL}?{parse.urlencode(params)}"
    raw = _http_get(url)
    payload = json.loads(raw)

    if payload.get("status") == "error":
        return {"error": payload.get("message", "Twelve Data returned an error"), "symbol": symbol}

    values = payload.get("values")
    if not isinstance(values, list) or not values:
        return {"error": "No Twelve Data values returned", "symbol": symbol}

    rows: List[Dict[str, Any]] = []
    for item in values:
        date_value = item.get("datetime") or item.get("date")
        if not date_value:
            continue

        rows.append(
            {
                "time": date_value,
                "open": item.get("open"),
                "high": item.get("high"),
                "low": item.get("low"),
                "close": item.get("close"),
                "volume": item.get("volume", 0),
            }
        )

    return {"source": "twelvedata", "data": normalize_ohlcv(rows)}
