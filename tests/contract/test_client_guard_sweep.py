"""Contract test: guard sweep — red lines, closed surfaces, fixture duty and
the no-history-rewrite net (Feature 072, User Story 6).

Pins `contracts/red-lines-and-surfaces.md` C-51…C-62 against every surface
Feature 072 touches. Unlike the five per-story contract groups, the assertions
here are *sweep* assertions: each scan conclusion is recomputable from the
live tree and the frozen plan-baseline commit (`6dca65a5`, the approved plan
commit recorded in the state spine), never from a hand-maintained diff.

* **C-51** — the four feedback red lines survive verbatim in their owner
  (`shared/workflow/feedback-step.md`, source and runtime mirror) and cover
  client entries with equal force;
* **C-52** — no new network call, external service, dependency, or resident
  process anywhere in the feature's edit surface (frozen dependency files,
  added-imports audit, banned-pattern scan over the touched surfaces);
* **C-53…C-57** — Feature 071's closed surfaces are preserved verbatim (record
  rotation, receipt/report exit alphabets and the receipt field block, the
  report's code-subsection field list, the review command's six closing
  steps, the per-run three-unit census); no `/speckit.*` command and no CLI
  entry face is added beyond the two authorized faces; the edit surface stays
  the framework sources; the two existing negative assertions are kept
  verbatim and shipped text stays client-neutral;
* **C-58/C-59** — every client-side behavior group executes inside the
  disposable client fixture (never framework self-testing), and a client
  repository that vendors any one of the five framework source directories
  takes the framework branch by the owner hat criterion — zero external
  entries, one `skipped` line citing the hat owner, never a five-value token;
* **C-60…C-62** — no history rewrite (no modified/deleted feedback entry or
  review report; the legacy monolithic store is read-only for this feature's
  actions), the guard suites only grow, and the engine additions stay bounded
  to exactly the two authorized faces.

Behavioural hat/capture assertions execute inside the disposable client
project built by `tests/fixtures/client_project.py` (C-58).
"""
from __future__ import annotations

import ast
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set

import pytest

from fixtures.client_project import (
    FRAMEWORK_ROOT,
    FRAMEWORK_SOURCE_DIRS,
    ClientProject,
    hat_of,
    make_client_project,
)

pytestmark = pytest.mark.contract

#: The approved plan commit — the frozen "before" of every sweep comparison
#: (state spine: plan_commit / approved_baseline_commit = 6dca65a5).
BASELINE_COMMIT = "6dca65a5"

REVIEW_SCRIPT = FRAMEWORK_ROOT / "skills" / "internal" / "code-review" / "scripts" / "git-delta-review.sh"
SKILL_MD = FRAMEWORK_ROOT / "skills" / "internal" / "code-review" / "SKILL.md"
MANAGE_FEEDBACK_SKILL = FRAMEWORK_ROOT / "skills" / "internal" / "manage-feedback" / "SKILL.md"
FEEDBACK_STEP = FRAMEWORK_ROOT / "shared" / "workflow" / "feedback-step.md"
FEEDBACK_STEP_MIRROR = FRAMEWORK_ROOT / ".specify" / "shared" / "workflow" / "feedback-step.md"
REVIEW_TEMPLATE = FRAMEWORK_ROOT / "templates" / "review-template.md"
REVIEW_COMMAND_TEMPLATE = FRAMEWORK_ROOT / "templates" / "commands" / "review.md"
FEEDBACK_ENGINE_SRC = FRAMEWORK_ROOT / "scripts" / "python" / "feedback-utils.py"

SPEC_DIR = ".specify/specs/072-guard-demo"
RECORD_REL = f"{SPEC_DIR}/code-review.md"
STAMP = "20261027T000000Z"
UNIT = "custom:fixture/unit"

#: The closed five-value disclosure set (C-22) — the vendored-hat skip line
#: MUST NOT take any of these forms (C-59).
FIVE_TOKENS = {
    "client-channel-armed",
    "client-channel-unarmed",
    "client-unit-ambiguous",
    "no-capture-object",
    "counts-unavailable",
}

HAT_OWNER_CITATION = "dogfooding-definitions.md"

