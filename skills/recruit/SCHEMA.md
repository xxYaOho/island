# Islander Design Schema

定义 `skills/recruit/agents/*.md` 的设计合同。名单与路由由引用方维护；本文件不复制编排 / 飞轮 / 项目组队流程。

## 1. 设计目标

- **职责唯一**：一个岛民对一个可判断的责任结果负责，并写明不属于自己的相邻职责。
- **权限最小**：工具只覆盖完成责任所需能力。
- **上下文最小**：动手前只索取当前工作单元所需输入。
- **责任闭合**：行动者验证自己的产出；负责人整合叶子并统一验证；Reviewer 只裁决，不代替直接验证。
- **返回可解析**：稳定分节；不确定项单列；以 STATUS 收束。

## 2. 形态

| 形态 | 责任 | 可否派叶子 | 终止状态 |
| --- | --- | --- | --- |
| 叶子执行者 | 完成一个边界明确的工作单元 | 否 | `DONE \| BLOCKED` |
| 行动负责人 | 理解完整交付单元，整合并统一验证 | 是（仅白名单叶子） | `DONE \| BLOCKED` |
| 调查 / 诊断 / 审计 | 收集证据并给出结论，不改目标状态 | 否 | `DONE \| BLOCKED` |
| Reviewer | 对权威基线独立裁决，不改产物 | 否 | `PASS \| FAIL \| BLOCKED` |

保持至多两层：`编排者 → 负责人 → 叶子`。禁止负责人再派负责人或 Reviewer。

蜂群是调度形态，不是岛民形态。

## 3. 六问（正文必须答完）

1. **是谁** — 唯一责任；明确「不是谁」  
2. **何时请来** — 派遣信号；何时不该请来  
3. **动手前要什么** — 最小输入；缺则 `BLOCKED`，并写清缺什么、谁补  
4. **怎么干** — 边界、可动范围、停止条件；权限最小化  
5. **交什么回来** — 稳定字段；不确定与结论分开；末项可保留 `ESCALATE`  
6. **怎样算结束** — 只用约定状态词（见上表）

## 4. Frontmatter

```yaml
---
name: role-id
description: >
  Responsibility, trigger, boundary, and returned result.
tools: Read, Grep, Glob
model: inherit
effort: high
---
```

- `name`：kebab-case，与文件名一致；按责任命名，不按一次性动作命名。  
- `description`：责任 → 派遣信号 → 边界 → 返回物；必要时写反向边界。  
- 不要用更高 `effort` 补偿模糊职责或缺失输入。

### 工具（最小集）

| 需要 | 工具 |
| --- | --- |
| 静态读 | `Read, Grep, Glob` |
| 外部资料 | 加上 `WebSearch` |
| 受控诊断 | 加上 `Bash`（不改持久状态） |
| 改项目 | `Read, Grep, Glob, Bash, Edit, Write` |
| 派叶子 | 仅负责人再加分派能力 |

Reviewer 不得拥有写入或分派能力。

## 5. 建议正文顺序

Role →（可选）内部短流程 → PRECONDITION → Operating Rules → Output → STATUS。

PRECONDITION 必须包含机械句：缺少必需输入时不要猜；`STATUS: BLOCKED`，并说明 WHAT / WHO。

表达约束：`Be terse. No praise. No filler.`  
STATUS 固定为文件可见合同的最后一行状态约定。

## 6. 岛上多钉的两钉

1. **稳定 vs 用工**：岛民说明书不随单次项目改；项目差异进任务说明，不进 `agents/*.md` 正文。  
2. **生成短路径**：意图 → 形态 → 六问 → 自检 → 落盘（见 `SKILL.md`）。

## 7. 自检

- 仅凭 `description` 能否决定派 / 不派？  
- Role 是否只有一个责任结果，并排除了相邻角色？  
- 工具是否最小？负责人是否限制了叶子白名单？  
- PRECONDITION 是否最小且含 WHAT / WHO？  
- 不确定项是否与结论分离？  
- STATUS 是否使用固定词汇？  
- 是否把项目临时约束写进了说明书正文？（若是，挪出）
