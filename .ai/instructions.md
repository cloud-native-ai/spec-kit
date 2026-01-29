# Spec Kit Project Instructions

## 1. Project Overview
Spec Kit is an extensible CLI tool designed to help developers adopt Specification-Driven Development (SDD) practices. It facilitates updating documentation, managing features through a constitution and feature index, and generating new plans and specs using AI agents.

## 2. Documentation Map
The following table maps key project concepts to their definitive source of truth in the repository. **Always read the relevant file before implementing changes.**

| Concept              | Source File(s)               | Purpose                                                                 |
| :------------------- | :--------------------------- | :---------------------------------------------------------------------- |
| **Constitution**     | `memory/constitution.md`    | Core principles, critical rules, and forbidden patterns.                 |
| **Feature Index**    | `memory/feature-index.md`   | Registry of all implemented features and their status.                   |
| **Development**      | `CONTRIBUTING.md`            | Setup, testing, and pull request guidelines.                             |
| **Architecture**     | `docs/index.md`              | High-level architecture and design documentation (in `docs/`).           |
| **Core Workflow**    | `spec-driven.md`             | Explanation of the SDD workflow (spec -> plan -> task).                  |
| **CLI Commands**     | `src/specify_cli/`           | Source code for the CLI implementation.                                  |
| **Prompt Templates** | `templates/`                 | Markdown templates used by the CLI (instructions, specs, plans).         |

## 3. Technology Stack
*   **Language**: Python 3.11+
*   **Package Manager**: uv
*   **CLI Framework**: Typer
*   **UI Library**: Rich
*   **HTTP Client**: httpx

## 4. Tool Selection Strategy
*   **Listing Files**: Use `ls -R` or `find` to explore structure.
*   **Reading Files**: Use `read_file` for specific content. 
*   **Search**: Use `grep_search` to find code usages or text patterns.
*   **Terminal**: Use `run_in_terminal` for git operations, file moves, and running the `specify` CLI.

## Tools
<!-- TOOLS_PLACEHOLDER -->

## Skills
<!-- SKILLS_PLACEHOLDER -->
