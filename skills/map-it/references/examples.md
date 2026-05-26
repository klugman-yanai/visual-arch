# Examples

Bundled examples demonstrate structure and verification expectations. They are not universal style mandates.

## DNS

- Path: `examples/dns/visual-architecture.html`.
- Mode: CDN-backed online.
- Purpose: protocol/topology explainer with recursive lookup, authority traversal, DNSSEC, caching, endpoint connection, and debugging.
- Use as a benchmark for rich interactive behavior and graph readability.
- Do not copy its palette or protocol vocabulary into unrelated projects.

## Keyboard Interrupt

- Path: `examples/keyboard-interrupt/visual-architecture.html`.
- Mode: pure offline HTML/CSS/JS.
- Purpose: OS/runtime lifecycle map showing Ctrl+C through terminal handling, signal delivery, runtime interruption, cleanup, shell status, and debugging.
- Use as a benchmark for no-dependency interaction.

## Service Topology

- Path: `examples/service-topology/visual-architecture.html`.
- Mode: CDN-backed online.
- Purpose: non-flow topology example with clients, APIs, service layer, storage, async workers, object storage, observability, and external identity.
- Use as proof that swimlanes are optional and the skill can model non-pipeline systems.

## Maintenance Rule

When examples improve, update their `model.json` and regenerate with:

```bash
python scripts/build_example.py
```

Then validate each generated document and run render checks where available. Treat generated HTML as an artifact, not the source of truth.
