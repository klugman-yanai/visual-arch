#!/usr/bin/env python3
"""Extract an evidence-audit checklist from a map-it model or HTML file."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from validate_architecture_doc import is_intentional_nonlocal_source, load_models, source_exists


def as_items(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    text = str(value).strip()
    return [text] if text else []


def source_status(source: str, root: Path) -> str:
    source = source.strip()
    if is_intentional_nonlocal_source(source):
        return "intentional non-local"
    if source_exists(source, root):
        return "exists"
    return "missing"


def add_claim_section(lines: list[str], title: str, value: Any) -> None:
    items = as_items(value)
    if not items:
        return
    lines.append(f"  - {title}:")
    for item in items:
        lines.append(f"    - [ ] {item}")


def render_audit(path: Path, source_root: Path | None, include: str) -> str:
    _domains, _owners, board, _group_details = load_models(path)
    root = source_root or path.parent
    nodes = board["nodes"]
    selected = [
        node for node in nodes
        if include == "all" or node.get("details", {}).get("source_confidence") == include
    ]

    lines = [
        "# Architecture Map Evidence Audit",
        "",
        f"- Input: `{path}`",
        f"- Source root: `{root}`",
        f"- Nodes in model: {len(nodes)}",
        f"- Nodes in audit: {len(selected)}",
        f"- Inclusion: `{include}`",
        "",
        "## Audit Instructions",
        "",
        "- Check each listed claim against the cited sources.",
        "- Keep `source-backed` only when the cited evidence directly supports the claim.",
        "- Downgrade weak claims to `inferred`, `external`, or `unknown` in the model before sharing.",
        "- Treat this checklist as an evidence workflow, not proof that the claims are true.",
        "",
        "## Claims",
        "",
    ]

    if not selected:
        lines.append("_No nodes matched the requested confidence filter._")
        return "\n".join(lines) + "\n"

    for node in selected:
        details = node["details"]
        confidence = details.get("source_confidence", "unknown")
        lines.extend([
            f"### {node['title']} (`{node['id']}`)",
            "",
            f"- Confidence: `{confidence}`",
            f"- Domain: `{node.get('domain', 'unknown')}`",
            f"- Owner: `{node.get('owner', 'unknown')}`",
            "- Sources:",
        ])
        for source in as_items(details.get("source")):
            lines.append(f"  - [{source_status(source, root)}] `{source}`")
        if not as_items(details.get("source")):
            lines.append("  - [missing] _No source references_")
        lines.append("- Claims to verify:")
        add_claim_section(lines, "Card purpose", node.get("purpose"))
        add_claim_section(lines, "Summary", details.get("summary"))
        add_claim_section(lines, "What", details.get("what"))
        add_claim_section(lines, "Why", details.get("why"))
        add_claim_section(lines, "Inputs", details.get("inputs"))
        add_claim_section(lines, "Outputs", details.get("outputs"))
        add_claim_section(lines, "Failures/debug", details.get("failures"))
        lines.extend([
            "- Audit result:",
            "  - [ ] Supported as written",
            "  - [ ] Downgrade confidence",
            "  - [ ] Revise wording",
            "  - [ ] Remove claim",
            "",
        ])

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a Markdown checklist for auditing map-it source-backed claims."
    )
    parser.add_argument("input", type=Path, help="Generated HTML document or source model JSON")
    parser.add_argument(
        "--source-root",
        type=Path,
        help="Root for displaying local source-reference status. Defaults to the input file's directory.",
    )
    parser.add_argument(
        "--include",
        choices=["source-backed", "inferred", "external", "unknown", "all"],
        default="source-backed",
        help="Which confidence bucket to include in the checklist.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Write the checklist to this Markdown file instead of stdout.",
    )
    args = parser.parse_args()
    if not args.input.exists():
        print(f"ERROR: file does not exist: {args.input}", file=sys.stderr)
        raise SystemExit(1)

    text = render_audit(args.input, args.source_root, args.include)
    if args.output:
        args.output.write_text(text, encoding="utf-8")
        print(f"OK: wrote evidence audit checklist to {args.output}")
    else:
        print(text)


if __name__ == "__main__":
    main()
