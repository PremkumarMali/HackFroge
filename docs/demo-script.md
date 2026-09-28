# Demo Script

**Owner:** Person 4 (with Person 3 for scripts)
**Target length:** ~5 minutes
**Status:** draft. Steps marked *(planned)* depend on work not built yet.

## Before the demo

- [ ] `backend/.env` created from `.env.example`
- [ ] Backend starts cleanly and `GET /health` returns 200
- [ ] Frontend open in the browser, both sockets show "connected" *(planned)*
- [ ] Baseline warmed up: generator has run for at least
      `BASELINE_WINDOW_COUNT × WINDOW_SIZE_SECONDS`. For the demo, shrink
      `WINDOW_SIZE_SECONDS` (e.g. 5) and `BASELINE_WINDOW_COUNT` (e.g. 12).
- [ ] (Optional) LocalStack running: `docker compose --profile aws up`
- [ ] Terminal windows pre-arranged: backend logs, generator, injector

## Flow

| Time | Say                                                                 | Do |
|------|---------------------------------------------------------------------|----|
| 0:00 | The problem: logs grow faster than anyone can read them, and incidents hide in the noise. | Show `data/app.log` growing (`tail -f`). |
| 0:45 | Architecture in one line: file → parser → window → baseline → detector → severity → live feed + AWS. | Show the diagram in `README.md`. |
| 1:30 | Normal traffic: metrics flat, severity `NORMAL`, feed empty. | Start `python scripts/generate_logs.py` *(planned)*. Point at the chart. |
| 2:15 | Inject an incident: database timeouts in payment-service. | `python scripts/inject_anomaly.py --kind error-burst` *(planned)* |
| 2:30 | Alert appears within one window, colour-coded, with the explanation and sample lines. | Expand the alert in the feed *(planned)*. |
| 3:15 | The same alert went to AWS: metric in CloudWatch, `HIGH` notification on SNS. | Show LocalStack output / `awslocal` query *(planned)*. |
| 4:00 | Why statistical first: no training data, explainable, real time. ML is an optional add-on. | Show `docs/model-card.md`. |
| 4:30 | Wrap-up and questions. | |

## Backup plan

- If the live generator fails, replay the committed `data/app.log`, which
  ends with an error burst.
- If AWS/LocalStack fails, skip that step. CloudWatch and SNS are optional
  publishers and the live feed does not depend on them.
- Keep a screen recording of a successful run.
