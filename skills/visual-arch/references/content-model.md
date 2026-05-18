# Content Model

Use this model as the intermediate artifact before generating HTML. It can live in scratch notes, a temp JSON file, or directly inside the template as `ARCHITECTURE_MODEL`.

Required top-level fields:

```json
{
  "title": "Project Architecture",
  "subtitle": "Short boundary statement",
  "domains": {},
  "owners": {},
  "lanes": [],
  "nodes": [],
  "edges": [],
  "views": {}
}
```

## Fields

`domains`: map of domain key to `{ "label": "...", "color": "#...", "soft": "#..." }`.

`owners`: map of owner key to `{ "label": "...", "description": "..." }`. Use functional ownership if people/teams are unknown, such as `runtime`, `build`, `storage`, `external`.

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

## Authoring Rules

- Include only claims supported by source or clearly marked inference.
- Prefer coarse nodes with strong details over many tiny nodes.
- Keep node titles under 30 characters when possible.
- Keep card `purpose` under 140 characters.
- Every node should have at least one source reference.
- Every important edge should name the contract, not just "uses".
- Use coordinates that create a left-to-right or top-to-bottom reading path.
- Keep external systems as nodes when they affect architecture.
