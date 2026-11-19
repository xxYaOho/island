# AGENTS

## Simple Wiki

只沉淀可复用知识, 一次性日志、临时命令输出、未经验证的猜测和普通 TODO 不应进入 wiki。

- 若项目已维护 `docs/simple-wiki/code/INDEX.md`，先读它建立代码模块、关键关系与约束的初步认知；涉及具体修改时再回到源码、测试和契约核对。
- 从 `docs/simple-wiki/wiki/INDEX.md` 了解项目已积累的知识和事实
- `docs/simple-wiki/raw` 记录稳定原始材料：项目目标、决策、验证契约和研报等等。
- `docs/simple-wiki/wiki` 是给未来 agent 查阅的知识文档, 当某个改动产生会影响未来 agent 判断的知识时，同步更新这些页面。
- 项目发现 yes-swiki 有新版本时，先读取新版本的 `SKILL.md` 与 `reference/SCHEMA.md`，使用 `scripts/migrate.sh` 同步项目 Schema，再检查项目根 `AGENTS.md`，补充新增的入口与约束。
- 一次性查阅资料超过 10 份时, 加载 `/yes-swiki`, 按情况安排子代理 swarm-reader
- `docs/simple-wiki/LINT.md` 记录查阅中确认的存疑文档及反馈：主体条目待 curator 核实，「ESCALATE」区块内待人工裁决. 查阅中发现存疑，先向 human 反馈，确认后才写入 LINT.md.
