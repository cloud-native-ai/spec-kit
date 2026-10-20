# Contract: CLI Capability Profiles（CLI 能力档案）

**Feature**: 064（CLI 档案权威归属；收编 Feature 063 的 provisional 范围）
**Owning FR**: FR-033…FR-045
**实体**: `data-model.md` § E9；决策 `research.md` § R10；063 逐条裁决 `notes/063-overlap-adjudication.md`
**Implementation surface**: `skills/external/sdd-loop-driver/references/cli/index.md`（schema/观测程序 owner）、`references/cli/<cli>.md`、`SKILL.md`（H2 节）、`docs/reference/skills/sdd-loop-driver.md`、`shared/definitions/probe-definitions.md`（Probe Object 一行）、`tests/contract/test_sdd_loop_driver_cli_profiles.py`

## A. Profile Set & Shape

- **CLP-01（档案集合与落点）**: 每个作为 subagent 调用的 CLI MUST 拥有独立档案 `skills/external/sdd-loop-driver/references/cli/<cli>.md`；集合 MUST 至少含 `qodercli`、`claude`、`codex`、`opencode`、`hermes`。schema 与观测程序的单一 owner 是 `references/cli/index.md`（索引型文件按宪法 X 的路径语义命名；宪法 X 的保留名阻断严格范围只覆盖项目根与 `docs/`，此处为命名一致性选择）。没有档案的 CLI MUST NOT 被派发：驱动 MUST 先建立最小骨架、记录缺口，再按安全缺省派发（FR-033）。
- **CLP-02（八个必填维度）**: 每份档案 MUST 覆盖：① 调用方式与关键参数、提示词/权限模式；② 输出模式（`-p` 缓冲 vs `--output-format stream-json`）与事件形状；③ 后台/超时上限（`BASH_DEFAULT_TIMEOUT_MS`/`BASH_MAX_TIMEOUT_MS`、默认最大 600,000 ms、正值覆盖、0/负值语义）及与阶段 deadline 的区分；④ 哨兵可靠性与非终止回显；⑤ 缓冲/可见性行为；⑥ session/run 日志位置；⑦ detach 行为（`setsid`/`nohup`/`disown`）、信号/退出与孤儿检测；⑧ 已知缺陷、版本适用性与证据。缺一维即契约失败（FR-034）。
- **CLP-03（known/unknown 与 provenance）**: 每条目 MUST 标 `known|unknown`；`known` MUST 带 `observed_at`、`cli_version`、`evidence_ptr`；`unknown` MUST NOT 被猜测值填充。每份档案 MUST 有 `## Provenance` 表（日期/触发点/观测摘要/档案变更/反馈 id）。版本/平台不一致 MUST 视为新观测，不得沿用旧结论（FR-035, V-CLP-2）。
- **CLP-04（qodercli 初始事实）**: `qodercli.md` MUST 至少记录：`-p` 缓冲至退出；`BASH_DEFAULT_TIMEOUT_MS`/`BASH_MAX_TIMEOUT_MS` 正值覆盖；默认最大 600,000 ms；`--output-format stream-json` 支持；session/run 日志位于 `~/.qoder/logs/` 的实测路径；主会话故障需脱离 runner 才能存活。超时环境变量 0/负值语义 MUST 记 `known` 或 `unknown`，不得猜测（本阶段记 `unknown`，待实测）（FR-036）。
- **CLP-05（骨架纪律）**: `claude`/`codex`/`opencode`/`hermes` 的未观测维度 MUST 显式标 `unknown`；骨架 MUST 仍覆盖八维度并留空值，不得以训练知识填充（FR-033, FR-035）。
- **CLP-06（单一知识落点）**: `references/cli/` MUST 是 CLI 行为知识的唯一落点；其他 references、阶段提示词与 docs MUST 只引用，MUST NOT 复制档案内容（FR-042, 宪法 XIV）。
- **CLP-07（SKILL.md 入口）**: `SKILL.md` MUST 增加 H2 `CLI Capability Profiles` 节，声明：派发前查档；U4/U5 观测后更新；`references/cli/` 是唯一落点；schema owner 是 `references/cli/index.md`（FR-042）。

