# E-thick

使用提供的 yes-subagents 技能处理本任务。

代码仓库位于 `{{REPO}}`。上游已经完成产品对齐和计划审查，批准计划、执行总览、当前计划的节点切片及审查凭证位于 `{{HANDOFF_DIR}}`。

请消费现有计划，按其既定推进顺序完成全部节点的实施、验证与门禁检查。不要重新生产或重新审查计划；不要把上游节点对话当作施工输入。若实现暴露出必须改变既定目标、范围、验收、设计或节点边界的结构性问题，按技能合同停止并记录。

Coder Plus 在每个 Milestone 内按逻辑完整性创建本地原子提交；叶子代理不得提交。commit 只是施工检查点，不代表 gate 通过；将 Milestone 交付 gate 前提交全部 Milestone-owned 改动，交付后冻结受审历史，FAIL 修复使用追加提交。不要 push。将节点交付分别保存为 `{{OUTPUT_DIR}}/milestone-1-result.md`、`{{OUTPUT_DIR}}/milestone-2-result.md`，并将最终结果与验证证据保存为 `{{OUTPUT_DIR}}/result.md`、`{{OUTPUT_DIR}}/verification.md`。全部完成后再汇报。
