"""Contract tests for the proactive-trigger seed rule set (spec 050).

Maps to ``contracts/seed-derivation.md`` clauses C-1 … C-10.

The seed is a hand-written derived copy of situation→flow knowledge whose owner
is the ``## Handoffs`` prose of the command templates (plus a few
owning-section paragraphs). Prose cannot be parsed deterministically, so drift
is *detected* rather than *prevented*: C-6/C-7 open the provenance target and
assert the verbatim quote and the flow name are still there. When a source
section is rewritten, these tests fail naming the ruleId, the file, the anchor
kind and the missing flow — the fix is to sync the seed, never to loosen here.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SEED = ROOT / "templates" / "proactive-trigger-seed.json"
SEED_MIRROR = ROOT / ".specify" / "templates" / "proactive-trigger-seed.json"
DATA_MODEL = (
    ROOT / ".specify" / "specs" / "050-proactive-flow-trigger" / "data-model.md"
)

# C-2: closed top-level schema.
TOP_KEYS = {"schemaVersion", "generatedFrom", "situations", "rules"}

# C-3: rule entry key set (`notes` is the only optional extra).
RULE_REQUIRED = {
    "ruleId", "situationId", "flow", "invocation", "rationale",
    "confirmationClass", "origin", "priority", "provenance",
}
RULE_ALLOWED = RULE_REQUIRED | {"notes"}
# Runtime state must never ship in the package.
RULE_FORBIDDEN = {"tuning", "stats", "promotion", "state"}

# C-4: the isomorphism difference between a seed entry and a learned one.
LEARNED_ONLY = {"tuning", "stats", "promotion", "state"}
SEED_ONLY = {"provenance", "notes"}
# The seven fields C-4 names as semantically identical, plus `origin` — which both
# sides carry (C-3 requires it) and whose *value* is the seed/learned discriminator.
SHARED_SEMANTIC = {
    "ruleId", "situationId", "flow", "invocation", "rationale",
    "confirmationClass", "priority",
} | {"origin"}

PROVENANCE_KEYS = {"file", "anchorKind", "anchor", "quote"}
ANCHOR_KINDS = {"handoffs", "owning-section"}

# E1 full shape (C-8).
SITUATION_KEYS = {"id", "name", "stage", "signals", "match"}
MATCH_KEYS = {"stage", "signalsAll", "signalsAny"}

SITUATION_COUNT = 13
RULE_COUNT = 13

# Controlled vocabulary (data-model.md §受控词表). 9 stages / 12 signals.
STAGES = {
    "no-spec", "requirements-unclear", "requirements-draft", "planned",
    "tasks-ready", "implementing", "implemented", "review-pending", "non-feature",
}
SIGNALS = {
    "needs-clarification", "no-plan", "no-tasks", "open-tasks", "deferred-tasks",
    "checklist-absent", "feedback-threshold", "introspection-pending", "docs-drift",
    "instructions-stale", "feature-index-absent", "constitution-absent",
}

# C-9: classification column, taken from data-model.md's named-situation table.
DESTRUCTIVE_RULES = {"r-006", "r-011", "r-013"}

RULE_ID_RE = re.compile(r"^r-[0-9]{3}$")
SITUATION_ID_RE = re.compile(r"^s[0-9]{2}$")


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


@pytest.fixture(scope="module")
def seed() -> dict:
    assert SEED.is_file(), f"missing seed file: {SEED}"
    return json.loads(SEED.read_text(encoding="utf-8"))


def section_body(text: str, heading: str) -> str | None:
    """Body of `## <heading>` up to the next `## ` heading."""
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if re.match(r"^##\s+" + re.escape(heading) + r"\b", line):
            start = i
            break
    if start is None:
        return None
    for j in range(start + 1, len(lines)):
        if lines[j].startswith("## "):
            return "\n".join(lines[start:j])
    return "\n".join(lines[start:])


# --- C-1: dual surface, byte-identical ---


def test_c1_seed_exists_and_mirror_is_byte_identical():
    assert SEED.is_file(), f"missing seed: {SEED}"
    json.loads(SEED.read_text(encoding="utf-8"))  # valid JSON
    assert SEED_MIRROR.is_file(), f"missing seed mirror: {SEED_MIRROR}"
    assert SEED.read_bytes() == SEED_MIRROR.read_bytes(), "seed mirror drift"


# --- C-2: closed top-level schema ---


def test_c2_top_level_schema_closed(seed):
    assert set(seed) == TOP_KEYS, (
        f"top-level keys must be exactly {sorted(TOP_KEYS)}, got {sorted(seed)}"
    )
    assert isinstance(seed["schemaVersion"], int)
    assert isinstance(seed["generatedFrom"], str) and seed["generatedFrom"]
    assert isinstance(seed["situations"], list)
    assert isinstance(seed["rules"], list)


# --- C-3: rule entry schema ---


def test_c3_rule_entry_key_set(seed):
    for rule in seed["rules"]:
        rid = rule.get("ruleId", "<missing>")
        keys = set(rule)
        missing = RULE_REQUIRED - keys
        extra = keys - RULE_ALLOWED
        forbidden = keys & RULE_FORBIDDEN
        assert not missing, f"{rid}: missing keys {sorted(missing)}"
        assert not extra, f"{rid}: unexpected keys {sorted(extra)}"
        assert not forbidden, (
            f"{rid}: runtime state must not ship in the package: {sorted(forbidden)}"
        )
        assert rule["origin"] == "seed", f"{rid}: origin must be 'seed'"


def test_c3_identifier_and_type_grammar(seed):
    for rule in seed["rules"]:
        rid = rule["ruleId"]
        assert RULE_ID_RE.match(rid), f"{rid}: ruleId must match ^r-[0-9]{{3}}$"
        assert SITUATION_ID_RE.match(rule["situationId"]), (
            f"{rid}: situationId {rule['situationId']!r} must match ^s[0-9]{{2}}$"
        )
        assert isinstance(rule["flow"], str) and rule["flow"], f"{rid}: empty flow"
        assert isinstance(rule["invocation"], str) and rule["invocation"], (
            f"{rid}: invocation must be a non-empty copy-ready string (FR-006)"
        )
        assert isinstance(rule["rationale"], str) and rule["rationale"], f"{rid}: empty rationale"
        assert isinstance(rule["priority"], int), f"{rid}: priority must be int"
        assert rule["confirmationClass"] in {"reversible", "destructive"}, (
            f"{rid}: confirmationClass {rule['confirmationClass']!r} out of range"
        )


# --- C-4: isomorphic with learned rules ---


def test_c4_seed_and_learned_shapes_are_isomorphic(seed):
    for rule in seed["rules"]:
        keys = set(rule)
        # The seed side adds provenance (+ optional notes); the runtime side adds
        # the four state objects. Everything else must be the shared semantic core.
        assert keys - LEARNED_ONLY - {"provenance", "notes"} == SHARED_SEMANTIC, (
            f"{rule['ruleId']}: shared semantic field set diverged — "
            f"got {sorted(keys - LEARNED_ONLY - {'provenance', 'notes'})}, "
            f"expected {sorted(SHARED_SEMANTIC)}"
        )
        assert not (keys & LEARNED_ONLY), (
            f"{rule['ruleId']}: carries runtime-only fields {sorted(keys & LEARNED_ONLY)}"
        )


# --- C-5: every seed rule carries traceable provenance ---


def test_c5_provenance_four_keys_present(seed):
    for rule in seed["rules"]:
        rid = rule["ruleId"]
        prov = rule.get("provenance")
        assert isinstance(prov, dict), f"{rid}: origin=seed but provenance missing"
        assert set(prov) == PROVENANCE_KEYS, (
            f"{rid}: provenance keys must be exactly {sorted(PROVENANCE_KEYS)}, "
            f"got {sorted(prov)}"
        )
        assert prov["anchorKind"] in ANCHOR_KINDS, (
            f"{rid}: anchorKind {prov['anchorKind']!r} not in {sorted(ANCHOR_KINDS)}"
        )
        for key in PROVENANCE_KEYS:
            assert isinstance(prov[key], str) and prov[key].strip(), (
                f"{rid}: provenance.{key} must be a non-empty string"
            )
        expected_anchor = (
            "## Handoffs" if prov["anchorKind"] == "handoffs" else prov["anchor"]
        )
        assert prov["anchor"] == expected_anchor or prov["anchorKind"] == "owning-section", (
            f"{rid}: handoffs-kind anchor must be '## Handoffs', got {prov['anchor']!r}"
        )


# --- C-6 / C-7: the source section really exists and still says this ---


def _anchor_body(prov: dict, rid: str) -> str:
    path = ROOT / prov["file"]
    assert path.is_file(), f"{rid}: provenance.file does not exist: {prov['file']}"
    heading = "Handoffs" if prov["anchorKind"] == "handoffs" else prov["anchor"]
    body = section_body(path.read_text(encoding="utf-8"), heading)
    assert body is not None, (
        f"{rid}: anchor section not found in {prov['file']}: "
        f"anchorKind={prov['anchorKind']} anchor={prov['anchor']!r}"
    )
    return body


def test_c6_quote_is_verbatim_substring_of_source_section(seed):
    for rule in seed["rules"]:
        rid = rule["ruleId"]
        prov = rule["provenance"]
        body = norm(_anchor_body(prov, rid))
        quote = norm(prov["quote"])
        assert quote in body, (
            f"{rid}: provenance.quote is not a verbatim substring of the anchor "
            f"section (whitespace-normalized).\n"
            f"  file       : {prov['file']}\n"
            f"  anchorKind : {prov['anchorKind']}\n"
            f"  anchor     : {prov['anchor']}\n"
            f"  quote      : {quote!r}\n"
            f"  FIX: re-copy the quote verbatim from that section, or sync the seed "
            f"to the rewritten source. Do NOT loosen this assertion."
        )


def test_c7_flow_name_still_present_in_source_section(seed):
    """Drift detection: the owner section must still name the target flow."""
    for rule in seed["rules"]:
        rid = rule["ruleId"]
        prov = rule["provenance"]
        flow = rule["flow"]
        body = _anchor_body(prov, rid)
        # The flow may be written bare (`/speckit.clarify`) or with a mode suffix
        # in the rule; the source must name at least the callable itself.
        callable_name = flow.split()[0].strip("`")
        assert callable_name in body, (
            f"DRIFT DETECTED — {rid}: flow {callable_name!r} no longer appears in its "
            f"provenance section.\n"
            f"  file       : {prov['file']}\n"
            f"  anchorKind : {prov['anchorKind']}\n"
            f"  anchor     : {prov['anchor']}\n"
            f"  missing flow: {callable_name}\n"
            f"  FIX: sync templates/proactive-trigger-seed.json to the rewritten "
            f"source section. Do NOT loosen this assertion — a silent divergence is "
            f"exactly what this clause exists to prevent."
        )


# --- C-8: coverage completeness and identity resolvability ---


def test_c8_covers_all_thirteen_named_situations(seed):
    ids = [s["id"] for s in seed["situations"]]
    expected = [f"s{n:02d}" for n in range(1, SITUATION_COUNT + 1)]
    assert sorted(ids) == expected, (
        f"situations must be exactly {expected}, got {sorted(ids)}"
    )
    covered = {r["situationId"] for r in seed["rules"]}
    missing = set(ids) - covered
    assert not missing, f"situations with no rule: {sorted(missing)}"
    assert len(seed["rules"]) == RULE_COUNT, (
        f"expected {RULE_COUNT} seed rules, got {len(seed['rules'])}"
    )


def test_c8_situations_carry_full_e1_shape(seed):
    for sit in seed["situations"]:
        sid = sit.get("id", "<missing>")
        assert set(sit) == SITUATION_KEYS, (
            f"{sid}: situations[] must carry the full E1 shape {sorted(SITUATION_KEYS)}, "
            f"got {sorted(sit)}"
        )
        assert set(sit["match"]) == MATCH_KEYS, (
            f"{sid}: match must be exactly {sorted(MATCH_KEYS)}, got {sorted(sit['match'])}"
        )
        assert isinstance(sit["name"], str) and sit["name"], f"{sid}: empty name"
        assert isinstance(sit["signals"], list), f"{sid}: signals must be a list"
        for key in ("signalsAll", "signalsAny"):
            assert isinstance(sit["match"][key], list), f"{sid}: match.{key} must be a list"


def test_c8_v1_3_identity_is_unique(seed):
    seen: dict[tuple, str] = {}
    for sit in seed["situations"]:
        key = (sit["match"]["stage"], tuple(sorted(sit["match"]["signalsAll"])))
        assert key not in seen, (
            f"V1.3 violated: {sit['id']} and {seen[key]} both declare "
            f"(stage={key[0]!r}, signalsAll={sorted(key[1])}) — identity would not be unique"
        )
        seen[key] = sit["id"]


def test_c8_vocabulary_within_closed_enumeration(seed):
    for sit in seed["situations"]:
        sid = sit["id"]
        assert sit["stage"] in STAGES, f"{sid}: stage {sit['stage']!r} out of range"
        assert sit["match"]["stage"] in STAGES, (
            f"{sid}: match.stage {sit['match']['stage']!r} out of range"
        )
        for sig in list(sit["signals"]) + list(sit["match"]["signalsAll"]) + list(sit["match"]["signalsAny"]):
            assert sig in SIGNALS, f"{sid}: signal {sig!r} out of range"
        assert sit["stage"] == sit["match"]["stage"], (
            f"{sid}: stage and match.stage disagree"
        )
        assert sorted(sit["signals"]) == sorted(sit["match"]["signalsAll"]), (
            f"{sid}: signals must equal match.signalsAll"
        )


def test_c8_vocabulary_enumeration_sizes():
    """The vocabulary sizes are themselves the contract (9 stages / 12 signals)."""
    assert len(STAGES) == 9, f"stage enumeration must hold 9 values, got {len(STAGES)}"
    assert len(SIGNALS) == 12, f"signal enumeration must hold 12 values, got {len(SIGNALS)}"


def test_c8_vocabulary_matches_data_model():
    """Guard this test's own copy of the vocabulary against the design record."""
    text = DATA_MODEL.read_text(encoding="utf-8")
    for stage in STAGES:
        assert f"`{stage}`" in text, f"stage {stage!r} not found in data-model.md"
    for signal in SIGNALS:
        assert f"`{signal}`" in text, f"signal {signal!r} not found in data-model.md"


