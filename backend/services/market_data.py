from typing import Any, Dict

from .providers import binance, twelvedata, yfinance
from utils.symbol_parser import detect_asset_type


def get_market_data(symbol: str, interval: str = "1d") -> Dict[str, Any]:
    if not isinstance(symbol, str) or not symbol.strip():
        return {"error": "Symbol must be a non-empty string", "symbol": symbol}

    if not isinstance(interval, str) or not interval.strip():
        return {"error": "Interval must be a non-empty string", "symbol": symbol}

    asset_type = detect_asset_type(symbol)
    symbol = symbol.strip().upper()

    try:
        if asset_type == "crypto":
            result = binance.fetch(symbol, interval)
        elif asset_type in {"forex", "metal"}:
            result = twelvedata.fetch(symbol, interval)
        elif asset_type in {"us_stock", "indian_stock"}:
            result = yfinance.fetch(symbol, interval)
        else:
            result = {"error": "Unsupported asset type", "symbol": symbol}
    except ValueError as exc:
        return {"error": str(exc), "symbol": symbol}
    except Exception as exc:
        return {"error": "Data provider failure: %s" % str(exc), "symbol": symbol}

    if not isinstance(result, dict):
        return {"error": "Provider returned unexpected response", "symbol": symbol}

    if "error" in result:
        return result

    if "source" not in result or "data" not in result or not isinstance(result["data"], list):
        return {"error": "Provider returned invalid data structure", "symbol": symbol}

    return result
