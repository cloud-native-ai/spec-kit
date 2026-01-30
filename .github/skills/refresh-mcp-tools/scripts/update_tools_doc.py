#!/usr/bin/env python3
"""
Update Tools Doc Script
Updates the ## Tools section in .ai/instructions.md with the output from list_mcp_tools.py.
"""

import subprocess
import sys
from pathlib import Path


def update_instructions():
    # 1. Run list_mcp_tools.py to get JSON output
    # list_mcp_tools.py is in the same directory as this script
    current_dir = Path(__file__).resolve().parent
    # Calculate repo root: scripts -> refresh-mcp-tools -> skills -> spec-kit
    repo_root = current_dir.parent.parent.parent
    lister_script = current_dir / "list_mcp_tools.py"
    target_file = repo_root / ".ai/instructions.md"

    if not lister_script.exists():
        print(f"Error: Could not find {lister_script}")
        sys.exit(1)

    if not target_file.exists():
        print(f"Error: Could not find {target_file}")
        sys.exit(1)

    print(f"Fetching tools from {lister_script}...")
    try:
        # We might want to pass arguments or headers if needed, but for now simple execution
        result = subprocess.run(
            [sys.executable, str(lister_script), "--markdown"],
            capture_output=True,
            text=True,
            check=True,
        )
        tools_markdown = result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running list_mcp_tools.py: {e.stderr}")
        sys.exit(1)

    # 2. Read target file
    content = target_file.read_text(encoding="utf-8")

    # 3. Find markers
    marker = "<!-- TOOLS_PLACEHOLDER -->"
    start_idx = content.find(marker)

    if start_idx == -1:
        print(f"Error: Marker '{marker}' not found in {target_file}")
        sys.exit(1)

    # Calculate insertion point (after marker)
    insert_pos = start_idx + len(marker)

    # Find next section header to determine end of replacement zone
    # We look for the next "## " starting on a new line after the insertion point
    next_section_match = -1
    search_start = insert_pos

    # Simple search for next H2
    import re

    # Look for ^## followed by space, multiline mode
    match = re.search(r"^##\s", content[search_start:], re.MULTILINE)

    if match:
        end_idx = search_start + match.start()
        # Keep the next section header
        new_content = (
            content[:insert_pos]
            + "\n\n"
            + tools_markdown.strip()
            + "\n\n"
            + content[end_idx:]
        )
    else:
        # No following section, just append
        new_content = content[:insert_pos] + "\n\n" + tools_markdown.strip() + "\n"

    # 4. Write back
    target_file.write_text(new_content, encoding="utf-8")
    print(f"Successfully updated {target_file}")


if __name__ == "__main__":
    update_instructions()