#: Feature 072's complete edit surface (C-56) — framework sources only.
TOUCHED_SURFACES = [
    FEEDBACK_ENGINE_SRC,
    FRAMEWORK_ROOT / "scripts" / "python" / "probe-utils.py",
    SKILL_MD,
    REVIEW_SCRIPT,
    MANAGE_FEEDBACK_SKILL,
    FRAMEWORK_ROOT / "skills" / "internal" / "manage-feedback" / "references" / "path-a-digest.md",
    FRAMEWORK_ROOT / "skills" / "internal" / "self-improvement" / "SKILL.md",
    FRAMEWORK_ROOT / "shared" / "guidelines" / "dogfooding.md",
    FRAMEWORK_ROOT / "shared" / "workflow" / "self-improvement-workflow.md",
    FRAMEWORK_ROOT / "templates" / "commands" / "feedback.md",
    FRAMEWORK_ROOT / "templates" / "commands" / "improve.md",
    REVIEW_COMMAND_TEMPLATE,
]

#: Guard-suite floors frozen at T001 (notes/pre-change-measurements.md §5) —
#: the named suites stay green with assertion counts only growing (C-57/C-61).
GUARD_SUITES = {
    "071 six suites": (
        ["test_review_code_composition.py", "test_code_review_skill_contract.py",
         "test_coverage_receipt.py", "test_status_gate_owner.py",
         "test_review_feedback_boundary.py", "test_review_docs_isomorphism.py"],
        161,
    ),
    "expression compatibility (C-5 frozen hash)": (["test_expression_compatibility.py"], 16),
    "071 P1 review loop": (["test_review_p1_review_loop.py"], 10),
}
FEEDBACK_PROBE_FAMILY_FLOOR = 18

#: Shipped files whose neutrality violations predate Feature 072 (audited
#: 2026-10-27: Feature 064/066/067/070 references in the sdd-loop-driver
#: skill and flow-class-definitions.md — all present at the T002 baseline
#: capture, none touched by this feature). Feature 072 shipped text MUST NOT
#: add a single fresh violation (C-57).
PRE_EXISTING_NEUTRALITY_DEBT = {
    "shared/definitions/flow-class-definitions.md",
    "skills/external/sdd-loop-driver/templates/stage-team-preset.md",
    "skills/external/sdd-loop-driver/references/decomposition-model.md",
    "skills/external/sdd-loop-driver/scripts/loop-state.py",
    "skills/external/sdd-loop-driver/scripts/wp-report.py",
}

BANNED_NETWORK_PATTERNS = [
    re.compile(r"\bcurl\b"), re.compile(r"\bwget\b"), re.compile(r"\bnc\s+[-0-9]"),
    re.compile(r"\bsocket\b"), re.compile(r"\bhttpx\b"), re.compile(r"\brequests\b"),
    re.compile(r"\burllib\b"), re.compile(r"\baiohttp\b"), re.compile(r"\bwebsocket\b"),
    re.compile(r"\bssh\b\s"), re.compile(r"\brsync\b"), re.compile(r"\bscp\b"),
]
BANNED_RESIDENT_PATTERNS = [
    re.compile(r"\bnohup\b"), re.compile(r"\bsetsid\b"), re.compile(r"\bcron\b"),
    re.compile(r"\bsystemd\b"), re.compile(r"\blaunchd\b"), re.compile(r"\bdaemon\b"),
    re.compile(r"\btimer\b"), re.compile(r"\bscheduler\b"),
]


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #

def git(*args: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(FRAMEWORK_ROOT), *args],
        capture_output=True, text=True,
    )
    assert completed.returncode == 0, (
        f"git {' '.join(args)} failed:\n{completed.stdout}\n{completed.stderr}"
    )
    return completed.stdout


def baseline_text(rel: str) -> str:
    return git("show", f"{BASELINE_COMMIT}:{rel}")


def changed_name_status() -> List[str]:
    return git("diff", "--name-status", f"{BASELINE_COMMIT}..HEAD").splitlines()


def run_review(project: ClientProject, *args: str,
               extra_env: Optional[Dict[str, str]] = None):
    env = {"REVIEW_RUN_TIMESTAMP": STAMP}
    if extra_env:
        env.update(extra_env)
    return project.run_script(str(REVIEW_SCRIPT), *args, extra_env=env)


