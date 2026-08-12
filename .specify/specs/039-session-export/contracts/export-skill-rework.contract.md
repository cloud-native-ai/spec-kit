# Contract: export-skill-rework(export-session 支持面收敛与目录化)

**Surface**: `skills/export-session/SKILL.md` + `scripts/export.py`(stdlib-only 单脚本)
**Implements**: FR-006, FR-007, FR-008, FR-009, FR-010, FR-011, FR-015, FR-016
**Upstream contract**: 既有 v1.3.0 行为面(定位机制、退出码)叠加式修订,不改变其语义的部分全部保持。

## 1. 支持矩阵(FR-006)

恰好六家,规范工具名(STR-002):`claude-code / codex-cli / qoder-cli / copilot / opencode / hermes`。

- 保留并适配:`claude-code` / `codex-cli` / `qoder-cli` / `opencode`(既有 `*_available/_list/_pack` 适配器,pack 改目录写入)。
- 新增探测式适配器:`copilot` / `hermes`——`available()` 按已知候选路径探测;无落盘 → 声明"该平台会话存储未探测到",退出码 4;MUST NOT 臆造 pack 行为(FR-010)。
- 移除零残留:`qwen-code` / `qoder`(IDE)/ `qoderwork` / `oh-my-pi` / `kimi-code` / `codex-app` 的适配函数、辅助函数、路径常量、文档与示例、`PARSERS` 注册、`--tool` choices 全部删除;全文扫描这六个标识计数为 0。

## 2. 产物形态(FR-008,zip → 目录)

```text
.session-export/<name>/
├── main.<原生扩展名>      # 主记录(宿主原生形态)
├── subagents/             # 子代理日志(宿主有则导出)
├── state/                 # 状态目录与段日志(宿主有则导出)
├── large-results/         # 超大工具结果(既有分段机制迁移)
├── request-ids.jsonl      # 仅可提取者(claude-code 等,既有能力面保持)
├── session-meta.json      # 元信息机读形态(描述文档契约 §2)
└── SESSION.md             # 会话描述文档(描述文档契约)
```

- 目录名 = `--name`(命令面传入);导出根固定 `.session-export/`。
- 原子 zip 机制(`_open_zip_atomic`/`_commit_zip`/`_abort_zip`)随形态迁移移除,不保留双形态。
- 内容面不削弱(FR-011):既有 `_pack_main_plus_sibling` 的每类内容 MUST 在目录形态有对应落点;缺失类显式缺省(不造假目录)。

## 3. 定位机制(FR-009,保持)

- 自动识别优先级(env → 进程祖先 → 偏序)保留,候选面收敛为六家。
- `--verify <text>`(用户最近一句内容)跨工具重定位保留。
- `--session <id>` 显式定位、`--tool <name>` 显式指定保留;`--tool` choices = 六家规范名。
- 新增 `--name <name>` 必填;缺省 → 退出码 2。

## 4. 通用化(FR-007)

- 移除 SKILL.md §1「技能使用上报」段(`a1 skill report ...`)与 frontmatter `x-source` 标记。
- 调用段脚本路径探测仅保留六家对应技能目录 + `CLAUDE_SKILL_DIR` 通用环境变量。
- 无网络调用、无外部凭证——契约测试以全文扫描断言(无 `http://`/`https://` 出站调用、无 aone-open 标识)。
- 跨平台解释器探测纪律(bash/PowerShell 两组、`-V` 实跑挑选)保留。

## 5. 只读纪律(FR-016)

- 导出对宿主会话存储只读:不写、不删、不改权限;集成测试断言存储文件导出前后字节一致。
- 不改 `.gitignore`;不代用户决定导出目录入库与否。

## 6. 退出码(FR-009,五值保持)

| 码 | 含义 |
|----|------|
| 0 | 成功(stdout 打印导出目录绝对路径) |
| 2 | 参数无效(含缺 `--name`、`--session` 为空、`--name` 文法越界) |
| 3 | 当前项目没有匹配会话 |
| 4 | 没有任何支持的工具可用(含 copilot/hermes 探测无源的单工具场景);或前置检查失败 |
| 5 | IO 或 SQLite 错 |

## 7. Contract / Integration Test Pins

- 支持矩阵收敛:`PARSERS` 键集合 == 六家规范名;被移除六标识全文计数 0。
- 目录产物:构造 jsonl 夹具驱动 export.py,断言目录布局逐节(main/subagents/state/large-results/request-ids/meta/SESSION.md 的存在性按夹具内容)。
- 定位回归:既有 `--verify`/`--session`/`--tool` 行为在保留四家上与改造前一致(同夹具前后对照)。
- 只读:夹具存储导出前后 hash 一致。
- 探测式适配器:候选路径全缺 → 退出码 4 + stderr 含"未探测到"声明。
