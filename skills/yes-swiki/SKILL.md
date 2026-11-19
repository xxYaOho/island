---
name: yes-swiki
description: >
  在项目中收录可复用的研究、决策或验证材料，查阅 Simple Wiki，或维护馆藏健康时使用。
  覆盖 INGEST、READ、MAINTAIN；不用于普通文档写作、一次性摘要或与项目知识库无关的检索。
argument-hint: 收录、查阅或维护项目知识库
metadata:
  version: v0.6.0
---

# Yes! Simple Wiki

管理项目中可长期复用的知识，使事实能够从 wiki 回溯至不可变的 raw 正文。

```text
docs/simple-wiki/
  raw/       原始材料；正文不可修改，frontmatter 可维护
  wiki/      编译知识页与 INDEX.md
  LOG.md     馆藏操作时间线
  SCHEMA.md  已部署的项目规范
  LINT.md    馆藏健康记录
```

## 路由与诊断

先判断用户的当前目标，再运行 `<SKILL_SCRIPTS_DIR>/doctor.sh`：

- `INGEST`：将可复用研究、决策、已验证记录或其凭证以 raw-first 方式收录、编译并接线。
- `READ`：从现有馆藏查找、比较、综合并回答问题。
- `MAINTAIN`：处理 LINT、矛盾、过时、孤立页、链接或 INDEX 健康问题。

doctor 只报告机器可解析事实，不派遣、不迁移也不修复。使用其绝对路径 `WIKI_ROOT` 与 `SKILL_SCRIPTS_DIR`，以及当前目标所需的摘要或 `--detail ingest|maintain|all`；其他告警不得劫持已选目标。外部只读项目只允许 READ，或只读诊断，不得初始化、迁移或写入。

`NEED_INIT=true` 且项目可写时，运行 `init.sh` 后复跑 doctor。`SCHEMA_STATUS=legacy|outdated` 时，先运行 `migrate.sh <WIKI_ROOT>`，再复跑 doctor；`skill-outdated|invalid` 禁止写入并报告。结构仍可解析时，READ 可以继续。细节见 [SCHEMA](reference/SCHEMA.md)。

doctor 的关键收尾事实包括：`RAW_PENDING`、`RAW_PENDING_EVIDENCE`、`RAW_UNINTEGRATED`、`RAW_INGEST_ORPHAN`、`PAGE_CONTESTED_UNLINTED` 与 `RAW_INVALID_STATE`。`false/false` 为待处理，`true/false` 为待共享接线，`true/true` 为完成；`false/true` 是非法状态。

## INGEST

只收录独立于本次对话仍有价值的研究发现、决策背景、已验证的记录与必要溯源材料。不收录纯施工清单、一次性状态日志、临时输出或未经验证的猜测。源文档原有 frontmatter 保存在 `metadata`；raw 正文永不修改。

```yaml
---
class: material | evidence
ingested: false
integrated: false
metadata: ~
---
```

`material` 被编译为知识页；`evidence` 仅作为相关页面的 `sources` 凭证，不单独成页。独立 evidence 只有在当前任务、同批 material 或用户给出关联页候选时才交给 librarian；没有引用归宿时保持未处理并上报，不因 doctor 告警自动派遣。

### Ownership

- **librarian**：只写已协调的 wiki 页面、对应 raw 的 `ingested`，以及自己发现的 LINT `ESCALATE` 矛盾条目；返回处理 raw、触及页面、INDEX/LOG 建议、LINT 条目、未验证项与升级项。
- **orchestrator**：不复核 raw 或知识内容；汇总 librarian 结果，读取已编译页以生成描述，统一 upsert `INDEX.md`、追加并尽力去重 `LOG.md`，再以明确 raw 清单或 manifest 调用 `mark-integrated.sh`。
- **curator**：不参与收录编译；其在 MAINTAIN 中仍可直接维护 INDEX 与 LOG。

