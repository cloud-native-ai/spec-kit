"""Contract test: the code-review skill's own evolution (Feature 071).

Pins `contracts/code-review-skill.md` C-17…C-30 against the two surfaces that
carry them: `skills/internal/code-review/scripts/git-delta-review.sh` (the
deterministic entity every new capability must land on, C-30) and the skill body
plus its `references/` (the renderer-absence rewrite, C-22…C-25).

Group shape (the US2 band is the part that turns green first):

* **US2 band — C-17…C-21**, selected by ``-k us2``. Base resolution and its three
  tiers (explicit > first add of ``<spec>/requirements.md`` > merge base with the
  default trunk), the closed trunk-identification order with a negative case for
  each heuristic it forbids, the head rule (explicit ``--head``, else ``HEAD``
  read once and fixed for the run), the first-add instrument (never
  ``git log -1``), the refusal of a branch-name default, the four-step
  non-interactive enumeration read as four and not three, the single record
  header form, record creation and its archive rotation, and the code-path
  predicate behind the applicability triage in both directions plus the empty
  delta. Green points: T011 (``base``/``triage``) and T012 (``start``); T013 runs
  exactly this band.
* **US3 / boundary bands — C-22…C-25, C-26/C-27, C-29**, authored here in the same
  pass because they belong to this pinned file. Their green points are the US3
  rows (T016 rewrites the renderer clause and the evidence rule, T017 adds the
  explicit verdict input) and T031 (the sibling boundary) — T033/T036 for the
  final state. They are red until those rows land, which is their declared state.

What this file deliberately does NOT pin: the receipt block's grammar and its
closed exit alphabet (owner: `contracts/coverage-receipt.md`, pinned by
`tests/contract/test_coverage_receipt.py`), the composed command surface (owner:
`contracts/command-orchestration.md`), and the gate criteria (owner:
`templates/feature-details-template.md` § Canonical Status State Machine). A
second copy here would be the drift this feature exists to prevent.

Every case drives the real script inside a disposable git repository from
`tests/fixtures/review_git_repo.py` (T003), so the assertions are measured
against real git behaviour rather than against prose. The framework repository is
never written: the harness refuses a root inside it, and each invocation receives
an explicit ``cwd``, ``DELTA_BIN`` and ``REVIEW_DIR``.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from fixtures.review_git_repo import (
    FRAMEWORK_ROOT,
    RECEIPT_BEGIN,
    RECORD_FILENAME,
    REVIEW_SCRIPT_SOURCE,
    ReviewGitRepo,
    ScriptRun,
)

pytestmark = pytest.mark.contract

SKILL_BODY = (
    FRAMEWORK_ROOT / "skills" / "internal" / "code-review" / "SKILL.md"
)
SKILL_REFERENCES = FRAMEWORK_ROOT / "skills" / "internal" / "code-review" / "references"
DELTA_SETUP = SKILL_REFERENCES / "delta-setup.md"
SIBLING_BODY = (
    FRAMEWORK_ROOT / "skills" / "internal" / "review-sdd-process" / "SKILL.md"
)

#: `base_source` closed vocabulary, owned by data-model.md E5 (`base_sha`,
#: `head_sha`, `base_source`, `resolve_command`) and requirements FR-004.
TIER_EXPLICIT = "explicit"
TIER_FEATURE = "feature-first-commit"
TIER_TRUNK = "trunk-merge-base"
TIER_NONE = "not-evaluated"
BASE_SOURCES = (TIER_EXPLICIT, TIER_FEATURE, TIER_TRUNK, TIER_NONE)

#: The three applicability values, owned by requirements.md STR-005 / STR-001 /
#: STR-002 (referenced by name here, never redefined).
TRIAGE_RUN = "run"
TRIAGE_NOT_APPLICABLE = "not-applicable"
TRIAGE_NOT_EVALUATED = "not-evaluated"

#: The two legal `not-applicable` bases, owned by data-model.md E4 `basis`.
NOT_APPLICABLE_BASES = ("no code deliverable", "no committed code delta")
#: The basis an empty delta must carry (data-model.md V30).
EMPTY_DELTA_BASIS = "no committed code delta"

#: The closed forbidden-phrase list is owned by requirements.md SC-003. This file
#: searches those four literals **verbatim** and never a broad word such as
#: "render" or "review" — a broad match would red on legitimate prose and prove
#: nothing (contracts/code-review-skill.md C-23).
FORBIDDEN_PHRASES = (
    "已完成可视化评审",
    "rendered review complete",
    "visual review performed",
    "side-by-side review done",
)

#: `code-review-<YYYYMMDDTHHMMSSZ>.md` — data-model.md E11, FR-010.
ARCHIVE_RE = re.compile(r"^code-review-(\d{8}T\d{6}Z)\.md$")

#: The script's own legacy helper uses `<branch>-<YYYYMMDD-HHMMSS>.md` (local
#: time, dash form). That form MUST NOT be reused for an archive name
#: (research.md R6).
LEGACY_TIMESTAMP_RE = re.compile(r"^\d{8}-\d{6}$")

ANSI_RE = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #

@pytest.fixture()
def repo(tmp_path: Path) -> ReviewGitRepo:
    """A disposable git repository rooted in the case's own `tmp_path`.

    The harness refuses a root inside the framework tree, never changes the
    process working directory, and points `DELTA_BIN`/`REVIEW_DIR` explicitly, so
    no case can write the repository under test.
    """
    with ReviewGitRepo(root=tmp_path) as built:
        yield built


def _script_text() -> str:
    return REVIEW_SCRIPT_SOURCE.read_text(encoding="utf-8")


def _plain(text: str) -> str:
    return ANSI_RE.sub("", text)


def _flat(text: str) -> str:
    return re.sub(r"\s+", " ", text)


def _kv(source) -> dict:
    """Parse the script's `name=value` output lines (colours stripped)."""
    text = source.stdout if isinstance(source, ScriptRun) else source
    fields = {}
    for line in _plain(text).splitlines():
        match = re.match(r"^([a-z][a-z0-9_]*)=(.*)$", line.strip())
        if match:
            fields[match.group(1)] = match.group(2).strip()
    return fields


