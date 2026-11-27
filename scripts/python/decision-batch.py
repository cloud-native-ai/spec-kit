#!/usr/bin/env python3
"""decision-batch.py — deterministic batch decision panel engine (Feature 112).

The batch capability's rules are owned by ``shared/definitions/decision-definitions.md``
(batch extension): the closed pending-source roster, the pending-item block grammar, the
presentation contract, the recommended default and grounding join, the disposition and
reply contract, the batch record contract, the completeness/refusal rules and the replay
contract. This engine performs the Program-First judgements over them (scan, membership
validation, bookkeeping, pointer resolution) and never restates their tables.

Actions (closed set):
  scan    read-only: scan the closed source roster and render one presentation
          (text body + machine payload).
  record  the only writer: re-scan, validate the reply, mint the batch id and write the
          batch record through the memory engine.
  replay  read-only: reconstruct one recorded batch from the batch record and resolvable
          pointers alone; any unresolvable pointer is reported and the exit is non-zero.

Options of every action:
  --workspace-root PATH   the workspace the panel reads (default: the current directory)
  --format {text,json}    output format (default: text)
  --presentation PATH     the scan payload a reply is bound to (record)
  --reply PATH            the reply file carrying the user's verbatim text (record)
  --authorization {interactive,unattended}
                          caller-declared interaction authorization (record); missing
                          is treated as unattended and the record is refused
  --batch PATH            the batch record to replay (replay)
  -h / --help             this body (same body for both spellings), exit 0
  --version               one line ``<script-name> <framework-version>``, exit 0

Exit codes: 0 = success (including the explicit ``nothing-pending`` result) /
1 = a documented refusal / 2 = usage or environment error.

Side effects: scan and replay write nothing; record writes only through the named
carriers. Standard library only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

EXIT_OK = 0
EXIT_REFUSED = 1
EXIT_USAGE = 2

#: The closed declared action set (C-608). A fourth value MUST NOT be accepted before the
#: owner page and this tuple are revised in the same change.
ACTIONS = ("scan", "record", "replay")

#: Every declared flag; an undeclared ``-*`` token is refused before any action runs.
DECLARED_OPTIONS = (
    "--workspace-root", "--format", "--presentation", "--reply", "--authorization",
    "--batch", "--version", "-h", "--help",
)

# --version and the undeclared-option refusal come from the one shared helper; a copy that
# lacks the helper still runs its actions (same pattern as validate-decisions.py).
_SIG_DIR = str(Path(__file__).resolve().parent)
if _SIG_DIR not in sys.path:
    sys.path.insert(0, _SIG_DIR)
try:
    from script_interface_cli import attach_to_parser_tree as _sig_attach
    from script_interface_cli import configure_parser as _sig_configure
    from script_interface_cli import guard_argv as _sig_guard
    from script_interface_cli import resolve_version as _resolve_version
except ImportError:
    def _sig_configure(parser, **_kwargs):
        return parser

    def _sig_attach(parser, **_kwargs):
        return parser

    def _sig_guard(_argv=None, declared=None, **_kwargs):
        return None

    def _resolve_version(_start=None):
        return "unknown"


# --------------------------------------------------------------------------- #
# Owner-page constants (one owner: shared/definitions/decision-definitions.md)
# --------------------------------------------------------------------------- #
#: The closed two-source roster, in roster order (C-101).
SOURCES = ("register-open-decision-row", "authored-pending-item")
REGISTER_REL = ".specify/register.md"
SCAN_ROOTS = (".specify/specs", ".specify/goals", ".specify/anchoring", ".specify/teams")
BLOCK_HEADING_PREFIX = "### PENDING —"
BLOCK_FIELD_SET = frozenset((
    "decision_class", "subject", "same_name_conflict", "resource_locator", "context",
    "options", "basis", "origin", "created_at", "resolution",
))
REQUIRED_BLOCK_FIELDS = ("decision_class", "subject", "context", "options", "basis",
                         "origin", "created_at")
CLASS_DOMAIN = ("human-interactive", "ai-autonomous")
OPTION_ELEMENTS = ("consequences", "reversibility", "default", "evidence")
BATCH_ID_RE = re.compile(r"^B-\d{8}T\d{6}Z-[0-9a-f]{8}$")
BATCH_TITLE_PREFIX = "decision-batch-"
PRIOR_BATCH_FILE_PREFIX = "decision-batch-"

FIELD_RE = re.compile(r"^- \*\*([a-z][a-z0-9_]*)\*\*:\s*(.*)$")
BLOCK_HEADING_RE = re.compile(r"^### PENDING\s+—\s*(.+?)\s*$")
RECORD_HEADING_RE = re.compile(r"^###\s+(D-\d{3}(?:-[A-Za-z0-9]+)?)\s+—\s*(.*)$")
TENSION_TOKEN_RE = re.compile(r"(?<![A-Za-z0-9-])T-\d{3}(?![A-Za-z0-9-])")
REGISTER_ID_RE = re.compile(r"^(?:OI-|D-)")

FLOOR_KEYS = ("why_now", "silence_meaning", "how_to_object", "what_stays_pending",
              "completeness_disclosure")
FLOOR_LABELS = {
    "why_now": "为什么现在呈现",
    "silence_meaning": "沉默将意味着什么",
    "how_to_object": "如何提出异议或暂缓",
    "what_stays_pending": "哪些事项保持待定及原因",
    "completeness_disclosure": "完备性说明",
}

REASON_TEXT = {
    "authority-unresolved": "来源行没有给出可解析的显式块路径",
    "ambiguous-link": "来源行对应的载体上有多个块争用同一条来源行",
    "class-missing": "未声明决策类别或类别值无法识别",
    "malformed-field": "存在格式异常的字段行",
    "unknown-field": "存在未定义的字段",
    "duplicate-field": "同一字段重复出现",
    "option-count-mismatch": "选项声明数量与条目数量不一致",
    "missing-field": "缺少必填内容",
    "option-element-missing": "存在要素不全的选项",
    "evidence-unresolvable": "选项的证据指针无法解析",
    "default-missing": "没有声明默认选项",
    "multiple-defaults": "声明了多个默认选项",
    "default-irreversible": "建议的默认选项不可逆",
    "option-set-mismatch": "不同来源给出的选项集不一致",
    "prior-decision-conflict": "与既往决策的选中项不一致",
}

STATE_TEXT = {
    "eligible": "可以按建议默认值结案",
    "incomplete": "信息不完整，本次不会结案",
    "source-conflict": "不同来源的选项集不一致，需要您明确选择",
    "no-default": "没有唯一的默认选项，需要您明确选择",
    "irreversible-default": "建议的默认选项不可逆，需要您明确选择",
    "prior-decision-conflict": "与既往决策的选中项不一致，需要您明确选择",
}

OBJECTION_INSTRUCTIONS = (
    "点名本项的完整名称，并写出您选择的完整选项名称；也可以说明暂缓本项。"
)

EXCLUDED_FAMILY_KEYS = ("rec-row", "clarification-marker", "parked-idea",
                        "interactive-gate", "autonomous-checkpoint")


class Refusal(Exception):
    """A documented refusal (exit 1): named source, reason and detail."""

    def __init__(self, source_id: str, reason: str, detail: str = ""):
        super().__init__(f"{source_id}: {reason}: {detail}")
        self.source_id = source_id
        self.reason = reason
        self.detail = detail


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def read_text(path: Path, source_id: str, rel: str) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise Refusal(source_id, "unreadable", f"{rel}: {exc}")


def fenced_mask(lines: list[str]) -> list[bool]:
    mask: list[bool] = []
    in_fence = False
    for line in lines:
        if line.strip().startswith("```"):
            mask.append(True)
            in_fence = not in_fence
            continue
        mask.append(in_fence)
    return mask


# --------------------------------------------------------------------------- #
# Pending-item block parser (owner: § 待决策项块)
# --------------------------------------------------------------------------- #
def parse_blocks(text: str) -> list[dict]:
    """Every ``### PENDING —`` block outside fenced code, with its raw fields."""
    lines = text.splitlines()
    mask = fenced_mask(lines)
    blocks: list[dict] = []
    current: dict | None = None
    current_field: str | None = None
    for index, line in enumerate(lines, start=1):
        if mask[index - 1]:
            continue
        heading = BLOCK_HEADING_RE.match(line)
        if heading:
            current = {
                "subject": heading.group(1).strip(),
                "line": index,
                "fields": {},
                "continuations": {},
                "defects": [],
            }
            blocks.append(current)
            current_field = None
            continue
        if line.startswith("#"):
            current = None
            current_field = None
            continue
        if current is None:
            continue
        if not line.strip():
            continue
        field = FIELD_RE.match(line)
        if field:
            name, value = field.group(1), field.group(2).strip()
            if name not in BLOCK_FIELD_SET:
                current["defects"].append(("unknown-field", index, name))
            elif name in current["fields"]:
                current["defects"].append(("duplicate-field", index, name))
            else:
                current["fields"][name] = value
            current["continuations"].setdefault(name, [])
            current_field = name
            continue
        if line.startswith((" ", "\t")):
            if current_field:
                current["continuations"][current_field].append(line)
            else:
                current["defects"].append(("malformed-field", index, line.strip()))
            continue
        if line.startswith("- ") or line.strip():
            current["defects"].append(("malformed-field", index, line.strip()))
    for block in blocks:
        block["options"] = parse_options_block(block)
    return blocks


