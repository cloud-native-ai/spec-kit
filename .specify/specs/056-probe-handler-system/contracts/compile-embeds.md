# Contract: compile-embeds 编译动作（STR-003）

**Spec**: `.specify/specs/056-probe-handler-system/requirements.md` | **Date**: 2026-10-13
**Invocation**: `python3 scripts/python/probe-utils.py --action compile-embeds [--check] [--format text|json]`

## 输入

- **注册表**：`shared/definitions/probe-definitions.md`（Handler / HandlerBinding 章 + 既有 Class/Object 章）。
- **单元集**：scan_embed_units 同语义枚举（feedback-utils.py L1342–1364 迁入复用）——templates/commands/*.md + skills/{,external/,internal/}*/SKILL.md 中含字面 `## Feedback` 的单元；改后语义 = 含收尾段义务的编译单元集（实测改前 69 单元）。

## 解析与渲染（FR-010，算法详见 data-model.md）

1. Selector 命中 → 2. 扣减 per-unit 覆盖 → 3. Binding→Handler 解析 → 4. 按 order 升序、多 selector 合并 → 5. kind 固定派生调用形式：
   - **engine** → 一行 CLI 调用（引擎文件 + action，如 `python3 scripts/python/feedback-utils.py --action record`）
   - **agent** → 一行行为真源锚点引用（behavior_owner 路径 + 锚名）
   - **gate** → 一行治理条目引用（confirmation-gates.md 条目）
6. skill 面单元保留 runtime-mode gate 判定结构（FR-013）。

## 输出与写入语义

- **单段**：每单元至多一个 `## Wrap-up`（[[STR-001]]）段，带 AUTO-GENERATED 横幅（标记真源与指纹，供对账）。
- **零段语义**：零生效 handler 的单元不输出任何段（Q5 / FR-016）；简单命令与外部单元保持现状无段形态。
- **替换**：写入位置 = 既有手工 `## Feedback` 段落位；迁移完成态源模板面手工段清零（FR-016）。
- **原子写**：临时文件 + 原子替换（与 regen-command-copies.py / sync-mirrors.py 姊妹机制同型，FR-012）。
- **确定性不变量**：真源未变时两次编译逐字节一致（041 C-6 同型，FR-010）。

## `--check` 漂移预检（FR-012）

- 只读比对：产物内容 vs 由当前注册表再生成的内容。
- 不一致 → **exit 1** + 逐单元指名（ Sister 机制：regen-command-copies.py --check / sync-mirrors.py --check 同型）。
- 不写任何文件。

## 拒写条件（exit 2，封闭集）

孤儿 handler / 缺失 handler / 非法 action / order 冲突 / behavior_owner 不可达 / 重复 Binding 三元组 / **生成措辞命中 BLOCKING_PATTERNS（17 正则任一）**（FR-015/FR-017；命中即整体拒写并指名命中模式，不得以改 baseline 换通过）。

## 传播次序契约（FR-011，contract test 钉住）

```text
compile（probe-utils.py --action compile-embeds，写 templates/ 与 skills/ 源面）
  → regen（regen-command-copies.py，扇出 4 工具副本树）
  → sync（sync-mirrors.py --write，同步 6 对镜像）
```

- 次序固定；MUST NOT 新建传播器。
- 每步的漂移预检（--check）可独立运行；完整链路的次序由契约测试断言（mock 或 dry-run 形态证明能红）。

## 标题迁移义务（FR-010 尾句）

- 新段名 `## Wrap-up` 落地时，**同一变更内**迁移：041 C-5 嵌入点对账机制的标题钉点 + 既有契约测试中钉 `## Feedback` 段标题的断言（例：test_feedback_step_reference_form.py 的 surface 计数面、test_docs_step_injection.py 的邻接断言）。
- 迁移后：全仓源面不存在手工 `## Feedback` 嵌入段与 docs-sync 手工段（FR-016 完成态判据）。

## 契约测试锚点（route (b) 预登记）

| 不变量 | 测试落点（tasks 阶段建） |
|--------|--------------------------|
| 封闭集 5 action | test_probe_engine_action_sets |
| 确定性编译 | test_compile_embeds_determinism |
| --check exit 1 / 拒写 exit 2 | test_compile_embeds_check_and_reject |
| 零段语义 | test_compile_embeds_zero_handler_no_section |
| compile→regen→sync 次序 | test_compile_propagation_order |
| BLOCKING_PATTERNS 零命中 | test_wrap_up_wording_gate_safe |
| SC-007 ≤853 | test_wrap_up_line_budget |
