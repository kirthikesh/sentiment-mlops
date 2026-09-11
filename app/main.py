"""
sentiment-mlops — model-serving API.

Exposes:
  GET  /health   liveness/readiness probe for Kubernetes
  POST /predict  run sentiment analysis on a piece of text
  GET  /metrics  Prometheus scrape endpoint (request count, latency,
                  prediction confidence — the "model-aware" metrics
                  that make this more than a plain infra dashboard)
"""
import time

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response

from app.model import predict, MODEL_NAME

app = FastAPI(title="sentiment-mlops", version="0.1.0")

# --- Prometheus metrics -----------------------------------------------
REQUEST_COUNT = Counter(
    "predict_requests_total", "Total number of /predict requests", ["label"]
)
REQUEST_LATENCY = Histogram(
    "predict_latency_seconds", "Time spent running inference"
)
PREDICTION_CONFIDENCE = Histogram(
    "predict_confidence_score",
    "Model confidence score per prediction (used to watch for drift)",
    buckets=(0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.99, 1.0),
)


class PredictRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=2000, examples=["I love this product!"])


class PredictResponse(BaseModel):
    label: str
    score: float
    model: str = MODEL_NAME


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictResponse)
def run_predict(payload: PredictRequest):
    start = time.perf_counter()
    try:
        result = predict(payload.text)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    elapsed = time.perf_counter() - start

    REQUEST_LATENCY.observe(elapsed)
    REQUEST_COUNT.labels(label=result["label"]).inc()
    PREDICTION_CONFIDENCE.observe(result["score"])

    return PredictResponse(label=result["label"], score=result["score"])


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
