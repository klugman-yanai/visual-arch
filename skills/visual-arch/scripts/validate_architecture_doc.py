#!/usr/bin/env python3
"""Validate a generated standalone visual architecture HTML document."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


BOARD_RE = re.compile(
    r"const\s+BOARD\s*=\s*(\{.*?\});\s*const\s+GROUP_DETAILS\s*=",
    re.DOTALL,
)
CONFIDENCE_VALUES = {"source-backed", "inferred", "external", "unknown"}


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_model(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if "<!doctype html>" not in text.lower():
        fail("document is not an HTML document with a doctype")
    if "ReactFlow" not in text:
        fail("document does not appear to include the React Flow renderer")
    match = BOARD_RE.search(text)
    if not match:
        fail("could not find React Flow `const BOARD = {...};` model")
    try:
        return json.loads(match.group(1))
    except json.JSONDecodeError as error:
        fail(f"BOARD is not valid JSON: {error}")


def require_keys(obj: dict, keys: set[str], label: str) -> None:
    missing = sorted(keys - set(obj))
    if missing:
        fail(f"{label} missing required keys: {', '.join(missing)}")


def validate(path: Path) -> None:
    model = load_model(path)
    require_keys(model, {"lanes", "nodes", "edges", "views"}, "model")

    nodes = model["nodes"]
    edges = model["edges"]
    if not isinstance(nodes, list) or len(nodes) < 3:
        fail("model.nodes must contain at least three nodes")
    if not isinstance(edges, list) or not edges:
        fail("model.edges must contain at least one edge")
    if "overview" not in model["views"]:
        fail("model.views must include an overview view")

    node_ids: set[str] = set()
    for index, node in enumerate(nodes):
        require_keys(node, {"id", "title", "domain", "owner", "position", "purpose", "details"}, f"node[{index}]")
        node_id = node["id"]
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", node_id):
            fail(f"node id is not kebab-case: {node_id!r}")
        if node_id in node_ids:
            fail(f"duplicate node id: {node_id}")
        node_ids.add(node_id)
        details = node["details"]
        require_keys(details, {"summary", "inputs", "outputs", "why", "failures", "source", "source_confidence"}, f"node[{node_id}].details")
        if not details["source"]:
            fail(f"node {node_id} has no source references")
        if details["source_confidence"] not in CONFIDENCE_VALUES:
            fail(f"node {node_id} has invalid source_confidence {details['source_confidence']!r}")

    for index, edge in enumerate(edges):
        if not isinstance(edge, list) or len(edge) < 3:
            fail(f"edge[{index}] must be [source, target, label, kind?]")
        source, target, label = edge[:3]
        if not label:
            fail(f"edge[{index}] has empty label")
        if source not in node_ids:
            fail(f"edge[{index}] has unknown source {source}")
        if target not in node_ids:
            fail(f"edge[{index}] has unknown target {target}")

    for key, view in model["views"].items():
        require_keys(view, {"label", "focus"}, f"view[{key}]")
        unknown = [node_id for node_id in view["focus"] if node_id not in node_ids]
        if unknown:
            fail(f"view {key} references unknown nodes: {', '.join(unknown)}")

    print(f"OK: {path} contains {len(nodes)} nodes, {len(edges)} edges, {len(model['views'])} views")


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Validate standalone visual-arch HTML generated from the bundled production-style React Flow template."
        )
    )
    parser.add_argument("html", type=Path)
    args = parser.parse_args()
    if not args.html.exists():
        fail(f"file does not exist: {args.html}")
    validate(args.html)


if __name__ == "__main__":
    main()
