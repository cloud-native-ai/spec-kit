# Contract: 不变量与分发（Invariants & Distribution）

**Feature**: 077-doc-sdd-integration
**Spec**: [requirements.md](../requirements.md)
**Owner 指针**：八阶段集合与 P0/P1 定义归 `shared/workflow/expression-gates.md` § 阶段不变量；
镜像对归 `scripts/python/sync-mirrors.py` 的 `MIRROR_PAIRS`；命令副本归 `scripts/python/regen-command-copies.py`。

## 零新增机制

- **C-001** 本特性 MUST NOT 新增 `/speckit.*` 命令：`templates/commands/*.md` 的文件清单 MUST 与基线提交
  `c1cd4600` 逐字相同（差异集为空）。(FR-022)

- **C-002** 本特性 MUST NOT 引入运行时调度器、评分器、报表引擎或常驻服务，MUST NOT 新增第三方依赖。
  新增的确定性检查 MUST 只用标准库并落在既有 `scripts/python/` 下。(FR-022)

- **C-003** 门禁面数量 MUST NOT 改变：`doc-consistency-check.py --faces` 仍为四面，六面 owner 的封闭集不变；
  新增能力 MUST 以「既有检查器的新动作」或「既有引擎的新键族」实现。(FR-022, FR-023)

## 编辑面与镜像

- **C-004** 改动的唯一编辑面 MUST 是框架源与框架测试面（`templates/`、`shared/`、`skills/`、`scripts/`、`tests/`）。`.specify/` 运行时副本
  MUST 由既有同步机制产出，MUST NOT 手改。(FR-024)

- **C-005** 分发判据 MUST 是「相对改动前基线零新增漂移」：`sync-mirrors.py --check` 与
  `regen-command-copies.py --check` 在本特性改动后 MUST 相对基线（两者均为退出码 0）无新增漂移。
  `templates/commands/**` MUST NOT 进入 templates 镜像对，只经 per-tool 命令副本分发。**副本套数 MUST 以脚本为准**：
  `regen-command-copies.py` 的 `_ASSISTANT_COMMAND_DIRS` 最多登记六个目标，而它只为**本仓已存在**的目标目录产出副本
  （当前本仓四个：`.claude` / `.github` / `.qoder` / `.opencode`）；契约 MUST NOT 写死某个套数，MUST NOT 把「六」当成
  「本仓应产出的数量」。(FR-024)

- **C-006** 未刷新的项目 MUST 保持改动前行为：旧副本不含类别读取，其七个模板 MUST NOT 出现接线子节。
  「刷新前后差异只出现在是否含类别读取」这一点上，MUST NOT 顺带改变其他行为。(FR-024)

## 与既有 Feature 的边界

- **C-007** 本特性 MUST NOT 削弱 069 已建立的不变量：八阶段集合不变、门禁数量不降、P0/P1 定义不动、
  analyze 与 review 调用率 100%。(FR-025)

- **C-008** 一条 spec 目录 MUST 只绑一个 Feature。077 MUST 作为**新建 Feature 的承接边**而非 069 的新切片；
  承接关系 MUST 记录在 `features/077.md` 与 requirements § Related Feature。(FR-025)

- **C-009** 两份 owner 文档的变更 MUST 是**类条件追加**（新增特性线声明面与调用点行），MUST NOT 重写其既有条款；
  逐流程台账 MUST 保持 79 行量级且零缺口（新增 `spec:` 键不进台账）。(FR-023, FR-025)
