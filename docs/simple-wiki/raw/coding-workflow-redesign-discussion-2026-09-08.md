---
class: material
ingested: true
integrated: true
metadata:
  class: material
  ingested: true
  integrated: true
  metadata: ~
  source_repo: "https://github.com/xxYaOho/skill-subagents"
  source_commit: e427ed6
  source_path: docs/simple-wiki/raw/coding-workflow-redesign-discussion-2026-09-08.md
---

# Coding workflow 重构讨论纪要（2026-09-08）

## 背景

yes-subagents 多轮评估始终存在较大编排方差。问题不只是个别条款缺失：现行 `workflow/coding.md` 同时承担计划生产、计划审查、实施分派、gate、提交和收尾，既与 `go-spec`、`SKILL.md` 重复，也不符合真实协作中的进入时点。

本轮决定不再修补现有三阶段结构，将 coding 完全重写为「计划消费与施工编排器」。本纪要保存已确认的设计结论；具体文本尚未实施。

## 总体目标

yes-subagents 的目标是一条因果链，而不是互相竞争的多个指标：合理分派维持主会话上下文健康，使 Orchestrator 保持判断与 gate 能力，并降低完成已验证交付所需的 token 和费用。

效率术语另见《已验证交付单元的 token 与成本指标》：以 TPVD（`kTokens/VD`）为 workflow 主效率指标，CPVD 为成本结果，CPTK 为价格构成诊断。

## 职责边界

- `SKILL.md`：编排原语和全局原则，包括角色、组合、飞轮、待机、监察与完成条件。
- `go-spec`：生产计划，维护决策层、Draft、Implement Plan、Milestone 与派生切片。
- `workflow/coding.md`：消费计划，判断厚薄实施层、选择施工协作形态、推进 gate 和收尾。
- `subagents/*.md`：各角色收到任务后的内部执行契约。

coding 不再重复飞轮定义、最大轮次、通用等待机制、go-spec 的计划生产过程或子代理完整契约。

## 流式、多线程评估

Step 是评估阶段，不等于一个线程。计划作者的 self-review、fresh strict、施工 Orchestrator、执行者和 gate reviewer 分属不同上下文；评估重点是职责分离和线程间工件传递。

评估至少包含薄计划与厚计划两条流水线：

```text
P-thin  -> 通过审查的薄计划  -> E-thin
P-thick -> 通过审查的厚计划  -> E-thick-M1 -> E-thick-M2（可选）
```

- 计划作者线程负责产出与 self-review；self-review 是完整性、一致性和格式检查，不构成独立 critique。
- strict 不论计划厚薄均交给 fresh-agent；其职责与作者线程分离。
- Step 1 向 Step 2 交付批准后的计划、PASS 凭证和未阻断事项，不传完整讨论 transcript。
- Step 2 不重复 Step 1 已完成的 strict，只消费计划并观察 self-executor、子代理分派和 gate。
- 厚实施层只需完成 1 个 Milestone；需要观察跨节点流转时再增加第 2 个，不要求跑完整项目。
- 稳定回归使用冻结的已批准计划；动态 Step 1 -> Step 2 接力只承担集成观察，避免上游方差污染规则归因。

## 计划与执行层级

- 薄计划自然流转到薄实施层；厚计划自然流转到厚实施层。
- Orchestrator 首层派遣时，Task 使用 `coder`，Milestone 使用 `coder-plus`。
- 该映射只约束 Orchestrator 的首层派遣。coder-plus 对整个 Milestone 负责，默认自行完成其中需求；必要时可分派子代理协助，不限于 coder，也可能使用 swarm、researcher 等合适角色。
- Orchestrator 不把 Milestone 扁平拆成多个 Task 后逐项直接派遣；Milestone 内部如何实施由 coder-plus 负责。
- 风险、迁移、新颖性等属性主要影响计划审查深度、gate 验证内容和安全前提，不用于替代 Task/Milestone 的结构映射。

## Gate 生命周期

一个批准计划对应一个 gate reviewer 生命周期。整个计划复用同一个 gate reviewer，不为不同 Milestone 更换 reviewer。

- 子代理实施时，由 Orchestrator 兼任整个计划的 gate reviewer。
- Orchestrator 自己实施时，创建一个独立 `critic-gate`，并在整个计划中持续复用。
- 实施者负责 self-verification，但不能作最终 gate。
- 同一 reviewer 处理后续 Milestone、FAIL 修正与补证，以保持基线连续性并减少重复读取。
- 计划发生结构性变更、reviewer 不可用或上下文已经失真时，才结束该生命周期并重新建立 gate。

strict 与 gate 的会话策略不同：strict 需要 fresh 视角；gate 审查同一计划的实施忠诚度，需要连续判断。

## 收尾

Pruner 保留在 coding 的计划级收尾，不在每个 Milestone 后重复运行。全部实施节点 gate PASS 后，执行一次 `pruner -> scout`；只处理 scout 判定为 SAFE 的目标，随后直接验证并完成收束。

## Coding 预期骨架

1. 角色与入口。
2. 获取计划并确认审查状态。
3. 判断薄计划或厚计划。
4. 薄计划施工：Task -> coder，或在适用条件下由 Orchestrator 自行完成。
5. 厚计划施工：Milestone -> coder-plus。
6. 计划级持久 gate reviewer。
7. 失败、偏差与计划结构变更的分流。
8. Pruner -> Scout 收尾。
9. 完整交付。

## Coder Plus 当前状态与待讨论项

现行 `coder-plus.md` 已具备有限分派能力：拥有 Agent 工具；能自行完成简单实现并把独立工作交给 coder/swarm；限制两层派遣深度；要求向叶子过滤上下文；禁止轮询；最终对整个 Milestone 的验收负责。

当前不足：允许派遣的角色只有 coder/swarm，不能调用 researcher；「简单自己做、需要独立上下文才分派」不足以指导角色选择；没有明确建立 Task 依赖、并行边界和文件所有权；没有说明叶子 BLOCKED、局部失败或调查结果返回后的处理；输出也不要求披露关键分派决策。

后续讨论应确定 coder-plus 是保持「自执行为主、有限助手」还是升级为「有边界的里程碑实施负责人」，以及允许调用哪些调查/诊断角色、如何避免复制根 Orchestrator 的完整编排系统。
