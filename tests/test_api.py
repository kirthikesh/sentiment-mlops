from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_predict_positive():
    resp = client.post("/predict", json={"text": "I absolutely love this!"})
    assert resp.status_code == 200
    body = resp.json()
    assert body["label"] == "POSITIVE"
    assert 0.0 <= body["score"] <= 1.0


def test_predict_negative():
    resp = client.post("/predict", json={"text": "This is terrible and I hate it."})
    assert resp.status_code == 200
    assert resp.json()["label"] == "NEGATIVE"


def test_predict_rejects_empty_text():
    resp = client.post("/predict", json={"text": ""})
    assert resp.status_code == 422  # pydantic min_length validation


def test_metrics_endpoint_exposes_prometheus_format():
    resp = client.get("/metrics")
    assert resp.status_code == 200
    assert b"predict_requests_total" in resp.content
