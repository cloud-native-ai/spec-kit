# Contract: derive-utils.py 引擎 CLI(需求 048 / Feature 049)

**Requirement → Feature**: `048-derive-command` → Feature 049 Derivation Command
**交付物**: `scripts/python/derive-utils.py`(stdlib-only,Python ≥ 3.8),strict 镜像至 `.specify/scripts/python/derive-utils.py`
**概念真源**: `shared/definitions/derivation-definitions.md`;规则的执行面见 `contracts/derivation-model.md`;算子库物理契约见 `contracts/move-library.md`。本契约只拥有 **CLI 形态、信封、退出码与写入权**。
**消费方**: `templates/commands/derive.md`(内联调用)、`tests/contract/test_derive_engine_contract.py`、`tests/unit/test_derive_validate.py`、Tool 记录 `.specify/memory/tools/derive-utils.py.md`

## 1. 模块形态

- C-1 引擎 MUST 为单文件 stdlib-only 脚本:`from __future__ import annotations` 置于 docstring 之后、导入之前;可用模块限于 `argparse` / `json` / `os` / `re` / `sys` / `unicodedata` / `urllib.request` / `urllib.error` / `socket` / `datetime` / `pathlib` / `subprocess`(仅 `probe-links` 的传输缝可能需要)。任何第三方导入 MUST 使契约测试失败。
- C-2 模块 docstring MUST 命名概念真源与本契约路径(照 `scripts/python/goal-utils.py` 先例:`Concept authority:` + `Contract:` 两行),MUST 列出六动作与退出码表,且 MAY 携带 `Feature 049 / requirement 048` 标识 —— `scripts/` 不在 FR-037 的客户中性范围内(该范围是 `templates/` 与 `shared/`),`sanitize-utils.py` 已有同形先例。
- C-3 退出码 MUST 为具名常量 `EXIT_OK = 0` / `EXIT_USAGE = 1` / `EXIT_INPUT_ERROR = 2` / `EXIT_NOT_FOUND = 3` / `EXIT_INVALID = 4`,语义逐字对应 [[STR-004]];`main()` MUST 返回 `int`,脚本 MUST 以 `sys.exit(main())` 收尾,使测试可直接调用 `main(argv)`。
- C-4 模块 MUST 携带 `.specify` 镜像守卫(照 `scripts/python/scan-confirmation-gates.py` 第 30–33 行):`_HERE = Path(__file__).resolve()`;`REPO_ROOT = _HERE.parents[2]`;`if REPO_ROOT.name == ".specify": REPO_ROOT = REPO_ROOT.parent`。守卫派生的 `REPO_ROOT` MUST 只用于定位仓内只读资产(概念锚,供 C-19 的自检);工作区解析一律走 `--workspace-root`,二者 MUST NOT 混用。
- C-5 路径常量 MUST 钉为 `ARCHIVE_DIRNAME = ".specify/derive"`、`MOVES_FILENAME = "moves.md"`、`ARCHIVE_FILENAME = "derive.md"`([[STR-006]]);引擎 MUST NOT 从环境变量、配置文件或产物字段读取存储位置。
- C-6 topic slug 语法 MUST 复用 `goal-utils.py` 的 `_IDENTITY = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.\-]*$")`;不合语法的 `--slug` → 退出码 2。MUST NOT 新造第二套身份语法。

## 2. CLI 形态

