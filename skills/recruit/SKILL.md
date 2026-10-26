---
name: recruit
description: >
  Design and land islander role specs for Island. Use when creating or revising
  a subagent/islander markdown, when asked to 招募 / 设计岛民 / 写角色说明书,
  or when another Island skill needs a new reusable agent role. Does not staff
  a project team, open tavern picks, or run orchestration flywheels.
---

# Recruit

招募 = **设计并落盘岛民说明书**。说明书合格，岛民即存在。

## 边界

| 做 | 不做 |
|---|---|
| 从意图起草 / 修订岛民 `.md` | 按项目临时改岛民正文 |
| 按设计规范自检 | 酒馆选人、组队、派工编排 |
| 把合格文件放到本技能约定目录 | 发明第二套合同方言 |

项目要人 → 去酒馆 / 组队能力（另议）；此处只产出**稳定**岛民。

## 岛民存放

- 目录：`skills/recruit/agents/`
- 文件：`<role-id>.md`（kebab-case，与 frontmatter `name` 一致）
- 合格标准：通过同目录 `SCHEMA.md` 自检

## 工作方式

1. 收齐意图：唯一责任、派遣信号、边界、预期回报  
2. 选形态：叶子执行者 / 行动负责人 / 调查·诊断·审计 / Reviewer  
3. 按 `SCHEMA.md` 填说明书（六问）  
4. 自检；缺输入则停下问清，不猜  
5. 写入 `agents/<role-id>.md`  
6. 向岛主交代：文件路径、责任一句话、何时该请来

## 生成短路径（意图 → 初稿）

```
意图
  → 形态
  → 六问（是谁 / 何时请来 / 动手前要什么 / 怎么干 / 交什么 / 怎样结束）
  → 自检
  → 落盘
```

## 参考

设计合同真源：`SCHEMA.md`（本目录）。思想可借鉴既有 subagent 设计实践，但本岛文件树与命名以本技能为准。