def parse_options_block(block: dict) -> dict:
    """The closed option set of one block: declared count, entries, forced, defects."""
    result = {"declared": None, "entries": [], "forced": "", "present": "options" in block["fields"]}
    if not result["present"]:
        return result
    raw = block["fields"].get("options", "").strip()
    count = re.match(r"^(\d+)\s*$", raw)
    if count:
        result["declared"] = int(count.group(1))
    else:
        block["defects"].append(("malformed-field", block["line"], "options value"))
    entries: list[dict] = []
    for line in block["continuations"].get("options", []):
        entry = re.match(r"^\s{2,}-\s+label\s*:\s*(.*)$", line)
        if entry:
            entries.append({
                "label": entry.group(1).strip(),
                "consequences": "", "reversibility": "", "default": "", "evidence": "",
                "path": "",
            })
            continue
        element = re.match(r"^\s{2,}([a-z_]+)\s*:\s*(.*)$", line)
        if element:
            name, value = element.group(1), element.group(2).strip()
            if name == "forced":
                result["forced"] = value
                continue
            if entries and name in OPTION_ELEMENTS + ("path",):
                entries[-1][name] = value
                continue
        if line.strip():
            block["defects"].append(("malformed-field", block["line"], line.strip()))
    result["entries"] = entries
    if result["declared"] is not None and result["declared"] != len(entries):
        block["defects"].append(("option-count-mismatch", block["line"], raw))
    labels: set[str] = set()
    for entry in entries:
        label = entry["label"]
        missing = [name for name in OPTION_ELEMENTS if not entry.get(name, "").strip()]
        if not label:
            missing.append("label")
        if missing:
            block["defects"].append(("option-element-missing", block["line"], label or "?"))
        if entry["default"].strip() and entry["default"].strip() not in ("yes", "no"):
            block["defects"].append(("malformed-field", block["line"], "default value"))
        key = label.casefold()
        if key in labels:
            block["defects"].append(("malformed-field", block["line"], f"duplicate label {label!r}"))
        labels.add(key)
        if label.casefold() == "other" and not entry["path"].strip():
            block["defects"].append(("option-element-missing", block["line"], "other without path"))
    if len(entries) == 1 and not result["forced"].strip():
        block["defects"].append(("option-element-missing", block["line"], "forced"))
    return result


def block_class(block: dict) -> str | None:
    value = block["fields"].get("decision_class", "").strip()
    return value or None


def block_locator(block: dict) -> str:
    if block["fields"].get("same_name_conflict", "").strip().lower() == "true":
        return block["fields"].get("resource_locator", "").strip()
    return ""


def default_entries(block: dict) -> list[dict]:
    return [entry for entry in block["options"]["entries"]
            if entry["default"].strip().lower() == "yes"]


# --------------------------------------------------------------------------- #
# Prior-experience carriers (owner: § 建议默认值与依据)
# --------------------------------------------------------------------------- #
def parse_decision_records(text: str) -> list[dict]:
    """``### D-NNN`` records outside fences, with context / chosen / rationale values."""
    lines = text.splitlines()
    mask = fenced_mask(lines)
    records: list[dict] = []
    current: dict | None = None
    for index, line in enumerate(lines, start=1):
        if mask[index - 1]:
            continue
        heading = RECORD_HEADING_RE.match(line)
        if heading:
            current = {"id": heading.group(1), "subject": heading.group(2).strip(),
                       "line": index, "fields": {}}
            records.append(current)
            continue
        if line.startswith("#"):
            current = None
            continue
        if current is None:
            continue
        field = FIELD_RE.match(line)
        if field:
            current["fields"].setdefault(field.group(1), field.group(2).strip())
    return records


def parse_batch_record_subjects(text: str) -> set[str]:
    """Settled identities of a prior batch record: the ``### D-NNN — subject`` headings.

    A parked row produces no decision record, so the parked identity stays presentable.
    """
    return {record["subject"] for record in parse_decision_records(text) if record["subject"]}


def iter_scan_root_files(root: Path):
    for rel_root in SCAN_ROOTS:
        base = root / rel_root
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*.md")):
            rel = path.relative_to(root).as_posix()
            yield rel, path


def build_prior_index(root: Path) -> dict:
    """Prior decision records, batch-settled subjects and the resolvable text cache."""
    records: list[dict] = []
    texts: dict[str, str] = {}
    batch_subjects: set[str] = set()
    for rel, path in iter_scan_root_files(root):
        text = read_text(path, "authored-pending-item", rel)
        texts[rel] = text
        for record in parse_decision_records(text):
            records.append({**record, "carrier": rel})
    knowledge = root / ".specify" / "knowledge"
    if knowledge.is_dir():
        for path in sorted(knowledge.glob("*.md")):
            rel = path.relative_to(root).as_posix()
            text = read_text(path, "prior-batch-records", rel)
            texts[rel] = text
            if path.name.startswith(PRIOR_BATCH_FILE_PREFIX):
                if not re.search(r"(?<![A-Za-z0-9-])B-\d{8}T\d{6}Z-[0-9a-f]{8}(?![A-Za-z0-9-])", text):
                    raise Refusal("prior-batch-records", "unparseable",
                                  f"{rel}: a decision-batch entry carries no batch id")
                batch_subjects |= parse_batch_record_subjects(text)
            for record in parse_decision_records(text):
                records.append({**record, "carrier": rel})
    records.sort(key=lambda rec: (rec["carrier"], rec["line"]))
    return {"records": records, "texts": texts, "batch_subjects": batch_subjects}


