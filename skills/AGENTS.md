# Skills

本目录是 Island 上所有可安装 skill 的真源。改任何一个 skill 之前先读本文，再读该技能目录里的 `AGENTS.md` 与 `SKILL.md`。

共同约束只写在这里。各技能目录的 `AGENTS.md` 只补充局部约定，并指向本文，不重复展开共同层。

## Layout

- 一个 skill 一个目录：`skills/<skill-id>/`
- 目录名必须与该目录 `SKILL.md` frontmatter 的 `name` 一致
- 可安装入口是含 `SKILL.md` 的目录本身，不是仓库根，也不是上一级 `skills/`
- 每个技能目录放一份 `AGENTS.md`（局部约定 + 指回本文）

## 安装

用户级挂载：

```bash
ln -s <本技能目录的绝对路径> ~/.agents/skills/<skill-id>
```

- 链接名必须等于 `name`
- 宿主扫描 `~/.agents/skills/`（Claude Code、Kimi Code、Codex、DeepSeek Harness 等也会读各自专用目录，但以这份约定为准）
- 项目级如需覆盖，放到该仓库的技能扫描目录，规则相同

## 共同约束

- 正式文案用语见 `docs/vocabulary.md`。对话可用俚语；本文与各 `SKILL.md` 用 `skill`、`agent` / `subagent`、`create`、`role spec` 等工程用语。
- 创建或修订可派遣 agent role，走 `skills/recruit`（及其 `SCHEMA.md`）。不要在业务 skill 里另起一套 role 合同方言。存量 skill 内已有的 SCHEMA / agents 可暂留，迁入与收敛另议。
- 项目侧选用角色，不改 role spec 正文。
- 共享能力以本目录对应 skill 为真源，其它 skill 引用、不要再复制一份（例如知识库合同以 `yes-swiki` 为准，交接协议以 `yes-handoff` 为准）。
- 不要把未就绪能力写成已可用承诺。
- 不要把 skill 放到本目录以外。
- 不要把个人昵称写进目录名或 skill id。

## 清单

| skill | 职责 |
|---|---|
| `island` | `/island` 入口与路由 |
| `recruit` | 设计并落盘 agent role spec |
| `yes-subagents` | 分派 subagent，维护主会话上下文 |
| `yes-swiki` | 项目内知识真源 |
| `yes-handoff` | 将会话浓缩为可恢复的交接 |
| `yes-designer` | 在已有前端上继承骨架并落地设计 |
| `go-spec` | 把讨论沉淀为可升层、可切片的计划 |
| `go-trail` | 沉思对话（不求解、不代做决定） |
