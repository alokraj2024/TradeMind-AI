import joblib
from pathlib import Path
from typing import Any, Dict

import pandas as pd

MODEL_PATH = Path(__file__).resolve().parent.parent / "ml" / "model.pkl"


def load_model(model_path: Path = MODEL_PATH):
    payload = joblib.load(model_path)
    if not isinstance(payload, dict) or "model" not in payload or "features" not in payload:
        raise ValueError("Saved model payload is invalid")
    return payload["model"], payload["features"]


def make_prediction(model, feature_columns, latest_row: pd.DataFrame) -> Dict[str, Any]:
    try:
        if model is None:
            raise ValueError("Prediction model is not loaded")

        if not isinstance(latest_row, pd.DataFrame):
            raise ValueError("latest_row must be a pandas DataFrame")

        X = latest_row[feature_columns].copy()
        prediction = model.predict(X)[0]
        probabilities = model.predict_proba(X)[0]
        confidence = float(max(probabilities)) * 100.0

        if confidence < 60.0:
            signal = "HOLD"
        elif prediction == 1:
            signal = "BUY"
        elif prediction == 0:
            signal = "SELL"
        else:
            signal = "HOLD"

        mapping = {0: "SELL", 1: "BUY", 2: "HOLD"}
        return {
            "signal": signal,
            "prediction": int(prediction),
            "confidence": round(confidence, 2),
            "features_used": feature_columns,
            "raw_prediction": mapping.get(prediction, "HOLD"),
        }
    except Exception as exc:
        return {
            "signal": "HOLD",
            "confidence": 0.0,
            "features_used": feature_columns if isinstance(feature_columns, list) else [],
            "error": str(exc),
        }