def is_prior_carrier(rel: str, text: str) -> bool:
    if rel.startswith((".specify/history/", ".specify/feedback/", ".specify/knowledge/")):
        return True
    if any(rel.startswith(root + "/") for root in SCAN_ROOTS):
        return bool(re.search(r"(?m)^### (?:D-\d{3}|T-\d{3})", text))
    return False


def resolve_pointer(root: Path, pointer: str) -> tuple[bool, str]:
    path_part, _, anchor = pointer.partition("#")
    path_part = path_part.strip()
    if not path_part:
        return False, "empty path"
    raw = Path(path_part)
    if raw.is_absolute() or path_part.startswith(("http://", "https://")):
        return False, "not a repository-relative path"
    target = root / path_part
    if not target.is_file():
        return False, "path does not exist"
    if anchor.strip():
        try:
            body = target.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            return False, "carrier unreadable"
        if anchor.strip().casefold() not in body.casefold():
            return False, "anchor not findable"
    return True, ""


def compute_grounding(root: Path, prior: dict, subject: str, default_block: dict | None,
                      default_label: str | None) -> dict:
    """The deterministic closed-input join of § 建议默认值与依据."""
    pointers: list[str] = []

    def add(pointer: str) -> None:
        if pointer not in pointers:
            pointers.append(pointer)

    texts = prior["texts"]
    if default_block is not None and default_label:
        for entry in default_block["options"]["entries"]:
            if entry["label"] != default_label:
                continue
            for pointer in entry["evidence"].split(";"):
                pointer = pointer.strip()
                if not pointer:
                    continue
                path_part = pointer.partition("#")[0].strip()
                rel = path_part.lstrip("./")
                resolved, _ = resolve_pointer(root, pointer)
                if not resolved:
                    continue
                text = texts.get(rel)
                if text is None:
                    try:
                        text = (root / rel).read_text(encoding="utf-8")
                    except (OSError, UnicodeDecodeError):
                        continue
                if is_prior_carrier(rel, text):
                    add(pointer)
    matched = [rec for rec in prior["records"] if subject and subject in rec["fields"].get("context", "")]
    for record in matched:
        add(record["carrier"])
    for record in matched:
        for token in sorted(set(TENSION_TOKEN_RE.findall(record["fields"].get("rationale", "")))):
            for rel, text in sorted(texts.items()):
                if token in text:
                    add(rel)
                    break
    return {"status": "grounded" if pointers else "no-evidence", "pointers": pointers}


def detect_prior_conflict(prior: dict, subject: str, default_label: str | None) -> dict | None:
    if not default_label:
        return None
    for record in prior["records"]:
        if not subject or subject not in record["fields"].get("context", ""):
            continue
        chosen = record["fields"].get("chosen_option", "").strip()
        if chosen and chosen != default_label:
            return {"pointer": record["carrier"], "chosen_label": chosen}
    return None


# --------------------------------------------------------------------------- #
# Register source (owner: § 待决策项来源清单)
# --------------------------------------------------------------------------- #
def parse_register_rows(text: str) -> list[tuple[int, list[str]]] | None:
    """(line number, de-emphasised-free cells) of the register's table; None if unparseable."""
    lines = text.splitlines()
    header_index = None
    for index, line in enumerate(lines):
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if len(cells) < 4:
            continue
        following = lines[index + 1].strip() if index + 1 < len(lines) else ""
        if following.startswith("|") and set(following.replace("|", "").replace(" ", "")) <= set("-: "):
            header_index = index
            break
    if header_index is None:
        return None
    rows: list[tuple[int, list[str]]] = []
    for index in range(header_index + 2, len(lines)):
        stripped = lines[index].strip()
        if not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if len(cells) < 4:
            continue
        rows.append((index + 1, cells))
    return rows


def de_emphasis(cell: str) -> str:
    return re.sub(r"[*`]", "", cell).strip()


def explicit_repo_path(cell: str) -> str | None:
    cleaned = de_emphasis(cell)
    match = re.match(r"^(?:\./)?(\.specify/[A-Za-z0-9._/-]+\.md)$", cleaned)
    return match.group(1) if match else None


def scan_register(root: Path) -> dict:
    path = root / REGISTER_REL
    outcome = {"source_id": "register-open-decision-row", "presence": "read",
               "candidates": [], "rec_rows": 0}
    if not path.is_file():
        outcome["presence"] = "absent"
        outcome["absent_reason"] = "register file is not present"
        return outcome
    text = read_text(path, "register-open-decision-row", REGISTER_REL)
    rows = parse_register_rows(text)
    if rows is None:
        raise Refusal("register-open-decision-row", "unparseable",
                      f"{REGISTER_REL}: the table cannot be parsed into its columns")
    for position, (line, cells) in enumerate(rows):
        row_id = de_emphasis(cells[0])
        status = de_emphasis(cells[3]) if len(cells) > 3 else ""
        if not REGISTER_ID_RE.match(row_id):
            if row_id.startswith("REC-") and re.match(r"open\b", status):
                outcome["rec_rows"] += 1
            continue
        if not re.match(r"open\b", status):
            continue
        outcome["candidates"].append({
            "source_id": "register-open-decision-row",
            "carrier": REGISTER_REL,
            "locator": row_id,
            "position": position,
            "line": line,
            "authority": cells[2] if len(cells) > 2 else "",
            "subject": row_id,
        })
    return outcome


def resolve_row_block(root: Path, row: dict) -> tuple[dict | None, str | None]:
    rel = explicit_repo_path(row["authority"])
    if not rel:
        return None, "authority-unresolved"
    path = root / rel
    if not path.is_file():
        return None, "authority-unresolved"
    text = read_text(path, "authored-pending-item", rel)
    blocks = [block for block in parse_blocks(text)
              if re.search(r"(?<![A-Za-z0-9_-])" + re.escape(row["locator"]) + r"(?![A-Za-z0-9_-])",
                           block["fields"].get("origin", ""))]
    if not blocks:
        return None, "authority-unresolved"
    if len(blocks) > 1:
        return None, "ambiguous-link"
    return blocks[0], None


def scan_authored(root: Path) -> dict:
    outcome = {"source_id": "authored-pending-item", "presence": "read",
               "candidates": [], "absent_roots": []}
    present = 0
    for rel_root in SCAN_ROOTS:
        base = root / rel_root
        if not base.is_dir():
            outcome["absent_roots"].append(rel_root)
            continue
        present += 1
        for path in sorted(base.rglob("*.md")):
            rel = path.relative_to(root).as_posix()
            text = read_text(path, "authored-pending-item", rel)
            for block in parse_blocks(text):
                outcome["candidates"].append({
                    "source_id": "authored-pending-item",
                    "carrier": rel,
                    "locator": f"L{block['line']}",
                    "position": block["line"],
                    "subject": block["subject"],
                    "block": block,
                })
    if present == 0:
        outcome["presence"] = "absent"
        outcome["absent_reason"] = "every scan root is absent"
    return outcome


# --------------------------------------------------------------------------- #
# Scan core (owner: § 批次状态 / § 批次呈现契约 / § 完备性与拒绝)
# --------------------------------------------------------------------------- #
SOURCE_ORDER = {source_id: index for index, source_id in enumerate(SOURCES)}


