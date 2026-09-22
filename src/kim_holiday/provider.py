"""Provider boundary for future LLM-backed agents."""

from dataclasses import dataclass
from typing import Protocol


class ContentProvider(Protocol):
    """Generate text from a role prompt without owning business truth."""

    def generate(self, role: str, instruction: str) -> str:
        ...


@dataclass(frozen=True)
class RuleBasedProvider:
    """Deterministic local provider used by tests and the draft CLI."""

    def generate(self, role: str, instruction: str) -> str:
        return f"{role}: {instruction}"