def capture_lines(stdout: str) -> List[str]:
    return [line for line in stdout.splitlines() if line.startswith("capture:")]


def external_count(project: ClientProject) -> int:
    return int(project.feedback_list_json(kind="external")["count"])


def qualified_run(project: ClientProject) -> Path:
    project.write("src/app.py", "def f():\n    return 1\n")
    project.commit("base", ["src/app.py"])
    project.write("src/app.py", "def f():\n    return 2\n")
    project.commit("change", ["src/app.py"])
    triage = run_review(project, "triage", "--since", "HEAD~1", "--head", "HEAD")
    assert triage.returncode == 0 and "triage=run" in triage.stdout, triage.describe()
    start = run_review(project, "start", "--spec", SPEC_DIR,
                       "--since", "HEAD~1", "--head", "HEAD", "--triage", "run")
    assert start.returncode == 0, start.describe()
    record = project.path / RECORD_REL
    assert record.is_file()
    return record


def armed_capture(project: ClientProject, *extra: str):
    return run_review(project, "capture", "--review-file", RECORD_REL,
                      "--triage", "run", *extra)


# --------------------------------------------------------------------------- #
# T023 / C-51 — the four red lines, verbatim, equally binding on client entries
# --------------------------------------------------------------------------- #

def test_c51_four_red_lines_verbatim_and_equal_client_coverage():
    for name, raw in (("source", FEEDBACK_STEP.read_text(encoding="utf-8")),
                      ("mirror", FEEDBACK_STEP_MIRROR.read_text(encoding="utf-8"))):
        text = " ".join(raw.split())   # the owner wraps prose across lines
        for red_line in (
            "**Target = the Spec Kit framework itself.**",
            "**Feedback is user data and fully optional.**",
            "**Zero automated transmission.**",
            "**Local workaround value.**",
        ):
            assert red_line in text, (
                f"red line {red_line!r} MUST survive verbatim in the {name} owner "
                f"({FEEDBACK_STEP.relative_to(FRAMEWORK_ROOT)}) (C-51)"
            )
        # Equal coverage of client entries (FR-024): the owner states the
        # host-project-local / never-upstream closure for custom units, and
        # the zero-transmission rule names the manual package path as the
        # only legitimate transmission.
        assert "their entries stay host-project-local and never enter upstream packages" in text, (
            "red line 1/3 MUST cover client entries with equal force (C-51)"
        )
        assert "only legitimate transmission paths are (a) the user manually sending a packaged zip" in text, (
            "red line 3 (zero automatic transmission) MUST keep manual delivery of a "
            "package as the only legal path (C-51)"
        )
    # The owner text is untouched by this feature (verbatim preservation is
    # a diff-level fact, not only a containment check).
    assert git("diff", "--name-only", f"{BASELINE_COMMIT}..HEAD",
               "--", "shared/workflow/feedback-step.md") == "", (
        "the four-red-line owner MUST NOT be edited by this feature (C-51)"
    )


# --------------------------------------------------------------------------- #
# T023 / C-52 — no network call, external service, dependency, resident process
# --------------------------------------------------------------------------- #

def test_c52_dependency_files_frozen_and_no_new_scripts():
    assert git("diff", "--name-only", f"{BASELINE_COMMIT}..HEAD",
               "--", "pyproject.toml", "uv.lock") == "", (
        "C-52: no new dependency may be added — pyproject.toml / uv.lock MUST be "
        "unchanged by this feature"
    )
    added_scripts = git("diff", "--diff-filter=A", "--name-only",
                        f"{BASELINE_COMMIT}..HEAD", "--", "scripts/", ".specify/scripts/")
    assert added_scripts == "", (
        f"C-52/C-62: no new engine or script may be created; added:\n{added_scripts}"
    )


def test_c52_added_imports_are_stdlib_only():
    added_imports: Set[str] = set()
    for rel in ("scripts/python/feedback-utils.py", "scripts/python/probe-utils.py"):
        for line in git("diff", f"{BASELINE_COMMIT}..HEAD", "--", rel).splitlines():
            m = re.match(r"^\+(?:import\s+(\w+)|from\s+(\w+)\s+import\s)", line)
            if m:
                added_imports.add(m.group(1) or m.group(2))
    stdlib = set(sys.stdlib_module_names)
    non_stdlib = added_imports - stdlib
    assert not non_stdlib, (
        f"C-52: the feature's engine edits may only import stdlib modules; "
        f"found non-stdlib: {sorted(non_stdlib)}"
    )


