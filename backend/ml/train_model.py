import pandas as pd
import argparse
from pathlib import Path

import joblib
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

from ml.features import build_training_data, get_feature_columns, load_training_data


DATA_DIR = Path(__file__).resolve().parent.parent / "data"
MODEL_DIR = Path(__file__).resolve().parent
DEFAULT_MODEL_PATH = MODEL_DIR / "model.pkl"


def train_model(df):
    df = build_training_data(df)

    # 🔥 FIX 1: Handle bad values BEFORE selecting features
    df = df.replace([float("inf"), float("-inf")], None)
    df = df.dropna()

    feature_columns = get_feature_columns(df)

    # 🔥 FIX 2: Ensure only numeric columns are used
    X = df[feature_columns].apply(pd.to_numeric, errors="coerce")
    y = df["target"].astype(int)

    # 🔥 FIX 3: Final cleanup (in case coercion created NaNs)
    X = X.replace([float("inf"), float("-inf")], None)
    valid_idx = X.dropna().index
    X = X.loc[valid_idx]
    y = y.loc[valid_idx]

    print("train_model - cleaned data shape:", X.shape)

    class_counts = y.value_counts().to_dict()
    print("train_model - class distribution:", class_counts)

    if len(class_counts) < 2:
        raise ValueError("Training requires at least two classes in the target labels.")

    stratify = y if all(count >= 2 for count in class_counts.values()) else None
    if stratify is None:
        print(
            "Warning: stratified split disabled because some classes have fewer than 2 samples."
        )

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=stratify,
    )

    model = XGBClassifier(
        n_estimators=200,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        use_label_encoder=False,
        eval_metric="mlogloss",
        n_jobs=-1,
        random_state=42,
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    print(f"Model trained. Test accuracy: {accuracy:.4f}")
    print("Classification report:\n", classification_report(y_test, predictions, digits=4))

    return model, feature_columns


def save_model(model, feature_columns, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(
        {
            "model": model,
            "features": feature_columns,
        },
        output_path,
    )
    print(f"Saved model and metadata to: {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Train an XGBoost model for TradeMind AI.")
    parser.add_argument(
        "--csv",
        type=Path,
        default=DATA_DIR / "training_data.csv",
        help="Path to training CSV file.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_MODEL_PATH,
        help="Output path for the trained model.",
    )
    args = parser.parse_args()

    df = load_training_data(args.csv)
    model, feature_columns = train_model(df)
    save_model(model, feature_columns, args.output)


if __name__ == "__main__":
    main()
