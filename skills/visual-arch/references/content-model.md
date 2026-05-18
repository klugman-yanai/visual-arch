# Content Model

Use this model as the intermediate artifact before generating HTML. It can live in scratch notes, a temp JSON file, or directly inside the template as `VISUAL_ARCH_DATA`.

Required top-level fields:

```json
{
  "domains": {},
  "owners": {},
  "board": {
    "layout": { "orientation": "vertical" },
    "lanes": [],
    "nodes": [],
    "edges": [],
    "views": {}
  },
  "groupDetails": {}
}
```

## Fields

`domains`: map of domain key to `{ "label": "...", "color": "#...", "soft": "#..." }`.

`owners`: map of owner key to `{ "label": "...", "description": "..." }`. Use functional ownership if people/teams are unknown, such as `runtime`, `build`, `storage`, `external`.

`layout`: optional board metadata. Prefer `{ "orientation": "vertical" }` for a modern sequence-diagram reading path across tall responsibility lanes unless the project or user asks for another shape.

`lanes`: large background columns/rows. Each lane needs `{ "id", "title", "domain", "x", "y", "width", "height" }`.

`nodes`: primary architecture elements. Each node needs:

```json
{
  "id": "stable-kebab-id",
  "title": "Short Node Title",
  "domain": "runtime",
  "owner": "runtime",
  "x": 120,
  "y": 240,
  "purpose": "One sentence shown on the card.",
  "details": {
    "summary": "What this does.",
    "inputs": ["Specific input, file, event, API, artifact"],
    "outputs": ["Specific output, file, event, API, artifact"],
    "why": "Why this exists in the system.",
    "failures": ["Where to check first when this breaks"],
    "source": ["path/to/file.ext", "inferred from path/to/config.yml"],
    "source_confidence": "source-backed",
    "related": ["other-node-id"]
  }
}
```

`edges`: directed contracts between nodes:

```json
{
  "id": "source-to-target",
  "source": "source-node-id",
  "target": "target-node-id",
  "label": "artifact/API/event",
  "kind": "control"
}
```

Use `kind` values consistently:

- `control`: orchestration, calls, task dispatch, lifecycle transitions.
- `data`: data movement, files, databases, object storage, streams.
- `signal`: status, checks, notifications, health, telemetry.
- `dependency`: build/runtime dependency or package relationship.

`views`: map of view key to `{ "label": "Overview", "focus": ["node-id"] }`. Include `overview`.

## Source Confidence

Every node and important claim must use one of:

- `source-backed`: direct evidence in source, config, tests, docs, workflows, or generated artifacts intentionally referenced.
- `inferred`: reasonable inference from evidence; visible text should say "inferred".
- `external`: external service, user, vendor, or manually operated system.
- `unknown`: visible gap where evidence is missing.

## Authoring Rules

- Include only claims supported by source or clearly marked inference.
- Prefer coarse nodes with strong details over many tiny nodes.
- Keep node titles under 30 characters when possible.
- Keep card `purpose` under 140 characters.
- Every node should have at least one source reference.
- Every node should have `details.source_confidence`.
- Every important edge should name the contract, not just "uses".
- Use coordinates that create a top-to-bottom reading path by default. Use left-to-right only when that better matches the user's goal or the system's shape.
- Keep external systems as nodes when they affect architecture.
- Exclude generated, vendored, cached, secret, and low-level utility files unless they define a real architecture contract.
