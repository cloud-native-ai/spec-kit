# Feature Reference: 043-init-commit-stamp

**Bound Feature**: Feature 045 Framework Source Provenance(`.specify/memory/features/045.md`)  
**Binding rationale**(2026-08-17 `/speckit.clarify` 裁定):**新建** Feature 045——来源溯源(commit 轴)与 024 的 workspace schema 版本轴(迁移注册表/upgrade)正交;024 保持 Draft 不动,双方已互相交叉引用并注明文件名保留(`.specify/version` 归 024 设想,本需求用 `.specify/source.json`)。

## 映射(本需求 → Feature 045 的能力面)

| 本需求交付 | Feature 045 能力面(详情页 Key Changes) |
|------------|------------------------------------------|
| `resolve_source_commit` + `_probe_head_commit`(三态解析/唯一探测文法) | Key Changes 2 前半:checkout 直测 |
| `hatch_build.py` 构建钩子 + `_source_commit.json` 嵌入 | Key Changes 2 后半:分发形态构建期嵌入 |
| `write_source_stamp` + init 调用点(source.json 落章/覆写) | Key Changes 1:来源标识落盘 |
| 重复 init 刷新零残留 / 存量项目零迁移 | Key Changes 3:刷新与兼容 |
| unavailable 哨兵 + 原因、写入失败不阻塞 | Key Changes 4:诚实降级 |

## 对相邻 Feature 的影响

- **Feature 024(Specification Workspace Versioning,Draft)**:零改动——schema 版本轴与来源轴正交;`.specify/version` 路径在 024 详情页显式保留给其设想标记,本需求落 `.specify/source.json`,无文件名冲突。
- **Feature 015(CLI Interface)**:init 属其命令面,但本需求不新增选项/不改交互——015 能力面无变化,仅在 `src/specify_cli/__init__.py` 内部新增函数与一个收尾调用点。
- **Feature 034(CI/CD Pipeline)**:零改动——仓内现状无 workflows/CI;构建为本地 `hatch build`,钩子在本地构建环境内同样生效。若未来 CI 落地,actions/checkout 的浅克隆下 `git rev-parse HEAD` 依旧可用(嵌入不受浅克隆影响;回溯方克隆深度是其自身责任,见 requirements Edge Cases)。
- **Feature 008(Instructions Command)/模板面**:零改动——落章由 CLI 直写,不经模板、不镜像、不改 instructions.md。

## 状态口径

Feature 045 由本 plan 推进 **Draft → Planned**(canonical state machine;`/speckit.implement` 完成后追加 implemented 记录,状态机归属不变)。