def test_c52_no_network_or_resident_process_in_touched_surfaces():
    violations = []
    for path in TOUCHED_SURFACES:
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(FRAMEWORK_ROOT).as_posix()
        for label, patterns in (("network", BANNED_NETWORK_PATTERNS),
                                ("resident-process", BANNED_RESIDENT_PATTERNS)):
            for pattern in patterns:
                for m in pattern.finditer(text):
                    line = text[: m.start()].count("\n") + 1
                    violations.append(f"{rel}:{line} ({label}): {pattern.pattern}")
    assert not violations, (
        "C-52: banned network / resident-process construct found in a Feature 072 "
        "surface:\n" + "\n".join(violations[:15])
    )


# --------------------------------------------------------------------------- #
# T024 / C-53 — Feature 071's closed surfaces, verbatim
# --------------------------------------------------------------------------- #

def test_c53_record_rotation_receipt_alphabets_and_field_block_verbatim():
    skill = SKILL_MD.read_text(encoding="utf-8")
    # Record form and rotation (071 closed surface; the only authorized
    # amendment is the step enumeration, which C-10 owns — the rotation line
    # itself MUST read as before).
    assert "先把上一份记录归档为 `code-review-<YYYYMMDDTHHMMSSZ>.md`" in skill, (
        "the record rotation form MUST be preserved verbatim (C-53)"
    )
    # Receipt / report exit-code alphabets.
    assert "退出 0 允许 / 1 拒绝 / 2 输入错误" in skill, (
        "the summary gate's exit alphabet MUST be preserved verbatim (C-53)"
    )
    assert "退出 0 完整 / 1 覆盖缺口 / 2 不可评估" in skill, (
        "the receipt's exit alphabet MUST be preserved verbatim (C-53)"
    )
    # The receipt field block fence literals in the deterministic script.
    script = REVIEW_SCRIPT.read_text(encoding="utf-8")
    assert "RECEIPT_BEGIN_LITERAL='<!-- coverage-receipt:begin -->'" in script
    assert "RECEIPT_END_LITERAL='<!-- coverage-receipt:end -->'" in script, (
        "the receipt's field-block fence literals MUST be preserved verbatim (C-53)"
    )


def test_c53_report_code_subsection_field_list_closed():
    template = REVIEW_TEMPLATE.read_text(encoding="utf-8")
    subsection = template.split("### 2.1 Code Segment (Verdict and Pointers)", 1)[1]
    subsection = subsection.split("## ", 1)[0]
    fields = re.findall(r"(?m)^\|\s*([^|]+?)\s*\|\s*\[", subsection)
    expected = [
        "Base commit", "Head commit", "Base source", "Renderer mode",
        "Changed / judged / skipped / gap files", "Segment verdict", "Gate verdict",
        "Reason, when one applies", "Uncommitted scope", "Record", "Archive",
    ]
    assert fields == expected, (
        f"the report's code-subsection field list is a 071 closed surface and MUST "
        f"stay verbatim; drift: {fields!r} (C-53)"
    )


def test_c53_closing_step_set_and_three_unit_census_verbatim():
    template = REVIEW_COMMAND_TEMPLATE.read_text(encoding="utf-8")
    wrapup = re.split(r"(?m)^## Wrap-up\s*$", template)[1]
    wrapup = re.split(r"(?m)^## ", wrapup)[0]
    steps = re.findall(r"(?m)^\d+\.\s+(\w[^—`]*?)\s+—", wrapup)
    expected = ["Run Determination", "Exec Quant", "Feedback Record",
                "Threshold Notice", "Token Reflection", "Docs Sync Eval"]
    assert steps == expected, (
        f"the review command's closing-step set MUST stay the published six, verbatim; "
        f"drift: {steps!r} (C-53)"
    )
    skill = SKILL_MD.read_text(encoding="utf-8")
    assert "一次运行的单元普查为**三个单元**" in skill, (
        "the per-run three-unit census MUST be preserved verbatim (C-53)"
    )
    for unit in ("/speckit.review", "skill:review-sdd-process", "skill:code-review"):
        assert unit in skill
    # The single authorized amendment — the step enumeration — reads as five
    # steps with the deterministic capture fifth (owned in detail by C-10).
    assert "### 非交互路径（Agent / CI：五步，不是四步）" in skill


