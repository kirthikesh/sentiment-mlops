# sentiment-mlops

MLOps pipeline that deploys and monitors a sentiment-analysis model in
production — Docker → Kubernetes/Helm → Jenkins CI (with a model-accuracy
gate) → ArgoCD GitOps → canary rollout via Argo Rollouts → Prometheus/Grafana
+ EFK observability, on Terraform-provisioned cloud infra.

Architecture diagram and full build plan: see `docs/`.

## Local dev

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
```

Then visit http://localhost:8000/docs for the interactive API, or:

```bash
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{"text": "I love this!"}'
```

## Tests

```bash
pytest -v
```

## Status

- [x] Phase 1 — model-serving app (FastAPI + DistilBERT-SST2)
- [ ] Phase 2 — Terraform cloud infra
- [ ] Phase 3 — Jenkins CI pipeline
- [ ] Phase 4 — ArgoCD GitOps + canary rollout
- [ ] Phase 5 — Observability (Prometheus/Grafana + EFK)
- [ ] Phase 6 — Secrets management
- [ ] Phase 7 — Polish & ship
