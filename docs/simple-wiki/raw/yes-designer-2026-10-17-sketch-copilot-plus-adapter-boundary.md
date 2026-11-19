---
class: evidence
ingested: true
integrated: true
metadata:
  source_repo: "https://github.com/xxYaOho/skill-designer"
  source_commit: 71ffb95
  source_path: docs/notes/2026-10-17-sketch-copilot-plus-adapter-boundary.md
---
# sketch-copilot-plus 适配边界

- 日期：2026-10-17
- 状态：背景参考，未批准实现合同
- 来源：[Skills/yes-subagents#1](http://127.0.0.1:3100/Skills/yes-subagents/issues/1)
- 关联：`sketch-copilot-plus`、`yes-subagents`、新设计协作 skill

> 本文已被 `2026-10-18-yes-designer-design-work-loop-v6.md` 取代；术语与契约以该文 §3 为准；本文为历史背景，不再更新。

## 目的

新设计协作 skill 负责通用的设计理解、实现基线、差量实现和结构验收。`sketch-copilot-plus` 在存在 Sketch 时作为证据适配器，为它提供可回溯的 Sketch 事实。Sketch skill 不决定代码路径，也不复制一套通用设计编排器。

新 skill 不应要求一定存在 Sketch。它还可以消费 Figma、截图、既有页面、上一任务结果、运行页面和 Human 的明确描述。Sketch 是一种证据来源。

## 职责分层

### 新设计协作 skill

- 识别 source of truth 和参考来源。
- 判断任务是 `copy`、`extend`、`variant` 还是 `independent`。
- 建立跨任务 `IMPLEMENTATION_BASELINE` / `REUSE_BASELINE`。
- 执行 bounded repository reuse scan。
- 拆分 `preserve` 和 `delta`，并维护允许变更范围及失效条件。
- 生成代码侧 `STRUCTURE_DECISIONS`。
- 组织 `DISCOVER → CLASSIFY → BASELINE → BUILD → PREVIEW → REVIEW → FIX → REVERIFY` loop。
- 分开验收 `DESIGN_FIDELITY`、`STRUCTURAL_CONFORMANCE` 和工程结果。
- 将事实完整但价值取舍未决的事项交给 Human。

### `yes-subagents`

维护通用 dispatch、角色合同、上下文边界、handoff、调度、reviewer 生命周期和通用 gate。它消费冻结后的中性实现基线，不承担 Sketch 语义。

### `workflow/coding`

消费已冻结的实现边界，负责代码实现、测试、类型检查、构建和工程验证。Coder 不得在缺少结构决策时静默改判为 `new`。

### `sketch-copilot-plus`

提供以下 Sketch 证据：

- 已确认的 document、Page、Frame、state 和 layer 锚点；
- 父子层级、Stack、Relative/Fill、wrap、padding、border 和坐标事实；
- Tint、fill、gradient、shadow、visibility、asset 和 SymbolInstance 事实；
- 设计语言、角色关系和视觉结构证据；
- 设计侧的保留项、差量和未知项；
- `DESIGN_FIDELITY` 所需的截图和回溯路径。

它不负责：

- 决定代码文件或组件路径；
- 执行代码仓库复用扫描；
- 生成代码侧 `reuse / extend / new / blocked` 决策；
- 维护跨任务实现基线；
- 代替新设计协作 skill 调度 Coder。

## Sketch 侧证据形状

保留 standalone packet 的 `REUSE_MAP` 名称，但其语义只表示设计证据，不表示代码复用已经确定。新生成的 packet 可以包含以下可选设计关系区块：

```text
design_relation: variant | independent | unknown
source_design_anchor:
  documentId / pageId / layerID / frame
preserve:
  - 页面角色、层级关系、交互状态、设计语言
delta:
  replace: []
  add: []
  remove: []
  unknown: []
evidence_refs: []
```

`source_design_anchor` 是 Sketch 锚点或用户确认的设计来源，不是代码文件路径。Sketch 侧不得写入 `candidate_paths`、`scan_scope`、`exclusions` 或代码侧 `STRUCTURE_DECISIONS`。

关系判断规则：

- 有明确来源锚点或用户确认复制关系时，使用 `variant`。
- 有明确设计证据表明没有继承关系时，才使用 `independent`。
- 只有视觉差异、没有来源信息或证据不足时，使用 `unknown`，不能猜成独立页面。
- 未知项必须进入 `delta.unknown` 或对应的 unresolved 记录。

设计关系不会直接决定代码决策。`variant` 只表示代码侧应优先检查继承；`independent` 也不代表代码侧无需扫描。

## 交接规则

```text
Sketch MCP
  → sketch-copilot-plus
  → REUSE_MAP / Sketch design evidence
  → 新设计协作 skill 的 IMPLEMENTATION_BASELINE
  → STRUCTURE_DECISIONS
  → yes-subagents / coding
```

新设计协作 skill 可以在 `STRUCTURE_DECISIONS.evidence_refs` 中引用 packet 的 `REUSE_MAP` 条目、Sketch 锚点和证据路径，不复制完整 Sketch 对象或建立第二份视觉真源。

如果只有视觉差量、没有代码来源：

- Sketch 侧输出 `variant` 或 `unknown` 设计证据；
- 新设计协作 skill 继续 bounded repository scan；
- 候选或排除证据不足时为 `BLOCKED`；
- 代码事实完整但价值取舍未决时为 `ESCALATE`；
- `STRUCTURE_DECISIONS` 达到 `COMPLETE` 前不得进入 coding。

视觉截图或 computed style 通过，不能补足结构复用证据。

## 不迁移到新 skill 的 Sketch 专属能力

以下内容继续由 `sketch-copilot-plus` 维护：

- Sketch document/Page 选择和 document ID 固定；
- Stack、percentageSize、Relative、Fill、wrap、min/max 和 parent content box 解释；
- Stack validation probe 和 validator；
- Tint 的容器级 contributor 语义及 RGB/alpha 规则；
- SymbolInstance、overrides、graphic/icon、资源导出和 visibility 事实；
- Sketch 样式 contributor、border、shadow、blur 和截图证据边界；
- Inspection Map 的 Sketch 快照分类和稳定 action ID。

Inspection Map 是证据路由产物。它由新设计协作 skill 消费，但不负责实现 loop、代码扫描或结构决策。

## 当前已知边界

- `sketch-copilot-plus` 当前 `coordinate.md` 和 packet 模板仍混有代码复用描述，需要在 0.2.x 调整中澄清。
- `implement.md` 和 `verify.md` 仍包含 standalone 的代码实现路径；新 skill 接入后应作为 fallback 或 Sketch-to-code 翻译参考，不应成为双重编排器。
- `evidence_domain` 不作为迁移前置条件。
- ASD-STE100-inspired authoring profile 不在本阶段迁移。

本笔记只提供新 skill 的背景上下文。新 skill 的最终名称、schema、触发矩阵、基线生命周期和 eval 仍需独立草案及 Human 审阅。
