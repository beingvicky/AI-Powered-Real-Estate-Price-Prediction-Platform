import os
import json
import pickle
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

try:
    from xgboost import XGBRegressor
except Exception:  # pragma: no cover
    XGBRegressor = None

BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "app"


MARKET_PRICE_PER_SQFT = {
    "Mysuru": {
        "Apartment": 8400,
        "Villa": 9800,
        "Independent House": 9300,
        "Plot": 5100,
    },
    "Bengaluru": {
        "Apartment": 9800,
        "Villa": 12700,
        "Independent House": 11800,
        "Plot": 6100,
    },
    "Hyderabad": {
        "Apartment": 8100,
        "Villa": 10500,
        "Independent House": 9800,
        "Plot": 5200,
    },
    "Chennai": {
        "Apartment": 8300,
        "Villa": 10600,
        "Independent House": 9900,
        "Plot": 5400,
    },
    "Pune": {
        "Apartment": 8800,
        "Villa": 11200,
        "Independent House": 10000,
        "Plot": 5600,
    },
    "Mumbai": {
        "Apartment": 13600,
        "Villa": 17000,
        "Independent House": 15000,
        "Plot": 7200,
    },
    "Delhi": {
        "Apartment": 11000,
        "Villa": 14000,
        "Independent House": 13000,
        "Plot": 6500,
    },
}


def generate_dataset(n_samples=2500):
    rng = np.random.default_rng(42)
    locations = ["Bengaluru", "Mysuru", "Hyderabad", "Chennai", "Pune", "Mumbai", "Delhi"]
    property_types = ["Apartment", "Villa", "Independent House", "Plot"]

    rows = []
    for _ in range(n_samples):
        location = rng.choice(locations)
        property_type = rng.choice(property_types)
        area = float(rng.uniform(500, 5000))
        bedrooms = int(rng.integers(1, 6))
        bathrooms = int(rng.integers(1, 5))
        floor = int(rng.integers(0, 25))
        parking = int(rng.integers(0, 3))
        age = int(rng.integers(0, 35))

        market_rate = MARKET_PRICE_PER_SQFT[location][property_type]
        locality_adjustment = rng.uniform(0.88, 1.18)
        age_penalty = max(0, age - 5) * 0.012
        floor_bonus = floor * 0.015
        bedroom_bonus = bedrooms * 0.08
        bathroom_bonus = bathrooms * 0.06
        parking_bonus = parking * 0.04

        total_price = area * market_rate * locality_adjustment
        total_price *= (1 + floor_bonus + bedroom_bonus + bathroom_bonus + parking_bonus - age_penalty)

        if property_type == "Plot":
            total_price *= 0.65

        price_lakhs = total_price / 100000

        rows.append({
            "location": location,
            "area": round(area, 2),
            "bedrooms": bedrooms,
            "bathrooms": bathrooms,
            "property_type": property_type,
            "floor": floor,
            "parking": parking,
            "age": age,
            "price_lakhs": round(price_lakhs, 2),
        })

    return pd.DataFrame(rows)


def compute_metrics(y_true, y_pred):
    return {
        "r2": round(float(r2_score(y_true, y_pred)), 4),
        "mae": round(float(mean_absolute_error(y_true, y_pred)), 4),
        "rmse": round(float(np.sqrt(mean_squared_error(y_true, y_pred))), 4),
    }


def build_model_pipeline(model):
    categorical_features = ["location", "property_type"]
    numeric_features = ["area", "bedrooms", "bathrooms", "floor", "parking", "age"]

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", "passthrough", numeric_features),
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
        ]
    )
    return Pipeline(steps=[("preprocessor", preprocessor), ("model", model)])


def train_and_save_models():
    df = generate_dataset()
    X = df.drop(columns=["price_lakhs"])
    y = df["price_lakhs"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    models = {
        "Linear Regression": LinearRegression(),
        "Random Forest": RandomForestRegressor(n_estimators=300, random_state=42),
        "Gradient Boosting": GradientBoostingRegressor(random_state=42),
    }

    if XGBRegressor is not None:
        models["XGBoost"] = XGBRegressor(objective="reg:squarederror", n_estimators=300, random_state=42, max_depth=6, learning_rate=0.08)

    metrics = {}
    for name, model in models.items():
        pipeline = build_model_pipeline(model)
        pipeline.fit(X_train, y_train)
        prediction = pipeline.predict(X_test)
        metrics[name] = compute_metrics(y_test, prediction)
        joblib_path = MODEL_DIR / f"{name.lower().replace(' ', '_')}.joblib"
        joblib.dump(pipeline, joblib_path)

    best_model_name = max(metrics, key=lambda key: metrics[key]["r2"])
    model_metadata = {
        "best_model": best_model_name,
        "models": metrics,
    }
    with open(MODEL_DIR / "model_metadata.json", "w", encoding="utf-8") as f:
        json.dump(model_metadata, f, indent=2)

    return model_metadata


if __name__ == "__main__":
    os.makedirs(MODEL_DIR, exist_ok=True)
    import joblib
    train_and_save_models()
    print("Models trained and saved successfully.")
