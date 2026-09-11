"""
This is the file the Jenkins "Model Eval Gate" stage will run.
It's a tiny fixed evaluation set with known-correct labels — if the
model's accuracy on this set drops below the threshold, the build
should fail rather than deploy a regressed model.
"""
from app.model import predict

EVAL_SET = [
    ("I love this, it's amazing!", "POSITIVE"),
    ("Best purchase I've made all year.", "POSITIVE"),
    ("This is awful and completely broken.", "NEGATIVE"),
    ("Waste of money, very disappointed.", "NEGATIVE"),
    ("Absolutely fantastic service.", "POSITIVE"),
    ("Terrible experience, would not recommend.", "NEGATIVE"),
]

ACCURACY_THRESHOLD = 0.9
LATENCY_THRESHOLD_SECONDS = 2.0


def test_model_meets_accuracy_threshold():
    correct = 0
    for text, expected_label in EVAL_SET:
        result = predict(text)
        if result["label"] == expected_label:
            correct += 1
    accuracy = correct / len(EVAL_SET)
    assert accuracy >= ACCURACY_THRESHOLD, f"model accuracy {accuracy:.2f} below threshold {ACCURACY_THRESHOLD}"


def test_model_latency_is_reasonable():
    import time
    start = time.perf_counter()
    predict("Quick latency check.")
    elapsed = time.perf_counter() - start
    assert elapsed < LATENCY_THRESHOLD_SECONDS, f"inference took {elapsed:.2f}s, over {LATENCY_THRESHOLD_SECONDS}s threshold"
