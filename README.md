# visual-arch

Reusable agent skill for creating project-agnostic visual architecture documents.

## Install

Run the interactive installer and choose your agent/harness:

    npx skills add klugman-yanai/visual-arch

For a targeted non-interactive install:

    npx skills add klugman-yanai/visual-arch --skill visual-arch -a codex -a claude-code

## Use

    Use visual-arch to create an interactive visual architecture document for this project.

The skill uses specialized discovery, stack-selection, content, and verification passes to choose an appropriate architecture-document stack for each project. It includes standalone React Flow and Mermaid HTML templates plus a validator for generated documents.
