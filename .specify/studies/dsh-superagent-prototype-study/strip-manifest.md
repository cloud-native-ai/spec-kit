# Strip Manifest — dsh-superagent-prototype

## Provenance

| Item | Value |
|---|---|
| Target repo | `/storage/project/cloud-native-ai/dsh-superagent-prototype` |
| Origin | `git@github.com:deepseek-ai/dsh-superagent-prototype.git` |
| Single commit (shallow) | `8c32a9dc5d72c033816c6a8110b37f40cf94fba4` — "feat: add the dsh-superagent research prototype" |
| Commit author/date | DeepSeek Harness Team <team@dsh.dev>, 2026-11-01 (epoch 1793448339 +0800) |
| Study workspace | `/home/agent/tmp/study-code/dsh-superagent-prototype-study/` |
| Materialized from | working-tree `cp -a` (see § Anomaly: original git state damaged) |

## Deletion summary

| Class | Deleted files | Detail |
|---|---|---|
| 工程类配置 | 0 | None present at root: no `package.json` / lockfile / `tsconfig*` / `*.config.*` / `Makefile` / `Dockerfile` / CI dirs / `.gitignore` ran in this snapshot. The bundle appears to be consumed by a host (no package manifest), so there was nothing to strip. |
| 脚手架/生成物 | 180 | `.qoder/repowiki/` — Qoder-generated repo knowledge tree (see per-directory purpose rows below) |
| 测试用例 | 0 | No `tests/`, `test/`, `spec*`, `__tests__/`, fixtures in snapshot |
| 其他（非研读材料） | 1 | `LICENSE` — MIT boilerplate; no design information |
| **Total deleted** | **181** | 301 files before → **120 files kept** |

## Per-deleted-item purpose (Step 4 tech-stack evidence)

- `.qoder/repowiki/` (180 files, 2.4 MB) — AI-generated repository wiki:
  - `.qoder/repowiki/knowledge/zh/**` (≈100 files: `_module.yaml`, `概述.md`, `架构设计.md`, `技术栈.md`, `编码规范.md` per module) — 由 Qoder 静态分析生成的模块知识树，**二手解读**，用于交叉验证而不作一手证据。
  - `.qoder/repowiki/zh/content/**` (≈74 files: 快速开始 / 架构设计 / 核心引擎 / 源插件系统 / 数据存储 …) — 生成的"使用文档"视图，内容与 `docs/` 重叠但为派生文本。
  - `.qoder/repowiki/zh/meta/repowiki-metadata.json` — 生成器元数据。
  - 技术栈证据价值：该目录的存在与其自称内容表明 **TypeScript + pnpm + tsdown + Vitest + Cordis 插件框架 + Zod + SQLite**（见 `knowledge/zh/基于 tsdown + pnpm + Vitest 的 DSH Bundle 构建系统/*.md`），与 `src/` 的 import 形态一致（`define`/`Context` 来自 `@cordisjs/*` 系列，推断）。
- `LICENSE` (1 file) — MIT 许可证正文，无设计信息。

## Exceptions (kept despite matching deletion heuristics)

- `prompts/` — 文案资产（角色提示词），是产品行为的一部分而非脚手架，保留。
- `locale/` — 双语字符串资源（启动画面文案），保留。
- `docs/000–007*.md` — 项目自述设计文档，保留为 Step 3 文档清单来源。

## Anomaly: original git state damaged (not repaired in target)

- 原仓库 `.git/refs/heads/main` 被清零（0 字节），`HEAD` 指向未出生的 `main`，导致 `git clone file://…` 返回空仓库；`.git/index` 同时不可读（Permission denied）。
- 对象库完好：`git cat-file -t 8c32a9d…` = commit，`rev-list --count` = 1（shallow）。
- 处置：**不修改原仓库**；在研读工作区内用工作树拷贝 + 记录 commit hash 达成可追溯性。
- 影响：`git log` 深度历史不可得（本来就是 depth-1 研究原型单提交），git-analysis 仅能覆盖单次提交事实。
