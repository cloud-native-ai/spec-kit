# Red-First Evidence — 056-probe-handler-system

> 运行期证据落点（tasks.md T001 创建）。记录每个红优先测试在实现前的失败证据：测试名、失败断言、失败原因归因（制品缺失 vs 断言写错）。

## 格式

每条记录：

```
### <test file>::<test id>
- 时间: <UTC timestamp>
- 命令: <exact command>
- 输出（决定性摘录）: <paste>
- 归因: <subject 缺失 | assertion 缺陷 | 外部在途>
- 恢复: <实现落地后转绿的证据或引用>
```