单 librarian 时，直接以 manifest 和协调后的 `PAGE_PLAN` 派遣 INGEST，不进入多方 PLAN 分流。多个 librarian 时：先根据材料和现有 INDEX 为每份材料选择一个关联度最高的粗主题（仅用于聚类调度，不写入 raw，也不决定最终 Topic），并行派遣 `PLAN`；根据返回的实际页面计划分流。计划互斥的单元可并行 INGEST，重叠计划合并给一个 librarian 串行处理。协调后的 `PAGE_PLAN` 是写入白名单；出现计划外需要时，librarian 返回 `PLAN_DEVIATION` 且不写越界页面，保留相关 raw 的 `ingested: false`，由 orchestrator 重新协调。

多 librarian 的 LINT 条目在页面写入后串行追加，以避免并发改动 `LINT.md`。librarian 不写 INDEX 或 LOG；所有 librarian 完成后才由 orchestrator 做共享接线，再标记 `integrated: true`。若 librarian 已翻转 `ingested` 但回复丢失，依据 doctor 和 wiki `sources` 重建 INDEX/LOG，不需重新判断 raw；没有来源映射的已处理 raw 交回 librarian 修复。每次写入完成后复跑 doctor。

调用细节见 [librarian](agents/librarian.md)；raw 状态和页面语义见 [SCHEMA](reference/SCHEMA.md)。

## READ

从 INDEX 选择候选页，运行 `<SKILL_SCRIPTS_DIR>/context-stats.sh <候选页...>` 或 `--topic <主题>`。`SWARM_ADVISE=true` 时，将显式、互斥的页面清单派给 swarm-reader；否则直接阅读。命令的缺页、无 topic 或用法错误先修正后重试，不能绕开预算无限制读取。

swarm-reader 只读并返回带来源的提炼和 `DOUBTS`；orchestrator 汇总跨 reader 的矛盾，确认后再决定是否进入 LINT。READ 不因其他馆藏告警转为维护任务。调用细节见 [swarm-reader](agents/swarm-reader.md)。

## Code Wiki 能力

项目可选维护 `docs/simple-wiki/code/`，让 agent 先获得代码模块认知，再按需读取源码。

```text
docs/simple-wiki/code/
  INDEX.md   语义模块级代码索引
  SCHEMA.md  代码索引格式与范围规则
```

代码源文件是该模块的 raw authority。代码条目直接引用仓库相对路径，使用 `F/R/A/S` 记录职责、关键关系、入口或契约，以及高风险约束。默认索引语义模块；入口、公共契约和高风险边界可以独立成条目；普通叶子文件由所属模块覆盖。

`code-administrator` 按调用方提供的显式 scope 规划或更新代码 Wiki，写入范围由调用方提供。它返回代码单元计划、路径覆盖、条目变更、未验证项和验证结果。角色合同见 [code-administrator](agents/code-administrator.md)。

代码 Wiki 使用自己的 `code/SCHEMA.md` 和 Git revision freshness。raw 材料的 `ingested/integrated` 状态以及 wiki 页的 `context` 预算适用于 `raw/` 与 `wiki/`，代码模块按自身规范记录来源和新鲜度。外层工作流负责决定何时调用该能力，以及是否与其他角色组合。

## MAINTAIN

根据 doctor 的维护明细与 LINT 判断范围，派 curator `scope: targeted|full`。轻微、边界明确的问题用 `targeted`；严重、密集或持续的健康问题先向用户说明并确认，再直接派 `full`。不引入 Quality Auditor。

curator 在 MAINTAIN 中负责 LINT、矛盾、过时、孤立页、链接、INDEX 漂移与 context 健康，并可直接写 INDEX、LOG。bundled SCHEMA 的受管核心是基础规范唯一真源；项目补充只能由 orchestrator 作为独立配置提案写入本地补充区，不提升基础版本，实质改变解释或范围时先向用户确认。调用细节见 [curator](agents/curator.md)。

## Compound Interest

仅当维护中发现可复用的新知识时形成局部闭环：将综合笔记写入 raw，交 librarian 编译为 `synthesis`，按普通 INGEST 完成接线与验证。普通 synthesis 无需逐次确认；争议内容、SCHEMA 变化、外部只读目标或明显扩大范围时先确认。