# --------------------------------------------------------------------------- #
# T024 / C-55 — no new /speckit.* command, no new CLI entry face
# --------------------------------------------------------------------------- #

def test_c55_no_new_command_template_or_entry_face():
    status = changed_name_status()
    for prefix in ("templates/commands/", ".claude/commands/", ".github/prompts/",
                   ".opencode/command/", ".qoder/commands/"):
        added_or_deleted = [s for s in status
                            if s.split("\t")[-1].startswith(prefix)
                            and not s.startswith("M")]
        assert not added_or_deleted, (
            f"C-55: no /speckit.* command may be added or removed; under {prefix!r}: "
            f"{added_or_deleted}"
        )


def test_c55_engine_faces_grow_by_exactly_the_two_authorized():
    # The review script's dispatch grows by exactly `capture`.
    base_dispatch = set(re.findall(
        r"(?m)^\s*(\w[\w-]*)\)\s+cmd_",
        baseline_text("skills/internal/code-review/scripts/git-delta-review.sh")))
    cur_dispatch = set(re.findall(
        r"(?m)^\s*(\w[\w-]*)\)\s+cmd_",
        REVIEW_SCRIPT.read_text(encoding="utf-8")))
    assert cur_dispatch - base_dispatch == {"capture"}, (
        f"C-55/C-62: the script may gain exactly the capture subcommand; "
        f"added {sorted(cur_dispatch - base_dispatch)}"
    )
    assert not base_dispatch - cur_dispatch, "no existing subcommand may be lost"
    # Its added long options are bounded to the authorized set.
    added_opts = set()
    for line in git("diff", f"{BASELINE_COMMIT}..HEAD", "--",
                    "skills/internal/code-review/scripts/git-delta-review.sh").splitlines():
        m = re.match(r"^\+\s*(--[a-z-]+)\)", line)
        if m:
            added_opts.add(m.group(1))
    assert added_opts <= {"--format", "--review-file", "--triage", "--unit"}, (
        f"C-55: added CLI options MUST be bounded to --format json / capture's own "
        f"parameters; found {sorted(added_opts)}"
    )
    # The feedback engine's --action alphabet grows by exactly client-metrics.
    base_actions = set(re.findall(
        r'"([a-z-]+)"',
        baseline_text("scripts/python/feedback-utils.py").split("choices=[", 1)[1].split("]", 1)[0]))
    cur_actions = set(re.findall(
        r'"([a-z-]+)"',
        FEEDBACK_ENGINE_SRC.read_text(encoding="utf-8").split("choices=[", 1)[1].split("]", 1)[0]))
    assert cur_actions - base_actions == {"client-metrics"}, (
        f"C-62: the feedback engine may gain exactly the read-only client-metrics "
        f"action; added {sorted(cur_actions - base_actions)}"
    )


# --------------------------------------------------------------------------- #
# T024 / C-56 — the edit surface is the framework sources only
# --------------------------------------------------------------------------- #

def test_c56_every_runtime_projection_change_has_a_source_change():
    status = [s.split("\t")[-1] for s in changed_name_status()]
    projection_prefixes = (".specify/scripts/", ".specify/shared/",
                           ".specify/skills/internal/")
    for rel in status:
        if rel.startswith(projection_prefixes):
            source = rel[len(".specify/"):]
            assert source in status, (
                f"C-56: runtime projection {rel} changed without its framework "
                f"source {source} changing — mirrors are generated, never hand-edited"
            )
    for rel in status:
        for prefix, template, suffix in (
            (".claude/commands/speckit.", "templates/commands/{}.md", ".md"),
            (".opencode/command/speckit.", "templates/commands/{}.md", ".md"),
            (".qoder/commands/speckit.", "templates/commands/{}.md", ".md"),
            (".github/prompts/speckit.", "templates/commands/{}.md", ".prompt.md"),
        ):
            if rel.startswith(prefix):
                name = rel[len(prefix):]
                assert name.endswith(suffix), f"unexpected copy name: {rel}"
                source = template.format(name[:-len(suffix)])
                assert source in status, (
                    f"C-56: per-tool command copy {rel} changed without its template "
                    f"{source} changing"
                )