def candidate_sort_key(candidate: dict) -> tuple:
    return (SOURCE_ORDER[candidate["source_id"]], candidate["carrier"], candidate["position"])


def classify_groups(root: Path, groups: list[list[dict]], prior: dict) -> tuple[list[dict], list[dict]]:
    items: list[dict] = []
    exclusions: list[dict] = []
    for members in groups:
        members = sorted(members, key=candidate_sort_key)
        blocks = [member["block"] for member in members if member.get("block")]
        primary = members[0]
        primary_block = blocks[0] if blocks else None
        subject = primary_block["subject"] if primary_block else primary["locator"]
        locator = block_locator(primary_block) if primary_block else ""
        classes = sorted({block_class(block) for block in blocks if block_class(block)})

        def exclude(reason: str, via: str | None = None) -> None:
            for member in members:
                entry = {
                    "reason": reason,
                    "source_id": member["source_id"],
                    "carrier": member["carrier"],
                    "locator": member["locator"],
                    "subject": subject,
                }
                if via:
                    entry["via"] = via
                if reason == "not-human-held" and len(classes) > 1:
                    entry["classes"] = classes
                elif reason == "not-human-held":
                    entry["classes"] = ["ai-autonomous"]
                exclusions.append(entry)

        if len(classes) > 1 or classes == ["ai-autonomous"]:
            exclude("not-human-held")
            continue
        if any("resolution" in block["fields"] for block in blocks):
            exclude("already-resolved", via="resolution-field")
            continue
        if subject in prior["batch_subjects"]:
            exclude("already-resolved", via="prior-batch")
            continue

        reasons: list[str] = []
        missing_fields: list[str] = []
        if primary_block is None:
            reasons.append(primary.get("link_error") or "authority-unresolved")
            reasons.append("class-missing")
            missing_fields.extend(REQUIRED_BLOCK_FIELDS)
        else:
            for name in REQUIRED_BLOCK_FIELDS:
                if name == "subject":
                    continue
                if not primary_block["fields"].get(name, "").strip():
                    reasons.append("missing-field")
                    missing_fields.append(name)
            if not block_class(primary_block) or block_class(primary_block) not in CLASS_DOMAIN:
                reasons.append("class-missing")
            for defect in primary_block["defects"]:
                reasons.append(defect[0])
            for entry in primary_block["options"]["entries"]:
                for pointer in entry["evidence"].split(";"):
                    pointer = pointer.strip()
                    if pointer and not resolve_pointer(root, pointer)[0]:
                        reasons.append("evidence-unresolvable")
        reason_set = sorted(set(reasons), key=reasons.index) if reasons else []

        option_sets = [tuple(entry["label"].strip() for entry in block["options"]["entries"])
                       for block in blocks]
        defaults = default_entries(primary_block) if primary_block else []
        default_label = defaults[0]["label"].strip() if len(defaults) == 1 else None
        conflict = detect_prior_conflict(prior, subject, default_label) if default_label else None
        grounding = compute_grounding(root, prior, subject, primary_block, default_label)

        if reason_set:
            state = "incomplete"
            state_reasons = reason_set
        elif len(option_sets) > 1 and any(labels != option_sets[0] for labels in option_sets[1:]):
            state = "source-conflict"
            state_reasons = ["option-set-mismatch"]
            default_label = None
        elif len(defaults) != 1:
            state = "no-default"
            state_reasons = ["multiple-defaults" if len(defaults) > 1 else "default-missing"]
            default_label = None
        elif defaults[0]["reversibility"].strip().lower().startswith("irreversible"):
            state = "irreversible-default"
            state_reasons = ["default-irreversible"]
        elif conflict:
            state = "prior-decision-conflict"
            state_reasons = ["prior-decision-conflict"]
        else:
            state = "eligible"
            state_reasons = []

        options = []
        for entry in (primary_block["options"]["entries"] if primary_block else []):
            option = {
                "label": entry["label"],
                "consequences": entry["consequences"],
                "reversibility": entry["reversibility"],
                "default": entry["default"],
                "evidence": entry["evidence"],
            }
            if entry["path"]:
                option["path"] = entry["path"]
            options.append(option)
        qualification = {
            "state": state,
            "reasons": state_reasons,
            "missing_fields": missing_fields,
        }
        if primary_block is not None and primary_block["options"]["forced"]:
            qualification["forced"] = primary_block["options"]["forced"]
        if conflict:
            qualification["prior_decision"] = conflict
        items.append({
            "identity": {"subject": subject, "resource_locator": locator or None},
            "sources": [
                {"source_id": member["source_id"], "carrier": member["carrier"],
                 "locator": member["locator"], "position": member["position"]}
                for member in members
            ],
            "decision_class": block_class(primary_block) if primary_block else None,
            "context": (primary_block["fields"].get("context") or None) if primary_block else None,
            "options": options,
            "recommended_default": {
                "label": default_label,
                "status": grounding["status"],
                "pointers": grounding["pointers"],
                "basis": (primary_block["fields"].get("basis", "") if primary_block else ""),
            },
            "qualification": qualification,
            "objection_instructions": OBJECTION_INSTRUCTIONS,
        })
    return items, exclusions


def group_candidates(candidates: list[dict]) -> list[list[dict]]:
    order: list[tuple[str, str]] = []
    groups: dict[tuple[str, str], list[dict]] = {}
    for candidate in candidates:
        block = candidate.get("block")
        subject = block["subject"] if block else candidate["locator"]
        locator = block_locator(block) if block else ""
        key = (subject, locator)
        if key not in groups:
            groups[key] = []
            order.append(key)
        groups[key].append(candidate)
    ordered = [groups[key] for key in order]
    ordered.sort(key=lambda members: candidate_sort_key(min(members, key=candidate_sort_key)))
    return ordered


def batch_context(payload_items: list[dict], bookkeeping: dict) -> dict:
    pending = [item for item in payload_items if item["qualification"]["state"] != "eligible"]
    if pending:
        parts = []
        for item in pending:
            reasons = "、".join(REASON_TEXT.get(reason, reason)
                                for reason in item["qualification"]["reasons"])
            parts.append(f"{item['identity']['subject']}（{STATE_TEXT[item['qualification']['state']]}：{reasons}）")
        stays = "；".join(parts) + "。"
    else:
        stays = "本次没有需要保持待定的事项。"
    sources_text = "；".join(
        f"{source['source_id']} 在场状态为 {source['presence']}，候选 {source['candidates']} 项"
        for source in bookkeeping["sources"])
    absent_roots = []
    for source in bookkeeping["sources"]:
        absent_roots.extend(source.get("absent_roots", []))
    disclosure = (
        f"本次扫描读取了封闭来源清单中的全部来源（{sources_text}）；每个候选恰被分类一次，"
        f"恒等式成立：候选 {bookkeeping['candidates']} = 呈现行 {bookkeeping['presented_rows']}"
        f" + 合并引用 {bookkeeping['duplicate_merged']} + 具名排除 {len(bookkeeping['named_exclusions'])}。"
    )
    if absent_roots:
        disclosure += " 缺席的扫描根：" + "、".join(absent_roots) + "（按缺席空来源计）。"
    return {
        "why_now": "本批次汇总了登记册中仍标记为待定的决策行，以及项目文档载体中撰写的待决策条目；"
                   "每次调用都重新扫描全部来源，因此呈现的是此刻完整的未决状态。",
        "silence_meaning": "在交互式批次中，如果您对本次呈现作出明确回复，未被点名的可结案事项将按建议默认值结案；"
                           "信息不全、没有唯一默认值、默认不可逆或与既往决定冲突的事项不会因沉默结案。",
        "how_to_object": "对某项有异议时，请点名该项的完整名称，并写出您选择的完整选项名称；"
                         "也可以要求暂缓某项。",
        "what_stays_pending": stays,
        "completeness_disclosure": disclosure,
    }


