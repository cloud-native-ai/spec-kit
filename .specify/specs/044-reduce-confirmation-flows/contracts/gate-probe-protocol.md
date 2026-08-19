# Gate Probe Protocol Contract(门控必要性探针契约,044 Phase 7)

钉住 FR-012~FR-015 的机械不变量;执行入口为契约测试与扫描器。

## C-1 注册表结构

- C-1.1 `shared/definitions/probe-definitions.md` Classes 表 MUST 含 `command-gate`(target_slice=commands)与 `skill-gate`(target_slice=skills),kind=internal,insertion_type=`confirm-gate`。
- C-1.2 Objects 表中每个 gate 对象的 `lifecycle_point` 形如 `gate-<slug>` 且全局唯一;wrap-up 行 MUST 排在 gate 行之前(行序即无 lifecycle_point 解析的优先级)。
- C-1.3 `.specify/shared/definitions/probe-definitions.md` 镜像与 canonical 字节一致(sync-mirrors 对账)。

## C-2 指针双向对账

- C-2.1 每个 gate 对象 MUST 在门控点位存在单行指针 `> Gate probe: <object_id> — …`(tool-definitions.md:121 与 tools.md:91 共用 `gate-tools-invoke-prompt` 一个对象、两处锚点)。
- C-2.2 指针措辞 MUST NOT 命中 `scan-confirmation-gates.py` BLOCKING_PATTERNS:落地后 `--json` total == 22、by_class == {governance_kept:10, destructive:12}、violations 空。
- C-2.3 gate 对象不参与 wrap-up embed 对账(`--action probes --reconcile` 对无 `## Feedback` 嵌入的 gate 对象 exit 0);embed-without-object 方向仍 exit 2。

## C-3 引擎解析

- C-3.1 `--action record --lifecycle-point <gate_id>` MUST 按 (unit, lifecycle_point) 解析到 gate 对象,frontmatter 落 `probe/kind/slice`。
- C-3.2 不带 `--lifecycle-point` 的 record MUST 仍解析 wrap-up 对象(回退行为字节级不变)。
- C-3.3 未知 (unit, lifecycle_point) 组合 MUST exit 2,错误信息含 `lifecycle_point`。

## C-4 观察条目

- C-4.1 条目正文 MUST 含字面标记 `confirm-gate`;`--action list --contains confirm-gate` 可检索。
- C-4.2 run_id 形如 `gate:<object_id>:<UTC ts>`(同分钟重复追加 `:<seq>`);(unit_id, run_id) 去重键允许多次触发。
- C-4.3 采集红线:只自动记录、零额外提问、非阻塞;记录失败不得使宿主流程失败(协议见 `shared/guidelines/confirmation-gates.md` §门控观察协议)。
