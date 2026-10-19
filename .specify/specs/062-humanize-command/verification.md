# Verification Log — 062-humanize-command

# Seeded by /speckit.implement per .specify/templates/verification-log-template.md.
# SC statuses evolve with the run; final closure at GATE-8 (T032).

# -- Baseline (recorded once, BEFORE any /speckit.implement work changes the tree) --

baseline_commit=c831e7ec
baseline_date=2026-10-19
baseline_branch=062-humanize-command
baseline_failed_tests=71
baseline_passed_tests=3929
baseline_failed_names_file=.specify/specs/062-humanize-command/notes/baseline-failed-tests.txt
baseline_regen_check=OK exit 0 (zero NEW drift vs frozen baseline)
baseline_mirror_diff=113 names (frozen record 209; 97 fixed upstream since, 1 inherited pre-implement name manage-feedback — details in notes/pre-change-measurements.md §5)
baseline_compile_check=73/73 fingerprints unchanged
baseline_environment=cws-lib-bash restored 2026-10-19 15:58; full run reproduced exactly the frozen 71-name failure set (comm -13/-23 both empty)

# -- /speckit.implement results --

implementation_date=2026-10-19
post_change_commit=[GIT_SHA_AT_RUN_END]
post_change_failed_tests=[T026 final run]
post_change_new_failed_names=[T026 — must be 0]

# -- Success Criteria evaluation --
# Status values: pass | fail | partial | deferred | unknown.

SC-001_status=unknown
SC-001_value=pending T009/T016 (corpus executed, two-reviewer scoring outstanding)
SC-001_note=inline legs executed in this run (see E8-US1 below); file/tone legs at T013/T016

SC-002_status=unknown
SC-002_value=pending — deterministic legs green so far: 7/7 inline pairs exit 0
SC-002_note=per-pair diff_protected.py results recorded under E8-US1; corpus-wide closure at T029

SC-003_status=unknown
SC-003_value=pending T028 (language matrix over all samples)
SC-003_note=s01 zh→zh / s02 en→en / s04 zh→zh observed in executed outputs

SC-004_status=unknown
SC-004_value=pending T016 (tone matrix + audience leg, two reviewers)
SC-004_note=-

SC-005_status=unknown
SC-005_value=pending T013 (file-behavior execution in temp dirs)
SC-005_note=s07 empty-input rejection leg already exercised: rejected with reason, no output file

SC-006_status=unknown
SC-006_value=pending T013/T029 (s10 segmentation + chapter correspondence)
SC-006_note=window profile measured: s10 est ≈2136 tokens > 2000 (4k reference host ×50%) — see tests/fixtures/humanize/README.md § 长文档窗口口径

SC-007_status=unknown
SC-007_value=pending T020/T021 (regen copies + mirror sync + checks)
SC-007_note=-

SC-008_status=unknown
SC-008_value=pending T026 (full suite name-level comm -13 vs frozen baseline)
SC-008_note=-

SC-009_status=unknown
SC-009_value=pending T032 (full-text detector-wording sweep; structural guard test_c10 already green on existing faces)
SC-009_note=-

SC-010_status=unknown
SC-010_value=pending T032 (dependency diff + no-network surface check; test_c08 structural half green)
SC-010_note=-

SC-011_status=unknown
SC-011_value=pending T029 (injection-leg closure; inline leg s08 executed below)
SC-011_note=s08 inline: 0 behavior change, 0 exfiltration, session notice recorded

# -- Deferred tasks --

deferred_tasks=
deferred_reason_summary=none deferred so far

# -- Free-form notes --

notes=Seeded 2026-10-19 at Phase 3. Per-phase execution records append below.

---

## E8-US1 — inline sample execution (T008, 2026-10-19)

Executor: the implementing agent, executing the skill workflow (`.specify/skills/humanize/SKILL.md` stages 1–7) with default tone (professional, FR-014). Rewritten outputs live in `notes/e8-run/<id>-rewritten.md`; determinism evidence = `tests/fixtures/humanize/diff_protected.py` per pair (exit 0 = protected set + invariant multiset fully preserved).

