# Intake Decisions

Resolve decisions from the user request, current conversation, and a light repo scan. Ask only when a decision would materially change the output.

## Mandatory Decision

Dependency mode must be explicit before generation:

- CDN-backed online HTML.
- Pure offline HTML/CSS/JS with no external or bundled runtime dependencies.
- Existing-app/docs integration.

If the request does not clearly select one, ask a direct question before building.

Good question:

> Should the output be pure offline HTML/CSS/JS with no external dependencies, or may it use public CDN dependencies for richer graph interaction?

## Other Decisions

Infer these when the evidence is clear:

- Trust level: `draft`, `reviewable`, or `shareable`.
- Target scope: full repo, service, subsystem, protocol, workflow, incident path, package, or docs slice.
- Primary reader: new maintainer, reviewer, operator, architect, product/leadership, or mixed.
- Emphasis: runtime behavior, data movement, debugging, deployment, package structure, ownership, lifecycle, or protocol mechanics.
- Map structure: topology, lifecycle, journey, process flow, dependency graph, ownership view, matrix, radial, swimlanes, or hybrid.
- Visual direction: existing project design, neutral technical UI, dense operations view, editorial explainer, or user-supplied reference.
- Sensitivity: preserve exact source paths/names or generalize for a wider audience.
- Output path and overwrite policy.

Ask when there are multiple plausible answers with different artifacts:

- "Should this read as a topology map, lifecycle map, process flow, ownership view, or debugging journey?"
- "Who is the primary reader: new maintainer, reviewer, operator, or leadership?"
- "Should this prioritize runtime behavior, data movement, deployment/release mechanics, or repo/package structure?"
- "Should the visual style follow an existing project/design system or use a neutral technical default?"
- "Should source paths and internal system names be preserved, or generalized?"
- "Is this a quick draft, a reviewable maintainer handoff, or a shareable high-trust artifact?"

## Defaults After Mode Is Resolved

When the user does not answer non-mode questions, use conservative defaults and state them:

- `reviewable` trust level for a normal requested deliverable; `draft` for sketches/brainstorming.
- Current workspace as target scope.
- Maintainer audience.
- Mixed runtime/debug emphasis.
- Structure best supported by repo evidence.
- Clean neutral technical UI.
- Default output path from `SKILL.md`.
- Preserve exact paths/names unless sensitivity concerns are visible.

Do not block on low-value questions such as left-to-right versus top-to-bottom when the content itself makes the answer obvious.
