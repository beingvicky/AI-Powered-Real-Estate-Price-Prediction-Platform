import json
from pathlib import Path

import pandas as pd
import joblib
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .schemas import PredictionRequest, PredictionResponse

app = FastAPI(title="Real Estate AI Price Predictor")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR


def load_model(model_name: str):
    path = MODEL_DIR / f"{model_name.lower().replace(' ', '_')}.joblib"
    return joblib.load(path)


def load_metadata():
    with open(MODEL_DIR / "model_metadata.json", "r", encoding="utf-8") as f:
        return json.load(f)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/models")
def get_models():
    return load_metadata()


@app.post("/predict", response_model=PredictionResponse)
def predict(payload: PredictionRequest):
    metadata = load_metadata()
    best_model_name = metadata["best_model"]
    model = load_model(best_model_name)

    df = pd.DataFrame([
        {
            "location": payload.location,
            "area": payload.area,
            "bedrooms": payload.bedrooms,
            "bathrooms": payload.bathrooms,
            "property_type": payload.property_type,
            "floor": payload.floor,
            "parking": payload.parking,
            "age": payload.age,
        }
    ])

    prediction = float(model.predict(df)[0])
    lower = max(prediction * 0.9, 0.1)
    upper = prediction * 1.1

    return PredictionResponse(
        estimated_price_lakhs=round(prediction, 2),
        price_range_lakhs={
            "min_lakhs": round(lower, 2),
            "max_lakhs": round(upper, 2),
        },
        model_used=best_model_name,
        metrics=metadata["models"][best_model_name],
        input_summary={
            "location": payload.location,
            "area": payload.area,
            "bedrooms": payload.bedrooms,
            "bathrooms": payload.bathrooms,
            "property_type": payload.property_type,
            "floor": payload.floor,
            "parking": payload.parking,
            "age": payload.age,
        },
    )
