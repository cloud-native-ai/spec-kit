# Quickstart: Feedback 自省流程(047)

端到端走查:在**临时工作区**(`--workspace-root`)中造条目 → 自省 → 确认处置 → 富化打包 → 验包。全程无网络、不碰真实存储。

> 执行验证说明:带 ⚙️ 的命令使用**既有**引擎动作,已于本规划阶段对真实引擎执行验证(2026-08-28);带 📌 的命令使用**新增**动作/flag,由契约测试(engine-cli C-1..C-12)在实现期钉死并执行验证。

## 0. 准备临时工作区 ⚙️

```bash
tmp=$(mktemp -d)
mkdir -p "$tmp/.specify/memory/feedback"
```

## 1. 造两条 open 条目(模拟同单元同类摩擦) ⚙️

```bash
python3 .specify/scripts/python/feedback-utils.py --workspace-root "$tmp" --action record \
  --unit-id "/speckit.plan" --unit-type command --run-id "demo-run-1" \
  --review "plan 模板 Phase 1 摘要占位易被预先填写" \
  --points-file <(echo "- 模板应强调 summarize-after 纪律")
python3 .specify/scripts/python/feedback-utils.py --workspace-root "$tmp" --action record \
  --unit-id "/speckit.plan" --unit-type command --run-id "demo-run-2" \
  --review "plan 模板摘要预写导致返工" \
  --points-file <(echo "- 同上,计数漂移")
```

## 2. 范围快照(摘要投影,summary-first) ⚙️

```bash
python3 .specify/scripts/python/feedback-utils.py --workspace-root "$tmp" \
  --action list --disposition open --format json
```

→ 得到条目 id 清单与摘要(不含正文),构成自省范围快照。

> 注:本临时工作区无 probe 注册表,条目 `kind` 为空,故此处不加 `--kind internal`;真实客户项目(注册表在位)可加 `--kind internal` 收窄到内部条目(执行验证 2026-08-28:registry 缺失时 `--kind internal` 会过滤掉全部遗留条目)。

## 3. 场景化分析(agent 推理)与报告落盘

agent 调出 `/speckit.plan` 模板当前源码核验两条主张 → 聚类为一个 Finding → 按 `contracts/introspection-report.md` schema 写报告到 `$tmp/.specify/memory/feedback/introspection/introspection-<ts>.md`。

## 4. 注册报告(结构校验 + 条目关联) 📌 engine-cli C-1..C-6

```bash
python3 .specify/scripts/python/feedback-utils.py --workspace-root "$tmp" \
  --action introspect-register --report-file "$tmp/.specify/memory/feedback/introspection/introspection-<ts>.md"
```

→ 输出 `report_id` / `linked=2` / `disposed=0`;条目 frontmatter 写入 `introspection_ref`。

## 5. 用户确认 → 批量处置生效 📌 engine-cli C-3/C-7

```bash
python3 .specify/scripts/python/feedback-utils.py --workspace-root "$tmp" \
  --action introspect-register --report-file <同上> --confirm
```

→ 报告 `status=confirmed`;报告建议处置逐条生效(等价 `dispose --to processed --reason ... --ref ...`)。

## 6. 富化打包 📌 engine-cli C-9..C-11

```bash
python3 .specify/scripts/python/feedback-utils.py --workspace-root "$tmp" \
  --action package --include-introspection
unzip -l "$tmp/.specify/memory/feedback/packages/feedback-*.zip"
```

→ zip 内含条目 `.md` + `MANIFEST.md`(末尾 `## Introspection Reports` 节)+ `introspection/introspection-<ts>.md`。

## 7. 清理

```bash
rm -rf "$tmp"
```
