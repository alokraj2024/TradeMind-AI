from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
import pandas as pd


BASE_FEATURES = ["open", "high", "low", "close", "rsi", "sma_20"]
OPTIONAL_FEATURES = ["volume_change"]


def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [col.lower() for col in df.columns]
    return df


def _select_required_columns(df: pd.DataFrame) -> pd.DataFrame:
    required_columns = ["time", "open", "high", "low", "close", "volume"]
    selected = [col for col in required_columns if col in df.columns]
    return df[selected].copy()


def _convert_numeric(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    for column in columns:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")
    return df


def _assert_numeric(df: pd.DataFrame, columns: List[str]) -> None:
    bad_columns = [col for col in columns if col in df.columns and not pd.api.types.is_numeric_dtype(df[col])]
    if bad_columns:
        raise ValueError(f"Expected numeric columns but found non-numeric types: {bad_columns}")


def compute_features(df: pd.DataFrame) -> pd.DataFrame:
    df = _normalize_columns(df)
    df = _select_required_columns(df)

    missing = {"time", "open", "high", "low", "close", "volume"} - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    df = _convert_numeric(df, ["open", "high", "low", "close", "volume"])
    print("compute_features - dtypes:\n", df.dtypes)
    print("compute_features - first rows:\n", df.head().to_dict(orient="records"))

    df = df.dropna(subset=["open", "high", "low", "close", "volume"])
    if df.empty:
        raise ValueError("No valid numeric data available after conversion")

    _assert_numeric(df, ["open", "high", "low", "close", "volume"])

    df["sma_20"] = df["close"].rolling(window=20, min_periods=1).mean()
    df["ema_10"] = df["close"].ewm(span=10, adjust=False).mean()
    df["ema_20"] = df["close"].ewm(span=20, adjust=False).mean()

    ema_12 = df["close"].ewm(span=12, adjust=False).mean()
    ema_26 = df["close"].ewm(span=26, adjust=False).mean()
    df["macd"] = ema_12 - ema_26
    df["macd_signal"] = df["macd"].ewm(span=9, adjust=False).mean()
    df["macd_hist"] = df["macd"] - df["macd_signal"]

    rolling_std = df["close"].rolling(window=20, min_periods=1).std()
    df["bb_upper"] = df["sma_20"] + 2 * rolling_std
    df["bb_lower"] = df["sma_20"] - 2 * rolling_std
    df["bb_width"] = df["bb_upper"] - df["bb_lower"]

    df["return_1"] = df["close"].pct_change(periods=1)
    df["return_5"] = df["close"].pct_change(periods=5)
    df["volatility"] = df["return_1"].rolling(window=10, min_periods=1).std()
    df["volume_change"] = df["volume"].pct_change()

    df = df.reset_index(drop=True)
    print("compute_features - output dtypes:\n", df.dtypes)
    print("compute_features - output head:\n", df.head().to_dict(orient="records"))
    return df


def get_feature_columns(df: pd.DataFrame) -> List[str]:
    columns = BASE_FEATURES + ["ema_10", "ema_20", "macd", "macd_signal", "macd_hist", "bb_upper", "bb_lower", "bb_width", "return_1", "return_5", "volatility"]
    if "volume_change" in df.columns:
        columns.append("volume_change")
    return [col for col in columns if col in df.columns]


def build_target_labels(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["close_next"] = df["close"].shift(-1)
    df["target"] = (df["close_next"] > df["close"]).astype(int)
    df = df.dropna(subset=["close_next", "close", "target"])
    df["target"] = df["target"].astype(int)
    print("build_target_labels - class distribution:", df["target"].value_counts().to_dict())
    return df


def build_training_data(df: pd.DataFrame) -> pd.DataFrame:
    df = compute_features(df)
    df = build_target_labels(df)

    feature_columns = get_feature_columns(df)
    required_columns = set(feature_columns + ["target"])
    df = df.dropna(subset=required_columns)
    return df


def load_training_data(csv_path: Path) -> pd.DataFrame:
    if not csv_path.exists():
        raise FileNotFoundError(f"Training CSV not found: {csv_path}")
    df = pd.read_csv(csv_path, parse_dates=["time"])
    return df