- C-7 参数风格沿用 `sanitize-utils.py`:`--action <name>`(必填)+ `--workspace-root <path>`(缺省 `.`)+ `--format text|json`(缺省 `json`)。`--action` 的 choices 恰为 [[STR-003]] 六值,逐值语法由 C-8 的表拥有(本契约 MUST NOT 在别处再列一遍);未知或缺失 action → 退出码 1,输出 `{"ok": false, "action": null, "errors": [{"rule": null, "code": "usage-error", ...}], ...}`。**实现期修订**:code 定为 `usage-error` 而非 `unknown-action` —— argparse 的用法违例是一个**类**(未知 action、缺失 action、动作不接受的 flag),一个 code 覆盖全类、具体形态由 `message` 携带,比为每种形态各设一个 code 更省且不丢信息;`action: null` 与退出码 1 的要求不变。
- C-8 除三个全局 flag 外,引擎 MUST 只接受下表列出的动作级 flag;任何未列 flag MUST 被 argparse 拒绝(退出码 1 由 argparse 的 `error()` 触发,MUST NOT 被吞成 0)。特别地 MUST NOT 引入 `--timeout`、`--limit`、`--offline`、`--dry-run`:探测超时是常量 `PROBE_TIMEOUT_SECONDS = 10`,离线是 C-31 的自动降级而非开关。

| action | 必填 | 可选 | 写入 |
|---|---|---|---|
| `init` | `--slug <topic-slug>` | `--force`, `--max-steps <int>` | 创建 `.specify/derive/<slug>/derive.md`;必要时创建 `moves.md` |
| `validate` | `--file <path>` **或** `--slug <slug>`(互斥,恰给一个) | `--max-steps <int>` | 零写入 |
| `moves-list` | — | `--name-contains <substr>`, `--status <active\|superseded>`, `--anchor <S-id 或 topic-slug.S-id>` | 零写入 |
| `moves-add` | `--file <json>` | — | **仅** `moves.md`(C-16) |
| `probe-links` | `--file <json>` | — | 零写入 |
| `stats` | — | `--file <path>` **或** `--slug <slug>` | 零写入 |

- C-9 `--max-steps` MUST 为正整数;预算解析次序为**两级**:显式 `--max-steps` > 模块常量 `DEFAULT_MAX_STEPS = 12`。产物 `## Termination` 里声明的 budget **不参与**解析(它是运行对自己所用预算的报告,不是第二个真源);声明值 ≠ 生效值时由 `validate` 报 `step-budget-diverges`(`contracts/derivation-model.md` §3 的 C6 行),MUST NOT 被静默采用。非正整数 → 退出码 2。
- C-10 `--file` / `--slug` 同时给出或同时缺失 → 退出码 2;`--slug` 指向不存在的档案 → 退出码 3;`--file` 指向不存在的文件 → 退出码 3;`--file` 存在但不可解析(Markdown 无 `## Sources` 节 / JSON 非法)→ 退出码 2。
- C-11 `--status` 与 `--anchor` 取值 MUST 校验:`--status` 不在库的**持久**二值枚举内(取值归概念锚 §Move Record)→ 退出码 2 —— 运行相对处置不是库状态,MUST NOT 作为该 flag 的取值;`--anchor` 既不匹配 `^S-\d{3,}$` 也不匹配限定形式 `^[A-Za-z0-9][A-Za-z0-9_.\-]*\.S-\d{3,}$` → 退出码 2。过滤器 MAY 组合,语义为 AND;组合后零命中是合法结果(退出码 0,`payload.returned == 0`)。

## 3. 退出码

| 码 | 常量 | 触发形态 |
|---|---|---|
| 0 | `EXIT_OK` | 成功。**含**「零发现」「零命中」「降级运行」(`derivation-model.md` C-46)与 `probe-links` 全离线 |
| 1 | `EXIT_USAGE` | 未知/缺失 `--action`、未列 flag、argparse 用法错误 |
| 2 | `EXIT_INPUT_ERROR` | slug 语法违例、`--file`/`--slug` 组合非法、JSON schema 违例、`--max-steps` 非正、库不可安全追加(C-18)、状态迁移非法 |
| 3 | `EXIT_NOT_FOUND` | 档案/库/输入文件不存在 |
| 4 | `EXIT_INVALID` | `validate` 的 `errors[]` 非空 —— 一切 C1–C7 / A1–A14 机械违例 |

