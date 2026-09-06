---
id: "20260903T145945Z-skill-create-skills"
unit_id: "skill:create-skills"
unit_type: "skill"
run_id: "create-skills-git-server-init-20260903"
scope: "local"
probe: "skill-create-skills-wrapup"
kind: "internal"
slice: "skills"
partial: false
created: "2026-09-03T14:59:45Z"
summary: "以 spec-kit 仓库根 skills/ 为 canonical 源创建 git-server-init（把普通 SSH 服务器置备为 Git 服务器：git 用户 + 裸仓库 + 公钥授权 + 本机 ssh config 条目）。走完 Step 0 模式判定（Spec Kit project mode）、跨 SSOT 命名冲突扫描（8 处加载目录零命中）、可写性预检、脚手架、身份定稿、校验（"
---

## Review
以 spec-kit 仓库根 skills/ 为 canonical 源创建 git-server-init（把普通 SSH 服务器置备为 Git 服务器：git 用户 + 裸仓库 + 公钥授权 + 本机 ssh config 条目）。走完 Step 0 模式判定（Spec Kit project mode）、跨 SSOT 命名冲突扫描（8 处加载目录零命中）、可写性预检、脚手架、身份定稿、校验（skills-utils validate=true、resolve 命中镜像实体无 fallback）、契约套件基线对照、真实冒烟验证（以 baremetal_9 端到端置备，关1/关2/关3b 全绿，关3a 因本机云壳 DLP 禁推而不可执行并已显式声明）、Step 7 角色匹配（本 fork 无点名的 7 个角色 agent，无匹配故不传播）。冒烟验证捕获并修复两个真实缺陷，且纠正了自身文档中一处关于 IdentityFile 语义的错误论断（实测证明它是列表型累加选项，不适用 first-match-wins）。

## Optimization Points
- 脚手架 `create-new-skill.sh --output-dir <mirror-source>` 生成的 `skill_id` 会带上自定义输出目录（本次为 `<SKILL:skills/git-server-init/SKILL.md>`），而仓库内全部既有兄弟技能一律用已安装规范路径 `<SKILL:.specify/skills/<name>/SKILL.md>`；同一份生成文件里 `## Resource ID` 的 Canonical Path 又写的是 `.specify/skills/...`，自相矛盾。建议：脚手架在 `--output-dir` 指向某个镜像对（如 `skills/`）的 canonical 源时，把 skill_id 归一化到镜像侧的已安装路径，或至少让 skill_id 与 Canonical Path 两处取值一致。
- Step 7 硬编码「读 `.specify/agents/templates/` 下 7 个内置角色 agent」（requirements-analyst / system-designer / module-designer / test-engineer / qa-engineer / knowledge-manager / ux-analyst），但本 fork 该目录下只有 `skill-verifier` 与 `structure-adjuster` 两个 Meta agent，7 个点名对象全部不存在。建议：Step 7 改为「枚举 `.specify/agents/templates/*.agent.md` 实际内容再判断角色匹配」，不预设固定名单——这与本仓库既有的「硬编码计数/名单是脆弱信号」教训同源。
- Step 6 要求跑 `pytest tests/contract/ -q -k "skill or runtime_mode"` 但未要求先建基线。实测该选择器下有 15 项既有失败（含 `test_skills_mirror_parity`、`test_skill_home_workdir_template` 系列），照字面执行会把既有基线失败误读成新技能引入的回归。本次靠「临时移出技能目录再跑一次做对照」才定性。建议：Step 6 显式引用 AGENTS.md 的测试基线纪律，并把「加/不加新技能两次运行结果必须一致」写成判定口径。
- token-efficiency：本次冒烟验证中 push 失败的归因走了约 6 轮试探（先怀疑 hooks、再怀疑 ssh 二进制、再怀疑 stdin 管道、再做本地 push 对照），而**决定性对照实验（向另一台已知稳定运行多年的 server push）本应第一步就做**。固定顺序应为「先跨对象对照定性（客户端 vs 服务端），再深挖机制」。已把该纪律写进新技能的 references/troubleshooting.md 症状 3b，但 create-skills 自身在「实测验证」环节缺少这条排查顺序指引。
- 新技能实测捕获并修复了两个真实缺陷（脚手架与文档审阅都发现不了）：① `mkdir -p` 在 sudo 下创建的命名空间目录留下 root 属主，导致 git 用户无法在该命名空间下自建仓库，而两份参考机均为 git:git；② 原「关 3：真实 push」门禁把服务器正确性与客户端环境耦合，本机 DLP 类安全软件禁推时门禁恒失败——已改造为关 3a（本机 push）/ 关 3b（服务端写路径判据）双路。佐证 Step 6.5 对 utility 技能「以真实冒烟调用替代 RED-GREEN」的要求是有效且必要的，不宜放宽。