def scan_workspace(root: Path) -> dict:
    register = scan_register(root)
    authored = scan_authored(root)
    prior = build_prior_index(root)

    candidates: list[dict] = []
    for row in register["candidates"]:
        block, link_error = resolve_row_block(root, row)
        candidate = {
            "source_id": row["source_id"],
            "carrier": row["carrier"],
            "locator": row["locator"],
            "position": row["position"],
        }
        if block is not None:
            candidate["block"] = block
        else:
            candidate["link_error"] = link_error
        candidates.append(candidate)
    candidates.extend(authored["candidates"])

    groups = group_candidates(candidates)
    items, exclusions = classify_groups(root, groups, prior)

    presented_refs = {item["identity"]["subject"] for item in items}
    presented_refs.discard("")
    presented_rows = len(items)
    duplicate_merged = 0
    for members in groups:
        blocks = [member["block"] for member in members if member.get("block")]
        subject = blocks[0]["subject"] if blocks else members[0]["locator"]
        if subject in {item["identity"]["subject"] for item in items}:
            duplicate_merged += len(members) - 1

    books = {
        "sources": [
            {"source_id": register["source_id"], "presence": register["presence"],
             "candidates": len(register["candidates"]),
             **({"absent_reason": register["absent_reason"]} if register.get("absent_reason") else {})},
            {"source_id": authored["source_id"], "presence": authored["presence"],
             "candidates": len(authored["candidates"]),
             **({"absent_roots": authored["absent_roots"]} if authored["absent_roots"] else {}),
             **({"absent_reason": authored["absent_reason"]} if authored.get("absent_reason") else {})},
        ],
        "candidates": len(candidates),
        "presented_rows": presented_rows,
        "duplicate_merged": duplicate_merged,
        "named_exclusions": exclusions,
        "excluded_families": {**{key: 0 for key in EXCLUDED_FAMILY_KEYS},
                              "rec-row": register["rec_rows"]},
        "verdict": "complete",
    }
    del presented_refs
    result = "nothing-pending" if not candidates else "presentation"
    return {
        "action": "scan",
        "result": result,
        "batch_context": batch_context(items, books),
        "bookkeeping": books,
        "items": items,
    }