- C-12 `init` 撞已存在档案且未给 `--force` → 退出码 2(no-clobber 是**输入冲突**,不是「未找到」);给出 `--force` → 覆盖脚手架,`payload.clobbered` MUST 为 `true` 且 `payload.backupPath` MUST 记录被覆盖内容的 `.bak` 路径。`--force` MUST NOT 影响 `moves.md`(库永不被 `init` 改写)。
- C-13 退出码 MUST 与信封 `ok` 字段一致:`ok == true` ⟺ 退出码 0。MUST NOT 出现「`ok: true` 且退出码 4」这类可用于粉饰失败的组合。

## 4. JSON 信封

- C-14 `--format json` 时 stdout MUST 恰为一个 JSON 对象(无前后缀文本、无多行拼接),顶层键固定且恒存在:

```json
{
  "ok": true,
  "action": "validate",
  "workspaceRoot": "/abs/path",
  "generatedAt": "2026-09-05T10:00:00Z",
  "errors":   [ { "rule": "C3", "code": "banned-justification",
                  "locator": "D-004.derivation", "message": "...",
                  "value": "<matched literal from [[STR-001]]>" } ],
  "warnings": [ { "code": "unresolved-title", "locator": "S-003.resolved_title", "message": "..." } ],
  "semanticChecksPending": ["A11", "A14"],
  "notes":    ["<[[STR-007]]>: degraded run, chain not built"],
  "payload":  { }
}
```

- C-15 `errors[]` / `warnings[]` / `semanticChecksPending[]` / `notes[]` MUST 恒为数组(空时为 `[]`,MUST NOT 为 `null`),使消费方永不 KeyError。`semanticChecksPending` MUST 在 `validate` 上恒为 `["A11", "A14"]`,在其余五动作上恒为 `[]`(它们不做自审);该键的存在性与恒定性是 FR-030 的机械锚点。
- C-16 `generatedAt` MUST 为 UTC ISO-8601(`%Y-%m-%dT%H:%M:%SZ`)。`workspaceRoot` MUST 为 `Path(...).resolve()` 后的绝对路径。
- C-17 `--format text` MUST 输出人类可读摘要:错误/警告分区呈现、每行携带 `code` 与 `locator`、末尾一行计数汇总;MUST NOT 输出 JSON。两种格式 MUST 由同一份内部结果渲染,MUST NOT 各算一遍。

## 5. 各动作 payload

