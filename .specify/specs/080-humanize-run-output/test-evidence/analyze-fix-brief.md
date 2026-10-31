# Analyze 回环修复简报（079，loop 1/1）

来源：`/speckit.analyze` 2026-10-30，门判 C=0 / H=5。以下为必须关闭的 HIGH 与同批 MEDIUM 的最小修复面。

## HIGH（必须关闭）

- **H-01 结论取值集无 owner**：FR-019 四值、RP-05 五值、Edge Case 第六种文案并存。修复：由 `requirements.md` FR-019 拥有封闭集 `success / partial / failure / aborted / needs-confirmation`，并显式声明 `not-an-action` 的文案与 verdict 映射（建议映射为 `success` + 明示「未执行任何动作」文案，或明确为第六文案但 verdict 取 `success`）；`contracts/report-assembly` RP-05 与 `data-model` E5/E7 改为引用 FR-019，不再各自定义；明确 verdict 的呈现形态（英文 token 还是本地化措辞）。
- **H-02 封闭接线面有名无主**：A11 把封闭集委托给可再生的 tasks.md，SC-006 分母是自选集。修复：A11/SC-006 改为「无限制 grep + 分类规则（活源 / 派生副本 / 镜像 / dated record / 冻结验证）+ 稳定 owner（requirements 内一节或 tasks 冻结清单）+ 闭环守卫（补集与不变量）」；tasks 的 7-path grep 改为无限制发现；不得把封闭集委托给可再生的 tasks.md。
- **H-03 注入防护范围缺口**：FR-025/SC-010/CM-06 只覆盖指令原文与 `--file`/`--inline`；执行体回传的 `final_output`/`evidence`/`products` 与产物内容未声明为 data-not-instructions。修复：FR-025 扩到执行体回传与产物内容；SC-010 增加一条回传注入样本；CM-06 引用扩展后的 FR-025。
- **H-04 失败禁用词表不可测**：SC-003 说「按报告语言索引的封闭词表」但无清单/owner；source 用「成功/完成/通过等」开放式；「完成」与允许的「部分完成」子串冲突。修复：由 requirements 拥有按语言的最小封闭禁用词表（至少 zh/en），并明确子串匹配规则（例如以词边界或先剥离允许短语再匹配）。
- **H-05 Decision Tension 记录不完整**：`validate-decision-tensions.py` 报 3 条 `expected-sacrifice-unmapped` HIGH。修复：`plan.md` T-001/T-002/T-003 的 `expected_sacrifice` 各以恰一个 `SC-NNN Source ↓` 开头（T-001→SC-007；T-002→SC-007；T-003→SC-008 或说明最近来源），复跑校验器到 0。

## 同批 MEDIUM（要求修复）

- **M-01**：FR-011 的 MAY 与 SC-009/EX-04 的必降级冲突 → 统一为 MUST，并写明降级路径的派发计数口径（0 还是 1，建议 0 次真实派发 + 1 条降级记录）。
- **M-02**：FR-030/Edge Case 未限定「运行模式」；「同一仓库」范围与 active-run 观察载体不清；三类拒绝（active-run / output-occupied / nested）无 SC → 限定仅运行模式，定义仓库范围（git work tree root）与观察载体（`.specify/.tmp/humanize/` 占位文件），补 SC。
- **M-03**：SC-007 的网络/重试审计未指名仪器 → 指定「静态扫描 + `git status` + 派发记录行」，并把 T019 加入 SC-007 的覆盖行（tasks 侧）。
- **M-04**：FR-014（上下文装配）无任何契约条款 → 在 `report-assembly` 补一条 clause/test 认领，或在 plan 显式声明 doc-only 及理由。
- **M-05**：FR-004「`--output` 语义沿用」在运行模式失效 → 把 FR-004 收窄到内容模式；运行模式的扩展名集由 FR-024 拥有。
- **M-06**：`--audience` 空值无拒收规则 → 明确「空 audience = 未提供」，或新增 reject code。
- **M-07**：quickstart S3 的「不派发」与 `not-an-action`（已派发）冲突 → 改为「一次派发 + `dispatches: 1` + Evidence `none`」。
- **M-08**：来源清单「实际读取/使用」缺可观察定义；E6 的 `session` 无 `not-read` → 定义 read（摘要/行投影）与 used 的可观察判据，或删除 used 条款。
- **M-09**：用户拒绝确认时无 `denied` 状态 → 增加 `denied` 并给出 verdict 映射（建议 `aborted` + 文案）。
- **M-10**：主会话能否把确认转达给用户未定 → 明确「转达 ≠ 代答，允许转达；子代理 fail-closed」。
- **M-11**：超时未量化 → 委托给宿主/执行体超时 owner，或给出有界等待。
- **M-12**：嵌套 token 集与逃逸方式只在 IP-13 → 在 FR-030 记录封闭 token 规则并给出显式转义/引用方式（避免「更新 /speckit.humanize 文档」被误拒）。
- **M-13**：语言域仅 `zh|latin` → 增加 `other` 或明确回退规则。
- **M-14**：`--output` 文件是否包含载体标记行与迁移提示行未定 → 显式规定（建议写入完整报告，含元数据行；迁移提示仅会话回显）。
- **M-15**：结论「按影响排序」无尺度 → 给出排序依据（用户可见行为 > 接线 > 文档；并列按文件序）或要求执行体声明依据。
- **M-16**：`## Evidence` 写 `none` 与派发记录行冲突 → 定义 `none` 只替代证据指针，派发记录行保留。
- **M-17**：派发记录键名 `dispatches` 无 owner → 加入 Shared Strings 或由 RP-08/EX-21 拥有。
- **M-18**：SC-002「抽样 5 条」无选择规则 → 固定为夹具前 5 条 Key Changes 或全部结论。
- **M-19**：plan Constitution Check IV = Pass vs tasks IV = Partial → 统一为 Partial（template-only 门）或给出独立理由。
- **M-20**：Feature 062 详情元数据陈旧 → `Last Updated`→2026-10-30，Description 改新定位，Key Changes 重新编号（无重复）。
- **M-21**：条款覆盖机制 → tasks 冻结 `coverage-baseline.txt`；修正 IP-15→T025/CM-04、WC-20→T033；WC-05..15 补红先行测试行；加「条款 id ↔ 测试名」核对，或把条款改成 `C-<n>` 再走 `clause_extract.py`。

## 修复归属

- **requirements 轮**：H-01、H-02、H-03、H-04、M-01、M-02、M-05、M-06、M-08、M-09、M-10、M-11、M-13、M-14、M-15、M-16、M-18（及 A4 提示语言、A7 语言域、派发键名若属 STR）。
- **plan/contracts 轮**：H-05、M-04、M-07、M-17、M-19、RP-05/E7/CM-06/IP-16/E2/E6/plan 索引对齐。
- **tasks 轮**：H-02 的发现/守卫、M-03、M-21（覆盖映射与测试行）。

## 复跑

修复后重跑 `/speckit.analyze`（第二轮，也是本轮唯一允许的回环）：目标 C=0 / H=0；M 级须带 disposition。
