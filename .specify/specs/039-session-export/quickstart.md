# Quickstart: 039-session-export 端到端走查

验证「导出 → 命名 → 描述 → 追溯」闭环的最小路径。所有命令示例由 `contracts/` 三份契约逐条 pin(实现尚未落盘,示例按契约文法书写;实施阶段 MUST 重跑本走查并回写结果)。

## 前置

- 一个已安装的目标 CLI(claude-code / codex-cli / qoder-cli / opencode 任一)且当前项目下有会话落盘。
- `skills/export-session` 改造完成(六家矩阵、目录形态)。

## 1. 导出当前会话为用户命名目录(US1)

```bash
python3 skills/export-session/scripts/export.py --name my-first-export --verify "用户最近一句内容"
```

验证点:
- 生成 `.session-export/my-first-export/`,含 `main.*` + `session-meta.json` + `SESSION.md`(子代理/状态/大结果按宿主落盘出现)。
- stdout 打印导出目录绝对路径;退出码 0。
- `--session <id>` / `--tool <name>` 显式路径各演练一次,行为与契约 §3 一致。
- 缺 `--name` → 退出码 2;`--name` 含 `/` → 退出码 2。
- 同名再导 → 拒绝(命令面交互确认后方可覆盖;脚本面直接失败)。

## 2. 支持矩阵收敛(US2)

```bash
grep -ciE 'qwen|qoderwork|oh-my-pi|kimi|codex-app' skills/export-session/SKILL.md skills/export-session/scripts/export.py
# 期望:0(被移除产品零残留;注意 qoder-cli 保留,"qoder" 单独出现不计)

python3 skills/export-session/scripts/export.py --tool copilot --name copilot-probe --verify x
# 期望:退出码 4,stderr 声明"该平台会话存储未探测到"(本环境探测结论)
```

验证点:
- `PARSERS` 键集合 == 六家规范名(契约测试断言)。
- 无平台专属依赖:SKILL.md 无 `a1 skill report` 段、无 `x-source`;全文无出站 URL(契约测试断言)。
- 保留四家逐家真跑导出(内容面不削弱:与改造前同夹具产物对照)。

## 3. 会话描述文档(US3)

对 §1 的导出产物:

- `session-meta.json` 字段逐一对照原始记录(tool/session_id/model/时间窗/规模计数)——程序提取,100% 一致。
- `SESSION.md` 元信息节与 meta.json 逐字段一致;总结节含任务脉络/关键决策/产物清单三段。
- 超预算构造:以大夹具触发 `over_summary_budget: true` → 骨架总结 + 降级声明(阈值与实际值)。

## 4. 团队 run 追溯衔接(US4)

```bash
python3 skills/export-session/scripts/export.py --name <team-slug>--<run-stamp>--<member-role> --verify "..."
```

- 以派发 label 命名导出派成员会话;run report 映射表(label → CLI → 成员)可引用该目录。
- 运行中会话导出:`snapshot: true`,总结声明截至时点。

## 5. 只读与零副作用(全场景)

- 导出前后宿主会话存储 hash 一致(集成测试断言;抽查手动对照)。
- `.gitignore` 未被修改;导出目录入库与否由用户自管。


---

## 走查记录(实施回写)

### 2026-08-12 — US1 首跑(T008,真实 claude-code 会话)

**§1 导出**:全部通过——
- `--name t008-e2e --tool claude-code` 成功,目录 `.session-export/t008-e2e/` 含 `main.jsonl` + `session-meta.json` + `SESSION.md`,stdout 末行为目录绝对路径;
- `--session <id>` 显式定位成功(t008-byid);
- 缺 `--name` → exit 2(「--name 必填」);`--name has/slash` → exit 2(文法越界,附文法说明);
- 同名冲突 → exit 2(「拒绝覆盖」,指名目录);无 --force 旁路;
- 命令流程第 5 步演练:agent 依据 main.jsonl 忠实补写结构化总结(该会话实为一次 /exit,总结如实写「无决策无产物」),元信息节字节未动。
- 测试产物已清理(.session-export/ 移除)。

### 2026-08-12 — US2 首跑(T012)

**§2 支持矩阵收敛**:全部通过——
- 被移除产品残留扫描(SKILL.md + export.py 双文件):`grep -ciE 'qwen|qoderwork|oh-my-pi|kimi|codex-app'` 均为 0;契约测试 42 例(rework 23 + genericity 19)全绿;
- `--tool copilot` / `--tool hermes` → exit 4 + 「会话存储未探测到」诚实声明(本环境探测结论,FR-010);
- 保留家 claude-code 真跑成功(目录形态 + 描述文档双件);opencode/codex-cli/qoder-cli 本环境未安装,按未安装路径(集成夹具已在契约测试覆盖);
- 平台依赖清零:SKILL.md 无 `a1 skill report` / `x-source`,全文无出站 URL;解释器探测纪律保留。

### 2026-08-12 — US3 首跑(T015)

**§3 描述文档**:全部通过——
- `tests/integration/test_session_description.py` 5 例全绿:meta 字段逐值一致(tool/session_id/model/workspace/时间窗/计数)、`over_summary_budget` 两侧(50,001 行夹具 true、正常 false)、SESSION.md 结构(STR-003 标识行 + 元信息节 + 总结占位节)、两形态逐字段一致、snapshot 窗口判定;
- 真实会话复验:meta↔SESSION.md 一致性 mismatch 为 none;null 字段全部标注「null(记录未含)」;stdout 输出预算判定(within summary budget);
- 预算常量冻结:SUMMARY_LINE_LIMIT=50000 / SUMMARY_BYTE_LIMIT=32MB(export.py:58-62)。

### 2026-08-12 — US4 首跑(T016)

**§4 追溯衔接**:通过——以派发 label 形 `viz-arena--20260812T120000Z--renderer` 为 `--name` 导出成功(文法天然兼容,`-` 为合法字符);目录名与 label 逐字相等,可被 run report 映射表引用;`snapshot: true` 快照语义复验通过;总结占位节在位(待 agent 补写)。测试产物已清理。

### 2026-08-12 — T020 全走查复跑(refresh-verify)

- **§1**:导出成功(SESSION.md + session-meta.json 在位)+ 同名冲突拒绝(exit 2)复跑通过。
- **§2**:copilot 探测 exit 4 + 声明复跑通过;残留扫描双文件计数 0/0。
- **§3**:meta↔SESSION.md 一致性、预算判定两侧(首跑证据 + 集成测试 5 例)。
- **§4**:label 形 `--name` 单独复跑 exit 0(组合脚本中一次 exit=1 为 grep -c 零计数截断 && 链的脚本假象,非缺陷,已归因)。
- **§5**:宿主会话存储导出前后 sha256 一致(只读取证)。

**SC 取证来源对照**:SC-001 → §1–§4 走查 + test_export_skill_rework(23 例)/test_session_command_surface(16 例);SC-002 → meta 字段程序提取对照(test_session_description 5 例)+ 真实会话 mismatch none + 总结忠实性抽查(t008-e2e /exit 会话如实写「无」);SC-003 → 定位机制回归(test_export_skill_rework 定位/退出码用例)+ 保留家真跑;SC-004 → test_export_skill_genericity(平台依赖/出站 URL 扫描 0)+ SKILL.md 重写后无 a1 上报段;SC-005 → test_export_skill_rework::test_export_does_not_touch_the_host_store + T020 §5 hash 对照 + 同名冲突 100% 拒绝(无旁路);SC-006 → T016 label 命名演练(目录名 == label)+ snapshot 语义。
