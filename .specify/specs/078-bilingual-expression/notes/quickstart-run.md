# quickstart S1–S8 实跑留档 — 078 双语表述（Bilingual Expression）

**实跑阶段**：implement Part 4（T018 收口；2026-10-30T11:58–12:05Z）
**权威场景源**：`.specify/specs/078-bilingual-expression/quickstart.md` S1–S8（MUST NOT 改写）

## 场景清单与各自判据

| 场景 | 内容 | 判据 | 状态 |
|------|------|------|------|
| S1 | 约定核对（读者面，无命令） | 四步核对可自判合规（信号 / 方向 / 形态 / 豁免） | done |
| S2 | 检查器形态判定 ×3（合规 / 全角 / 同向） | 退出码 0/1 与 finding 码、行号定位形态 | done |
| S3 | 覆盖面核验 | `coverage` 不接受 `--path`；覆盖面清单只读 owner 文档 | done |
| S4 | 下游 instructions 生成（pilot 管道） | 产物含逐字 ambient 标题、四组枚举关键词零命中、含 [[STR-001]] 指针；pilot 拆除 | done |
| S5 | 镜像零新增漂移 | 本特性三对相对 `plan-sync-mirrors-baseline.txt` 无新增 DIFF | done |
| S6 | 结构面零新增 | `docs-utils.py --action validate` violations 相对基线 4 零新增 | done |
| S7 | SC-001 关键词扫描 | 程序派生关键词表；排除 owner 自身与指针行后命中数 0 | done |
| S8 | census（SC-005） | 退出码 0；中文侧逐字比对；100% census | done（受控语料；真实词汇表实跑归 review） |

## S1 实跑

标本：`shared/guidelines/token-efficiency.md:7` 的 `## 程序优先(Program-First)`（存量行，约定成文前的既有实践）。
四步核对（依据 [[STR-001]] § 定义处与可判定信号 / § 方向规则与唯一形态 / § 豁免面）：
① 信号：S2 章节标题行，且 `shared/guidelines/` 在覆盖定义面封闭集内 → 受约束。
② 方向：文档无 S4 主语言声明，按保守缺省取 CJK 占比高者 → 主语言 zh ⇒ 形态须为 `中文(English)`。
③ 形态：半角 `(` `)`、紧贴无空格（`程序优先(Program-First)`）→ 符合 [[STR-002]] 逐字形态。
④ 豁免：非代码标识符 / 路径 / 命令字面量 / API 名 / YAML 键 / 第三方专名 / 公认缩写 → 不落豁免面。
判定：合规。四步可自判，无需裁决。

## S2 实跑

- 合规例：`python3 scripts/python/bilingual-expression-check.py --action scan --path tests/fixtures/bilingual/compliant-definition.md`
  输出 `{"action": "scan", "files_scanned": 1, "findings_count": 0, ...}`；rc=0。
- 全角例：同命令扫 `fullwidth-definition.md` →
  `tests/fixtures/bilingual/fullwidth-definition.md:3 [full-width-parens] 全角括号紧贴词条: Fast Fail Discipline`；rc=1（行号定位形态符合 quickstart 期望）。
- 同向例：同命令扫 `same-language-definition.md` →
  `tests/fixtures/bilingual/same-language-definition.md:3 [same-language-bracket] 括号语言与词条同向: Fast Fail Discipline`；rc=1。

## S3 实跑

`python3 scripts/python/bilingual-expression-check.py --action coverage` →
`{"action": "coverage", "files_scanned": 7, "findings_count": 0, ...}`；rc=0（七面齐全无 coverage-missing）。
边界核验：`--action coverage --path shared/guidelines/bilingual-expression.md` →
`error: coverage does not accept --path (scope = owner-document coverage list)`；rc=2（S3 判据「不接受 --path」成立）。

## S4 实跑

pilot 根：`.specify/.tmp/078-bilingual-expression/s4-pilot-t018`（受认可 .specify/.tmp 根；git init + 复制
`.specify/templates/` 与 `.specify/scripts/` 镜像为 init 载荷；在 pilot 目录内以框架源脚本绝对路径运行）。
`bash <framework-abs>/scripts/bash/generate-instructions.sh` → tail：
`success Instructions generated/updated at .specify/instructions.md`；generator_rc=0。
断言（程序派生关键词表，复用契约测试 derive_keywords）：
`grep -c '^## Bilingual Expression (双语表述)' .specify/instructions.md` = 1；小节内四组枚举关键词命中 = 0；含 [[STR-001]] 指针 = True。全过。
拆卸：`rm -rf` pilot（done）；`git status --ignored --porcelain .specify/.tmp/` 仅 `!! .specify/.tmp/` 空根，不作新增。

## S5 实跑

`python3 scripts/python/sync-mirrors.py --check` → rc=0；六对全 ok：
templates 22 / skills/external 406 / skills/internal 136 / agents 3 / scripts 118 / shared 61；per-tool 命令副本 OK。
与 `plan-sync-mirrors-baseline.txt` 逐行比对：唯一差异为 scripts 117→118、shared 60→61 的计数行——
即本特性新增的检查器与 owner 文档（源 + 镜像各一），T008 已裁决为特性内新增非漂移；无其它新增 DIFF。

## S6 实跑

`python3 skills/external/create-docs/scripts/docs-utils.py --action validate` → docs_utils_rc=0；
violations = 4（broken-link 3 + note-frontmatter 1），对 plan 基线逐条 JSON 比较 new=0 / gone=0。
（命令形态与 S6 文档记录的 `.specify/skills/create-docs/...` 为同一脚本的框架源/镜像两路径。）

## S7 实跑

程序派生关键词表（22 个字面量，四组枚举；复用契约测试 derive_keywords，MUST NOT 手写）；
检索 shared/、templates/、.specify/（排除 .specify/specs/ 与 .specify/history/，git ls-files 全量）。
本次实跑：raw 命中 44 = owner 文档自身枚举行 22 项 × 框架源 + 镜像两路径（全部按排除规则 (i) 排除）；
含 [[STR-001]] 指针行命中 0；计入复制位置数 = 0。与交付日快照 `test-evidence/us9-sc001-keyword-snapshot.txt`
判定一致（快照的「排除 0」口径为不重复计入 owner 自身；两口径下复制位置数均为 0）。

## S8 实跑（受控语料；真实词汇表实跑归 review）

按 tasks 约定（T015／tasks Notes：SC-005 真实词汇表 census 归 review 阶段，implement 不预支），
本场景以 T015 受控语料实跑验证命令形态与判定行为；真实树同一命令由契约腿 test_census_action 钉死（T017 全绿含该腿）。
命令：`python3 <temp-root>/scripts/python/bilingual-expression-check.py --action census --json`
（REPO_ROOT 由脚本位置解析至临时根；受控词汇表 3 条紧贴双语 Canonical + 覆盖定义面样本 4 件）
三轮：一致语料 rc=0、census_total=3、findings 0；注入错写中文侧负控 rc=1 且恰好 1 条
`missing-bilingual`（中文侧逐字比对真实执行，非恒绿）；恢复后 rc=0。
中文侧比对逐字执行（含 Variants 归一），100% census（分母 3 = 全量双语词条，无抽样）。
拆卸：临时根已 rm -rf；真词汇表零修改。详见 `test-evidence/us15-census-controlled.txt`。
