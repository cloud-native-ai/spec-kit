# Contract: Distribution & Docs（分发、docs 参考面与测试接线契约）

> 本契约钉死 FR-024（注册面与文档面同步）与 FR-025（投递形态无关）的交付义务。条款 D-n 一条一断言，逐条映射到 `tests/contract/test_sdd_loop_driver_skill.py` 的一个测试函数（D 类条款）或一个实现期核对动作。

## Artifact-class Clauses（D-1…D-7）

- **D-1 docs 参考页存在且定位正确**: `docs/reference/skills/sdd-loop-driver.md` 存在；面向人类读者（XV 判据：无未注解内部标识、路径引用足量）；内容覆盖①机制一句话定义与真源指针（skill 文件）、②双拓扑实例化指引（远端 ssh+su / 本地直驱，入口参数清单）、③执行侧可移植性说明（零 `.specify/` 依赖、三种投递形态等价）、④目标项目侧依赖说明（`.specify/` 仅在目标项目侧需要）。
- **D-2 docs 页为该目录形态合规成员**: 落位 `docs/reference/skills/<name>.md`（语义路径 `<area>/<topic>.md`）；不使用保留文件名；不声称 docs/ 页面为运行时必读。
- **D-3 契约测试文件存在且逐条款**: `tests/contract/test_sdd_loop_driver_skill.py` 存在，pytest marker `contract`；C-1…C-12 与 D-1…D-6 每条至少一个测试函数（`test_c1_...` / `test_d1_...` 命名对应）。
- **D-4 名册基线更新**: `tests/contract/test_run_skills_wiring.py` 的 `BASELINE_EXTERNAL` 名册加入 `sdd-loop-driver`（该测试自身 roster↔目录集合断言保持绿）。
- **D-5 镜像无 NEW drift**: `sync-mirrors.py --check --only skills/external/sdd-loop-driver` 在实现落地后对触及对报 ok（首跑 MISS→写入后 0 DIFF）；判据为触及对无 NEW drift，不取全树绝对判据（全树存在无关既有漂移，053 记录）。
- **D-6 零越界面**: 实现不改动 `templates/`、`src/specify_cli/`、`scripts/`（既有引擎零改动——FR-024 复用 sync-mirrors 不新建传播器；`match-team-preset.py` 与本特性无关）；`git diff --stat` 对这些目录为空。
- **D-7 门控基线不动**: `scan-confirmation-gates.py` total 保持 23 / violations 空（本特性交付面不在扫描面 `SCAN_ROOT_FILES=("templates",)` 内；该断言由既有测试持有，本特性以其仍绿为间接判据，不新增断言）。

## Behavior-class Clauses（D-8…D-9，不进测试钉死）

- **D-8 投递演练设置**: SC-009 验收的宿主环境设置为「预先手动放置 skill 文件」（三形态任一：宿主技能安装 / 提示词内嵌 / 路径引用）——实现期演练按此设置执行并记录形态。
- **D-9 真实演练 dogfood**: SC-001/SC-005 的验收以至少一次真实或演练驱动执行（入口一句话 → 断点探测 → 阶段派发 → DONE 校验 → 合并收尾），全程零用户提醒；演练记录归档特性目录 verification 材料。

## Mapping

| FR | 条款 |
|----|------|
| FR-003 | D-6（间接：零硬编码由 C 条款承载） |
| FR-024 | D-1, D-2, D-3, D-4, D-5, D-6 |
| FR-025 | D-1③, D-8 |
| SC-009 | D-8 |
| SC-001/SC-005 | D-9 |
| 宪章 IX/XI | D-6（零越界面 + 两顶帽子：框架源侧交付） |
