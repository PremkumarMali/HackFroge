# ml_research

Notebooks and experiments for the **optional** ML detectors (Isolation Forest,
DeepLog-style LSTM).

Rules:

- Nothing here is on the critical path. Start only after the core statistical
  detector in `backend/app/core/` meets the minimum requirements end to end.
- Trained models go to `backend/artifacts/`. Large binaries are git-ignored.
- Do not commit raw production logs or anything containing secrets or PII.
- ML dependencies (scikit-learn, torch, etc.) belong in a separate
  `ml_research/requirements.txt`, not in `backend/requirements.txt`, until the
  backend actually loads a model.
