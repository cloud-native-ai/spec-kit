# 会话获取方法对比:export-session 技能 vs spec-kit 证据采集(session 泳道)

> 日期:2026-07-29
> 对比对象:A = `export-session` 技能(v1.1.0,`/cws_work/export-session.zip`,单文件 `scripts/export.py` 1640 行);
> B = spec-kit 证据基础设施(`scripts/js/better-harness/session-analysis/` + `evidence-utils.py` session 泳道)
> 结论速览:**两者目标不同**(A 归档原文 zip,B 产出规范化证据),但在"如何找到会话"这一共同底层问题上,A 在 5 个具体技术点上明显更强,B 在规范化/隐私/合同上独有。文末给出 6 项可落地的优化项(按价值排序)。

## 1. 定位差异(先说明,避免错比)

| | A export-session | B evidence(session 泳道) |
|---|---|---|
| 目的 | 把**当前会话的原始记录**打包 zip(主 jsonl + subagent 日志 + 状态目录 + 大工具结果 + requestId) | 从**历史会话**提取结构化执行证据(Task Episode、工具失败、返工信号)→ findings.json |
| 输出 | 原文 zip(人/工具可读归档) | 七态证据条目(机器合同,消费者中立) |
| 视角 | 向后看"这一次" | 向后看"这一批" |
| 隐私 | 原样打包(含原文) | 脱敏双闸(语义面片,不出原文) |

共同底层问题:**多 AI 工具 × 多项目目录 × 多种存储格式下,如何精确找到"属于本工作区的会话"**。以下对比聚焦于此。

## 2. 会话获取方法逐项对比

### 2.1 项目目录 → 工作区的归属判定(核心差异)

| | A | B |
|---|---|---|
| 方法 | **读文件内的真实 `cwd` 字段**精确匹配(`_read_cwd_from_jsonl`,前 200 行窗口);彻底规避目录名编码差异 | **workspace → slug 目录名变体**(`workspaceToClaudeSlugVariants` 等),按目录存在性/命名匹配 |
| 脆弱性 | 几乎无(cwd 是会话自身记录的事实) | 高:本批已实证——claude slug 规则漏了下划线(`/cws_work` → 实际目录 `-cws-work`),导致真实落盘 0 发现;每个平台都要猜准编码规则 |

**B 当前现状**:qoder/claude/codex/cursor/opencode 全部用 slug 变体探测(`platforms/*.mjs` 的 `workspaceToXSlugVariants`)。

### 2.2 "当前会话"识别(A 独有,B 几乎空白)

| 因子 | A 的实现 | B 的现状 |
|---|---|---|
| 客户端注入 env | `CLAUDE_(CODE_)SESSION_ID`、`CODEX_THREAD_ID/SESSION_ID` 逐个取 | 仅 claude 读 `CLAUDE_SESSION_ID`、opencode 读 `OPENCODE_SESSION_ID`;codex 无 |
| 属主 pid 命中进程祖先链 | Qwen `<sid>.runtime.json` 的 pid ↔ `ps` 祖先链(`_owner_pid_current`) | 无 |
| tty 终端关联 | oh-my-pi `terminal-sessions/<tty>` 反查(`_my_ttys`) | 无 |
| IDE 状态库 | Qoder `workspaceStorage/<hash>/state.vscdb` 的 `aicoding.chat.tabs` 精确活动会话 + 每会话真实模型(`chat.modelConfig.session.<sid>`) | qoder 适配器无 IDE 侧读取 |
| 内容校验重定位 | `--verify <文本>`:末条文本校验,未命中跨工具重定位(`_verify_or_relocate`) | 无 |
| 兜底 | 内容时间戳最新 + (mtime, sid) 确定性排序 | 时间窗过滤 + lastSeen 排序(等价,但无"当前"概念) |

### 2.3 工具覆盖与存储格式

