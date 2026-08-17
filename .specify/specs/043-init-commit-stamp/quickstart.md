# Quickstart: 043-init-commit-stamp

从零走一遍"init 落章 → 读标识 → 反向回溯代码切片"。

**验证标注**:标 ✅ 的命令已在仓内实际执行验证(2026-08-17);标 📌 的是本需求新增面,由契约测试钉住(`tests/contract/test_source_stamp.py`、`test_build_hook.py`、集成 `test_init_source_stamp.py`),实现合入后方可照抄执行。

## 0. 前置

```bash
git rev-parse HEAD          # ✅ 框架仓当前 commit,落章的期望值(40-hex)
```

## 1. 安装形态:init 落章(2026-08-17 实测)

```bash
cd <spec-kit 仓> && python3 -m build --wheel          # ✅ 构建钩子嵌入源 commit
python3 -m venv /tmp/venv && /tmp/venv/bin/pip install dist/specify_cli-*.whl
cd /tmp && mkdir stamp-demo && cd stamp-demo
/tmp/venv/bin/specify init demo-proj --ai qoder --no-git --ignore-agent-tools --skip-tls   # ✅ exit 0
```

上例实测产出 `demo-proj/.specify/source.json`(commit == wheel 内嵌入值):

```json
{
  "framework": "spec-kit",
  "commit": "<框架仓 HEAD 的 40-hex>",
  "stamped_at": "20260817T……Z"
}
```

安装形态 commit 来自构建嵌入(`origin=embedded`);开发 checkout(editable 安装)下经 git 探测(`origin=git`,由集成测试钉);不含 `reason` 键(可得时不出现)。注:裸 checkout 直跑 `python3 src/specify_cli/__init__.py init` 因模板仅随 wheel 分发而不可用(既有事实,与本需求无关)。

## 2. 反向回溯(用户核心动作)

```bash
cd <框架仓> && git show <上一步读到的 commit> --stat   # ✅ git 既有面;📌 配对输入来自 source.json
```

一条命令命中产出该脚手架的精确代码切片——不需要目标项目保存框架仓副本。

## 3. 升级刷新

```bash
# 框架仓前进到新 commit 后,再次 init(升级路径):
python3 <repo>/src/specify_cli/__init__.py init demo-proj --ai qoder   # 📌 stamp 整体覆写为新 commit
grep <旧commit> demo-proj/.specify/source.json   # 📌 期望 0 命中(零残留)
```

## 4. wheel 形态:构建期嵌入

```bash
hatch build    # 📌 构建钩子写 src/specify_cli/_source_commit.json 并随 wheel 分发
unzip -p dist/specify_cli-*.whl specify_cli/_source_commit.json   # 📌 嵌入值 == 构建时 HEAD
```

wheel 安装(uv/pip)后对任意项目 init → `source.json` 的 commit 来自嵌入值(`origin=embedded`);无 git 环境构建的包 → `commit: "unavailable"` + `reason`(诚实降级,init 照常成功)。

## 5. 语义速查(三态)

| source.json 状态 | 含义 | 动作 |
|---|---|---|
| `commit` 为 40-hex | 有效来源 | 框架仓 `git show` 回溯 |
| `commit` 为 `"unavailable"`(+`reason`) | 显式不可得 | 查 reason;不猜 |
| 文件缺失 | 来源未知(存量项目/被删) | 下次 init 重生 |
