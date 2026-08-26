from fastapi.testclient import TestClient

from app import main


class DummyModel:
    def predict(self, dataframe):
        assert list(dataframe.columns) == [
            "location",
            "area",
            "bedrooms",
            "bathrooms",
            "property_type",
            "floor",
            "parking",
            "age",
        ]
        return [125.5]


def test_health_check_returns_ok():
    client = TestClient(main.app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_predict_returns_estimate_and_model_metadata(monkeypatch):
    monkeypatch.setattr(
        main,
        "load_metadata",
        lambda: {
            "best_model": "Gradient Boosting",
            "models": {
                "Gradient Boosting": {
                    "r2": 0.9617,
                    "mae": 34.2649,
                    "rmse": 48.4187,
                }
            },
        },
    )
    monkeypatch.setattr(main, "load_model", lambda model_name: DummyModel())
    client = TestClient(main.app)

    response = client.post(
        "/predict",
        json={
            "location": "Bengaluru",
            "area": 1200,
            "bedrooms": 2,
            "bathrooms": 2,
            "property_type": "Apartment",
            "floor": 5,
            "parking": 1,
            "age": 8,
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["estimated_price_lakhs"] == 125.5
    assert body["price_range_lakhs"] == {
        "min_lakhs": 112.95,
        "max_lakhs": 138.05,
    }
    assert body["model_used"] == "Gradient Boosting"
    assert body["metrics"]["r2"] == 0.9617
