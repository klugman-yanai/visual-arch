# Research-Backed Design Principles

Load this when choosing layout, interaction, or visual hierarchy for a generated architecture document.

## Source-Backed Direction

- **Use swimlanes only when the project is a process flow across responsibilities.** BPMN uses pools and lanes to organize process participants and responsibilities, and IBM's BPMN guidance frames swimlanes as a way to show who does what in a process. For architecture documents, choose the map structure from the reader's task and the repository evidence: topology, lifecycle, ownership, dependency, capability, journey, and process-flow maps are all valid.
- **Use overview, focus/filter, details on demand.** Shneiderman's visual-information mantra is still the right interaction model for complex diagrams: overview first, then filtering/zooming, then detail when requested. The default view should not expose every supporting node or edge.
- **Make relationships and contracts explicit.** Microsoft Azure architecture diagram guidance emphasizes diagrams as a way to communicate components, relationships, and design decisions. Edge labels should name contracts such as API, artifact, event, queue, file, status, handoff, or storage path.
- **Use color as semantic support, not layout.** IBM data visualization guidance treats color as a way to encode meaning and aid comparison, not as decoration. Domains/colors should help readers scan after the structure is already clear.
- **Put notation in the diagram, not only in prose.** C4 notation guidance recommends clear labels, notation keys, and metadata. Use concise node labels, a quiet legend only when it clarifies edge/domain semantics, and visible source-confidence labels in details.
- **Route connectors deliberately.** FigJam connector guidance and common technical-diagram practice treat connector shape and attachment as part of readability. Choose handles and paths so the main process path is easy to follow and crossings are intentional.
- **Interactive diagrams should reduce duplication, not create a puzzle.** The interactive software-documentation literature argues for one navigable model that supports multiple reader queries. Focus views should preserve spatial memory and filter/highlight the same map instead of re-laying it into unrelated shapes.

## Design Defaults

- Default layout: the clearest architecture map for the target project, with a stable reading path and explicit grouping only where it clarifies comprehension.
- Lanes are optional broad responsibility regions, not a rigid grid. Use them only when columns clarify ownership, lifecycle stage, or handoff; otherwise use clustering, topology, hierarchy, timeline, or focus-filtered graph structure.
- First viewport: title, view controls, primary map, and enough grouping context to orient the reader. Avoid splash/landing pages.
- Overview view: primary happy path plus a small number of essential branches. Target 8-18 primary nodes; hide or dim supporting mechanics until focus/selection/details.
- Focus views: same coordinates, filtered/highlighted subsets. Do not re-layout the system when switching views.
- Details: use the drawer for explanation, sources, failures, and "why this exists"; use optional hidden/detail nodes only when they clarify selected context.
- Edges: solid high-contrast control flow; quieter dashed artifact/data/dependency flow; distinct signal/reporting/status flow. Labels should be short and contract-specific.
- Legend: compact and outside the main reading path. Remove it if labels and details already explain the notation.
- Icons: secondary orientation aids. Do not make icon zones or domain color bands the primary navigation system.
- Controls: each visible control should do one distinct thing. Remove duplicate viewport/actions such as separate "fit all" and "reset view" buttons when they lead to the same state.

## When To Use Another Structure

Use a non-swimlane layout when the reader's core task is not process comprehension:

- topology or dependency graph: force-directed or clustered graph may be better.
- ownership matrix or capability comparison: matrix/table may be better.
- hierarchy/package tree: tree or nested containment may be better.
- timeline-only story: timeline may be better.

Write the chosen structure and its reason into the working summary, and keep overview/focus/details interactions.

## Layout Review Checklist

- Can a new maintainer trace the main flow without opening the drawer?
- Are responsibility changes visible without making the layout look like a spreadsheet?
- Are secondary edges quieter than the main process path?
- Does selecting a node reveal direct upstream/downstream context without moving the map unexpectedly?
- Do focus views preserve spatial memory?
- Are colors, icons, and legends useful but subordinate to node order and edge contracts?
- Are claims source-backed or visibly marked as inferred, external, or unknown?

## References

- OMG BPMN: https://www.omg.org/bpmn/
- IBM BPMN overview: https://www.ibm.com/think/topics/bpmn
- Microsoft Azure architecture diagrams: https://learn.microsoft.com/en-us/azure/well-architected/architect-role/design-diagrams
- Shneiderman, information visualization mantra: https://www.cs.umd.edu/~ben/about.html
- IBM data visualization basics: https://www.ibm.com/design/language/data-visualization/design/basics
- IBM technical diagrams: https://www.ibm.com/design/language/infographics/technical-diagrams/design/
- Figma FigJam connectors: https://help.figma.com/hc/en-us/articles/1500004414542-Create-diagrams-and-flows-with-connectors-in-FigJam
- C4 notation guidance: https://c4model.com/diagrams/notation
- Interactive diagrams for software documentation: https://arxiv.org/abs/2407.21621
