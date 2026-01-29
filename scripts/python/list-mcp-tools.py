#!/usr/bin/env python3
"""
List MCP Tools Script
Reference implementation based on Plan B from original design docs.
Extracts 'mcpServers' configuration from VS Code mcp.json files.
"""

import json
import os
import platform
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Dict, List


def fetch_mcp_tools(url: str, headers: Dict[str, str] = None) -> List[Dict[str, Any]]:
    """
    Attempt to fetch the list of tools from an MCP server.
    Tries to establish an SSE connection first to discover the POST endpoint
    (MCP Standard), then sends the JSON-RPC 'tools/list' request.
    Falls back to direct POST if SSE handshake fails or isn't applicable.
    """
    if not url.startswith(("http://", "https://")):
        return []

    post_url = url
    sse_response = None

    # 1. Attempt SSE Handshake to find the correct POST endpoint
    # Many MCP servers require an active SSE session and provide a dynamic POST URL.
    try:
        sse_headers = {
            "Accept": "text/event-stream",
            "User-Agent": "mcp-tool-lister/1.0",
            "Cache-Control": "no-cache",
        }
        if headers:
            sse_headers.update(headers)

        # Short timeout for discovery
        req = urllib.request.Request(url, headers=sse_headers, method="GET")
        response = urllib.request.urlopen(req, timeout=3)

        content_type = response.getheader("Content-Type", "")
        if "text/event-stream" in content_type:
            sse_response = response
            # Read events to find "endpoint"
            found_endpoint = None
            current_event = None

            # Read first few lines (safeguard against infinite stream)
            for _ in range(50):
                line = response.readline()
                if not line:
                    break

                line_str = line.decode("utf-8").strip()
                if not line_str:
                    continue

                if line_str.startswith("event:"):
                    current_event = line_str.split(":", 1)[1].strip()
                elif line_str.startswith("data:") and current_event == "endpoint":
                    data = line_str.split(":", 1)[1].strip()
                    found_endpoint = data
                    break

            if found_endpoint:
                # Resolve relative URL against original base
                post_url = urllib.parse.urljoin(url, found_endpoint)
        else:
            # Not an SSE stream, close and assume direct POST
            response.close()

    except Exception:
        # If SSE handshake fails (e.g. 405 Method Not Allowed on GET),
        # it might be a direct POST endpoint. Ignore error and proceed.
        if sse_response:
            try:
                sse_response.close()
            except:
                pass
        sse_response = None

    # 2. Send JSON-RPC Request to valid endpoint
    # Strict payload as requested
    payload = {
        "jsonrpc": "2.0",
        "method": "tools/list",
        "id": 1,
    }

    data = json.dumps(payload).encode("utf-8")

    # Prepare headers
    req_headers = {
        "Content-Type": "application/json",
        "User-Agent": "mcp-tool-lister/1.0",
    }
    if headers:
        req_headers.update(headers)

    try:
        req = urllib.request.Request(
            post_url, data=data, headers=req_headers, method="POST"
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                resp_data = json.loads(response.read().decode("utf-8"))

                # Close SSE if we opened one, we don't need it anymore
                # (Note: In a real client, we'd keep it open, but for listing tools, this suffices)
                if sse_response:
                    sse_response.close()

                if "result" in resp_data and "tools" in resp_data["result"]:
                    return resp_data["result"]["tools"]
                if "error" in resp_data:
                    print(f"    [RPC Error] {resp_data['error']}", file=sys.stderr)
            else:
                print(f"    [HTTP Error] Status: {response.status}", file=sys.stderr)

    except urllib.error.URLError as e:
        print(f"    [Connection Error] {e}", file=sys.stderr)
        # Attempt to read error body if available (e.g. 400 Bad Request details)
        if hasattr(e, "read"):
            try:
                err_body = e.read().decode("utf-8")
                print(f"    [Server Message] {err_body}", file=sys.stderr)
            except:
                pass

    except Exception as e:
        print(f"    [Error] {e}", file=sys.stderr)

    finally:
        if sse_response:
            try:
                sse_response.close()
            except:
                pass

    return []


def expand_path_variables(value: str) -> str:
    """
    Expand VSCode-style variables like ${env:VAR} and ${userHome} in strings.
    """
    if not isinstance(value, str):
        return str(value)

    # 1. Handle ${userHome}
    if "${userHome}" in value:
        value = value.replace("${userHome}", str(Path.home()))

    # 2. Handle ${env:VARIABLE}
    # Pattern to match ${env:VAR_NAME}
    env_pattern = re.compile(r"\$\{env:([a-zA-Z_][a-zA-Z0-9_]*)\}")

    def replace_env(match):
        var_name = match.group(1)
        # Return env var value, or empty string if not set
        val = os.environ.get(var_name)
        if val is None:
            # Warn locally? Or just return empty?
            # For header auth, empty usually breaks it, but explicit warning is better.
            print(
                f"    [Warning] Environment variable '{var_name}' not found.",
                file=sys.stderr,
            )
            return ""
        return val

    return env_pattern.sub(replace_env, value)


def get_vscode_settings_paths() -> List[Path]:
    """
    Get potential paths for VS Code MCP configuration files.
    Priority:
    1. Workspace Config (.vscode/mcp.json)
    2. Remote Config (VS Code Server data)
    3. User Config (OS-specific standard User paths)
    """
    paths = []
    home = Path.home()

    # 1. Workspace Config (Highest Priority)
    paths.append(Path.cwd() / ".vscode" / "mcp.json")

    # 2. Remote Config (VS Code Server)
    # Check both standard and insiders servers
    # These are typically found on the remote machine when using VS Code Remote
    paths.append(home / ".vscode-server" / "data" / "User" / "mcp.json")
    paths.append(home / ".vscode-server-insiders" / "data" / "User" / "mcp.json")

    # 3. User Config (Local machine via standard paths)
    # For a purely remote script, these might not exist or might refer to the remote user's desktop config.
    system = platform.system()
    if system == "Windows":
        appdata = os.environ.get("APPDATA")
        if appdata:
            base = Path(appdata)
            paths.append(base / "Code" / "User" / "mcp.json")
            paths.append(base / "Code - Insiders" / "User" / "mcp.json")
    elif system == "Darwin":  # macOS
        base = home / "Library" / "Application Support"
        paths.append(base / "Code" / "User" / "mcp.json")
        paths.append(base / "Code - Insiders" / "User" / "mcp.json")
    else:  # Linux
        base = home / ".config"
        paths.append(base / "Code" / "User" / "mcp.json")
        paths.append(base / "Code - Insiders" / "User" / "mcp.json")
        paths.append(base / "Code - OSS" / "User" / "mcp.json")

    return paths


def load_mcp_servers() -> List[Dict[str, Any]]:
    """
    Scan all settings paths and aggregate unique MCP servers defined in 'copilot.mcpServers'.
    """
    mcp_servers = []
    seen_names = set()

    search_paths = get_vscode_settings_paths()
    print(
        f"Scanning for VS Code settings in {len(search_paths)} locations...",
        file=sys.stderr,
    )

    for p in search_paths:
        if p.exists():
            try:
                print(f"  Reading: {p}", file=sys.stderr)
                with open(p, "r", encoding="utf-8") as f:
                    # Allow comments in json (standard for vscode settings)
                    # Simple hack: remove lines starting with keys that might be comments?
                    # Actually standard json.load might fail on comments.
                    # For a robust script, we might need a comment-stripping parser.
                    # For now, try standard json load.
                    content = f.read()

                # Basic comment stripping (C-style //)
                # This is fragile but better than nothing for settings.json
                clean_content = "\n".join(
                    [
                        line
                        for line in content.splitlines()
                        if not line.strip().startswith("//")
                    ]
                )

                settings = json.loads(clean_content)

                current_file_servers = []

                # Handle mcp.json format
                # Supports both "mcpServers" (standard) and "servers" (legacy/variant) keys
                mcp_servers_dict = settings.get("mcpServers", {})
                if not mcp_servers_dict:
                    mcp_servers_dict = settings.get("servers", {})

                if isinstance(mcp_servers_dict, dict):
                    for name, config in mcp_servers_dict.items():
                        server_entry = config.copy()
                        server_entry["name"] = name
                        current_file_servers.append(server_entry)

                if not isinstance(current_file_servers, list):
                    print(
                        f"  [Info] No valid server list found in {p}", file=sys.stderr
                    )
                    continue

                for server in current_file_servers:
                    name = server.get("name")
                    if name and name not in seen_names:
                        seen_names.add(name)
                        server["_source"] = str(p)  # metadata
                        mcp_servers.append(server)

            except json.JSONDecodeError as e:
                print(f"  [Warning] Failed to parse JSON in {p}: {e}", file=sys.stderr)
            except Exception as e:
                print(f"  [Warning] Error reading {p}: {e}", file=sys.stderr)

    return mcp_servers


def main():
    servers = load_mcp_servers()

    # Enrich servers with tools
    print("\nFetching tools from available servers...", file=sys.stderr)
    for server in servers:
        # Check if server matches criteria for extraction (http/sse)
        # Note: "type" is optional in some contexts but usually present.
        srv_type = server.get("type", "unknown")
        srv_url = server.get("url")

        if srv_url and srv_type in (
            "http",
            "sse",
        ):  # Assuming 'http' type uses JSON-RPC over HTTP
            print(
                f"  Probing {server.get('name', 'unnamed')} ({srv_url})...",
                file=sys.stderr,
            )
            # Some entries might have 'headers' config
            # Extract extra headers if present in config (e.g. auth)
            headers = {}
            config_headers = server.get("headers")
            if isinstance(config_headers, dict):
                for k, v in config_headers.items():
                    # Expand variables in values (e.g. ${env:MCP_TOKEN})
                    headers[k] = expand_path_variables(str(v))

            tools = fetch_mcp_tools(srv_url, headers)
            if tools is not None:
                server["tools"] = tools
                server["tools_count"] = len(tools)
                print(f"    -> Found {len(tools)} tools", file=sys.stderr)
            else:
                print("    -> No tools retrieved", file=sys.stderr)

        elif srv_type == "stdio":
            print(
                f"  Skipping stdio server {server.get('name', 'unnamed')}: Cannot list tools via script",
                file=sys.stderr,
            )

    output = {
        "timestamp": __import__("datetime").datetime.now().isoformat(),
        "count": len(servers),
        "servers": servers,
        "note": "This list represents configured MCP servers. 'tools' field populated for HTTP servers if reachable.",
    }

    # Print formatted JSON to stdout
    print(json.dumps(output, indent=2, ensure_ascii=False))

    if not servers:
        print(
            "\nNo MCP servers found in standard VS Code configuration paths.",
            file=sys.stderr,
        )
        print(
            "Ensure you have configured 'copilot.mcpServers' in your settings.json.",
            file=sys.stderr,
        )


if __name__ == "__main__":
    main()
