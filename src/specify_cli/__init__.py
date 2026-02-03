#!/usr/bin/env python3

"""
Specify CLI - Setup tool for Specify projects

Usage:
    uvx specify-cli.py init <project-name>
    uvx specify-cli.py init .
    uvx specify-cli.py init --here

Or install globally:
    uv tool install --from specify-cli.py specify-cli
    specify init <project-name>
    specify init .
    specify init --here
"""

import json
import os
import re
import shlex
import shutil
import ssl
import subprocess
import sys

# Check Python version
if sys.version_info < (3, 8):
    sys.exit("Error: Specify CLI requires Python 3.8 or higher.")

# For cross-platform keyboard input
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

import httpx
# For cross-platform keyboard input
import readchar
import typer
from rich.align import Align
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.tree import Tree
from typer.core import TyperGroup

try:
    import truststore

    ssl_context = truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
except (ImportError, AttributeError):
    ssl_context = ssl.create_default_context()

client = httpx.Client(verify=ssl_context)

# Get the directory where this module is located
MODULE_DIR = Path(__file__).parent.resolve()


# Agent configuration with name, folder, install URL, and CLI tool requirement
AGENT_CONFIG = {
    "copilot": {
        "name": "GitHub Copilot",
        "folder": ".github/",
        "install_url": None,  # IDE-based, no CLI check needed
        "requires_cli": False,
    },
    "qwen": {
        "name": "Qwen Code",
        "folder": ".qwen/",
        "install_url": "https://github.com/QwenLM/qwen-code",
        "requires_cli": True,
    },
    "opencode": {
        "name": "opencode",
        "folder": ".opencode/",
        "install_url": "https://opencode.ai",
        "requires_cli": True,
    },
}

SCRIPT_TYPE_CHOICES = {"sh": "POSIX Shell (bash/zsh)"}


BANNER = """
███████╗██████╗ ███████╗ ██████╗██╗███████╗██╗   ██╗
██╔════╝██╔══██╗██╔════╝██╔════╝██║██╔════╝╚██╗ ██╔╝
███████╗██████╔╝█████╗  ██║     ██║█████╗   ╚████╔╝ 
╚════██║██╔═══╝ ██╔══╝  ██║     ██║██╔══╝    ╚██╔╝  
███████║██║     ███████╗╚██████╗██║██║        ██║   
╚══════╝╚═╝     ╚══════╝ ╚═════╝╚═╝╚═╝        ╚═╝   
"""

TAGLINE = "GitHub Spec Kit - Spec-Driven Development Toolkit"


class StepTracker:
    """Track and render hierarchical steps without emojis, similar to tree output.
    Supports live auto-refresh via an attached refresh callback.
    """

    def __init__(self, title: str):
        self.title = title
        self.steps = []  # list of dicts: {key, label, status, detail}
        self.status_order = {
            "pending": 0,
            "running": 1,
            "done": 2,
            "error": 3,
            "skipped": 4,
        }
        self._refresh_cb = None  # callable to trigger UI refresh

    def attach_refresh(self, cb):
        self._refresh_cb = cb

    def add(self, key: str, label: str):
        if key not in [s["key"] for s in self.steps]:
            self.steps.append(
                {"key": key, "label": label, "status": "pending", "detail": ""}
            )
            self._maybe_refresh()

    def start(self, key: str, detail: str = ""):
        self._update(key, status="running", detail=detail)

    def complete(self, key: str, detail: str = ""):
        self._update(key, status="done", detail=detail)

    def error(self, key: str, detail: str = ""):
        self._update(key, status="error", detail=detail)

    def skip(self, key: str, detail: str = ""):
        self._update(key, status="skipped", detail=detail)

    def _update(self, key: str, status: str, detail: str):
        for s in self.steps:
            if s["key"] == key:
                s["status"] = status
                if detail:
                    s["detail"] = detail
                self._maybe_refresh()
                return

        self.steps.append(
            {"key": key, "label": key, "status": status, "detail": detail}
        )
        self._maybe_refresh()

    def _maybe_refresh(self):
        if self._refresh_cb:
            try:
                self._refresh_cb()
            except Exception:
                pass

    def render(self):
        tree = Tree(f"[cyan]{self.title}[/cyan]", guide_style="grey50")
        for step in self.steps:
            label = step["label"]
            detail_text = step["detail"].strip() if step["detail"] else ""

            status = step["status"]
            if status == "done":
                symbol = "[green]●[/green]"
            elif status == "pending":
                symbol = "[green dim]○[/green dim]"
            elif status == "running":
                symbol = "[cyan]○[/cyan]"
            elif status == "error":
                symbol = "[red]●[/red]"
            elif status == "skipped":
                symbol = "[yellow]○[/yellow]"
            else:
                symbol = " "

            if status == "pending":
                # Entire line light gray (pending)
                if detail_text:
                    line = (
                        f"{symbol} [bright_black]{label} ({detail_text})[/bright_black]"
                    )
                else:
                    line = f"{symbol} [bright_black]{label}[/bright_black]"
            else:
                # Label white, detail (if any) light gray in parentheses
                if detail_text:
                    line = f"{symbol} [white]{label}[/white] [bright_black]({detail_text})[/bright_black]"
                else:
                    line = f"{symbol} [white]{label}[/white]"

            tree.add(line)
        return tree