def presentation_digest(payload: dict) -> str:
    clone = {key: value for key, value in payload.items()
             if key not in ("scan_time", "presentation_digest")}
    body = json.dumps(clone, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


# --------------------------------------------------------------------------- #
# Text projection (user-facing body: no internal identifiers)
# --------------------------------------------------------------------------- #
def state_sentence(item: dict) -> str:
    qualification = item["qualification"]
    text = STATE_TEXT[qualification["state"]] + "。"
    if qualification["reasons"]:
        details = []
        for reason in qualification["reasons"]:
            if reason == "missing-field" and qualification["missing_fields"]:
                fields = "、".join(qualification["missing_fields"])
                details.append(f"缺少必填内容：{fields}")
            else:
                details.append(REASON_TEXT.get(reason, reason))
        text = STATE_TEXT[qualification["state"]] + "（" + "；".join(details) + "）。"
    prior = qualification.get("prior_decision")
    if prior:
        text += f" 既往记录（{prior['pointer']}）选择了「{prior['chosen_label']}」。"
    return text


def render_text(payload: dict) -> str:
    context = payload["batch_context"]
    lines = ["批量决策面板 · 本次呈现", ""]
    if payload["result"] == "nothing-pending":
        lines.append("当前没有待决策项。")
        lines.append("")
        lines.append(context["completeness_disclosure"])
        return "\n".join(lines) + "\n"
    for key in FLOOR_KEYS:
        lines.append(f"【{FLOOR_LABELS[key]}】")
        lines.append(str(context[key]))
        lines.append("")
    for index, item in enumerate(payload["items"], start=1):
        identity = item["identity"]
        title = identity["subject"]
        if identity.get("resource_locator"):
            title += f"（定位：{identity['resource_locator']}）"
        lines.append(f"==== 事项 {index}：{title} ====")
        source_bits = []
        for source in item["sources"]:
            where = source["carrier"]
            if source["source_id"] == "register-open-decision-row":
                where += f"（登记行 {source['locator']}）"
            source_bits.append(where)
        lines.append("来源：" + "；".join(source_bits))
        if item["context"]:
            lines.append("上下文：" + item["context"])
        default = item["recommended_default"]
        if default["label"]:
            lines.append("建议默认值：" + str(default["label"]))
        else:
            lines.append("建议默认值：本项没有唯一的默认选项。")
        if default["basis"]:
            lines.append("建议依据：" + str(default["basis"]))
        if default["status"] == "grounded":
            lines.append("实践经验：" + "；".join(default["pointers"]))
        else:
            lines.append("实践经验：暂无可以指向的既往经验证据。")
        lines.append("当前状态：" + state_sentence(item))
        if item["options"]:
            lines.append("选项：")
            for option in item["options"]:
                mark = "默认" if option["default"].strip().lower() == "yes" else "备选"
                evidence = f"；证据：{option['evidence']}" if option.get("evidence") else ""
                lines.append(
                    f"  - {option['label']}：{option['consequences']}"
                    f"（可逆性：{option['reversibility']}；{mark}{evidence}）")
        else:
            lines.append("选项：本项尚未撰写可比较的选项集。")
        lines.append("异议或暂缓：" + item["objection_instructions"])
        lines.append("")
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------------------- #
# Reply parsing and settlement (owner: § 决策批次与应答 / § 批次处置)
# --------------------------------------------------------------------------- #
REPLY_TOP_KEYS = ("reply_verbatim", "objections", "no_objections")
OBJECTION_KEYS = ("subject", "action", "option_label", "resource_locator")


def parse_reply_file(path: Path) -> dict:
    """The restricted reply-artifact grammar: verbatim text + structured entries."""
    if not path.is_file():
        raise Refusal("reply-file", "missing", str(path))
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise Refusal("reply-file", "unreadable", f"{path}: {exc}")
    lines = text.splitlines()
    verbatim: str | None = None
    no_objections: bool | None = None
    objections: list[dict] = []
    current: dict | None = None
    index = 0
    while index < len(lines):
        line = lines[index]
        stripped = line.strip()
        index += 1
        if not stripped or stripped.startswith("#"):
            continue
        if line.startswith("reply_verbatim:"):
            value = line.split(":", 1)[1].strip()
            if value == "|":
                block: list[str] = []
                while index < len(lines):
                    following = lines[index]
                    if not following.strip():
                        block.append("")
                        index += 1
                        continue
                    if following.startswith(("  ", "\t")):
                        block.append(re.sub(r"^(?: {2,}|\t)", "", following, count=1))
                        index += 1
                        continue
                    break
                verbatim = "\n".join(block).strip("\n")
            else:
                verbatim = value.strip("'\"")
            continue
        if line.startswith("no_objections:"):
            value = line.split(":", 1)[1].strip().lower()
            if value not in ("true", "false"):
                raise Refusal("reply-file", "malformed", f"no_objections: {value!r}")
            no_objections = value == "true"
            continue
        if stripped.startswith("objections:"):
            continue
        entry = re.match(r"^\s*-\s+([a-z_]+)\s*:\s*(.*)$", line)
        if entry and entry.group(1) in OBJECTION_KEYS:
            current = {key: None for key in OBJECTION_KEYS}
            current[entry.group(1)] = entry.group(2).strip()
            objections.append(current)
            continue
        field = re.match(r"^\s+([a-z_]+)\s*:\s*(.*)$", line)
        if field and current is not None and field.group(1) in OBJECTION_KEYS:
            current[field.group(1)] = field.group(2).strip()
            continue
        if not line.startswith((" ", "\t")):
            raise Refusal("reply-file", "malformed", f"unknown key: {stripped}")
    if verbatim is None or not verbatim.strip():
        raise Refusal("reply-file", "not-a-reply",
                      "the reply artifact carries no reply_verbatim text")
    if no_objections is True and objections:
        raise Refusal("reply-file", "malformed",
                      "no_objections: true conflicts with structured objections")
    if no_objections is None and not objections:
        raise Refusal("reply-file", "not-a-reply",
                      "neither a no-objections declaration nor structured objections; a "
                      "follow-up question is not a reply")
    if no_objections is False and not objections:
        raise Refusal("reply-file", "not-a-reply",
                      "no_objections: false without structured objections")
    for objection in objections:
        if not objection.get("subject"):
            raise Refusal("reply-file", "malformed", "an objection carries no subject")
        if objection.get("action") not in ("alternative", "park"):
            raise Refusal("reply-file", "malformed",
                          f"objection action {objection.get('action')!r} is outside "
                          "'alternative' / 'park'")
        if objection["action"] == "alternative" and not objection.get("option_label"):
            raise Refusal("reply-file", "malformed",
                          "an alternative objection carries no option_label")
        if objection["action"] == "park" and objection.get("option_label"):
            raise Refusal("reply-file", "malformed",
                          "a park objection must not name an option")
    return {"verbatim": verbatim, "objections": objections,
            "no_objections": bool(no_objections)}


def identity_key(item: dict) -> tuple[str, str]:
    return (item["identity"]["subject"], item["identity"].get("resource_locator") or "")


def item_fingerprint(item: dict) -> dict:
    default = item["recommended_default"]
    qualification = item["qualification"]
    return {
        "options": [[option.get("label"), option.get("consequences"),
                     option.get("reversibility"), option.get("default"),
                     option.get("evidence")] for option in item.get("options", [])],
        "default": default.get("label"),
        "grounding": [default.get("status"), list(default.get("pointers", []))],
        "qualification": [qualification.get("state"), list(qualification.get("reasons", []))],
        "sources": sorted((source["source_id"], source["carrier"], source["locator"])
                          for source in item.get("sources", [])),
    }


def drift_diff(presentation: dict, fresh: dict) -> list[str]:
    diffs: list[str] = []
    presented = {identity_key(item): item for item in presentation.get("items", [])}
    current = {identity_key(item): item for item in fresh.get("items", [])}
    for key in sorted(set(current) - set(presented)):
        diffs.append(f"candidate added: {key[0]}")
    for key in sorted(set(presented) - set(current)):
        diffs.append(f"candidate removed: {key[0]}")
    for key in sorted(set(presented) & set(current)):
        before = item_fingerprint(presented[key])
        after = item_fingerprint(current[key])
        for field in sorted(before):
            if before[field] != after[field]:
                diffs.append(f"{key[0]}: {field} changed")
    before_books = presentation.get("bookkeeping", {})
    after_books = fresh.get("bookkeeping", {})
    if before_books.get("candidates") != after_books.get("candidates"):
        diffs.append("candidate count changed")
    before_exclusions = sorted(
        (entry.get("reason", ""), entry.get("subject", ""))
        for entry in before_books.get("named_exclusions", []))
    after_exclusions = sorted(
        (entry.get("reason", ""), entry.get("subject", ""))
        for entry in after_books.get("named_exclusions", []))
    if before_exclusions != after_exclusions:
        diffs.append("named exclusions changed")
    return diffs


def recordable_options(item: dict) -> bool:
    """D-9: an incomplete item's alternative needs a grammatically complete record basis."""
    if not item.get("options") or not item.get("context"):
        return False
    if item.get("decision_class") not in CLASS_DOMAIN:
        return False
    blocked = {"option-count-mismatch", "option-element-missing", "malformed-field",
               "unknown-field", "duplicate-field", "missing-field", "evidence-unresolvable"}
    if set(item["qualification"].get("reasons", [])) & blocked:
        return False
    labels: set[str] = set()
    for option in item["options"]:
        for element in OPTION_ELEMENTS:
            if not str(option.get(element, "")).strip():
                return False
        label = str(option.get("label", "")).strip()
        if not label or label.casefold() in labels:
            return False
        labels.add(label)
    return True


def plan_settlements(presentation: dict, reply: dict) -> list[dict]:
    items = presentation.get("items", [])
    objections: dict[int, dict] = {}
    for objection in reply["objections"]:
        subject = objection["subject"]
        locator = objection.get("resource_locator")
        matches = [
            item for item in items
            if item["identity"]["subject"] == subject
            and (locator is None or item["identity"].get("resource_locator") == locator)
        ]
        if not matches:
            raise Refusal("reply-request", "unknown-identity",
                          f"{subject!r} is not an item of this presentation")
        if len(matches) > 1:
            raise Refusal("reply-request", "ambiguous-identity",
                          f"{subject!r} needs a resource_locator to bind one item")
        item = matches[0]
        if id(item) in objections:
            raise Refusal("reply-request", "duplicate-identity",
                          f"{subject!r} carries more than one objection")
        if objection["action"] == "park":
            objections[id(item)] = {"action": "park"}
            continue
        label = objection["option_label"].strip()
        labels = [option["label"] for option in item["options"]]
        if label not in labels:
            other = [option for option in item["options"]
                     if option["label"].strip().casefold() == "other"]
            suffix = ("; the item declares an 'other' option with a path — follow that path "
                      "to add a new option" if other and other[0].get("path")
                      else "; a new option requires an 'other' option carrying a path")
            raise Refusal("reply-request", "non-member-label",
                          f"{label!r} is not a member of the presented option set{suffix}")
        if item["qualification"]["state"] == "incomplete" and not recordable_options(item):
            reasons = ", ".join(item["qualification"].get("reasons", [])) or "incomplete"
            raise Refusal("reply-request", "incomplete-item",
                          f"{subject!r} is incomplete ({reasons}); the resulting record would "
                          "fail the decision grammar")
        objections[id(item)] = {"action": "alternative", "label": label}

    plan: list[dict] = []
    for item in items:
        key = id(item)
        if key in objections:
            objection = objections[key]
            if objection["action"] == "park":
                plan.append({"item": item, "disposition": "objected-parked"})
            else:
                plan.append({"item": item, "disposition": "objected-alternative",
                             "chosen": objection["label"]})
        elif item["qualification"]["state"] == "eligible":
            plan.append({"item": item, "disposition": "accepted-default",
                         "chosen": item["recommended_default"]["label"]})
        else:
            plan.append({"item": item, "disposition": None})
    return plan


# --------------------------------------------------------------------------- #
# Batch record composition and write (owner: § 批次记录契约)
# --------------------------------------------------------------------------- #
def knowledge_slug(title: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", title.strip().lower()).strip("-")[:60].strip("-")
    return slug or "entry"


def mint_batch_id(presentation: dict, reply_verbatim: str) -> str:
    scan_time = str(presentation.get("scan_time", ""))
    if not re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$", scan_time):
        raise Refusal("record-request", "malformed-presentation",
                      "scan_time is not an ISO-8601 UTC timepoint")
    stamp = scan_time.replace("-", "").replace(":", "")
    suffix = hashlib.sha256(
        (str(presentation.get("presentation_digest", "")) + "\n" + reply_verbatim)
        .encode("utf-8")).hexdigest()[:8]
    return f"B-{stamp}-{suffix}"


def render_decision_record(entry: dict, batch_id: str, record_rel: str,
                           created_at: str) -> list[str]:
    item = entry["item"]
    disposition = entry["disposition"]
    default = item["recommended_default"]
    lines = [f"### {entry['decision_id']} — {item['identity']['subject']}", ""]
    lines.append(f"- **decision_class**: {item['decision_class']}")
    context = item.get("context") or "（来源块未提供上下文）"
    lines.append(f"- **context**: {context}")
    lines.append(f"- **options**: {len(item['options'])}")
    for option in item["options"]:
        lines.append(f"  - label: {option['label']}")
        lines.append(f"    consequences: {option['consequences']}")
        lines.append(f"    reversibility: {option['reversibility']}")
        lines.append(f"    default: {option['default']}")
        lines.append(f"    evidence: {option['evidence']}")
        if option.get("path"):
            lines.append(f"    path: {option['path']}")
    forced = item["qualification"].get("forced")
    if forced:
        lines.append(f"  forced: {forced}")
    lines.append(f"- **chosen_option**: {entry['chosen']}")
    basis = default.get("basis") or "（来源块未提供理由）"
    if disposition == "accepted-default":
        reply_note = "用户未对本项提出异议，按建议默认值结案。"
    else:
        reply_note = f"用户改选「{entry['chosen']}」。"
    lines.append(f"- **rationale**: 建议依据：{basis}；{reply_note}")
    pointers = list(default.get("pointers", []))
    source_pointer = item["sources"][0]["carrier"] if item.get("sources") else ""
    evidence = [pointer for pointer in pointers if pointer]
    if source_pointer:
        evidence.append(source_pointer)
    evidence.append(record_rel)
    lines.append("- **evidence**: " + "; ".join(evidence))
    lines.append("- **actor**: user")
    lines.append(f"- **created_at**: {created_at}")
    lines.append("- **transmission_status**: not-transmitted")
    lines.append(f"- **batch_id**: {batch_id}")
    lines.append(f"- **batch_disposition**: {disposition}")
    lines.append(f"- **recommendation_grounding**: {default.get('status')}")
    lines.append("")
    return lines


def compose_batch_record(presentation: dict, reply: dict, plan: list[dict], batch_id: str,
                         record_rel: str, version: str, created_at: str) -> str:
    books = presentation["bookkeeping"]
    context = presentation["batch_context"]
    lines = [f"# 决策批次记录 {batch_id}", "", "## 批次头", ""]
    lines.append(f"- batch_id: {batch_id}")
    lines.append(f"- 扫描时点: {presentation['scan_time']}")
    lines.append(f"- 工具版本: decision-batch {version}")
    lines.append("- 来源与候选计数:")
    for source in books["sources"]:
        extra = ""
        if source.get("absent_reason"):
            extra += f"; 缺席原因: {source['absent_reason']}"
        if source.get("absent_roots"):
            extra += "; 缺席根: " + "、".join(source["absent_roots"])
        lines.append(f"  - {source['source_id']}: presence={source['presence']}; "
                     f"candidates={source['candidates']}{extra}")
    lines.append(f"- 完备性: candidates={books['candidates']} = "
                 f"presented_rows={books['presented_rows']} + "
                 f"duplicate_merged={books['duplicate_merged']} + "
                 f"named_exclusions={len(books['named_exclusions'])}; "
                 f"verdict={books['verdict']}")
    lines.append("- 授权: interactive")
    lines.append("- 用户应答原文:")
    lines.append("")
    for line in (reply["verbatim"].splitlines() or [""]):
        lines.append("> " + line if line else ">")
    lines.append("")
    lines.append("## 逐项行表")
    lines.append("")
    lines.append("| 主体 | 来源 | 资格 | 接地 | 建议默认 | 处置 | 决策 |")
    lines.append("|------|------|------|------|----------|------|------|")
    for entry in plan:
        item = entry["item"]
        subject = item["identity"]["subject"]
        locator = item["identity"].get("resource_locator")
        if locator:
            subject = f"{subject}（{locator}）"
        sources = "; ".join(f"{source['source_id']}@{source['carrier']}"
                            for source in item["sources"])
        qualification = item["qualification"]["state"]
        reasons = item["qualification"].get("reasons", [])
        if reasons:
            qualification += "(" + ",".join(reasons) + ")"
        default = item["recommended_default"]
        lines.append(f"| {subject} | {sources} | {qualification} | "
                     f"{default.get('status')} | {default.get('label') or '—'} | "
                     f"{entry['disposition'] or 'pending'} | {entry.get('decision_id') or '—'} |")
    lines.append("")
    lines.append("## 决策记录")
    lines.append("")
    settled = [entry for entry in plan if entry.get("decision_id")]
    if settled:
        for entry in settled:
            lines.extend(render_decision_record(entry, batch_id, record_rel, created_at))
    else:
        lines.append("本次批次没有已决项。")
        lines.append("")
    lines.append("## 收尾")
    lines.append("")
    pending = [entry for entry in plan if not entry["disposition"]]
    if pending:
        for entry in pending:
            item = entry["item"]
            reasons = ",".join(item["qualification"].get("reasons", [])) or "—"
            lines.append(f"- 保持待定：{item['identity']['subject']}"
                         f"（{item['qualification']['state']}: {reasons}）")
    else:
        lines.append("- 保持待定：无。")
    for entry in plan:
        if entry["disposition"] == "objected-parked":
            lines.append(f"- 暂缓：{entry['item']['identity']['subject']}"
                         "（不产生决策记录，下次批次重新呈现）")
    lines.append("- 来源更新：本批次写入批次记录；登记册与待决策项的更新由批次登记动作承接。")
    lines.append("")
    lines.append("## 批次上下文")
    lines.append("")
    for key in FLOOR_KEYS:
        lines.append(f"- {FLOOR_LABELS[key]}: {context[key]}")
    lines.append("")
    return "\n".join(lines)


def load_presentation(path: Path) -> dict:
    if not path.is_file():
        raise Refusal("record-request", "missing-presentation", str(path))
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, ValueError) as exc:
        raise Refusal("record-request", "malformed-presentation", f"{path}: {exc}")
    if payload.get("action") != "scan" or payload.get("result") != "presentation":
        raise Refusal("record-request", "malformed-presentation",
                      "the presentation payload is not a scan presentation")
    if payload.get("presentation_digest") != presentation_digest(payload):
        raise Refusal("record-request", "malformed-presentation",
                      "the presentation payload fails its own digest check")
    return payload


def write_batch_record(root: Path, record_rel: str, title: str, batch_id: str,
                       body: str) -> None:
    import subprocess
    memory_engine = Path(__file__).resolve().parent / "memory-utils.py"
    if not memory_engine.is_file():
        raise Refusal("record-request", "environment",
                      f"memory engine not found beside the batch engine: {memory_engine.name}")
    command = [sys.executable, str(memory_engine), "--action", "record",
               "--workspace-root", str(root), "--scope", "knowledge",
               "--source", "/speckit.decide", "--title", title,
               "--tags", f"decision-batch,{batch_id.lower()}",
               "--session-id", batch_id]
    try:
        completed = subprocess.run(command, input=body, capture_output=True, text=True)
    except OSError as exc:
        raise Refusal("record-request", "environment", f"memory engine failed to start: {exc}")
    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout or "").strip()[-500:]
        raise Refusal("record-request", "memory-engine-error", detail)
    target = root / record_rel
    if not target.is_file():
        raise Refusal("record-request", "write-verification",
                      f"the memory engine reported success but {record_rel} is absent")