def test_c56_changed_paths_stay_on_the_declared_edit_surface():
    status = [s.split("\t")[-1] for s in changed_name_status()]
    allowed_exact = {
        "scripts/python/feedback-utils.py",
        "scripts/python/probe-utils.py",
        "shared/guidelines/dogfooding.md",
        "shared/workflow/self-improvement-workflow.md",
        "skills/internal/code-review/SKILL.md",
        "skills/internal/code-review/scripts/git-delta-review.sh",
        "skills/internal/manage-feedback/SKILL.md",
        "skills/internal/manage-feedback/references/path-a-digest.md",
        "skills/internal/self-improvement/SKILL.md",
        "templates/commands/feedback.md",
        "templates/commands/improve.md",
        "templates/commands/review.md",
        # ID register is updated by review's REC-registration duty (071/063
        # obligations) — a legitimate project record, not a hand edit of
        # framework sources. Narrow exact entry; do NOT widen .specify/memory/.
        ".specify/memory/register.md",
    }
    allowed_prefixes = (
        "docs/reference/commands/",   # command reference docs (C-56)
        ".specify/specs/072-client-self-improvement/",   # this feature's spec artifacts
        ".specify/memory/features",    # feature registry rows (072 line + detail)
        ".specify/memory/exec-quant/records/",   # dogfooding loop records (new entries only)
        ".specify/memory/session/",                # dogfooding loop records (new entries only)
        ".specify/memory/feedback/",               # dogfooding loop records (new entries only)
        "tests/contract/", "tests/fixtures/",      # contract tests are the declared surface
        ".claude/commands/", ".github/prompts/",
        ".opencode/command/", ".qoder/commands/",  # per-tool copies (regenerated)
        ".specify/scripts/", ".specify/shared/",  # mirrors
        ".specify/skills/",  # all skill mirrors are produced by sync-mirrors (generated, never hand-edited)
    )
    offenders = []
    for rel in status:
        if rel in allowed_exact or rel.startswith(allowed_prefixes):
            continue
        if rel.startswith(".specify/scripts/"):
            continue
        offenders.append(rel)
    assert not offenders, (
        "C-56: files outside the declared framework-source edit surface were changed:\n"
        + "\n".join(offenders)
    )


# --------------------------------------------------------------------------- #
# T024 / C-57 — negative assertions verbatim, neutrality, guard counts grow
# --------------------------------------------------------------------------- #

def test_c57_two_negative_assertions_kept_verbatim():
    text = " ".join(MANAGE_FEEDBACK_SKILL.read_text(encoding="utf-8").split())
    assert "can never move an external entry upstream" in text, (
        "C-57: the negative assertion 'a client project's own feedback is never "
        "routed upstream' MUST be kept verbatim"
    )
    assert "which is the runtime mirror, not the source" in text, (
        "C-57: the negative assertion 'the hat criterion tests framework source "
        "directories rather than runtime mirrors' MUST be kept verbatim"
    )
    assert "Do NOT gate on `feedback/` directory existence" in text


def test_c57_shipped_text_adds_no_fresh_neutrality_violation():
    violations: Dict[str, List[str]] = {}
    for root_name in ("templates", "shared", "skills", "agents"):
        for path in (FRAMEWORK_ROOT / root_name).rglob("*"):
            if not path.is_file() or path.suffix not in {".md", ".py", ".sh", ".yaml", ".yml", ".json"}:
                continue
            rel = path.relative_to(FRAMEWORK_ROOT).as_posix()
            text = path.read_text(encoding="utf-8", errors="replace")
            for pattern in (
                re.compile(r"\b(?:req|requirement)\s+\d{3}\b", re.IGNORECASE),
                re.compile(r"\bFeature\s+\d{3}\b"),
                re.compile(r"\.specify/specs/\d{3}-"),
                re.compile(r"\.specify/memory/features/\d{3}"),
            ):
                if pattern.search(text):
                    violations.setdefault(rel, []).append(pattern.pattern)
    fresh = sorted(set(violations) - PRE_EXISTING_NEUTRALITY_DEBT)
    assert not fresh, (
        "C-57: Feature 072 shipped text introduced fresh framework-runtime "
        "references:\n" + "\n".join(fresh)
    )
    for rel in PRE_EXISTING_NEUTRALITY_DEBT:
        assert (FRAMEWORK_ROOT / rel).exists(), f"pre-existing debt entry stale: {rel}"


