#!/usr/bin/env python3
"""Validate a generated visual architecture HTML document."""

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
DATA_RE = re.compile(
    r"const\s+VISUAL_ARCH_DATA\s*=\s*(\{.*?\});\s*const\s+DOMAINS\s*=\s*VISUAL_ARCH_DATA\.domains",
    re.DOTALL,
)
DOMAINS_RE = re.compile(
    r"const\s+DOMAINS\s*=\s*(\{.*?\});\s*const\s+OWNERS\s*=",
    re.DOTALL,
)
OWNERS_RE = re.compile(
    r"const\s+OWNERS\s*=\s*(\{.*?\});\s*const\s+BOARD\s*=",
    re.DOTALL,
)
CONFIDENCE_VALUES = {"source-backed", "inferred", "external", "unknown"}
EDGE_KIND_VALUES = {"control", "artifact", "data", "signal", "decision", "dependency"}
NODE_TIER_VALUES = {"primary", "support", "detail"}
SOURCE_PREFIXES = (
    "external:",
    "generated ",
    "generated artifact",
    "inferred from ",
    "unknown:",
)


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def extract_json(text: str, pattern: re.Pattern[str], label: str) -> dict:
    match = pattern.search(text)
    if not match:
        fail(f"could not find React Flow `const {label} = ...;` model")
    try:
        return json.loads(match.group(1))
    except json.JSONDecodeError as error:
        fail(f"{label} is not valid JSON: {error}")


def normalize_model(raw: dict) -> tuple[dict, dict, dict, dict]:
    if {"domains", "owners", "board", "groupDetails"}.issubset(raw):
        return raw["domains"], raw["owners"], raw["board"], raw["groupDetails"]
    fail("model JSON must contain domains, owners, board, and groupDetails")


def load_models(path: Path) -> tuple[dict, dict, dict, dict]:
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".json":
        return normalize_model(json.loads(text))
    if "<!doctype html>" not in text.lower():
        fail("document is not an HTML document with a doctype")
    data_match = DATA_RE.search(text)
    if data_match:
        try:
            return normalize_model(json.loads(data_match.group(1)))
        except json.JSONDecodeError as error:
            fail(f"VISUAL_ARCH_DATA is not valid JSON: {error}")
    domains = extract_json(text, DOMAINS_RE, "DOMAINS")
    owners = extract_json(text, OWNERS_RE, "OWNERS")
    board = extract_json(text, BOARD_RE, "BOARD")
    fail("legacy HTML constants are missing VISUAL_ARCH_DATA.groupDetails; regenerate with the current template")


def require_keys(obj: dict, keys: set[str], label: str) -> None:
    missing = sorted(keys - set(obj))
    if missing:
        fail(f"{label} missing required keys: {', '.join(missing)}")


def is_intentional_nonlocal_source(source: str) -> bool:
    return source.startswith(SOURCE_PREFIXES)


def source_exists(source: str, root: Path) -> bool:
    if any(char in source for char in "*?["):
        return bool(list(root.glob(source)))
    return (root / source).exists()


def validate(path: Path, source_root: Path | None = None) -> None:
    domains, owners, model, group_details = load_models(path)
    source_root = source_root or path.parent
    require_keys(model, {"lanes", "nodes", "edges", "views"}, "model")
    if not domains:
        fail("DOMAINS must contain at least one domain")
    if not owners:
        fail("OWNERS must contain at least one owner")
    if not isinstance(group_details, dict) or not group_details:
        fail("groupDetails must be a non-empty object")
    if "overview" not in group_details:
        fail("groupDetails must include overview")
    require_keys(group_details["overview"], {"title", "summary"}, "groupDetails.overview")

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
        for source in details["source"]:
            if not isinstance(source, str) or not source.strip():
                fail(f"node {node_id} has an empty or non-string source reference")
            source = source.strip()
            if is_intentional_nonlocal_source(source):
                continue
            if not source_exists(source, source_root):
                fail(f"node {node_id} source reference does not exist from {source_root}: {source}")
        if details["source_confidence"] not in CONFIDENCE_VALUES:
            fail(f"node {node_id} has invalid source_confidence {details['source_confidence']!r}")
        if node["domain"] not in domains:
            fail(f"node {node_id} references unknown domain {node['domain']!r}")
        if node["owner"] not in owners:
            fail(f"node {node_id} references unknown owner {node['owner']!r}")
        if node.get("tier", "primary") not in NODE_TIER_VALUES:
            fail(f"node {node_id} has invalid tier {node['tier']!r}")
        if "hidden" in node and not isinstance(node["hidden"], bool):
            fail(f"node {node_id} hidden must be a boolean")

    for node in nodes:
        unknown_reveal = [node_id for node_id in node.get("revealFor", []) if node_id not in node_ids]
        if unknown_reveal:
            fail(f"node {node['id']} revealFor references unknown nodes: {', '.join(unknown_reveal)}")

    for index, lane in enumerate(model["lanes"]):
        require_keys(lane, {"id", "title", "domain", "position"}, f"lane[{index}]")
        if lane["domain"] not in domains:
            fail(f"lane {lane['id']} references unknown domain {lane['domain']!r}")

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
        if len(edge) >= 4 and edge[3] not in EDGE_KIND_VALUES:
            fail(f"edge[{index}] has invalid kind {edge[3]!r}")

    for key, view in model["views"].items():
        require_keys(view, {"label", "focus"}, f"view[{key}]")
        if key not in group_details:
            fail(f"groupDetails missing entry for view {key!r}")
        require_keys(group_details[key], {"title", "summary"}, f"groupDetails[{key}]")
        unknown = [node_id for node_id in view["focus"] if node_id not in node_ids]
        if unknown:
            fail(f"view {key} references unknown nodes: {', '.join(unknown)}")

    print(f"OK: {path} contains {len(nodes)} nodes, {len(edges)} edges, {len(model['views'])} views")


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Validate map-it HTML generated from the bundled production-style React Flow template."
        )
    )
    parser.add_argument("input", type=Path, help="Generated HTML document or source model JSON")
    parser.add_argument(
        "--source-root",
        type=Path,
        help="Root for validating local source references. Defaults to the input file's directory.",
    )
    args = parser.parse_args()
    if not args.input.exists():
        fail(f"file does not exist: {args.input}")
    validate(args.input, args.source_root)


if __name__ == "__main__":
    main()
