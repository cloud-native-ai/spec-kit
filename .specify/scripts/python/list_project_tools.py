#!/usr/bin/env python3
"""List project script files from .specify/scripts or scripts directory."""

import ast
import json
from pathlib import Path
from typing import Dict, List, Optional


def find_root_dir(start: Optional[Path] = None) -> Path:
	"""Find repository root directory."""
	current = (start or Path.cwd()).resolve()
	for candidate in [current, *current.parents]:
		if (candidate / ".git").exists():
			return candidate
		if (candidate / "pyproject.toml").exists() and (candidate / "scripts").exists():
			return candidate
	return current


def detect_scripts_dir(root_dir: Path) -> Optional[Path]:
	"""Prefer .specify/scripts, fallback to scripts."""
	specify_scripts = root_dir / ".specify" / "scripts"
	local_scripts = root_dir / "scripts"
	if specify_scripts.exists() and specify_scripts.is_dir():
		return specify_scripts
	if local_scripts.exists() and local_scripts.is_dir():
		return local_scripts
	return None


def extract_python_docstring(file_path: Path) -> str:
	try:
		content = file_path.read_text(encoding="utf-8")
		doc = ast.get_docstring(ast.parse(content))
		if doc:
			return doc.splitlines()[0].strip()
	except Exception:
		pass
	return "No description available"


def extract_shell_comment(file_path: Path) -> str:
	try:
		for line in file_path.read_text(encoding="utf-8").splitlines():
			stripped = line.strip()
			if stripped.startswith("#!"):
				continue
			if stripped.startswith("#"):
				return stripped.lstrip("#").strip() or "No description available"
	except Exception:
		pass
	return "No description available"


def list_project_scripts(root_dir: Path) -> List[Dict[str, str]]:
	scripts_dir = detect_scripts_dir(root_dir)
	if not scripts_dir:
		return []

	results: List[Dict[str, str]] = []
	for file_path in sorted(scripts_dir.rglob("*")):
		if not file_path.is_file():
			continue
		if file_path.suffix not in {".sh", ".py"}:
			continue

		rel_path = file_path.resolve().relative_to(root_dir.resolve()).as_posix()
		script_type = "python" if file_path.suffix == ".py" else "bash"
		if script_type == "python":
			description = extract_python_docstring(file_path)
		else:
			description = extract_shell_comment(file_path)

		results.append(
			{
				"name": file_path.name,
				"path": rel_path,
				"type": script_type,
				"description": description,
			}
		)
	return results


def main() -> int:
	import argparse

	parser = argparse.ArgumentParser(description="List project scripts")
	parser.add_argument(
		"--root-dir",
		default=".",
		help="Root directory to scan (default: current directory)",
	)
	args = parser.parse_args()

	root_dir = find_root_dir(Path(args.root_dir))
	records = list_project_scripts(root_dir)
	print(json.dumps(records, ensure_ascii=False, indent=2))

	return 0


if __name__ == "__main__":
	raise SystemExit(main())
