# Contract: 算子库物理契约 `.specify/derive/moves.md`(需求 048 / Feature 049)

**Requirement → Feature**: `048-derive-command` → Feature 049 Derivation Command
**交付物**: `.specify/derive/moves.md`(项目级累积算子库,引擎独写,git 跟踪)
**概念真源**: `shared/definitions/derivation-definitions.md` §Reasoning Move / §Move Library / §Projection, Not Copy —— Move Record 的七字段语义、库的选址理由、三条防复写机制的**定义点**。本契约 MUST NOT 复述其字段含义,只规定**可被程序解析的物理形态**与**写入权状态机**。
**消费方**: `scripts/python/derive-utils.py`(`moves-add` / `moves-list` / `validate` / `stats`)、`contracts/derivation-model.md` §8、`templates/commands/derive.md`、`tests/unit/test_derive_moves.py`、`tests/contract/test_derive_move_library.py`

## 1. 物理形态(引擎按位置解析)

- C-1 文件 MUST 为单一 Markdown 文件,路径恒为 `.specify/derive/moves.md`([[STR-006]]),位于 `.specify/derive/` **根**而非 `<topic-slug>/` 内(库跨主题,选址理由见概念锚 §Move Library,引用不复述)。MUST NOT 分裂为「一算子一文件」或另建索引文件。
- C-2 文件 MUST 恰含一张表。表头行与分隔行 MUST 逐字为:

```markdown
| move_id | name | inference_form | prevents | applies_when | anchor | status |
|---------|------|----------------|----------|--------------|--------|--------|
```

- C-3 引擎 MUST **按位置**解析单元格(第 1 列 = `move_id` … 第 7 列 = `status`),故列序 MUST NOT 变更、MUST NOT 增列、MUST NOT 减列。任何列序调整都是破坏性变更,须同时改本契约与引擎。
- C-4 列切分 MUST 用正则 `(?<!\\)\|`(不切被反斜杠转义的竖线);每数据行 MUST 恰解析出 **7** 个非空单元格,否则 error `moves-library-hand-edited`,子因 `row-shape`。
- C-5 数据行 MUST 单行:单元格内 MUST NOT 含换行。多行内容 MUST 由写入方压成一行(以 `;` 分隔子句)。理由:引擎逐行解析,跨行单元格会把一行变成两条残缺记录,而残缺记录的 ID 会被误判为单调性违例。
- C-6 单元格内的字面竖线 MUST 写为 `\|`;`anchor` 列的多个来源 MUST 以 `, ` 分隔,且每项 MUST 为**限定形式** `<topic-slug>.S-<nnn>`(概念锚 §Move Record:`M-` 项目级而 `S-` 每主题,裸写 `S-003` 跨主题不可解析),例 `topic-a.S-001, topic-b.S-007`;不匹配该语法(裸 `S-<nnn>`、含 `#` / `/`、slug 段不合 `contracts/derive-engine.md` C-27 的限定式)→ error `moves-library-hand-edited`,子因 `anchor-form`。`inference_form` 中的命名槽位 MUST 以反引号包裹(`P`、`D`),这是 C-14 槽位同构归一化的输入形态,也是概念锚 §Litmus tests 2「槽位测试」的机械抓手。
- C-7 表格之前 MUST 存在标题行 `# Reasoning Move Library` 与引擎写入标记行,后者 MUST 逐字为:

```markdown
<!-- engine-written: derive-utils.py --action moves-add is the only writer; hand edits are DETECTED by validate, never silently accepted -->
```

  标记缺失或被改写 → error `moves-library-hand-edited`,子因 `header-marker-missing`。该标记是 A13 的机械抓手:它让「独写者」在文件自身上留痕,而不只存在于代码里。
- C-8 数据行 MUST 按 `move_id` 升序连续排列,中间 MUST NOT 有空行、注释行或第二张表。文件末尾 MUST 恰以一个换行结束。

## 2. 身份语法与单调发放

- C-9 `move_id` MUST 匹配 `^M-\d{3,}$`:零填充至**最少** 3 位,第 1000 条起自然增宽为 4 位(`M-1000`),MUST NOT 在第 999 条处报错或回绕。
- C-10 `move_id` MUST **项目级**(跨全部 topic 档案)单调发放、永不复用、永不重编号。发放规则:下一个 ID = 库中现存最大编号 + 1。库为空时首个 ID MUST 为 `M-001`。
- C-11 发放 MUST 由 `moves-add` 独占(`contracts/derive-engine.md` C-24/C-26)。库的单调性已被破坏(存在降序、跳号后的回填、重复 ID)时 `moves-add` MUST 拒绝发放并退出码 2,子因 `id-not-monotonic` / `duplicate-id`;MUST NOT 通过重编号让追加「成功」。
- C-12 `validate` MUST 独立复检 ID 不变量(不依赖写入时的自律):语法、严格递增、无重复。三者任一不成立 → A13 判 `fail`(`contracts/derivation-model.md` C-40)。

