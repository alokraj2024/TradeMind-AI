import logging
from datetime import datetime, timezone
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


def to_iso(value: Any) -> str:
    if isinstance(value, (int, float)):
        return datetime.utcfromtimestamp(value / 1000).replace(tzinfo=timezone.utc).isoformat().replace("+00:00", "Z")
    if isinstance(value, str):
        try:
            dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
        except ValueError:
            raise ValueError(f"Unable to parse datetime string: {value}")
    if isinstance(value, datetime):
        dt = value
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
    raise ValueError(f"Unsupported datetime type: {type(value)}")


def to_float(value: Any) -> float:
    if value is None:
        raise ValueError("Numeric value cannot be None")
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        return float(value.replace(",", ""))
    raise ValueError(f"Unsupported numeric type: {type(value)}")


def _get_case_insensitive(row: Dict[str, Any], *keys: str, default: Any = None) -> Any:
    for key in keys:
        if key in row:
            return row[key]
    return default


def normalize_ohlcv(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    normalized = []

    for row in rows:
        time_value = _get_case_insensitive(row, "time", "datetime", "date")
        if time_value is None:
            raise ValueError(f"Missing required time field in row: {row}")

        open_value = _get_case_insensitive(row, "open", "Open")
        high_value = _get_case_insensitive(row, "high", "High")
        low_value = _get_case_insensitive(row, "low", "Low")
        close_value = _get_case_insensitive(row, "close", "Close")
        volume_value = _get_case_insensitive(row, "volume", "Volume", default=0)

        if open_value is None:
            raise ValueError(f"Missing required OHLC field 'open' in row: {row}")
        if high_value is None:
            raise ValueError(f"Missing required OHLC field 'high' in row: {row}")
        if low_value is None:
            raise ValueError(f"Missing required OHLC field 'low' in row: {row}")
        if close_value is None:
            raise ValueError(f"Missing required OHLC field 'close' in row: {row}")

        normalized.append(
            {
                "time": to_iso(time_value),
                "open": to_float(open_value),
                "high": to_float(high_value),
                "low": to_float(low_value),
                "close": to_float(close_value),
                "volume": to_float(volume_value if volume_value is not None else 0),
            }
        )

    normalized.sort(key=lambda item: item["time"])

    if normalized:
        logger.debug("Sample normalized row: %s", normalized[0])

    return normalized
