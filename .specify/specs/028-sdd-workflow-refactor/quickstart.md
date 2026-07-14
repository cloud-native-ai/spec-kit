# Quickstart: Verifying the Shared Reference Directory Refactor

**Spec**: `028-sdd-workflow-refactor` | **Feature**: 029

This walkthrough verifies the refactor end-to-end. Run from repo root.

## 1. Source tree is correct

```bash
# New shared directory exists with all ten docs; old skill is gone
ls shared/workflow/            # → 10 .md files
test ! -e skills/sdd-workflow  # → skill directory deleted
```

Expected: `shared/workflow/` lists the ten reference documents; `skills/sdd-workflow/` no longer exists.

## 2. Content parity

```bash
# Each shared doc matches the pre-refactor original (compare against git history)
git show HEAD~:skills/sdd-workflow/references/user-input-protocol.md \
  | diff - shared/workflow/user-input-protocol.md   # → no diff
```

Expected: no differences for any of the ten files.

## 3. Packaging includes shared/

```bash
grep -A6 'force-include' pyproject.toml | grep 'shared'   # → "shared" = "specify_cli/shared"
```

## 4. Fresh init installs the shared directory

```bash
tmp=$(mktemp -d)
specify init "$tmp" --ai claude --script bash --no-git   # or the project's local test harness
ls "$tmp"/.specify/shared/workflow/                        # → 10 .md files
test ! -e "$tmp"/.specify/skills/sdd-workflow             # → not present
test ! -e "$tmp"/.github/skills/sdd-workflow              # → not present in symlink surface
```

## 5. Re-init retains the shared directory

```bash
touch "$tmp"/.specify/shared/workflow/.sentinel
specify init "$tmp" --ai claude --script bash --no-git --force   # re-init
test -e "$tmp"/.specify/shared/workflow/.sentinel                # → still present (retained)
```

## 6. References resolve (no dead links)

```bash
# In generated command files, shared refs point at existing installed files
grep -roh '\.specify/shared/workflow/[a-z0-9-]*\.md' "$tmp"/.claude/commands/ \
  | sort -u | while read p; do test -e "$tmp/$p" || echo "DEAD LINK: $p"; done
# → no "DEAD LINK" output
```

## 7. Zero-reference acceptance gate

```bash
grep -rn "sdd-workflow" . \
  --exclude-dir=.git --exclude-dir=.venv --exclude-dir=docs/history \
  | grep -v "docs/summary/03-sdd-workflow-refactor-proposal.md" \
  | grep -v ".specify/specs/028-sdd-workflow-refactor/"
# → no output
```

## 8. Test suite

```bash
pytest -q            # → no new failures vs. pre-refactor baseline
```

All eight steps passing = Feature 029 acceptance criteria (SC-001…SC-006) met.