## 3. 去重键与拒绝-返回既有 ID

- C-13 **去重键 = 归一化 `inference_form`**,归一化函数 MUST 复用 `contracts/derivation-model.md` C-22 的 `normalize_text`(NFKC → casefold → 剥标点/符号 → 折叠空白 → 空串为 `None`)。MUST NOT 以 `name` 去重:名字是标签,同一形状可有两个好名字,以名字去重会分叉出变体。
- C-14 去重为**两级**,两级都判为重复:
  1. **精确重复** —— 归一化串相等;
  2. **近重复(槽位同构)** —— 在归一化串上再把每个槽位记号替换为字面 `<SLOT>` 后相等;槽位记号定义为「反引号包裹的记号」与「独立的单大写字母记号」(正则 `` `[^`]+` `` 与 `(?<![A-Za-z])[A-Z](?![A-Za-z])`)。
  **为何需要第二级**:概念锚只说「dedups on normalized `inference_form`」与「near-duplicate」而未定义近似;若只做第一级,同一形状换个槽位名(`P`/`D` → `X`/`Y`)就会分叉出新行,而槽位名恰恰是**不承载语义**的部分 —— 那正是本命令要抽取的可重放性所在。
- C-15 **拒绝-返回既有 ID 语义**:命中任一级重复时 `moves-add` MUST NOT 写入新行,MUST 在 `payload.duplicates[]` 返回 `{"requestIndex", "normalizedForm", "existingMoveId"}`,`payload.deduped` +1,整体退出码 **0**(拒绝是成功路径,不是错误)。运行据此把该条目的**处置**记为 `reinforced`(需带新锚点,C-19),库行的持久 `status` 不变。
- C-16 `validate` 与 `stats` MUST 复检库内**持久状态为 `active` 的行之间**不存在重复归一化 `inference_form`(两级同检);存在即 error `moves-library-hand-edited`,子因 `duplicate-form`,`payload.moves.duplicateForms` 记其计数(SC-003 要求该计数恒为 0)。**实现期修订:范围限定为 `active` 行**——C-18 允许「某形状被 supersede 后再次需要时落一条**新行**」,这天然产生一条 superseded 行与其 active 后继共享同一形状;若把复检范围扩到全部行,C-16 与 C-18 直接冲突。真正的缺陷是**两条同时可引用的行**共享形状(去重本应拒绝第二条),故范围取 `active`。

## 4. `status` 状态机与永不删除

- C-17 `status` 为**持久**封闭二值枚举 `active` / `superseded`(语义见概念锚 §Move Record);枚举外值 → error `moves-library-hand-edited`,子因 `status-not-in-enum`。运行相对处置 `new` / `reused` / `reinforced` **不是**库状态,MUST NOT 出现在该列(它们只由 `moves-add` / `stats` 的 payload 报告,见 `contracts/derive-engine.md` C-21/C-23);写入即 `status-not-in-enum`。**为何**:把运行相对值写进持久行,库会在第二次运行时自相矛盾(同一行既 `new` 又 `reused`)。
- C-18 合法迁移 MUST 恰为下表(集合封闭,未列出的迁移一律非法 → `moves-add` 退出码 2,`code: illegal-status-transition`,message 携带 `from → to`):

| from | 合法 to | 附加前置条件 |
|---|---|---|
| `active` | `active`(处置 `reused` 不写库;处置 `reinforced` 只就地增 `anchor`,见 C-19/C-20) | `reinforced` MUST 带来新锚点 |
| `active` | `superseded` | 由 `intent: supersede` 触发;写入后该算子永久不可引用(C-26) |
| `superseded` | —(**终态**) | 需要该形状时 MUST 由 `moves-add` 落**新行**,MUST NOT 复活 |

- C-19 处置 `reinforced` MUST 由 payload 提供至少一个**不在**该行现有 `anchor` 列中的限定来源引用;否则退出码 2,`code: reinforce-without-new-anchor`。**理由**:概念锚把 `reinforced` 定义为「reused 且新增了锚点」,无新锚点的 `reinforced` 就是 `reused`,允许它会让处置报告变成运行次数的虚报。
- C-20 `anchor` 列 MUST **只增不减**:更新行时引擎 MUST 取「既有 ∪ 新增」并按限定引用排序写回(先 slug 段字典序,再 `S-` 编号数值升序),MUST NOT 接受移除既有锚点的 payload。**实现期修订**:「只增不减」在当前输入 schema 下是**结构性保证**而非需要拒绝的分支——`moves-add` 的 `anchor` 字段语义是「本次要新增的引用集」(`contracts/derive-engine.md` C-28),没有任何输入形态能表达移除,写入又恒为并集,故 `anchor-removal-refused` 不可达。该 code 保留为将来若引入显式移除动词时的预留位;在那之前,任何声称触发它的测试都是错的。锚点是该算子被哪些来源展示过的证据,抹掉它等于抹掉可核查性。
- C-21 **永不删除**:`moves-add` MUST NOT 删除任何行,引擎 MUST NOT 提供任何删除/压缩/重写动作;`superseded` 行 MUST 原样保留(概念锚 §Storage:终态内容保留,使放弃它的理由仍可发现)。库 MUST 只以「追加新行」与「就地更新既有行的 `anchor` / `status`」两种方式变化。
- C-22 就地更新 MUST 保持行的列序、单行性与单元格转义(C-3…C-6),MUST NOT 重排全表、MUST NOT 重写表头、MUST NOT 触碰其他行。

## 5. 投影 vs 复写(与 A9 的接口)

- C-23 运行 MUST 经 `moves-list` 的**投影**消费库,`derive.md` 的 `## Reasoning Moves Applied` MUST 以 `M-<nnn>` 身份引用而非复制整行(FR-015)。
- C-24 当行内可读性确需拼出形状时,该复写 MUST 被标记为投影:在复写行的**紧邻上一行**放置字面 HTML 注释 `<!-- projection of moves.md#M-<nnn> -->`,且注释中的 ID MUST 与该行的 `move_id` 逐字相同。该标记是「合法投影」与「非法陈旧副本」的唯一判别物。
- C-25 A9 据此三态判定(执行细节归 `contracts/derivation-model.md` C-42,本契约只拥有物理判据):
  1. `## Reasoning Moves Applied` 中匹配 `^\| M-\d{3,} \|` 的行 = **复写行**;不含该形态、只出现 `M-<nnn>` 的行 = **裸引用**,恒合法;
  2. 复写行无 C-24 标记 → error `unmarked-move-copy`(它是一条会被下次运行信任的陈旧副本);
  3. 复写行有标记,但其 `inference_form` 单元格经 `normalize_text` 后与库中同 ID 行不等 → error `divergent-move-projection`(A9 拒绝与库分歧的复写行)。
