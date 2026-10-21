# Recheck 2026-10-22 — implement checklist gate (snapshot-contract items)

**Round**: implement-feature Step 2 (implement dispatch, run sdd-loop-065a-20261022T1723Z).
**Answers**: `checklists/snapshot-contract.md` (37 items). Per the recheck protocol this file
is append-only; the original checklist's unchecked rows stay as history. Each answered entry
quotes the requirement line that answers it (verbatim, with anchor). The 5 `[Gap]` items carry
inline dispositions in the checklist itself, verified by `test-evidence/analyze-findings-r3.md`
(§ Checklist accountability, GREEN); their rows below record the disposition anchors.
**Gate outcome**: all 37 answered → no genuinely unresolved items → gate passes without waiver.

## Answers

- CHK001 — answered YES. `requirements.md` SA-4: "065a 的所有执行路径 MUST NOT 写状态脊、写四件套、移动/删除证据、提交或杀进程；显式 `--out` 持久化是唯一例外，且不得写入状态目录或工作树"（closed list; `contracts/loop-state-cli.md` C-10 enumerates the same forbidden effects + exit 2 boundary）.
- CHK002 — answered YES. Observable audit is defined by tasks T003 ("快照只读 mtime 审计" contract test) and T029 (mtime audit + `git diff --stat` scope proof); `contracts/loop-state-cli.md` C-10: "`--out` 写入 MUST 为同目录临时文件 + 原子替换…MUST NOT 留下任何文件".
- CHK003 — answered YES. `requirements.md` FR-001: "快照动作 MUST NOT 写文件、改状态、杀进程或修改工作树（显式 `--out` 持久化除外）"; `contracts/loop-state-cli.md` C-10 specifies realpath-then-compare, symlink/relative cases, atomic write, same-envelope content, exit 2.
- CHK004 — answered YES. `contracts/loop-state-cli.md` C-6 table: "必需输入（required input）…MUST 以退出码 `2` 拒绝" vs "证据源（evidence source）…MUST 显式记为 `missing`（值用 `null`），并仍以退出码 `0` 完成求值"; FR-002 carries the same split.
- CHK005 — answered YES. `requirements.md` FR-003 slice clarification: "`missing` = 期望的证据源/路径不存在或不可读，`na` = 该信号对本阶段/本次尝试不适用"; `contracts/snapshot-envelope.md` C-21 reproduces the four-row table incl. the never-dispatched row.
- CHK006 — answered YES. FR-003 clarification: "`unknown` 是值级标记，用于证据源存在但值无法判定…缺失值用 `null`，MUST NOT 用零值、空串或 `ok` 代替"; C-22: "`unknown` 是值级标记（`value_state`），MUST NOT 被塞进 `status` 枚举".
- CHK007 — answered YES. FR-005 slice clarification defines the full three-state mapping ("取得判定：`present=true`、`status=present`、`value_state=known`…不可用…`reason=unavailable`…无活动 watch target：`present=false`、`status=na`"); C-25 embeds the same table plus `attribution`/`detail`.
- CHK008 — answered YES (conflict fixed by analyze R1 C-01, verified GREEN in R3). FR-004: "本表的唯一 owner 是本条（parent #FR-004）；`references/state-awareness.md §Derived Mapping` 与 `loop-state.py` 的映射 MUST 仅为该表的镜像，并由契约测试验证逐项一致；除本条外任何位置 MUST NOT 声称拥有该表"; FR-043 now reads "派生映射表（FR-004）不在本条 owner 文档的拥有范围内".
- CHK009 — answered YES. `requirements.md` A-18: "状态枚举扩展为 `running / retrying / stalled / reentry-required / done`"; FR-004 rule (1): "状态脊 `spine_state=stalled` → `STALLED`，[[STR-004]] → `REENTRY_REQUIRED`"; `running`/`retrying`/`done` participate only through rules (2)–(7) evidence, and C-23 declares legacy degrade without guessing. The spine file semantics' owner stays 058 (Key Entities: "State Spine（状态脊，既有）…本切片增加读取与一致性报告，不改变其状态词表与写入时点").
- CHK010 — answered YES. `contracts/interruption-and-action.md` C-40 closes the evidence set: "无哨兵…无退出记录、状态脊非 `stalled`/`reentry-required`"; FR-004 rule (5) consumes the same terminal-evidence set ("无终态").
- CHK011 — answered YES. FR-004 orders the ladder so `ANOMALY` precedes `FAILED` ("若（退出记录存在或进程已死）且日志最后非空行以 `ANOMALY:` 开头 → `ANOMALY`，否则退出记录 `exit≠0` → `FAILED`") and pins the sentinel as last-line ("更早出现的哨兵字样…不构成完成证据"); T007 requires the live-process + trailing-`ANOMALY:` case to not judge DONE.
- CHK012 — answered YES. FR-007: "「哨兵在而产物缺」MUST 判为伪完成（`INCOMPLETE` 语义）"; C-42: "`false_completion` 是同一判据的另一侧…二者互斥，MUST NOT 同时为真" — literal `loop_state` may remain FAILED/DEAD per FR-004 while `false_completion` flags the semantics.
- CHK013 — answered YES. C-32: "相同输入两次运行，除 `evaluated_at` 外所有字段 MUST 逐字相等。输出 MUST NOT 包含 `age_seconds`、剩余时间或其他随调用时刻变化的派生数值"; R-11 forbids recomputing probe freshness locally; deterministic fixtures pin `--watch-script` to a missing path (quickstart §2 premises).
- CHK014 — answered YES. C-44: "watcher 调用失败 MUST NOT 映射为该形态（那是 `watch_verdict.reason=unavailable`，走 derived）"; remote-unreachable fires only from probe shape (b) — disjoint by construction.
- CHK015 — answered YES (fixed by analyze R1 I-05, verified GREEN in R3). C-23/C-39: "一致性字段 MUST 为嵌套 `spine.consistent`；MUST NOT 输出顶层 `spine_consistent` 别名"; parent requirements now use the nested form (analyze R3 § Prior-finding delta, I-05 FIXED).
- CHK016 — answered YES. FR-009 slice clarification (in the requirement body): "切片澄清（2026-10-21）：065a 的只读检测覆盖六类形态…`heartbeat-stalled` 与 `lifecycle-spine-violation` 的形态判定，以及上述六类形态的细化谓词，由 `065b-interruption-lifecycle` 承接".
- CHK017 — answered YES (operationalized). C-33: "065a MUST 只产出 `unwatched`、…、`remote-unreachable` 六类" — a closed production set that can never emit the two 065b forms; FR-009 reserves their "词表、字段与 `missing`/`unknown` 语义".
- CHK018 — answered YES. FR-012 slice clarification: "本条的“全部中断形态”按切片累计解释——065a 的 `--self-test` 覆盖六类已实现形态…`heartbeat-stalled`、`lifecycle-spine-violation` 由 065b 追加，并发锁与拒绝路径由 065c 追加"; C-18 folds the not-implemented refusal envelope into 065a's self-test scope.
- CHK019 — answered YES. C-2: "`owner` 字段逐动作钉死：`check-spine` → `owner=065b`；`recover` → `owner=065c`。两个动作的行为实现归属与 `notes/decomposition-gate.md` 一致"; feature-ref §2 assigns `check-spine` to 065b — one owner per action, consistent.
- CHK020 — answered YES. T026 executes BOTH drills in-slice ("移除 `unwatched` 检测分支…至少一条转红；然后…移除 `IA-16`（`C-48`）的 salvage 完整记录门…至少一条 salvage 用例转红"); the FR-046 mapping row's deferral ("「旧信号隔离」「salvage 门」的变异演练由 065c 承接") covers 065c's write-side behavior; an evaluation-side drill here is a superset, not a contradiction.
- CHK021 — `[Gap]` dispositioned inline: "covered-by requirements.md SA-1". SA-1: "把旧信号列入 `stale_signals[]` 与 `interruptions[]`，从本次 `loop_state`/产物/动作求值中排除（IA-11），不因单纯 stale 改变候选动作…执行…归 065c".
- CHK022 — answered YES. C-40 defines `unwatched` by watchbeat evidence ("watchbeat 标记缺失，或标记年龄 > 其自身 `window=` + deadline-grace") independent of verdict source, and forbids it when a last-line sentinel exists; watcher-unavailable is a different object (C-15: `watch_verdict.reason=unavailable`).
- CHK023 — answered YES. FR-002 slice clarification (requirement body): "`--probe <file>` 接受两类 JSON 形状——(a) 与快照同信封的只读快照（含 `watch_verdict` 与 `evidence`…）或 (b) 最小可达性对象 `{schema_version:1, reachable:false, reason}`。未知字段 MUST 被忽略".
- CHK024 — answered YES. FR-002: "显式提供时以它为准并在输出标注 `evidence_source=probe`" governs evidence precedence; the same FR pins exclusion: "`--probe` 与 `--spine`/…/`--watch-script` 互斥：同时提供 MUST 以退出码 `2` 拒绝，且 MUST NOT 读取任何本地证据" — precedence and co-provision are different situations, no conflict; C-12/C-13 pin the rejections.
- CHK025 — answered YES. C-11 shape (a): "probe 自带 freshness 视为权威"; R-09: "probe 内部的 `fresh` 等由证据所在主机计算，消费侧不重算时间判定" — same probe input replays identically (SC-002 preserved).
- CHK026 — answered YES. A-14 (as clarified): "满足时输出 `UNKNOWN` + `reason=not-dispatched`、动作 `none`"; C-35 states it as iff-normative and R-07 places both pre-shorts before FR-004 rule (6) ("否则规则 (6) 会把从未派发的线误判为 `NO_SIGNAL`").
- CHK027 — answered YES. C-35: "`--stage` 是调用方意图，不是派发证据"; the predicate counts only "Registry 条目缺失或条目没有 `stage`" — an explicit `--stage` is not dispatch evidence (A-14 same sentence).
- CHK028 — answered YES. C-35: "命中时输出…四件套、watchbeat、artifacts、commits MUST 记 `status=na`、`value_state=na`"; a dispatched line with absent files falls under Q2's `missing` row (C-6/C-21).
- CHK029 — `[Gap]` dispositioned inline: "covered-by contracts/loop-state-cli.md C-7 and contracts/interruption-and-action.md C-35/C-36".
- CHK030 — `[Gap]` dispositioned inline: "covered-by tasks.md §Requirement Coverage Map + coverage-baseline.txt (accountant: claimed clauses 60, FR 25/25, baseline 495)".
- CHK031 — answered YES. C-52: "`plan` 的五个必需产物与 `research.md` 合起来 MUST 覆盖 `efficiency-model.md` §3.1 的 plan-owned 集合。`research.md` 在 plan 模板中是条件产物，故列 owned-only".
- CHK032 — `[Gap]` dispositioned inline: "covered-by contracts/stage-artifact-map.md C-54 (checklist requires a file added/modified since stage_base_commit; pre-existing files do not count)".
- CHK033 — `[Gap]` dispositioned inline: "covered-by contracts/interruption-and-action.md C-46 rows 5/6 and contracts/stage-artifact-map.md C-57".
- CHK034 — answered YES. FR-010 Parent FR Mapping row (in requirements): "标记写入属驱动者行为，快照只读消费"; plan §Slice Landing Notes carries the same split for 065b.
- CHK035 — answered YES. C-2 pins exactly one owner per action (`065b` / `065c`), matching feature-ref §2 and the decomposition-gate allocation.
- CHK036 — answered YES (resolved by the 2026-10-21 analyze amendment, verified in R3). requirements §Related Feature (current text): "不新建 Feature ID、不新增注册行；Draft→Planned 的状态推进由 plan 阶段按 Feature Integration 拥有"; plan §Disclosed Deviations 1 records the rewrite; feature-ref §1/§6 align.
- CHK037 — answered YES. SC-005 Measurement Sources: "`sync-mirrors.py --check…`、`docs/reference/skills/sdd-loop-driver.md` 存在性与内容断言、依赖清单比对"; T029 executes the dependency/scope audit.

## Verification note

All quoted lines re-read from the live tree during this gate pass (2026-10-22). The checklist's
`[Gap]`-subset accountability statement ("unchecked + unraised + undispositioned = 0") is
confirmed by `test-evidence/analyze-findings-r3.md` § Checklist accountability (GREEN verdict).
