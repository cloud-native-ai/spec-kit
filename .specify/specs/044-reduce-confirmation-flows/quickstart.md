# Quickstart: 确认门控精简(Feature 046)

三条走查,覆盖 P1(team 零确认)、度量面(扫描脚本)、保护面(破坏性门控保留)。

## 1. team 全流程零确认走查(SC-001)

前置:改写后的 `templates/commands/team.md` 与 `skills/create-team/` 已落盘并经副本再生。

1. 以 `/speckit.team` create 提供一个目标与成员设定。
2. **预期**:定义直接落盘为 `.specify/teams/<slug>.team.md`,流程输出定义内容与修改途径(无"是否确认创建"停等)。
3. 以 `/speckit.team` run 运行该 team(parallel 或 serial 模式)。
4. **预期**:直接启动执行,无"MUST NOT execute before confirmation"类停等。
5. 运行结束进入收尾。
6. **预期**:总结与记录自动完成;输出含三要素的执行报告;若反馈条目达阈值,仅在报告中附一行非阻塞提交提示(`python3 .specify/scripts/python/feedback-utils.py --action package`),收尾不被打断。
7. **断言**:全流程阻塞确认打断次数 = 0。continuous 模式另走一次:预期既有分级门控仍在。

## 2. 门控扫描:治理前后对比(SC-002 / SC-005)

```bash
# 治理前基线(实现期首扫存档)
python3 scripts/python/scan-confirmation-gates.py --json > baseline.json

# 治理后复扫并对比
python3 scripts/python/scan-confirmation-gates.py --json --baseline baseline.json
```

**预期**:
- `baseline_delta.total` 显示总数较基线(≈55–60)下降 ≥75%;
- 残留门控的 `action_class` 全部落在 `destructive` / `governance_kept` / `intrinsic`;
- `violations` 为空;退出码 0。
- 后续新增命令若引入非破坏性阻塞门控:复扫退出码 2(回流违例)。

注:扫描脚本为本需求新增交付物,上述命令形态由 `contracts/gate-scanner-contract.md` C-1/C-4/C-5 钉住并由契约测试验证。

## 3. 破坏性门控保留抽查(SC-004)

对保护清单逐项触发一次,确认前置确认仍在:

| 抽查项 | 触发方式 | 预期 |
|--------|----------|------|
| 反馈包删除前确认 | `/speckit.feedback` process 至 consume 报告 | 原子删除前停等确认 |
| 文档移动/归档 | `/speckit.docs` 发起 move/archive | dry-run 计划停等确认 |
| 会话导出同名覆盖 | `/speckit.session export --name <已存在名>` | 覆盖前停等确认 |
| 远程推送 | git-workflow 流程触发 push | 停等确认 |
| 访谈退出门 | `/speckit.interview` 尝试收尾 | 需用户显式确认结果稳定 |

**断言**:5/5 保留;任一缺失即 SC-004 失败。
