# Content draft workflow

1. The orchestrator receives a specific topic and loads the evidence ledger.
2. The content strategist selects one grounded angle.
3. The Instagram curator writes a concise caption and CTA.
4. The brand guardian checks claims against the evidence labels.
5. The anti-slop reviewer rejects generic or fabricated copy.
6. The pipeline emits `schemas/content-draft.schema.json`-shaped JSON with `status: "draft"` and `approval_required: true`.

Run locally without an API key:

```bash
python -m kim_holiday "questions to ask before planning"
python -m kim_holiday "questions to ask before planning" --output draft.json
```

No draft is published. Add a real provider by implementing `ContentProvider.generate`; keep the deterministic provider for tests.
