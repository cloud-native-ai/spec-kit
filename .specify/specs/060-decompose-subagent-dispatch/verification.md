# Verification Log: 060-decompose-subagent-dispatch

**Feature**: 060 「驱动子代理」机制的技能化分解与公用化
**Implemented**: 2026-10-17（implement run；基线冻结 2026-10-16/17 见 notes/pre-change-measurements.md）
**DoD Status**: green（逐项见下；无 void 行）

## SC Status

- SC-001_status: pass — T034 实跑：sdd-executor 模板实例化 2 个职责实例（sdd-setup-executor / sdd-requirements-executor，`capacity-scope: sdd-executor`），引用审计零复述（能力面三标记在实例体零命中）；render-agents 渲染 7 agents 含两实例。
- SC-002_status: pass — T035 实跑：本地拓扑真实派发（`qodercli -w /tmp/sdd-exec-sandbox --permission-mode auto -p "$(cat brief-t035.md)"`，exit 0，哨兵 REPORT-DONE + 诚实 ANOMALY 行）；远端形态按 SC-002 允许的命令形态审计替代实跑（dispatch-recipes R3 命令逐要素含 ssh/su/CLI/目录四要素）；两形态下 Template/Instance 制品零改动（git status 实例文件跨运行不变）。
- SC-003_status: pass — T031 复测：五族检查表成组共现恰 1 落点（run-agent dispatch-preflight.md）、nohup 形态恰 1 权威落点（loop-driver R3，H-04 裁定）、反嵌套义务字面迁出（"MUST NOT 加载本手册" 零命中）；P 表 15 行全填实（T022）；义务清单逐条追溯见 contracts/delegation-parity.md。
- SC-004_status: pass — T036 端到端：经 run-agent 机制派发（qodercli 本地拓扑 + 阶段简报）完成真实 SDD 阶段 /speckit.constitution——三条件齐备（CONSTITUTION-DONE 哨兵 / constitution.md 产物 20.5KB / 显式 ANOMALY 行 ×2 诚实披露）；子代理输入反嵌套审计：brief 与回传日志中驱动技能引用零命中。
- SC-005_status: pass — 终跑 name-level 对比：NEW=0（vs 37 项基线，notes/baseline-failed.txt）；RESOLVED=12（instructions-template 镜像对比发散簇——T005 批量 --write 按源侧收敛，超出基线的改善，披露）；现行失败 25 全为既有欠账。
- SC-006_status: pass — test_c3_no_third_owner_of_three_layers 绿；三层词条 owner 仍为 agent-definitions.md + subagent-definitions.md 两文档（接线段为引用不定义）。

## FR Coverage

FR-001..016 全部落地（feature-ref.md FR→C 映射表逐行对账；test_agent_dispatch_mechanism.py 35 条款全绿）。

## Gate Re-validation（Completion Gate）

- GATE-1 ✓：NEW=0（comm -13 baseline current 为空；本文件顶注记）
- GATE-2 ✓：sync-mirrors --check 全 ok（0 DIFF——既有 instructions-template DIFF 已收敛，披露于 SC-005）
- GATE-3 ✓：`grep -cE '^- \[[ >]\]' tasks.md` = 0
- GATE-4 ✓：本文件逐 SC 记录（SC-001..006 全 pass）
- GATE-5 ✓：test_agent_dispatch_mechanism.py 35/35 绿（0 failed）

## Notes

- **既有欠账披露**：25 个现行失败全为基线既有（12 个 060 前欠账 + 7 个 exec-quant 环境性 + ~6 个 fast_fail/gate 族），与 060 无关（构成归因见 notes/pre-change-measurements.md）。
- **超基线改善披露**：instructions-template 镜像 DIFF（既有 1 条）在 T005 批量镜像同步中按源侧收敛——mirror_parity 测试簇 15 个恢复绿；该面不属 060 触碰对，收敛系 sync 引擎的机制行为。
- **钉住测试蓄意更新**：test_sdd_loop_driver_skill（c3/c4/c14/c20）与 test_sdd_project_setup（c3/c8）+ fast_fail（i10/i12 FACTORY_PRESETS/bounded set）——断言钉的是委派化前旧态，按 060 已裁定变更蓄意更新（变更证据见 tasks 相位提交）。
- **T035/T036 真实派发环境**：qodercli 1.1.72 本地 headless；沙箱 /tmp/sdd-exec-sandbox（specify init --here --ai qoder）；回传日志存 /tmp/t035-run.log、/tmp/t036-run.log。
- gate 拒绝重试计数：0（全程无 gate 失败重试）。
