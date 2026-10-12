"""Contract tests for the merge-skills no-loss gate and its provenance re-verification.

These two scripts are the only mechanical proof that a skill merge did not silently drop
a capability, and both are only trustworthy if they go RED when their subject breaks. Each
test here is written as that red/green pair: a green assertion next to the mutation that
must turn it red. A gate that cannot fail is worse than no gate, because it is believed.

Scripts under test live in the skill, not in .specify/scripts (skill-owned executables):
    skills/external/merge-skills/scripts/coverage_probe.py
    skills/external/merge-skills/scripts/provenance_check.py
"""

import importlib.util
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "skills" / "external" / "merge-skills" / "scripts"
PROBE = SCRIPTS / "coverage_probe.py"
CHECKER = SCRIPTS / "provenance_check.py"


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def cp():
    sys.path.insert(0, str(SCRIPTS))
    return _load("coverage_probe_under_test", PROBE)


def run(script, *args):
    """Run a gate script and return (exit_code, combined_output)."""
    p = subprocess.run([sys.executable, str(script), *args],
                       capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


# --------------------------------------------------------------------------- #
# Fixtures: a source skill, a target that absorbed it, and a provenance record
# --------------------------------------------------------------------------- #

SOURCE_A = """# a-skill
Endpoint `/api/v1/scan`. Flags --dry-run --strict --unit-type.
Identifiers onExistingPackageJson, code_challenge, CONST_READY_VALUE.
Enums `pass` `fail` READ WRITE. Codes 201 404. URL https://a.example/spec#limits
Heading token `## Git Workflow` and path docs/inventory.md
"""

TARGET_A = """# Target C — scope A
Endpoint `/api/v1/scan`. Flags --dry-run --strict --unit-type.
Identifiers onExistingPackageJson, code_challenge, CONST_READY_VALUE.
Enums `pass` `fail` READ WRITE. Codes 201 404. URL https://a.example/spec#limits
Heading token `## Git Workflow` and path docs/inventory.md
"""

TARGET_B = "# Target C — scope B\nProvisions with `--user git` and code 422.\n"

RECORD = """# Merge Provenance — c-skill

Re-verify with `provenance_check.py <this-skill-dir>`.

## Source: a-skill

- **Merged**: 2026-10-11
- **Source identity**: `a-skill` · class: peer (host-managed)
- **Baseline**: `./merge-provenance/a-skill.baseline.txt`
{a_corpus}
### Capability inheritance

| # | Capability (what the source could do) | Target destination | Verification | Status |
|---|---------------------------------------|--------------------|--------------|--------|
| 1 | Run an inventory scan | `references/a-topic.md` | `--dry-run` walk-through | verified |

## Source: b-skill

- **Merged**: 2026-10-11
- **Baseline**: `./merge-provenance/b-skill.baseline.txt`
{b_corpus}
### Capability inheritance

| # | Capability (what the source could do) | Target destination | Verification | Status |
|---|---------------------------------------|--------------------|--------------|--------|
| 1 | Provision a server | `references/b-topic.md` | `--user git` dry run | verified |
| 2 | Legacy telnet mode | `references/b-topic.md` | decision 2026-10-11 | dropped(upstream retired it) |
"""


def build_skill(tmp_path, a_corpus="", b_corpus=""):
    """A merged target skill with two absorbed sources, real emitted baselines."""
    skill = tmp_path / "c-skill"
    (skill / "references" / "merge-provenance").mkdir(parents=True)
    (skill / "SKILL.md").write_text("# c-skill\nFormerly a-skill and b-skill.\n",
                                    encoding="utf-8")
    (skill / "references" / "a-topic.md").write_text(TARGET_A, encoding="utf-8")
    (skill / "references" / "b-topic.md").write_text(TARGET_B, encoding="utf-8")
    src = tmp_path / "src"
    src.mkdir()
    (src / "a.md").write_text(SOURCE_A, encoding="utf-8")
    (src / "b.md").write_text("# b-skill\nProvisions with `--user git` and code 422.\n",
                              encoding="utf-8")
    for name in ("a-skill", "b-skill"):
        code, out = run(PROBE, "--emit-baseline",
                        str(skill / "references" / "merge-provenance"
                            / f"{name}.baseline.txt"),
                        str(src / f"{name[0]}.md"), str(skill))
        assert code == 0, f"fixture emit failed for {name}: {out}"
    (skill / "references" / "merge-provenance.md").write_text(
        RECORD.format(a_corpus=a_corpus, b_corpus=b_corpus), encoding="utf-8")
    return skill


# --------------------------------------------------------------------------- #
# coverage_probe — extraction
# --------------------------------------------------------------------------- #

class TestTokenExtraction:
    def test_independent_enum_word_is_not_swallowed_by_a_longer_constant(self, cp):
        """`READ` is a fact; `READY` inside `CONST_READY_VALUE` is residue.

        A plain substring test dropped both, which is a silent false-negative in a gate
        whose whole job is not losing facts.
        """
        toks = cp.extract_tokens("Enums READ and READY with CONST_READY_VALUE")
        assert "READ" in toks
        assert "CONST_READY_VALUE" in toks
        assert "READY" not in toks  # a real component of the constant -> residue

    def test_round_trip_of_a_bare_token_list_is_lossy_so_baselines_load_verbatim(self, cp):
        """Why --baseline never re-extracts: backtick-derived tokens and relative paths
        do not survive a second extraction pass."""
        first = cp.extract_tokens("Enums `pass` `fail` and `docs/inventory.md`")
        assert {"pass", "fail", "docs/inventory.md"} <= first
        again = cp.extract_tokens("\n".join(sorted(first)))
        assert {"pass", "fail", "docs/inventory.md"} & again == set()
        # the relative path degrades to its leading-slash fragment rather than vanishing
        assert "/inventory.md" in again

    def test_baseline_write_read_is_lossless_including_hash_tokens(self, cp, tmp_path):
        """A token that is itself a Markdown heading must not be read back as a comment."""
        toks = cp.extract_tokens(SOURCE_A)
        assert "## Git Workflow" in toks and "https://a.example/spec#limits" in toks
        path = tmp_path / "b.txt"
        reasons = {"READ": "reworded in the target"}
        cp.write_baseline(str(path), toks, reasons, "src/a.md")
        back = cp.load_baseline(str(path))
        assert set(back) == toks
        assert back["READ"] == "reworded in the target"


# --------------------------------------------------------------------------- #
# coverage_probe — gate behaviour
# --------------------------------------------------------------------------- #

class TestProbeGate:
    def test_clean_merge_passes_and_a_dropped_fact_fails(self, tmp_path):
        src = tmp_path / "s.md"
        src.write_text(SOURCE_A, encoding="utf-8")
        tgt = tmp_path / "t.md"
        tgt.write_text(TARGET_A, encoding="utf-8")
        assert run(PROBE, str(src), str(tgt))[0] == 0
        tgt.write_text(TARGET_A.replace("--strict", ""), encoding="utf-8")
        code, out = run(PROBE, str(src), str(tgt))
        assert code == 3 and "--strict" in out

    def test_a_probe_that_read_nothing_is_never_a_pass(self, tmp_path):
        empty = tmp_path / "empty"
        empty.mkdir()
        (empty / "s.md").write_text("prose only, no fact tokens at all", encoding="utf-8")
        tgt = tmp_path / "t.md"
        tgt.write_text(TARGET_A, encoding="utf-8")
        assert run(PROBE, str(tmp_path / "missing"), str(tgt))[0] == 4
        assert run(PROBE, str(empty), str(tgt))[0] == 4

    def test_emit_is_refused_while_the_merge_is_lossy(self, tmp_path):
        src = tmp_path / "s.md"
        src.write_text(SOURCE_A, encoding="utf-8")
        tgt = tmp_path / "t.md"
        tgt.write_text(TARGET_A.replace("--strict", ""), encoding="utf-8")
        out_path = tmp_path / "b.txt"
        code, out = run(PROBE, "--emit-baseline", str(out_path), str(src), str(tgt))
        assert code == 3 and "refused" in out
        assert not out_path.exists(), "a lossy state must never become a baseline"

    def test_emit_is_refused_when_an_allowance_carries_no_reason(self, tmp_path):
        """A frozen token with no reason re-reads as REQUIRED, so an unreasoned
        allowance would become a permanent false red on every later re-verification."""
        src = tmp_path / "s.md"
        src.write_text("Flag --gone-here\n", encoding="utf-8")
        tgt = tmp_path / "t.md"
        tgt.write_text("nothing relevant\n", encoding="utf-8")
        allow = tmp_path / "allow.txt"
        allow.write_text("--gone-here\n", encoding="utf-8")
        code, out = run(PROBE, "--allow", str(allow), "--emit-baseline",
                        str(tmp_path / "b.txt"), str(src), str(tgt))
        assert code == 3 and "no reason" in out
        allow.write_text("# renamed in the target\n--gone-here\n", encoding="utf-8")
        assert run(PROBE, "--allow", str(allow), "--emit-baseline",
                   str(tmp_path / "b.txt"), str(src), str(tgt))[0] == 0

    def test_baseline_reverification_needs_no_scratch_and_catches_drift(self, tmp_path):
        skill = build_skill(tmp_path)
        baseline = skill / "references" / "merge-provenance" / "a-skill.baseline.txt"
        assert run(PROBE, "--baseline", str(baseline), str(skill))[0] == 0
        topic = skill / "references" / "a-topic.md"
        topic.write_text(topic.read_text(encoding="utf-8").replace("--strict", ""),
                         encoding="utf-8")
        code, out = run(PROBE, "--baseline", str(baseline), str(skill))
        assert code == 3 and "--strict" in out

    def test_a_baseline_is_not_part_of_its_own_corpus(self, tmp_path):
        """The false-green this guards: a baseline enumerates every frozen token, so
        reading it back as target content satisfies all of them unconditionally."""
        skill = build_skill(tmp_path)
        for f in ("references/a-topic.md", "SKILL.md"):
            p = skill / f
            p.write_text(p.read_text(encoding="utf-8").replace("--strict", ""),
                         encoding="utf-8")
        baseline = skill / "references" / "merge-provenance" / "a-skill.baseline.txt"
        code, out = run(PROBE, "--baseline", str(baseline), str(skill))
        assert code == 3, "the baseline dir must be excluded from the corpus"
        assert "--strict" in out

    def test_annotated_false_positive_stays_allowed_but_required_tokens_do_not(self,
                                                                              tmp_path):
        skill = build_skill(tmp_path)
        baseline = skill / "references" / "merge-provenance" / "a-skill.baseline.txt"
        text = baseline.read_text(encoding="utf-8")
        baseline.write_text(text.replace("READ\n", "READ # reworded as read-only\n"),
                            encoding="utf-8")
        topic = skill / "references" / "a-topic.md"
        body = topic.read_text(encoding="utf-8")
        topic.write_text(body.replace("READ", "").replace("--strict", ""),
                         encoding="utf-8")
        code, out = run(PROBE, "--baseline", str(baseline), str(skill))
        assert code == 3, "only reason-carrying tokens may be accepted"
        assert "ALLOWED  READ" in out and "MISSING  --strict" in out


# --------------------------------------------------------------------------- #
# provenance_check — the committed record
# --------------------------------------------------------------------------- #

class TestProvenanceRecord:
    def test_a_complete_record_holds(self, tmp_path):
        skill = build_skill(tmp_path)
        code, out = run(CHECKER, str(skill))
        assert code == 0, out
        assert "2 source(s)" in out and "verified row(s)" in out

    def test_absent_or_unparsable_record_is_not_a_pass(self, tmp_path):
        skill = build_skill(tmp_path)
        (skill / "references" / "merge-provenance.md").unlink()
        assert run(CHECKER, str(skill))[0] == 4
        skill = build_skill(tmp_path / "second")
        (skill / "references" / "merge-provenance.md").write_text(
            "# Merge Provenance\n\nno source sections here\n", encoding="utf-8")
        assert run(CHECKER, str(skill))[0] == 4

    def test_usage_errors(self, tmp_path):
        assert run(CHECKER)[0] == 2
        not_a_skill = tmp_path / "bare"
        not_a_skill.mkdir()
        assert run(CHECKER, str(not_a_skill))[0] == 2

    def test_dropped_fact_renamed_destination_and_pending_row_all_go_red(self, tmp_path):
        skill = build_skill(tmp_path)
        topic = skill / "references" / "a-topic.md"
        topic.write_text(topic.read_text(encoding="utf-8").replace("--strict", ""),
                         encoding="utf-8")
        code, out = run(CHECKER, str(skill))
        assert code == 3 and "--strict" in out

        skill = build_skill(tmp_path / "rename")
        (skill / "references" / "a-topic.md").rename(skill / "references" / "inventory.md")
        code, out = run(CHECKER, str(skill))
        assert code == 3 and "does not resolve" in out

        skill = build_skill(tmp_path / "pending")
        rec = skill / "references" / "merge-provenance.md"
        rec.write_text(rec.read_text(encoding="utf-8").replace(
            "| verified |", "| pending |", 1), encoding="utf-8")
        code, out = run(CHECKER, str(skill))
        assert code == 3 and "pending" in out

    def test_dropped_requires_a_reason_and_verification_may_not_be_empty(self, tmp_path):
        skill = build_skill(tmp_path)
        rec = skill / "references" / "merge-provenance.md"
        rec.write_text(rec.read_text(encoding="utf-8").replace(
            "dropped(upstream retired it)", "dropped"), encoding="utf-8")
        code, out = run(CHECKER, str(skill))
        assert code == 3 and "dropped" in out

        skill = build_skill(tmp_path / "noverify")
        rec = skill / "references" / "merge-provenance.md"
        rec.write_text(rec.read_text(encoding="utf-8").replace(
            "| `--dry-run` walk-through |", "|  |"), encoding="utf-8")
        code, out = run(CHECKER, str(skill))
        assert code == 3 and "Verification" in out

    def test_missing_or_emptied_baseline_is_a_finding_not_a_pass(self, tmp_path):
        skill = build_skill(tmp_path)
        (skill / "references" / "merge-provenance" / "a-skill.baseline.txt").unlink()
        assert run(CHECKER, str(skill))[0] == 3
        skill = build_skill(tmp_path / "empty")
        (skill / "references" / "merge-provenance" / "a-skill.baseline.txt").write_text(
            "# header only\n", encoding="utf-8")
        code, out = run(CHECKER, str(skill))
        assert code == 3 and "0 frozen tokens" in out

    def test_table_is_found_by_column_name_not_position(self, tmp_path):
        """Columns may be reordered and headers qualified; the contract is the names."""
        skill = build_skill(tmp_path)
        rec = skill / "references" / "merge-provenance.md"
        text = rec.read_text(encoding="utf-8")
        text = text.replace(
            "| # | Capability (what the source could do) | Target destination "
            "| Verification | Status |",
            "| Status | Verification | # | Capability — as served by the source "
            "| Target destination |")
        text = text.replace(
            "| 1 | Run an inventory scan | `references/a-topic.md` "
            "| `--dry-run` walk-through | verified |",
            "| verified | `--dry-run` walk-through | 1 | Run an inventory scan "
            "| `references/a-topic.md` |")
        text = text.replace(
            "| 1 | Provision a server | `references/b-topic.md` "
            "| `--user git` dry run | verified |",
            "| verified | `--user git` dry run | 1 | Provision a server "
            "| `references/b-topic.md` |")
        text = text.replace(
            "| 2 | Legacy telnet mode | `references/b-topic.md` "
            "| decision 2026-10-11 | dropped(upstream retired it) |",
            "| dropped(upstream retired it) | decision 2026-10-11 | 2 | Legacy telnet mode "
            "| `references/b-topic.md` |")
        rec.write_text(text, encoding="utf-8")
        assert run(CHECKER, str(skill))[0] == 0

    def test_an_escaped_pipe_inside_a_cell_is_not_a_malformed_row(self, tmp_path):
        skill = build_skill(tmp_path)
        rec = skill / "references" / "merge-provenance.md"
        rec.write_text(rec.read_text(encoding="utf-8").replace(
            "`--dry-run` walk-through", "`--status pass\\|fail` walk-through"),
            encoding="utf-8")
        assert run(CHECKER, str(skill))[0] == 0


class TestScopedCorpus:
    """A multi-source merge into one target needs per-source corpus scoping.

    Measured on the real draw-* family: 14-34% of each engine's fact tokens also occur
    in sibling engines. Against a whole-target corpus, a fact lost from its own engine
    but present in a sibling reads as covered — a false green that scales with the number
    of sources absorbed.
    """

    def test_unscoped_corpus_masks_loss_that_scoped_corpus_catches(self, tmp_path):
        scoped = build_skill(
            tmp_path / "scoped",
            a_corpus="- **Corpus**: `references/a-topic.md`, `SKILL.md`\n")
        topic = scoped / "references" / "a-topic.md"
        body = topic.read_text(encoding="utf-8").replace("--strict", "")
        topic.write_text(body, encoding="utf-8")
        # the fact survives only in the sibling engine's doc
        sib = scoped / "references" / "b-topic.md"
        sib.write_text(sib.read_text(encoding="utf-8")
                       + "\nSibling still mentions `--strict`.\n", encoding="utf-8")

        unscoped = build_skill(tmp_path / "unscoped")
        u_topic = unscoped / "references" / "a-topic.md"
        u_topic.write_text(u_topic.read_text(encoding="utf-8").replace("--strict", ""),
                           encoding="utf-8")
        u_sib = unscoped / "references" / "b-topic.md"
        u_sib.write_text(u_sib.read_text(encoding="utf-8")
                         + "\nSibling still mentions `--strict`.\n", encoding="utf-8")

        assert run(CHECKER, str(unscoped))[0] == 0, "documents the masking this prevents"
        code, out = run(CHECKER, str(scoped))
        assert code == 3 and "--strict" in out

    def test_an_unresolvable_scope_is_a_finding_not_a_silent_widening(self, tmp_path):
        skill = build_skill(tmp_path, a_corpus="- **Corpus**: `references/nope.md`\n")
        code, out = run(CHECKER, str(skill))
        assert code == 3 and "resolves to nothing" in out

    def test_a_scope_may_use_globs_that_exclude_sibling_subtrees(self, tmp_path):
        """`references/*.md` must not match `references/types/**` — that is how a merged
        target keeps one engine's corpus out of another's."""
        skill = build_skill(tmp_path)
        nested = skill / "references" / "types" / "other"
        nested.mkdir(parents=True)
        (nested / "doc.md").write_text("sibling engine mentions --strict here\n",
                                       encoding="utf-8")
        topic = skill / "references" / "a-topic.md"
        topic.write_text(topic.read_text(encoding="utf-8").replace("--strict", ""),
                         encoding="utf-8")
        rec = skill / "references" / "merge-provenance.md"
        rec.write_text(rec.read_text(encoding="utf-8").replace(
            "- **Baseline**: `./merge-provenance/a-skill.baseline.txt`",
            "- **Baseline**: `./merge-provenance/a-skill.baseline.txt`\n"
            "- **Corpus**: `references/*.md`, `SKILL.md`"), encoding="utf-8")
        code, out = run(CHECKER, str(skill))
        assert code == 3 and "--strict" in out


# --------------------------------------------------------------------------- #
# The scripts themselves must stay executable and self-documenting
# --------------------------------------------------------------------------- #

class TestScriptSurface:
    @pytest.mark.parametrize("script", [PROBE, CHECKER])
    def test_script_exists_and_documents_its_exit_codes(self, script):
        assert script.is_file(), f"skill-owned executable missing: {script}"
        doc = _load(script.stem + "_doc", script).__doc__
        for code in ("0", "2", "3", "4"):
            assert code in doc, f"{script.name} docstring does not document exit {code}"

    def test_no_compiled_residue_is_tracked(self):
        tracked = subprocess.run(
            ["git", "-C", str(ROOT), "ls-files", str(SCRIPTS)],
            capture_output=True, text=True).stdout
        assert tracked.strip(), "the skill-owned scripts must be tracked"
        assert "__pycache__" not in tracked and ".pyc" not in tracked
