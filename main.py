from fastapi import FastAPI, HTTPException

from features import create_model_features
from model import best_threshold, pipeline
from schema import PredictionResponse, ShopperInput

app = FastAPI(
    title="Online Shoppers Purchase Prediction API",
    description="Deploy a Session 1 scikit-learn model with FastAPI.",
    version="2.0.0",
)

# TODO:
# 2. Predict probability
# 3. Compare with threshold
# 4. Return response

@app.get("/")
def root():
    return {
        "message": "Online Shoppers Purchase Prediction API",
        "docs": "/docs",
        "health": "/health",
        "predict": "/predict"
    }