# --- C-9: classification does not overreach ---


def test_c9_confirmation_class_matches_data_model_column(seed):
    by_id = {r["ruleId"]: r for r in seed["rules"]}
    for rid, rule in by_id.items():
        expected = "destructive" if rid in DESTRUCTIVE_RULES else "reversible"
        assert rule["confirmationClass"] == expected, (
            f"{rid}: confirmationClass must be {expected!r} per data-model.md's "
            f"named-situation table, got {rule['confirmationClass']!r}"
        )


def test_c9_destructive_entries_cite_criteria_by_reference(seed):
    for rule in seed["rules"]:
        if rule["confirmationClass"] != "destructive":
            continue
        rid = rule["ruleId"]
        notes = rule.get("notes")
        assert notes, (
            f"{rid}: destructive entry must carry `notes` explaining the criteria's provenance"
        )
        assert "confirmation-gates.md" in notes, (
            f"{rid}: notes must cite shared/guidelines/confirmation-gates.md by path"
        )


def test_c9_seed_does_not_restate_the_criteria_table(seed):
    raw = SEED.read_text(encoding="utf-8")
    assert "| 门控 | 所在面 | 保留理由 |" not in raw, (
        "the governance-kept classification table must not be restated in the seed"
    )
    for bullet in (
        "删除文件或数据(delete / 清空存储)",
        "移动/归档既有工件(move / archive / restructure)",
    ):
        assert bullet not in raw, f"destructive list restated in the seed: {bullet!r}"


