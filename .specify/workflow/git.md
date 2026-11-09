# Git Workflow (Spec Kit framework)

Machine-maintained by the `git-utils` skill (scope A) — the managed block below is the
**single source of truth** for the git workflow **under the Spec Kit framework**: the
declared model, branch structure, and the close-out discipline followed by both human
developers and the framework's unattended mechanisms. Do not edit it by hand.
`.specify/instructions.md` carries only a pointer to this file.

> **Why this is not a developer's personal git flow:** Spec Kit runs unattended
> mechanisms (SDD loop driver, periodic house-keeping, feedback digest, automatic
> close-out) that commit, merge, and push on a programmatic cadence. The declared
> workflow therefore constrains both human and automated executors, and the state
> file lives on the framework runtime surface (`.specify/workflow/`) rather than in
> the documentation space.

<!-- GIT_WORKFLOW_START -->
<!-- Workflow model is a framework-level declaration under Spec Kit (menu: single-branch / dual-branch / temp-branch / MAIN-PRE-DEV three-tier; single-branch never even creates temp branches); the declaration below records THIS project's choice, followed by its operating rules. While no workflow is established yet, keep the `None yet.` line as the model declaration so Bootstrap can detect the unfilled state. -->
- **Workflow model**: 临时分支（trunk-based）—— 单主干 + 短命特性分支；开发在临时分支上进行，完成即合入主干并删除
- **Trunk**: `master`（tracks `gitlab/master`；推送时 `github/master` 与 `gitee/master` —— 同一 fork 的镜像 —— 一并更新）
- **Feature branch convention**: `NNN-<slug>`（`NNN` = 需求编号，如 `050-proactive-flow-trigger`）；自 `master` 切出，完成后合回 `master`，随即删除本地分支（`git branch -d`，已合并才允许）
- **`.gitexcludes`**: 未初始化 —— 该机制服务层间同步的分支专属文件保护，本模型无长期并行层，无消费者；将来改声明三层模型时再初始化
- **⚠ NOT a sync peer**: `main`（tracks `github/main`）属**上游项目** `github/spec-kit` 的另一条世系，相对 `master` 大幅分叉（2026-10-13 本地 ref 口径实测：ahead 736 / behind 716）。它不是 `master` 的别名，不参与本工作流的任何同步或合并；把它当作 MAIN 会让每次同步都面对巨大分叉
- **⚠ Remote roles**: `origin` = 上游 `github/spec-kit` —— **只读参照，禁止推送**；`github` / `gitlab` / `gitee` = 同一 fork `cloud-native-ai/spec-kit` 的三处镜像。注意 `remote.origin.url` 指向上游而非本 fork，故任何 `{REPO_URL}@{SHA}` 形式的引用都不可解析
- **Closeout**: `ask`（四值闭集 `commit+merge+push` / `commit+merge` / `commit-only` / `ask`；缺失或未填即取 default `ask`，不得从相邻行推断取值）—— 收口序列由 `git-utils` 技能 scope A 的 `closeout` 操作按本块模型推导并呈现，本行只声明策略
- **Closeout remotes**: `github`, `gitlab`, `gitee`（同一 fork 的三处镜像；`origin` 只读上游按角色排除，不得出现在此列表；显式空列表 empty 或未填 absent 即 "no pushable remote"，推送步退化为 skipped 并在报告说明原因）
- **Last updated**: 2026-11-09
<!-- GIT_WORKFLOW_END -->
