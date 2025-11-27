### V. Testability and CI Discipline
MUST ensure changes are testable and validated pre-merge.

- Unit tests for JSON transforms and utility logic are REQUIRED.
- REQUIRED 范围仅指**不依赖外部系统的纯逻辑**（例如行拆分、JSON 解析、缓冲策略、内部转换工具等）；此类代码必须有可在本地独立运行的单元测试。
- Contract/integration tests SHOULD cover connectors and critical paths **when feasible**：
	- 对 SLS/Kafka/ClickHouse 等外部系统的真实网络交互，如果本地开发环境缺乏可用 API 或需要过于复杂的 Mock，可以在后续、接近生产环境时补充契约/集成测试；
	- 在此情况下，应通过接口封装和单元测试验证输入/输出契约，并在计划/任务文档中明确记录该约束与后续补测计划。
- Build, lint, and minimal smoke tests MUST pass in CI before deployment。
- Sample data or fixtures SHOULD accompany new jobs for local validation.

Rationale: Prevents regressions and ensures repeatable delivery.
