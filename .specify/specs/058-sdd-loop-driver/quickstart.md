# Quickstart: 无人值守 SDD 循环驱动机制（Feature 058）

> 场景状态两态标注：【已执行】= 本规划期真实跑过、输出原样粘贴；【实现后验证】= 依赖尚未落地的交付物，命令与预期由契约测试钉死（路由 b）或留待 implement 实跑。每个【实现后验证】示例逐例列前提（premises），`/speckit.tasks` 与 `/speckit.implement` 据此重测而非继承。

## Scenario 1 — 镜像与注册基线（US4/FR-024）【已执行·规划期基线】

触碰前基线测量（2026-10-15 实跑，输出原样）：

```bash
python3 scripts/python/sync-mirrors.py --check --only skills/external
```

实测输出（尾部）：

```text
DIFF  .specify/skills/git-workspace/SKILL.md
DIFF  .specify/skills/git-workspace/scripts/git_fleet.py
DRIFT detected — run: python3 scripts/python/sync-mirrors.py --write
```

**基线判读**：外部对存在 2 条**无关既有漂移**（git-workspace，非本特性触及文件）——实现判据取「sdd-loop-driver 触及对无 NEW drift」（D-5），禁止绝对全绿判据。注意：对尚不存在的子域跑 `--only skills/external/sdd-loop-driver` 会命中 `placeholder-only source` 跳过分支（0 源文件触发，文案误导但方向不变），基线测量必须取外层对。

既有测试基线（2026-10-15 实跑）：

```bash
bash scripts/bash/run-tests.sh tests/contract/test_run_skills_wiring.py -q
```

实测输出：`12 passed in 0.18s`。**实现后预期**：`BASELINE_EXTERNAL` 加入 `sdd-loop-driver` 且目录落地后，同一命令仍 `12 passed`（roster 集合断言是单个测试函数，名册加行不增测试数）——若转红即名册/目录失配。

**前提**：无（规划期即成立）。pytest 解释器由 `scripts/bash/run-tests.sh` 解析（`SPECKIT_PYTHON` / `.venv/bin/python` / `python3` / `python` 顺序，实测本机在候选链中解析成功；裸 `python3 -m pytest` 不可用——系统 python3 无 pytest，**必须经 runner**）。

## Scenario 2 — Skill 结构自包含核验（US4/FR-001/FR-002）【实现后验证】

```bash
# frontmatter 四字段与分类（C-1/C-2 钉死）
sed -n '1,12p' skills/external/sdd-loop-driver/SKILL.md
# 自包含反例扫描（C-10 钉死）：对 .specify/ 的每处出现必须处于底稿/背景语境
grep -n 'MUST.*\.specify/' skills/external/sdd-loop-driver/SKILL.md skills/external/sdd-loop-driver/references/*.md
# 预期：零命中（无「MUST 读框架路径」形态的运行时义务句）
```

**前提**：① `skills/external/sdd-loop-driver/` 已按 data-model E-1 落地（SKILL.md + 2 references）；② 契约测试文件 `tests/contract/test_sdd_loop_driver_skill.py` 已实现 C-1…C-12（D-3）——本场景的 grep 断言与 frontmatter 形态由该测试逐条钉死（路由 b），实现期以测试转绿为主证据、本场景命令为人工复核面。

## Scenario 3 — 零框架宿主加载与本地拓扑演练（US4/US6/SC-009/SC-005 本地段）【实现后验证】

```bash
# 宿主环境自证：无 .specify/（SC-009 前提探测，输出留痕）
[ ! -e .specify ] && echo "no .specify in host cwd" || echo "SPECIFY PRESENT - INVALID SETUP"
# 投递（三形态之一，FR-025）：复制 skill 到宿主技能目录（或粘贴/路径引用——等价）
cp -r <框架源>/skills/external/sdd-loop-driver <host-skills-dir>/
# 一遍性入口（本地拓扑，[[STR-002]] 起步或断点续跑）：
#   「使用SDD开发模式推动 <本地项目> …… 需要使用一个循环来完成这项工作，而不是每次由我提醒你『重试』或者『继续』。」
```

**前提**：① 宿主环境 cwd 无 `.specify/` 且未安装 spec-kit（前置探测留痕，D-8）；② 本地 qodercli 在宿主 PATH（`DISPATCH_CLI` 可覆盖）；③ 目标本地项目具备 `.specify/`（或演练选取新切片以覆盖 Edge Case 3 首推场景）；④ 演练目标仓库接受特性分支与本地合并（push 缺省不执行，G5）。
**边界/失败快速线**：断点探测无法判定 → 停线上送（Edge Case 1）；目标项目无 `.specify/` → 报告停线不自动初始化（Edge Case 2）。

## Scenario 4 — 一遍性入口远端拓扑演练（US1/US2/US3/SC-001…SC-004）【实现后验证】

入口话术 = 需求简报 §3 模板（ssh root@<别名> → su develop → qodercli 子代理 → 双线并行）。机制按 U0–U6 执行：断点探测 → 阶段派发（heredoc prompt 文件 + runner + 后台）→ 日志轮询至 `<STAGE>-DONE` → 独立校验 → 续环 → git 状态判定合并收尾 → 收尾汇总。

**前提**：① 远端别名可达、su 运行身份与项目路径就绪；② qodercli 在远端执行身份 PATH；③ 目标项目 `.specify/` 就绪且终态权威文档存在；④ 重试/超时缺省值（90 分钟 / 2 次）接受或入口覆盖；⑤ 合并收尾授权范围明确（缺省本地合并）。
**验收观测点**：全程用户「重试/继续」类提醒 = 0（SC-001）；伪完成样本判未完成（SC-003 变异演练）；异常注入达上限即停线落盘出上送件（SC-004）；双拓扑各一轮（SC-005）。

## 环境探测（规划期实测）

- pytest 仅经 `scripts/bash/run-tests.sh` 可用（Scenario 1 实测）；无需容器/镜像/网络。
- 交付面全部为文件制品——实现期环境依赖仅 pytest 与 git。
