# Data Model: 无人值守 SDD 循环驱动机制（Feature 058）

> 本特性零可执行运行时代码——本文件定义的 8 个实体中，E-1 是**交付物**（skill 手册本体），E-2…E-8 是 skill 在运行期于宿主/目标项目侧** prescribe 落盘的制品 schema**（格式与程序由 skill 内容固化，本文件是它们的规划期定义点）。字段命名以 skill 内联文本为准；运行期取值示例来自需求简报 §3–§5 已验证形态。

## E-1 Skill 手册（Loop Driver Skill）

机制唯一承载（FR-001/FR-002）。

- **落位**：框架源 `skills/external/sdd-loop-driver/`（SKILL.md + `references/dispatch-recipes.md` + `references/stage-prompts.md`）；运行时镜像 `.specify/skills/sdd-loop-driver/`（sync-mirrors 平铺投影，禁手改）。
- **frontmatter schema**（4 字段，先例 create-skills/git-workspace 逐字实测）：

| 字段 | 值 | 约束 |
|------|----|------|
| `name` | `sdd-loop-driver` | 与 [[STR-003]] 逐字相等 |
| `description` | 一段长描述 + 触发词 | 触发词含「使用SDD开发模式」「无人值守」「sdd-loop-driver」（一遍性入口话术的检索面，G4） |
| `skill_id` | `<SKILL:.specify/skills/sdd-loop-driver/SKILL.md>` | external 平铺路径形态 |
| `classification` | `external` | clarify 裁决（依赖轴）；词面张力注解写在 frontmatter 后正文首行 |

- **自包含规则**（FR-002/FR-025）：五类内容（骨架/五机制/变体/纪律/三硬需求运行规则）全部内联；框架文档与 shared 底稿仅可作「撰写底稿/背景」注解出现，MUST NOT 构成运行时必读依赖；「手动放置即可用」。
- **关系**：消费 [[STR-001]]（哨兵后缀）、[[STR-002]]（阶段链）、[[STR-003]]（机制标识）；引用既有契约 `subagent-definitions.md` 的观测要求时以内联操作要点形态（FR-011）。

## E-2 项目线（Project Line）

一次无人值守推进的执行单元；多线并行时彼此隔离（FR-020/FR-021）。

- **身份字段**：line label（入口声明或派生，稳定、跨阶段不变）。
- **参数字段**（全部入口化，FR-003 零硬编码）：登录别名、登录用户（如 root → `su develop` 的运行身份）、项目路径、子代理 CLI（缺省 qodercli，`DISPATCH_CLI` 可覆盖）、终态权威文档路径、断点声明（可空 → 触发探测）。
- **运行字段**：当前阶段、已试次数、断点判定结果、日志文件指针、状态指针。

## E-3 断点（Breakpoint）

目标项目当前所处 SDD 阶段的判定结果（FR-005/FR-006 产出）。

- **取值域**：[[STR-002]] 六阶段之一，或「review 后仅剩合并」收尾态（G6 收尾场景）；或 `undetermined`（探测失败 → 停线上送，Edge Case 1，禁止猜测）。
- **证据字段**：`git branch --show-current` 输出、`git log --oneline -3` 输出、`.specify/specs/` 目录清单、终态权威文档存在性。
- **生命周期**：入口/重入时探测一次 → 写入 E-6 状态脊 → 作为 U2 派发起点的输入。

## E-4 阶段提示词文件（Stage Prompt File）

单阶段完整指令的落盘文件（FR-007/FR-008）。

- **命名与落位**：`prompt-<line>-<stage>.md`，落运行用户家目录（已验证形态：`/home/develop/prompt-<项目>-<阶段>.md`；路径参数化，FR-003）。
- **三段骨架 schema**（固定，skill 固化）：
  1. 背景与权威文档：终态文档路径 / 宪法 / 上一阶段提交号；
  2. 执行要求（G5 默认纪律）：直接执行不要确认；访谈式问题自行裁决并记录假设；只提交本特性产物；既有脏文件不提交不还原；不要 push（除非明确授权）；
  3. 完成尾标要求：最后一行输出 `<STAGE>-DONE`（[[STR-001]]）；**回传契约**：最后一行 = 完成哨兵**或**显式异常行，二者皆无 = 卡死信号（宪法 XVI 派发注入义务的操作化，C-13 钉死）。
