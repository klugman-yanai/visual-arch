#!/usr/bin/env python3
"""Build the example HTML files from the skill template and models."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOKEN = "__VISUAL_ARCH_DATA__"


def main() -> None:
    online_template_path = ROOT / "skills/map-it/assets/visual-architecture-template.html"
    offline_template_path = ROOT / "skills/map-it/assets/visual-architecture-offline-template.html"
    templates = {
        "online": online_template_path.read_text(),
        "offline": offline_template_path.read_text(),
    }
    for name, template in templates.items():
        if TOKEN not in template:
            raise SystemExit(f"{name} template missing {TOKEN}")

    model_paths = sorted((ROOT / "examples").glob("*/model.json"))
    if not model_paths:
        raise SystemExit("no example model.json files found")

    for model_path in model_paths:
        output_path = model_path.with_name("visual-architecture.html")
        model = json.loads(model_path.read_text())
        mode = "offline" if model_path.parent.name == "keyboard-interrupt" else "online"
        template = templates[mode]
        rendered = template.replace(TOKEN, json.dumps(model, indent=8))
        output_path.write_text(rendered)
        print(f"wrote {output_path.relative_to(ROOT)} ({mode})")


if __name__ == "__main__":
    main()