def _ok(run: ScriptRun) -> dict:
    assert run.returncode == 0, "expected a successful run:\n" + run.describe()
    return _kv(run)


def _spec(key: str) -> str:
    return f".specify/specs/{key}"


def _paragraphs(text: str) -> list:
    return [p for p in re.split(r"\n\s*\n", text) if p.strip()]


def _canonical_label(label: str) -> list:
    """Map a header-row label onto its canonical field token(s).

    English and Chinese labels are both accepted, because the script's existing
    record style is Chinese-published (`分支` / `基准` / `目标` / `Reviewer` /
    `日期`). What is pinned is the *order and content* of the fields, not the
    language of the label. A combined `Base / Head` row is expanded into its two
    fields, so both the one-row and the two-row shape satisfy C-21.
    """
    low = label.strip().strip("*").strip().lower()
    if "基准来源" in low or "base source" in low or "base_source" in low:
        return ["base source"]
    if "渲染" in low or "renderer" in low:
        return ["renderer"]
    if "reviewer" in low or "审阅" in low:
        return ["reviewer"]
    if "日期" in low or "date" in low:
        return ["date"]
    if "分支" in low or "branch" in low:
        return ["branch"]
    if ("基准" in low and "目标" in low) or ("base" in low and "head" in low):
        return ["base", "head"]
    if "基准" in low or low == "base":
        return ["base"]
    if "目标" in low or low == "head":
        return ["head"]
    return ["?" + low]


def _header_table(text: str) -> list:
    """The record's one header table as ordered `(canonical_fields, value)` rows."""
    rows = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            if rows:
                break
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        label = cells[0]
        bare = label.strip("*").strip()
        if not bare or set(bare) <= set("-: "):
            continue  # separator row
        if bare.lower() in {"attribute", "属性", "field", "字段"}:
            continue  # table heading row, not a field
        value = cells[1] if len(cells) > 1 else ""
        rows.append((_canonical_label(label), value))
    return rows


def _header_fields(text: str) -> dict:
    """Flatten `_header_table` into `{canonical field: value}` (first wins)."""
    fields = {}
    for names, value in _header_table(text):
        for name in names:
            fields.setdefault(name, value)
    return fields


def _header_order(text: str) -> list:
    order = []
    for names, _value in _header_table(text):
        order.extend(names)
    return order


def _bare(value: str) -> str:
    return value.replace("`", "").replace("*", "").strip()


def _standard(repo: ReviewGitRepo) -> dict:
    return repo.build_standard_history()


def _archive_path(repo: ReviewGitRepo, fields: dict) -> str:
    return _bare(fields.get("archive", ""))


# --------------------------------------------------------------------------- #
# US2 band — C-18: base resolution, three tiers, no branch-name default
# --------------------------------------------------------------------------- #

def test_us2_base_source_vocabulary_is_closed_and_reachable(repo: ReviewGitRepo):
    shapes = _standard(repo)
    seen = set()
    cases = (
        ("explicit", ("base", "--spec", _spec(repo.key), "--since", shapes["code"].base)),
        ("feature", ("base", "--spec", _spec(repo.key))),
        ("trunk", ("base", "--spec", _spec(repo.key) + "-absent")),
    )
    for label, argv in cases:
        fields = _ok(repo.run_script(*argv))
        assert fields.get("base_source") in BASE_SOURCES, (
            f"{label}: `base_source` MUST be one of {BASE_SOURCES}, "
            f"got {fields.get('base_source')!r}"
        )
        assert re.fullmatch(r"[0-9a-f]{40}", fields.get("base", "")), (
            f"{label}: `base=` MUST print a full commit id, got {fields.get('base')!r}"
        )
        assert re.fullmatch(r"[0-9a-f]{40}", fields.get("head", "")), (
            f"{label}: `head=` MUST print a full commit id, got {fields.get('head')!r}"
        )
        seen.add(fields["base_source"])
    assert seen == {TIER_EXPLICIT, TIER_FEATURE, TIER_TRUNK}, (
        "all three base tiers MUST be reachable; reached " + repr(sorted(seen))
    )


def test_us2_an_explicit_base_wins_the_first_tier(repo: ReviewGitRepo):
    shapes = _standard(repo)
    fields = _ok(
        repo.run_script("base", "--spec", _spec(repo.key), "--since", shapes["code"].base)
    )
    assert fields["base_source"] == TIER_EXPLICIT
    assert fields["base"] == shapes["code"].base
    assert fields["head"] == repo.head, "no `--head` was given, so head is the run-start HEAD"