- C-18 `init` → `{"slug", "archivePath", "movesPath", "created": ["<相对路径>", ...], "clobbered": bool, "backupPath": str|null, "maxSteps": int, "terminationCondition": null}`。脚手架 MUST 含概念锚定义的全部节(`## Sources` / `## Unverifiable Sources` / `## Reasoning Moves Applied` / `## Derivation Chain` / `## Derived Architecture` / `## Open Questions` / `## Termination` / `## Self-Audit`),且 `## Self-Audit` MUST 预填 14 行、A1–A10/A12/A13 的 `result` 为 `pending`、A11/A14 的 `result` 为 `pending`。
- C-19 `validate` → `{"file", "degraded": bool, "sources": {"total", "byGrade": {}, "byAccess": {}, "titleMismatch": int}, "steps": {"total", "anchorable", "byConfidence": {}, "budget", "budgetReached": bool}, "moves": {"cited": int, "resolved": int, "missing": []}, "elements": {"total", "byConfidence": {}, "untraceable": int}, "openQuestions": {"total", "brokenLinks": []}, "audit": {"engine": {"A1": "pass", ...}, "semantic": {"A11": "pending", "A14": "pending"}}}`。`byGrade` / `byAccess` / `byConfidence` 的键集 MUST 恒为完整枚举(缺项计 0),使 SC-001/SC-002 的分组计数可直接断言而无需先探形状。
- C-20 `moves-list` → `{"total", "returned", "projection": true, "filters": {"nameContains", "status", "anchor"}, "librarySize": {"lines": int, "bytes": int}, "fullReadAllowed": bool, "moves": [{"moveId", "name", "inferenceForm", "prevents", "appliesWhen", "anchor", "status"}]}`。`fullReadAllowed` 按 `shared/guidelines/token-efficiency.md` 的小文件阈值计算(阈值常量与漂移纪律见 `contracts/move-library.md` C-29);引擎 MUST 只给出布尔判定,MUST NOT 在输出里复述阈值数值。
- C-21 `moves-add` → `{"requested": int, "appended": int, "deduped": int, "superseded": int, "issued": ["M-<nnn>", ...], "dispositions": [{"moveId", "disposition"}], "duplicates": [{"requestIndex", "normalizedForm", "existingMoveId"}]}`。`dispositions[].disposition` 取值封闭为 `new` / `reused` / `reinforced`,是**运行相对**处置(概念锚 §Move Record「Durable state vs run-relative disposition」),MUST NOT 被写入库的 `status` 列;`superseded` 计的是本次执行的**持久**迁移 `active → superseded` 次数,它不是处置,故 MUST NOT 出现在 `dispositions[]`。`issued[]` 只含本次新发放的 `M-<nnn>`,它是 A13 的核验面(`contracts/derivation-model.md` C-41)。**去重-拒绝语义**:归一化 `inference_form` 命中既有行时 MUST NOT 写入新行,MUST 在 `duplicates[]` 返回既有 `move_id`、`deduped` +1,该条目的处置记为 `reinforced` **当且仅当**本次带来了该行 `anchor` 列尚无的限定来源引用,无新锚点时处置为 `reused`(`contracts/move-library.md` C-19)。**实现期修订**:本条原先一律写作 `reinforced`,与 move-library C-19「无新锚点的 reinforced 就是 reused」矛盾;引擎从 C-19,因为允许无新锚点的 `reinforced` 会让处置报告变成运行次数的虚报。两种情况都 MUST NOT 分叉出变体(FR-013)。拒绝是**成功路径**,退出码 MUST 为 0。
- C-22 `probe-links` → `{"probed", "online": bool, "degraded": bool, "results": [{"url", "access", "resolvedVia": str|null, "httpStatus": int|null, "snapshotTs": str|null, "error": str|null, "evidence": str}]}`。`access` 与 `resolvedVia` 的取值 MUST 落在概念锚 §Source Record 的枚举内(引用不复述);**实现期修订**:`resolvedVia` 为 `str|null` —— 传输缝异常时探测根本没走完任何一级,此时不存在「经由哪条路径解析」这一事实,`null` 是诚实值而空串是枚举外值:直连可解析但正文在付费墙后、仅摘要公开 → `paywalled`(锚 §Dead-Link Protocol 第 1 步);传输缝异常使协议无法跑完 → `unknown`,MUST NOT 报 `dead`(第 4 步)。`evidence` MUST 是可直接写入产物 `verification` 列的具体串(`contracts/derivation-model.md` C-33 的证据记号形态),MUST NOT 是 `verified` 一类裸断言。
- C-23 `stats` → `{"moves": {"total", "byStatus": {}, "duplicateIds": int, "duplicateForms": int}, "dispositions": {"new": int, "reused": int, "reinforced": int}, "archives": {"total", "topics": []}, "lastRun": {"slug", "generatedAt"}|null}`。`byStatus` 的键集 MUST 恒为库的**持久**二值枚举(缺项计 0);`dispositions` 是**运行相对**计数,取自 `--file`/`--slug` 所指档案 `## Reasoning Moves Applied` 的处置列(SC-003 的机械锚点:同主题第二次运行的 `reused` + `reinforced` > 0),未给档案时 MUST 三项全为 0 而非缺键。`duplicateIds` 与 `duplicateForms` MUST 恒为 0(SC-003 的机械锚点);非 0 时 MUST 同时产出 `moves-library-hand-edited` error 到顶层 `errors[]`。

