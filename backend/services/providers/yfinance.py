import pandas as pd
import yfinance as yf
from typing import Any, Dict, List

from utils.interval_mapper import map_interval
from utils.normalizer import normalize_ohlcv


def _period_for_interval(interval: str) -> str:
    interval = interval.strip().lower()
    if interval == "1m":
        return "7d"
    if interval in {"5m", "15m"}:
        return "60d"
    if interval == "1h":
        return "180d"
    return "1y"


def fetch(symbol: str, interval: str) -> Dict[str, Any]:
    mapped_interval = map_interval("yfinance", interval)
    period = _period_for_interval(interval)
    ticker = yf.Ticker(symbol)
    df = ticker.history(period=period, interval=mapped_interval)

    if df.empty:
        return {"error": "No yfinance data returned", "symbol": symbol}

    df = df.copy()
    if isinstance(df.index, pd.DatetimeIndex):
        if df.index.tz is None:
            df.index = df.index.tz_localize("UTC")
        else:
            df.index = df.index.tz_convert("UTC")

    rows: List[Dict[str, Any]] = []
    for index, row in df.iterrows():
        rows.append(
            {
                "time": index.isoformat().replace("+00:00", "Z"),
                "open": row.get("Open"),
                "high": row.get("High"),
                "low": row.get("Low"),
                "close": row.get("Close"),
                "volume": row.get("Volume", 0),
            }
        )

    return {"source": "yfinance", "data": normalize_ohlcv(rows)}