def test_c57_c61_guard_suite_assertion_counts_only_grow():
    for label, (files, floor) in GUARD_SUITES.items():
        total = 0
        for name in files:
            text = (FRAMEWORK_ROOT / "tests" / "contract" / name).read_text(encoding="utf-8")
            total += len(re.findall(r"(?m)^\s*def test_", text))
        assert total >= floor, (
            f"C-61: the {label} guard suite had {floor} tests at the T001 freeze and "
            f"MUST only grow; now {total}"
        )
    family = len([p for p in (FRAMEWORK_ROOT / "tests" / "contract").iterdir()
                  if p.name.startswith(("test_feedback_", "test_probe_"))])
    assert family >= FEEDBACK_PROBE_FAMILY_FLOOR, (
        f"C-61: the feedback/probe contract family had {FEEDBACK_PROBE_FAMILY_FLOOR} "
        f"files at the T001 freeze and MUST only grow; now {family}"
    )


# --------------------------------------------------------------------------- #
# T025 / C-58 — the five behavior groups execute inside the fixture only
# --------------------------------------------------------------------------- #

def test_c58_framework_repo_can_never_take_the_client_branch():
    assert hat_of(FRAMEWORK_ROOT) == "framework", (
        "C-58: the framework repository wears the framework hat by the owner "
        "criterion — which is exactly why client behavior is unverifiable by "
        "framework self-testing and needs the fixture"
    )


def test_c58_five_behavior_groups_run_inside_the_fixture():
    groups = [
        "test_client_capture.py",
        "test_client_armed_state.py",
        "test_client_package_exclusion.py",
        "test_client_improve_loop.py",
        "test_client_metrics.py",
    ]
    for name in groups:
        path = FRAMEWORK_ROOT / "tests" / "contract" / name
        tree = ast.parse(path.read_text(encoding="utf-8"))
        imported = set()
        called_in_tests = 0
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                imported.update(a.name for a in node.names)
            elif isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
                for sub in ast.walk(node):
                    if (isinstance(sub, ast.Call)
                            and isinstance(sub.func, ast.Name)
                            and sub.func.id in ("make_client_project",
                                                "make_framework_hat_twin")):
                        called_in_tests += 1
        assert "make_client_project" in imported, (
            f"C-58: {name} MUST drive the client fixture, not framework self-testing"
        )
        assert called_in_tests > 0, (
            f"C-58: {name} MUST execute its behavioral assertions inside a fixture "
            f"project (no make_client_project call inside any test function)"
        )


def test_c59_fixture_topology_both_hat_directions():
    with make_client_project() as project:
        assert project.hat == "client"
        assert project.framework_source_dirs_present == []
        assert (project.path / ".specify" / "scripts" / "python" / "feedback-utils.py").is_file()
        assert (project.path / ".specify" / "shared" / "definitions" / "probe-definitions.md").is_file()
        assert project.feedback_dir.is_dir()
        assert project.probe_registry_available()
    from fixtures.client_project import make_framework_hat_twin
    with make_framework_hat_twin() as twin:
        assert twin.hat == "framework"
        assert twin.framework_source_dirs_present == list(FRAMEWORK_SOURCE_DIRS)


# --------------------------------------------------------------------------- #
# T025 / C-59 — a client repo vending any one framework source dir takes the
# framework branch: the same capture flow adds zero external entries and
# discloses `skipped` with the hat owner citation, never a five-value token
# --------------------------------------------------------------------------- #

