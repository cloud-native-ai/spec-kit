# Quickstart: 站点记忆三态走查(需求 046 / Feature 048)

**Requirement → Feature**: `046-browser-site-memory` → Feature 048 Browser Utils Skill

CLI 示例遵循 contracts/site-memory-engine.md;引擎落地后由 tests/contract/test_browser_site_memory.py 逐一钉住(`--action` 集合、退出码、JSON 信封)。`$SKILL_HOME` = 调用方项目内 `.specify/skills/browser-utils`。

## 走查 1:探索期 —— 陌生站点首次任务(US1)

1. 路由:无内置浏览器工具 → Tier 2;`get-state` 返回 `state: null` → 进入探索期。
2. 初始化:

   ```bash
   python3 $SKILL_HOME/scripts/site-memory.py --action init --url "https://g.aliyun-inc.com/project/..." --skill-home "$SKILL_HOME"
   # → {"ok": true, "site": "g.aliyun-inc.com", "state": "exploration", "created": true}
   ```

3. 完成任务(页面级方向:Playwright 驱动,逐步查看/填表/点击),过程中把每条 DOM 操作与网络请求写入记忆:

   ```bash
   python3 $SKILL_HOME/scripts/site-memory.py --action append-record --site g.aliyun-inc.com --task query-baseline \
     --record '{"seq":1,"at":"2026-08-24T02:00:01Z","kind":"network","ok":true,"method":"POST","url":"https://g.aliyun-inc.com/console_api/api.json?ApiName=ListBaseline","headers":{"cookie":"<cookie:aliyun>"},"body_template":{"pageNum":1},"response_shape":{"status":200,"json_keys":["data","total"]}}' \
     --skill-home "$SKILL_HOME"
   ```

4. 验证点:任务目标已达成;`site/g.aliyun-inc.com/records/query-baseline.jsonl` 完整覆盖关键步骤(含失败重试行);`grep -c '"cookie": "[^<]' records/*.jsonl` 为 0(无原值泄漏)。
5. 留痕完整 → `validate-records` 返回 `complete: true` → `transition --to optimization`。

## 走查 2:优化期 —— 蒸馏请求级步骤集(US3)

1. 再次接到同站点同类任务;`get-state` = optimization。
2. 分析 `records/query-baseline.jsonl`,蒸馏出 `recipe.json`:请求级步骤(方法/URL/参数模板/动态字段解析来源/预期响应特征),无法请求化的步骤显式 `type: "page"` + `reason`。
3. 落盘并进入验证期:

   ```bash
   python3 $SKILL_HOME/scripts/site-memory.py --action write-recipe --site g.aliyun-inc.com --file /tmp/recipe.json --skill-home "$SKILL_HOME"
   python3 $SKILL_HOME/scripts/site-memory.py --action transition --site g.aliyun-inc.com --to validation --evidence "recipe.json steps=5 page_steps=1" --skill-home "$SKILL_HOME"
   ```

4. 本次任务以混合方式完成(请求级为主、页面级为辅),页面探测步骤数较探索期明显减少(SC-002 计数来源:两次运行记录的行数对比)。

## 走查 3:验证期 → sealed / 回退(US4)

1. 验证期:端到端执行 recipe 步骤(页面上下文 fetch,继承会话),逐步对照 `expect`:

   ```bash
   # 验证证据由执行路径汇总后落盘:
   python3 $SKILL_HOME/scripts/site-memory.py --action record-validation --site g.aliyun-inc.com --file /tmp/evidence.json --skill-home "$SKILL_HOME"
   # verdict=pass → {"state": "sealed"};verdict=fail → 自动回退 {"state": "optimization"}
   ```

2. sealed 后再次执行同类任务:`get-state` = sealed → 直接执行 recipe,**零页面探测**(FR-010);单步失败即 `transition --to optimization --evidence <漂移证据>` 并提示重新蒸馏。
3. 回退后既有 records/recipe/validation 全部保留(SC-004),基于失败证据修订 recipe 后重新走查 3。

## 异常走查

- **记忆目录被删**:`get-state` 返回 `state: null, memory: "absent"` → 重新走查 1。
- **脱敏拒绝**:`append-record` 对含原值 cookie 的记录退出 1 并指出字段路径 → 改写为 `<cookie:名>` 后重试。
- **跳态拒绝**:`transition --to sealed`(当前 exploration)→ 退出 1,输出合法目标集合。