- C-26 引用 `status: superseded` 的算子 → error `superseded-move-applied`(终态即永久不可引用;判据见 `contracts/derivation-model.md` C-43)。
- C-27 `moves-list` 的投影 MUST 是**摘要优先**输出:每行只带七字段的投影值,`payload.projection` 恒为 `true`;引擎 MUST NOT 在投影里附带库原文、git 历史或跨行统计明细。

## 6. 读取升级与小文件阈值

- C-28 有界整读 `moves.md` 仅在文件落在**小文件阈值**内时合法;该阈值的唯一定义点是 `shared/guidelines/token-efficiency.md` §小文件阈值 —— 本契约与命令模板 MUST 引用它,MUST NOT 复述其数值。超过阈值时 `moves-list` 投影为**强制**读取路径。
- C-29 引擎 MUST 把该阈值钉为模块常量 `SMALL_FILE_MAX_LINES` 与 `SMALL_FILE_MAX_BYTES`(取值逐字取自 C-28 所指的定义点),并由漂移守卫测试断言二者与该节文本一致 —— 与禁用论证集同一纪律(`contracts/derivation-model.md` C-16):概念文档是所有者,引擎持有钉定副本,测试保证二者相等。
- C-30 `moves-list` MUST 在 payload 中给出 `librarySize: {"lines", "bytes"}` 与布尔 `fullReadAllowed`(= 两条件同时满足),使「本次是否允许整读」由程序判定而非由模型估算(Token Efficiency 的 Program-First)。引擎 MUST NOT 在输出里复述阈值数值本身。
- C-31 命令模板 MUST 依 `fullReadAllowed` 行事:为 `true` 时 MAY 有界整读,MUST 在当次运行产物或反馈中留一句升级理由(判据文档的阶梯第 3 级要求留痕);为 `false` 时 MUST 只消费投影。任一情况下 MUST NOT 把库原文整段贴进对话上下文。

