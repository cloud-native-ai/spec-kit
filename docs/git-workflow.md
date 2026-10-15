# Git Workflow

Machine-maintained by the `git-utils` skill (scope A) — the managed block below is the
**single source of truth** for this project's declared git workflow model and branch
conventions; do not edit it by hand.
`.specify/instructions.md` carries only a pointer to this file.

<!-- GIT_WORKFLOW_START -->
<!-- Workflow model is a per-project choice (menu: single-branch / dual-branch / temp-branch / MAIN-PRE-DEV three-tier; single-branch never even creates temp branches); the declaration below records THIS project's choice, followed by its operating rules. While no workflow is established yet, keep the `None yet.` line as the model declaration so Bootstrap can detect the unfilled state. -->
- **Workflow model**: 临时分支（trunk-based）—— 单主干 + 短命特性分支；开发在临时分支上进行，完成即合入主干并删除
- **Trunk**: `master`（tracks `gitlab/master`；推送时 `github/master` 与 `gitee/master` —— 同一 fork 的镜像 —— 一并更新）
- **Feature branch convention**: `NNN-<slug>`（`NNN` = 需求编号，如 `050-proactive-flow-trigger`）；自 `master` 切出，完成后合回 `master`，随即删除本地分支（`git branch -d`，已合并才允许）
- **`.gitexcludes`**: 未初始化 —— 该机制服务层间同步的分支专属文件保护，本模型无长期并行层，无消费者；将来改声明三层模型时再初始化
- **⚠ NOT a sync peer**: `main`（tracks `github/main`）属**上游项目** `github/spec-kit` 的另一条世系，相对 `master` 大幅分叉（2026-10-13 本地 ref 口径实测：ahead 736 / behind 716）。它不是 `master` 的别名，不参与本工作流的任何同步或合并；把它当作 MAIN 会让每次同步都面对巨大分叉
- **⚠ Remote roles**: `origin` = 上游 `github/spec-kit` —— **只读参照，禁止推送**；`github` / `gitlab` / `gitee` = 同一 fork `cloud-native-ai/spec-kit` 的三处镜像。注意 `remote.origin.url` 指向上游而非本 fork，故任何 `{REPO_URL}@{SHA}` 形式的引用都不可解析
- **Last updated**: 2026-10-13
<!-- GIT_WORKFLOW_END -->
