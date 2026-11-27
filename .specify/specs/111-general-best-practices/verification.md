# Verification Log — 111-general-best-practices

<!-- Spec-side derivation from test-evidence/verification-input.md (T019) per the review round-1 hand-back (missing verification.md, closure checker exit 2). Statuses are gate products copied verbatim from the input; no new measurement was invented. -->

# -- Baseline --

baseline_commit=0419adae5
baseline_date=2026-11-27
baseline_branch=111-general-best-practices
baseline_failed_names=223
baseline_failed_names_path=.specify/specs/111-general-best-practices/baseline-failed.txt

# -- Implementation results --

implementation_date=2026-11-27
post_change_commit=65b495b86

# -- Smoke test record (exactly one per feature) --

smoke_command=env SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_general_best_practices.py
smoke_exit_code=0
smoke_evidence_path=.specify/specs/111-general-best-practices/notes/us3-green.txt

# -- Deferred tasks --

deferred_tasks=

# -- Success Criteria evaluation --

SC-001_status=pass
SC-001_value=模块顶层文件集 5/5（README.md + 四个 owner 文件，无额外文件）；清单唯一分类表 3 列 4 数据行、每行恰 1 个相对链接、链接目标集合 = 四个 owner 文件（4/4）；清单 ↔ owner 相对链接可解析 4/4 = 100%；交付态占位「尚无条目」出现数 = 3 且 3 个空分类各零 `## ` 条目（种子文件 1 条目 0 占位；守卫按互斥不变式判定，不冻结数量）
SC-001_note=3 passed in 6.25s，rc 0（腿 (a)(b)(f)；另见快速启动 S-1 / S-2 分段运行各自 rc 0）；notes/us1-green.txt；notes/quickstart-run.md § S-1 / S-2

SC-002_status=pass
SC-002_value=种子条目 `## Git clone 的默认协议` 三项事实齐备（默认用 HTTPS 作 clone URL；特殊仓库走 HTTP/SSH 时必须显式提示协议与凭据；`~/.git-credentials` 记录 HTTP 凭据而 install 以 HTTPS clone 的协议错位反例、导致 clone 失败）+ 延伸 SSH 口径在场；种子无 `**来源**` 行、无编造 feedback id
SC-002_note=1 passed in 6.26s，rc 0（腿 (c)）；notes/us1-green.txt § SC-002；notes/quickstart-run.md § S-3

SC-003_status=pass
SC-003_value=指针链可解析 2/2（`.specify/scripts/python/feedback-utils.py --help` 动作集含 `record`；`shared/guidelines/knowledge-promotion.md` 存在）；`[best-practice]` 标记在清单机制声明中在场；第二机制可判定读数 = 0（`scripts/python/` 下 `best-practices*.py` / `best_practices*.py` 均不存在）；晋升程序与通用判据由清单「逐步积累机制」节自有声明（A-22）
SC-003_note=1 passed in 6.29s，rc 0（腿 (d)）；notes/us2-green.txt § SC-003；notes/quickstart-run.md § S-4

SC-004_status=pass
SC-004_value=框架地图源与镜像各恰 1 行同时带 `.specify/shared/best-practices/` 与 `Feature 111`（2/2；Notes 单元含模块 `README.md` 指针与 `(framework source: shared/best-practices/)`）；`sync-mirrors.py --check` rc 0，`shared/` 对 122 文件字节一致、DIFF 行数 0；init 分发三证据齐备（代码路径引用 + 既有 `test_init_new_layout.py` 运行同一拷贝步骤 rc 0 + `.specify/.tmp/` 只读演练 rc 0 且恰五文档）；`git diff --numstat 0419adae5..HEAD -- src/` 零行
SC-004_note=rc 0；`ok shared/ == .specify/shared/ (122 files, byte-identical)`；腿 (e) 见 notes/us3-green.txt § T015；test-evidence/init-distribution-proof.txt；test-evidence/containment.txt § Zero-difference readings

SC-005_status=pass
SC-005_value=模块五文档 `ai-harness` / `.ah/` / `/ah.` 出现数 = 0 / 0 / 0；模块引用的仓内路径存在率 = 100%（守卫模块读取前导断言，最小集合四条路径每次执行均解析）；归属声明为 `Feature 111`（清单与登记行）
SC-005_note=6 passed in 6.29s，rc 0（smoke 运行同时覆盖前导残留扫描与引用路径存在性）；notes/us3-green.txt § SC-005；notes/us1-green.txt

SC-006_status=pass
SC-006_value=变更路径集 ⊆ FR-009 声明集：`0419adae5..HEAD` 131 路径 = 声明集命中 108 + 三记账存储残余 23（记录体均含特性 key `111-general-best-practices` 或 run id `r20261127T071500Z-111a`）；集合外违规 = 0；引擎/模板/技能/代理/命令/宪法/指令/存储布局/决策治理面改动数 = 0
SC-006_note=A-20 残余判定程序与逐条残余清单记录在 test-evidence/containment.txt（Reading 1 @ f985cca92）；src/ numstat 零行；收口后 wrap-up 记账记录追加最终重读

SC-007_status=pass
SC-007_value=守卫经唯一入口执行 rc 0（6 passed；red-first 记录在场：模块缺席时 6 errors）；镜像参数化套件 888 passed、相对入口基线零新增红；全量套件 frozen-tree 读数失败名集 = 入口基线 223 名（`comm -13` = 0、`comm -23` = 0、`cmp` 字节相同）；run 1 的两个临时新名已归因并保留（age_seconds 跨秒边界抖动；执行体在飞行中改 tasks.md 造成的无效窗口）
SC-007_note=rc 1（仓库既有红）；test-evidence/full-suite.txt（两次运行与归因）；test-evidence/targeted-set.txt；test-evidence/mirror-parity-names.txt（0 entries）；notes/red-first-evidence.md

# -- Runtime Stack joint acceptance (AS-05 / C-18) --

RS-001_joint_acceptance=verified by behaviour on the delivered tree: the module's five-document set is 5/5 with no extras; the manifest's four owner links resolve 4/4; the closed four-category set and the entry form are pinned by the red-first guard (`tests/contract/test_general_best_practices.py`, 6 passed, exit 0); the module ships through the existing `shared/` init copy (init-distribution proof lists exactly five documents).
RS-002_joint_acceptance=verified by behaviour on the delivered tree: the observation→promotion procedure and generality criterion are declared by the manifest's 逐步积累机制 section (A-22) and the pointer chain resolves (`feedback-utils.py --action record` present; `shared/guidelines/knowledge-promotion.md` exists); no second engine file (`scripts/python/best-practices*.py` absent); guard accumulation legs green.
RS-003_joint_acceptance=verified by behaviour on the delivered tree: the framework-map registration row is present in source and mirror; `sync-mirrors.py --check` reports zero drift for this module; the containment reading includes the row; the init distribution proof lists exactly the five module documents.
