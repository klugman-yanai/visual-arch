---
name: visual-arch
description: "Create robust, project-agnostic, high-quality visual architecture documents for codebases, systems, repositories, services, products, and technical projects. Produces source-backed standalone React Flow HTML architecture maps with graph views, navigable nodes, lanes/groups, detail content, source confidence labels, coordinated subagent analysis, and verification. Use for architecture maps, onboarding docs, system overviews, pipeline diagrams, service maps, repo maps, and dependency/workflow visualizations."
---

# Visual Arch

Create a polished, self-contained React Flow architecture HTML document from any project. The skill is intentionally project-agnostic: infer the domain from source files and docs; do not bake in any project-specific vocabulary unless it appears in the target project.

## Quick Workflow

1. Define the target and output path.
   - Default target: current workspace.
   - Default output: `docs/visual-architecture.html` if a `docs/` folder exists, otherwise `visual-architecture.html`.
   - Ask only if overwriting a meaningful existing artifact would be risky.

2. Dispatch specialized subagents when the user explicitly asked for subagents, parallel agents, delegation, or this skill.
   - Use `references/agent-prompts.md` for role prompts.
   - Start with the intake strategist if the request leaves important choices ambiguous.
   - Dispatch cartographer, flow analyst, contract auditor, and design planner in parallel when possible.
   - Use the environment's available subagent mechanism (`spawn_agent`, task agents, or equivalent). If no subagent tool exists, run the same roles locally in named passes and state that fallback.
   - Require structured output from each role: facts, candidate nodes, candidate edges, exclusions, uncertainties, and evidence paths.

3. Build a content model before writing HTML.
   - Use `references/content-model.md`.
   - Capture domains/groups, nodes, edges, views, owners, source files, inputs, outputs, failure/debug entry points, source confidence, and "why this exists".
   - Prefer truthful incompleteness over invented certainty. Mark inferred details with `source_confidence: "inferred"`.

4. Generate the document.
   - Use `assets/visual-architecture-template.html` as the primary bundled template.
   - Build a `VISUAL_ARCH_DATA` object with `domains`, `owners`, `board`, and `groupDetails`.
   - Replace the `__VISUAL_ARCH_DATA__` token in the template with that JSON object.
   - Default to a vertical, top-to-bottom flow. Treat the artifact as a modern interactive upgrade of a sequence diagram: entrypoints at the top, orchestration/policy/work in the middle, state/reporting/signal at the bottom.
   - Preserve standalone behavior: no private runtime services, useful fallback content, accessible controls, responsive layout.

5. Verify before completion.
   - Run `python scripts/validate_architecture_doc.py <output.html>`.
   - Run `python scripts/render_check.py <output.html>` when Playwright is available.
   - Check that every source reference exists or is intentionally labeled external/generated.
   - Check that the first viewport has a clear title, visible controls, a nonblank diagram, and no text overlap at desktop and mobile widths.
   - Use the completion checklist below before saying the work is done.

## Quality Bar

The document must be useful to a new maintainer. Include the architecture shape, not just a diagram:

- System purpose and boundary.
- Major runtime/build/deploy/data/control-flow stages.
- Contracts between stages: artifacts, APIs, files, events, queues, databases, protocols, or human handoffs.
- Ownership or responsibility boundaries when discoverable.
- Failure/debug entry points for important nodes.
- Concrete source references.
- Source confidence labels: `source-backed`, `inferred`, `external`, or `unknown`.
- Multiple views for complex systems: overview plus focused flows.

Do not create a marketing landing page. The first screen is the actual interactive architecture surface.

## User Questions

Ask the user only when a choice materially changes the artifact and cannot be inferred from the project or request. The default orientation is vertical sequence-style flow. Ask about orientation only when the user hints at a preference, the system is primarily spatial/topological, or the flow could be read equally well in multiple directions.

Good intake questions:

- "Should this read as a vertical sequence-style flow, or as a horizontal lifecycle map?"
- "Who is the primary reader: new maintainer, reviewer, operator, or product/leadership?"
- "Should the document prioritize runtime behavior, deployment/release flow, data movement, or repo/package structure?"

Avoid blocking on questions that have a safe default. When in doubt, create a vertical maintainer-oriented first draft and note the assumption.

