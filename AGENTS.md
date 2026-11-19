# To Agent

Island 是一座个人工作岛屿：**空白岛 + 基建**。提供规范与基础能力；地标按需建造，不是一上来就齐全。

当前目标：**先自用跑通**。是否对外分享暂不作为结构约束；命名与目录按工程惯例，不把个人昵称写进路径或技能 id。

气质：给底座，不替人盖楼。

## Layout

- 所有技能统一放在 `skills/<skill-id>/`（含 `SKILL.md`）
- **技能共同约束**：`skills/AGENTS.md`（改任何 skill 先读）
- 用户入口：`skills/island/`（`/island` → 路由表）
- agent role spec：由 `skills/recruit/` 产出并存放在其约定目录
- `docs/`：门廊之外的说明与笔记；不放可安装技能

## First Time

1. 读完本文（门廊）
2. 读 `skills/AGENTS.md`（技能共同约束与清单）
3. **用户入口**：`/island` → 读 `skills/island/SKILL.md`
4. 创建 / 修订 agent role → 读 `skills/recruit/SKILL.md`（及同目录 SCHEMA）
5. 动某个 skill → 先读该目录 `AGENTS.md`，再读 `SKILL.md`
6. 项目侧选用角色 → 近处说明优先；**不改** role spec 正文

不要跳过门廊与 `skills/AGENTS.md` 直接改技能。人类日常只需记 `/island`。

## Climate（气候）

可点名的薄规范。岛民「怎么写」以 `skills/recruit/` 为准；其余气候（Human 边界、完成标准等）可后置 `docs/climate/`，未建前以门廊与招募文档为准。

## Recruit（招募）

**招募 = 设计并落盘岛民说明书的能力。** 说明书合格，岛民即存在。

真源：`skills/recruit/`

- 不管：项目组队、酒馆选人、编排飞轮
- 岛民说明书不随单次项目改版；项目差异进任务说明
- 酒馆 / 组队：按名引用岛民，为项目派工

## Skills

可安装 skill 的清单与共同约束见 `skills/AGENTS.md`。意图 → skill 的对照以 `skills/island` 路由表为准。

已收拢：`island`、`recruit`、`yes-subagents`、`yes-swiki`、`yes-handoff`、`yes-designer`、`go-spec`、`go-trail`。

尚未收拢的能力（路由表中仍标未就绪）：项目组队 / 选人、向导。

## Do not

- 不要把未就绪能力写成已可用承诺
- 不要在业务 skill 外另起一套岛民设计方言（应走 `skills/recruit`）
- 不要用重型编排当默认路径
- 不要把一次性日志写进图书馆类真源
- 不要为「将来分享」过早抽象
- 不要把个人昵称写进目录、技能 id 或合同文件名
- 不要把技能放到 `skills/` 以外的路径

## Who's It

- **岛主**：本仓维护者；与 Agent 对等讨论产品与架构
- **本仓**：Island 图纸与基建
- **外部参考**（可引用、非本仓真源）：各 skill 迁入前的独立仓库；早期重型编排仅作语感参考，不收入本仓

## 撰写与演进

- 人类向说明见 `README.md`；Agent 以本文为准。冲突时先修门廊或 README。
- 对话俚语 ↔ 正式用语对照见 `docs/vocabulary.md`（改写规范另议）。
- 新技能只加在 `skills/`，并同时更新 `skills/AGENTS.md` 清单与（如需要）`skills/island` 路由表；避免把门廊写成百科。

## Simple Wiki

只沉淀可复用知识, 一次性日志、临时命令输出、未经验证的猜测和普通 TODO 不应进入 wiki。

- 从 `docs/simple-wiki/wiki/INDEX.md` 了解项目已积累的知识和事实
- `docs/simple-wiki/raw` 记录稳定原始材料：项目目标、决策、验证契约和研报等等。
- `docs/simple-wiki/wiki` 是给未来 agent 查阅的知识文档, 当某个改动产生会影响未来 agent 判断的知识时，同步更新这些页面。
- 一次性查阅资料超过 10 份时, 加载 `/yes-swiki`, 按情况安排子代理 swarm-reader
- `docs/simple-wiki/LINT.md` 记录查阅中确认的存疑文档及反馈：主体条目待 curator 核实，「ESCALATE」区块内待人工裁决. 查阅中发现存疑，先向 human 反馈，确认后才写入 LINT.md.

