---
name: refresh-mcp-tools
description: |
  Use when you need to update the documentation with the latest available MCP tools in the environment.
---

# refresh-mcp-tools

## Overview
This skill automates the process of updating the project's documentation (`.ai/instructions.md`) to reflect the currently active Model Context Protocol (MCP) tools. It ensures that the AI agent is always aware of the tools available in the environment by querying the endpoint and injecting the list directly into the context file.


## Workflow / Instructions
1. **Execute Update**: Run the bundled script to fetch tools and update the documentation automatically.
   ```bash
   python3 skills/refresh-mcp-tools/scripts/update_tools_doc.py
   ```
2. **Verify**: Check the output for "Successfully updated .ai/instructions.md".


## Available Tools & Resources

### Scripts (`./scripts/`)
- `list_mcp_tools.py`: 通过环境变量提供的信息获取所有可用mcp server和mcp tools
- `update_tools_doc.py`: Orchestrates the fetching of MCP tools (via `list_mcp_tools.py`) and injection into `.ai/instructions.md`.

### References (`./references/`)
- No references currently. (Add documentation/schemas here to be loaded on-demand)

### Assets (`./assets/`)
- No assets currently. (Add output templates/files here)
