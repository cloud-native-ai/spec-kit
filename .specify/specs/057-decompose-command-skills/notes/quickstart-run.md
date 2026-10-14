# Quickstart Run — 057-decompose-command-skills

三场景实跑留痕(2026-10-14,implement T021/T022)。teardown 全部实跑并验证。

## 场景 A — run-skills 运行未注册技能(实跑,fresh-context)

- **方法**:临时夹具技能 `fixture-draft` 置于 `skills/internal/`(已知位置集内,frontmatter 自declared 非名册成员);派发 fresh-context 子代理,唯一允许读物 = run-skills SKILL.md,调用 `run-skills fixture-draft`,附快速失败注入子句。
- **真实结果**(子代理回报逐字要点):
  - 解析:`/storage/project/cloud-native-ai/spec-kit/skills/internal/fixture-draft/SKILL.md`,**命中搜索顺序位置 1**(canonical internal),位置 2–4 全部未中——canonical 优先裁定在实跑中生效;
  - 路径披露:按程序要求立即披露所选路径;
  - 执行转述:夹具按其自身 SKILL.md 输出 `RUN-TOKEN-ALPHA` / `RUN-TOKEN-BETA` 两行,逐字转述;
  - 注册提示:目标不在任何宿主扫描面 → 尽力检测正确地**不**发提示;
  - runtime-mode 门:工作区含 `.specify/`,standalone 跳过不适用;
  - 无 ambient 上下文条件下仅凭技能体完成全流程 → **SC-001 成立**(单命中腿)。
- **异常回报(注入子句生效)**:子代理按二值分流把「编译 Wrap-up 嵌入的引擎命令行未含 `--run-id` 约定」判为 decision 并原样上送,未就地编造——该嵌入面是 71 单元统一的编译产物,修补属 probe 体系(跨特性),已记入反馈与 verification notes,不阻断本特性。
- **SC-002 腿覆盖说明**:确定性(同输入同路径)由位置 1 命中 + 顺序内联一次写明佐证;零命中/多命中腿为 agent 行为面(行为类条款 B-2),本运行未触发,按行为类纪律留评审强制,不声称已测。

## 场景 B — /speckit.team run 平价(结构实跑 + 义务对映)

- **实跑腿**:`test_c5/test_c6`(team.md 全部 run 指向 + Run Mode 程序性清零)、`test_c26`(五查调用形在 run-team 恰一次)、`test_focus_target_resolution` 六守卫(解析顺序/`resolve_effective_target`/团队默认后缀/`**Target 指派**`/逐字节等价/预填语义,全部对 run-team 实测)——117 项守卫全绿。
- **对映腿**:P-1…P-10 逐条对映核对(行为类义务,评审强制):每条在 run-team 对应节以同等强度在场,`本次 Target:` 三逐字形态与 `**Target 指派**` 字段逐字落位(grep 实测 3 处 + 1 处)。
- **变更前后 live run 对照**:未执行——`.specify/teams/` 下无现存团队;构造 goal+team 夹具需写 goal 注册表(共享状态、超出本特性范围)。处置:SC-003 的验收走其声明的度量源(义务对映表 + 评审抽样核对),live 对照腿记为 deferred 事实并写入 verification.md notes;此为前提证伪后的诚实降格,非静默跳过。

## 场景 C — /speckit.skills 路由全族(结构实跑)

- `test_c10`:路由表 5 行 + run 行语法钉住 `run-skills <名称|路径>` 全部实测在场;
- merge/think 意图词形与既有技能描述核对(实跑 grep):merge-skills/think-skills 描述含"合并""思想模拟/mental simulate"触发域,路由条件词形一致,未发明新词;
- 各意图 → 既有技能,零内联实现(goal T-003)。

## Teardown 记录

- `fixture-draft` 删除:`ls skills/internal/ | grep -c fixture` → 0;`git status --short skills/` → 空(名册恢复,C-12 口径不变)。
- 镜像复测:sync-mirrors --check 回到恰 1 条既有 DIFF(git_fleet.py),templates/skills.md 漏同步已在同轮修复(教训入反馈)。
