# Contract: Distribution & Docs（分发、docs 参考面与测试接线契约）

> 本契约钉死 FR-024（注册面与文档面同步）与 FR-025（投递形态无关）的交付义务。条款 C-14…C-22 一条一断言（条款 id 语法真源 `shared/definitions/contract-clause-definitions.md` § 1 规定 id 形态为 `C-<数字>`，本文件沿用 C 命名空间续编；编号 = 交付顺序），逐条映射到 `tests/contract/test_sdd_loop_driver_skill.py` 的一个测试函数（D 面条款）或一个实现期核对动作。

## Artifact-class Clauses（C-14…C-19，编号 = 交付顺序）

- **C-14 docs 参考页存在且定位正确**: `docs/reference/skills/sdd-loop-driver.md` 存在；面向人类读者（XV 判据：无未注解内部标识、路径引用足量）；内容覆盖①机制一句话定义与真源指针（skill 文件）、②双拓扑实例化指引（远端 ssh+su / 本地直驱，入口参数清单）、③执行侧可移植性说明（零 `.specify/` 依赖、三种投递形态等价）、④目标项目侧依赖说明（`.specify/` 仅在目标项目侧需要）。
- **C-15 docs 页形态合规**: 落位 `docs/reference/skills/<name>.md`（语义路径 `<area>/<topic>.md`）；不使用保留文件名；不声称 docs/ 页面为运行时必读。
- **C-16 契约测试文件完整**: `tests/contract/test_sdd_loop_driver_skill.py` 存在，pytest marker `contract`；本契约 C-14…C-19 与 skill-structure.md C-1…C-13 每条至少一个测试函数（`test_c<N>_...` 命名对应）。
- **C-17 名册基线更新**: `tests/contract/test_run_skills_wiring.py` 的 `BASELINE_EXTERNAL` 名册加入 `sdd-loop-driver`（该测试自身 roster↔目录集合断言保持绿）。
- **C-18 镜像无 NEW drift**: `sync-mirrors.py --check --only skills/external/sdd-loop-driver` 在实现落地后对触及对报 ok（首跑 MISS→写入后 0 DIFF）；判据为触及对无 NEW drift，不取全树绝对判据（全树存在无关既有漂移，053 记录）。
- **C-19 零越界面（归属化形态，2026-10-15 implement 期修订）**: 本特性的交付面 MUST NOT 含引擎路径（templates/、src/、scripts/）——以特性交付文件集断言（test_c19 检查特性各交付物路径不落引擎前缀）。原「`git diff --stat` 对引擎目录为空」的全树形态在并发会话作业下前提失效（实测：scripts/python/sanitize-utils.py、templates/instructions-template.md 存在并发会话未提交改动，外部归因、非本特性产物），已按 gate-premise-decay 规则注记；全树形态的核对改由 T030 以「特性归属文件清单」+外部差异披露执行。

## Behavior-class Clauses（C-20…C-22，不进测试钉死）

- **C-20 门控基线不动**: `scan-confirmation-gates.py` total 保持 23 / violations 空（本特性交付面不在扫描面 `SCAN_ROOT_FILES=("templates",)` 内；该断言由既有测试持有，本特性以其仍绿为间接判据，不新增断言）。
- **C-21 投递演练设置**: SC-009 验收的宿主环境设置为「预先手动放置 skill 文件」（三形态任一：宿主技能安装 / 提示词内嵌 / 路径引用）——实现期演练按此设置执行并记录形态。
- **C-22 真实演练 dogfood**: SC-001/SC-005 的验收以至少一次真实或演练驱动执行（入口一句话 → 断点探测 → 阶段派发 → DONE 校验 → 合并收尾），全程零用户提醒；演练记录归档特性目录 verification 材料。

## Mapping

| FR | 条款 |
|----|------|
| FR-003 | C-19（间接：零硬编码由 skill-structure 条款承载） |
| FR-024 | C-14, C-15, C-16, C-17, C-18, C-19 |
| FR-025 | C-14③, C-21 |
| SC-009 | C-21 |
| SC-001/SC-005 | C-22 |
| 宪章 IX/XI | C-19（零越界面 + 两顶帽子：框架源侧交付） |
