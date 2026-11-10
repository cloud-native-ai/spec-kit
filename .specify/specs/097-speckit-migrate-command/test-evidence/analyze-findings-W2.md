# Analyze findings — Wave 2（097-speckit-migrate-command）

- **Stage**: analyze（并发波 W2）· **Date**: 2026-11-10 · **Round**: 1（全严重度）
- **Read domain**: `plan.md`、`data-model.md`、`quickstart.md`、`contracts/migrate-cli.md`、`contracts/migrate-engine.md`、`contracts/migrate-template.md`（6 文件）
- **Method**: analyze-artifacts passes A–I，只读检测，无修复、无产物改动
- **Not evaluated here（读域外，本波不作结论）**: requirements.md 对照、tasks.md 覆盖、checklists H pass、clause-coverage accountant（skill 步骤 3）、feature registry 联动（G pass 外部证据）——由本阶段汇总波/协调方覆盖
- **Summary**: CRITICAL 0 · HIGH 2 · MEDIUM 3 · LOW 8（共 13）

## Findings

| ID | Severity | 锚点 | 事实（一句话） | 建议归属 |
|----|----------|------|----------------|----------|
| W2-01 | HIGH | `contracts/migrate-engine.md:15`；`data-model.md:121,124` | C-2 声明消费 `sync-mirrors.py --check` 的「六个镜像对」，而 E-8 在五维中只按维度枚举了五个镜像对（templates/skills/agents + scripts/shared），两处必有一处与 `sync-mirrors.MIRROR_PAIRS` 的实际计数不符。 | 以 `sync-mirrors.MIRROR_PAIRS` 为唯一 owner 复核后修正 C-2 计数或 E-8 补漏的镜像对；校验波需实读 owner 列表定案。 |
| W2-02 | MEDIUM | `data-model.md:41,54-70`；`contracts/migrate-cli.md:62` | E-2 称 `workspace` 绝对路径「回执中记录」、C-4 把回执中的 `workspace` 列为易变字段，但 E-3 的 Receipt 字段表没有 `workspace` 字段（C-4 的 json 包络同样无此键）。 | data-model E-3 补字段（或同步修正 E-2/C-4 措辞）。 |
| W2-03 | MEDIUM | `data-model.md:59`；`contracts/migrate-engine.md:77` | Receipt `status` 枚举含 `aborted`，但全文未定义任何写 `aborted` 的触发条件（正常收束写 `completed`、崩溃留 `running`），且 `outcome=blocked` 的 apply 回执应记何种 `status` 也未声明。 | data-model E-3 定义触发或删 token；engine C-7 对齐。 |
| W2-04 | HIGH | `data-model.md:100`；`contracts/migrate-cli.md:50,77`；`contracts/migrate-template.md:26` | `error` 在 E-5 与 C-3 中被列为 outcome 并给出 exit 2，但 C-4 的 json `outcome` 枚举、C-6 的「四类结局」、T-2 的转述清单与 `plan.md:51`（XIX）均只含 clean/planned/applied/blocked 四类——`--format json` 在 error 情形是否输出包络、是否携带 `outcome=error` 无定义。 | migrate-cli C-3/C-4/C-6 统一（显式声明 error 不入包络，或补入枚举），T-2 与 plan XIX 跟随。 |
| W2-05 | MEDIUM | `data-model.md:23,121,124`；`contracts/migrate-engine.md:27-36` | E-1 的 `mechanism` 枚举预留了 `mirror-engine`，但 C-3 处置映射与 E-8 处置来源从未赋予该值，导致框架源模式下经 `sync-mirrors --write`/`generate_commands` 写入的项在回执 `items[].mechanism` 中应记何值未定义。 | migrate-engine C-3 增补框架源写入行（mechanism=mirror-engine），E-8 处置来源对齐。 |
| W2-06 | LOW | `data-model.md:119`；`contracts/migrate-engine.md:62-65` | 两处 Markdown 表结构破损：E-8 的表头行与标题写在同一行（第 119 行），C-5 的复用边界表被「链接修复的职责说明」段落从中截断、后三行（镜像与生成副本、goal/team、周期治理）落在表外。 | Phase 1 制品作者修复排版，不改语义。 |
| W2-07 | LOW | `plan.md:33,153-166` | WP 表 14 行的 FR 列覆盖 FR-001…FR-025 中除 FR-004、FR-013 之外的全部编号，而 Constitution Check 声称 25/25 可回溯（矩阵在被引用的 feature-ref.md，本波读域外）；其中 FR-013 的静止指针是 E-9 定义的显式交付物却无 WP 落点。 | plan WP 表补 FR-013 归属（如 WP02/WP06），或由 feature-ref 矩阵显式标注非 WP 承载。 |
| W2-08 | LOW | `plan.md:100,199`；`quickstart.md` 全篇 | plan 的目录树注释称 quickstart 为「4 个用户旅程场景」，但同文件 Phase 1 汇总与 quickstart 实际内容均为 6 个场景（0–5）。 | plan.md 目录树注释。 |
| W2-09 | LOW | `plan.md:177`；`quickstart.md:68` | 跨引用失效/歧义：EP-006 指向 `contracts/migrate-engine.md`「§ 平台降级」而该契约无此章节（内容散见 C-3/C-4）；quickstart 场景 4 的「`refuse` 语义如 C-3」未限定文件，而 migrate-cli 与 migrate-engine 各有一节 C-3。 | plan EP-006 改指 C-3/C-4；quickstart 引用补文件名。 |
| W2-10 | LOW | `contracts/migrate-engine.md:3,23` | 契约头部的 Spec 行声明覆盖 `FR-005…FR-018、FR-023…FR-025`，但正文 C-2 两处引用 FR-020（不在该区间内），头部枚举与正文引用不一致。 | migrate-engine 头部补 FR-020 或复核正文引用。 |
| W2-11 | LOW | `plan.md:155`；`data-model.md:30` | 去重键不一致：WP03 写「按 target 去重」，E-1 的唯一性规则是 `(dimension, target)` 唯一，两入口若按不同键去重会产生不同计划（T-3 等价性风险）。 | plan WP03 对齐 E-1 的键。 |
| W2-12 | LOW | `data-model.md:139-143`；`contracts/migrate-cli.md:83-86` | 「干跑零写入」「先归档后替换」不变量在 data-model I-1/I-2、migrate-cli C-7、plan Constraints 与 quickstart 多处重述且无唯一 owner 声明；I 集合（5 条）与 C-7 集合（4 条）成员不同，后续修订易漂移。 | 声明 data-model 不变量为 owner，C-7 标注为测试投影（或反向）。 |
| W2-13 | LOW | `quickstart.md:10-16` | 场景 0 的实测在仓库外 ad-hoc 目录 `~/tmp/speckit-migrate-quickstart` 执行，与 AGENTS.md 摘要的临时目录纪律（sanctioned temp root、禁 ad-hoc 目录）不一致。 | quickstart 作者：实测记录与建议目录改用已登记临时根，或明确表述为用户自选目录。 |

