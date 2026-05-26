# map-it

Create interactive architecture maps for codebases, systems, services,
workflows, protocols, and technical products.

`map-it` turns a repo or system description into an evidence-labeled portable
HTML map with focused views, clickable nodes, detail panels, edge labels, source
references, and confidence labels.

## Install

```bash
npx skills add klugman-yanai/map-it
```

Target specific agents if needed:

```bash
npx skills add klugman-yanai/map-it --skill map-it -a codex -a claude-code
```

## Use

```text
Use $map-it to map this repo for a new maintainer.
```

```text
Use $map-it to explain how the authentication flow works.
```

```text
Use $map-it to create an architecture map for the build and release pipeline.
```

## What It Creates

- A portable `visual-architecture.html` file.
- Context-sensitive architecture structure: topology, flow, lifecycle, ownership, dependency map, or another fit.
- Focus views and clickable nodes with summaries, inputs, outputs, failure modes, and "why this exists" notes.
- Source references and confidence labels: `source-backed`, `inferred`, `external`, or `unknown`.
- Local validation scripts, optional render checks, and an evidence-audit checklist.

## Modes

- **Online**: CDN-backed HTML with React and XYFlow for richer graph interaction.
- **Offline**: pure HTML/CSS/JS with no CDN, bundled runtime libraries, or downloaded packages.
- **Integrated**: uses an existing docs/app stack when the project calls for it.

Trust levels:

- **Draft**: structural validation and stated assumptions.
- **Reviewable**: validation, render/browser check when available, and representative evidence audit.
- **Shareable**: validation, render/browser check, and audit of every `source-backed` node.

Agents using this skill must ask before downloading, installing, or prompting the
user to install dependencies such as Playwright, browser binaries, npm packages,
runtime libraries, or vendored assets.

## Examples

- `examples/keyboard-interrupt/visual-architecture.html` - pure offline map of Ctrl+C through terminal handling, signal delivery, runtime interruption, cleanup, and debugging.
- `examples/dns/visual-architecture.html` - online protocol map of DNS lookup, recursive resolution, authority traversal, DNSSEC, TTLs, caching, connection, and debugging.
- `examples/service-topology/visual-architecture.html` - online non-swimlane service topology with clients, API edge, service core, storage, async workers, external identity, and telemetry.

## Development

Regenerate examples:

```bash
python scripts/build_example.py
```

Run release checks:

```bash
python scripts/release_check.py
```

Run individual validation:

```bash
python skills/map-it/scripts/validate_architecture_doc.py examples/dns/visual-architecture.html --source-root examples/dns
```

Generate an evidence-audit checklist:

```bash
python skills/map-it/scripts/audit_claims.py examples/dns/visual-architecture.html --source-root examples/dns --output /tmp/dns-evidence-audit.md
```

Maintainer notes live in `docs/maintainer-notes.md`.