def get_resource_path() -> Optional[Path]:
    """
    Get the path containing templates/memory/scripts.
    Checks MODULE_DIR first (installed package), then repo root (local dev).
    """
    # Check installed package location
    if (MODULE_DIR / "templates").exists():
        return MODULE_DIR

    # Check repo root (assuming src/specify_cli structure)
    repo_root = MODULE_DIR.parent.parent
    if (repo_root / "templates").exists():
        return repo_root

    return None


def has_local_templates() -> bool:
    """Check if local templates are available."""
    return get_resource_path() is not None


def rewrite_paths(content: str) -> str:
    """Rewrite paths in content to use .specify/ prefix."""
    import re

    # Only rewrite paths that don't already start with .specify/
    # Use negative lookbehind to ensure we don't match paths that already have .specify/
    content = re.sub(r"(?<!\.specify/)memory/", r".specify/memory/", content)
    content = re.sub(r"(?<!\.specify/)scripts/", r".specify/scripts/", content)
    content = re.sub(r"(?<!\.specify/)templates/", r".specify/templates/", content)
    return content


def generate_commands(
    agent: str, ext: str, arg_format: str, output_dir: Path, script_variant: str
) -> None:
    """Generate command files from templates for the specified agent."""
    output_dir.mkdir(parents=True, exist_ok=True)

    resource_path = get_resource_path()
    if not resource_path:
        return

    commands_dir = resource_path / "templates" / "commands"
    if not commands_dir.exists():
        return

    for template_file in commands_dir.glob("*.md"):
        if not template_file.is_file():
            continue

        name = template_file.stem

        # Read template content
        with open(template_file, "r", encoding="utf-8") as f:
            file_content = f.read()

        # Normalize line endings
        file_content = file_content.replace("\r\n", "\n").replace("\r", "\n")

        # Extract description from YAML frontmatter
        import re

        description_match = re.search(
            r'description:\s*["\']?([^"\']+)["\']?', file_content
        )
        description = (
            description_match.group(1) if description_match else f"Command for {name}"
        )

        # Extract script command for the script variant
        script_match = re.search(
            rf"^\s*{script_variant}:\s*\|\s*$", file_content, re.MULTILINE
        )
        if script_match:
            # Multi-line block starting after the `sh: |` line until the next dedented key or frontmatter end
            lines = file_content.split("\n")
            start_idx: Optional[int] = None
            indent_prefix = ""
            for i, line in enumerate(lines):
                if re.match(rf"^\s*{script_variant}:\s*\|\s*$", line):
                    start_idx = i + 1
                    if start_idx < len(lines):
                        indent_match = re.match(r"^(\s+)", lines[start_idx])
                        indent_prefix = (
                            indent_match.group(1) if indent_match else "    "
                        )
                    break

            block_lines: List[str] = []
            if start_idx is not None:
                for j in range(start_idx, len(lines)):
                    ln = lines[j]
                    # Stop when we reach a new top-level/frontmatter key
                    if ln.strip().startswith(
                        (
                            "description:",
                            "scripts:",
                            "agent_scripts:",
                            "handoffs:",
                            "---",
                        )
                    ) and not ln.startswith(indent_prefix):
                        break
                    # Only strip the leading indent corresponding to the block
                    if indent_prefix and ln.startswith(indent_prefix):
                        block_lines.append(ln[len(indent_prefix) :])
                    else:
                        block_lines.append(ln)

            script_command = (
                "\n```bash\n" + "\n".join(block_lines).rstrip("\n") + "\n```\n"
                if block_lines
                else "(Missing script command)"
            )
        else:
            # Fallback: single-line form like `sh: some-command {ARGS}`
            single_line_match = re.search(
                rf"^\s*{script_variant}:\s*(.+)$", file_content, re.MULTILINE
            )
            script_command = (
                single_line_match.group(1).strip()
                if single_line_match
                else "(Missing script command)"
            )

        # Replace {ARGS} placeholder in script command
        script_command = script_command.replace("{ARGS}", arg_format)

        # Remove scripts: and agent_scripts: sections from frontmatter
        # This is complex, so we'll keep the original frontmatter but remove those sections
        lines = file_content.split("\n")
        new_lines = []
        in_frontmatter = False
        skip_scripts_section = False

        for line in lines:
            if line.strip() == "---":
                new_lines.append(line)
                in_frontmatter = not in_frontmatter
                continue

            if in_frontmatter:
                if line.strip().startswith("scripts:") or line.strip().startswith(
                    "agent_scripts:"
                ):
                    skip_scripts_section = True
                    continue
                if skip_scripts_section and line.strip() and not line.startswith(" "):
                    skip_scripts_section = False

                if skip_scripts_section:
                    continue

            new_lines.append(line)

        # Reconstruct content without scripts sections
        cleaned_content = "\n".join(new_lines)

        # Extract body (everything after the frontmatter)
        body_parts = cleaned_content.split("---")
        if len(body_parts) >= 3:
            body = "---".join(body_parts[2:]).strip()
        else:
            body = cleaned_content.strip()

        # Replace placeholders in the final body
        body = body.replace("{SCRIPT}", script_command)
        body = body.replace("__AGENT__", agent)

        # Apply path rewrites
        body = rewrite_paths(body)

        # Write the command file based on format
        output_path = output_dir / f"speckit.{name}.{ext}"
        if ext == "toml":
            toml_content = (
                f'description = "{description}"\n\n'
                + 'prompt = """\n'
                + body
                + '\n"""\n'
            )
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(toml_content)
        else:
            # For "prompt.md" and "md" just write the body
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(body)


