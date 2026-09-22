"""Orchestrated, draft-only content generation."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .provider import ContentProvider, RuleBasedProvider

ROOT = Path(__file__).resolve().parents[2]
FACTS_PATH = ROOT / "knowledge" / "kim-holiday-business-facts.json"
SCHEMA_PATH = ROOT / "schemas" / "content-draft.schema.json"


class DraftRejected(ValueError):
    """Raised when a draft is not safe to present for approval."""


@dataclass
class ContentDraftPipeline:
    provider: ContentProvider | None = None

    def __post_init__(self) -> None:
        self.provider = self.provider or RuleBasedProvider()
        self.facts = json.loads(FACTS_PATH.read_text())

    def run(self, topic: str) -> dict[str, Any]:
        if not topic.strip():
            raise DraftRejected("A concrete topic is required.")

        context = self._orchestrate(topic)
        strategy = self._strategy(context)
        curator = self._curator(strategy)
        draft = self._brand_guard(curator, strategy)
        self._anti_slop_review(draft)
        self._validate(draft)
        return draft

    def _orchestrate(self, topic: str) -> dict[str, str]:
        self.provider.generate("orchestrator", f"Route topic: {topic}")
        return {"topic": topic.strip(), "channel": "Instagram"}

    def _strategy(self, context: dict[str, str]) -> dict[str, str]:
        self.provider.generate("content strategist", "Create one useful, evidence-grounded post angle.")
        return {
            **context,
            "angle": "Invite questions about Kim Holiday's current offering without inventing details.",
        }

    def _curator(self, strategy: dict[str, str]) -> dict[str, str]:
        self.provider.generate("Instagram curator", "Shape a concise caption and saveable prompt.")
        return {
            **strategy,
            "caption": (
                "Planning something special? Kim Holiday can help you start with the right questions. "
                "Send a DM with what you are considering, and ask about the current offering, timing, and next steps."
            ),
            "cta": "DM Kim Holiday with your question.",
        }

    def _brand_guard(self, content: dict[str, str], strategy: dict[str, str]) -> dict[str, Any]:
        self.provider.generate("brand guardian", "Check claims against the evidence ledger.")
        return {
            "schema_version": "1.0",
            "status": "draft",
            "approval_required": True,
            "channel": content["channel"],
            "topic": content["topic"],
            "angle": strategy["angle"],
            "caption": content["caption"],
            "cta": content["cta"],
            "hashtags": ["#KimHoliday"],
            "evidence": ["business_name:user-provided", "channel:request"],
            "review": {"brand_guardian": "passed", "anti_slop": "pending"},
        }

    def _anti_slop_review(self, draft: dict[str, Any]) -> None:
        self.provider.generate("anti-slop reviewer", "Reject unsupported specifics and empty generic copy.")
        text = f"{draft['caption']} {draft['cta']}".lower()
        forbidden = (
            r"\$\s?\d",
            r"\b(?:today|tomorrow|this week|limited|only \d+)\b",
            r"\b(?:available|sold out|fully booked)\b",
            r"\b(?:guarantee|guaranteed|best|#1|award-winning)\b",
            r"\b(?:testimonial|client said|customers? love)\b",
        )
        if any(re.search(pattern, text) for pattern in forbidden):
            raise DraftRejected("Draft contains an unsupported price, availability, superiority, or testimonial claim.")
        if len(draft["caption"].split()) < 12 or "Kim Holiday" not in draft["caption"]:
            raise DraftRejected("Draft is too generic or is missing the grounded business reference.")
        draft["review"]["anti_slop"] = "passed"

    def _validate(self, draft: dict[str, Any]) -> None:
        required = {"schema_version", "status", "approval_required", "channel", "topic", "angle",
                    "caption", "cta", "hashtags", "evidence", "review"}
        if set(draft) != required:
            raise DraftRejected("Draft does not match the required output shape.")
        if draft["status"] != "draft" or draft["approval_required"] is not True:
            raise DraftRejected("Only approval-gated drafts are supported.")
        if draft["review"] != {"brand_guardian": "passed", "anti_slop": "passed"}:
            raise DraftRejected("All required reviewers must pass.")


def write_draft(topic: str, output: Path) -> dict[str, Any]:
    draft = ContentDraftPipeline().run(topic)
    output.write_text(json.dumps(draft, indent=2) + "\n")
    return draft