def test_us2_the_feature_tier_uses_the_first_add_and_not_the_latest_commit(repo: ReviewGitRepo):
    _standard(repo)
    fields = _ok(repo.run_script("base", "--spec", _spec(repo.key)))
    assert fields["base_source"] == TIER_FEATURE
    assert fields["base"] == repo.commits["seed"], (
        "the feature-slice base MUST be the parent of the commit that FIRST added "
        "`<spec>/requirements.md` (the seed commit here). A `git log -1` over the "
        f"spec directory would have produced {repo.commits['feature']!r} instead, "
        "because the newest commit touching that directory is the later "
        "spec-only commit."
    )
    assert fields["base"] != repo.commits["feature"], (
        "the latest-commit-over-the-directory reading MUST NOT be used (C-19)"
    )
    # The discriminating history is real: the spec directory has a later commit
    # than the requirements.md add.
    later = repo.git(
        "log", "--format=%H", "--", f".specify/specs/{repo.key}"
    ).stdout.split()
    assert later[0] == repo.commits["spec_only"], (
        "fixture precondition: the newest commit over the spec directory is the "
        f"spec-only commit, got {later[:1]}"
    )


def test_us2_the_same_repository_state_resolves_the_same_base_twice(repo: ReviewGitRepo):
    _standard(repo)
    first = _ok(repo.run_script("base", "--spec", _spec(repo.key)))
    second = _ok(repo.run_script("base", "--spec", _spec(repo.key)))
    assert (first["base"], first["head"], first["base_source"]) == (
        second["base"],
        second["head"],
        second["base_source"],
    ), "FR-022: the same repository state MUST resolve the same base on every run"


def test_us2_the_feature_tier_never_consults_the_scripts_builtin_default(repo: ReviewGitRepo):
    _standard(repo)
    # `master` does not exist in this repository, so a resolver that fell back to
    # the script's `GIT_BASE` default would either fail or resolve elsewhere.
    fields = _ok(
        repo.run_script("base", "--spec", _spec(repo.key), extra_env={"GIT_BASE": "master"})
    )
    assert fields["base_source"] == TIER_FEATURE
    assert fields["base"] == repo.commits["seed"]


def test_us2_the_trunk_tier_is_reached_only_after_the_feature_tier(repo: ReviewGitRepo):
    _standard(repo)
    fields = _ok(repo.run_script("base", "--spec", _spec(repo.key) + "-absent"))
    assert fields["base_source"] == TIER_TRUNK
    merge_base = repo.git("merge-base", "main", "HEAD").stdout.strip()
    assert fields["base"] == merge_base, (
        "the third tier is the merge base with the repository's default trunk"
    )


def test_us2_no_tier_resolves_to_not_evaluated_with_the_failing_command(repo: ReviewGitRepo):
    # Only `trunk` and `work` exist: no `--trunk`, no `refs/remotes/origin/HEAD`,
    # no `main`, no `master`.
    repo.create()
    repo.write("README.md", "# seed\n")
    repo.commit("chore: seed", ["README.md"])
    repo.git("branch", "-m", "main", "trunk")
    repo.git("checkout", "-q", "-b", "work")
    repo.write("work.txt", "work\n")
    repo.commit("feat: work", ["work.txt"])

    run = repo.run_script("base", "--spec", _spec("absent"))
    assert run.returncode == 2, (
        "an unresolvable base MUST exit 2 (cannot evaluate), not 0 or 1:\n"
        + run.describe()
    )
    fields = _kv(run)
    assert fields.get("base_source") == TIER_NONE, (
        "an unresolvable base MUST be recorded as `not-evaluated` (STR-002)"
    )
    assert fields.get("reason"), "`not-evaluated` MUST carry its failure reason (C-20)"
    assert fields.get("resolve_command"), (
        "`not-evaluated` MUST carry a reproducible command (C-20 / E5 `resolve_command`)"
    )
    assert "base" not in fields, "no guessed base may be printed"


def test_us2_a_trunk_shaped_branch_participates_only_when_explicitly_named(repo: ReviewGitRepo):
    repo.create()
    repo.write("README.md", "# seed\n")
    repo.commit("chore: seed", ["README.md"])
    repo.git("branch", "-m", "main", "trunk")
    repo.git("checkout", "-q", "-b", "work")
    repo.write("work.txt", "work\n")
    repo.commit("feat: work", ["work.txt"])

    unnamed = repo.run_script("base", "--spec", _spec("absent"))
    assert unnamed.returncode == 2, (
        "a branch that merely LOOKS like a trunk MUST NOT be picked by a heuristic "
        "outside the closed order (C-18):\n" + unnamed.describe()
    )
    named = _ok(repo.run_script("base", "--spec", _spec("absent"), "--trunk", "trunk"))
    assert named["base_source"] == TIER_TRUNK
    assert named["base"] == repo.git("merge-base", "trunk", "HEAD").stdout.strip()


def test_us2_trunk_order_ignores_the_remote_origin_happens_to_point_at(repo: ReviewGitRepo):
    """The forbidden heuristic: "whatever branch `origin` points at"."""
    repo.create()
    repo.write("README.md", "# seed\n")
    seed = repo.commit("chore: seed", ["README.md"])  # main tip
    repo.git("checkout", "-q", "-b", "hot")
    repo.write("hot.txt", "hot\n")
    hot = repo.commit("feat: hot", ["hot.txt"])  # newer than main
    repo.git("remote", "add", "origin", "https://example.invalid/upstream.git")
    repo.git("update-ref", "refs/remotes/origin/develop", hot)
    assert repo.git(
        "rev-parse", "--verify", "--quiet", "refs/remotes/origin/HEAD", check=False
    ).returncode != 0, "fixture precondition: origin/HEAD is not resolvable here"

    fields = _ok(repo.run_script("base", "--spec", _spec("absent")))
    assert fields["base_source"] == TIER_TRUNK
    assert fields["base"] == repo.git("merge-base", "main", "HEAD").stdout.strip() == seed
    assert fields["base"] != hot, (
        "the base MUST NOT be derived from the remote's most advanced branch — that "
        "is the open heuristic the closed order forbids"
    )


