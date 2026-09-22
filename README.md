# Kim Holiday marketing-agent vertical slice

This repository contains a local, draft-only marketing pipeline for Kim Holiday. It follows a specialist-agent shape—**orchestrator → content strategist → Instagram curator → brand guardian → anti-slop reviewer → validated JSON draft**—without requiring an API key.

```bash
PYTHONPATH=src python -m kim_holiday "questions to ask before planning"
PYTHONPATH=src python -m unittest discover -s tests
PYTHONPATH=src python -m kim_holiday.api
```

The deterministic provider is the testable default. A future LLM adapter can implement `ContentProvider` in `src/kim_holiday/provider.py`, while the evidence ledger in `knowledge/kim-holiday-business-facts.json` remains the source of truth. Unknown price, availability, capacity, and testimonials are never filled in. Every output is `status: "draft"` with `approval_required: true`; nothing is published.

## Draft API

The local API listens on port 8080 and exposes `GET /health` and `POST /draft`. The draft endpoint accepts `{"topic":"..."}` and returns validated JSON.

```bash
PYTHONPATH=src python -m kim_holiday.api
curl http://127.0.0.1:8080/health
curl --header 'Content-Type: application/json' \
  --data '{"topic":"questions to ask before planning"}' \
  http://127.0.0.1:8080/draft
docker build -t kim-holiday-draft-api .
docker run --rm -p 8080:8080 kim-holiday-draft-api
```

See [workflows/content-draft.md](workflows/content-draft.md) for the workflow and [CI.md](CI.md) for repository validation.

## Three-day draft trial

GitHub Actions can run the deterministic agent once per day for three UTC calendar days. It only uploads a JSON draft artifact; it never publishes or deploys.

1. Open **Actions → Kim Holiday 3-day draft trial → Run workflow**, optionally set `start_date` (`YYYY-MM-DD`), and run it once.
2. Monitor the workflow runs and each generated artifact in the workflow’s run summary. Scheduled runs occur at 00:15 UTC.
3. Download artifacts named `kim-holiday-draft-day-<day>-<run-id>` from each successful run.
4. Stop early by disabling the workflow in the Actions UI, or remove the schedule after the trial. Runs outside the three-day window exit with a notice.

Each artifact includes `run_metadata`, evidence labels, `approval_required: true`, and `publication: "disabled"`. Human approval is still required and no auto-publish path exists.
