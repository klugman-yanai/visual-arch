# visual-arch

Reusable agent skill for creating polished, project-agnostic visual architecture documents.

`visual-arch` helps Codex and Claude inspect a project, coordinate focused analysis passes, and produce a source-backed React Flow architecture map as a standalone HTML document.

## Install

Run the interactive installer and choose your agent/harness:

    npx skills add klugman-yanai/visual-arch

For a targeted non-interactive install:

    npx skills add klugman-yanai/visual-arch --skill visual-arch -a codex -a claude-code

## Use

    First explore the project, then use $visual-arch to create an interactive visual architecture document for this project.

## What It Creates

- A standalone React Flow HTML architecture document.
- Clickable architecture nodes with detail panels.
- Lanes, focused views, edge labels, source references, and confidence labels.
- Local validation and optional browser render checks.

See `examples/project-agnostic/visual-architecture.html` for a simplified, project-agnostic sample.

## Design Benchmark

This skill is based on the evolving production document at
`kardome-bmt-suite/docs/visual-architecture.html`. When maintaining this repo,
compare the template and example against that document's current design
language: grouped lanes, clean tracks, deliberate edge handles, polished detail
panels, and a first viewport that feels like a usable architecture tool rather
than a generic diagram.

Keep the public skill project-agnostic. Do not copy Kardome-specific names into
the skill description or example model unless they are only mentioned here as
maintainer context.

The sample is generated from:

- `skills/visual-arch/assets/visual-architecture-template.html`
- `examples/project-agnostic/model.json`

Regenerate it with:

    python scripts/build_example.py

## Trust And Runtime Notes

- The skill itself does not send project code anywhere.
- Agents using the skill inspect local project files to build the document.
- The bundled HTML template loads React, React DOM, and XYFlow from public CDNs.
- The validator scripts run locally.
- Generated documents should be reviewed before publishing when they include private paths, internal system names, or inferred architecture claims.
