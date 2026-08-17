# Verification Log — 043-init-commit-stamp

# -- Baseline (recorded once, BEFORE any /speckit.implement work changes the tree) --

baseline_commit=0cc13ff8^ (branch head at run start)
baseline_date=2026-08-17
baseline_branch=043-init-commit-stamp
baseline_failed_tests=47  # name-level list: baseline-failed.txt in this directory
baseline_total_passed=1890

# -- /speckit.implement results --

implementation_date=2026-08-17
post_change_failed_tests=46  # 47 baseline minus 1 now-green (registry count pin synced 44→45 with Feature 045 registration); zero NEW failures (comm -13 empty)
post_change_total_passed=1937  # +47 new tests across 3 new files
post_change_wheel_build=exit 0; wheel contains specify_cli/_source_commit.json with commit == HEAD char-exact

# -- Success Criteria evaluation --

SC-001_status=pass
SC-001_value=stamp 存在率 100%;commit 与 git rev-parse HEAD 逐字符一致
SC-001_note=集成 test_init_source_stamp(真实 git 探测路径)+ 契约解析组真 git 仓夹具;wheel e2e 实测 stamp==嵌入值==构建时 HEAD

SC-002_status=pass
SC-002_value=双 commit(HEAD/HEAD~1)落章后 git show --quiet 均 exit 0;0 次命中错误切片
SC-002_note=tests/integration/test_init_source_stamp.py::test_reverse_lookup_hits_both_stamped_commits

SC-003_status=pass
SC-003_value=哨兵记录率 100%;臆造 id 0 次;落章导致 init 失败 0 次
SC-003_note=契约降级组 + 集成 test_unavailable_resolution_still_leaves_init_green(exit 0 + unavailable+reason);40-hex 正则钉防臆造;write 失败返回 False 黄色告警

SC-004_status=pass
SC-004_value=升级刷新后旧 commit 残留 0
SC-004_note=契约 test_refresh_overwrites_with_zero_stale_residue(grep 旧 id 0 命中,新值在场)+ 集成 --here --force 再 init 刷新

SC-005_status=pass
SC-005_value=正式版本号作唯一标识 0 次
SC-005_note=test_payload_values_never_carry_the_formal_version(读 pyproject version 比对全部载荷值);commit 键取值域 = 40-hex | unavailable(契约钉)

# -- Deferred tasks --

deferred_tasks=none  # 19/19 closed; T016 升级为实跑(pip 镜像可达,真实 wheel 构建闭环)未走 [~]

# -- Notes --

- note=设计期修正:构建钩子不能加载整个 specify_cli.__init__(构建环境无 typer/rich)→ 探测/解析/时间戳抽为 stdlib-only 子模块 specify_cli/_provenance,运行时与钩子同对象复用(对象同一性被 test_build_hook 钉死);__init__ 的 _utc_compact_stamp 同步别名化,消双实现。
- note=实测缺陷修复:hatchling 不保证收录 initialize 期间写出的文件——首版 wheel 缺 _source_commit.json,经 build_data force_include 显式注入后重建验证通过(两次真实构建对比)。
- note=既有事实澄清:裸 checkout 直跑 init 因模板仅随 wheel 分发而不可用(pre-043 即如此)——quickstart §1 与 installation.md 已按实测改写(wheel 安装形态 ✅;editable 安装为 git 探测形态)。
- note=环境串台:shell PYTHONPATH 指向无关项目遮蔽 pip 安装的 build 包;`env -u PYTHONPATH` 规避,已具名记录。
- note=顺手修正(非 043 范围):Feature 045 注册使 test_c3_features_header_count 计数钉过期(44→45),按 pin-hygiene 同步修正,基线 47→46 属改善非回归。
- note=pyproject.toml 编辑经仓写门禁 confirm 流程获用户批准(2026-08-17,AskUserQuestion 存档于会话)。
- note=端到端(T019,/tmp/043-e2e):venv 装 wheel → specify init exit 0 → stamp {framework: spec-kit, commit: decf8101…, stamped_at} → git show 命中 US2 提交;checkout-origin(git 探测)由集成测试证明。