def test_us2_trunk_order_ignores_the_most_recently_active_branch(repo: ReviewGitRepo):
    repo.create()
    repo.write("README.md", "# seed\n")
    seed = repo.commit("chore: seed", ["README.md"])  # main tip
    repo.git("checkout", "-q", "-b", "hot")
    repo.write("hot.txt", "hot\n")
    hot = repo.commit("feat: hot", ["hot.txt"])  # most recently active = HEAD

    fields = _ok(repo.run_script("base", "--spec", _spec("absent")))
    assert fields["base"] == seed, (
        "the trunk tier is `main` by the closed order, not the branch that moved "
        f"last (which would have produced {hot})"
    )


def test_us2_trunk_order_prefers_a_resolvable_origin_head_over_a_local_main(repo: ReviewGitRepo):
    repo.create()
    repo.write("README.md", "# seed\n")
    seed = repo.commit("chore: seed", ["README.md"])
    repo.git("checkout", "-q", "-b", "develop")
    repo.write("develop.txt", "develop\n")
    develop = repo.commit("feat: develop", ["develop.txt"])
    repo.git("checkout", "-q", "main")
    repo.write("main.txt", "main\n")
    main_tip = repo.commit("feat: main moves on", ["main.txt"])
    repo.git("update-ref", "refs/remotes/origin/HEAD", develop)

    fields = _ok(repo.run_script("base", "--spec", _spec("absent")))
    assert fields["base_source"] == TIER_TRUNK
    assert fields["base"] == repo.git("merge-base", "develop", "HEAD").stdout.strip() == seed
    assert fields["base"] != main_tip, (
        "a resolvable `refs/remotes/origin/HEAD` is tier 2 and MUST beat the local "
        "`main` (tier 3)"
    )


def test_us2_an_explicit_trunk_beats_a_resolvable_origin_head(repo: ReviewGitRepo):
    repo.create()
    repo.write("README.md", "# seed\n")
    seed = repo.commit("chore: seed", ["README.md"])
    repo.git("checkout", "-q", "-b", "develop")
    repo.write("develop.txt", "develop\n")
    develop = repo.commit("feat: develop", ["develop.txt"])
    repo.git("checkout", "-q", "main")
    repo.write("main.txt", "main\n")
    main_tip = repo.commit("feat: main moves on", ["main.txt"])
    repo.git("update-ref", "refs/remotes/origin/HEAD", develop)

    fields = _ok(repo.run_script("base", "--spec", _spec("absent"), "--trunk", "main"))
    assert fields["base_source"] == TIER_TRUNK
    assert fields["base"] == main_tip, (
        "an explicit `--trunk` is tier 1 of the closed order and MUST beat the "
        f"resolvable origin/HEAD (which would have yielded {seed})"
    )


def test_us2_head_is_the_explicit_value_when_given(repo: ReviewGitRepo):
    shapes = _standard(repo)
    fields = _ok(
        repo.run_script("base", "--spec", _spec(repo.key), "--head", shapes["code"].head)
    )
    assert fields["head"] == shapes["code"].head
    assert "head_source" not in fields, (
        "head carries no source tier — two forms, no ordered search (data-model.md V31)"
    )


def test_us2_head_is_read_once_and_fixed_for_the_whole_run(repo: ReviewGitRepo):
    shapes = _standard(repo)
    pinned = _ok(repo.run_script("base", "--spec", _spec(repo.key)))["head"]
    repo.write("src/late.py", "LATE = 1\n")
    late = repo.commit("feat: lands mid-run", ["src/late.py"])
    assert late != pinned, "fixture precondition: a commit landed after the head was read"

    fields = _ok(repo.run_script("start", "--spec", _spec(repo.key), "--head", pinned))
    assert fields["head"] == pinned, (
        "the record MUST carry the head fixed at run start, not a later read of HEAD"
    )
    record = repo.record_path.read_text(encoding="utf-8")
    assert pinned in record and repo.short(pinned) in record
    assert late not in record, (
        "a commit that landed mid-run MUST NOT enter the reviewed range (C-18/C-21)"
    )


def test_us2_base_offers_a_machine_readable_form(repo: ReviewGitRepo):
    _standard(repo)
    run = repo.run_script("base", "--spec", _spec(repo.key), "--json")
    assert run.returncode == 0, run.describe()
    payload = json.loads(_plain(run.stdout))
    for key in ("base", "head", "base_source"):
        assert key in payload, f"the JSON form MUST carry {key!r}; got {sorted(payload)}"
    assert payload["base_source"] in BASE_SOURCES


def test_us2_the_feature_tier_never_derives_from_the_latest_commit_over_the_spec():
    script = _script_text()
    assert "--diff-filter=A" in script, (
        "the feature-slice tier MUST use the first-add instrument (C-19)"
    )
    assert re.search(r"--diff-filter=A[^\n]*requirements\.md", script), (
        "the instrument MUST target `<spec>/requirements.md`"
    )
    executable = "\n".join(
        line for line in script.splitlines() if not line.lstrip().startswith("#")
    )
    assert "git log -1" not in executable, (
        "`git log -1` over the spec directory is the instrument C-19 forbids; the "
        "check ignores comments so a comment may still name it"
    )


# --------------------------------------------------------------------------- #
# US2 band — C-17: the four-step non-interactive path
# --------------------------------------------------------------------------- #

