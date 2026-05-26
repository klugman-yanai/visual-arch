# Content Model

Use this model as the intermediate artifact before generating HTML. It can live in scratch notes, a temp JSON file, or directly inside the template as `VISUAL_ARCH_DATA`.

Required top-level fields:

```json
{
  "domains": {},
  "owners": {},
  "board": {
    "lanes": [],
    "nodes": [],
    "edges": [],
    "edgeHandles": {},
    "views": {}
  },
  "groupDetails": {}
}
```

## Fields

`domains`: map of domain key to `{ "label": "...", "accent": "#...", "soft": "#..." }`.

`owners`: map of owner key to `{ "label": "...", "description": "..." }`. Use functional ownership if people/teams are unknown, such as `runtime`, `build`, `storage`, `external`.

`board.layout`: optional board metadata, such as `{ "orientation": "left-to-right", "design_basis": "service-topology" }` or `{ "orientation": "vertical", "design_basis": "process-flow" }`. Choose the orientation and design basis from the user prompt, repo evidence, and reader task.

`lanes`: optional large background columns/rows. Each lane needs `{ "id", "title", "domain", "position", "width", "height" }`. Use lanes when responsibility, lifecycle, geography, or ownership regions clarify the map. Omit lanes for topology, hierarchy, matrix, or compact dependency maps where columns would add visual noise.

`nodes`: primary architecture elements. Each node needs:

```json
{
  "id": "stable-kebab-id",
  "title": "Short Node Title",
  "domain": "runtime",
  "owner": "runtime",
  "position": { "x": 120, "y": 240 },
  "tier": "primary",
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

Optional node display fields:

- `step`: short sequence label such as `"01"`.
- `chips`: short tags. Use sparingly.
- `tier`: `"primary"`, `"support"`, or `"detail"`. `primary` is default.
- `hidden`: `true` for detail/satellite nodes that should stay out of the overview until details are enabled or a related node is selected.
- `revealFor`: array of node ids that should reveal this hidden/detail node when selected.

`edges`: directed contracts between nodes. The template expects compact arrays:

```json
["source-node-id", "target-node-id", "artifact/API/event", "control"]
```

`edgeHandles`: optional map of edge id (`source->target`) to `[sourceHandle, targetHandle]`. Use it for polished routing. Prefer `out-bottom` to `in-top` for vertical sequence steps, `out-right` to `in-left` for left-to-right handoffs, and `out-left` to `in-right` only for intentional reverse handoffs or return signals.

Use `kind` values consistently:

- `control`: orchestration, calls, task dispatch, lifecycle transitions.
- `artifact`: data movement, files, databases, object storage, streams, generated outputs.
- `signal`: status, checks, notifications, health, telemetry.
- `decision`: gate, policy branch, verdict, approval, or conditional path.
- `dependency`: build/runtime dependency or package relationship. Use only when dependency structure is the point of the view.

`data` is accepted as a compatibility alias for `artifact`, but prefer `artifact` in new models because the edge label should name the concrete contract.

`views`: map of view key to `{ "label": "Overview", "focus": ["node-id"] }`. Include `overview`. The overview focus should be the primary reading path, not a dump of every node. Focus views preserve the same coordinates and show or emphasize subsets; do not use them to create unrelated layouts.

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
- Every polished output should set edge handles or equivalent routing metadata for nontrivial layouts; do not leave the renderer to guess connector placement when edges would cross or wander.
- Use coordinates that create the clearest reading path for the target system. Top-to-bottom, left-to-right, clustered topology, lifecycle bands, matrix, and radial arrangements are all acceptable when they match the reader task.
- Use swimlanes for process flows that cross responsibilities only when they orient the reader without turning the board into a spreadsheet.
- Choose domain colors and labels for the target project. Do not reuse example palettes or labels unless they match the generated model.
- Keep overview nodes and edges sparse enough that the main flow can be traced without opening the drawer. Move supporting mechanics into focus views, hidden detail nodes, or the detail drawer.
- Hidden/detail nodes should never be required to understand the overview.
- Keep external systems as nodes when they affect architecture.
- Exclude generated, vendored, cached, secret, and low-level utility files unless they define a real architecture contract.
