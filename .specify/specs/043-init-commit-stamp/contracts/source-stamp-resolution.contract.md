# Contract: 来源解析(resolve_source_commit)

**Spec**: [requirements.md](../requirements.md) FR-004, FR-005, FR-008  
**Surface**: `src/specify_cli/__init__.py`(新增函数)  
**Authority**: git 探测文法唯一权威 = `_probe_head_commit`;本契约只定义解析层,不定义落盘(见 source-stamp-write 契约)

## C-1 探测函数(唯一文法)

```
_probe_head_commit(start_dir: Path) -> tuple[str | None, str | None]
```

- 执行 `git -C <start_dir> rev-parse HEAD`(subprocess,timeout 5s);stdout 逐字符匹配 `^[0-9a-f]{40}$` 才返回 `(commit, None)`。
- git 二进制缺失 / 非零退出 / 超时 / 输出不符 40-hex → `(None, <短原因>)`;**永不抛异常**(解析层不可得是数据,不是错误)。
- 本函数是全仓唯一 git 探测实现——构建钩子(hatch_build.py)经 importlib 加载 `src/specify_cli/__init__.py` 复用它,MUST NOT 存在第二实现(Constitution XII)。

## C-2 解析顺序(恒定)

```
resolve_source_commit() -> {"commit": str | None,
                            "origin": "git" | "embedded" | "unavailable",
                            "reason": str | None}
```

1. **checkout 形态**:`_probe_head_commit(MODULE_DIR)` 成功 → `{"commit": <40hex>, "origin": "git", "reason": None}`(开发 checkout 下 git 恒新,覆盖可能陈旧的嵌入值)。
2. **分发形态**(探测结构性失败):读 `MODULE_DIR / "_source_commit.json"`——存在且 `commit` 为合法值 → `{"commit": <值>, "origin": "embedded", "reason": None}`;嵌入文件缺失/JSON 畸形/字段非法 → 视为无嵌入(原因记入 reason),落到 3。
3. **不可得**:→ `{"commit": None, "origin": "unavailable", "reason": <探测原因 + 嵌入状态合并的短原因>}`。

- 解析**只读**:不写任何文件、不发网络、不读环境变量之外的进程状态。
- 零臆造:`origin=unavailable` 时 `commit` 恒 `None`;任何路径都不得编造 40-hex。

## C-3 嵌入文件读取的容错

- 嵌入文件是构建产物,内容不可信:`json.JSONDecodeError`/`OSError`/字段类型不符 → 等价于"无嵌入",不抛、不告警(最终 unavailable 语义由落章侧披露)。
- 嵌入 `commit == "unavailable"` → 透传不可得语义(`origin="embedded"`,落章侧写 STR-002 + 嵌入 reason)。

## 验证

- `tests/contract/test_source_stamp.py` 解析组——临时真 git 仓夹具(`git init` + commit)monkeypatch `MODULE_DIR` 指入:命中 → `origin=git` 且 commit 与 `git rev-parse HEAD` 一致;指入含嵌入文件的普通目录 → `origin=embedded`;两者皆无 → `origin=unavailable` + reason 非空;畸形嵌入 JSON → unavailable 而非异常;40-hex 断言逐字符。