## Subagent Roles

Use 4-6 specialized passes when allowed. Parallelize the first four roles; synthesize them yourself before writing the HTML.

- **Intake strategist**: decide whether user questions are needed, choose default orientation, audience, and emphasis. Do not ask low-value questions.
- **Project cartographer**: inventory repo shape, languages, docs, manifests, services, entrypoints.
- **Flow analyst**: identify runtime, build, deploy, data, and control flows.
- **Contract auditor**: extract interfaces, artifacts, persistence, external systems, failure points.
- **Design planner**: choose visual grouping, node density, vertical lane layout by default, views, color roles, and interaction priorities.
- **Narrative editor**: turn findings into concise node/detail text for maintainers.
- **Visual verifier**: inspect the generated HTML for blank render, overlap, missing controls, broken references.

Merge results yourself. Resolve contradictions by checking source. Do not let subagents write overlapping files unless explicitly assigned disjoint outputs.

## Implementation Notes

- Use the repo's existing documentation first, then code/config/workflows/tests.
- Prefer `rg`/`fd` for discovery.
- Keep text short enough for nodes; put depth in the detail drawer.
- Use stable IDs (`lower-kebab-case`) for nodes and edges.
- Keep the graph readable: 8-30 primary nodes is usually better than exhaustive file-level mapping.
- Use lanes/groups to express responsibility or lifecycle phases. Prefer horizontal lanes stacked vertically, so the reading path is top-to-bottom.
- Use colors by function, not by brand, unless the project has explicit design guidance.
- Keep the output static and portable by default. Avoid requiring npm installs, bundlers, private assets, or live services unless the selected stack is intentionally integrated into an existing app.
- Cite generated or inferred sources honestly: `inferred from <path>`, `external: <name>`, or `generated artifact`.

## Do Not Map

Exclude noise unless it is architecturally important:

- Generated output, vendored dependencies, lockfiles, snapshots, caches, minified bundles, and build artifacts.
- Broad utility modules that do not define system boundaries.
- Every test file individually; map tests only when they define contracts, gates, or workflows.
- Every component/class/function; map subsystem responsibilities and contracts instead.
- Secrets, private credentials, personal data, or sensitive internal endpoints.

## Source Confidence

Assign every node and important claim one confidence value:

- `source-backed`: directly supported by source, config, tests, docs, or workflows.
- `inferred`: reasonable inference from multiple source clues; label it as inferred in text.
- `external`: known external system or user-operated boundary.
- `unknown`: visible architecture gap; explain what evidence is missing.

Never upgrade inferred or unknown claims to source-backed during editing unless you checked the evidence.

## Stack Rubric

React Flow is the primary bundled stack because this skill is meant to produce a rich interactive maintainer tool: clickable nodes, detail drawers, grouped lanes, focus views, and navigable source-backed contracts.

Use React Flow unless one of these is true:

- The user explicitly asks for integration into an existing docs/app stack.
- The target already has a required documentation component system.
- The graph is very large and needs graph algorithms or clustering beyond simple focus views; consider Cytoscape.js.
- The visual form is primarily a hierarchy, radial map, timeline, or matrix; consider D3/SVG.
- Spatial/3D structure is essential to understanding the system; consider Three.js.

Do not use text-first diagram stacks for this skill's primary output. This skill is for high-quality visual designs.

## Completion Checklist

Before final response:

- The graph model validates with `validate_architecture_doc.py`.
- The document render was checked with `render_check.py` or a browser, or the limitation is stated.
- Every node has source references and `source_confidence`.
- Inferred and unknown claims are visibly labeled.
- Excluded generated/vendor/noise areas are noted in the working summary when relevant.
- Desktop and mobile first viewports show title, controls, diagram, and details without obvious overlap.
- The final answer reports the output path and verification commands.

## Resources

- `assets/visual-architecture-template.html`: primary standalone React Flow HTML template. Copy or adapt it unless constraints point to another stack.
- `references/content-model.md`: expected model structure and authoring rules.
- `references/agent-prompts.md`: copy-ready prompts for specialized subagents.
- `scripts/validate_architecture_doc.py`: structural validator for generated HTML.
- `scripts/render_check.py`: optional Playwright render smoke test for desktop and mobile viewports.