def test_us2_the_non_interactive_path_is_four_steps_read_as_four(repo: ReviewGitRepo):
    run = repo.run_script("--help")
    assert run.returncode == 0, run.describe()
    help_text = _plain(run.stdout)

    steps = re.findall(r"(?m)^\s*([1-4])\.\s+(\S+)", help_text)
    assert [word for _n, word in steps] == ["base", "start", "note", "receipt"], (
        "the non-interactive path MUST be enumerated as four steps in this order — "
        "base resolution, record creation/rotation, opinion capture, receipt and "
        f"verdict; found {steps!r}"
    )
    assert re.search(r"(?i)four steps", help_text), (
        "the enumeration MUST be readable as four, not three (C-17)"
    )
    assert re.search(r"(?i)rotat", help_text), (
        "record creation and rotation is a REQUIRED step from the second run on — "
        "calling it out is what makes the enumeration four rather than three"
    )
    for subcommand in ("base", "start", "note"):
        assert re.search(rf"(?m)^\s+{subcommand}\s", help_text), (
            f"step {subcommand!r} MUST be documented as a subcommand, not only as a "
            "numbered line"
        )
    # `receipt` (step 4) gets its COMMANDS entry with its implementation (T015); the
    # four-step declaration above is what C-17 requires of this file, and group 4
    # (`test_coverage_receipt.py`) owns its behaviour.


def test_us2_base_start_and_note_complete_without_a_prompt_or_a_tty(repo: ReviewGitRepo):
    shapes = _standard(repo)
    # `receipt` (step 4) lands with the coverage receipt; its non-interactive
    # reachability is pinned by `tests/contract/test_coverage_receipt.py` (T014/T018).
    runs = (
        repo.run_script("base", "--spec", _spec(repo.key)),
        repo.run_script(
            "triage", "--since", shapes["code"].base, "--head", shapes["code"].head
        ),
        repo.run_script("start", "--spec", _spec(repo.key)),
        repo.run_script(
            "note",
            "-s",
            "suggestion",
            "-f",
            "src/fixture_demo.py",
            "-c",
            "non-interactive capture",
            "--review-file",
            str(repo.record_path),
        ),
    )
    for run in runs:
        assert run.returncode == 0, (
            "no step may require an answer to a prompt or a manufactured terminal:\n"
            + run.describe()
        )
        assert "操作 [" not in _plain(run.stdout), (
            "the non-interactive path MUST NOT print the interactive per-file prompt"
        )


def test_us2_additional_subcommands_do_not_break_the_existing_closed_loop(repo: ReviewGitRepo):
    shapes = _standard(repo)
    help_text = _plain(repo.run_script("--help").stdout)
    for existing in ("diff", "review", "note", "report"):
        assert re.search(rf"(?m)^\s+{existing}\b", help_text), (
            f"the pre-existing {existing!r} subcommand MUST stay documented (C-28)"
        )
    stat = repo.run_script(
        "diff", "--stat", "--since", shapes["code"].base, "--head", shapes["code"].head
    )
    assert stat.returncode == 0 and repo.CODE_PATH in stat.stdout


# --------------------------------------------------------------------------- #
# US2 band — C-21: the single record header form
# --------------------------------------------------------------------------- #

def test_us2_the_record_header_has_one_form_in_a_fixed_field_order(repo: ReviewGitRepo):
    shapes = _standard(repo)
    fields = _ok(repo.run_script("start", "--spec", _spec(repo.key)))
    record = repo.record_path.read_text(encoding="utf-8")

    assert _header_order(record) == [
        "branch",
        "base",
        "head",
        "base source",
        "renderer",
        "reviewer",
        "date",
    ], (
        "the record MUST carry exactly one header form, in this field order (C-21 / "
        f"data-model.md E6); found {_header_order(record)!r}"
    )

    header = _header_fields(record)
    assert _bare(header["base"]).startswith(fields["base"]), (
        "the header's base MUST be the resolved base id"
    )
    assert repo.short(fields["base"]) in header["base"], (
        "the header MUST carry both the full and the short form of the base"
    )
    assert fields["head"] in header["head"] and repo.short(fields["head"]) in header["head"], (
        "the header MUST carry both the full and the short form of the head"
    )
    assert _bare(header["base source"]) in (TIER_EXPLICIT, TIER_FEATURE, TIER_TRUNK)
    assert _bare(header["renderer"]) in ("renderer: text", "renderer: delta"), (
        "the renderer field carries the marker literal (STR-003 / STR-008), got "
        f"{header['renderer']!r}"
    )
    assert _bare(header["branch"]), "the header MUST name the branch"
    assert _bare(header["reviewer"]), "the header MUST name the reviewer"
    assert _bare(header["date"]), "the header MUST carry the run date"


def test_us2_start_reports_the_range_the_base_step_resolved(repo: ReviewGitRepo):
    _standard(repo)
    base_step = _ok(repo.run_script("base", "--spec", _spec(repo.key)))
    start_step = _ok(repo.run_script("start", "--spec", _spec(repo.key)))
    assert (
        start_step["base"],
        start_step["head"],
        start_step["base_source"],
    ) == (
        base_step["base"],
        base_step["head"],
        base_step["base_source"],
    ), "the record MUST be created over the range the resolution step produced"
    assert _bare(start_step["record"]).endswith(RECORD_FILENAME)


# --------------------------------------------------------------------------- #
# US2 band — record creation, rotation, and the same-second disposition
# --------------------------------------------------------------------------- #

def test_us2_a_first_run_creates_the_record_and_reports_no_archive(repo: ReviewGitRepo):
    _standard(repo)
    fields = _ok(repo.run_script("start", "--spec", _spec(repo.key)))
    assert repo.record_path.is_file()
    assert _bare(fields["archive"]) == "none", (
        "a first run has nothing to rotate and records STR-009 (`none`), never an "
        f"empty field; got {fields.get('archive')!r}"
    )
    assert repo.archives() == []