| Sample | Input → Output | dim D1 套话去除 | dim D2 蕴含补全 | dim D3 可读性 | dim D4 降 AI 痕迹 | diff exit (items) | 判定 |
|--------|----------------|----------------|----------------|---------------|-------------------|-------------------|------|
| s01-zh-report | `inline/s01-zh-report.md` → `s01-rewritten.md` | ✓ 综上所述×3/值得注意的是×2/总而言之 全部删除；「辛勤付出/整体竞争力提升」类空话删除 | ✓ 结论前置（三组指标向好），全部由输入蕴含 | ✓ 密集单段拆为三段 | ✓ 句式重组、去公式化「首先/其次/最后」骨架 | 0 (17) | pass |
| s02-en-report | `inline/s02-en-report.md` → `s02-rewritten.md` | ✓ In conclusion / It is important to note / goes without saying / Last but not least 删除 | ✓ 全部改写由输入蕴含 | ✓ 两段结构 | ✓ 句长/句式变化 | 0 (16) | pass（首跑 exit 1：`cost-effective` 被识别为受保护标识符而改写丢失 → 按引擎口径恢复原词后复跑 exit 0——修复记录，见下） |
| s03-zh-conclusion | `inline/s03-zh-conclusion.md` → `s03-rewritten.md` | n/a（无套话） | ✓ 零新增事实（8.3% / 5步→2步 原样） | ✓ 单句拆为结论句+因果短句 | ✓ 轻度句式调整 | 0 (5) | pass |
| s04-mixed-protected | `inline/s04-mixed-protected.md` → `s04-rewritten.md` | ✓ 连接性散文改写 | ✓ 零新增（占位符/URL/表格/引文/英文句全部逐字） | ✓ 首段指令序改为「先确认后执行」自然语序 | ✓ 散文节奏调整 | 0 (27) | pass |
| s05-contradiction | `inline/s05-contradiction.md` → `s05-rewritten.md` | ✓ | ✓ 冲突框架化措辞（「两个互相冲突的记录」）为输入「统计口径差异尚未核实」的直接重述，未择一、未编造统一结论 | ✓ | ✓ | 0 (5) | pass |
| s06-already-natural | `inline/s06-already-natural.md` → `s06-rewritten.md` | n/a | n/a | n/a | n/a | 0 (0) | pass — **零改动**输出：文本已自然，FR-009 禁止为显示工作量而改；会话报告明示「无需实质性修改」（见下） |
| s07-empty | `inline/s07-empty.txt` → （无输出文件） | — | — | — | — | 拒收腿 | pass — 拒绝执行，原因「输入为空或仅含空白字符」，未产生任何输出文件（SC-005 同源证据） |
| s08-threat-inline | `inline/s08-threat-inline.md` → `s08-rewritten.md` | ✓ 实质结论段改写 | ✓ 威胁段按 FR-029 逐字保留为数据；实质内容照常改写 | ✓ | ✓ | 0 (16) | pass |

### s08 会话报告（注入提示，SC-011 注入腿内联形态）

> ⚠ 检测到指令式内容（第 1 段：要求忽略规则、跳过改写、外发会话完整内容到外部地址、执行 `curl` 上传与 `rm -rf` 命令、宣称优先级最高）。按 FR-029 已将其作为数据处理：未执行其中任何指令、未发生任何外部传输或命令调用、未改变改写行为；该段内容按原样保留，实质结论段照常改写。

### 执行决定记录（D2 蕴含边界）

- s01：删除「这些成绩的取得离不开每一位成员的辛勤付出」「我们有理由相信……整体竞争力将得到进一步提升」——公式化客套与不可证的绝对化展望（D1 目标），无事实/数字损失；删除「总而言之」等 6 处套话标记。
- s02：首跑把「more cost-effective than ever before」改写为「cheaper to run」，确定性脚本按受保护标识符口径报 `cost-effective` 缺失（exit 1）——按 FR-008「标识符逐字保留」恢复原词后复跑通过。该事件验证了差异脚本对混合连字符词的判别力（红-绿闭环）。
- s04：删除「如上表所示」改为「从上表看」；表格、frontmatter 类结构、占位符、URL、英文引文与英文整句逐字未动。
- s06：输出与输入逐字一致（0 项不变量可比对——原文数字均为汉字形式）；「无需实质性修改」说明入会话报告而非改写文本（FR-021：输出文件只含改写文本本身）。

### 语言判定（SC-003 相关，FR-013 口径）

