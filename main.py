from fastapi import FastAPI, HTTPException

from features import create_model_features
from model import best_threshold, pipeline
from schema import PredictionResponse, ShopperInput

app = FastAPI(
    title="Online Shoppers Purchase Prediction API",
    description="Deploy a Session 1 scikit-learn model with FastAPI.",
    version="2.0.0",
)

@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_loaded": True,
        "threshold": best_threshold,
    }


@app.post("/predict", response_model=PredictionResponse)
def predict(input_data: ShopperInput):
    try:
        # Step 1: Convert the API input into the same columns used in training.
        model_features = create_model_features(input_data)

        # Step 2: Ask the model for the probability of Revenue=True.
        probability = float(pipeline.predict_proba(model_features)[:, 1][0])

        # Step 3: Convert probability into a class using Session 1's threshold.
        will_purchase = probability >= best_threshold

        return PredictionResponse(
            will_purchase=will_purchase,
            prediction=1 if will_purchase else 0,
            prediction_label="Will Purchase" if will_purchase else "Will Not Purchase",
            probability=round(probability, 4),
            threshold=best_threshold,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

@app.get("/")
def root():
    return {
        "message": "Online Shoppers Purchase Prediction API",
        "docs": "/docs",
        "health": "/health",
        "predict": "/predict"
    }