def strip_comments(text: str) -> str:
    """Removes C-style comments (// and /* */) from text."""

    def replacer(match):
        s = match.group(0)
        if s.startswith("/"):
            return " "
        else:
            return s

    pattern = re.compile(
        r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
        re.DOTALL | re.MULTILINE,
    )
    return re.sub(pattern, replacer, text)


def detect_tech_stack(root_dir: Path) -> Set[str]:
    stack = set()
    # Java
    if (root_dir / "pom.xml").exists() or (root_dir / "build.gradle").exists():
        stack.add("java")

    # Python
    if (
        (root_dir / "pyproject.toml").exists()
        or (root_dir / "requirements.txt").exists()
        or (root_dir / "setup.py").exists()
    ):
        stack.add("python")

    # Node/JS/TS
    if (root_dir / "package.json").exists():
        stack.add("javascript")
        if (root_dir / "tsconfig.json").exists():
            stack.add("typescript")

    return stack


def configure_vscode_settings(
    project_path: Path, tracker: Optional[StepTracker] = None
) -> None:
    """Generate VS Code settings based on project context."""
    template_path = project_path / ".specify" / "templates" / "vscode-settings.json"
    output_path = project_path / ".vscode" / "settings.json"

    if not template_path.exists():
        # Try using existing settings file as template
        if output_path.exists():
            template_path = output_path
        # Fallback to source template if not found in project (e.g. during local dev copy)
        elif (resource_path := get_resource_path()) and (
            resource_path / "templates" / "vscode-settings.json"
        ).exists():
            template_path = resource_path / "templates" / "vscode-settings.json"
        else:
            return

    if tracker:
        tracker.start("vscode-settings", "Configuring VS Code settings")

    try:
        # Load template
        with open(template_path, "r", encoding="utf-8") as f:
            content = f.read()
            json_content = strip_comments(content)
            settings = json.loads(json_content)

        # Analyze context
        stack = detect_tech_stack(project_path)

        # Apply settings
        if "java" in stack:
            settings.setdefault(
                "java.configuration.updateBuildConfiguration", "automatic"
            )
            settings.setdefault(
                "java.format.settings.url", ".vscode/java-formatter.xml"
            )

        if "python" in stack:
            settings.setdefault("python.analysis.typeCheckingMode", "basic")
            settings.setdefault("python.formatting.provider", "black")

        if "typescript" in stack or "javascript" in stack:
            settings.setdefault("editor.defaultFormatter", "esbenp.prettier-vscode")

        # Ensure .vscode exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Write output
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=2, ensure_ascii=False)

        if tracker:
            tracker.complete(
                "vscode-settings",
                f"Updated for {', '.join(stack) if stack else 'generic'}",
            )

    except Exception as e:
        if tracker:
            tracker.error("vscode-settings", str(e))
        else:
            console.print(f"[red]Error configuring VS Code settings:[/red] {e}")


def copy_local_templates(
    project_path: Path,
    ai_assistant: str,
    script_type: str,
    is_current_dir: bool = False,
    tracker: Optional[StepTracker] = None,
) -> Path:
    """Copy local templates to create a new project.
    Returns project_path.
    """
    resource_path = get_resource_path()
    if not resource_path:
        raise RuntimeError("Local templates not found")

    if tracker:
        tracker.add("local-templates", "Using local templates")
        tracker.start("local-templates", "checking template structure")

    # Create project directory only if not using current directory
    if not is_current_dir:
        project_path.mkdir(parents=True)

    try:
        # Create the .specify directory structure that the original template expects
        specify_dir = project_path / ".specify"
        specify_dir.mkdir(exist_ok=True)

        # Copy memory directory
        if (resource_path / "memory").exists():
            memory_src = resource_path / "memory"
            memory_dest = specify_dir / "memory"
            memory_dest.mkdir(exist_ok=True)

            # Specific files to handle
            memory_files = ["constitution.md", "features.md"]

            for filename in memory_files:
                src_file = memory_src / filename
                dest_file = memory_dest / filename

                if src_file.exists():
                    if tracker:
                        tracker.start("local-templates", f"copying {filename}")

                    # Check if destination file already exists
                    if dest_file.exists():
                        console.print(
                            f"[yellow]Memory file {filename} already exists - skipping copy to preserve existing content[/yellow]"
                        )
                    else:
                        # Copy the file
                        shutil.copy2(src_file, dest_file)
                        if tracker:
                            tracker.complete("local-templates", f"{filename} copied")
                else:
                    if tracker:
                        tracker.skip(
                            "local-templates", f"{filename} not found in source"
                        )

        # Copy scripts directory
        if (resource_path / "scripts").exists():
            if tracker:
                tracker.start("local-templates", "copying scripts")
            shutil.copytree(
                resource_path / "scripts",
                specify_dir / "scripts",
                dirs_exist_ok=True,
            )

            # Handle script type filtering if needed
            # Only bash scripts are supported now
            pass

        # Copy templates directory (excluding commands which will be handled specially)
        if (resource_path / "templates").exists():
            if tracker:
                tracker.start("local-templates", "copying templates")
            # Copy all templates except commands directory
            for item in (resource_path / "templates").iterdir():
                if item.name != "commands":
                    if item.is_dir():
                        shutil.copytree(
                            item,
                            specify_dir / "templates" / item.name,
                            dirs_exist_ok=True,
                        )
                    else:
                        specify_dir.mkdir(parents=True, exist_ok=True)
                        (specify_dir / "templates").mkdir(exist_ok=True)
                        shutil.copy2(item, specify_dir / "templates" / item.name)

        # Handle AI assistant specific command files using the same logic as release script
        if (resource_path / "templates" / "commands").exists():
            if tracker:
                tracker.start("local-templates", f"generating {ai_assistant} commands")

            # Map AI assistant to their command directory and format (same as release script)
            if ai_assistant == "copilot":
                generate_commands(
                    "copilot",
                    "prompt.md",
                    "$ARGUMENTS",
                    project_path / ".github" / "prompts",
                    script_type,
                )
                # VS Code settings are handled by configure_vscode_settings() later
            elif ai_assistant == "qwen":
                generate_commands(
                    "qwen",
                    "toml",
                    "{{args}}",
                    project_path / ".qwen" / "commands",
                    script_type,
                )
            elif ai_assistant == "opencode":
                generate_commands(
                    "opencode",
                    "md",
                    "$ARGUMENTS",
                    project_path / ".opencode" / "command",
                    script_type,
                )
            else:
                # Fallback: copy commands to .specify/templates/commands
                shutil.copytree(
                    MODULE_DIR / "templates" / "commands",
                    specify_dir / "templates" / "commands",
                    dirs_exist_ok=True,
                )

        # Also copy any root-level files that might be in the original project structure
        root_files = ["README.md", ".gitignore", "spec-driven.md", "LICENSE"]
        for file_name in root_files:
            # Look for these files in the parent directory of the module (src/specify_cli -> .. -> spec-kit root)
            src_file = MODULE_DIR.parent.parent / file_name
            if src_file.exists():
                shutil.copy2(src_file, project_path / file_name)
            else:
                # If not found in development structure, check if they exist at module level (installed package)
                src_file = MODULE_DIR / file_name
                if src_file.exists():
                    shutil.copy2(src_file, project_path / file_name)

        # Copy skills directory
        if (resource_path / "skills").exists():
            if tracker:
                tracker.start("local-templates", "copying skills")

            # Determine destination: Default to .github/skills as it is the Open Standard location
            # User specifically requested this for Copilot, and it works for others too.
            skills_dest = project_path / ".github" / "skills"
            skills_dest.mkdir(parents=True, exist_ok=True)

            shutil.copytree(
                resource_path / "skills",
                skills_dest,
                dirs_exist_ok=True,
            )
            if tracker:
                tracker.complete("local-templates", "skills copied")

    except Exception as e:
        if tracker:
            tracker.error("local-templates", str(e))
        else:
            console.print(f"[red]Error copying local templates:[/red] {e}")
        # Clean up project directory if created and not current directory
        if not is_current_dir and project_path.exists():
            shutil.rmtree(project_path)
        raise typer.Exit(1)

    return project_path