## 6. 写入权与身份发放

- C-24 **`moves.md` 独写者规则**:`moves-add` MUST 是引擎中唯一以写模式打开 `.specify/derive/moves.md` 的代码路径。`init` MAY 在库不存在时创建它(仅表头 + 分隔行 + 引擎写入标记,零数据行),MUST NOT 改写既有库;`validate` / `moves-list` / `probe-links` / `stats` MUST 零写入。
- C-25 手工编辑 MUST 被**检出而非静默接受**:`validate` 与 `stats` MUST 运行库不变量检查(`contracts/move-library.md` §1–§4),任一不成立即报 `moves-library-hand-edited`。引擎 MUST NOT 自动修复、自动重排或自动重编号;修复途径是人工编辑后重跑 `validate`,或经 `moves-add` 走合法路径。
- C-26 `M-<nnn>` MUST 由 `moves-add` 项目级单调发放:下一个 ID = 现存最大编号 + 1,零填充至最少 3 位;已发放的 ID MUST NOT 被复用或重编号。库的单调性被破坏时 `moves-add` MUST 拒绝发放并退出码 2(`moves-library-hand-edited`,子因 `id-not-monotonic`)—— MUST NOT 通过重编号「让追加成功」。
- C-27 `S-` / `D-` / `A-` / `Q-` 四类身份由 agent 在档案中书写,引擎**校验**其语法但 MUST NOT 发放。语法按概念锚分两族,逐字为:`S-` MUST 匹配 `^S-\d{3,}$`(锚 §Source Record 定义其为 `S-<nnn>`),其**跨主题限定形式** MUST 匹配 `^[A-Za-z0-9][A-Za-z0-9_.\-]*\.S-\d{3,}$`(锚 §Move Record 要求库内 `anchor` 写 `<topic-slug>.S-<nnn>`;slug 段语法同 C-6,即复用 goal 身份语法,容 `.` 不容 `#` / `/`);`D-` / `A-` / `Q-` MUST 匹配 `^(D|A|Q)-\d{1,}$`(锚的 Step / Element / Open Question 记录定义为 `D-<k>` / `A-<k>` / `Q-<k>`)。各族 MUST 在各自节内单调递增且无重复。唯一由引擎发放的身份是 `M-`(因为库是唯一由引擎独写的文件)。这是对概念锚 §Script / Prompt Boundary「identity grammar and monotonic ID issuance」一行的执行面收窄:发放只在独写文件上有意义,其余四类只能事后校验。
- C-28 `moves-add` 的输入 MUST 为 JSON 文件 `{"moves": [ {...} ]}`;schema 校验失败 → 退出码 2 且**零写入**(全有或全无,照 `sanitize-utils.py --action record` 先例)。每个条目 MUST 给出 `name` / `inferenceForm` / `prevents` / `appliesWhen` / `anchor`(≥1 个来源引用,写入库时 MUST 为限定形式 `<topic-slug>.S-<nnn>`)/ `intent`。`intent` 取值封闭为 `new` / `reuse` / `reinforce` / `supersede`,它表达**本次运行要做什么**,不是库状态,也 MUST NOT 被写进任何列:`new` 走追加(命中去重则该条目的处置转为 `reinforced` 并返回既有 id),`reuse` 零写入、只报处置,`reinforce` 就地只增 `anchor`,`supersede` 就地把持久 `status` 迁为 `superseded`(终态)。后三者 MUST 同时给出 `existingMoveId`,由引擎按 `contracts/move-library.md` C-18 的合法迁移表与 C-19 的新锚点前置条件校验后**就地更新该行**(更新也是写,故仍归 `moves-add` 独写)。
- C-29 `moves-add` MUST 原子写:先写 `<moves.md>.part` 再 `os.replace`;写入失败 MUST 不留下半截文件,且 MUST 以退出码 2 报告。

