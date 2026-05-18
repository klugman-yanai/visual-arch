# visual-arch

Reusable agent skill for creating project-agnostic visual architecture documents.

## Install

Run the interactive installer and choose your agent/harness:

    npx skills add klugman-yanai/visual-arch

For a targeted non-interactive install:

    npx skills add klugman-yanai/visual-arch --skill visual-arch -a codex -a claude-code

## Use

    First explore the project, then use $visual-arch to create an interactive visual architecture document for this project.

The skill uses specialized discovery, stack-selection, content, and verification passes to create a source-backed architecture document. React Flow is the primary bundled template for rich interactive maps. Mermaid is included only for constrained cases where the user explicitly wants a text-native, Markdown-adjacent, or no-React document.
