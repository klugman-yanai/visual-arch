---
name: visual-arch
description: "Create robust, project-agnostic visual architecture documents for codebases, systems, repositories, services, products, and technical projects. Produces source-backed standalone HTML architecture maps with graph views, navigable nodes, lanes/groups, detail content, stack selection, and verification. Use for architecture maps, onboarding docs, system overviews, pipeline diagrams, service maps, repo maps, and dependency/workflow visualizations."
---

# Visual Arch

Create a self-contained, interactive architecture HTML document from any project. The skill is intentionally project-agnostic: infer the domain from source files and docs; do not bake in Kardome, BMT, or any other project-specific vocabulary unless it appears in the target project.

## Quick Workflow

1. Define the target and output path.
   - Default target: current workspace.
   - Default output: `docs/visual-architecture.html` if a `docs/` folder exists, otherwise `visual-architecture.html`.
   - Ask only if overwriting a meaningful existing artifact would be risky.

2. Dispatch specialized subagents when the user explicitly asked for subagents, parallel agents, delegation, or this skill.
   - Use `references/agent-prompts.md` for role prompts.
   - Use the environment's available subagent mechanism (`spawn_agent`, task agents, or equivalent). If no subagent tool exists, run the roles locally in named passes and state that fallback.
   - Start with the stack selector unless the user already mandated a specific stack.
   - Keep each subagent bounded and ask for evidence with file paths.

3. Build a content model before writing HTML.
   - Use `references/content-model.md`.
   - Capture domains/groups, nodes, edges, views, owners, source files, inputs, outputs, failure/debug entry points, and "why this exists".
   - Prefer truthful incompleteness over invented certainty. Mark inferred details as inferred in prose.

4. Generate the document.
   - Use the stack selector's recommendation when it fits the project and constraints.
   - Use `assets/visual-architecture-template.html` as the primary bundled template for rich interactive architecture maps.
   - Replace the `ARCHITECTURE_MODEL` object with project-specific data.
   - Preserve the chosen artifact's standalone behavior unless the user explicitly wants integration into an app: no private runtime services, useful fallback content, accessible controls, responsive layout.

5. Verify before completion.
   - Run `python scripts/validate_architecture_doc.py <output.html>` for the bundled React Flow and Mermaid standalone templates.
   - For a custom stack, run the closest structural/build/render checks and document them.
   - If the project has a browser test path available, open the file or run a local static server and inspect the page visually.
   - Check that every source reference exists or is intentionally labeled external/generated.
   - Check that the first viewport has a clear title, visible controls, a nonblank diagram, and no text overlap at desktop and mobile widths.

## Quality Bar

The document must be useful to a new maintainer. Include the architecture shape, not just a diagram:

- System purpose and boundary.
- Major runtime/build/deploy/data/control-flow stages.
- Contracts between stages: artifacts, APIs, files, events, queues, databases, protocols, or human handoffs.
- Ownership or responsibility boundaries when discoverable.
- Failure/debug entry points for important nodes.
- Concrete source references.
- Multiple views for complex systems: overview plus focused flows.

Do not create a marketing landing page. The first screen is the actual interactive architecture surface.

## Subagent Roles

Use 4-6 specialized passes when allowed:

- **Stack selector**: decide the most relevant rendering/document stack for this project and output constraints.
- **Project cartographer**: inventory repo shape, languages, docs, manifests, services, entrypoints.
- **Flow analyst**: identify runtime, build, deploy, data, and control flows.
- **Contract auditor**: extract interfaces, artifacts, persistence, external systems, failure points.
- **Narrative editor**: turn findings into concise node/detail text for maintainers.
- **Visual verifier**: inspect the generated HTML for blank render, overlap, missing controls, broken references.

Merge results yourself. Resolve contradictions by checking source. Do not let subagents write overlapping files unless explicitly assigned disjoint outputs.

## Implementation Notes

- Use the repo's existing documentation first, then code/config/workflows/tests.
- Prefer `rg`/`fd` for discovery.
- Keep text short enough for nodes; put depth in the detail drawer.
- Use stable IDs (`lower-kebab-case`) for nodes and edges.
- Keep the graph readable: 8-30 primary nodes is usually better than exhaustive file-level mapping.
- Use lanes/groups to express responsibility or lifecycle phases.
- Use colors by function, not by brand, unless the project has explicit design guidance.
- Keep the output static and portable by default. Avoid requiring npm installs, bundlers, private assets, or live services unless the selected stack is intentionally integrated into an existing app.
- Cite generated or inferred sources honestly: `inferred from <path>`, `external: <name>`, or `generated artifact`.

## Stack Selection Guidance

React Flow is the primary bundled stack because this skill is meant to produce a rich interactive maintainer tool: clickable nodes, detail drawers, grouped lanes, focus views, and navigable source-backed contracts.

Prefer:

- React Flow or XYFlow for the normal case: interactive node graphs with detail drawers, filters, lanes, focus views, and many cross-links.
- Mermaid only when the user explicitly wants a text-native, Markdown-adjacent, no-React, or highly diffable artifact and accepts reduced interactivity.
- D3/SVG for custom hierarchical, radial, matrix, or timeline visuals.
- Cytoscape.js for large dependency graphs, clusters, and graph algorithms.
- Three.js only when spatial/3D structure is central to understanding the system.
- Native app/docs stack components when the project already has a documentation site or design system and the user wants integration over standalone portability.

Make the selector justify the recommendation using project evidence, output constraints, likely graph size, maintainability, offline/static needs, and verification cost.

## Resources

- `assets/visual-architecture-template.html`: primary standalone React Flow HTML template. Copy or adapt it unless constraints point to another stack.
- `assets/mermaid-architecture-template.html`: constrained standalone Mermaid HTML template for explicit text-native, Markdown-adjacent, no-React, or highly diffable output requests.
- `references/content-model.md`: expected model structure and authoring rules.
- `references/agent-prompts.md`: copy-ready prompts for specialized subagents.
- `scripts/validate_architecture_doc.py`: lightweight structural validator for generated HTML.