def test_us2_a_rerun_rotates_the_previous_record_under_the_utc_second_form(repo: ReviewGitRepo):
    _standard(repo)
    _ok(repo.run_script("start", "--spec", _spec(repo.key)))
    noted = repo.run_script(
        "note",
        "-s",
        "blocking",
        "-f",
        "src/fixture_demo.py",
        "-c",
        "kept across the rotation",
        "--review-file",
        str(repo.record_path),
    )
    assert noted.returncode == 0, noted.describe()

    fields = _ok(repo.run_script("start", "--spec", _spec(repo.key)))
    archives = repo.archives()
    assert len(archives) == 1, f"exactly one archive per re-run, found {archives!r}"
    assert ARCHIVE_RE.match(archives[0].name), (
        "the archive name MUST be `code-review-<YYYYMMDDTHHMMSSZ>.md` (UTC, second "
        f"resolution), got {archives[0].name!r}"
    )
    stamp = ARCHIVE_RE.match(archives[0].name).group(1)
    assert not LEGACY_TIMESTAMP_RE.match(stamp), (
        "the interactive helper's local dash form MUST NOT be reused (research.md R6)"
    )
    assert Path(_archive_path(repo, fields)).name == archives[0].name, (
        "the run MUST report the archive path it produced"
    )
    assert "kept across the rotation" in archives[0].read_text(encoding="utf-8"), (
        "the previous record MUST be preserved, not lost"
    )
    assert "kept across the rotation" not in repo.record_path.read_text(encoding="utf-8"), (
        "the stable name always denotes the latest run"
    )


def test_us2_a_same_second_rerun_never_overwrites_an_archive(repo: ReviewGitRepo):
    _standard(repo)
    _ok(repo.run_script("start", "--spec", _spec(repo.key)))
    first_body = repo.record_path.read_text(encoding="utf-8")

    pinned = "20261027T061144Z"
    collision = repo.spec_dir / f"code-review-{pinned}.md"
    collision.write_text("# existing archive - never overwritten\n", encoding="utf-8")
    before = collision.read_bytes()

    run = repo.run_script(
        "start", "--spec", _spec(repo.key), extra_env={"REVIEW_RUN_TIMESTAMP": pinned}
    )
    assert collision.read_bytes() == before, (
        "an existing archive MUST never be overwritten, whatever disposition the "
        "run takes (V12)"
    )
    assert repo.record_path.is_file(), (
        "a refused rotation MUST NOT destroy the record it could not archive"
    )
    if run.returncode == 2:
        assert "archive" in _plain(run.stdout + run.stderr).lower(), (
            "the exit-2 disposition MUST name its reason:\n" + run.describe()
        )
        assert repo.record_path.read_text(encoding="utf-8") == first_body, (
            "a refused rotation MUST leave the previous record intact"
        )
    else:
        assert run.returncode == 0, run.describe()
        produced = _archive_path(repo, _kv(run))
        assert produced != "none" and Path(produced).name != collision.name, (
            "the alternative legal disposition waits for a different second and "
            f"archives elsewhere; got {produced!r}"
        )


def test_us2_a_triage_value_other_than_run_creates_no_record(repo: ReviewGitRepo):
    _standard(repo)
    for value in (TRIAGE_NOT_APPLICABLE, TRIAGE_NOT_EVALUATED):
        run = repo.run_script("start", "--spec", _spec(repo.key), "--triage", value)
        assert run.returncode != 0, (
            f"`start --triage {value}` MUST refuse to create a record (C-11/V29):\n"
            + run.describe()
        )
        assert not repo.record_path.exists(), (
            f"triage {value!r} MUST write no record file, not even an empty one"
        )
        assert value in _plain(run.stdout + run.stderr), (
            "the refusal MUST name the triage value it refused"
        )


# --------------------------------------------------------------------------- #
# US2 band — the code-path predicate and the empty-delta answer
# --------------------------------------------------------------------------- #

def test_us2_triage_runs_when_the_delta_contains_a_code_path(repo: ReviewGitRepo):
    shapes = _standard(repo)
    fields = _ok(
        repo.run_script(
            "triage",
            "--since",
            shapes["code"].base,
            "--head",
            shapes["code"].head,
        )
    )
    assert fields["triage"] == TRIAGE_RUN
    assert int(fields["changed_files"]) == 2, (
        f"the code shape has two changed files, got {fields.get('changed_files')!r}"
    )


def test_us2_triage_is_not_applicable_for_a_spec_only_delta(repo: ReviewGitRepo):
    shapes = _standard(repo)
    fields = _ok(
        repo.run_script(
            "triage",
            "--since",
            shapes["spec-only"].base,
            "--head",
            shapes["spec-only"].head,
        )
    )
    assert fields["triage"] == TRIAGE_NOT_APPLICABLE
    assert int(fields["changed_files"]) == 1
    assert any(basis in fields.get("basis", "") for basis in NOT_APPLICABLE_BASES), (
        "a `not-applicable` triage MUST carry one of the two legal bases (E4), got "
        f"{fields.get('basis')!r}"
    )
    assert not repo.record_path.exists(), "only `run` writes a record"


