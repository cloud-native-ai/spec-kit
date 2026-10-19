# 文件行为夹具清单（`tests/fixtures/humanize/files/`）

覆盖 FR-018/019/021/022/029 与 C-28..C-35 的文件级分支。调用期分支（无实体文件）在 § 调用期分支登记。

## 实体夹具

| 夹具 | 形态 | 验证分支 | 条款 |
|------|------|----------|------|
| `yaml-frontmatter.md` | YAML frontmatter + 中文正文 | frontmatter 逐字保留，仅正文改写 | C-33 / FR-008 |
| `toml-frontmatter.md` | TOML frontmatter + 中文正文 | TOML 同样逐字保留（不得收窄为 YAML） | C-33 / F-02 |
| `plain-sample.txt` | 纯文本 | 输出为纯文本，FR-022 封闭清单核验零 Markdown 语法 | C-32 / FR-022 |
| `empty.md` | 0 字节 | 空文件拒收，不产生输出 | C-29 / FR-019 |
| `frontmatter-only.md` | 仅 frontmatter 无正文 | 视为空输入拒收 | C-29 / L-01 |
| `bom-sample.md` | UTF-8 BOM + 正文 | BOM 容忍且不计入正文，正常改写 | C-29 / L-01 |
| `upper-case.MD` | 大写扩展名 | 扩展名匹配大小写不敏感，按 Markdown 处理 | C-29 / L-01 |
| `binary-sample.dat` | 非 UTF-8 二进制字节 | 二进制/不可解码拒收，不输出乱码 | C-29 / FR-019 |
| `unsupported-sample.pdf` | 不支持扩展名 | 拒收并列出支持格式 `.md/.markdown/.txt` | C-29 / FR-019 |
| `existing-output.md` | 已存在的输出目标 | 未获 `--force` 拒绝覆盖，逐字节不变 | C-31 / FR-021 |
| `input-for-same-path.md` + `symlink-to-input.md`（符号链接 → 输入） | 同路径输出目标 | 真实路径解析相同 → 原地覆盖拒绝 | C-30 / U-06 |
| `input-for-hardlink.md` + `hardlink-alias.md`（同 inode 硬链接，ls -li 验证 link count=2） | 硬链接别名输出目标 | 指向同一底层文件 → 原地覆盖拒绝 | C-30 / U-06 |
| `instruction-threat-file.md` | YAML frontmatter + 指令式内容正文 | 注入防线文件腿：行为改变 0、外发 0、会话提示，frontmatter 保留，实质内容保真改写 | C-35 / SC-011 / FR-029 |
| `protected-content-sample.md` | `{{API_KEY}}`/`${FALLBACK_KEY}` 占位符、URL、版本号、表格、行内命令 | 受保护 token 逐项比对（`diff_protected.py`） | C-17 / F-01 |

## 调用期分支（无实体文件，判定协议见 `rubric.md` § 文件安全协议）

| 调用形态 | 期望 | 条款 |
|----------|------|------|
| 输入路径指向目录（如本目录自身） | 拒绝并指出路径问题 | C-29 |
| 路径不存在 / 不可读 | 拒绝并指出具体路径问题 | C-28/C-29 |
| `--file` 与非空内联同给 | 拒绝（一次只接受一个输入源） | C-28 |
| 既无 `--file` 也无非空内联（含无任何输入） | 拒绝 | C-28 |
| 输出扩展名不受支持（如 `.pdf`） | 拒绝，不创建目标 | C-32 |
| 输出扩展名与输入格式族冲突（Markdown 输入配 `.txt` 输出） | 拒绝，不创建/不修改目标 | C-32 |
| 不可写输出路径（父目录无写权限，测试中以 chmod 临时目录构造） | 报告写入失败、不声称成功、无部分输出 | C-31 / U-05 |
| 一次多个文件 | 拒绝（首版不支持批量） | C-28 |

## 洁净纪律

本目录文件均为评估夹具：`binary-sample.dat`、`unsupported-sample.pdf` 为**故意非法**的字节样本，勿修复；符号/硬链接对是判定夹具，重新生成时须保持指向关系（`ln -sf` / `ln -f`，`ls -li` 验证同 inode）。