def get_key():
    """Get a single keypress in a cross-platform way using readchar."""
    key = readchar.readkey()

    if key == readchar.key.UP or key == readchar.key.CTRL_P:
        return "up"
    if key == readchar.key.DOWN or key == readchar.key.CTRL_N:
        return "down"

    if key == readchar.key.ENTER:
        return "enter"

    if key == readchar.key.ESC:
        return "escape"

    if key == readchar.key.CTRL_C:
        raise KeyboardInterrupt

    return key


def select_with_arrows(
    options: Dict,
    prompt_text: str = "Select an option",
    default_key: Optional[str] = None,
) -> str:
    """
    Interactive selection using arrow keys with Rich Live display.

    Args:
        options: Dict with keys as option keys and values as descriptions
        prompt_text: Text to show above the options
        default_key: Default option key to start with

    Returns:
        Selected option key
    """
    option_keys = list(options.keys())
    if default_key and default_key in option_keys:
        selected_index = option_keys.index(default_key)
    else:
        selected_index = 0

    selected_key = None

    def create_selection_panel():
        """Create the selection panel with current selection highlighted."""
        table = Table.grid(padding=(0, 2))
        table.add_column(style="cyan", justify="left", width=3)
        table.add_column(style="white", justify="left")

        for i, key in enumerate(option_keys):
            if i == selected_index:
                table.add_row("▶", f"[cyan]{key}[/cyan] [dim]({options[key]})[/dim]")
            else:
                table.add_row(" ", f"[cyan]{key}[/cyan] [dim]({options[key]})[/dim]")

        table.add_row("", "")
        table.add_row(
            "", "[dim]Use ↑/↓ to navigate, Enter to select, Esc to cancel[/dim]"
        )

        return Panel(
            table,
            title=f"[bold]{prompt_text}[/bold]",
            border_style="cyan",
            padding=(1, 2),
        )

    console.print()

    def run_selection_loop():
        nonlocal selected_key, selected_index
        with Live(
            create_selection_panel(),
            console=console,
            transient=True,
            auto_refresh=False,
        ) as live:
            while True:
                try:
                    key = get_key()
                    if key == "up":
                        selected_index = (selected_index - 1) % len(option_keys)
                    elif key == "down":
                        selected_index = (selected_index + 1) % len(option_keys)
                    elif key == "enter":
                        selected_key = option_keys[selected_index]
                        break
                    elif key == "escape":
                        console.print("\n[yellow]Selection cancelled[/yellow]")
                        raise typer.Exit(1)

                    live.update(create_selection_panel(), refresh=True)

                except KeyboardInterrupt:
                    console.print("\n[yellow]Selection cancelled[/yellow]")
                    raise typer.Exit(1)

    run_selection_loop()

    if selected_key is None:
        console.print("\n[red]Selection failed.[/red]")
        raise typer.Exit(1)

    return selected_key


console = Console()


