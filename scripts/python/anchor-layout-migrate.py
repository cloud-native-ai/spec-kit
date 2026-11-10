#!/usr/bin/env python3
"""anchor-layout-migrate.py — converge a project to the anchor layout (feature 094-era architecture).

Layout owned here (mechanism): the project anchors live at the `.specify/` root —
`features.md`, `constitution.md`, `glossary.md`, `register.md`, `tools.md` — and the feature-detail files
live at `.specify/features/<NNN>-<slug>.md`. The legacy layout kept the five anchors under
`.specify/memory/` and the details at `.specify/memory/features/<NNN>.md`.

`--check`  detect only: exit 0 clean, 1 findings (a plan), 2 input error.
`--apply`  perform the moves: never overwrite an existing target; moves only (archive-not-delete: no file is
           ever deleted; a move whose target already exists is reported as skipped, never forced). Idempotent:
           a second apply is a no-op. Prints the reference paths the caller must update (the script never
           rewrites project documents).

Options (closed set): --workspace PATH, --check, --apply, --json. `-h/--help`, `--version` answer without acting.
Side effects: `--apply` renames/moves files under `.specify/`; the flags write nothing.
Exit codes: 0 clean/applied; 1 findings (check) or refused (apply); 2 argument or environment error.
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path

ANCHORS = ("features.md", "constitution.md", "glossary.md", "register.md", "tools.md")


def _slug_from_registry(workspace: Path, fid: str):
    # The registry lives at the anchor root in a migrated project and under memory/ in a legacy one.
    for candidate in (workspace / ".specify" / "features.md",
                      workspace / ".specify" / "memory" / "features.md"):
        if candidate.is_file():
            registry = candidate
            break
    else:
        return None
    pattern = re.compile(r"^\|\s*" + re.escape(fid) + r"\s*\|")
    for line in registry.read_text(encoding="utf-8", errors="replace").splitlines():
        if not pattern.match(line):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        spec = cells[5] if len(cells) > 5 else ""
        match = re.search(r"specs/(\d{3})-([A-Za-z0-9-]+)/", spec)
        if match and match.group(1) == fid:
            return match.group(2)
    return None


def _slug_from_content(path: Path):
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    for line in text.splitlines()[:12]:
        heading = re.sub(r"^#+\s*", "", line).strip()
        if heading:
            heading = re.sub(r"^\d{3}\s*[—:-]\s*", "", heading)
            slug = re.sub(r"[^a-z0-9]+", "-", heading.lower()).strip("-")
            return slug or None
    return None


def plan(workspace: Path):
    spec = workspace / ".specify"
    steps = []
    if not spec.is_dir():
        raise SystemExit("input error: no .specify/ directory under %s" % workspace)
    memory = spec / "memory"
    for anchor in ANCHORS:
        legacy = memory / anchor
        target = spec / anchor
        if legacy.is_file():
            if target.exists():
                steps.append({"kind": "refuse-existing-target", "from": str(legacy), "to": str(target)})
            else:
                steps.append({"kind": "move", "from": str(legacy), "to": str(target)})
    legacy_details = memory / "features"
    if legacy_details.is_dir():
        for item in sorted(legacy_details.glob("[0-9][0-9][0-9].md")):
            fid = item.stem
            slug = _slug_from_registry(workspace, fid) or _slug_from_content(item) or "feature"
            target = spec / "features" / ("%s-%s.md" % (fid, slug))
            steps.append({"kind": "move", "from": str(item), "to": str(target)})
    return steps


def apply(workspace: Path, steps):
    done = []
    skipped = []
    for step in steps:
        if step["kind"] != "move":
            continue
        src, dst = Path(step["from"]), Path(step["to"])
        if not src.is_file() or dst.exists():
            skipped.append(step)
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        os.replace(str(src), str(dst))
        done.append(step)
    return done, skipped


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="anchor-layout-migrate.py",
        description="Detect or apply the anchor layout (.specify/{features,constitution,glossary,register,tools}.md; .specify/features/<NNN>-<slug>.md).",
    )
    parser.add_argument("--action", choices=("check", "apply"), default="check")
    parser.add_argument("--workspace", default=".")
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument("--version", action="version", version="anchor-layout-migrate.py 1.0.0")
    args = parser.parse_args(argv)
    workspace = Path(args.workspace).expanduser().resolve()
    steps = plan(workspace)
    if args.action == "check":
        if args.as_json:
            print(json.dumps({"steps": steps, "clean": not steps}, indent=2))
        else:
            if not steps:
                print("anchor layout: clean")
            else:
                for step in steps:
                    print("%s: %s -> %s" % (step["kind"], step["from"], step["to"]))
        return 0 if not steps else 1
    done, skipped = apply(workspace, steps)
    if args.as_json:
        print(json.dumps({"applied": done,
                          "refused": [s for s in steps if s["kind"] != "move"],
                          "skipped": skipped}, indent=2))
    else:
        for step in done:
            print("moved: %s -> %s" % (step["from"], step["to"]))
        for step in steps:
            if step["kind"] != "move":
                print("refused: %s (target exists) %s" % (step["from"], step["to"]))
        for step in skipped:
            print("skipped: %s (target exists) %s" % (step["from"], step["to"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