# --- C-10: whole-copy distribution reachable, merge never reverts tuning ---


def test_c10_seed_is_reachable_by_init_whole_copy():
    """templates/ top-level non-commands files are copied by iterdir(); no manifest edit."""
    cli = (ROOT / "src" / "specify_cli" / "__init__.py").read_text(encoding="utf-8")
    assert "def copy_local_templates" in cli, "copy_local_templates disappeared"
    # The copy must stay a generic whole-directory walk, not a per-file manifest
    # that a new template would have to be added to.
    body = cli[cli.index("def copy_local_templates"):]
    body = body[: body.index("\ndef ", 10)]
    assert "iterdir()" in body, (
        "copy_local_templates no longer walks templates/ with iterdir(); a new "
        "top-level template would need a manifest edit, which C-10 says must not"
    )
    assert SEED.parent.name == "templates", "seed must live at the top level of templates/"


def test_c10_rule_id_pairing_is_stable(seed):
    """r-00N pairs with s0N so quickstart and contracts can cite stable ids."""
    for rule in seed["rules"]:
        n = int(rule["ruleId"].split("-")[1])
        expected = f"s{n:02d}"
        assert rule["situationId"] == expected, (
            f"{rule['ruleId']} must pair with {expected}, got {rule['situationId']!r}"
        )
    ids = sorted(int(r["ruleId"].split("-")[1]) for r in seed["rules"])
    assert ids == list(range(1, RULE_COUNT + 1)), (
        f"seed ruleIds must be the contiguous block r-001..r-{RULE_COUNT:03d}, got {ids}"
    )


def test_c10_v2_4_flow_unique_per_situation(seed):
    seen: dict[str, str] = {}
    for rule in seed["rules"]:
        key = rule["situationId"]
        assert key not in seen or seen[key] != rule["flow"], (
            f"V2.4 violated: {rule['ruleId']} and {seen[key]} both map "
            f"{key} to the same flow"
        )
        seen.setdefault(key, rule["flow"])


def test_c10_generated_from_records_the_derivation_batch(seed):
    gen = seed["generatedFrom"]
    assert "Handoffs" in gen, (
        f"generatedFrom must name the derivation source, got {gen!r}"
    )