## B. Dispatch & Observation

- **CLP-08（U2 查阅）**: U2 派发前 MUST 只读查阅目标 CLI 档案，并据此选择超时形态与 detach 形态；**输出模式的吞吐默认（stream-json）由 Feature 063 拥有，档案只记录该模式的缓冲/事件事实，并在已知不兼容时提供回退观测，不得改写 063 默认**（边界见 `notes/063-overlap-adjudication.md` §2.7）；派发记录 MUST 带 `profile_id`、`profile_version`、`observed_cli_version`。匹配且无新事实时 MUST NOT 产生反馈（FR-037, V-CLP-3）。
- **CLP-09（U4/U5 比对）**: U4 独立校验 MUST 比对输出模式/事件形状、哨兵来源、status/exit 字段、runner rc 与 watcher 判定、日志/session 位置；U5 停线 MUST 比对已知缺陷、超时上限、detach/孤儿行为（FR-038）。
- **CLP-10（观测事件与写序）**: 观测事件 = (a) 与 `known` 不符；(b) `unknown` 获得已验证值；(c) 新版本/平台行为首次出现。处置顺序 MUST 为：先写状态脊 `cli_observations` → 更新档案 provenance → 记录恰好一条反馈。一次观测事件恰好一条反馈；无新事实零反馈（FR-039, V-CLP-3）。
- **CLP-11（稳定标记）**: 反馈 MUST 经既有 `feedback-utils.py --action record --unit-id "skill:sdd-loop-driver" --unit-type skill` 记录，`--review`/`--points` 含稳定标记 `cli-profile:<cli>`；可由 `--action list --contains "cli-profile:<cli>"` 检索。MUST NOT 复制/替代 feedback 引擎，MUST NOT 自动外传（FR-040, STR-001）。宿主无 `.specify/`（standalone）时，按编译 `## Wrap-up` 的 runtime-mode gate 跳过引擎调用，但档案更新与收尾汇总中的观测报告仍是必需项。
- **CLP-12（Probe Object）**: 观测点 MUST 经既有 probe 注册表登记为最小 Probe Object `skill-sdd-loop-driver-cli-profile`：`class_id=skill-wrapup`、`unit=skill:sdd-loop-driver`、`lifecycle_point=wrap-up`，以 `probe-utils.py --action probes --validate` exit 0 为唯一登记判据。该主落点已实测通过（2026-10-20）；`custom:` unit 不匹配注册表 unit 正则、external 形态要求 `ext-` 前缀，二者 MUST NOT 作为 fallback 登记。MUST NOT 新增 lifecycle point、Probe Class、Handler 或 HandlerBinding；若主落点未来被拒绝，MUST 先修订注册表契约并记录裁决（FR-040）。
- **CLP-13（行为不变）**: 档案更新 MUST NOT 改变哨兵语义、watcher 判定状态机/退出码、确认门、阶段 deadline 或测试预算；当前阶段 MUST 使用 U2 记录的形态，更新 MUST NOT 回溯改变。若观测冲突使当前阶段无法安全完成，MUST 走既有 U5 停线/重试程序，MUST NOT 以更新档案代替行为修复（FR-041, V-CLP-4）。
- **CLP-14（版本与缺陷生命周期）**: `known` 条目 MUST 声明适用版本；缺陷保留历史，修复记 `fixed_in`，不得在未复测时把旧缺陷当当前事实；冲突观测同存并附证据，不得静默择一（FR-035, V-CLP-6）。

## C. Boundary & Delivery

