from typing import Literal

AssetType = Literal["crypto", "forex", "metal", "us_stock", "indian_stock"]


def detect_asset_type(symbol: str) -> AssetType:
    if not isinstance(symbol, str) or not symbol.strip():
        raise ValueError("Symbol must be a non-empty string")

    normalized = symbol.strip().upper()

    if "/" in normalized:
        return "forex"
    if normalized.endswith(".NS") or normalized.endswith(".BO"):
        return "indian_stock"
    if normalized.endswith("USDT"):
        return "crypto"
    if normalized in {"XAUUSD", "XAGUSD"}:
        return "metal"

    return "us_stock"
