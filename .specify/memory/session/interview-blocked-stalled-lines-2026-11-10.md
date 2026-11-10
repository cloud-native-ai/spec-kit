# Interview Ledger: .specify/state/{095,096,097,098}-*-u5-handoff.md + .specify/state/074-goal-team-sdd-unification.md

- **Started**: 2026-11-10
- **Target artifact**: .specify/state/{095,096,097,098}-*-u5-handoff.md + .specify/state/074-goal-team-sdd-unification.md
- **Mode**: informal
- **Branches**: 095 | 096 | 097 | 098 | 074 (五条线相互独立)
- **Recording**: overwrite-style; latest round wins
- **Status legend**: ⬜ open / 🔄 asked / ✅ settled / ⏭ deferred / ↩︎ retracted

| ID | Round | Branch | Question | dependsOn | Status | Decision | Artifact span | Superseded by |
|----|-------|--------|----------|-----------|--------|----------|---------------|---------------|
| D-074 | 1 | 074 | 074 停滞条目的关闭与父级收口 | — | ✅ | 将 074a/074b 回合到 074；SDD 流程新增 split+merge 流程；注册表条目在合并后关闭 | 074 spine §U5 处置；framework split+merge |  |
| D-095 | 1 | 095 | 095 处置:4 条已验 HIGH 与线的去向 | — | ✅ | 重启该线 | 095-u5-handoff.md §4 处置记录 |  |
| D-095-R | 3 | 095 | 095 重启的具体形态(从哪个阶段、修复范围) | D-095 | ✅ | 授权按建议修复 095 的 4 条 HIGH 并重开 analyze 一次 | 095-u5-handoff.md §5 |  |
| D-074-R1 | 2 | 074 | 074a/074b 回合到 074 的具体含义与产物 | D-074 | ✅ | 分片产出合并回写父级：各分片同名输出件(tasks.md 等)合并回 074，含编号重排/语义对齐/词汇表对齐；所有输出件走同一流程；最终确认在 /speckit.seal | 074 spine §访谈裁定；父级输出件 |  |
| D-074-R2 | 2 | 074 | split+merge 流程在 SDD 中的落点与形态 | D-074 | ✅ | 新增 /speckit.seal 命令：按 review 结论封装 spec；sealed 是 Ready for Review 之后的最终态，sealed 后可归档 | 074 spine §访谈裁定；新命令 spec |  |
| D-096 | 1 | 096 | 096 处置:1C+3H 与线的去向 | — | ✅ | 按建议修复：处置 1C+3H 后重开 analyze 一次 | 096-u5-handoff.md §4 |  |
| D-097 | 1 | 097 | 097 处置:3 条已验 HIGH 与线的去向 | — | ✅ | 按建议修复：处置 3H 后重开 analyze 一次 | 097-u5-handoff.md §4 |  |
| D-098 | 1 | 098 | 098 处置:SC-004 目标重定 | — | ✅ | 按建议修复：重定 SC-004 判据后重开 analyze 一次 | 098-u5-handoff.md §4 |  |
| D-POLICY-ANALYZE | 3 | policy | 无人值守 SDD 的 analyze 门应自主修复而非中断 | D-095-R | ✅ | 确认：无人值守 SDD 流程中 analyze 门按建议自行修复并续环，不得中断等待用户确认；该规则写入用户决策判定门（confirmation-gates）；今后 analyze 门均按此执行 | shared/guidelines/confirmation-gates.md § Decision gate；driver analyze 门规则 |  |
