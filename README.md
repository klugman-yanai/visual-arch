# visual-arch

Reusable agent skill for creating project-agnostic visual architecture documents.

## Install

Install for Codex and Claude Code:

    npx skills add klugman-yanai/visual-arch --skill visual-arch -a codex -a claude-code

Install globally for all supported agents interactively:

    npx skills add klugman-yanai/visual-arch --skill visual-arch -g

## Use

    Use visual-arch to create an interactive visual architecture document for this project.

The skill uses specialized discovery, stack-selection, content, and verification passes to choose an appropriate architecture-document stack for each project. It includes standalone React Flow and Mermaid HTML templates plus a validator for generated documents.
