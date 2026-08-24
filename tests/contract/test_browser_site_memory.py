"""Contract tests: browser-utils site memory engine + file formats.

Contracts: .specify/specs/046-browser-site-memory/contracts/site-memory-engine.md
           .specify/specs/046-browser-site-memory/contracts/site-memory-formats.md
Requirement 046 / Feature 048.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE = REPO_ROOT / "skills" / "browser-utils" / "scripts" / "site-memory.py"

STATES = ("exploration", "optimization", "validation", "sealed")


def run_engine(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(ENGINE), *args],
        capture_output=True,
        text=True,
    )


def run_ok(*args: str) -> dict:
    proc = run_engine(*args)
    assert proc.returncode == 0, f"engine failed: {proc.stderr}{proc.stdout}"
    return json.loads(proc.stdout)


def init_site(home: Path, url: str = "https://g.aliyun-inc.com/console/page") -> dict:
    return run_ok("--action", "init", "--url", url, "--skill-home", str(home))


def net_record(seq: int, **over) -> dict:
    rec = {
        "seq": seq,
        "at": "2026-08-24T03:00:00Z",
        "kind": "network",
        "ok": True,
        "method": "POST",
        "url": "https://g.aliyun-inc.com/console_api/api.json?ApiName=ListBaseline",
        "headers": {"content-type": "application/json", "cookie": "<cookie:aliyun>"},
        "body_template": {"pageNum": 1, "pageSize": 20},
        "response_shape": {"status": 200, "json_keys": ["data", "total"]},
    }
    rec.update(over)
    return rec


def dom_record(seq: int, **over) -> dict:
    rec = {
        "seq": seq,
        "at": "2026-08-24T03:00:00Z",
        "kind": "dom",
        "ok": True,
        "action": "click",
        "target": "button#query",
        "input": None,
        "result": "navigated",
    }
    rec.update(over)
    return rec


def append(home: Path, site: str, task: str, record: dict) -> subprocess.CompletedProcess:
    return run_engine(
        "--action", "append-record",
        "--site", site, "--task", task,
        "--record", json.dumps(record, ensure_ascii=False),
        "--skill-home", str(home),
    )


# --------------------------------------------------------------------- init


class TestInit:
    def test_init_derives_dir_and_creates_state(self, tmp_path):
        out = init_site(tmp_path)
        assert out["ok"] is True
        assert out["site"] == "g.aliyun-inc.com"
        assert out["state"] == "exploration"
        state = json.loads(
            (tmp_path / "site" / "g.aliyun-inc.com" / "state.json").read_text(encoding="utf-8")
        )
        assert state["state"] == "exploration"
        assert state["history"][0]["evidence"] == "init"

    def test_init_is_idempotent(self, tmp_path):
        init_site(tmp_path)
        out = init_site(tmp_path)
        assert out["created"] is False

    def test_init_derives_host_with_explicit_port(self, tmp_path):
        out = run_ok(
            "--action", "init", "--url", "http://Example.COM:8080/x?y=1",
            "--skill-home", str(tmp_path),
        )
        assert out["site"] == "example.com:8080"
        assert (tmp_path / "site" / "example.com:8080").is_dir()

    def test_init_omits_default_port(self, tmp_path):
        out = run_ok(
            "--action", "init", "--url", "https://example.com:443/x",
            "--skill-home", str(tmp_path),
        )
        assert out["site"] == "example.com"


# ---------------------------------------------------------------- get-state


class TestGetState:
    def test_absent_site_reports_null_state(self, tmp_path):
        out = run_ok(
            "--action", "get-state", "--site", "no-such-host",
            "--skill-home", str(tmp_path),
        )
        assert out["state"] is None
        assert out["memory"] == "absent"

    def test_corrupt_state_treated_as_absent(self, tmp_path):
        init_site(tmp_path)
        (tmp_path / "site" / "g.aliyun-inc.com" / "state.json").write_text(
            "{broken", encoding="utf-8"
        )
        out = run_ok(
            "--action", "get-state", "--site", "g.aliyun-inc.com",
            "--skill-home", str(tmp_path),
        )
        assert out["state"] is None
        assert out["memory"] == "absent"

    def test_get_state_reads_back(self, tmp_path):
        init_site(tmp_path)
        out = run_ok(
            "--action", "get-state", "--site", "g.aliyun-inc.com",
            "--skill-home", str(tmp_path),
        )
        assert out["state"] == "exploration"
        assert out["recipe_present"] is False


# ------------------------------------------------------------ append-record


class TestAppendRecord:
    def test_append_network_and_dom_records(self, tmp_path):
        init_site(tmp_path)
        assert append(tmp_path, "g.aliyun-inc.com", "task-1", dom_record(1)).returncode == 0
        assert append(tmp_path, "g.aliyun-inc.com", "task-1", net_record(2)).returncode == 0
        lines = (
            tmp_path / "site" / "g.aliyun-inc.com" / "records" / "task-1.jsonl"
        ).read_text(encoding="utf-8").strip().splitlines()
        assert len(lines) == 2

    def test_append_rejects_seq_gap(self, tmp_path):
        init_site(tmp_path)
        assert append(tmp_path, "g.aliyun-inc.com", "task-1", dom_record(1)).returncode == 0
        proc = append(tmp_path, "g.aliyun-inc.com", "task-1", net_record(3))
        assert proc.returncode == 1
        assert "seq" in proc.stdout

    def test_append_rejects_missing_required_fields(self, tmp_path):
        init_site(tmp_path)
        bad = net_record(1)
        del bad["response_shape"]
        proc = append(tmp_path, "g.aliyun-inc.com", "task-1", bad)
        assert proc.returncode == 2

    def test_append_rejects_raw_cookie_value(self, tmp_path):
        init_site(tmp_path)
        bad = net_record(1, headers={"cookie": "session=abc123def456ghi7; other=x"})
        proc = append(tmp_path, "g.aliyun-inc.com", "task-1", bad)
        assert proc.returncode == 1
        assert "cookie" in proc.stdout

    def test_append_rejects_bearer_prefix(self, tmp_path):
        init_site(tmp_path)
        bad = net_record(1, headers={"authorization": "Bearer eyJhbGciOiJIUzI1NiJ9"})
        proc = append(tmp_path, "g.aliyun-inc.com", "task-1", bad)
        assert proc.returncode == 1

    def test_append_rejects_high_entropy_token_field(self, tmp_path):
        init_site(tmp_path)
        bad = net_record(1, body_template={"csrf_token": "a1b2c3d4e5f6g7h8i9j0k1l2"})
        proc = append(tmp_path, "g.aliyun-inc.com", "task-1", bad)
        assert proc.returncode == 1

    def test_append_accepts_resolve_placeholder(self, tmp_path):
        init_site(tmp_path)
        good = net_record(
            1, body_template={"csrf_token": "<resolve:page-var:csrfToken>"}
        )
        assert append(tmp_path, "g.aliyun-inc.com", "task-1", good).returncode == 0

    def test_failed_record_requires_error_field(self, tmp_path):
        init_site(tmp_path)
        bad = dom_record(1, ok=False)
        proc = append(tmp_path, "g.aliyun-inc.com", "task-1", bad)
        assert proc.returncode == 2
        good = dom_record(1, ok=False, error="timeout waiting for #list")
        assert append(tmp_path, "g.aliyun-inc.com", "task-1", good).returncode == 0


# --------------------------------------------------------- validate-records


class TestValidateRecords:
    def test_complete_records(self, tmp_path):
        init_site(tmp_path)
        append(tmp_path, "g.aliyun-inc.com", "task-1", dom_record(1))
        append(tmp_path, "g.aliyun-inc.com", "task-1", net_record(2))
        out = run_ok(
            "--action", "validate-records",
            "--site", "g.aliyun-inc.com", "--task", "task-1",
            "--skill-home", str(tmp_path),
        )
        assert out["complete"] is True
        assert out["counts"] == {"dom": 1, "network": 1, "failed": 0}

    def test_incomplete_without_network_record(self, tmp_path):
        init_site(tmp_path)
        append(tmp_path, "g.aliyun-inc.com", "task-1", dom_record(1))
        out = run_ok(
            "--action", "validate-records",
            "--site", "g.aliyun-inc.com", "--task", "task-1",
            "--skill-home", str(tmp_path),
        )
        assert out["complete"] is False
        assert any("network" in m for m in out["missing"])

    def test_missing_task_file_is_incomplete(self, tmp_path):
        init_site(tmp_path)
        out = run_ok(
            "--action", "validate-records",
            "--site", "g.aliyun-inc.com", "--task", "nope",
            "--skill-home", str(tmp_path),
        )
        assert out["complete"] is False


# ------------------------------------------- US2: routing section structure


SKILL_MD = REPO_ROOT / "skills" / "browser-utils" / "SKILL.md"
REFERENCES = REPO_ROOT / "skills" / "browser-utils" / "references"


class TestSkillRoutingSection:
    def test_skill_md_has_site_memory_routing_section(self):
        text = SKILL_MD.read_text(encoding="utf-8")
        assert re.search(r"^## .*[Ss]ite [Mm]emory", text, re.MULTILINE), (
            "SKILL.md must carry a site-memory routing section"
        )

    def test_skill_md_mentions_all_four_states(self):
        text = SKILL_MD.read_text(encoding="utf-8")
        for state in STATES:
            assert state in text, f"SKILL.md routing must reference state {state!r}"

    def test_references_exist_and_are_linked(self):
        for name in ("site-memory.md", "request-level-patterns.md"):
            target = REFERENCES / name
            assert target.is_file(), f"missing reference: {target}"
            assert name in SKILL_MD.read_text(encoding="utf-8"), (
                f"SKILL.md must point at references/{name}"
            )

    def test_caller_ownership_reporting_obligation(self):
        text = SKILL_MD.read_text(encoding="utf-8")
        assert "Reporting obligation" in text and "caller-owned" in text, (
            "SKILL.md must oblige the closing report to state that site/ memory "
            "is caller-owned and archived by the calling project/agent"
        )
        ref = (REFERENCES / "site-memory.md").read_text(encoding="utf-8")
        assert "never ships or archives" in ref and "## Ownership" in ref, (
            "references/site-memory.md must carry the ownership/archival guidance"
        )

    def test_mirrors_byte_identical(self):
        for rel in (
            "SKILL.md",
            "references/site-memory.md",
            "references/request-level-patterns.md",
            "scripts/site-memory.py",
        ):
            src = REPO_ROOT / "skills" / "browser-utils" / rel
            dst = REPO_ROOT / ".specify" / "skills" / "browser-utils" / rel
            assert dst.is_file(), f"mirror missing: {dst}"
            assert src.read_bytes() == dst.read_bytes(), f"mirror drift: {rel}"


# ------------------------------------------- US3: write-recipe + transition


def make_recipe(tmp_path, home, site="g.aliyun-inc.com", task="task-1"):
    init_site(home)
    append(home, site, task, dom_record(1))
    append(home, site, task, net_record(2))
    recipe = {
        "task": task,
        "distilled_from": f"records/{task}.jsonl",
        "distilled_at": "2026-08-24T03:10:00Z",
        "steps": [
            {
                "n": 1, "type": "request", "method": "POST",
                "url": "https://g.aliyun-inc.com/console_api/api.json?ApiName=ListBaseline",
                "params_template": {"pageNum": 1},
                "dynamic_fields": {"x-csrf-token": "<resolve:page-var:csrfToken>"},
                "expect": {"status": 200, "json_keys": ["data"]},
            },
            {"n": 2, "type": "page", "reason": "验证码步骤无法请求化", "action": "manual-captcha"},
        ],
    }
    path = tmp_path / "recipe.json"
    path.write_text(json.dumps(recipe, ensure_ascii=False), encoding="utf-8")
    return path


class TestWriteRecipe:
    def test_write_valid_recipe(self, tmp_path):
        recipe_path = make_recipe(tmp_path, tmp_path)
        out = run_ok(
            "--action", "write-recipe", "--site", "g.aliyun-inc.com",
            "--file", str(recipe_path), "--skill-home", str(tmp_path),
        )
        assert out == {"ok": True, "steps": 2, "page_steps": 1}
        assert (tmp_path / "site" / "g.aliyun-inc.com" / "recipe.json").is_file()

    def test_request_step_missing_expect_rejected(self, tmp_path):
        recipe_path = make_recipe(tmp_path, tmp_path)
        recipe = json.loads(recipe_path.read_text(encoding="utf-8"))
        del recipe["steps"][0]["expect"]
        recipe_path.write_text(json.dumps(recipe, ensure_ascii=False), encoding="utf-8")
        proc = run_engine(
            "--action", "write-recipe", "--site", "g.aliyun-inc.com",
            "--file", str(recipe_path), "--skill-home", str(tmp_path),
        )
        assert proc.returncode == 2

    def test_page_step_missing_reason_rejected(self, tmp_path):
        recipe_path = make_recipe(tmp_path, tmp_path)
        recipe = json.loads(recipe_path.read_text(encoding="utf-8"))
        recipe["steps"][1]["reason"] = ""
        recipe_path.write_text(json.dumps(recipe, ensure_ascii=False), encoding="utf-8")
        proc = run_engine(
            "--action", "write-recipe", "--site", "g.aliyun-inc.com",
            "--file", str(recipe_path), "--skill-home", str(tmp_path),
        )
        assert proc.returncode == 2

    def test_distilled_from_must_exist(self, tmp_path):
        recipe_path = make_recipe(tmp_path, tmp_path)
        recipe = json.loads(recipe_path.read_text(encoding="utf-8"))
        recipe["distilled_from"] = "records/nope.jsonl"
        recipe_path.write_text(json.dumps(recipe, ensure_ascii=False), encoding="utf-8")
        proc = run_engine(
            "--action", "write-recipe", "--site", "g.aliyun-inc.com",
            "--file", str(recipe_path), "--skill-home", str(tmp_path),
        )
        assert proc.returncode == 2


class TestTransition:
    def test_exploration_to_optimization_requires_complete_records(self, tmp_path):
        init_site(tmp_path)
        proc = run_engine(
            "--action", "transition", "--site", "g.aliyun-inc.com",
            "--to", "optimization", "--task", "task-1",
            "--skill-home", str(tmp_path),
        )
        assert proc.returncode == 1
        append(tmp_path, "g.aliyun-inc.com", "task-1", dom_record(1))
        append(tmp_path, "g.aliyun-inc.com", "task-1", net_record(2))
        out = run_ok(
            "--action", "transition", "--site", "g.aliyun-inc.com",
            "--to", "optimization", "--task", "task-1",
            "--skill-home", str(tmp_path),
        )
        assert out == {"ok": True, "from": "exploration", "to": "optimization"}

    def test_optimization_to_validation_requires_valid_recipe(self, tmp_path):
        make_recipe(tmp_path, tmp_path)  # records complete but recipe not written
        run_ok(
            "--action", "transition", "--site", "g.aliyun-inc.com",
            "--to", "optimization", "--task", "task-1",
            "--skill-home", str(tmp_path),
        )
        proc = run_engine(
            "--action", "transition", "--site", "g.aliyun-inc.com",
            "--to", "validation", "--skill-home", str(tmp_path),
        )
        assert proc.returncode == 1
        recipe_path = tmp_path / "recipe.json"
        run_ok(
            "--action", "write-recipe", "--site", "g.aliyun-inc.com",
            "--file", str(recipe_path), "--skill-home", str(tmp_path),
        )
        out = run_ok(
            "--action", "transition", "--site", "g.aliyun-inc.com",
            "--to", "validation", "--skill-home", str(tmp_path),
        )
        assert out["to"] == "validation"

    def test_illegal_skip_transition_rejected_with_legal_targets(self, tmp_path):
        init_site(tmp_path)
        proc = run_engine(
            "--action", "transition", "--site", "g.aliyun-inc.com",
            "--to", "sealed", "--skill-home", str(tmp_path),
        )
        assert proc.returncode == 1
        assert "optimization" in proc.stdout


# ----------------------------------- US4: record-validation + sealed rollback


def reach_validation(tmp_path):
    home = tmp_path
    site = "g.aliyun-inc.com"
    recipe_path = make_recipe(tmp_path, home)
    run_ok(
        "--action", "transition", "--site", site,
        "--to", "optimization", "--task", "task-1",
        "--skill-home", str(home),
    )
    run_ok(
        "--action", "write-recipe", "--site", site,
        "--file", str(recipe_path), "--skill-home", str(home),
    )
    run_ok(
        "--action", "transition", "--site", site,
        "--to", "validation", "--skill-home", str(home),
    )
    return home, site


def write_evidence(tmp_path, name="evidence.json", **over):
    evidence = {
        "run_id": "run-001",
        "task": "task-1",
        "verdict": "pass",
        "steps_total": 2,
        "steps_passed": 2,
        "failures": [],
        "at": "2026-08-24T04:00:00Z",
    }
    evidence.update(over)
    path = tmp_path / name
    path.write_text(json.dumps(evidence, ensure_ascii=False), encoding="utf-8")
    return path


def site_state(home, site="g.aliyun-inc.com"):
    return json.loads(
        (home / "site" / site / "state.json").read_text(encoding="utf-8")
    )["state"]


class TestRecordValidation:
    def test_pass_verdict_seals_from_validation(self, tmp_path):
        home, site = reach_validation(tmp_path)
        ev = write_evidence(tmp_path)
        out = run_ok(
            "--action", "record-validation", "--site", site,
            "--file", str(ev), "--skill-home", str(home),
        )
        assert out == {
            "ok": True, "verdict": "pass",
            "evidence": "validation/run-001.json", "state": "sealed",
        }
        assert (home / "site" / site / "validation" / "run-001.json").is_file()
        assert site_state(home, site) == "sealed"

    def test_fail_verdict_rolls_back_to_optimization(self, tmp_path):
        home, site = reach_validation(tmp_path)
        ev = write_evidence(
            tmp_path, verdict="fail", steps_passed=1,
            failures=[{"step": 2, "reason": "http 500"}],
        )
        out = run_ok(
            "--action", "record-validation", "--site", site,
            "--file", str(ev), "--skill-home", str(home),
        )
        assert out["state"] == "optimization"
        assert (home / "site" / site / "validation" / "run-001.json").is_file()

    def test_fail_verdict_requires_non_empty_failures(self, tmp_path):
        home, site = reach_validation(tmp_path)
        ev = write_evidence(tmp_path, verdict="fail", steps_passed=1)
        proc = run_engine(
            "--action", "record-validation", "--site", site,
            "--file", str(ev), "--skill-home", str(home),
        )
        assert proc.returncode == 2
        assert not (home / "site" / site / "validation" / "run-001.json").exists()

    def test_state_mismatch_keeps_evidence_but_refuses_move(self, tmp_path):
        home = tmp_path
        site = "g.aliyun-inc.com"
        init_site(home)  # still exploration; pass -> sealed is illegal from here
        ev = write_evidence(tmp_path)
        out = run_ok(
            "--action", "record-validation", "--site", site,
            "--file", str(ev), "--skill-home", str(home),
        )
        assert out["state"] == "exploration"
        assert "transition_error" in out
        assert (home / "site" / site / "validation" / "run-001.json").is_file()

    def test_sealed_rollback_requires_evidence(self, tmp_path):
        home, site = reach_validation(tmp_path)
        ev = write_evidence(tmp_path)
        run_ok(
            "--action", "record-validation", "--site", site,
            "--file", str(ev), "--skill-home", str(home),
        )
        assert site_state(home, site) == "sealed"
        proc = run_engine(
            "--action", "transition", "--site", site,
            "--to", "optimization", "--skill-home", str(home),
        )
        assert proc.returncode == 2
        assert site_state(home, site) == "sealed"

    def test_rollback_preserves_records_recipe_validation_sc004(self, tmp_path):
        home, site = reach_validation(tmp_path)
        ev = write_evidence(tmp_path)
        run_ok(
            "--action", "record-validation", "--site", site,
            "--file", str(ev), "--skill-home", str(home),
        )
        out = run_ok(
            "--action", "transition", "--site", site,
            "--to", "optimization", "--evidence", "recipe drifted: api renamed",
            "--skill-home", str(home),
        )
        assert out == {"ok": True, "from": "sealed", "to": "optimization"}
        root = home / "site" / site
        assert (root / "records" / "task-1.jsonl").is_file()
        assert (root / "recipe.json").is_file()
        assert (root / "validation" / "run-001.json").is_file()
