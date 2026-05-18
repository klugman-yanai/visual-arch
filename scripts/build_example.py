#!/usr/bin/env python3
"""Build the project-agnostic example HTML from the skill template and model."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOKEN = "__VISUAL_ARCH_DATA__"


def main() -> None:
    template_path = ROOT / "skills/visual-arch/assets/visual-architecture-template.html"
    model_path = ROOT / "examples/project-agnostic/model.json"
    output_path = ROOT / "examples/project-agnostic/visual-architecture.html"

    template = template_path.read_text()
    if TOKEN not in template:
        raise SystemExit(f"template missing {TOKEN}")

    model = json.loads(model_path.read_text())
    rendered = template.replace(TOKEN, json.dumps(model, indent=8))
    output_path.write_text(rendered)
    print(f"wrote {output_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
