#!/usr/bin/env python3
"""Run local release checks for the map-it skill examples."""

from __future__ import annotations

import re
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "skills/map-it/scripts/validate_architecture_doc.py"
AUDITOR = ROOT / "skills/map-it/scripts/audit_claims.py"
OFFLINE_FORBIDDEN = re.compile(
    r"https?://(?!www\.w3\.org/2000/svg)|unpkg|jsdelivr|esm\.sh|ReactDOM|ReactFlow|@xyflow|import\s*\(",
    re.IGNORECASE,
)


def run(command: list[str]) -> None:
    print("+", " ".join(command))
    result = subprocess.run(command, cwd=ROOT, text=True)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def check_offline_html(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    matches = [match.group(0) for match in OFFLINE_FORBIDDEN.finditer(text)]
    if matches:
        sample = ", ".join(sorted(set(matches))[:8])
        raise SystemExit(f"offline example has forbidden dependency markers: {sample}")
    print(f"OK: {path.relative_to(ROOT)} has no external runtime dependency markers")


def check_topology_model(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    if '"lanes": []' not in text:
        raise SystemExit("service-topology example must remain a no-lane topology regression case")
    print("OK: service-topology remains a no-lane topology example")


def main() -> None:
    python = sys.executable
    run([python, "scripts/build_example.py"])

    for html in sorted((ROOT / "examples").glob("*/visual-architecture.html")):
        source_root = html.parent
        run([python, str(VALIDATOR), str(html), "--source-root", str(source_root)])
        with tempfile.TemporaryDirectory(prefix="map-it-audit-") as tmpdir:
            audit_path = Path(tmpdir) / "evidence-audit.md"
            run([
                python,
                str(AUDITOR),
                str(html),
                "--source-root",
                str(source_root),
                "--include",
                "all",
                "--output",
                str(audit_path),
            ])
            if not audit_path.exists() or audit_path.stat().st_size < 1_000:
                raise SystemExit(f"evidence audit checklist looked empty for {html}")

    check_offline_html(ROOT / "examples/keyboard-interrupt/visual-architecture.html")
    check_topology_model(ROOT / "examples/service-topology/model.json")
    print("OK: release checks passed")


if __name__ == "__main__":
    main()
