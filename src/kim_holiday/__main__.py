from __future__ import annotations

import argparse
import json
from pathlib import Path

from .pipeline import ContentDraftPipeline, write_draft


def main() -> None:
    parser = argparse.ArgumentParser(description="Create an approval-gated Kim Holiday content draft.")
    parser.add_argument("topic", help="Specific topic or audience question for the draft.")
    parser.add_argument("-o", "--output", type=Path, help="Write JSON to this path instead of stdout.")
    args = parser.parse_args()
    if args.output:
        write_draft(args.topic, args.output)
        print(f"Wrote draft to {args.output}")
    else:
        print(json.dumps(ContentDraftPipeline().run(args.topic), indent=2))


if __name__ == "__main__":
    main()
