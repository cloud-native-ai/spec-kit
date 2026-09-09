# Git Workflow Branch Roles

Machine-maintained by the `git-workflow` skill — the managed block below is the
**single source of truth** for branch roles in this project; do not edit it by hand.
`.specify/instructions.md` carries only a pointer to this file.

<!-- GIT_WORKFLOW_START -->
<!-- Record one row per branch role (MAIN / PRE / DEV). While no workflow is established, keep the `None yet.` row. -->
| Role | Branch | Tracking | Purpose |
|------|--------|----------|---------|
| MAIN | `master` | `gitlab/master` | 主干:接收已通过验证的特性合并;推送时 `github/master` 与 `gitee/master`(同一 fork 的镜像)一并更新 |
| PRE | *(不适用)* | - | 本项目采用 SDD 开发模式的分支规范,无预发层 |
| DEV | *(不适用)* | - | 同上,无长期开发层;开发在短命特性分支上进行 |

- **Sync chain (rebase)**: 不适用 —— 无 PRE/DEV 层,故无层间 rebase 链
- **Merge chain**: `master <- NNN-<slug>` —— 特性分支自 `master` 切出,完成后合回 `master`
- **Feature branch convention**: `NNN-<slug>`(`NNN` = 需求编号,如 `050-proactive-flow-trigger`);合并后删除本地分支(`git branch -d`,已合并才允许)
- **`.gitexcludes`**: 不适用 —— 该机制用于层间同步时保护分支专属文件,本项目无层间同步,故无消费者;若将来引入 PRE/DEV 再初始化
- **⚠ NOT a sync peer**: `main`(tracks `github/main`)属**上游项目** `github/spec-kit` 的另一条世系,相对 `master` 为 539 ahead / 1507 behind。它不是 `master` 的别名,不参与本工作流的任何同步或合并;把它当作 MAIN 会让每次同步都面对巨大分叉
- **⚠ Remote roles**: `origin` = 上游 `github/spec-kit` —— **只读参照,禁止推送**;`github` / `gitlab` / `gitee` = 同一 fork `cloud-native-ai/spec-kit` 的三处镜像。注意 `remote.origin.url` 指向上游而非本 fork,故任何 `{REPO_URL}@{SHA}` 形式的引用都不可解析
- **Last updated**: 2026-09-09
<!-- GIT_WORKFLOW_END -->