- **写入方式**：heredoc 经 ssh 写远端（已验证形态）；不内联进命令行。

## E-5 Runner 脚本（Runner Script）

单阶段子代理执行的包装（FR-010）。

- **命名与落位**：`run-<line>-<stage>.sh`，运行用户家目录。
- **内容模板**（已验证形态）：`cd <project-dir> && <CLI> -w <project-dir> --permission-mode auto -p "$(cat <prompt-file>)"`。
- **派生规则**：下一阶段 runner 由上一阶段 runner 经文件名替换派生（如 sed 替换提示词文件名）——runner 形态跨阶段恒同。
- **执行形态**：`ssh <alias> "su - <run-user> -c 'bash <runner>'" > <本地日志> 2>&1 &`（后台，一线一连接，FR-011）。

## E-6 线状态（Line State）

状态脊实体（FR-019）——跨周期唯一记忆，零上下文可接手。

- **落位**：每线一份，随线命名；由 skill 固化写入时机与格式（markdown 定长字段表）。
- **字段**：line label、当前阶段、已试次数、断点判定（E-3）、最近证据指针（日志路径 / 提交号 / 校验结论引用）、卡死状态（stalled/retrying/running/done）。
- **程序规则**：**先写状态后派发**（U2/U4/U5 三个转移点强制落盘）；续环（U4→U2）与重入（任意时刻）都从状态脊恢复，MUST NOT 依赖会话记忆。
- **校验规则**：重试计数与重试上限（缺省 2）比对、阶段超时（缺省 90 分钟）计时基线由此文件承载（数值缺省值 informed guess，入口可覆盖，FR-017）。

## E-7 校验结论（Verification Verdict）

独立校验步骤对单阶段完成判定的可复现结论（FR-015/FR-016）。

- **判定条件**（多条件同时成立方判完成）：[[STR-001]] 尾标出现在本次阶段输出末尾（必要条件；日志正文回显不算——Edge Case 7）＋ 产物核验（git log 新增该阶段提交、该阶段 spec 文件存在性）＋ 纪律合规抽查（E-4 第 2 段未被违反）。
- **校验者约束**：校验者 MUST NOT 是该阶段执行子代理（循环执行侧自身或另行派发的校验代理）。
- **可复现规则**：结论含逐项证据指针，第二位复核者可独立复现；伪完成判未完成。

## E-8 收尾汇总（Final Summary）

全部线收束后的终态报告（FR-014）——无人值守结束于一份可处置的汇总而非沉默。

- **逐线字段**：line label、终态阶段、合并结果（git 状态判定，FR-013：特性分支提交已包含于集成分支且无未合并/冲突残留）、遗留异常与证据指针。
- **程序规则**：全部线到达终态（done 或 stalled-with-report）后产出一份汇总；合并/push 类收尾动作维持确认门控破坏性分类（缺省本地合并，push 须入口显式授权）。

## 关系总览

```text
E-1 Skill 手册（承载）
 └─运行期实例化──> E-2 项目线 ──探测──> E-3 断点
                     │  └─派发──> E-4 阶段提示词文件 ──包装──> E-5 Runner 脚本
                     │  └─每转移点落盘──> E-6 线状态（状态脊）
                     │  └─校验──> E-7 校验结论
                     └─收束──> E-8 收尾汇总
```

## 校验规则汇总（V-1…V-6）

- **V-1**: E-1 frontmatter 恰为 4 字段且 `classification: external`、`name` == [[STR-003]]（契约测试钉死）。
- **V-2**: E-4 三段骨架缺一段即派发非法（skill 固化骨架检查程序）。
- **V-3**: E-6 在 U2/U4/U5 三转移点 MUST 已更新（先写状态后派发；契约测试钉死程序文本）。
- **V-4**: E-7 判定条件任一不成立 → verdict = fail（尾标在而产物缺 = fail，SC-003 变异演练载体）。
- **V-5**: E-8 逐线字段齐备（缺遗留异常列即汇总非法）。
- **V-6**: 全部取值示例（路径/用户/CLI）为参数化占位，skill 文本零硬编码（FR-003）。
