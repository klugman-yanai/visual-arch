# Maintainer Notes

## Generated Examples

The examples are generated from:

- `skills/visual-arch/assets/visual-architecture-template.html`
- `examples/*/model.json`

Regenerate all examples with:

    python scripts/build_example.py

Validate generated documents with:

    python skills/visual-arch/scripts/validate_architecture_doc.py examples/keyboard-interrupt/visual-architecture.html
    python skills/visual-arch/scripts/validate_architecture_doc.py examples/dns/visual-architecture.html

## Design Benchmark

This skill is based on the evolving production document at
`kardome-bmt-suite/docs/visual-architecture.html`. When maintaining this repo,
compare the template and examples against that document's current design
language: grouped lanes, clean tracks, deliberate edge handles, polished detail
panels, and a first viewport that feels like a usable architecture tool rather
than a generic diagram.

Keep the public skill project-agnostic. Do not copy Kardome-specific names into
the skill description or example model unless they are only mentioned here as
maintainer context.
