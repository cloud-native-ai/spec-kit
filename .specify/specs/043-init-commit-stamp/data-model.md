# Data Model: 043-init-commit-stamp

实体均为文件系统之上的**增量**;两个新文件形态(目标项目落章文件、包内构建嵌入文件)与一个纯函数返回的瞬态解析值,无数据库、无既有结构改动。

## 1. 框架来源标识(目标项目侧持久化实体,唯一面向用户的落盘物)

| 属性 | 值 |
|------|-----|
| 位置 | `<project>/.specify/source.json`([[STR-001]];与 024 预留的 `.specify/version` schema 轴路径显式互斥) |
| 格式 | JSON,UTF-8,indent 2 |
| 字段 | `framework`: 恒为 `spec-kit`([[STR-003]],字符串,标识来源框架) |
|      | `commit`: 完整 40 位十六进制 git commit id(`^[0-9a-f]{40}$`),或 `unavailable`([[STR-002]]) |
|      | `reason`: 仅当 `commit == unavailable` 时出现的短字符串(不可得原因,如 `git probe failed` / `no embedded source commit`) |
|      | `stamped_at`: UTC ISO-8601 basic 时间戳(`_utc_compact_stamp()`,形如 `20260817T075305Z`) |
| 写入者 | 仅 `specify init`(经 `write_source_stamp`);无其他写入面(Out of Scope) |
| 生命周期 | init 落盘 → 下次 init **整体覆写**(不合并、不追加;旧 commit 零残留,FR-006) → 使用者可删(下次 init 重生,读取方遇缺失=来源未知) |
| 读取语义 | 三态:有效 commit(40-hex)/ 显式不可得(`unavailable` + `reason`)/ 文件缺失(来源未知);**无第四态**——任何实现不得写入占位/臆造 id |

## 2. 构建嵌入文件(框架包侧,分发期生成,面向 init 运行时读取)

| 属性 | 值 |
|------|-----|
| 位置 | `src/specify_cli/_source_commit.json`(随 wheel/sdist 打包;`.gitignore`——构建产物不入库) |
| 生成者 | 仓根 `hatch_build.py` 自定义构建钩子(hatchling custom hook),构建时写入源码树,包目录内文件天然随 wheel 分发 |
| 字段 | `commit`: 40-hex 或 `unavailable`;`reason`: 仅不可得时;`embedded_at`: `_utc_compact_stamp()` 构建时刻 |
| 语义 | **构建环境的**框架源 commit(本地 `hatch build` 于 checkout 内 → 恒可得;无 git 环境构建 → 诚实降级 `unavailable` + 原因);commit 探测复用 CLI 的 `_probe_head_commit`(零第二套文法) |
| 运行时消费 | `resolve_source_commit()` 以 **checkout git 探测 > 嵌入值 > unavailable** 的顺序解析——开发 checkout 下 git 探测恒新(覆盖可能陈旧的嵌入值),site-packages 下探测结构性失败、嵌入值生效 |

## 3. 解析结果(瞬态,纯函数返回,不持久化)

```
resolve_source_commit() -> {"commit": str | None,
                            "origin": "git" | "embedded" | "unavailable",
                            "reason": str | None}
```

- 只解析、不落盘;`write_source_stamp` 消费它格式化 §1 的载荷。
- 探测文法唯一权威 `_probe_head_commit(start_dir) -> (commit | None, reason | None)`:`subprocess.run(["git", "-C", start_dir, "rev-parse", "HEAD"], timeout=5)` + 40-hex 校验;git 缺失/超时/非 git 目录 → `(None, <原因>)`,永不抛异常;构建钩子与运行时经同一函数(禁止第二实现)。

## 4. 关系图(文字)

```
框架仓 checkout ──(hatch build)──> _source_commit.json(嵌入,随 wheel)
     │                                   │
     │(dev 直跑)                        │(site-packages 安装)
     ▼                                   ▼
   git 探测  ────── resolve_source_commit ──────> 嵌入值读取
                    (git > embedded > unavailable)
                          │
                  specify init 末尾 write_source_stamp
                          ▼
        <project>/.specify/source.json(framework/commit/reason?/stamped_at)
                          │
              人在框架仓:git show <commit> → 精确代码切片
```