class BannerGroup(TyperGroup):
    """Custom group that shows banner before help."""

    def format_help(self, ctx, formatter):
        # Show banner before help
        show_banner()
        super().format_help(ctx, formatter)


app = typer.Typer(
    name="specify",
    help="Setup tool for Specify spec-driven development projects",
    add_completion=False,
    invoke_without_command=True,
    cls=BannerGroup,
)


def show_banner():
    """Display the ASCII art banner."""
    banner_lines = BANNER.strip().split("\n")
    colors = ["bright_blue", "blue", "cyan", "bright_cyan", "white", "bright_white"]

    styled_banner = Text()
    for i, line in enumerate(banner_lines):
        color = colors[i % len(colors)]
        styled_banner.append(line + "\n", style=color)

    console.print(Align.center(styled_banner))
    console.print(Align.center(Text(TAGLINE, style="italic bright_yellow")))
    console.print()


@app.callback()
def callback(ctx: typer.Context):
    """Show banner when no subcommand is provided."""
    if (
        ctx.invoked_subcommand is None
        and "--help" not in sys.argv
        and "-h" not in sys.argv
    ):
        show_banner()
        console.print(
            Align.center("[dim]Run 'specify --help' for usage information[/dim]")
        )
        console.print()


def run_command(
    cmd: List[str],
    check_return: bool = True,
    capture: bool = False,
    shell: bool = False,
) -> Optional[str]:
    """Run a shell command and optionally capture output."""
    try:
        if capture:
            result = subprocess.run(
                cmd, check=check_return, capture_output=True, text=True, shell=shell
            )
            return result.stdout.strip()
        else:
            subprocess.run(cmd, check=check_return, shell=shell)
            return None
    except subprocess.CalledProcessError as e:
        if check_return:
            console.print(f"[red]Error running command:[/red] {' '.join(cmd)}")
            console.print(f"[red]Exit code:[/red] {e.returncode}")
            if hasattr(e, "stderr") and e.stderr:
                console.print(f"[red]Error output:[/red] {e.stderr}")
            raise
        return None


def check_tool(tool: str, tracker: Optional[StepTracker] = None) -> bool:
    """Check if a tool is installed. Optionally update tracker.

    Args:
        tool: Name of the tool to check
        tracker: Optional StepTracker to update with results

    Returns:
        True if tool is found, False otherwise
    """
    found = shutil.which(tool) is not None

    if tracker:
        if found:
            tracker.complete(tool, "available")
        else:
            tracker.error(tool, "not found")

    return found


def is_git_repo(path: Optional[Path] = None) -> bool:
    """Check if the specified path is inside a git repository."""
    if path is None:
        path = Path.cwd()

    if not path.is_dir():
        return False

    try:
        # Use git command to check if inside a work tree
        subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            check=True,
            capture_output=True,
            cwd=path,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def init_git_repo(
    project_path: Path, quiet: bool = False
) -> Tuple[bool, Optional[str]]:
    """Initialize a git repository in the specified path.

    Args:
        project_path: Path to initialize git repository in
        quiet: if True suppress console output (tracker handles status)

    Returns:
        Tuple of (success: bool, error_message: Optional[str])
    """
    try:
        original_cwd = Path.cwd()
        os.chdir(project_path)
        if not quiet:
            console.print("[cyan]Initializing git repository...[/cyan]")
        subprocess.run(["git", "init"], check=True, capture_output=True, text=True)
        subprocess.run(["git", "add", "."], check=True, capture_output=True, text=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit from Specify template"],
            check=True,
            capture_output=True,
            text=True,
        )
        if not quiet:
            console.print("[green]✓[/green] Git repository initialized")
        return True, None

    except subprocess.CalledProcessError as e:
        error_msg = f"Command: {' '.join(e.cmd)}\nExit code: {e.returncode}"
        if e.stderr:
            error_msg += f"\nError: {e.stderr.strip()}"
        elif e.stdout:
            error_msg += f"\nOutput: {e.stdout.strip()}"

        if not quiet:
            console.print(f"[red]Error initializing git repository:[/red] {e}")
        return False, error_msg
    finally:
        os.chdir(original_cwd)


def ensure_executable_scripts(
    project_path: Path, tracker: Optional["StepTracker"] = None
) -> None:
    """Ensure POSIX .sh scripts under .specify/scripts (recursively) have execute bits (no-op on Windows)."""
    if os.name == "nt":
        return  # Windows: skip silently
    scripts_root = project_path / ".specify" / "scripts"
    if not scripts_root.is_dir():
        return
    failures: List[str] = []
    updated = 0
    for script in scripts_root.rglob("*.sh"):
        try:
            if script.is_symlink() or not script.is_file():
                continue
            try:
                with script.open("rb") as f:
                    if f.read(2) != b"#!":
                        continue
            except Exception:
                continue
            st = script.stat()
            mode = st.st_mode
            if mode & 0o111:
                continue
            new_mode = mode
            if mode & 0o400:
                new_mode |= 0o100
            if mode & 0o040:
                new_mode |= 0o010
            if mode & 0o004:
                new_mode |= 0o001
            if not (new_mode & 0o100):
                new_mode |= 0o100
            os.chmod(script, new_mode)
            updated += 1
        except Exception as e:
            failures.append(f"{script.relative_to(scripts_root)}: {e}")
    if tracker:
        detail = f"{updated} updated" + (
            f", {len(failures)} failed" if failures else ""
        )
        tracker.add("chmod", "Set script permissions recursively")
        (tracker.error if failures else tracker.complete)("chmod", detail)
    else:
        if updated:
            console.print(
                f"[cyan]Updated execute permissions on {updated} script(s) recursively[/cyan]"
            )
        if failures:
            console.print("[yellow]Some scripts could not be updated:[/yellow]")
            for f in failures:
                console.print(f"  - {f}")


