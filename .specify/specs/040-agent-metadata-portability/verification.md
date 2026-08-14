# Verification Log: 040-agent-metadata-portability (Feature 044)

**Date**: 2026-08-14
**Branch**: `040-agent-metadata-portability`
**Baseline**: 39 failed / 1720 passed / 1 skipped(`baseline-failed.txt`,name-level tracking)

## Success Criteria

| SC | Description | Status | Evidence |
|----|-------------|--------|----------|
| SC-001 | 三目录元信息中工具专属字段命中数为 0 | **pass** | `pytest tests/contract/test_neutral_vocabulary_scan.py` 5/5 绿(19 文件 frontmatter 重写后扫描清零) |
| SC-002 | 四家渲染工具 init 后符号链接数 0、真实文件数 = 中立源 agent 数 | **pass** | `tests/integration/test_init_agents.py::test_rendered_files_created_after_copy`(4 工具参数化)+ e2e:`specify init demo --ai qoder` 渲染 7 个真实文件、`find -type l` 计数 0 |
| SC-003 | 映射覆盖 6 工具(4 渲染 + 2 标注),交付时"待核实"为 0 | **pass** | `pytest tests/contract/test_tool_mapping.py` 9/9 绿(M-1 以 AGENT_CONFIG 键域动态对照;claude 行以官方页 + VS Code 二手核实双出处记录) |
| SC-004 | 新增目标工具支持所需 agent 定义文件改动数为 0 | **pass** | SC-004 drill:向 `_AGENT_METADATA_MAPPING` 注入 imaginetool 标注行,渲染为空且三目录 tree-hash 前后一致;已还原 |
| SC-005 | 同源同工具两次渲染逐字节一致 | **pass** | `tests/contract/test_agent_render.py::test_r4_deterministic_output` |
| SC-006 | 升级路径用户内容丢失数 0、悬空链接数 0 | **pass** | `test_agent_render_migration.py` 6/6 绿 + SC-006 drill(legacy link + 自写 agent + 手改产物):loss=0, dangling=0,备份可取回 |
| SC-007 | 三目录抽样一步判类正确率 100% | **pass** | SC-007 drill:8/8 文件按 T-1 表一步判定正确 |
| SC-008 | 全量回归相对基线零新增失败 | **pass** | 终态 `run-tests.sh`:37 failed(= 基线 39 − 2 条方言时代失败的修复),`comm -13 baseline final` 输出为空 |

## Completion Gate(复验)

| Gate | 命令 | 结果 |
|------|------|------|
| GATE-1 | `run-tests.sh` + `comm -13 baseline final` | 空(0 新增) |
| GATE-2 | 集成测试断言零符号链接 | 绿 |
| GATE-3 | `python3 scripts/python/sync-mirrors.py --check` | exit 0 |
| GATE-4 | `pytest tests/contract/test_neutral_vocabulary_scan.py` | 绿 |
| GATE-5 | `pytest tests/contract/test_tool_mapping.py` | 绿(无"待核实") |
| GATE-6 | `ls -la AGENTS.md`(软链接)+ `/speckit.instructions` 刷新 | 链接完好,instructions 再生成成功 |

## Deferred

- **T036**(术语表 5 条候选:Meta Agent 目录级 / Worker Agent 模板级 / 渲染产物 / 渲染清单 /"原 Agent"更正)—— 写入需用户显式确认(术语表协议);候选清单见 `feature-ref.md`。
- `tests/integration/test_context_injection.py::TestRoleSpecificContext` 的 7 条失败为**基线既有失败**(引用已废止的 `agent-role-*-template.md` 命名),非本需求引入,亦不在本需求 scope 内。

## Notes

- 实施中修复两个渲染器缺陷(均由新契约测试红→绿驱动):R-7 跨工具 prune 越界(清单按工具目标目录作用域化)、R-8 dangling legacy symlink 清理缺口。
- 发现并修复一个迁移张力:被替换的薄脚手架携带 Feature 025 上下文注入占位符,迁入的狗食正文携带具体事实 —— 处置为把参数化 Project Context 拼回模板(不实现 Feature 033 的 init 期渲染)。
- analyze 三项修订已落实:I-1(claude 行双出处,见 `_AGENT_METADATA_MAPPING` provenance)、U-1(`lite` 入 model-tier 域、`none` = 不下发)、U-2(render-pipeline 契约未提正文校验立场 —— body 不透明承载,见 R-2)。
- 提交序列(每个 phase 边界一次,全部 name-level 回归为空):`25ece787`(P1-P3)→ `b2fc6279`(US2)→ `5b3773f8`(US3)→ `e4ab56ae`(US4)→ `bf14894b`(US5)→ 本次 polish 提交。