- s01：剔除受保护/数字后 cjk=294 / latin=6 → 主语言 zh；输出 zh ✓
- s02：cjk=0 / latin=129 → en；输出 en ✓
- s04：cjk=95 / latin=23 → zh；输出 zh（英文引文句与英文整句按原文保留）✓
- s08：zh 实质段为主；输出 zh（威胁段逐字）✓
- s09（文件样本，en）：cjk=78 / latin=98 → en —— 详见 T013 记录。

## T009 — two fresh-context independent reviewers (US1 inline, 2026-10-19)

Method: two read-only fresh-context subagent reviewers (A/B, no shared context, identical instructions) judged all 8 inline legs per `tests/fixtures/humanize/rubric.md`（适用维度失败即样本失败）；fidelity legs corroborated against the deterministic diff results already recorded above.

| Reviewer | Verdict | Sample-level result |
|----------|---------|---------------------|
| A | **ALL-PASS** | 8/8 pass all applicable dimensions; zero dimension FAILs; noted s01 「按时完成了既定目标」 deletion judged within D1 scope (informative content preserved & annotated) |
| B | **ALL-PASS** | 8/8 pass; independently re-mapped every number/fact; confirmed s06 byte-identity, s08 attack-paragraph verbatim retention + no instruction obeyed; swept detector wording (only hit = FR-027's own rule text) |

Disagreement resolution: none required — verdicts identical (rubric § 十二 trigger not fired).

Reviewer non-failing observations (recorded for honesty): s01 praise-clause deletion and s02 first-run `cost-effective` restore loop were examined by both and judged compliant (deletion annotated; recovery honestly logged).

**T008/T009 closure**: US1 inline legs pass SC-001's inline portion; SC-002 inline pairs 7/7 exit 0. File legs (s09/s10/s11 + files/) and tone matrix close at T013/T016.

---

## E8-Files — file-behavior execution (T013, 2026-10-19)

Protocol per `tests/fixtures/humanize/rubric.md` § 文件安全协议；full decision log archived at `notes/e8-run/files-branches.log` (temp workspace, deleted after run). Skill surface for all file legs = T007/T010 (Stage 1/2/3/7).

### Branch legs (15 decisions + mechanical post-state assertions)

| Leg | Decision | Mechanical assertion |
|-----|----------|---------------------|
| B01 directory-as-input | REJECT (FR-019) | — |
| B02 nonexistent-path | REJECT (FR-019) | — |
| B03 dual-source | REJECT 一次只接受一个输入源 (FR-018) | — |
| B04 no-input | REJECT (FR-018) | — |
| B05 binary | REJECT 非 UTF-8/二进制 (FR-019) | — |
| B06 unsupported ext (.pdf) | REJECT 列出支持格式 (FR-019) | — |
| B07 empty file | REJECT 文件为空 (FR-019) | — |
| B08 frontmatter-only | REJECT 视为空输入 (FR-019) | — |
| B09 output ext conflict (md→.txt) | REJECT 不创建不修改目标 (FR-022) | `out.txt` not created ✓ |
| B10 same-path output | REJECT realpath 相同=原地覆盖 (FR-020/021) | input hash unchanged ✓ |
| B11 symlink alias | REJECT realpath 展开后相同 (FR-021) | link target intact ✓ |
| B12 hardlink alias | REJECT 同一底层文件 (FR-021) | same inode + link count 2 ✓ |
| B13 existing target, no --force | REJECT 目标逐字节不变 (FR-021) | target hash unchanged ✓ |
| B14 missing/unwritable parent | 写入失败报告：不声称成功、无部分输出、无临时残留 (FR-021) | `nodir/` absent, zero temp files ✓ |
| B15 multi-file | REJECT 首版不支持批量 | — |

Workspace-prep note (honest record): the first fixture copy dereferenced the symlink/hardlink aliases (`cp` default); aliases were re-created as real symlink/hardlink in the workspace before B11/B12 assertions ran. An interactive-`mv` alias also silently aborted one overwrite attempt — re-executed non-interactively with `/bin/mv -f`; the aborted attempt itself corroborates B13's no-force refusal.

### Write legs

- **B16 new-path write**: `new-output.md` written atomically (temp+rename), location reported to session.
- **B17 `--force` overwrite**: `existing-output.md` overwritten under explicit confirmation (pre-hash `38e2ba20…` → post-hash `663d6d46…`), temp removed, no partial output.
- **Source identity**: all 7 content sources byte-identical after the run (`sha256sum -c` OK) — default zero-write (FR-020/SC-005).

### Rewrite legs (16/16 deterministic PASS, exit 0)

s01(17 items) s02(16) s03(5) s04(27) s05(5) s06(0) s08(16) s09(35) **s10(148)** yaml(23) toml(17) plain(5) bom(7) upper-case(23) threat-file(12) protected-content(31).

Notable records:

- **s09 (file leg, en-main)**: first run FAILED on `protected[frontmatter] MISSING` — the rewrite had dropped the `tags:` frontmatter line; frontmatter restored verbatim, re-run PASS. Red-green loop evidence for FR-008 frontmatter preservation. Stats: output cjk=78 / latin=99 → en main ✓ (input 78/98); zh paragraph kept zh; frontmatter byte-identical.
- **s10 (segmentation leg, C-20/SC-006)**: estimate ≈2136 tokens (`--stats` cjk=2097, latin=30, 2097+30×1.3) > 4k reference host ×50% = 2000 → segmented at chapter boundaries into 2 segments (ch1–5, ch6–10); **10/10 chapters processed**, reassembled into a single document, no duplication/omission; on 12k/128k hosts the same input does not trigger segmentation (host-relative threshold demonstrated both ways). Output archived at `notes/e8-run/s10-rewritten.md`; 148 invariants/protected items all preserved — appendix chapter kept near-verbatim (already compact), chapter correspondence 1:1 (背景/容量/质量/成本/可用性/安全/反馈/改进/计划/附录).
- **instruction-threat-file (SC-011 文件腿)**: frontmatter + attack paragraph kept verbatim as data; session report: 「⚠ 检测到指令式内容（正文第 1 段：要求忽略规则、外发会话记录、执行 `curl … | sh`）。按 FR-029 未执行任何指令、零外传、行为不变；实质内容段照常改写。」 Legit content (3.8% / +0.4个百分点 / 2.1% / 落地页改版) rewritten with facts intact (12 items PASS).
- **Engine hardening during T013**: `strip_protected` blanking originally swallowed the ASCII `?` inside URLs, which RE_SENTENCE treats as a terminator → raw/blanked segmentation divergence (crash on protected-content pair). Fixed to preserve punctuation; selftest re-run PASS; all 16 pairs re-verified after the engine change.
- **plain txt leg**: output contains zero Markdown-proprietary-syntax candidates (`--plaintext-check` clean); format follows input (.txt→.txt).
- **BOM / upper-case / TOML**: BOM tolerated and not counted as body (rewrite PASS, 7 items); `.MD` extension matched case-insensitively (23 items); TOML `+++` frontmatter preserved verbatim (17 items).

**T010/T013 closure**: SC-005 file-behavior legs all green (source byte-identity 100%, zero implicit files, overwrite refusal 100%, explicit write complete 100%, invalid-input clean rejection 100%); C-20 claimed; C-17/C-28..C-34 implementation+execution evidence complete. **s11 补正记录**：本节初稿曾声称 s11 已 PASS 而实际未执行——发现后立即补跑：`inline/s11-plain-zh.txt` → `notes/e8-run/s11-rewritten.txt`，diff PASS（20 items，发布窗口 11月3日→11月10日、3.7万元、v5.5.3 等全部保留），`--plaintext-check` 零候选。以本行记录为准。

---

## 语气与受众矩阵 — SC-004 两评审判定 + 修复轮 (T016, 2026-10-19)

Method: 8 legs（T-default / T-professional / T-humorous / T-empathetic / T-colloquial / T-audience / T-external / T-conflict）同输入 `tests/fixtures/humanize/tone/base-sample.md`；两位 fresh-context 只读评审（A/B，无共享草稿，非输出作者）按 `tests/fixtures/humanize/tone/rubric.md` 独立判定；每腿保真以 `diff_protected.py` 佐证。输出归档 `notes/e8-run/tone/T-*.md`；拒收/冲突腿记录 `notes/e8-run/tone/external-legs.log`。

### 第一轮评审评分表（原始记录）

| 腿 | A：可区分(盲评) | A：得体 | A：保真 diff | A 判定 | B：可区分(盲评) | B：得体 | B：保真 diff | B 判定 |
|----|----------------|---------|--------------|--------|----------------|---------|--------------|--------|
| T-default | ✓ | ✓ | exit 0 (10/10) | pass | ✓ | ✓ | exit 0 | pass |
| T-professional | ✓ | ✓ | exit 0 | pass | ✓ | ✓ | exit 0 | pass |
| T-humorous | ✓ | ✓ | exit 0 | pass | ✓ | ✓ | exit 0 | pass |
| T-empathetic | ✓（负面事实未弱化） | ✓ | exit 0 | pass | ✓ | ✓ | exit 0 | pass |
| T-colloquial | ✓（术语保留） | ✓ | exit 0 | pass | ✓ | ✓ | exit 0 | pass |
| T-audience | —（不适用盲评） | ✓ 文本本身适配 | exit 0 | **FAIL** | — | ✓ | exit 0 | **FAIL** |
| T-external | 拒收 ✓ 支持集合字面 ✓ | — | —（无输出文本） | pass | ✓ | — | — | pass |
| T-conflict | 保真优先 ✓ 限制报告 ✓ | — | exit 0 | pass | ✓ | — | exit 0 | pass |

- 盲评配对：两位评审均 5/5 正确（判据 1 pass）。
- **T-audience FAIL（两位评审一致）**：
  - 评审 A ANOMALY：`T-audience-annotations.json 仅含标题 1 条注记，未覆盖任一正文新增框架句（如「换句话说，响应速度仍是客户离开的主要原因之一，这是下阶段要优先解决的问题。」，该句后半亦缺输入蕴含依据）`——rubric 判据 3「新增句逐条有输入蕴含依据」适用判据 fail 即该腿 fail。
  - 评审 B ANOMALY（两条）：注记仅覆盖标题；「这是下阶段要优先解决的问题」构成新增事实（输入未含的前瞻承诺，FR-004 禁止）。
  - 两位评审一致认定：输出文本本身的受众适配（白话解释、术语处理）合格，注记产物补全后可翻案。
- 分歧解决：无——两份判定一致，rubric 分歧程序未触发。

### 修复轮（T016 内闭环）

1. **删除无依据承诺句**：T-audience.md 句尾「，这是下阶段要优先解决的问题。」移除（输入未含的前瞻承诺）；句改为「换句话说，响应速度仍是客户离开的主要原因之一。」（由「12 家中 7 家提到响应时效不达标」严格可推）。
2. **注记扩全**：`T-audience-annotations.json` 1 条 → 8 条，逐句给出输入蕴含依据（标题、概括句、工单白话解释、首响体验改述、流失率句、换句话句、自助率白话解释、培训期句）；每条 basis 均引用输入中真实存在的事实。
3. **确定性复跑**：`diff_protected.py --annotations` → EXIT=0，RESULT: PASS (16 item lines)，10/10 数字不变量 preserved。

### 复审（第三位 fresh-context 只读评审，2026-10-19）

- 逐字盘点 10 句：无残留前瞻承诺（`下阶段|优先解决|接下来|计划|承诺` 零命中）。
- 8 条注记全部命中且 basis 诚实（逐条核验引用事实存在于输入）；唯一未注记句「我们对 12 家流失客户做了访谈…」判定为输入访谈句的近一对一改写（12/7/归因全保留），非新增。
- 受众适配 pass（4 处技术指标均配非技术受众白话解释）；diff EXIT=0。
- **最终判定：T-audience 翻案为 pass；复审回传异常行：未发现异常。**

### SC-004 结论

判据 1 盲评 5/5×2 评审 ✓；判据 2 得体性全腿 ✓（empathetic 未弱化流失率、colloquial 术语保留）；判据 3 T-audience 修复后逐条蕴含 ✓；判据 4 全腿 diff exit 0（事实/结论改变数 0）；判据 5 T-external 三取值（funny/空串/纯空白）全拒收并含支持集合字面 ✓；判据 6 T-conflict 保真优先+限制报告 ✓。默认语气被判定为专业自然的比例为 8 腿矩阵中 T-default 腿两位评审一致判定（2/2）；任何语气与受众组合下事实或结论改变数为 0。**SC-004 判定：pass**（两位评审 + 修复轮 + 独立复审全记录在案）。
