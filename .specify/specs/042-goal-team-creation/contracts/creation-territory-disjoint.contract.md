# Contract: 创建期 territory 两两不相交校验(territory 面)

**Spec**: [requirements.md](../requirements.md) FR-012, FR-013  
**Surface**: `skills/create-team/scripts/verify-territory-disjoint.py`(新,薄 I/O 包装)× `skills/create-team/references/create-mode.md`  
**Authority**: 重叠判定文法 = `build-summary-input.py` 的 `expand_scopes` / `scopes_overlap` / `overlap_verdict` / `detect_overlaps`(036/037 落地)——**import 复用,零第二文法**

## C-1 CLI 契约

```
python3 skills/create-team/scripts/verify-territory-disjoint.py \
  --input <proposals.json> [--repo-root <root>] [--json]
```

- 输入 JSON schema 见 [data-model.md §5](../data-model.md):`{goal_slug, teams[]}`,每条含 `write/read/forbidden/non_path`,值域与 team.md frontmatter `territory` 键一致。
- 校验对象 = 输入中的提议团队 **∪** 磁盘上同 `goal_slug` 的既有团队(从 `.specify/teams/*/team.md` frontmatter 读取);未声明 territory 的既有团队按既有语义记 `undecidable`,不猜测。
- 判定:对每对团队输出 `overlap_verdict` 三值之一;`non_path` 条目只列出供仲裁,永不参与求交(沿 037 语义)。

## C-2 退出码与输出

| 退出码 | 语义 |
|--------|------|
| `0` | 全部两两 `no-overlap`(write 域互不相交) |
| `2` | 输入 JSON 非法 / schema 不符(逐字段报错) |
| `3` | `--repo-root` 下无 `.specify/teams/` 或 goal_slug 解析失败 |
| `4` | 存在 `overlap`(列出争用区路径)或 `undecidable`(列出未声明方) |

- `--json` 输出 `{verdicts: [{a, b, verdict, contested?: [...]}], summary}`;人读模式逐对打印。退出码是 verdict,调用方 MUST 上报不得争论。

## C-3 创建流程集成(FR-012)

- 多团队方案的确认门禁 MUST 附 verify 结果:`exit 0` → 提议划分随各 team.md 落盘;`exit 4`(任何 overlap/undecidable)→ **MUST NOT 静默落盘已知重叠**——披露争用区/未声明方,人工改划后重跑,或移交 `/speckit.goal coordinate`(既有提议形重划,人批准)。
- 单团队路径:若同 goal 已有其他团队,同样 MUST 跑 verify(新团队的写域 vs 既有团队)——重叠同样披露并移交 coordinate;仅当该 goal 下无其他团队时免跑。
- 脚本自身零写入:只读输入 JSON 与 team.md frontmatter,输出 verdict;territory 的落盘仍由创建流程写 team.md。

## C-4 边界

- glob/brace 展开语义(如 `{a,b}/c`)与 summary 期一致(同一 `expand_scopes`),不另立展开规则;保守前缀嵌套判定(`scopes_overlap`)逐字复用。
- 跨 goal 团队不参与本校验(territory 纪律以共享同一 `goal_slug` 为界,沿 037)。
- 提议条目中的 `read`/`forbidden` 只呈现不拦截(write-write 才是争用;与既有 Overlap Finding 语义一致)。

## 验证

- 单元/契约测试:`tests/contract/test_goal_team_creation.py` 内 verify 组——构造提议集 + 既有团队夹具:全不相交 exit 0;write 相交 exit 4 + contested 路径;未声明既有团队 exit 4 + undecidable;非法 JSON exit 2;non_path 不参与求交。
- 文法一致性钉:脚本对相同输入的 verdict 与直接调用 `detect_overlaps` 一致(防包装层引入分叉)。
