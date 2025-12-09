import argparse
import json
import os
import re
import sys


def strip_comments(text):
    """
    Removes C-style comments (// and /* */) from text.
    """

    def replacer(match):
        s = match.group(0)
        if s.startswith("/"):
            return " "  # note: a space and not an empty string
        else:
            return s

    pattern = re.compile(
        r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
        re.DOTALL | re.MULTILINE,
    )
    return re.sub(pattern, replacer, text)


def detect_tech_stack(root_dir):
    stack = set()
    # Java
    if os.path.exists(os.path.join(root_dir, "pom.xml")) or os.path.exists(
        os.path.join(root_dir, "build.gradle")
    ):
        stack.add("java")

    # Python
    if (
        os.path.exists(os.path.join(root_dir, "pyproject.toml"))
        or os.path.exists(os.path.join(root_dir, "requirements.txt"))
        or os.path.exists(os.path.join(root_dir, "setup.py"))
    ):
        stack.add("python")

    # Node/JS/TS
    if os.path.exists(os.path.join(root_dir, "package.json")):
        stack.add("javascript")
        if os.path.exists(os.path.join(root_dir, "tsconfig.json")):
            stack.add("typescript")

    return stack


def main():
    parser = argparse.ArgumentParser(
        description="Generate VS Code settings based on project context."
    )
    parser.add_argument(
        "--template", required=True, help="Path to the template settings.json"
    )
    parser.add_argument(
        "--output", required=True, help="Path to the output settings.json"
    )
    parser.add_argument("--root", default=".", help="Project root directory to analyze")
    args = parser.parse_args()

    # 1. Load template
    if not os.path.exists(args.template):
        print(f"Error: Template file not found: {args.template}")
        sys.exit(1)

    try:
        with open(args.template, "r", encoding="utf-8") as f:
            content = f.read()
            # Handle JSONC by stripping comments
            json_content = strip_comments(content)
            settings = json.loads(json_content)
    except Exception as e:
        print(f"Error loading template: {e}")
        sys.exit(1)

    # 2. Analyze project context
    stack = detect_tech_stack(args.root)
    print(f"Detected tech stack: {', '.join(stack)}")

    # 3. Apply dynamic settings based on stack
    if "java" in stack:
        # Example Java settings
        settings.setdefault("java.configuration.updateBuildConfiguration", "automatic")
        settings.setdefault("java.format.settings.url", ".vscode/java-formatter.xml")

    if "python" in stack:
        # Example Python settings
        settings.setdefault("python.analysis.typeCheckingMode", "basic")
        settings.setdefault("python.formatting.provider", "black")

    if "typescript" in stack or "javascript" in stack:
        settings.setdefault("editor.defaultFormatter", "esbenp.prettier-vscode")

    # 4. Check for constitution/feature-index (placeholder for future logic)
    constitution_path = os.path.join(args.root, "memory", "constitution.md")
    if os.path.exists(constitution_path):
        # Could parse constitution here for specific rules
        pass

    feature_index_path = os.path.join(args.root, "memory", "feature-index.md")
    if os.path.exists(feature_index_path):
        # Example: Enable feature tracking if index exists
        pass

    # 5. Write output
    # Ensure output directory exists
    output_dir = os.path.dirname(args.output)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    try:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=2, ensure_ascii=False)
        print(f"Generated settings at {args.output}")
    except Exception as e:
        print(f"Error writing output: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
