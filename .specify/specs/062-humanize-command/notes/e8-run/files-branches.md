# T013 branch-leg execution log — 2026-10-19T09:44:14Z
workspace=/tmp/humanize-e8-files.uEVY (mktemp, deleted after run)

== B01 directory-as-input ==
decision: REJECT — path resolves to a directory, not a readable regular file (FR-019)
== B02 nonexistent-path ==
decision: REJECT — 路径不存在 (FR-019)
== B03 dual-source (--file + inline) ==
decision: REJECT — 一次只接受一个输入源 (FR-018)
== B04 no-input ==
decision: REJECT — 既无文件也无非空内联 (FR-018)
== B05 binary input (binary-sample.dat) ==
decision: REJECT — 非 UTF-8/二进制 (FR-019)
== B06 unsupported ext (unsupported-sample.pdf) ==
decision: REJECT — 扩展名不受支持，支持 .md/.markdown/.txt (FR-019)
== B07 empty file (empty.md, 0 bytes) ==
decision: REJECT — 文件为空 (FR-019)
== B08 frontmatter-only (frontmatter-only.md) ==
decision: REJECT — 仅有 frontmatter 无正文，视为空输入 (FR-019)
== B09 output ext conflict (md input --output out.txt) ==
decision: REJECT — 输出扩展名与输入格式族不一致；不创建、不修改目标 (FR-022)
== B10 same-path output (input-for-same-path.md --output input-for-same-path.md) ==
decision: REJECT — realpath 相同 = 原地覆盖 (FR-020/FR-021)
== B11 symlink alias (input-for-same-path.md --output symlink-to-input.md) ==
decision: REJECT — realpath 展开后相同 (FR-021)
== B12 hardlink alias (input-for-hardlink.md --output hardlink-alias.md) ==
decision: REJECT — 同一底层文件（inode 别名）(FR-021)
== B13 existing target without --force (existing-output.md) ==
decision: REJECT — 目标已存在且未获 --force；目标逐字节不变 (FR-021)
== B14 unwritable/missing parent (--output nodir/out.md) ==
decision: 写入失败报告——不声称成功、删除临时文件、不留部分输出、既有目标不变 (FR-021)
== B15 multi-file (两个路径) ==
decision: REJECT — 首版不支持批量 (Edge Cases)

== post-state assertions (mechanical) ==
branch-verdict: PASS=6 FAIL=2
== workspace repair: cp had dereferenced the alias fixtures; recreated as real symlink/hardlink ==
recheck-verdict: PASS=3 FAIL=0

== output-write legs ==
B16 new-path write: new-output.md created atomically (temp+rename), location reported to session
B17 --force overwrite: existing-output.md overwritten under explicit --force; pre-hash 38e2ba20..., post-hash 663d6d46...; temp file removed
plaintext closed-list on rewritten-plain-sample.txt: zero candidates (exit 0)
source-identity: all 7 content sources byte-identical after run (sha256sum -c OK)

== T013 corpus-wide diff verdicts (engine v2: punctuation-preserving blank) ==
16/16 pairs exit 0: s01(17) s02(16) s03(5) s04(27) s05(5) s06(0) s08(16) s09(35) s10(148) yaml(23) toml(17) plain(5) bom(7) upper-case(23) threat-file(12) protected-content(31)

== s10 segmentation record ==
estimate basis: diff_protected.py --stats cjk=2097 latin=30 → est ≈ 2097 + 30×1.3 ≈ 2136 tokens (tests/fixtures/humanize/README.md § 窗口口径)
trigger: 2136 > 4k reference host × 50% = 2000 → segmentation fires; on 12k/128k hosts no split (single pass)
segments: 2 (第一章..第五章 | 第六章..第十章), all at chapter boundaries
chapters processed: 10/10, none skipped; reassembled single document; no duplicated/omitted chapter
chapter correspondence: 1:1 (report background/capacity/quality/storage-cost/availability/security/feedback/improvements/Q4-plan/appendix), appendix kept near-verbatim (already compact)