@pytest.mark.parametrize("vendored_dir", list(FRAMEWORK_SOURCE_DIRS))
def test_c59_vendored_framework_source_takes_the_framework_branch(vendored_dir):
    with make_client_project() as project:
        (project.path / vendored_dir).mkdir(parents=True, exist_ok=True)
        assert project.hat == "framework", (
            f"root ownership of {vendored_dir!r} MUST flip the hat to framework by "
            f"the owner criterion (C-59)"
        )
        project.arm(UNIT)
        qualified_run(project)
        run = armed_capture(project, "--unit", UNIT)
        assert run.returncode == 0, run.describe()
        assert external_count(project) == 0, (
            "the framework branch MUST gain zero external entries even when the "
            "channel is armed (C-59)"
        )
        lines = capture_lines(run.stdout)
        assert len(lines) == 1, lines
        line = lines[0]
        assert "skipped" in line and "hat=framework" in line, line
        assert HAT_OWNER_CITATION in line, (
            "the skip disclosure MUST cite the hat owner sentence basis (C-59), "
            f"got: {line}"
        )
        for token in FIVE_TOKENS:
            assert token not in line, (
                f"the framework-branch skip line MUST NOT mix into the five-value "
                f"closed set; found {token!r}"
            )


# --------------------------------------------------------------------------- #
# T026 / C-60 — no history rewrite; the legacy monolithic store stays read-only
# --------------------------------------------------------------------------- #

def test_c60_no_existing_feedback_entry_or_review_report_modified():
    modified_or_deleted = git(
        "diff", "--diff-filter=MD", "--name-only", f"{BASELINE_COMMIT}..HEAD", "--",
        ".specify/memory/feedback/", ".specify/review/",
    )
    assert modified_or_deleted == "", (
        "C-60: no existing review report or feedback entry may be modified or "
        f"deleted (no rewrite, no backfill):\n{modified_or_deleted}"
    )


def test_c60_legacy_monolithic_store_is_read_only_for_this_feature():
    with make_client_project() as project:
        legacy = project.feedback_dir / "index.json"
        legacy.write_text(json.dumps({"threshold": 5, "submitted_at": "2026-01-01T00:00:00Z"}),
                          encoding="utf-8")
        before = legacy.read_bytes()
        for argv in (
            ("feedback-utils.py", "--action", "list", "--format", "json"),
            ("feedback-utils.py", "--action", "client-metrics", "--format", "json"),
        ):
            run = project.run_engine(*argv, "--workspace-root", str(project.path))
            assert run.ok, run.describe()
        assert legacy.is_file(), (
            "C-60: the legacy monolithic store MUST NOT be retired by this "
            "feature's actions (read-only)"
        )
        assert legacy.read_bytes() == before, (
            "C-60: the legacy monolithic store MUST NOT be rewritten or backfilled "
            "by this feature's actions"
        )
        assert not (project.feedback_dir / "state").exists(), (
            "C-60: read-only actions of this feature MUST NOT materialize store "
            "state (no write point)"
        )


# --------------------------------------------------------------------------- #
# T026 / C-62 — engine additions bounded to exactly the two authorized faces
# --------------------------------------------------------------------------- #

def test_c62_no_new_engine_store_ledger_scoring_or_id_family():
    # No new engine / store / ledger files anywhere in the feature diff.
    added = git("diff", "--diff-filter=A", "--name-only", f"{BASELINE_COMMIT}..HEAD")
    banned_roots = ("scripts/", ".specify/scripts/", "src/")
    offenders = [p for p in added.splitlines() if p.startswith(banned_roots)]
    assert not offenders, (
        f"C-62: no new engine/store/ledger may be created; added under banned "
        f"roots:\n{offenders}"
    )
    # The feedback engine's added functions all serve the single read-only
    # client-metrics face (plus its metric helpers) — no second action, no
    # scoring system, no new id family.
    added_defs = set(re.findall(
        r"(?m)^\+def (\w+)",
        git("diff", f"{BASELINE_COMMIT}..HEAD", "--", "scripts/python/feedback-utils.py")))
    allowed_defs = {
        "_parse_iso_epoch", "_code_segment_record_stamps", "_entry_record_pointer",
        "_record_pairs", "_routing_backlog_rows", "_row_is_carried",
        "_row_owner_files_changed", "_not_evaluated", "_evaluated",
        "action_client_metrics",
    }
    assert added_defs <= allowed_defs, (
        f"C-62: unexpected new functions in the feedback engine (possible hidden "
        f"new face): {sorted(added_defs - allowed_defs)}"
    )
