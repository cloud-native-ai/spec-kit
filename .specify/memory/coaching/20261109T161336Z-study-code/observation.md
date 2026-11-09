# Observation — /study-code (core-concepts study of dsh-superagent-prototype)

**Run**: `20261109T161336Z-study-code`

## DispatchRecord

| Field | Value |
|---|---|
| trainee | raw `/study-code` · normalized `study-code` · kind `skill` · layer `external` (canonical `skills/external/study-code/SKILL.md`; installed mirror same skill) |
| workdir | `/storage/project/cloud-native-ai/spec-kit` |
| work (verbatim) | `分析 /storage/project/cloud-native-ai/dsh-superagent-prototype 中的核心概念` |
| mode | **fork** — external qodercli child through stage-runner (native in-process path banned under concurrency) |
| payload-ref | `.specify/.tmp/sdd-loop/forks/coach-study/prompt.txt` — **deleted with the driver scratch dir at ~00:16**; the dispatch text is reproducible from this run's brief and the fork session below |
| return carrier | qoder session store `/home/agent/.qoder/projects/-storage-project-cloud-native-ai-spec-kit/111683d8-20e5-4ebc-ad31-8949e7cf8a78.jsonl` (the fork's live-log evidence was deleted; the return was recovered from the session store, not invented) |
| runner status | process exited without a status file (fork dir deleted mid-run); completion judged by the recovered return + the independent artifact check (below) |

## Steps (self-report, recovered verbatim from the session store)

| # | Step | Evidence |
|---|---|---|
| 0 | Read `skills/external/study-code/SKILL.md` + 6 references | return §执行轨迹 |
| 1 | Target check; git `safe.directory` registration; `.git` corrupted (refs zeroed, index unreadable) diagnosed; default `$STUDY_DIR` mkdir failed → sanctioned `~/tmp/study-code/…`; empty shallow clone → object-store check → working-tree materialization (`cp -a`), commit `8c32a9dc` recorded; strip 301→120 files; `strip-manifest.md` | `~/tmp/study-code/dsh-superagent-prototype-study/strip-manifest.md`, `target-commit.txt` |
| 2–3 | Full scan, LOC, entry points; docs 000–007, README, prompts, locale; `outline-code.md` / `outline-docs.md` | same workspace |
| 4 | Core (11 files full), executor (2 full), app key 12, policy/deployment, prompt docs; `deep-study.md`; 4 `.puml` planning sources | same workspace |
| 5 | `docs/overview.md` (280 lines, index table + stable anchors + lookup guide); self-check: 42 evidence paths, 29/29 anchors, 21 index rows | `self-check-evidence.txt` |
| W | `run-determination` ×3 (c3 final) → `exec-quant` → `feedback-utils record` (c2 disposed) → temp cleanup (user-confirmed planned) | `.specify/memory/session/20261109T162154Z-…-c3.md`, exec-quant records, feedback entries |

## Primary artifact (independently checked)

`/home/agent/tmp/study-code/dsh-superagent-prototype-study/docs/overview.md` — 26,131 bytes, mtime 00:19;
workspace also holds `strip-manifest.md`, `outline-code.md`, `outline-docs.md`, `deep-study.md`,
`stripped/` (120 files), `figures/*.puml` ×4, `self-check-evidence.txt`.

## Target-repo integrity

The return states zero modifications (mtimes preserved at 11-09 21:07/20:13); only two reversible global git
config entries (`safe.directory`).

## Anomaly line (verbatim)

> **存在异常，按 fast-fail 分类处理**：① 目标仓库 `.git/refs/heads/main` 归零 + index 不可读（decision-free
> correction：不修原仓库，用对象库校验 + 工作树物化 + 记录 commit hash，已在 strip-manifest § Anomaly 披露）；
> ② 默认 `$STUDY_DIR` 父目录不可写（correction：改用受制裁的 `~/tmp` 根）；③ `src/sources/` 等 13+ 文件在快照中
> 缺失（事实，非可修：报告 §6 显式记录文档-代码冲突）；④ draw-diagram 渲染后端不可达（按 UML guide 降级：
> Mermaid 草图 + 保留 `.puml` + 可见降级注记）。

## Elapsed

~8 minutes of wall clock (00:14–00:22 local), self-report implied; under the 15-minute ceiling.
