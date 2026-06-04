from pathlib import Path

import joblib

BASE_DIR = Path(__file__).resolve().parent
ARTIFACTS_DIR = BASE_DIR / "artifacts"
MODEL_PATH = ARTIFACTS_DIR / "online_shoppers_model.pkl"
THRESHOLD_PATH = ARTIFACTS_DIR / "threshold.pkl"
MODEL_COLUMNS_PATH = ARTIFACTS_DIR / "model_columns.pkl"


if not MODEL_PATH.exists():
    raise RuntimeError("artifacts/online_shoppers_model.pkl was not found.")

if not MODEL_COLUMNS_PATH.exists():
    raise RuntimeError("artifacts/model_columns.pkl was not found.")

pipeline = joblib.load(MODEL_PATH)
model_columns = list(joblib.load(MODEL_COLUMNS_PATH))

if THRESHOLD_PATH.exists():
    best_threshold = float(joblib.load(THRESHOLD_PATH))
else:
    best_threshold = 0.5