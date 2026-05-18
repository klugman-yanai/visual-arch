# visual-arch

Create polished, interactive visual architecture documents for codebases, systems,
services, pipelines, and technical products.

`visual-arch` helps Codex and Claude turn a repo or system description into a
source-backed standalone HTML architecture map. The output is not a static
Mermaid diagram: it is a navigable React Flow document with lanes, focused
views, clickable nodes, detail panels, edge labels, source references, confidence
labels, and validation scripts.

Use it when you want a maintainer-friendly architecture map for onboarding,
review, incident orientation, system explanation, or technical planning.

## Install

Run the interactive installer and choose your agent/harness:

    npx skills add klugman-yanai/visual-arch

For a targeted non-interactive install:

    npx skills add klugman-yanai/visual-arch --skill visual-arch -a codex -a claude-code

## Use

    First explore the project, then use $visual-arch to create an interactive visual architecture document for this project.

You can also point it at a specific system, service, workflow, or question:

    Use $visual-arch to explain how the authentication flow works.

    Use $visual-arch to create a visual architecture doc for the build and release pipeline.

    Use $visual-arch to map this repo for a new maintainer.

## What It Creates

- A standalone `visual-architecture.html` file you can open in a browser.
- A research-backed swimlane/process-flow architecture graph with deliberate edge routing.
- Clickable nodes with summaries, inputs, outputs, failure modes, and "why this exists" notes.
- Focus modes for runtime, data flow, debugging, deployment, or other relevant slices.
- Source references and source-confidence labels so inferred claims stay visible.
- Local structural validation and optional browser render checks.

The default design follows the same pattern used by BPMN-style swimlanes and
interactive visualization practice: overview first, focused views next, details
on node selection, and semantic colors/icons that support the flow rather than
drive the layout. The source-backed checklist lives in
`skills/visual-arch/references/design-principles.md`.

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

## Examples

The repo includes two deeper example documents that show the intended shape and
level of detail:

- `examples/keyboard-interrupt/visual-architecture.html` - what happens when a
  keyboard interrupt occurs, from Ctrl+C through terminal handling, SIGINT,
  runtime interruption, cleanup, shell status, and debugging.
- `examples/dns/visual-architecture.html` - how DNS works, from application
  lookup through local resolver policy, recursive resolution, authority
  traversal, DNSSEC, TTLs, caching, endpoint connection, and debugging.

Regenerate all examples with:

    python scripts/build_example.py

Validate generated documents with:

    python skills/visual-arch/scripts/validate_architecture_doc.py examples/dns/visual-architecture.html

## When To Use It

Use this skill for:

- Architecture maps for unfamiliar repos.
- Runtime flow explanations.
- Service, pipeline, or protocol walkthroughs.
- Debugging-oriented system maps.
- Source-backed onboarding docs.
- Interactive alternatives to large static diagrams.

It is especially useful when the important knowledge is spread across code,
configuration, tests, docs, workflows, and operational conventions.

## How It Works

The skill guides the agent through a structured architecture pass:

1. Identify the target, audience, and output path.
2. Inspect source files, docs, tests, workflows, and configuration.
3. Build a content model with domains, owners, nodes, edges, views, details, and source confidence.
4. Render that model into the bundled standalone React Flow HTML template.
5. Validate the generated document and optionally run browser render checks.

The default output path is `docs/visual-architecture.html` when a `docs/`
directory exists, otherwise `visual-architecture.html`.

## Trust And Runtime Notes

- The skill itself does not send project code anywhere.
- Agents using the skill inspect local project files to build the document.
- The bundled HTML template loads React, React DOM, and XYFlow from public CDNs.
- The validator scripts run locally.
- Generated documents should be reviewed before publishing when they include private paths, internal system names, or inferred architecture claims.

## Development

Maintainer notes live in `docs/maintainer-notes.md`.