@app.command()
def init(
    project_name: str = typer.Argument(
        None,
        help="Name for your new project directory (optional if using --here, or use '.' for current directory)",
    ),
    ai_assistant: str = typer.Option(
        None,
        "--ai",
        help="AI assistant to use: copilot, qwen, or opencode",
    ),
    script_type: str = typer.Option(
        None, "--script", help="Script type to use: sh or ps"
    ),
    ignore_agent_tools: bool = typer.Option(
        False,
        "--ignore-agent-tools",
        help="Skip checks for AI agent tools like Qwen CLI or opencode",
    ),
    no_git: bool = typer.Option(
        False, "--no-git", help="Skip git repository initialization"
    ),
    here: bool = typer.Option(
        False,
        "--here",
        help="Initialize project in the current directory instead of creating a new one",
    ),
    force: bool = typer.Option(
        False,
        "--force",
        help="Force merge/overwrite when using --here (skip confirmation)",
    ),
    skip_tls: bool = typer.Option(
        False, "--skip-tls", help="Skip SSL/TLS verification (not recommended)"
    ),
    debug: bool = typer.Option(
        False,
        "--debug",
        help="Show verbose diagnostic output for network and extraction failures",
    ),
):
    """
    Initialize a new Specify project from the latest template.

    This command will:
    1. Check that required tools are installed (git is optional)
    2. Let you choose your AI assistant
    3. Use local templates (GitHub download is no longer supported)
    4. Extract the template to a new project directory or current directory
    5. Initialize a fresh git repository (if not --no-git and no existing repo)
    6. Optionally set up AI assistant commands

    Examples:
        specify init my-project
        specify init my-project --ai copilot --no-git
        specify init --ignore-agent-tools my-project
        specify init . --ai qwen           # Initialize in current directory
        specify init .                     # Initialize in current directory (interactive AI selection)
        specify init --here --ai opencode  # Alternative syntax for current directory
        specify init --here
        specify init --here --force  # Skip confirmation when current directory not empty
    """

    show_banner()

    if project_name == ".":
        here = True
        project_name = None  # Clear project_name to use existing validation logic

    if here and project_name:
        console.print(
            "[red]Error:[/red] Cannot specify both project name and --here flag"
        )
        raise typer.Exit(1)

    if not here and not project_name:
        console.print(
            "[red]Error:[/red] Must specify either a project name, use '.' for current directory, or use --here flag"
        )
        raise typer.Exit(1)

    if here:
        project_name = Path.cwd().name
        project_path = Path.cwd()

        existing_items = list(project_path.iterdir())
        if existing_items:
            console.print(
                f"[yellow]Warning:[/yellow] Current directory is not empty ({len(existing_items)} items)"
            )
            console.print(
                "[yellow]Template files will be merged with existing content and may overwrite existing files[/yellow]"
            )
            if force:
                console.print(
                    "[cyan]--force supplied: skipping confirmation and proceeding with merge[/cyan]"
                )
            else:
                response = typer.confirm("Do you want to continue?")
                if not response:
                    console.print("[yellow]Operation cancelled[/yellow]")
                    raise typer.Exit(0)
    else:
        # project_name is not None here due to validation above
        assert project_name is not None
        project_path = Path(project_name).resolve()
        if project_path.exists():
            error_panel = Panel(
                f"Directory '[cyan]{project_name}[/cyan]' already exists\n"
                "Please choose a different project name or remove the existing directory.",
                title="[red]Directory Conflict[/red]",
                border_style="red",
                padding=(1, 2),
            )
            console.print()
            console.print(error_panel)
            raise typer.Exit(1)

    current_dir = Path.cwd()

    setup_lines = [
        "[cyan]Specify Project Setup[/cyan]",
        "",
        f"{'Project':<15} [green]{project_path.name}[/green]",
        f"{'Working Path':<15} [dim]{current_dir}[/dim]",
    ]

    if not here:
        setup_lines.append(f"{'Target Path':<15} [dim]{project_path}[/dim]")

    console.print(Panel("\n".join(setup_lines), border_style="cyan", padding=(1, 2)))

    should_init_git = False
    if not no_git:
        should_init_git = check_tool("git")
        if not should_init_git:
            console.print(
                "[yellow]Git not found - will skip repository initialization[/yellow]"
            )

    if ai_assistant:
        if ai_assistant not in AGENT_CONFIG:
            console.print(
                f"[red]Error:[/red] Invalid AI assistant '{ai_assistant}'. Choose from: {', '.join(AGENT_CONFIG.keys())}"
            )
            raise typer.Exit(1)
        selected_ai = ai_assistant
    else:
        # Create options dict for selection (agent_key: display_name)
        ai_choices = {key: config["name"] for key, config in AGENT_CONFIG.items()}
        selected_ai = select_with_arrows(
            ai_choices, "Choose your AI assistant:", "copilot"
        )

    if not ignore_agent_tools:
        agent_config = AGENT_CONFIG.get(selected_ai)
        if agent_config and agent_config["requires_cli"]:
            install_url = agent_config["install_url"]
            if not check_tool(selected_ai):
                error_panel = Panel(
                    f"[cyan]{selected_ai}[/cyan] not found\n"
                    f"Install from: [cyan]{install_url}[/cyan]\n"
                    f"{agent_config['name']} is required to continue with this project type.\n\n"
                    "Tip: Use [cyan]--ignore-agent-tools[/cyan] to skip this check",
                    title="[red]Agent Detection Error[/red]",
                    border_style="red",
                    padding=(1, 2),
                )
                console.print()
                console.print(error_panel)
                raise typer.Exit(1)

    if script_type:
        if script_type not in SCRIPT_TYPE_CHOICES:
            console.print(
                f"[red]Error:[/red] Invalid script type '{script_type}'. Choose from: {', '.join(SCRIPT_TYPE_CHOICES.keys())}"
            )
            raise typer.Exit(1)
        selected_script = script_type
    else:
        default_script = "ps" if os.name == "nt" else "sh"

        if sys.stdin.isatty():
            selected_script = select_with_arrows(
                SCRIPT_TYPE_CHOICES,
                "Choose script type (or press Enter)",
                default_script,
            )
        else:
            selected_script = default_script

    console.print(f"[cyan]Selected AI assistant:[/cyan] {selected_ai}")
    console.print(f"[cyan]Selected script type:[/cyan] {selected_script}")

    tracker = StepTracker("Initialize Specify Project")

    setattr(sys, "_specify_tracker_active", True)

    tracker.add("precheck", "Check required tools")
    tracker.complete("precheck", "ok")
    tracker.add("ai-select", "Select AI assistant")
    tracker.complete("ai-select", f"{selected_ai}")
    tracker.add("script-select", "Select script type")
    tracker.complete("script-select", selected_script)
    for key, label in [
        ("local-check", "Check for local templates"),
        ("fetch", "Fetch latest release"),
        ("download", "Download template"),
        ("extract", "Extract template"),
        ("zip-list", "Archive contents"),
        ("extracted-summary", "Extraction summary"),
        ("chmod", "Ensure scripts executable"),
        ("cleanup", "Cleanup"),
        ("git", "Initialize git repository"),
        ("vscode-settings", "Configure VS Code"),
        ("final", "Finalize"),
    ]:
        tracker.add(key, label)

    # Track git error message outside Live context so it persists
    git_error_message = None

    with Live(
        tracker.render(), console=console, refresh_per_second=8, transient=True
    ) as live:
        tracker.attach_refresh(lambda: live.update(tracker.render()))
        try:
            verify = not skip_tls
            local_ssl_context = ssl_context if verify else False
            local_client = httpx.Client(verify=local_ssl_context)

            # First, check if local templates are available
            if has_local_templates():
                if tracker:
                    tracker.complete("local-check", "found - using local templates")
                elif debug:
                    console.print(
                        "[cyan]Local templates found - using installed templates instead of downloading from GitHub[/cyan]"
                    )

                # Use local templates
                copy_local_templates(
                    project_path, selected_ai, selected_script, here, tracker
                )
            else:
                if tracker:
                    tracker.error("local-check", "not found")

                error_msg = (
                    "Local templates not found. GitHub download is no longer supported."
                )
                console.print(f"[red]Error:[/red] {error_msg}")
                raise typer.Exit(1)
            # Ensure the features directory exists under .specify/memory for downstream workflows
            features_dir = project_path / ".specify" / "memory" / "features"
            try:
                if tracker:
                    tracker.start(
                        "features-dir", "creating .specify/memory/features directory"
                    )
                features_dir.mkdir(parents=True, exist_ok=True)
                if tracker:
                    tracker.complete("features-dir", f"created {features_dir}")
            except Exception as e:
                if tracker:
                    tracker.error("features-dir", str(e))
                else:
                    console.print(
                        f"[yellow]Warning: could not create features directory:[/yellow] {e}"
                    )

            ensure_executable_scripts(project_path, tracker=tracker)

            if not no_git:
                tracker.start("git")
                if is_git_repo(project_path):
                    tracker.complete("git", "existing repo detected")
                elif should_init_git:
                    success, error_msg = init_git_repo(project_path, quiet=True)
                    if success:
                        tracker.complete("git", "initialized")
                    else:
                        tracker.error("git", "init failed")
                        git_error_message = error_msg
                else:
                    tracker.skip("git", "git not available")
            else:
                tracker.skip("git", "--no-git flag")

            # Configure VS Code settings
            configure_vscode_settings(project_path, tracker=tracker)

            tracker.complete("final", "project ready")
        except Exception as e:
            tracker.error("final", str(e))
            console.print(
                Panel(
                    f"Initialization failed: {e}", title="Failure", border_style="red"
                )
            )
            if debug:
                _env_pairs = [
                    ("Python", sys.version.split()[0]),
                    ("Platform", sys.platform),
                    ("CWD", str(Path.cwd())),
                ]
                _label_width = max(len(k) for k, _ in _env_pairs)
                env_lines = [
                    f"{k.ljust(_label_width)} → [bright_black]{v}[/bright_black]"
                    for k, v in _env_pairs
                ]
                console.print(
                    Panel(
                        "\n".join(env_lines),
                        title="Debug Environment",
                        border_style="magenta",
                    )
                )
            if not here and project_path.exists():
                shutil.rmtree(project_path)
            raise typer.Exit(1)
        finally:
            pass

    console.print(tracker.render())
    console.print("\n[bold green]Project ready.[/bold green]")

    # Show git error details if initialization failed
    if git_error_message:
        console.print()
        git_error_panel = Panel(
            f"[yellow]Warning:[/yellow] Git repository initialization failed\n\n"
            f"{git_error_message}\n\n"
            f"[dim]You can initialize git manually later with:[/dim]\n"
            f"[cyan]cd {project_path if not here else '.'}[/cyan]\n"
            f"[cyan]git init[/cyan]\n"
            f"[cyan]git add .[/cyan]\n"
            f'[cyan]git commit -m "Initial commit"[/cyan]',
            title="[red]Git Initialization Failed[/red]",
            border_style="red",
            padding=(1, 2),
        )
        console.print(git_error_panel)

    # Agent folder security notice
    agent_config = AGENT_CONFIG.get(selected_ai)
    if agent_config:
        agent_folder = agent_config["folder"]
        security_notice = Panel(
            f"Some agents may store credentials, auth tokens, or other identifying and private artifacts in the agent folder within your project.\n"
            f"Consider adding [cyan]{agent_folder}[/cyan] (or parts of it) to [cyan].gitignore[/cyan] to prevent accidental credential leakage.",
            title="[yellow]Agent Folder Security[/yellow]",
            border_style="yellow",
            padding=(1, 2),
        )
        console.print()
        console.print(security_notice)

    steps_lines = []
    if not here:
        steps_lines.append(
            f"1. Go to the project folder: [cyan]cd {project_name}[/cyan]"
        )
        step_num = 2
    else:
        steps_lines.append("1. You're already in the project directory!")
        step_num = 2

    # Add Codex-specific setup step if needed
    if selected_ai == "codex":
        codex_path = project_path / ".codex"
        quoted_path = shlex.quote(str(codex_path))
        if os.name == "nt":  # Windows
            cmd = f"setx CODEX_HOME {quoted_path}"
        else:  # Unix-like systems
            cmd = f"export CODEX_HOME={quoted_path}"

        steps_lines.append(
            f"{step_num}. Set [cyan]CODEX_HOME[/cyan] environment variable before running Codex: [cyan]{cmd}[/cyan]"
        )
        step_num += 1

    steps_lines.append(f"{step_num}. Start using slash commands with your AI agent:")

    steps_lines.append(
        "   2.1 [cyan]/speckit.constitution[/] - Establish project principles"
    )
    steps_lines.append(
        "   2.2 [cyan]/speckit.feature[/] - Manage feature lifecycle & index"
    )
    steps_lines.append(
        "   2.3 [cyan]/speckit.specify[/] - Create baseline specification"
    )
    steps_lines.append("   2.4 [cyan]/speckit.plan[/] - Create implementation plan")
    steps_lines.append("   2.5 [cyan]/speckit.tasks[/] - Generate actionable tasks")
    steps_lines.append("   2.6 [cyan]/speckit.implement[/] - Implement feature")

    steps_panel = Panel(
        "\n".join(steps_lines), title="Next Steps", border_style="cyan", padding=(1, 2)
    )
    console.print()
    console.print(steps_panel)

    enhancement_lines = [
        "Optional commands that you can use for your specs [bright_black](improve quality & confidence)[/bright_black]",
        "",
        "○ [cyan]/speckit.clarify[/] [bright_black](optional)[/bright_black] - Ask structured questions to de-risk ambiguous areas before planning (run before [cyan]/speckit.plan[/] if used)",
        "○ [cyan]/speckit.analyze[/] [bright_black](optional)[/bright_black] - Cross-artifact consistency & alignment report (after [cyan]/speckit.tasks[/], before [cyan]/speckit.implement[/])",
        "○ [cyan]/speckit.checklist[/] [bright_black](optional)[/bright_black] - Generate quality checklists to validate requirements completeness, clarity, and consistency (after [cyan]/speckit.plan[/])",
        "○ [cyan]/speckit.review[/] [bright_black](optional)[/bright_black] - Review the full SDD artifact set for a feature and summarize it (after [cyan]/speckit.implement[/])",
    ]
    enhancements_panel = Panel(
        "\n".join(enhancement_lines),
        title="Enhancement Commands",
        border_style="cyan",
        padding=(1, 2),
    )
    console.print()
    console.print(enhancements_panel)