| 工具 | A | B |
|---|---|---|
| qoder(Qoder IDE) | transcript/*.jsonl + state.vscdb 模型 | ✓(上游完整) |
| Qoder CLI | 顶层 *.jsonl + 同名状态目录 + logs/sessions 段日志 + requestId | ✓(上游完整) |
| claude | jsonl + subagents/ + tool-results/ + requestId | ✓(P7-a2 核实补齐) |
| codex-cli / codex-app | **state_5.sqlite**(threads 表,source=cli/exec vs vscode 区分 CLI/App)→ rollout jsonl + **thread_spawn_edges 递归子 agent** | ✓(上游;rollout 遍历) |
| **opencode** | **`~/.local/share/opencode/opencode.db`(SQLite)**:session/message/part 表,**parent_id 递归子会话**,模型取 message.data.modelID | **JSON 文件布局**(project/<id>/storage/session/{info,message,part}),P7-b 自研——**未覆盖 SQLite 形态** |
| qwen-code | chats/*.jsonl + runtime.json(pid) + fork 派生 | ✗(P7-c 待做) |
| oh-my-pi / qoderwork | ✓ | ✗(不在矩阵) |

**重要格式发现**:opencode 存在**两种并行存储形态**——SQLite(`opencode.db`)与 JSON 文件布局(`storage/`)。B 的 P7-b 适配器只实现了后者;A 的实现证明前者真实存在于部署中。

### 2.4 子会话 / subagent 处理

| | A | B |
|---|---|---|
| claude | 打包 `{sid}/subagents/*` 目录 | `isSidechain` 标志(事件内嵌) |
| codex | SQLite `thread_spawn_edges` 递归收集全部后代 rollout | 单 rollout 遍历(未显式递归) |
| opencode | `parent_id` 递归(WITH RECURSIVE CTE) | 无父子概念(逐文件扫描,天然含全部会话) |

### 2.5 运行时元数据(模型/requestId)

| | A | B |
|---|---|---|
| 模型识别 | 三级回退:state.vscdb 真实模型 > transcript > audit 档位别名;opencode 取 message.data.modelID | claude/codex 事件内 model 字段;qoder 有 model-pricing.mjs;**未用 IDE state.vscdb**(Qoder 会话模型精度弱) |
| requestId | `chatcmpl-<uuid>` 剥前缀 → request-ids.jsonl(可追溯到大模型接口) | 无 requestId 概念 |

### 2.6 工程细节

| | A | B |
|---|---|---|
| 探测精度 | cwd 精确匹配;单工具故障不拖垮识别(try/continue) | doctor 三态探测(P7-a1,目录+内容二级校验) |
| 单文件 vs 分层 | 1640 行单文件 Python(stdlib-only) | Node 引擎 37+ 文件 + Python 编排 |
| 原子写 | zip `.part` + os.replace 原子提交 | findings 直接写(无原子语义) |

## 3. 各自优劣总结

**A 更强**:
1. 会话归属判定更鲁棒(cwd-in-file 免猜编码)
2. "当前会话"识别体系完整(env/pid/tty/IDE 状态库/内容校验五因子)
3. opencode SQLite 形态覆盖 + 子会话递归
4. 模型/requestId 元数据更全(IDE state.vscdb、百炼 requestId)

**B 更强(且 A 完全没有)**:
1. 规范化证据合同(七态、findingsDigest、泳道状态)——产出可被机器消费,不只是归档
2. 隐私纪律(脱敏漏斗 + 白名单双闸;session 泳道必带 privacyNote)
3. 证据语义(Task Episode 归并、返工/失败信号、recurrence 聚合)——从"记录"到"观察"
4. 五泳道编排与显式降级(不只是 session:project/assets/runs/feedback)

**互盲区**:A 没有脱敏与结构化;B 没有"当前会话"与 SQLite opencode。两者可互补:A 的归档是 B 的原始数据源之一,B 的规范化是 A 归档的下游消费。

## 4. 对 spec-kit 的优化建议(按价值排序)

### P1 — 会话归属判定改用"文件内 cwd 字段"为主、slug 变体为备
- **问题**:B 的 slug 变体法已在 claude 上实证过一次缺陷(P7-a2 下划线规则),每平台规则不同、易腐化。
- **方案**:在 `platforms/*.mjs` 的 `discoverSessions` 探测阶段,先读项目目录下首个可解析 jsonl 的顶层 `cwd` 字段(或 opencode info JSON 的 `directory`)与 scope.workspace 精确比对;slug 变体仅作"无 cwd 字段时"的 fallback。claude.mjs 已有 `probeTranscript` 读 cwd(workspaceMatch),可推广到 qoder/codex/cursor。
- **收益**:消除一整类目录编码缺陷;降低新平台适配器的编码猜测成本。
- **位置**:`scripts/js/better-harness/session-analysis/platforms/*.mjs` + provider-runner。

### P2 — opencode 适配器增加 SQLite(opencode.db)数据源
- **问题**:P7-b 仅实现 storage JSON 布局;A 证实 `~/.local/share/opencode/opencode.db`(session/message/part 表)真实存在,且是"会话→子会话"的权威关系源(parent_id)。
- **方案**:`platforms/opencode.mjs` 的 `discoverSourceRoots` 增加 `opencode-sqlite` 根(node 侧用 `node:sqlite` 或降级标记 unavailable——注意 node:sqlite 需 Node 22.5+);`readSession` 支持从 DB 还原 message/part;父子递归生成子会话条目。
- **收益**:opencode 覆盖真实部署形态;子会话信号(与 claude isSidechain 对齐)。
- **附注**:doctor 的 opencode 探测路径补 `~/.local/share/opencode/opencode.db` 存在性(现仅目录)。

### P3 — "当前会话"识别因子下沉到适配器 `currentSessionId()`
- **问题**:改进类技能在会话内自审时,需要"就是这一个会话"的精确性;B 目前只有 claude/opencode 各读一个 env 变量。
- **方案**:(a) 统一读 A 的 env 清单(`CLAUDE_(CODE_)SESSION_ID`、`CODEX_THREAD_ID/SESSION_ID`);(b) qwen 适配器(P7-c)直接复用 A 的 runtime.json pid ↔ 祖先链方法(`_owner_pid_current` 逻辑,node 侧 `process.ppid` 链);(c) oh-my-pi 类工具的 tty 反查备用。
- **收益**:`collect-evidence --target 当前会话` 场景从"最近一个"升级为"精确这一个"。

### P4 — qoder 模型识别引入 IDE state.vscdb
- **问题**:Qoder IDE transcript 不记模型,audit 仅档位别名——B 的 model-pricing/模型信号在 qoder 上精度受限。
- **方案**:移植 A 的 `_qoder_workspace_db` + `_vscdb_get` 逻辑(cwd → workspaceStorage hash → state.vscdb → `chat.modelConfig.session.<sid>`),作为 qoder 模型识别的第一优先级(>transcript>audit)。
- **位置**:`platforms/qoder.mjs` 的模型归一环节。

### P5(可选)— findings 增加 requestId 级引用
- **问题**:B 的 evidenceRefs 目前是会话哈希/相对路径;缺乏到大模型接口级(requestId)的可追溯引用。
- **方案**:qoder-cli/qwen 等 `chatcmpl-<uuid>` 形态的产品,在 episode facts 的 evidenceRef 中附带 requestId(仍不可逆,符合隐私纪律)。
- **价值**:与百炼侧日志对账时可直接关联(对 Outcome-supported 类纵向证据尤其有用)。

### P6(已有,保持)— 原子写与探测三态
- A 的 zip 原子提交(.part + rename)印证了一个可借鉴的工程习惯;B 的 findings.json 为一次性写后只读,若未来支持中断恢复可考虑同法。**doctor 三态探测 B 已实现(P7-a1),与 A 的"目录≠有会话"精神一致,保持。**

## 5. 反向借鉴(A 可从 B 学)

- 归档 zip 若需对外分享,应过 B 的脱敏漏斗(privacy-safe-text / semantic-facets);A 当前原样打包含原文,适合本地不适合外发。
- A 的九工具清单与 B 的八工具支持矩阵可互相参照:A 有 oh-my-pi/qoderwork(B 矩阵外),B 有 copilot/iflow(A 未支持)。

## 6. 证据清单

| 项 | 路径 |
|---|---|
| A 技能源 | `/cws_work/export-session.zip` → `SKILL.md` + `scripts/export.py`(1640 行) |
| A cwd 定位 | `export.py:50-99`(`_read_cwd_from_jsonl` / `_list_jsonl_projects`) |
| A 多因子锁定 | `export.py:1220-1419`(env/pid/tty/IDE state.vscdb/--verify) |
| A opencode SQLite | `export.py:894-1012`(`OPENCODE_DB`、parent_id 递归、modelID 提取) |
| B slug 变体法 | `scripts/js/better-harness/session-analysis/platforms/*.mjs`(`workspaceToXSlugVariants`) |
| B claude cwd 探测(已部分实现) | `platforms/claude.mjs:257-265`(`probeTranscript`/`isWorkspaceMatch`) |
| B 脱敏与合同 | `skills/collect-evidence/references/` + `.specify/specs/034-evidence-infra/contracts/` |
