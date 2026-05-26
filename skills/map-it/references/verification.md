# Verification

Verification has two layers: deterministic checks and human judgment. Scale them to the document's trust level.

## Trust Levels

Use the lightest level that fits the user's intent:

- `draft`: exploratory or internal sketch. Required: structural validation, confidence labels, and stated assumptions. Render/audit checks are optional.
- `reviewable`: normal maintainer handoff. Required: structural validation, evidence checklist generation, representative semantic audit, and render/browser check when available without new downloads.
- `shareable`: high-trust, external, executive, security-sensitive, or decision-support artifact. Required: structural validation, evidence checklist, audit of every `source-backed` node, render/browser check, and explicit residual-risk note.

If the user does not specify trust level, infer it from context. Default to `reviewable` for a normal requested deliverable, `draft` for brainstorming or "quick sketch", and `shareable` only when the prompt implies publication or high-stakes reliance.

## Structural Validation

Run from the installed skill directory:

```bash
python <map-it-skill-dir>/scripts/validate_architecture_doc.py <output.html> --source-root <target-root>
```

Use `--source-root` when generated HTML lives outside the repo or example directory that source paths should resolve from.

The validator checks:

- `domains`, `owners`, `board`, and `groupDetails` exist.
- Required node, edge, view, detail, and confidence fields exist.
- Local-looking source references exist relative to `--source-root` or the output file directory.
- Intentional non-local references use accepted labels such as `external:`, `generated ...`, `inferred from ...`, or `unknown:`.
- Every view has matching `groupDetails`.

## Render Check

Run only when Playwright Python or an approved no-download equivalent is already available:

```bash
python <map-it-skill-dir>/scripts/render_check.py <output.html>
```

The Playwright path checks desktop and mobile viewports, rendered nodes, visible title, duplicate visible controls, node selection, detail drawer content, source chips, and page errors.

If Playwright is unavailable, ask before any install or browser-binary download prompt. The CLI screenshot fallback, when available, is a smoke check only; it does not prove drawer behavior, semantic correctness, or no-overlap quality.

## Evidence Audit Checklist

Generate a Markdown checklist for semantic review:

```bash
python <map-it-skill-dir>/scripts/audit_claims.py <output.html> --source-root <target-root> --output <audit.md>
```

By default the script extracts nodes marked `source-backed`. Use `--include all` to review every node, or another confidence value to inspect a specific bucket.

The checklist includes:

- Node title, id, domain, owner, and confidence.
- Source references with local existence status where applicable.
- Card purpose, summary, what/why text, inputs, outputs, and failures/debug claims.
- Audit-result checkboxes for support, downgrade, revise, or remove.

For `reviewable`, review a representative sample before completion. For `shareable`, review every `source-backed` node or clearly state that the semantic audit is incomplete. For `draft`, generating the checklist is optional.

## Offline Check

For pure offline output, inspect the generated HTML for external runtime dependencies:

```bash
rg -n "https?://|unpkg|jsdelivr|esm.sh|React|ReactDOM|ReactFlow|@xyflow|import\\(" <output.html>
```

Review matches manually. Names in explanatory text are not automatically failures, but script/link imports, CDN URLs, and bundled dependency blobs are.

## Duplicate Controls

Each visible control should have a distinct user-facing purpose. Do not ship pairs such as "Fit all" and "Reset view" when both lead to the same viewport state. Prefer one clear control label.

## Semantic Audit

Tooling cannot prove that every narrative claim is supported by cited files. The checklist turns this boundary into an explicit workflow, but the audit decision is still judgment. Manually audit:

- Node summaries.
- Inputs, outputs, contracts, and protocols.
- Failure modes and debugging guidance.
- "Why this exists" text.
- Claims marked `source-backed`.

Downgrade claims to `inferred`, `external`, or `unknown` when the cited evidence does not directly support them.

Final reports should state one of:

- Semantic audit completed for all `source-backed` nodes.
- Semantic audit completed for representative nodes, with remaining risk.
- Semantic audit checklist generated but not reviewed.
