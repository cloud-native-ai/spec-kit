"""Integration smoke test for Feature 081 — the acceptance gate, the checker and mirror parity.

One command, three sub-checks, one evidence file (slice 081a, task T017; `plan.md` § D7).

Why this module exists rather than three separate contract tests: the feature's smoke record needs a
single end-to-end command over the feature's **main flow**, not the whole suite (`shared/workflow/
acceptance-hardening.md` § Verification Vocabulary — three fields, exactly one record per feature).
The three sub-checks below are that flow, in the order a consumer meets it:

1. ``specify init`` — the capability the feature's one ``in-scope`` runtime-stack row says this
   repository delivers (RS-004 / FR-005 ①). It is driven through the **installed console script in
   a real subprocess**, on a ``tmp_path`` fixture, because the resolver-fallback path this feature
   relies on (T002) only exists in the development checkout: an in-process call would exercise the
   import path and never the fallback.
2. the closure checker on the two declarative fixture sets — ``positive`` (``accept`` / exit 0) and
   ``negative`` (``block`` / exit 1, ``zero-final-path-pass``). That is the verdict `/speckit.implement`
   now calls before the status flip (FR-005 ②, GW-01).
3. ``regen-command-copies.py --check`` — the per-tool command copies still match their templates after
   this slice's edits (FR-005 ③ / FR-021 / FR-024).

Determinism, stated so the next slice does not have to guess: no network, no wall clock, no
assertion on elapsed time, and no absolute temporary path in the recorded evidence — the ``specify
init`` command is recorded with its ``<tmp_path>`` placeholder, so two runs of this module write a
byte-identical file and their exit codes are the only thing that can differ (T019 runs it twice).

The evidence file is the path the feature's smoke record will name:
``.specify/specs/081-acceptance-hardening/test-evidence/smoke-081.txt``. It is written **before** the
assertions, so a failing sub-check is still recorded rather than leaving the previous run's green
evidence in place — an evidence file that only exists when the run passed proves nothing.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.integration

ROOT = Path(__file__).resolve().parents[2]
CHECKER_REL = "scripts/python/closure-acceptance-check.py"
CHECKER = ROOT / CHECKER_REL
REGEN_REL = "scripts/python/regen-command-copies.py"
FIXTURES = ROOT / "tests" / "fixtures" / "acceptance-hardening"
SPEC = ROOT / ".specify" / "specs" / "081-acceptance-hardening"
EVIDENCE = SPEC / "test-evidence" / "smoke-081.txt"

#: The smoke command as a consumer runs it — recorded verbatim in the evidence file so the record
#: names the command that produced it instead of describing it.
SMOKE_COMMAND = (
    "bash scripts/bash/run-tests.sh tests/integration/test_acceptance_smoke.py -q"
)

#: Sub-check 1's command. `--ignore-agent-tools` keeps the run independent of which agent CLIs the
#: host machine happens to have installed; `--no-git` keeps it from touching the fixture's parent
#: repository. Neither flag changes what the check proves: the `.specify/` tree either materialises
#: from the checkout's own templates or the resolver fallback is broken.
INIT_ARGS = [
    "init", "smoke-081",
    "--ai", "claude", "--no-git", "--script", "sh", "--ignore-agent-tools",
]


def _run(argv, cwd):
    return subprocess.run(argv, cwd=str(cwd), capture_output=True, text=True, timeout=300)


def _specify_bin():
    """The installed console script, next to the interpreter running this test.

    A missing console script is an **environment** failure, not a skip: a smoke test that skips is
    indistinguishable from a smoke test that passed, which is the defect this feature exists to
    close (Constitution XVI — a green check is a claim, not evidence).
    """
    candidate = Path(sys.executable).parent / "specify"
    if candidate.is_file():
        return str(candidate)
    found = shutil.which("specify")
    assert found, (
        "no `specify` console script next to %s nor on PATH — the smoke test cannot drive the "
        "capability the feature claims to deliver (RS-004)" % sys.executable
    )
    return found


def _truncate(text, limit=800):
    text = (text or "").strip()
    return text if len(text) <= limit else text[:limit] + " …"


def test_acceptance_smoke(tmp_path):
    """The three sub-checks, one run, one evidence file — and no green without each of them."""
    results = []

    # ---- sub-check 1: `specify init` on a tmp_path fixture ------------------ #
    specify = _specify_bin()
    project = "smoke-081"
    init = _run([specify] + INIT_ARGS, tmp_path)
    project_dir = tmp_path / project
    spec_tree = project_dir / ".specify"
    generated = sorted(
        str(p.relative_to(project_dir)) for p in spec_tree.iterdir()
    ) if spec_tree.is_dir() else []
    results.append({
        "sub": 1,
        "heading": "specify init builds a `.specify/` tree from the checkout's own templates",
        "name": "specify init",
        "command": "%s %s   # cwd: <tmp_path>" % (Path(specify).name, " ".join(INIT_ARGS)),
        "exit": init.returncode,
        "note": "generated: %s" % (", ".join(generated) or "<none>"),
        "detail": init.stdout + init.stderr,
    })

    # ---- sub-check 2: the closure checker on both fixture sets -------------- #
    for case, expected_exit, expected_verdict in (
        ("positive", 0, "accept"),
        ("negative", 1, "block"),
    ):
        fixture = FIXTURES / case
        command = [sys.executable, str(CHECKER), "--spec-dir", str(fixture), "--json"]
        proc = _run(command, ROOT)
        try:
            payload = json.loads(proc.stdout) if proc.stdout.strip() else {}
        except json.JSONDecodeError:
            payload = {}
        codes = [reason.get("code") for reason in payload.get("reasons", [])]
        results.append({
            "sub": 2,
            "heading": "the closure checker on both fixture sets",
            "name": "closure checker on %s" % case,
            "command": "python3 %s --spec-dir tests/fixtures/acceptance-hardening/%s --json"
                       % (CHECKER_REL, case),
            "exit": proc.returncode,
            "note": "verdict=%s reasons=%s" % (payload.get("verdict"), codes),
            "detail": proc.stderr,
            "expected_exit": expected_exit,
            "expected_verdict": expected_verdict,
            "verdict": payload.get("verdict"),
            "codes": codes,
        })

    # ---- sub-check 3: the per-tool command copies still match their source --- #
    regen = _run([sys.executable, REGEN_REL, "--check"], ROOT)
    results.append({
        "sub": 3,
        "heading": "the per-tool command copies still match their templates",
        "name": "per-tool command copies",
        "command": "python3 %s --check" % REGEN_REL,
        "exit": regen.returncode,
        "note": ("mismatches: %d" % len(regen.stdout.splitlines())) if regen.returncode else "mismatches: none",
        "detail": regen.stdout + regen.stderr,
    })

    _write_evidence(results)

    # ---- assertions, one per sub-check, each naming its own evidence --------- #
    assert spec_tree.is_dir(), (
        "sub-check 1: `specify init` produced no `.specify/` tree under %s (exit %d)\n%s"
        % (tmp_path, init.returncode, _truncate(init.stdout + init.stderr))
    )
    assert init.returncode == 0, (
        "sub-check 1: `specify init` exited %d\n%s"
        % (init.returncode, _truncate(init.stdout + init.stderr))
    )
    for member in ("templates", "scripts", "memory"):
        assert (spec_tree / member).is_dir(), (
            "sub-check 1: the generated `.specify/` tree has no %r directory; the resolver "
            "fallback delivered an incomplete template set" % member
        )

    for result in results:
        if "expected_exit" not in result:
            continue
        assert result["exit"] == result["expected_exit"], (
            "sub-check 2: the checker exited %d on the %s fixture, expected %d\n%s"
            % (result["exit"], result["name"], result["expected_exit"],
               _truncate(str(result["detail"])))
        )
        assert result["verdict"] == result["expected_verdict"], (
            "sub-check 2: the %s fixture's verdict is %r, expected %r"
            % (result["name"], result["verdict"], result["expected_verdict"])
        )
    negative = [r for r in results if r["name"].endswith("negative")][0]
    assert "zero-final-path-pass" in negative["codes"], (
        "sub-check 2: the 026-shape fixture must block with `zero-final-path-pass`; got %r"
        % (negative["codes"],)
    )

    assert regen.returncode == 0, (
        "sub-check 3: `%s --check` exited %d — regenerate the per-tool copies instead of "
        "editing them\n%s" % (REGEN_REL, regen.returncode, _truncate(regen.stdout + regen.stderr))
    )


def _write_evidence(results):
    """Write the three sub-commands and their exit codes, before any assertion can fail.

    No timestamp and no absolute temporary path: two runs write the same bytes.
    """
    lines = [
        "# Feature 081 smoke record — the acceptance gate end to end",
        "# Command: %s" % SMOKE_COMMAND,
        "# Written by tests/integration/test_acceptance_smoke.py; no network, no wall clock.",
    ]
    current = None
    for result in results:
        if result["sub"] != current:
            current = result["sub"]
            lines.append("")
            lines.append("sub-check %d — %s" % (current, result["heading"]))
        lines.append("  $ %s" % result["command"])
        lines.append("  exit %d" % result["exit"])
        lines.append("  %s" % result["note"])
        lines.append("")
    EVIDENCE.parent.mkdir(parents=True, exist_ok=True)
    EVIDENCE.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
