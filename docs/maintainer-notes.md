# Maintainer Notes

## Generated Examples

The examples are generated from:

- `skills/map-it/assets/visual-architecture-template.html`
- `skills/map-it/assets/visual-architecture-offline-template.html`
- `examples/*/model.json`

Regenerate all examples with:

    python scripts/build_example.py

Validate generated documents with:

    python skills/map-it/scripts/validate_architecture_doc.py examples/keyboard-interrupt/visual-architecture.html --source-root examples/keyboard-interrupt
    python skills/map-it/scripts/validate_architecture_doc.py examples/dns/visual-architecture.html --source-root examples/dns
    python skills/map-it/scripts/validate_architecture_doc.py examples/service-topology/visual-architecture.html --source-root examples/service-topology

Generate evidence-audit checklists with:

    python skills/map-it/scripts/audit_claims.py examples/dns/visual-architecture.html --source-root examples/dns --output /tmp/dns-evidence-audit.md

Run the local release checks with:

    python scripts/release_check.py

`scripts/build_example.py` does not download dependencies. If example maintenance
needs local runtime assets, prepare them explicitly before running the builder.
Future offline examples should use pure HTML/CSS/JS rather than inlined React,
XYFlow, or other bundled runtime libraries.

Keep `examples/service-topology` as a no-lane topology regression case so the
skill continues to demonstrate project-agnostic structures beyond process flows.

## Design Benchmark

This skill is based on the evolving production document at
`kardome-bmt-suite/docs/visual-architecture.html` and shipped single-file
interactive HTML examples. Use those artifacts as quality benchmarks, not
templates to copy wholesale: clear hierarchy, non-duplicative controls,
deliberate edge handles, focused views, polished detail panels, useful
loading/fallback states, and a first viewport that feels like a usable
architecture tool rather than a generic diagram.

Keep the public skill project-agnostic. Do not copy Kardome-specific names into
the skill description or example model unless they are only mentioned here as
maintainer context. Example palettes, swimlanes, dark mode, node shapes, and BMT
vocabulary are not mandatory for unrelated projects.
