#!/usr/bin/env python3
"""List MCP servers and tools using cws_ai.mcp utilities."""

import dataclasses
import json
import os
import sys
from datetime import datetime
from typing import Dict, List

from cws_ai.mcp import get_all_mcp_servers, get_all_tools


def _group_tools_by_server() -> Dict[str, List[dict]]:
    tools = get_all_tools()
    tools_by_server: Dict[str, List[dict]] = {}
    for tool in tools:
        tools_by_server.setdefault(tool.server_name, []).append(
            dataclasses.asdict(tool)
        )
    return tools_by_server


def get_mcp_payload() -> dict:
    """Build MCP server/tool payload."""
    servers = get_all_mcp_servers()
    tools_by_server = _group_tools_by_server()

    servers_payload = []
    for server in servers:
        server_data = dataclasses.asdict(server)
        server_tools = tools_by_server.get(server.name, [])
        server_data["tools"] = server_tools
        server_data["tools_count"] = len(server_tools)
        servers_payload.append(server_data)

    return {
        "timestamp": datetime.now().isoformat(),
        "count": len(servers_payload),
        "servers": servers_payload,
        "note": "This list represents configured MCP servers. 'tools' field populated for HTTP servers if reachable.",
    }


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="List MCP servers and tools")
    parser.parse_args()

    # Preserve previous behavior: require MCP_AUTH when present in environment
    if not os.environ.get("MCP_AUTH"):
        print("[Error] MCP_AUTH environment variable is not set.", file=sys.stderr)
        return 1

    output = get_mcp_payload()
    print(json.dumps(output, indent=2, ensure_ascii=False))

    if not output.get("servers"):
        print(
            "\nNo MCP servers found in standard VS Code configuration paths.",
            file=sys.stderr,
        )
        print(
            "Ensure you have configured 'copilot.mcpServers' in your settings.json.",
            file=sys.stderr,
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
