from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from pdf_autogenerator.qa import run_qa  # noqa: E402


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Run dataset QA checks against a manifest")
    parser.add_argument("--manifest", required=True, help="Path to manifest.jsonl")
    args = parser.parse_args()

    report = run_qa(Path(args.manifest))
    print(json.dumps(report, indent=2))
    return 0 if report["overall_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