- **CLP-15（与 061 矩阵边界）**: 派发资格（可接受形态/旗标/支持集）MUST 以 `scripts/python/execution-config.py` 的 `CAPABILITY_MATRIX` 为唯一 owner；档案只记录观测行为。冲突时派发资格以矩阵为准，档案记录观测并产生反馈；矩阵变更 MUST 经其 owner 流程，不得由档案更新暗改（FR-043, V-CLP-5）。
- **CLP-16（交付与镜像）**: 档案与 `index.md` MUST 位于 `references/cli/`，经 `scripts/python/sync-mirrors.py --only skills/external/sdd-loop-driver` 同步到 `.specify/skills/sdd-loop-driver/`；契约测试 MUST 钉住档案集合、八维度、known/unknown 纪律、`cli-profile:<cli>` 标记、Probe Object 注册、SKILL.md H2 与 docs 入口；MUST NOT 新增技能、命令、常驻服务、外部依赖或模型 API（FR-045）。
- **CLP-17（063 收编与仓库级唯一 owner）**: 063 的 provisional `FR-044…FR-049` 与 `CP-01…CP-10` MUST 按 `notes/063-overlap-adjudication.md` 的逐条裁决迁移至本契约；063 合并时 MUST 删除其 provisional 档案契约并改为指向 064，MUST NOT 双 owner 或静默复制。仓库级唯一 owner 由 `test_clp_17_no_063_duplicate_owner` 守卫：扫描整个仓库（不限 064 规格目录），第二份 CLI-profile 契约、`references/cli/README.md`、`test_cli_profile_record.py` 或同 unit 的第二 Probe Object 均判失败；合并完成后守卫 MUST 转绿（FR-044）。

## 063 → 064 条款映射（摘要；逐条理由见 notes）

| 063 条款 | 064 归宿 | 裁决 |
|----------|----------|------|
| FR-044 / CP-01 档案集合与落点 | 064 FR-033 / CLP-01 | 迁入；`README.md` 改为 `index.md` |
| FR-045 / CP-02 维度 | 064 FR-034 / CLP-02 | 合并；七维扩为八维（detach/信号/孤儿） |
| CP-03 known/unknown/provenance | CLP-03 | 迁入 |
| FR-046 / CP-04 SKILL.md H2 与单一 owner | 064 FR-042 / CLP-06/07 | 迁入；H2 名保持 `CLI Capability Profiles` |
| FR-047 / CP-05 U2 查档 | 064 FR-037 / CLP-08 | 迁入 |
| FR-047 / CP-06 观测触发 | 064 FR-038/039 / CLP-09/10 | 迁入 |
| FR-047 / CP-07 probe+feedback | 064 FR-040 / CLP-11/12 | 迁入；Object id 改为 `skill-sdd-loop-driver-cli-profile` |
| FR-048 / CP-08 行为不变 | 064 FR-041 / CLP-13 | 迁入 |
| CP-09 版本/缺陷生命周期 | 064 FR-035 / CLP-14 | 迁入 |
| FR-049 / CP-10 交付与测试 | 064 FR-045 / CLP-16 | 迁入；测试文件改名 |
| 063 stream-json 默认 / nohup 脱离 | 063 保留 | 064 依赖引用，不复制；档案记录 stream-json 事实 |
| 063 E6/E7/E8 数据模型字段 | 063 保留 | 064 引用其派发记录/状态脊字段，扩展 `cli_observations` 与 provenance |

## Traceability

| Clause | FR/SC | Planned tests |
|--------|-------|---------------|
| CLP-01/CLP-05 | FR-033, SC-006 | `test_sdd_loop_driver_cli_profiles.py::test_clp_01_profile_set`, `test_clp_05_skeleton_unknown` |
| CLP-02/CLP-04 | FR-034, FR-036, SC-006 | `test_clp_02_eight_dimensions`, `test_clp_04_qodercli_initial_facts` |
| CLP-03/CLP-14 | FR-035 | `test_clp_03_known_unknown_provenance`, `test_clp_14_defect_lifecycle` |
| CLP-06/CLP-07 | FR-042 | `test_clp_06_single_knowledge_point`, `test_clp_07_skill_section` |
| CLP-08/CLP-09/CLP-10/CLP-11 | FR-037…FR-040, SC-006 | `test_clp_08_u2_consult_record`, `test_clp_10_write_order_one_feedback`, `test_clp_11_marker_retrievable` |
| CLP-12 | FR-040 | `test_clp_12_probe_object_registered` + `probe-utils.py --action probes --validate` |
| CLP-13/CLP-15 | FR-041, FR-043 | `test_clp_13_non_interference`, `test_clp_15_matrix_authority` |
| CLP-16/CLP-17 | FR-045, FR-044 | `test_clp_16_delivery_mirror_docs`, `test_clp_17_no_063_duplicate_owner` |
