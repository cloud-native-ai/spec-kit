# Contract: 构建期嵌入(hatch_build.py)

**Spec**: [requirements.md](../requirements.md) FR-004(分发形态可得)、FR-005(诚实降级)  
**Surface**: 仓根 `hatch_build.py`(新)× `pyproject.toml`(hook 声明)× `.gitignore`(嵌入产物)  
**Authority**: commit 探测复用 `src/specify_cli` 的 `_probe_head_commit`(source-stamp-resolution 契约 C-1)——构建期与运行期同一文法,零第二实现

## C-1 钩子行为

- 实现 hatchling **custom build hook**:`class SourceCommitHook(BuildHookInterface)`,`initialize()` 阶段执行;
- 计算:经 importlib(`spec_from_file_location`)加载 `src/specify_cli/__init__.py`,调用其 `_probe_head_commit(<仓根>)` 得 `(commit | None, reason | None)`——仓根 = 钩子文件父目录;
- 写入 `src/specify_cli/_source_commit.json`:

```json
{
  "commit": "<40-hex> | \"unavailable\"",
  "reason": "<仅不可得时>",
  "embedded_at": "20260817T075305Z"
}
```

- 钩子对 wheel 与 sdist 两个 target 均生效(同一文件,幂等覆写);包目录内文件由既有 `[tool.hatch.build.targets.wheel] packages` 配置天然随 wheel 分发,不需额外 force-include。

## C-2 失败语义

- **探测失败 ≠ 构建失败**:`_probe_head_commit` 返回 None → 嵌入 `unavailable` + reason,构建照常完成(诚实降级沿 FR-005;如 tarball/无 git 环境构建);
- **写入失败 = 构建失败**:`_source_commit.json` 无法写入(权限/磁盘)→ 钩子抛错终止构建——宁可不出包,不出版本面撒谎的 wheel。

## C-3 声明与版本管理

- `pyproject.toml` 增:

```toml
[tool.hatch.build.hooks.custom]
path = "hatch_build.py"
```

  (pyproject.toml 在仓写门禁 confirm 名单——implement 期编辑前需用户确认);
- `.gitignore` 增 `src/specify_cli/_source_commit.json`(构建产物不入库;dev checkout 内残留旧构建产物不会污染 git 状态);
- 钩子文件仅用 stdlib + hatchling 构建环境自带的 `hatchling` API(`hatchling.builders.hooks.plugin.interface`),不引入新的 requires。

## C-4 与运行时的衔接

- 嵌入文件是**数据**,不是代码:运行时 `resolve_source_commit()` 按 resolution 契约 C-2 顺序消费它(checkout git 探测优先,嵌入值兜底);
- 嵌入 `unavailable` 会被落章侧透传为 STR-002 + reason——分发期与运行期两级诚实降级链路闭合。

## 验证

- `tests/contract/test_build_hook.py`——importlib 加载仓根 `hatch_build.py`:① monkeypatch 探测函数返回固定 commit → `initialize()` 后嵌入文件逐字段断言;② 探测返回 None → `unavailable` + reason;③ 断言钩子调用的探测函数与 `specify_cli._probe_head_commit` 为**同一函数对象**(防第二文法);④ monkeypatch 写入抛 OSError → initialize 抛错(构建失败语义);
- 集成收口(implement 期可选实跑):`hatch build` 一次,解包 wheel 断言 `_source_commit.json` 在包内且 commit == 当前 HEAD。
