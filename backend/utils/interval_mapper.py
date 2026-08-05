from typing import Literal

ProviderInterval = Literal["1m", "5m", "15m", "1h", "4h", "1d", "1min", "5min", "15min", "1day"]

BINANCE_INTERVAL_MAP = {
    "1m": "1m",
    "5m": "5m",
    "15m": "15m",
    "1h": "1h",
    "4h": "4h",
    "1d": "1d",
}

TWELVE_DATA_INTERVAL_MAP = {
    "1m": "1min",
    "5m": "5min",
    "15m": "15min",
    "1h": "1h",
    "1d": "1day",
}

YFINANCE_INTERVAL_MAP = {
    "1m": "1m",
    "5m": "5m",
    "15m": "15m",
    "1h": "1h",
    "1d": "1d",
}

DEFAULT_INTERVAL = "1d"


def map_interval(provider: str, interval: str) -> str:
    if not isinstance(interval, str) or not interval.strip():
        raise ValueError("Interval must be a non-empty string")

    normalized = interval.strip().lower()

    if provider == "binance":
        if normalized not in BINANCE_INTERVAL_MAP:
            raise ValueError(f"Unsupported interval for Binance: {interval}")
        return BINANCE_INTERVAL_MAP[normalized]

    if provider == "twelvedata":
        if normalized not in TWELVE_DATA_INTERVAL_MAP:
            raise ValueError(f"Unsupported interval for Twelve Data: {interval}")
        return TWELVE_DATA_INTERVAL_MAP[normalized]

    if provider == "yfinance":
        if normalized not in YFINANCE_INTERVAL_MAP:
            raise ValueError(f"Unsupported interval for yfinance: {interval}")
        return YFINANCE_INTERVAL_MAP[normalized]

    raise ValueError(f"Unknown provider for interval mapping: {provider}")
