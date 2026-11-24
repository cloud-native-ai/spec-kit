# ADR-0004: Two-track strategy — spec-kit stable, ai-harness experimental

- **Status:** Accepted
- **Date:** 2026-11-24
- **Deciders:** Qiming Liu (John)
**Readers**: maintainers and operators deciding which track owns a change or a client project.
**Reading scenario**: when a spec-kit or ai-harness change needs a recorded home track, or when a client asks whether and when it will switch frameworks.

## Context

ai-harness and spec-kit are two implementations of the same SDD model with no shared git ancestry. ai-harness began on 2026-11-23 with `4afad22 chore: initialize independent ai-harness history`; it has 10 commits and has since added its own specs 069–082 (team-view parity, parent identity, subagent context, user-facing output envelope). spec-kit has 3074 commits and continues through spec 104 and the user-facing output mechanism.

The 2026-11-24 comparison found:

- **Structural equivalence**: both at 0.0.22; 32 command templates, 59 skill directories, 20 agents, 117 shared files; the same build/init/migrate/tool-surface shapes.
- **Semantic divergence**: ai-harness uses a capability-domain, 1:N feature registry (8 columns, `Relocated`, `Active Features`); 75 of 92 shared feature IDs carry different titles. Team view is inline in ai-harness but a dedicated `view-team` skill plus `team-view.py` in spec-kit. spec-kit 104's child-label/multi-child carriers are absent in ai-harness. TODO markers, environment variables, line-registry namespaces, and runtime roots differ (`SPECKIT TODO`/`SPECIFY_*`/`spec-kit/lines`/`.specify` vs `AI-HARNESS TODO`/`AI_HARNESS_*`/`ai-harness/lines`/`.ah`).
- **No ingest path**: ai-harness deliberately has no `.specify` reader (`RUNTIME_DIR_NAMES_ALL = (".ah",)`; `migrate --migrate-dir` has no legacy source). The existing switch engine is a repository renamer, not a project-data migrator; its map protects history trees and, when loaded, deletes `.specify` paths rather than translating them.
- **Shipped defects in ai-harness**: 43 broken `.ah/specs/.ah/...` asset paths, a corrupted sentence in `anchor-definitions.md`, a stale `.ah/instructions.md` backup, and a self-referential legacy environment reader.
- **Fleet state**: 27 `.specify` containers exist (26 clients plus spec-kit itself); ai-harness has no `.ah` outside its own repository. The installed environment had only ai-harness-cli; `specify` was an ai-harness alias shim.

The decider's direction is to keep both tracks alive: spec-kit remains the stable line for existing projects, while ai-harness is free to evolve more aggressively. Switching is not a current objective.

## Decision

1. **Two tracks with different change budgets.**
   - **spec-kit (stable)**: long-lived; stability, bug fixes, regression coverage, and compatibility first. No cross-framework migration work and no parity obligation toward ai-harness. Breaking changes require a separate accepted decision.
   - **ai-harness (experimental)**: independent evolution; may diverge, may ship features spec-kit does not have, and is not required to mirror spec-kit. Any spec-kit fix reaches ai-harness only by a deliberate port.
2. **No client switching or migration now.** The 26 clients remain on `.specify`. The existing switch engine is a repository-renaming tool and MUST NOT be applied to client projects as a migration. No project-migrator build is authorized by this ADR.
3. **Environment alignment.** The stable line pins `specify-cli 0.0.22` from the spec-kit repository; `specify` resolves to that CLI (user-level install, commit `fed513bcc`). The `ai-harness` CLI remains a separate installation for the experimental track. Both CLIs coexist; `origin` remains the read-only upstream and is not a mirror.
4. **Revisit triggers (closed list).** The migration question reopens only when one of the following is recorded:
   - the decider explicitly reopens it;
   - ai-harness passes a written readiness gate: no shipped path corruption or stale-backup defects; a project-level `.specify` ingestion/migration tool with dry-run, archive-not-delete, per-project receipts, and rollback; parity on client-critical behaviors (team view, `agents run` multi-child, feature registry semantics); and test parity on the SDD engines the clients use;
   - the stable line's cross-track porting burden exceeds 20% of its change budget for two consecutive releases, or a client requires an ai-harness-only capability with no spec-kit equivalent.
5. **If reopened**, a migration plan is mandatory before any project write: inventory, dry-run, backup, per-project receipts, verification, rollback rehearsal, and a feature-ID redirect policy.

## Alternatives

- **Switch all projects now** — rejected: no `.specify` ingest path; ai-harness carries shipped path/text defects; feature-ID semantics diverge; 26 clients would face data left behind, two command palettes, and two registries.
- **Keep strict parity / merge the forks** — rejected: independent histories and different release goals; permanent sync tax would constrain the experimental track and slow the stable track.
- **Freeze ai-harness** — rejected: loses the deliberately aggressive lane the decider wants to keep.
- **tension_id:** `T-001` — the record below is the carrier; no feature plan exists for this portfolio decision.

### T-001 — 两条轨道并行，而不是现在就统一到 ai-harness

- **decision**: 保持 spec-kit 稳定线与 ai-harness 实验线并行，暂不做客户端迁移。
- **antithesis**: 在迁移器与缺陷修复就绪后全量切换到 ai-harness；当单一框架的长期维护成本超过迁移风险、且客户端已具备可回滚的迁移路径时，它更优——一套技能、一套命名空间、一条演进线。
- **binding_constraints**:
  - pole_a: 26 个客户端的现有 `.specify` 数据、命令与工作流必须零丢失、零不可用。
  - pole_b: 实验线必须保持快速演进，不能被稳定线的兼容包袱拖慢。
- **discriminating_evidence**: 对一个低风险客户端执行一次 dry-run + 试点迁移，核对每一条回执、specs/features/memory/state 的逐项守恒、`/ah.status` 与 `/ah.team view` 可用性；结果二值：全部回执与验证通过（可扩大） / 任一数据丢失或验证失败（不扩大）。
- **expected_sacrifice**: 稳定线承担双轨维护与特性语义漂移的代价；测量来源为 `.specify/memory/feedback/backlog.md` 中跨轨移植/兼容条目占稳定线变更预算的比例，按 release 记录。
- **revision_trigger**: 连续两个 release 跨轨移植/兼容条目超过稳定线变更预算的 20%，或实验线通过 §Decision.4 的就绪门且出现只有 ai-harness 能服务的客户端需求 → 重开迁移决策。

## Consequences

- Positive: existing clients stay on the proven stable line; ai-harness can innovate without a parity tax; no dual-write or premature migration risk; both CLIs are available for their respective tracks.
- Negative: two skill sets, two CLIs, and diverging feature semantics must be maintained; cross-track fixes are manual; feature-ID references are not portable without a redirect policy; the migration debt grows while the trigger is not met.
- Operational: the 2026-11-24 fleet audit found 7 current containers (spec-kit plus 6 clients), 12 old-runtime clients, 7 partial/unreadable clients, and 1 broken copy; the stable line continues to serve them. Projects that are unreadable to the audit user need an owner-side or privileged read to complete their check.