def test_us2_triage_answers_an_empty_delta_before_any_receipt_runs(repo: ReviewGitRepo):
    shapes = _standard(repo)
    run = repo.run_script(
        "triage", "--since", shapes["empty"].base, "--head", shapes["empty"].head
    )
    fields = _ok(run)
    assert fields["triage"] == TRIAGE_NOT_APPLICABLE, (
        "an empty delta is triaged as not-applicable, never as a clean review (V30)"
    )
    assert int(fields["changed_files"]) == 0
    assert EMPTY_DELTA_BASIS in fields.get("basis", ""), (
        f"the empty-delta basis is {EMPTY_DELTA_BASIS!r}, got {fields.get('basis')!r}"
    )
    assert RECEIPT_BEGIN not in run.stdout, (
        "the empty delta MUST be answered before any receipt block is produced"
    )
    assert not repo.record_path.exists()
    assert "verdict" not in fields, "no segment verdict may be derived over nothing"


def test_us2_the_default_code_path_set_treats_docs_and_memory_as_non_code(repo: ReviewGitRepo):
    shapes = _standard(repo)
    repo.write("docs/notes.md", "# docs only\n")
    repo.write(".specify/memory/knowledge/note.md", "# memory only\n")
    docs_only = repo.commit(
        "docs: documentation and memory only",
        ["docs/notes.md", ".specify/memory/knowledge/note.md"],
    )
    fields = _ok(
        repo.run_script(
            "triage", "--since", shapes["spec-only"].head, "--head", docs_only
        )
    )
    assert fields["triage"] == TRIAGE_NOT_APPLICABLE, (
        "documentation, spec, and memory paths are expressly not code paths; the "
        "closed default set lives in this script and nowhere else"
    )


def test_us2_the_code_paths_override_narrows_the_predicate(repo: ReviewGitRepo):
    shapes = _standard(repo)
    fields = _ok(
        repo.run_script(
            "triage",
            "--since",
            shapes["code"].base,
            "--head",
            shapes["code"].head,
            "--code-paths",
            "tests/**",
        )
    )
    assert fields["triage"] == TRIAGE_NOT_APPLICABLE, (
        "the same delta MUST be judged by the caller's set: with `--code-paths "
        "tests/**` the `src/` file no longer counts as code"
    )
    assert any(basis in fields.get("basis", "") for basis in NOT_APPLICABLE_BASES)


def test_us2_the_code_paths_override_widens_the_predicate(repo: ReviewGitRepo):
    shapes = _standard(repo)
    fields = _ok(
        repo.run_script(
            "triage",
            "--since",
            shapes["spec-only"].base,
            "--head",
            shapes["spec-only"].head,
            "--code-paths",
            ".specify/specs/**",
        )
    )
    assert fields["triage"] == TRIAGE_RUN, (
        "the override works in both directions: a spec-only delta counts as code "
        "when the caller says so"
    )


def test_us2_triage_reports_not_evaluated_when_the_range_cannot_resolve(repo: ReviewGitRepo):
    _standard(repo)
    run = repo.run_script("triage", "--since", "does-not-exist", "--head", "HEAD")
    assert run.returncode == 2, (
        "an unusable range is `not-evaluated` with exit 2, never a silent "
        "`not-applicable`:\n" + run.describe()
    )
    fields = _kv(run)
    assert fields.get("triage") == TRIAGE_NOT_EVALUATED
    assert fields.get("reason"), "`not-evaluated` MUST carry its reason (E4)"
    assert not repo.record_path.exists()


# --------------------------------------------------------------------------- #
# C-22 — mode selection: the renderer AND a TTY, never availability alone
# --------------------------------------------------------------------------- #

def test_c22_the_rendered_marker_needs_the_renderer_and_a_terminal(repo: ReviewGitRepo):
    _standard(repo)
    host_delta = ReviewGitRepo.host_delta_bin()
    _ok(
        repo.run_script(
            "start",
            "--spec",
            _spec(repo.key),
            delta_bin=host_delta or repo.missing_delta_bin,
        )
    )
    record = repo.record_path.read_text(encoding="utf-8")
    marker = _bare(_header_fields(record)["renderer"])
    assert marker == "renderer: text", (
        "a call whose stdout is a pipe MUST take text mode even when the renderer "
        f"is installed (this host: {host_delta or 'delta absent'}); got {marker!r}"
    )
    assert "renderer: delta" not in record
    for phrase in FORBIDDEN_PHRASES:
        assert phrase not in record
    assert re.search(r"\[\[\s*-t\s+1\s*\]\]", _script_text()), (
        "the two-conditioned rule lives in the script and MUST test stdout's "
        "terminal-ness, not only the binary's presence"
    )
    body = _flat(SKILL_BODY.read_text(encoding="utf-8"))
    for literal in ("renderer: text", "renderer: delta"):
        assert literal in body, (
            "the skill body MUST carry both mode markers verbatim (STR-003 / STR-008): "
            f"{literal!r} is missing"
        )
    assert re.search(r"(?i)tty|交互终端", body), (
        "the skill body MUST state the second condition — stdout is an interactive "
        "terminal — because availability alone must not select the rendered mode"
    )


# --------------------------------------------------------------------------- #
# C-23 / C-24 / C-25 — the renderer-absence rewrite and the evidence rule
# --------------------------------------------------------------------------- #

def test_c23_the_four_forbidden_phrases_are_quoted_verbatim_as_a_prohibition():
    body = SKILL_BODY.read_text(encoding="utf-8")
    for phrase in FORBIDDEN_PHRASES:
        holders = [p for p in _paragraphs(body) if phrase in p]
        assert holders, (
            "the closed four-phrase prohibition (owner: requirements.md SC-003) MUST "
            f"quote {phrase!r} verbatim in the skill body; a broad word such as "
            "'render' is not a substitute"
        )
        assert any(
            re.search(r"禁止|不得|禁用|MUST NOT|must not|never", p) for p in holders
        ), f"{phrase!r} appears without a prohibition marker around it"


