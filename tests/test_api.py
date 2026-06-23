from fastapi.testclient import TestClient

from app.api.main import app


client = TestClient(app)


VALID_CUSTOMER = {
    "tenure_months": 7,
    "monthly_charge": 58.23,
    "total_charges": 326.5,
    "support_tickets": 2,
    "late_payments": 1,
    "avg_monthly_usage_gb": 81.83,
    "contract_type": "mensual",
    "payment_method": "transferencia",
    "internet_service": "cable",
    "has_streaming": 0,
    "has_security_pack": 1,
    "num_products": 3,
    "region": "centro",
    "customer_age": 53,
    "is_promo": 1,
}


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["application"] == "AndesLink Churn API"
    assert data["version"] == "1.0.0"
    assert data["documentation"] == "/docs"
    assert data["health"] == "/health"
    assert data["prediction"] == "/predict"


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"
    assert data["model_loaded"] is True


def test_predict_endpoint():
    response = client.post(
        "/predict",
        json=VALID_CUSTOMER,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["prediction"] in [0, 1]
    assert 0 <= data["churn_probability"] <= 1
    assert data["risk_level"] in ["bajo", "medio", "alto"]
    assert data["model_name"] == "logistic_regression"


def test_predict_rejects_invalid_age():
    invalid_customer = VALID_CUSTOMER.copy()
    invalid_customer["customer_age"] = -5

    response = client.post(
        "/predict",
        json=invalid_customer,
    )

    assert response.status_code == 422