def emit_refusal(action: str, refusal: Refusal, fmt: str) -> int:
    if fmt == "json":
        print(json.dumps({
            "action": action,
            "result": "refused",
            "refusals": [{"source_id": refusal.source_id, "reason": refusal.reason,
                          "detail": refusal.detail}],
        }, ensure_ascii=False, indent=2))
    else:
        print(f"拒绝：来源 {refusal.source_id} 不可用（{refusal.reason}）：{refusal.detail}",
              file=sys.stderr)
        print("本次没有呈现任何事项，也没有写入任何内容。")
    return EXIT_REFUSED


def action_scan(args: argparse.Namespace) -> int:
    root = Path(args.workspace_root).expanduser().resolve()
    try:
        payload = scan_workspace(root)
    except Refusal as refusal:
        return emit_refusal("scan", refusal, args.format)
    payload["scan_time"] = utc_now()
    payload["presentation_digest"] = presentation_digest(payload)
    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(render_text(payload), end="")
    return EXIT_OK


def action_record(args: argparse.Namespace) -> int:
    if not args.presentation:
        print("decision-batch.py: record requires --presentation PATH", file=sys.stderr)
        return EXIT_USAGE
    if not args.reply:
        print("decision-batch.py: record requires --reply PATH", file=sys.stderr)
        return EXIT_USAGE
    if args.authorization != "interactive":
        return emit_refusal("record", Refusal(
            "record-request", "authorization",
            "the caller must declare --authorization interactive; a missing level is treated "
            "as unattended and an unattended call cannot record acceptance — silence is not "
            "acceptance"), args.format)
    root = Path(args.workspace_root).expanduser().resolve()
    try:
        presentation = load_presentation(Path(args.presentation))
        reply = parse_reply_file(Path(args.reply))
        # The id is *derived* here (a pure string, no trace) so the create-only precondition
        # can be judged before the write surface; it is adopted as the batch id only after
        # every record precondition has passed (A-24).
        candidate_id = mint_batch_id(presentation, reply["verbatim"])
        title = f"{BATCH_TITLE_PREFIX}{candidate_id}"
        record_rel = f".specify/knowledge/{knowledge_slug(title)}.md"
        if (root / record_rel).exists():
            raise Refusal("record-request", "duplicate-batch",
                          f"{candidate_id}: {record_rel} already exists; a second record for "
                          "the same batch id is refused before the write surface runs")
        fresh = scan_workspace(root)
        diffs = drift_diff(presentation, fresh)
        if diffs:
            raise Refusal("record-request", "drift",
                          "the sources changed between presentation and record: "
                          + "; ".join(diffs[:10]))
        plan = plan_settlements(presentation, reply)
        batch_id = candidate_id
        settled = [entry for entry in plan if entry["disposition"] in
                   ("accepted-default", "objected-alternative")]
        for number, entry in enumerate(settled, start=1):
            entry["decision_id"] = f"D-{number:03d}"
        created_at = utc_now()
        version = _resolve_version(Path(__file__).resolve())
        body = compose_batch_record(presentation, reply, plan, batch_id, record_rel,
                                    version, created_at)
        write_batch_record(root, record_rel, title, batch_id, body)
    except Refusal as refusal:
        return emit_refusal("record", refusal, args.format)

    parked = [entry for entry in plan if entry["disposition"] == "objected-parked"]
    pending = [entry for entry in plan if not entry["disposition"]]
    decisions = [
        {"subject": entry["item"]["identity"]["subject"],
         "disposition": entry["disposition"],
         "decision_id": entry["decision_id"]}
        for entry in settled
    ]
    if args.format == "json":
        print(json.dumps({
            "action": "record",
            "result": "recorded",
            "batch_id": batch_id,
            "record_path": record_rel,
            "authorization": "interactive",
            "settled": len(settled),
            "parked": len(parked),
            "pending": len(pending),
            "decisions": decisions,
        }, ensure_ascii=False, indent=2))
    else:
        print(f"批次记录已写入：{record_rel}")
        print(f"批次编号：{batch_id}")
        print(f"已结案 {len(settled)} 项，暂缓 {len(parked)} 项，保持待定 {len(pending)} 项。")
        for decision in decisions:
            print(f"  {decision['decision_id']}  {decision['subject']}  {decision['disposition']}")
    return EXIT_OK


