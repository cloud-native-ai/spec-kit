# Contract: feedback-utils.py 引擎 CLI 扩展(047)

引擎(`.specify/scripts/python/feedback-utils.py` 及其框架源 `scripts/python/feedback-utils.py`,两镜像字节一致)为自省流程新增的确定性动作与既有动作扩展。契约条目 `C-N` 编号,供契约测试断言。所有新/扩展动作遵守既有纪律:无网络、无自动传输、条目正文永不改写。

## 新动作:`introspect-register`

```
python3 feedback-utils.py --action introspect-register --report-file <path> [--confirm] [--workspace-root <root>]
```

将一份自省报告注册进存储:结构性校验 → 条目关联写回 → 索引登记。

- **C-1**: 校验 MUST 覆盖 `introspection-report` 契约 C-1..C-10 全部结构性条款 + data-model 校验规则 V-1..V-5;任一违反 → 非零退出并逐条列出违规(既有 `--action probes --validate` 的报告风格),不写任何文件。
- **C-2**: 校验通过且报告 `status=draft`:条目 frontmatter 写 `introspection_ref: "<report-id>#F-<nn>"`(index.json 同步镜像);`index.json.introspections[]` 追加/更新该报告记录;`supersedes` 非空时被承继报告置 `superseded`。
- **C-3**: `--confirm`(用户已在会话中确认报告)时:报告 `status` 置 `confirmed`、写 `confirmed_at`;对报告建议的逐条目处置(见报告扩展字段,下述)批量生效,等价于逐条 `dispose --to <state> --reason <理由> --ref <report-id>#F-<nn>`。
- **C-4**: 幂等:同 `id` 重复 register 更新原记录并重链条目关联,不新增第二条 `introspections[]` 记录;`confirmed` 报告重复 register(无 `--confirm`)不翻案任何已生效处置。
- **C-5**: 报告建议处置的机读载体:`## Findings` 每问题块内可选 `**建议处置**: <entry-id>:<processed|ignored>, …` 行;缺席时 confirm 只置报告状态,不动条目处置。
- **C-6**: register 输出(text/json 随既有 `--format`)MUST 含:`report_id`、`linked`(关联条目数)、`disposed`(生效处置数,confirm 时)、`superseded`(被承继报告 id 或 null)。

## 既有动作扩展:`dispose`

```
python3 feedback-utils.py --action dispose --id <entry-id> [--to processed|ignored] [--reason <text>] [--ref <report-id>#F-<nn>]
```

- **C-7**: `--reason` / `--ref` 为可选;提供时分别写条目 frontmatter `disposition_reason` / `introspection_ref` 并镜像入 index.json;不提供时行为与现状逐字节一致(零回归)。
- **C-8**: `--ref`  MUST 匹配 `^introspection-[0-9TZ-]+#F-[0-9]{2,}$`,否则非零退出;引用不强制要求报告已存在(允许先 dispose 后 register 的落单顺序,但 register 时会以报告为准重链)。

## 既有动作扩展:`package`

```
python3 feedback-utils.py --action package [--include-introspection]
```

- **C-9**: `--include-introspection` 提供时:对本批入选条目(既有选择规则不变:created > submitted_at 或 `--all`,排除 external)收集其 `introspection_ref` 指向的报告文件集,以 `introspection/<report-id>.md` 路径并入 zip;MANIFEST.md 末尾追加 `## Introspection Reports` 节,逐行列 `report-id | 关联条目数 | status`。
- **C-10**: 未提供该 flag 时打包行为与现状逐字节一致(SC-004 零回归);条目无 `introspection_ref` 时 zip 不含 `introspection/` 目录、MANIFEST 不含该节。
- **C-11**: 引用报告文件缺失(被手动删除)时:打包不失败,MANIFEST 该行标注 `(missing)`;zip 内不含该文件。
- **C-12**: 外部条目恒不入包(既有红线);其 `introspection_ref` 报告若仅覆盖外部条目,则永不因本 flag 入包。

## 只读支撑(复用既有动作,零新增)

- **C-13**: 自省范围快照与条目摘要由既有 `--action list --disposition open --kind internal --format json`(摘要投影,summary-first)提供;引擎不为自省新增只读动作。
- **C-14**: `--action status` 输出不变;阈值提示语层的"可先自省再打包"建议由命令模板文案承担,引擎不改。

## 退出码

- **C-15**: 校验失败 = 2(与 `--action probes --validate` 一致);成功 = 0;参数错误 = argparse 既有 2。无新退出码种类。
