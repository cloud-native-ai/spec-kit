# Contract: 引擎子集边界与溯源(engine-subset-boundary)

> 合同 ID 前缀 C-B。验收:UPSTREAM.md 清单 ↔ 实际目录 diff 核对(SC-001)+ `tests/js/` 子集测试 + 镜像 `diff -rq`。

## C-B1 复制清单(MUST 完整存在)

以上游 commit `b2e621d` 为基线,`scripts/js/better-harness/` MUST 含:

| 路径 | 说明 |
|------|------|
| `session-analysis.mjs` | session 泳道 CLI 入口(上游根级,保持与 `session-analysis/` 平级的相对位置) |
| `session-analysis/`(整目录) | 37 顶层 .mjs + `platforms/{qoder,codex,claude,cursor}.mjs`;含 privacy-safe-text.mjs、semantic-facets.mjs 脱敏漏斗 |
| `core-change-watch/`(整目录 8 文件) | project 泳道;各文件自带 shebang 直接可执行 |
| `agent-customize/` | `cli.mjs, constants.mjs, storage.mjs, inventory.mjs, index.mjs, core/items.mjs, providers/{index,qoder,codex,claude,cursor}.mjs` |
| `coding-agent-practices/` | 仅 `asset-baseline.mjs, asset-integrity.mjs, inventory.mjs`(**不含 checkup/ 与 checkup.mjs**) |
| `agent-lint/`(4 文件) | `cli.mjs, index.mjs, hook-review.mjs, host-instructions.mjs`——asset-baseline 的 lint 依赖(勘察新增,记入 UPSTREAM.md 清单) |
| `dependency-governance/cli.mjs` | 可选依赖治理信号 |
| `package.json` | 最小化:`{"type":"module","engines":{"node":">=22.20.0 <25.0.0"}}`,**无 dependencies** |
| `UPSTREAM.md` | 溯源台账(C-B4) |
| `LICENSE` | 上游 MIT 副本 |

## C-B2 排除清单(MUST NOT 出现)

`harness-analysis/`(lead 分析器、report-source、渲染器、canvas-preview)、`better-harness-cli/`(registry 门面)、`evidence-bundle` 门面、`findings-recommend/`、`checkup/` 与 `checkup.mjs`、`packaging/`、`hooks/`、`doc-link-graph/`、`agent-guardrails/`、上游 `templates/ references/ case-studies/ docs/ skills/` 文档资产、`@vscode/tree-sitter-wasm` 与 `esbuild-wasm` 依赖。子集内 MUST 零 npm 外部依赖(仅 `node:` 内置模块;grep 断言无非 `node:`/相对路径的 import)。

## C-B3 相对路径不变式

子集内部交叉导入(`../session-analysis/...` 等)MUST 原样成立、零改写。允许的复制期修改仅限:(a) 删除对排除清单文件的引用(如有);(b) UPSTREAM.md 记录的显式修复。每处修改 MUST 在 UPSTREAM.md 修改日志留痕。

## C-B4 UPSTREAM.md 必填节

`# Upstream Provenance`:源仓库路径/URL、基线 commit `b2e621d`(上游 v0.3.0)、复制日期、许可(MIT);`## Subset Manifest`:C-B1 目录级清单 + agent-lint 纳入理由;`## Exclusions`:C-B2 摘要;`## Local Modifications`:表格(日期 | 文件 | 动机 | 可否回馈上游),初始至少含复制期修改(若零修改则写 "None");`## Resync Policy`:手动、按文件、diff 驱动,建议每季度审阅。

## C-B5 测试摘取清单

`tests/js/` MUST 含上游对应测试(同为 `node --test` 风格):`session-analysis.test.mjs`、`session-analysis-core-facts.test.mjs`、`session-analysis-providers.test.mjs`、`session-selection.test.mjs`、`session-episode-contract.test.mjs`、`core-change-watch.test.mjs`、`agent-customize.test.mjs`、`coding-agent-practices-inventory.test.mjs`、`agent-asset-baseline.test.mjs`、`agent-asset-integrity.test.mjs`、`agent-lint.test.mjs`、`dependency-governance.test.mjs`(+ 各自所需 fixtures);import 路径按新布局改写(此类改写属复制期修改,免逐条记录,UPSTREAM.md 总述一行)。`tests/js/run.sh` MUST 以 `node --test tests/js/` 一键运行,Node 缺失时以退出码 0 + skip 提示退出(CI 兼容)。

## C-B6 镜像不变式

`diff -rq scripts/js/better-harness .specify/scripts/js/better-harness` MUST 零差异(FR-014);任何引擎修改 MUST 双写。

## C-B7 边界侵蚀防御

`skills/collect-evidence/references/evidence-discipline.md` MUST 载明"采集子集只进事实,不进观点";向子集新增上游文件时 MUST 同步更新 UPSTREAM.md 清单,且新增文件不得来自 C-B2 排除清单(评审红线)。
