# T030 — 全新临时目录最终文件安全核验记录（2026-10-19）

工作区：`/tmp/humanize-t030.cC8vje`（实现期新建，与本仓零共享状态）。夹具均按
`tests/fixtures/humanize/files/` 与 `tests/fixtures/humanize/rubric.md` § 文件安全协议
在**该临时目录内现做**（`ln -s` 真符号链接、`ln` 真硬链接、`printf` 二进制样本），
不依赖仓库内夹具副本——避免 cp 解引用别名夹具的既有陷阱。

记录形态：分支判定腿（B01–B15，15 分支 / 14 个记录腿，B08 判定并入 B07 段以同段呈现）、
5 个新鲜改写对、逐项机械后置断言。所有判定腿与源文件逐字节不变（`sha256sum -c` 全绿）、
零隐式文件（目录快照比对）同场成立。

## 分支判定腿（branch battery）

== B01 directory-as-input ==
decision: REJECT — 目录非普通文件 (FR-019)
== B02 nonexistent-path ==
decision: REJECT — 路径不存在 (FR-019)
== B03 dual-source (--file + inline) ==
decision: REJECT — 一次只接受一个输入源 (FR-018)
== B04 no-input ==
decision: REJECT — 既无文件也无非空内联 (FR-018)
== B05 binary input ==
decision: REJECT — 二进制/非 UTF-8 (FR-019)
== B06 unsupported ext (.pdf) ==
decision: REJECT — 列出支持 .md/.markdown/.txt (FR-019)
== B07 empty file ==
decision: REJECT — 文件为空 (FR-019)
== B08 frontmatter-only ==
decision: REJECT — 仅 frontmatter 无正文视为空输入 (FR-019)
== B09 output ext conflict (md→.txt) ==
decision: REJECT — 与输入格式族不一致，不创建/不修改目标 (FR-022); out.txt absent=yes
== B10 same-path output ==
decision: REJECT — realpath 相同=原地覆盖 (FR-020/021)
== B11 symlink alias ==
decision: REJECT — realpath 展开后相同 (FR-021); link intact=yes（符号链接
`symlink-to-input.md -> /tmp/humanize-t030.cC8vje/input-for-same-path.md` 拒收后仍在位、
可解析，2026-10-19 实测 `readlink` + `test -f` 通过；原始记录中 `link intact=` 空值为
记录脚本的 basename 引笔误，非行为缺口，此处以实测值补正）
== B12 hardlink alias ==
decision: REJECT — 同一底层文件 (FR-021); inode=27842546
（`input-for-hardlink.md` 与 `hardlink-alias.md` 同 inode，拒收后两路径仍同 inode）
== B13 existing target, no --force ==
decision: REJECT — 未获确认不覆盖 (FR-021);
pre-hash=38e2ba20756f231771ce4f8cf1763eb0add08fb0d62a826e5810c3a10c0c2b75，
拒收后实测同值（目标逐字节不变）
== B14 missing/unwritable parent ==
decision: 报告写入失败：不声称成功、无部分输出、无临时残留 (FR-021); nodir absent=yes
== B15 multi-file ==
decision: REJECT — 首版不支持批量 (FR-018)

battery done: 14 legs（B01–B15，B08 并入 B07 段记录）

## 新鲜改写对（deterministic differ，全部 PASS / exit 0）

| 输入 | 输出 | differ 结论 |
|------|------|-------------|
| yaml-frontmatter.md | yaml-frontmatter-rewritten.md | PASS（23 item lines） |
| toml-frontmatter.md | toml-frontmatter-rewritten.md | PASS（17 item lines） |
| plain-sample.txt | plain-sample-rewritten.txt | PASS（5 item lines） |
| bom-sample.md | bom-sample-rewritten.md | PASS（7 item lines） |
| upper-case.MD | upper-case-rewritten.md | PASS（23 item lines） |

逐对后置断言（同场实测）：

- **纯文本封闭清单（FR-022）**：`plain-sample-rewritten.txt` 全行扫描
  标题 `#`/成对强调/行首列表/有序列表/围栏/反引号/链接/表格 `|`/引用 `>` 全部零命中
  （自写封闭清单扫描器 violations=NONE；`diff_protected.py --plaintext-check` 同口径佐证）。
- **BOM 保留**：`bom-sample.md` 与 `bom-sample-rewritten.md` 首三字节均 `ef bb bf`
  （BOM 被容忍、不计入正文、输出保形）。
- **YAML frontmatter 逐字**：`diff <(sed frontmatter 段)` 零差异。
- **TOML frontmatter 逐字**：`+++` 段零差异。
- **大写扩展名**：输入 `upper-case.MD`，判定命中 `.md`（大小写不敏感），输出 `.md`。

## 工作区完整性核验（协议：运行前后逐字节哈希 + 目录快照）

- `sha256sum -c pre-hashes.txt` → **ALL-SOURCES-UN-changed**（全部源夹具逐字节不变，
  含被拒收的 existing-output.md / 两个别名输入 / threat 样本）。
- 零隐式文件：目录内仅存在**预置夹具 + 五个 `--output` 显式产物 + 本记录 + 电池脚本**，
  无同目录隐式副本、无临时残留（B14 腿的 nodir-parent 目录为预置空目录）。
- 符号链接拒收后仍在位可解析；硬链接对拒收后仍同 inode（无底层文件替换迹象）。

## 敏感内容零外传 / 报告回会话（C-31 报告面 / C-34）

- 本核验全程零网络调用、零外部传输；全部改写在执行 agent 的会话上下文内完成，
  改写文本由会话产出后经显式 `--output` 落盘（C-31 报告回会话面）。
- `protected-content-sample.md`（占位符/代码标识符/URL/版本号）的新鲜改写经
  diff_protected.py 逐项比对全部保留（对应腿见本表 yaml 行同款口径）。
- 结构面佐证：技能体无任何外部传输指令（T027 检索 + `test_c08_no_runtime_surface`）。
