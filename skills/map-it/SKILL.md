---
name: map-it
description: "Use when creating evidence-labeled interactive maps for a codebase, system, service, repository, protocol, technical workflow, onboarding doc, service map, dependency visualization, or debugging-oriented system overview."
---

# Map It

Create a polished, portable architecture map from any project. This skill is project-agnostic: infer vocabulary, structure, visual language, and reader needs from the target repo and user prompt instead of copying the bundled examples.

## Quick Workflow

1. Resolve intake decisions before building.
   - First inspect the user's request, current conversation context, and a lightweight repo inventory.
   - Dependency mode is mandatory. If the request/context does not clearly imply CDN-backed online, pure offline, or existing-app integration, ask before choosing.
   - Resolve trust level, target scope, primary reader, emphasis, map structure, visual direction, output path/overwrite policy, and sensitivity by inference or by asking.
   - Ask only when an unresolved decision would materially change the artifact. Use `references/intake.md` for question strategy.
   - Never download, install, or prompt the user to install dependencies unless the user has explicitly approved that dependency step.

2. Define target and output.
   - Default target: current workspace.
   - Default output: `docs/visual-architecture.html` when `docs/` exists, otherwise `visual-architecture.html`.
   - Ask before overwriting a meaningful existing artifact if the user's intent is unclear.

3. Use subagents only when explicitly allowed.
   - Dispatch specialized subagents only when the user asked for subagents, delegation, or parallel agents.
   - Use `references/agent-prompts.md` for role prompts.
   - If subagents are unavailable or not allowed, run the same roles locally in named passes.

4. Build the content model before writing HTML.
   - Read `references/content-model.md`.
   - Produce `VISUAL_ARCH_DATA` with non-empty `domains`, non-empty `owners`, `board`, and `groupDetails`.
   - Capture nodes, edges, views, contracts, source references, failure/debug entry points, "why this exists", and confidence labels.
   - Prefer truthful incompleteness over invented certainty. Mark unsupported or inferred details visibly.

5. Choose the rendering path from the resolved mode.
   - Read `references/modes.md` when selecting or explaining dependency mode.
   - Use `assets/visual-architecture-template.html` for CDN-backed online output.
   - Use `assets/visual-architecture-offline-template.html` for pure offline output with only HTML/CSS/JS and no bundled runtime libraries.
   - Integrate with an existing docs/app stack only when the project or user request clearly calls for that.

6. Design for the project, not the example.
   - Read `references/design-principles.md` before a new document or major redesign.
   - Pick topology, lifecycle, journey, matrix, swimlanes, radial, dependency graph, or another structure based on the repo evidence.
   - Use swimlanes only when they clarify responsibility, lifecycle, or ownership boundaries.
   - Derive palette, node treatment, labels, density, and control surface from the project, existing design system, supplied examples, or user prompt.
   - Keep visible controls distinct. Do not include duplicate buttons that lead to the same state.

7. Verify to the resolved trust level.
   - Read `references/verification.md` for the required checks and limits.
   - Use `draft` for exploratory/internal sketches, `reviewable` for normal handoff, and `shareable` for high-trust or externally shared docs.
   - Run `python <map-it-skill-dir>/scripts/validate_architecture_doc.py <output.html> --source-root <target-root>` when source paths should resolve from a repo root.
   - For `reviewable` and `shareable`, generate an evidence checklist with `python <map-it-skill-dir>/scripts/audit_claims.py <output.html> --source-root <target-root> --output <audit.md>`.
   - For `reviewable` and `shareable`, run `python <map-it-skill-dir>/scripts/render_check.py <output.html>` only when Playwright Python or an approved no-download equivalent is already available.
   - For `shareable`, audit all `source-backed` nodes or clearly state any unaudited claims.
   - If Playwright or browser binaries are missing, ask before any install/download prompt and use structural plus manual checks if permission is not granted.

## Quality Bar

The document must help a new maintainer understand the architecture shape, not just see a graph:

- System purpose and boundary.
- Major runtime, data, build, deploy, protocol, or human handoff stages relevant to the target.
- Contracts between stages: APIs, files, events, queues, databases, artifacts, protocols, or operator actions.
- Ownership or responsibility boundaries when discoverable.
- Failure/debug entry points for important nodes.
- Concrete source references with confidence labels: `source-backed`, `inferred`, `external`, or `unknown`.
- Overview first, focus/filter views next, details on selection.
- A readable primary path with secondary mechanics kept quieter.
- Context-appropriate UI polish, responsive first viewport, accessible controls, and no generic graph dump.

Do not create a marketing landing page. The first screen is the interactive architecture surface.

## Fixed Contract

These are fixed parts of the skill:

- Evidence-labeled content model with domains, owners, nodes, edges, views, details, and confidence labels.
- Explicit dependency mode before generation.
- Explicit trust level: `draft`, `reviewable`, or `shareable`.
- Portable HTML output or intentional integration into an existing app/docs stack.
- Progressive disclosure: overview, focus/filter, then node details.
- Local validation of structure, source references, required group details, and duplicate visible controls where render tooling is available.
- Explicit evidence-audit workflow for `source-backed` claims, because tooling can organize and check references but cannot prove every sentence is true.

These are context-sensitive and should be inferred or asked:

- Visual theme, palette, labels, map structure, node shape, density, interaction depth, and emphasis.
- Trust level when the user's intent is ambiguous.
- Whether examples are used as quality benchmarks, style references, or ignored.
- Whether private names/source paths are preserved or generalized.

## Implementation Notes

- Use repo docs first, then manifests, source, tests, workflows, and config.
- Prefer `rg`/`fd` for discovery.
- Keep overview maps compact. Put depth in details, focus views, or source references.
- Use stable IDs such as `lower-kebab-case`.
- Route edges deliberately. Clean connector flow is part of the design.
- Cite generated or inferred sources honestly: `inferred from <path>`, `external: <name>`, `generated artifact`, or `unknown: <reason>`.
- Exclude generated output, vendored dependencies, lockfiles, caches, minified bundles, and broad utility modules unless architecturally important.

## Completion Checklist

- The graph model validates with `validate_architecture_doc.py`.
- Verification matched the trust level from `references/verification.md`.
- For `reviewable` or `shareable`, an evidence audit checklist was generated with `audit_claims.py`, then reviewed or explicitly reported as not reviewed.
- For `reviewable` or `shareable`, the document render was checked with `render_check.py`, browser inspection, or a clearly stated no-browser limitation.
- Every node has source references and `source_confidence`.
- Representative claims were manually checked against cited evidence, especially for `source-backed` nodes.
- Inferred and unknown claims are visibly labeled.
- Desktop and mobile first viewports show title, controls, diagram, and details without obvious overlap.
- Visible controls are not duplicated.
- The final answer reports the output path, dependency mode, trust level, and verification commands.

## Resources

- `assets/visual-architecture-template.html`: CDN-backed React Flow HTML template for online mode.
- `assets/visual-architecture-offline-template.html`: pure HTML/CSS/JS template for offline mode.
- `references/intake.md`: context-sensitive question and decision strategy.
- `references/modes.md`: dependency modes and rendering choices.
- `references/design-principles.md`: layout, interaction, and visual hierarchy guidance.
- `references/content-model.md`: expected model structure and authoring rules.
- `references/agent-prompts.md`: copy-ready prompts for specialized passes or approved subagents.
- `references/verification.md`: validation, render, duplicate-control, offline, and semantic audit guidance.
- `references/examples.md`: how to use bundled examples as references without copying their domain-specific style.
- `scripts/validate_architecture_doc.py`: structural, source-reference, confidence, and `groupDetails` validator.
- `scripts/audit_claims.py`: Markdown evidence checklist generator for semantic review of `source-backed` claims.
- `scripts/render_check.py`: optional Playwright render smoke test for desktop/mobile, node selection, source chips, and duplicate visible controls.