## 零发现声明（带证据）

- **Pass I（Decision Tension）**: T-001/T-002 字段齐备（decision / antithesis / binding_constraints / discriminating_evidence / expected_sacrifice / revision_trigger），见 `plan.md:64-84` —— 无 finding。
- **Constitution Check**: 22 行全部 Pass，未发现 CRITICAL 级宪法冲突（`plan.md:29-56`）。
- **维度封闭集与顺序**: E-1 token 序、E-8 映射序、engine C-1 三处一致（`data-model.md:18,119-125`；`contracts/migrate-engine.md:9`）。
- **退出码数值**: E-5 与 cli C-3 五行数值一致（clean 0 / planned 1 / applied 0 / blocked 3 / error 2）；枚举边界问题见 W2-04。
- **处置值域**: C-3 全部 disposition 落在 FR-014 六值（write / replace / archive / refuse / blocked / converged），与 plan「六值处置」一致（`contracts/migrate-engine.md:27-36`；`plan.md:25`）。
- **双键确认**: 四处表述一致（`plan.md:24`；`contracts/migrate-cli.md:67-72`；`contracts/migrate-engine.md:67-72`；`quickstart.md:50-60`）。

## 备注

- rerun delta：不适用（本波为 Round 1 检测，读域内无更早 analyze 报告引用）。
- W2-01 与 W2-04 为 HIGH，建议校验波以 `sync-mirrors.MIRROR_PAIRS` 实值与 requirements FR-019 实读分别定案后再进 implement。
