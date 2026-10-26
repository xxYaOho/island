# Vocabulary

对话可用俚语；落入本仓正式文案时用工程用语。如何改写现有 `AGENTS.md` / skills、是否单独做向导类 skill，**另议**——本文只做词语对照。

## 对照

| 对话可用（俚语） | 正式用语 | 说明 |
|---|---|---|
| 岛 / 上岛 | Island / 使用本仓 skills | 产品名 Island 可保留；动作说「使用 / 加载」 |
| 门廊 | `AGENTS.md` | Agent 入口说明 |
| 门户 | entry / router（现 `skills/island`） | 用户口令仍可是 `/island` |
| 向导 / 管家 | （待规范） | 定向、解说、交棒；形态未定（skill / agent / 并入 router 等） |
| 地标 | skill | 能力模块，路径 `skills/<id>/` |
| 岛民 | agent / subagent | 可派遣角色 |
| 说明书 | role spec（如 `agents/<role-id>.md`） | |
| 招募 | create（agent / role） | 现目录 `skills/recruit`，命名是否改为 create-* 另议 |
| 小酒馆 / 组队 | team selection（待建 skill） | 项目侧选人；不改 role spec |
| 图书馆 | wiki / knowledge skill（待建） | |
| 规划台 | plan / spec skill（待建） | |
| 篝火边 | contemplative skill（待建） | |
| 设计工作室 | design skill（待建） | |
| 交接处 | handoff skill（待建） | |
| 气候 | norms（如 `docs/climate/`） | |
| 岛主 | owner / maintainer | |
| 码头 | dock（如 `/.island`，未钉死） | 宿主发现用 |

## 正式文案优先词

`skill` · `agent` / `subagent` · `create` · `plugin` · `cordis`（宿主插件语境）· `role spec` · `router`

避免把「岛民 / 招募 / 地标 / 上岛 / 酒馆」等写成结构术语。路由里的口语触发词（匹配用户说法）可以保留，那是信号，不是定义。
