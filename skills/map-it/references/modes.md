# Dependency Modes

Choose the rendering path from the resolved dependency mode. Do not download, install, vendor, or prompt the user to install anything unless they explicitly approve that dependency step.

## CDN-Backed Online HTML

Use when the user allows online dependencies or asks for the richest portable interaction.

- Template: `assets/visual-architecture-template.html`.
- May load React, React DOM, and XYFlow from public CDNs.
- Good for pan/zoom graph exploration, richer node interaction, and polished single-file architecture boards.
- Be explicit that the artifact needs network access for CDN assets unless the browser has cached them.

## Pure Offline HTML/CSS/JS

Use when the user needs no internet and no dependency downloads.

- Template: `assets/visual-architecture-offline-template.html`.
- Must not use CDN dependencies, bundled library blobs, vendored runtime libraries, npm packages, or downloaded assets.
- Use plain HTML, CSS, SVG, and JavaScript authored in the file.
- Keep interactions reliable: focus filters, node selection, details, basic zoom/pan, responsive layout, and keyboard-safe controls.
- If a feature requires a library, either simplify the feature or ask for a different approved mode.

## Existing App/Docs Integration

Use when the target repo already has a required documentation shell or component system, or the user asks for integration.

- Follow the repo's frontend stack, routing, design tokens, and build/test workflow.
- Keep the same evidence-labeled model contract.
- Do not introduce new packages without permission.
- Prefer local components and existing graph/layout libraries already present in the project.

## Mode Selection Heuristics

- Corporate, air-gapped, security-sensitive, or "no internet" context: pure offline.
- One-off shareable explainer with permission for public dependencies: CDN-backed online.
- Existing docs app with clear conventions: integrate locally.
- Unknown mode: ask before building.