def test_c24_the_renderer_absence_clause_is_rewritten_not_deleted():
    body = SKILL_BODY.read_text(encoding="utf-8")
    setup = DELTA_SETUP.read_text(encoding="utf-8")

    for residue in ("环境缺失即停", "报错并给出安装命令后停止", "缺失时报错 + 安装指引，停止执行"):
        assert residue not in _flat(body), (
            f"no surface may retain the replaced 'stop when the renderer is missing' "
            f"assertion; found {residue!r}"
        )
    assert "命令后停止" not in _flat(body), (
        "the Phase 0 environment step MUST be rewritten as well, not left behind (C-24)"
    )

    rewrite = [
        p
        for p in _paragraphs(body)
        if re.search(r"覆盖率回执|coverage receipt", p) and re.search(r"替代|replac", p)
    ]
    assert rewrite, (
        "the skill MUST keep ONE statement naming the replaced clause, its substitute "
        "evidence form (the coverage receipt), and the reason for the replacement"
    )
    assert any(re.search(r"理由|因为|reason", p) for p in rewrite), (
        "the rewrite MUST state the reason, not only the substitution"
    )

    assert "报错 + 给出安装命令后停止" not in _flat(setup), (
        "the same rewrite MUST reach the `references/` wording (C-24)"
    )
    assert re.search(r"回执|receipt", setup), (
        "the references wording MUST name the substitute evidence form"
    )
    assert "不自动安装" in body, (
        "the neighbouring invariant survives verbatim: the skill never installs the "
        "renderer itself, and the path is announced with an install pointer"
    )
    assert re.search(r"delta-setup", body), "the install pointer MUST survive the rewrite"


def test_c25_the_receipt_is_the_only_evidence_form_for_reading_the_whole_diff():
    body = SKILL_BODY.read_text(encoding="utf-8")
    holders = [
        p
        for p in _paragraphs(body)
        if re.search(r"覆盖率回执|coverage receipt", p)
        and re.search(r"唯一|only|sole", p)
    ]
    assert holders, (
        "the skill MUST declare the coverage receipt the single evidence form for "
        "'the whole diff was read' (C-25)"
    )
    paragraph = _flat(" ".join(holders))
    substitutes = ("概览", "文件列表", "行数", "工具输出")
    named = [word for word in substitutes if word in paragraph]
    assert len(named) >= 3, (
        "the rule MUST name the substitutes it rejects — a diff overview, a "
        "changed-file listing, a small changed-line count, the mere existence of "
        f"tool output; found {named!r}"
    )


# --------------------------------------------------------------------------- #
# C-26 / C-27 — one verdict source, taking the record path explicitly
# --------------------------------------------------------------------------- #

def test_c26_the_verdict_keeps_the_script_as_its_only_source(repo: ReviewGitRepo):
    _standard(repo)
    _ok(repo.run_script("start", "--spec", _spec(repo.key)))

    allow = repo.run_script("report", "--summary", "--file", str(repo.record_path))
    assert allow.returncode == 0, (
        "a record with no `blocking` entry MUST allow (exit 0):\n" + allow.describe()
    )

    noted = repo.run_script(
        "note",
        "-s",
        "blocking",
        "-f",
        "src/fixture_demo.py",
        "-c",
        "a real defect",
        "--review-file",
        str(repo.record_path),
    )
    assert noted.returncode == 0, noted.describe()
    deny = repo.run_script("report", "--summary", "--file", str(repo.record_path))
    assert deny.returncode == 1, (
        "a current record carrying one `blocking` entry MUST deny with exit 1:\n"
        + deny.describe()
    )
    assert "1" in _plain(deny.stdout), "the denial MUST name the count"

    missing = repo.run_script(
        "report", "--summary", "--file", str(repo.spec_dir / "absent-record.md")
    )
    assert missing.returncode == 2, (
        "an input error MUST be exit 2, never confused with the deny code:\n"
        + missing.describe()
    )


def test_c27_an_omitted_record_path_labels_its_selection_as_implicit(repo: ReviewGitRepo):
    _standard(repo)
    _ok(repo.run_script("start", "--spec", _spec(repo.key)))
    # The feature directory holds both `review.md` and `code-review.md`; the legacy
    # newest-file selection must say so rather than look authoritative.
    (repo.spec_dir / "review.md").write_text(
        "# Process report\n\nNo blocking heading here.\n", encoding="utf-8"
    )
    run = repo.run_script("report", "--summary", review_dir=repo.spec_dir)
    text = _plain(run.stdout + run.stderr).lower()
    assert "implicit" in text or "隐式" in text, (
        "an invocation that omits the record path is a legacy mode and MUST label "
        f"its selection as implicit (C-27); got:\n{text}"
    )


# --------------------------------------------------------------------------- #
# C-29 — the sibling boundary is decidable from the documents alone
# --------------------------------------------------------------------------- #

def test_c29_both_skills_declare_distinct_judgment_objects_composed_by_the_command():
    for path in (SKILL_BODY, SIBLING_BODY):
        body = _flat(path.read_text(encoding="utf-8"))
        assert not re.search(
            r"(?i)keep the two separate|互不相关|no overlap|unrelated", body
        ), (
            f"the pre-composition wording MUST NOT survive in {path.name}: after the "
            "command composes both skills it is false (C-29)"
        )
        assert re.search(r"(?i)fixed order|固定顺序", body), (
            f"{path.name} MUST declare that the command composes the two in a fixed order"
        )
        assert re.search(r"(?i)judgment object|判定对象", body), (
            f"{path.name} MUST declare its own judgment object"
        )
        assert "speckit.review" in body, (
            f"{path.name} MUST name the composing command"
        )