## 7. 版本控制与布局登记

- C-32 库 MUST 被 git **跟踪**:`.gitignore` MUST NOT 新增任何命中 `.specify/derive/` 的条目(根级或嵌套)。契约测试 MUST 断言 `git check-ignore -v .specify/derive/moves.md` 与 `.specify/derive/<slug>/derive.md` 均返回非 0(即不被忽略)。
- C-33 **与 `.specify/memory/sanitize/` 的对照**(该目录在 `.gitignore` 第 70 行被忽略)是判据本身:findings 台账被忽略,因为确定性检查器在每次 `collect` 时**重新推导**它,丢失可零成本重建;算子**不可重新推导** —— 它来自 agent 对某个来源论证方式的阅读,丢失即永久丢失累积的推理资本(FR-016 / 概念锚 §Move Library「Tracked, never ignored」)。故二者判据相反,且 MUST 各自保持:任何把 `moves.md` 归入「可再生缓存」的改动都是概念错误,不只是配置错误。
- C-34 `superseded` 行随库一并跟踪,MUST NOT 以「清理历史」为由从版本库中移除;需要理解某算子为何被放弃时,该行与其锚点是唯一证据。
- C-35 `.specify/derive/` MUST 在框架布局图 `shared/definitions/framework-map.md` 的表中登记一行(FR-038),沿用该表三列形态(`What` | `Where` | `Notes`),Notes 只写「什么住在这里」不写「怎么用」:`Derivation store` | `.specify/derive/` | `moves.md`(项目级算子库,引擎独写)+ `<topic-slug>/derive.md`(一个主题一份推导档案);概念定义指向 `shared/definitions/derivation-definitions.md`。
- C-36 `.specify/derive/` MUST NOT 出现在 `sync-mirrors.py` 的 `MIRROR_PAIRS` 中:它是**项目运行时数据根**(与 `.specify/goal/`、`.specify/specs/` 同类),不是框架分发面的镜像目标;把它登记为镜像会让 `specify init` 的加法 copytree 把一份示例库推进每个下游项目。
- C-37 `init` MUST 在库不存在时创建它(标题行 + 引擎写入标记 + 表头 + 分隔行,零数据行),MUST NOT 改写既有库(`contracts/derive-engine.md` C-24)。库存在但结构违例时 `init` MUST 原样保留并让 `validate` 报错,MUST NOT「修复后重建」—— 那会静默吞掉手工编辑的证据。

## 8. 契约测试锚点

- C-38 表形夹具 MUST 逐条断言:C-2 表头与分隔行逐字;C-4 的 7 单元格与 `(?<!\\)\|` 切分(含单元格内 `\|` 的用例);C-5 跨行单元格被拒;C-6 的限定 `anchor` 形式被接受、裸 `S-<nnn>` 报子因 `anchor-form`;C-7 标记缺失被检出;C-8 行间空行被检出。
- C-39 去重夹具 MUST 覆盖 C-14 两级各自命中与各自不命中(同名不同形状 MUST 追加;同形状不同槽位名 MUST 拒绝并返回既有 ID),并断言 C-15 的退出码为 0 与 `duplicates[]` 内容。
- C-40 状态机夹具 MUST 参数化遍历持久二值枚举的 2×2 全部 `from → to` 组合,逐一断言 C-18 表的合法/非法判定(`active → superseded` 合法、`superseded → *` 一律非法),并断言 C-19(无新锚点的 `reinforced` 被拒)、C-20(移除锚点被拒)、C-21(任何动作后行数只增不减)、C-17(任何动作后 `status` 列都不含 `new` / `reused` / `reinforced`)。
- C-41 单调性夹具 MUST 断言:连续追加 N 条后 ID 为 `M-001`…`M-00N`;手工把某行改为重复 ID 或降序后,`moves-add` 拒绝发放且 `validate` 报 A13 `fail`。
- C-42 投影夹具 MUST 断言 C-25 三态:裸引用合法、无标记复写行报 `unmarked-move-copy`、有标记但形状分歧报 `divergent-move-projection`;并断言 `superseded` 引用报 `superseded-move-applied`。
- C-43 版本控制夹具 MUST 断言 C-32 的 `git check-ignore` 结果与 `.gitignore` 中不存在 `derive` 相关条目;阈值漂移夹具 MUST 断言 C-29 的两个常量与 `shared/guidelines/token-efficiency.md` §小文件阈值一致。
