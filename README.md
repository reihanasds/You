# Kim Holiday marketing-agent vertical slice

This repository contains a local, draft-only marketing pipeline for Kim Holiday. It follows a specialist-agent shape—**orchestrator → content strategist → Instagram curator → brand guardian → anti-slop reviewer → validated JSON draft**—without requiring an API key.

```bash
PYTHONPATH=src python -m kim_holiday "questions to ask before planning"
PYTHONPATH=src python -m unittest discover -s tests
```

The deterministic provider is the testable default. A future LLM adapter can implement `ContentProvider` in `src/kim_holiday/provider.py`, while the evidence ledger in `knowledge/kim-holiday-business-facts.json` remains the source of truth. Unknown price, availability, capacity, and testimonials are never filled in. Every output is `status: "draft"` with `approval_required: true`; nothing is published.

See [workflows/content-draft.md](workflows/content-draft.md) for the workflow and [CI.md](CI.md) for repository validation.