## 7. `probe-links` 离线容错

- C-30 全部网络 I/O MUST 收敛到单一传输缝函数 `_http_get(url: str, timeout: int) -> tuple[int | None, str]`(状态码或 `None`,响应体或错误串)。除该函数外,引擎 MUST NOT 出现任何 `urllib` / `socket` 调用;该唯一缝是「测试不得触网」可被机械断言的前提。
- C-31 任何网络异常(DNS 失败、超时、TLS 错误、非 2xx、连接被拒)MUST 被吞为该条结果的 `access: "unknown"` + `error: <异常类名与一句话>`,整个动作 MUST 以退出码 0 返回,`payload.online` MUST 为 `false`,`notes[]` MUST 含降级说明。`probe-links` MUST NOT 阻塞、MUST NOT 重试超过一次、MUST NOT 抛栈到调用方。
- C-32 `probe-links` MUST NOT 写入任何文件(它是证据供给者,不是档案作者);把结果落进 `## Sources` 是命令模板中 agent 的动作。
- C-33 **任何测试 MUST NOT 对真实网络调用 `probe-links`**:单测 MUST monkeypatch `_http_get`;契约测试 MUST 断言 (a) 模块中 `_http_get` 是唯一的传输缝(源码扫描 `urllib`/`socket` 出现处 ⊆ 该函数体),(b) 全部含 `probe-links` 的测试文件都出现 `monkeypatch`/`_http_get` 补丁痕迹。存档可用性查询 MUST 走同一缝,MUST NOT 另开第二条 I/O 路径。
- C-34 探测顺序 MUST 与概念锚 §Dead-Link Protocol 一致(直连〔含付费墙分支〕→ 存档可用性 → 由 agent 驱动归属搜索),引擎只承担前两级;第三级是 agent 的检索动作,`probe-links` MUST NOT 代替它,也 MUST NOT 在协议未跑完(缺第三级、传输缝异常、无连通性)时把来源判为 `dead` —— 判 `unknown`,由 agent 补(网络故障不是死链)。

## 8. 镜像、登记与测试锚点

- C-35 `scripts` 镜像对在 `sync-mirrors.py` 的 `MIRROR_PAIRS` 中已是 strict 全树对(`("scripts", ".specify/scripts", True, set())`),故新引擎 MUST 自动获得字节一致镜像,MUST NOT 另加按文件登记;`sync-mirrors.py --check` 退出码非 0 即为交付缺陷。
- C-36 `tests/contract/test_derive_engine_contract.py` MUST 断言:`--action` 的 choices 恰为 [[STR-003]] 六值且无多余;退出码常量与 [[STR-004]] 逐值相等;信封顶层键集恰为 C-14 所列;`semanticChecksPending` 恒为 `["A11","A14"]`(validate)/ `[]`(其余);stdlib-only(源码导入扫描);`.specify` 镜像守卫存在;`moves.md` 独写者(除 `moves-add`/`init`-create 外无写模式打开);预算解析为两级且 `DEFAULT_MAX_STEPS == 12`(C-9);`moves-add` 的 `intent` 取值集恰为 C-28 四值、`--status` 取值集恰为库的持久二值(C-11);`--anchor` 与库内 `anchor` 同时接受裸式与限定式(C-27);写入库的任何一行的 `status` 列 MUST NOT 出现 `new` / `reused` / `reinforced` 三个运行相对值(它们只出现在 payload 输出里,C-21)。
- C-37 引擎 `--help` 输出 MUST 与本契约的 flag 表一致(逐 flag 名),使 quickstart 中的可执行示例被契约测试钉死、flags 不漂移。
- C-38 引擎 MUST 有 Tool 记录 `.specify/memory/tools/derive-utils.py.md`(Tool Reuse 纪律,宪法 XII),记录六动作、退出码与「探测缝是唯一 I/O 出口」这一行为规则;记录 MUST 引用本契约而非复述。