def action_replay(args: argparse.Namespace) -> int:
    print(
        "decision-batch.py: action 'replay' is declared but its core has not landed in "
        "this build; it lands with the replay package",
        file=sys.stderr,
    )
    return EXIT_USAGE


def build_parser() -> argparse.ArgumentParser:
    """The closed action set with the declared flag surface on every action."""
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument(
        "--workspace-root", default=".", metavar="PATH",
        help="the workspace the panel reads (default: the current directory)")
    common.add_argument(
        "--format", choices=("text", "json"), default="text",
        help="output format (default: text)")
    common.add_argument(
        "--presentation", metavar="PATH",
        help="the scan payload a reply is bound to (record)")
    common.add_argument(
        "--reply", metavar="PATH",
        help="the reply file carrying the user's verbatim text (record)")
    common.add_argument(
        "--authorization", choices=("interactive", "unattended"),
        help="caller-declared interaction authorization (record); "
             "missing is treated as unattended")
    common.add_argument(
        "--batch", metavar="PATH",
        help="the batch record to replay (replay)")

    parser = argparse.ArgumentParser(
        prog="decision-batch.py",
        description="Scan pending decision items, record one batch through the existing "
                    "carriers, and replay a recorded batch from its record alone.",
    )
    _sig_configure(
        parser,
        effects="scan and replay write nothing; record writes only through the named "
                "carriers (batch record, register rows/status cells, block resolution)",
        codes="0 success (including nothing-pending); 1 a documented refusal; "
              "2 usage or environment error",
    )
    sub = parser.add_subparsers(dest="action", required=True)
    sub.add_parser("scan", parents=[common],
                   help="read-only: scan the closed source roster and present one batch")
    sub.add_parser("record", parents=[common],
                   help="the only writer: validate the reply and write the batch record")
    sub.add_parser("replay", parents=[common],
                   help="read-only: reconstruct a recorded batch from its record")
    _sig_attach(parser)
    return parser


def run_action(args: argparse.Namespace) -> int:
    if args.action == "scan":
        return action_scan(args)
    if args.action == "record":
        return action_record(args)
    return action_replay(args)


def main(argv=None) -> int:
    _sig_guard(argv, declared=DECLARED_OPTIONS)
    args = build_parser().parse_args(argv if argv is not None else sys.argv[1:])
    return run_action(args)


if __name__ == "__main__":
    raise SystemExit(main())