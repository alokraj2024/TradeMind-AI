import json
import os
from typing import Any, Dict, List
from urllib import parse, request

from utils.interval_mapper import map_interval
from utils.normalizer import normalize_ohlcv

BINANCE_KLINES_URL = os.getenv("BINANCE_KLINES_URL", "https://api.binance.com/api/v3/klines")


def _http_get(url: str, timeout: int = 20) -> str:
    req = request.Request(url, headers={"User-Agent": "TradeMindAI/1.0"})
    with request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8")


def fetch(symbol: str, interval: str, limit: int = 180) -> Dict[str, Any]:
    mapped_interval = map_interval("binance", interval)
    params = {
        "symbol": symbol,
        "interval": mapped_interval,
        "limit": str(limit),
    }
    url = f"{BINANCE_KLINES_URL}?{parse.urlencode(params)}"
    raw = _http_get(url)
    payload = json.loads(raw)

    if not isinstance(payload, list):
        return {"error": "Invalid Binance response format", "symbol": symbol}

    rows: List[Dict[str, Any]] = []
    for item in payload:
        try:
            rows.append(
                {
                    "time": int(item[0]),
                    "open": item[1],
                    "high": item[2],
                    "low": item[3],
                    "close": item[4],
                    "volume": item[5],
                }
            )
        except (IndexError, ValueError):
            continue

    return {"source": "binance", "data": normalize_ohlcv(rows)}