@app.command()
def check():
    """Check that all required tools are installed."""
    show_banner()
    console.print("[bold]Checking for installed tools...[/bold]\n")

    tracker = StepTracker("Check Available Tools")

    tracker.add("git", "Git version control")
    git_ok = check_tool("git", tracker=tracker)

    agent_results = {}
    for agent_key, agent_config in AGENT_CONFIG.items():
        agent_name = agent_config["name"]
        requires_cli = agent_config["requires_cli"]

        tracker.add(agent_key, agent_name)

        if requires_cli:
            agent_results[agent_key] = check_tool(agent_key, tracker=tracker)
        else:
            # IDE-based agent - skip CLI check and mark as optional
            tracker.skip(agent_key, "IDE-based, no CLI check")
            agent_results[agent_key] = False  # Don't count IDE agents as "found"

    # Check VS Code variants (not in agent config)
    tracker.add("code", "Visual Studio Code")
    code_ok = check_tool("code", tracker=tracker)

    tracker.add("code-insiders", "Visual Studio Code Insiders")
    code_insiders_ok = check_tool("code-insiders", tracker=tracker)

    console.print(tracker.render())

    console.print("\n[bold green]Specify CLI is ready to use![/bold green]")

    if not git_ok:
        console.print("[dim]Tip: Install git for repository management[/dim]")

    if not any(agent_results.values()):
        console.print("[dim]Tip: Install an AI assistant for the best experience[/dim]")


def main():
    app()


if __name__ == "__main__":
    main()
