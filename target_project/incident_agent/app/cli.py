"""Interface de linha de comando para o workflow."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from shared.aula_4.config import get_settings
from shared.aula_4.validation import validate_incident_input

from .workflow import run_workflow

PROJECT_DIR = Path(__file__).resolve().parents[1]


def load_incident(path: str | Path) -> dict:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    return validate_incident_input(payload)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Investigação multiagente de incidentes")
    subparsers = parser.add_subparsers(dest="command", required=True)
    investigate = subparsers.add_parser("investigate")
    investigate.add_argument("--incident-file", required=True)
    investigate.add_argument("--knowledge-dir", default=str(PROJECT_DIR / "data" / "knowledge"))
    investigate.add_argument("--env-file", default=str(PROJECT_DIR / ".env"))
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.command == "investigate":
        settings = get_settings(args.env_file)
        result = run_workflow(load_incident(args.incident_file), settings, args.knowledge_dir)
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
