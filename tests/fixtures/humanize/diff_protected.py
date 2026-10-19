#!/usr/bin/env python3
"""diff_protected.py — deterministic protected-content & invariant differ for the
062 humanize E8 evaluation corpus (SC-002 normalization criteria).

Owner of the **protected token list** construction (rubric.md § 四 cites this file
as the owner; do not maintain a second copy of the list): the list is built
deterministically from the INPUT text as

    FR-008 protected set        quotes, fenced/inline code, commands, file paths,
                                URLs, identifiers, formulas, template placeholders
                                ({{...}}, ${...}), YAML/TOML frontmatter, table data
      ∪ template placeholders   {{...}} / ${...} shapes
      ∪ code identifiers        backticked tokens + snake/camel/kebab-case tokens
      ∪ URLs & version numbers  http(s) links, x.y[.z...] version literals

Comparison criteria (SC-002, normalization — never unit conversion):
  - numbers/units/dates: strip thousands separators, unify whitespace,
    same-calendar-day dates are equivalent (2026-09-30 ≡ 2026年9月30日 ≡ 2026/9/30);
    NO unit conversion (4Gi ≠ 4096Mi, 0.5h ≠ 30min)
  - percentages, version numbers, identifiers, URLs, code tokens: verbatim
  - new sentences: every sentence flagged by this script as a "new candidate"
    must carry an entailment annotation (--annotations); an unannotated
    candidate or a fabricated number/date exits 1.

Usage:
  python3 diff_protected.py --input IN.md --output OUT.md [--annotations ann.json]
  python3 diff_protected.py --stats IN.md            # main-language counters (FR-013)
  python3 diff_protected.py --plaintext-check OUT.md # FR-022 closed-list candidates (informational)
  python3 diff_protected.py --selftest               # runs selftest/ pairs

Exit codes: 0 = every protected/invariant item present unchanged AND all new-sentence
candidates annotated (or none); 1 = any missing/changed item, fabricated number,
or unannotated new-sentence candidate; 2 = usage error. Stdlib only; no LLM, no
network (C-8).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

# --- protected-shape regexes -------------------------------------------------
RE_FENCE = re.compile(r"```.*?```", re.S)
RE_INLINE_CODE = re.compile(r"`([^`\n]+)`")
RE_PLACEHOLDER = re.compile(r"\{\{[^{}\n]+\}\}|\$\{[^{}\n]+\}")
RE_URL = re.compile(r"https?://[^\s)>\]\"'，。；」』]+")
RE_VERSION = re.compile(r"(?<![\w.])v?\d+(?:\.\d+){1,3}(?:-[0-9A-Za-z.-]+)?(?![\w.])")
RE_PATH = re.compile(r"(?<![\w])/(?:[A-Za-z0-9._-]+/)+[A-Za-z0-9._-]+|(?<![\w./\\])[A-Za-z0-9_-]+(?:/[A-Za-z0-9_.-]+)+\.[A-Za-z0-9]{1,5}")
RE_IDENT = re.compile(r"(?<![\w])[A-Za-z][A-Za-z0-9]*(?:[_-][A-Za-z0-9]+)+(?![\w])")
RE_QUOTE = re.compile(r"“([^”\n]{4,})”|\"([^\"\n]{4,})\"|「([^」\n]{6,})」")
RE_TABLE_ROW = re.compile(r"^\s*\|.*\|\s*$", re.M)
RE_FRONTMATTER = re.compile(r"\A(?:---\n.*?\n---|\+\+\+\n.*?\n\+\+\+)\s*\n", re.S)

# --- invariant numeric shapes ------------------------------------------------
RE_DATE = re.compile(r"(?<![\d])(\d{4})[./年](\d{1,2})[./月](\d{1,2})日?(?![\d])")
RE_NUMBER_UNIT = re.compile(
    r"(?<![\d.,])(\d{1,3}(?:,\d{3})+|\d+(?:\.\d+)?)(\s*)(%"
    r"|ms|[smhd](?![a-zA-Z])|TB|GB|MB|Mi|Gi|KB"
    r"|万元|个百分点|百分点|小时|分钟|秒|万人|万次|万字|万篇|万元|万元"
    r"|篇|个|起|条|笔|人|名|家|批次?|步|折)"
    r"?"
)
RE_SENTENCE = re.compile(r"[^。！？!?；;\n]+[。！？!?；;]?")

UNIT_EQUIV = {  # same-unit aliasing only; NEVER cross-unit conversion (SC-002)
    "s": "s", "秒": "秒",
}

CJK_RANGES = (("\u4e00", "\u9fff"), ("\u3400", "\u4dbf"), ("\uf900", "\ufaff"))


def is_cjk(ch: str) -> bool:
    return any(lo <= ch <= hi for lo, hi in CJK_RANGES)


def read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8-sig")  # UTF-8 BOM tolerated, not counted (FR-019)


def norm_ws(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def norm_num(s: str) -> str:
    """Strip thousands separators; canonical dot decimal."""
    return s.replace(",", "") if "," in s else s


def date_key(y: str, m: str, d: str):
    return (int(y), int(m), int(d))  # same calendar day equivalence


def extract_protected(text: str) -> list[dict]:
    """Build the protected token list from the input (see module docstring)."""
    items: list[dict] = []

    def add(kind: str, value: str, normalized: str | None = None):
        items.append({"kind": kind, "value": value, "normalized": normalized if normalized is not None else value})

    m = RE_FRONTMATTER.search(text)
    if m:
        add("frontmatter", m.group(0), norm_ws(m.group(0)))
    for m in RE_FENCE.finditer(text):
        add("code-block", m.group(0), norm_ws(m.group(0)))
    for m in RE_INLINE_CODE.finditer(text):
        add("inline-code", m.group(0), norm_ws(m.group(0)))
    for m in RE_PLACEHOLDER.finditer(text):
        add("placeholder", m.group(0))
    for m in RE_URL.finditer(text):
        add("url", m.group(0))
    for m in RE_VERSION.finditer(text):
        if "`" not in m.group(0):
            add("version", m.group(0))
    for m in RE_PATH.finditer(text):
        add("path", m.group(0))
    for m in RE_IDENT.finditer(text):
        add("identifier", m.group(0))
    for m in RE_QUOTE.finditer(text):
        q = next(g for g in m.groups() if g)
        add("quote", m.group(0), norm_ws(m.group(0)))
    for m in RE_TABLE_ROW.finditer(text):
        add("table-row", m.group(0), norm_ws(m.group(0).replace(" ", "")))
    return items


def extract_invariant_numbers(text: str) -> Counter:
    """Multiset of normalized (value, unit|None) + calendar-date keys."""
    numbers: Counter = Counter()
    dates: Counter = Counter()
    # dates first (avoid double-counting their digits)
    consumed = [(m.start(), m.end()) for m in RE_DATE.finditer(text)]

    def in_consumed(i: int) -> bool:
        return any(a <= i < b for a, b in consumed)

    for m in RE_DATE.finditer(text):
        dates[date_key(m.group(1), m.group(2), m.group(3))] += 1
    for m in RE_NUMBER_UNIT.finditer(text):
        if in_consumed(m.start(1)):
            continue
        val = norm_num(m.group(1))
        unit = m.group(3) or None
        numbers[(val, unit)] += 1
    return numbers + dates  # type: ignore[operator]


def sentences(text: str) -> list[str]:
    return [norm_ws(s) for s in RE_SENTENCE.findall(text) if norm_ws(s)]


def content_tokens(sentence: str) -> list[str]:
    return [m.group(0).lower() for m in re.finditer(r"[A-Za-z][A-Za-z0-9]*|[\u4e00-\u9fff]", sentence)]


def protected_spans(text: str) -> list[tuple[int, int]]:
    spans = []
    for rx in (RE_FRONTMATTER, RE_FENCE, RE_INLINE_CODE, RE_URL, RE_PLACEHOLDER, RE_TABLE_ROW):
        spans.extend((m.start(), m.end()) for m in rx.finditer(text))
    return spans


def strip_protected(text: str) -> str:
    spans = protected_spans(text)
    chars = list(text)
    for a, b in spans:
        for i in range(a, min(b, len(chars))):
            if chars[i] != "\n":  # newline-preserving: keeps line/sentence segmentation
                chars[i] = " "
    stripped = "".join(chars)
    # length-preserving number blank-out (keeps raw/stripped sentence index alignment)
    stripped = re.sub(r"\d+(?:\.\d+)*", lambda m: " " * len(m.group(0)), stripped)
    return stripped


def lang_stats(text: str) -> dict:
    body = strip_protected(text)
    cjk = sum(1 for ch in body if is_cjk(ch))
    latin_words = len(re.findall(r"[A-Za-z]+", body))
    return {"cjk_chars": cjk, "latin_words": latin_words}


def find_new_sentence_candidates(inp: str, out: str) -> list[str]:
    """Heuristic, deterministic: flag output sentences whose non-protected content
    tokens have <50% coverage by the input token set. Reviewers annotate each.
    Protected spans are blanked (length-preserving) BEFORE sentence splitting; because
    blanking only swaps in spaces, RE_SENTENCE segments raw and blanked text identically,
    so the two sentence lists pair 1:1 by index and the display form stays raw."""
    in_tokens = set()
    for s in RE_SENTENCE.findall(strip_protected(inp)):
        in_tokens.update(content_tokens(s))
    blanked = strip_protected(out)
    raw_parts = RE_SENTENCE.findall(out)
    blank_parts = RE_SENTENCE.findall(blanked)
    if len(raw_parts) != len(blank_parts):  # never expected: blanking is length-preserving
        raise AssertionError(
            f"sentence segmentation diverged raw={len(raw_parts)} blanked={len(blank_parts)}"
        )
    flagged = []
    protected_idents = {p.lower() for p in re.findall(r"[A-Za-z][A-Za-z0-9]*(?:[_-][A-Za-z0-9]+)+", inp)}
    for raw, blank in zip(raw_parts, blank_parts):
        s = norm_ws(blank)
        if not s:
            continue  # fully-protected sentence (frontmatter line, fence, table row)
        toks = [t for t in content_tokens(s) if t not in protected_idents]
        if len(toks) < 4:
            continue
        cov = sum(1 for t in toks if t in in_tokens) / len(toks)
        if cov < 0.5:
            flagged.append(norm_ws(raw))
    return flagged


def compare(input_path: Path, output_path: Path, annotations_path: Path | None) -> tuple[int, list[str]]:
    inp, out = read_text(input_path), read_text(output_path)
    lines: list[str] = []
    failures = 0

    def fail(msg: str):
        nonlocal failures
        failures += 1
        lines.append(f"FAIL  {msg}")

    def ok(msg: str):
        lines.append(f"OK    {msg}")

    # 1) protected items: verbatim / normalized presence
    for item in extract_protected(inp):
        val, norm = item["value"], item["normalized"]
        present = val in out or norm in out or norm_ws(val) in out
        if present:
            ok(f"protected[{item['kind']}] present: {val[:60]!r}")
        else:
            fail(f"protected[{item['kind']}] MISSING/CHANGED: {val[:60]!r}")

    # 2) invariant numbers/units/dates: normalized multiset equality
    in_nums, out_nums = extract_invariant_numbers(inp), extract_invariant_numbers(out)
    for key, cnt in in_nums.items():
        if out_nums.get(key, 0) < cnt:
            fail(f"invariant number/unit/date {key} ×{cnt} not preserved (output has {out_nums.get(key, 0)})")
        else:
            ok(f"invariant {key} ×{cnt} preserved")
    for key, cnt in out_nums.items():
        if cnt > in_nums.get(key, 0):
            fail(f"FABRICATED number/unit/date {key} ×{cnt} not in input")

    # 3) new-sentence candidates → entailment annotations
    candidates = find_new_sentence_candidates(inp, out)
    ann: list[dict] = []
    if annotations_path:
        ann = json.loads(annotations_path.read_text(encoding="utf-8"))
    ann_by_prefix = {norm_ws(a["sentence"])[:20]: a.get("basis", "").strip() for a in ann}
    for cand in candidates:
        basis = next((b for p, b in ann_by_prefix.items() if norm_ws(cand).startswith(p)), "")
        if basis:
            ok(f"new-sentence annotated (input-entailed): {cand[:40]!r} ← {basis[:60]!r}")
        else:
            fail(f"new-sentence candidate lacks entailment annotation: {cand[:60]!r}")
    if candidates and not annotations_path:
        lines.append(f"NOTE  {len(candidates)} new-sentence candidate(s) require --annotations (SC-002); without them the verdict is fail.")
        for cand in candidates:
            lines.append(f"CAND {cand}")
    return (1 if failures else 0), lines


def plaintext_check(text: str) -> list[str]:
    """FR-022 closed-list CANDIDATE lines (informational; human confirms context)."""
    checks = [
        ("行首标题 #", re.compile(r"(?m)^#{1,6}\s")),
        ("成对强调 **/__", re.compile(r"\*\*[^*]+\*\*|__[^_]+__")),
        ("行首列表 - ", re.compile(r"(?m)^\s*-\s")),
        ("行首列表 1. ", re.compile(r"(?m)^\s*\d+\.\s")),
        ("代码围栏 ```", re.compile(r"```")),
        ("行内反引号 `", re.compile(r"`[^`\n]+`")),
        ("链接 []()", re.compile(r"\[[^\]\n]+\]\([^)\n]+\)")),
        ("表格 | 行", re.compile(r"(?m)^\s*\|.*\|\s*$")),
        ("行首引用 >", re.compile(r"(?m)^\s*>\s")),
    ]
    found = []
    for name, rx in checks:
        for m in rx.finditer(text):
            line_no = text[: m.start()].count("\n") + 1
            found.append(f"{name} @ line {line_no}: {m.group(0)[:40]!r}")
    return found


def selftest() -> int:
    base = Path(__file__).resolve().parent / "selftest"
    code_clean, out_clean = compare(base / "clean-input.md", base / "clean-output.md", base / "clean-annotations.json")
    code_mut, out_mut = compare(base / "mutated-input.md", base / "mutated-output.md", None)
    print("== selftest clean pair (expect exit 0) ==")
    print("\n".join(out_clean[-6:]))
    print(f"clean pair exit = {code_clean} (expect 0)")
    print("== selftest mutated pair (expect exit 1) ==")
    print("\n".join(l for l in out_mut if l.startswith("FAIL")) or "(no FAIL lines!)")
    print(f"mutated pair exit = {code_mut} (expect 1)")
    good = code_clean == 0 and code_mut == 1
    print("SELFTEST", "PASS" if good else "FAIL")
    return 0 if good else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--input", type=Path)
    ap.add_argument("--output", type=Path)
    ap.add_argument("--annotations", type=Path)
    ap.add_argument("--stats", type=Path, help="print FR-013 main-language counters for a text")
    ap.add_argument("--plaintext-check", type=Path, help="list FR-022 closed-list candidate lines (informational)")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return selftest()
    if args.stats:
        s = lang_stats(read_text(args.stats))
        print(f"stats: cjk_chars={s['cjk_chars']} latin_words={s['latin_words']}")
        return 0
    if args.plaintext_check:
        found = plaintext_check(read_text(args.plaintext_check))
        if found:
            print("plaintext closed-list candidates (human confirms context per rubric § 九):")
            print("\n".join(found))
        else:
            print("plaintext closed-list: no candidates found")
        return 0
    if not (args.input and args.output):
        ap.error("--input and --output are required (or --selftest / --stats / --plaintext-check)")
    code, lines = compare(args.input, args.output, args.annotations)
    print("\n".join(lines))
    print(f"RESULT: {'PASS' if code == 0 else 'FAIL'} ({len(lines)} item lines)")
    return code


if __name__ == "__main__":
    sys.exit(main())
