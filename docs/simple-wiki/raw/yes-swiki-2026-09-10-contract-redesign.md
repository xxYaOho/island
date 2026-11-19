---
class: material
ingested: true
integrated: true
metadata:
  source_repo: "https://github.com/xxYaOho/skill_swiki"
  source_commit: 49f68a2
  source_path: docs/island/plans/2026-09-10-yes-swiki-contract-redesign.md
---
# Yes Swiki Contract Redesign

> 2026-09-10 · 状态：已对齐

## Problem Statement

Yes Swiki 当前能够完成知识收录、查阅和馆藏整理，但技能入口主要描述“收录”，激活后的任务路由不够明确；doctor 输出尚不能表达 SCHEMA 兼容性与编译后的共享状态；librarian 同时写页面、INDEX 和 LOG，使多个 librarian 无法可靠并行。现有 `ingested` 还把页面编译与全局接线混为一个状态，旧馆藏升级也缺少保留本地补充规范的迁移合同。

这些问题会让 agent 在真实项目中难以判断先做什么、从哪里获得路径和状态、哪些工作可以并行，以及中断后应从哪个阶段恢复。

## Solution

将技能收紧为 `INGEST / READ / MAINTAIN` 三类任务的轻量路由器，以 doctor 提供绝对路径、馆藏事实与 SCHEMA 状态。拆分知识编译和共享状态接线：librarian 只编译 wiki 页面并维护 `ingested`，orchestrator 在所有收录场景中统一写入 INDEX、LOG，再通过专用脚本维护 `integrated`。

为多 librarian 引入“粗略主题聚类、页面计划、冲突分流、实际编译”的两阶段流程。为存量馆藏引入版本化迁移脚本，同时更新 raw frontmatter 与项目 SCHEMA 的受管核心，保留本地补充规范。知识复利仅保留维护中发现新知识后的局部闭环。

## User Stories

1. 作为知识库使用者，我希望 agent 能根据收录、查阅或维护目标选择正确流程，以便馆藏问题不会劫持当前任务。
2. 作为知识库使用者，我希望新材料先保留原始正文，再被编译为可溯源的知识页，以便长期查阅时仍能回到事实来源。
3. 作为编排者，我希望多个 librarian 可以按相关性聚类并行工作，同时在页面写入重叠时自动转为安全处理，以便提高吞吐而不发生静默覆盖。
4. 作为编排者，我希望页面编译与 INDEX、LOG 接线具有独立、可观察的状态，以便中断后能准确恢复而不重复编译。
5. 作为旧馆藏维护者，我希望技能能检测并迁移过时 SCHEMA，同时保留 raw 正文和项目补充规范，以便升级不破坏既有知识。
6. 作为知识库查阅者，我希望维护过程中产生的可复用综合知识能够回到 raw 并编译为 synthesis，以便知识持续积累而不依赖聊天记录。

## Constraints

- `raw/` 正文不可修改；仅 frontmatter 属于可维护元数据。
- 保留 librarian、swarm-reader、curator 三个领域角色，不引入 Quality Auditor 或新的领域角色。
- orchestrator 是编排与共享文件汇总者，不承担知识内容复核。
- bundled SCHEMA 是基础规范的唯一真源；项目 SCHEMA 是已部署副本，可增加本地补充规范，但补充规范不提升基础版本。
- 外部只读项目不得初始化、迁移或写入。
- doctor 只观察并报告事实，不执行迁移、派遣决策或隐式修复。
- curator 保留 `targeted / full` 馆藏维护责任；本设计对 INDEX、LOG 的统一 ownership 仅约束 INGEST，MAINTAIN 中 curator 仍可直接维护二者。
- librarian 与 swarm-reader 的 agent prompt 保持英文；面向 human 的技能和参考文档保持中文。
- 保留工作区中已有的用户修改，不因本次调整回退或覆盖。
- 本 SPEC 只交付需求与草案设计，不展开实施计划。

## Implementation Decisions

1. 技能 description 覆盖以下触发面：项目中出现可沉淀的研究、笔记、决策或验证材料；用户要求查阅 Simple Wiki；用户要求整理或修复馆藏。普通文档写作、一次性摘要和与项目知识库无关的检索不触发。
2. 技能先判断用户目标属于 `INGEST / READ / MAINTAIN`，再运行 doctor 获取 `WIKI_ROOT`、`SKILL_SCRIPTS_DIR` 和该目标所需的状态。doctor 的其他告警不得自动改变用户目标。
3. doctor 提供摘要输出及 `ingest / maintain / all` 场景化明细；摘要保留 `NEED_INIT`，并分别报告待编译 material、待接线 evidence、待共享状态接线、已 ingested 但无 source 映射、contested 页面缺少 LINT 条目和非法状态。脚本只输出机器可解析事实，派遣策略留在技能正文。
4. SCHEMA 自身采用以下嵌套 frontmatter 原型：

   ```yaml
   ---
   metadata:
     version: v0.6.0
   ---
   ```

   项目 SCHEMA 与 bundled SCHEMA 版本相等时允许正常写入；版本缺失为 `legacy`、版本较旧为 `outdated`，两者都先运行迁移；项目版本较新表示当前技能过旧；格式错误为 `invalid`。后两者禁止写入。READ 在结构仍可解析时允许继续。
5. 项目 SCHEMA 分为技能维护的受管核心与本地补充区域。迁移脚本只替换受管核心并保留补充区域；旧 SCHEMA 的核心与已知版本不一致时失败并报告冲突，不猜测合并。普通补充规范由 orchestrator 提案，必要时经用户确认后写入本地补充区域；这属于独立的 SCHEMA 配置动作，不属于 INGEST 的 INDEX、LOG 汇总。
6. raw frontmatter 采用以下状态原型：

   ```yaml
   ---
   class: material | evidence
   ingested: false
   integrated: false
   metadata: ~
   ---
   ```

7. `ingested` 由 librarian 维护。对 material，`true` 表示知识已编译进 wiki 页面；对 evidence，`true` 表示凭证已被相关页面引用。`RAW_PENDING_EVIDENCE` 不自动触发派遣；只有当前任务、同批 material 或用户输入给出关联页候选时，orchestrator 才将 evidence 交给 librarian 接线。未找到引用归宿的 evidence 保持 `false`，作为信息上报，不在后续激活中反复自动派遣。
8. `integrated` 由 orchestrator 通过专用脚本维护。`true` 只表示本批所需 INDEX 和 LOG 汇总已经完成，不表示页面内容经过复核。
9. 合法状态为：`false/false` 待编译，`true/false` 待共享状态接线，`true/true` 完成；`false/true` 为非法状态。
10. 所有 INGEST，无论一个还是多个 librarian，均由 librarian 写 wiki 页面并翻转 `ingested`，由 orchestrator 统一 upsert INDEX、追加 LOG 并翻转 `integrated`。librarian 不直接写 INDEX 或 LOG。
11. librarian 返回结构化结果，至少包含已处理 raw、触及页面、INDEX 变更建议、LOG 条目、LINT 矛盾条目、页面计划偏差、未验证项和需升级事项。orchestrator 可读取已编译页面的 frontmatter 与形成 INDEX 描述所需的正文，但不与 raw 对照，不复核或重新判断知识内容。
12. 多 librarian 时，orchestrator 根据材料与现有 INDEX 粗略给出一个关联度最高的主题，仅用于聚类 raw 和减少交叉；该主题不写入 raw，也不限制最终页面 Topic。
13. 多 librarian 使用两阶段流程：第一阶段并行阅读并返回页面计划；orchestrator 根据实际待创建或修改的页面识别重叠；无重叠计划可并行写入，重叠计划合并给一个 librarian 串行处理。协调后的页面计划是该 librarian 的写入白名单；执行时发现计划外页面需求，应停止越界写入、返回 `PLAN_DEVIATION`，并保持相关 raw 为 `ingested: false`，由 orchestrator 重新协调。最终 Topic 由编译结果决定。
14. librarian 处理 `ingested: false` 的材料时按 `sources` 和正文引用调和已有内容，不盲目追加，以支持失败后的幂等重跑。
15. orchestrator 对 INDEX 使用 upsert，对本轮完整 LOG 行做尽力去重。LOG 不增加批次标识；中断后偶发重复可以接受。
16. 状态提交脚本只接受明确的 raw 文件清单或 manifest；它预检整批文件，仅将 `ingested: true, integrated: false` 翻为 `integrated: true`，已为 `true` 时幂等成功。脚本不提供全馆自动翻转，不创建缺失字段，不修改 raw 正文。若 librarian 在翻转 `ingested` 后未能交付回复，doctor 根据 wiki 页 `sources` 机械列出该 raw 所关联的页面；orchestrator 据此重建 INDEX、LOG 汇总，不需要复核 raw。已标记 ingested 却没有任何页面引用的 material 或 evidence 单独报告，由 librarian 修复。
17. 迁移脚本按版本顺序更新项目 SCHEMA 的受管核心和 raw frontmatter，最后提升 SCHEMA 版本。旧项目中 `ingested: true` 映射为 `integrated: true`，`ingested: false` 映射为 `integrated: false`。字段创建属于迁移脚本，不属于状态提交脚本。迁移重跑时同时接受“已知旧核心”和“目标核心已经写入但版本尚旧”两种状态；raw 中缺失或已正确写入的 `integrated` 均可继续处理。只有既非已知旧核心、也非目标核心的内容才判定为冲突。
18. 常规迁移无需逐次询问用户；SCHEMA 核心存在定制冲突时停止并报告。迁移完成后复跑 doctor。
19. librarian 保留收录中发现的新矛盾及其 LINT「ESCALATE」条目的 ownership。单 librarian 可在编译中直接写入；多 librarian 的页面写入完成后，由 orchestrator 串行调度相关 librarian 追加各自条目，避免并发修改 LINT。orchestrator 不撰写或复核条目。doctor 机械检测 `status: contested` 但 LINT 中无对应条目的页面；回复在串行追加前丢失时，重新派 librarian 根据该页面补齐条目。
20. curator 继续负责 LINT、矛盾、过时、孤立页、链接、INDEX 漂移及 context 健康；严重问题由 orchestrator 向用户说明并确认后直接派 `curator scope: full`，不经过 Quality Auditor。
21. swarm-reader 只接受显式、互斥的文件清单，不接受无边界目录；保持只读，并将 DOUBTS 与跨 reader 矛盾交回 orchestrator。
22. Compound Interest 仅表达局部闭环：维护中发现可复用新知识，形成综合笔记写入 raw，由 librarian 编译为 synthesis，完成验证与收尾。普通 synthesis 默认无需逐次确认；争议内容、SCHEMA 变化、外部只读目标或明显扩张范围时再确认。

## Testing Decisions

- 测试以可观察行为为准，不绑定 shell 函数或 prompt 内部措辞。
- doctor 覆盖初始化、无版本旧馆藏、当前版本、旧版本、技能过旧、非法版本、待编译 material、待接线 evidence、待共享状态接线、已 ingested 但无 source 映射、contested 页面缺少 LINT 条目、非法状态，以及三种 detail 场景。
- 迁移覆盖无版本旧馆藏、标准旧 SCHEMA、本地补充规范、核心冲突、完整重复执行、在 SCHEMA 核心写入后中断、在部分 raw 写入后中断、非法 raw frontmatter，并验证 raw 正文逐字节不变。
- 状态提交覆盖显式文件参数、manifest、已完成幂等、混合批次预检失败、`ingested: false`、缺失字段、路径越界和中断后重跑。
- librarian 覆盖 material、同批 evidence、独立 evidence 有关联页、evidence 无归宿、已有 source 的幂等调和，以及不直接写 INDEX/LOG。
- 多 librarian 覆盖页面计划互斥时并行、页面计划重叠时串行合并、执行中出现计划偏差、LINT 串行追加、粗略主题与最终 Topic 不一致，以及某一 librarian 失败后的局部恢复。
- curator 回归覆盖 `targeted / full` 责任及 MAINTAIN 中对 INDEX、LOG 的写入权。
- description 使用真实 should-trigger 与相邻 should-not-trigger 查询评估 INGEST、READ、MAINTAIN 三类触发准确率。
- 现有 fixture 与 eval 必须同步新状态和 ownership；旧评估仅作基线，不能直接证明新合同有效。

## Out of Scope

- 不让 orchestrator 复核、重写或独立验证 librarian 的知识内容。
- 不为并行 writer 引入 git worktree、文件锁或事务数据库。
- 不保证多个 Markdown 文件具有真正的跨文件原子提交；通过显式状态和幂等重跑恢复。
- 不自动理解或合并与 SCHEMA 受管核心重叠的任意本地改写。
- 不改变 LLM_WIKI 的原则性内容。
- 不重新评估三个专属 agent 的模型分配。
- 不编写实施计划、Milestone 或 Task。

## Further Notes

- `evidence` 是溯源凭证，不是独立知识页；它与 material 共用 `ingested / integrated` 状态机。
- 多 librarian 的粗略主题只是调度提示，页面计划才是并行写入安全的依据。
- LOG 重复的治理成本低于引入批次身份协议的复杂度，因此接受中断恢复中的低概率重复。
- 项目 SCHEMA 版本高于 bundled SCHEMA 不是合法定制状态，而是当前技能版本落后的诊断信号。

## Draft Plan

### 结构总览

```text
用户目标
  -> SKILL 路由 INGEST / READ / MAINTAIN
  -> doctor 获取路径、SCHEMA 与馆藏状态

INGEST
  -> orchestrator 创建 raw 与初始状态
  -> 单 librarian 直接编译
     或多 librarian 粗分组 -> PAGE_PLAN -> 冲突分流 -> 编译
  -> librarian 写 wiki + ingested=true
  -> librarian 直接或串行追加自己发现的 LINT 条目
  -> orchestrator 汇总 INDEX + LOG
  -> mark-integrated 提交 integrated=true
  -> doctor 收尾

NEED_INIT
  -> init 创建最新骨架
  -> doctor 复验

SCHEMA legacy / outdated
  -> migrate 更新受管 SCHEMA + raw frontmatter
  -> doctor 复验

READ
  -> INDEX 候选 -> context 预算 -> 内联读取或 swarm-reader

MAINTAIN
  -> doctor 明细 -> curator targeted/full
```

### 关键契约

doctor 提供但不消费状态：

```text
NEED_INIT=true|false
WIKI_ROOT=<absolute-path>
SKILL_SCRIPTS_DIR=<absolute-path>
SCHEMA_VERSION=<local>
SCHEMA_LATEST_VERSION=<bundled>
SCHEMA_STATUS=legacy|outdated|current|skill-outdated|invalid
RAW_PENDING=<material && ingested=false>
RAW_PENDING_EVIDENCE=<evidence && ingested=false>
RAW_UNINTEGRATED=<ingested=true && integrated=false>
RAW_INGEST_ORPHAN=<ingested=true && no page sources reference>
PAGE_CONTESTED_UNLINTED=<contested page absent from LINT>
RAW_INVALID_STATE=<ingested=false && integrated=true>
```

librarian 的两种调用形态：

```text
PLAN: 输入 raw manifest 与粗略主题，输出 PAGE_PLAN，不写馆藏。
INGEST: 输入 raw manifest 与已协调的 PAGE_PLAN，只写白名单页面和 ingested，返回共享文件建议；计划外需求返回 PLAN_DEVIATION。
```

状态提交接口：

```text
mark-integrated <raw/file.md...>
mark-integrated --manifest <newline-delimited-file>
```

迁移接口：

```text
migrate <WIKI_ROOT resolved from doctor>
```

两个写脚本均应预检输入、限制写入 `WIKI_ROOT`、幂等执行，并通过机器可解析的 `KEY=VALUE` 输出结果。

### 文件结构

- `skill/SKILL.md`：触发描述、三类任务路由、doctor 消费规则、INGEST ownership、两阶段并行、Compound Interest。
- `skill/reference/SCHEMA.md`：SCHEMA 版本、受管核心、本地补充区域、raw 状态机、evidence 与共享状态语义。
- `skill/agents/librarian.md`：PLAN/INGEST 模式、PAGE_PLAN 写入白名单、LINT ownership、结构化结果、幂等与验证合同。
- `skill/agents/curator.md`：保留 MAINTAIN ownership，移除 Quality Auditor 依赖并对齐统一 agent 合同。
- `skill/agents/swarm-reader.md`：将输入收紧为显式互斥清单，对齐 DOUBTS 与输出合同，不改变领域责任。
- `skill/scripts/doctor.sh`：SCHEMA 版本、raw 双状态、非法状态和场景化明细。
- `skill/scripts/init.sh`：初始化最新 SCHEMA 与包含 `integrated: false` 的合同入口。
- `skill/scripts/migrate.sh`：版本化升级 SCHEMA 受管核心和 raw frontmatter。
- `skill/scripts/mark-integrated.sh`：对明确批次执行受约束的状态提交。
- `skill/reference/migrations/`：记录各 SCHEMA 版本之间的受管变更与迁移依据；仅在迁移脚本需要独立版本资料时创建。
- `evals/evals.json`：更新既有断言并增加路由、并行、迁移和恢复场景。
- `tests/`：同步 fixture，增加 doctor、迁移和状态脚本的行为回归。

### 风险与未决

- 首次迁移的旧 SCHEMA 尚无受管区标记；脚本只能自动迁移已知旧核心或识别已经写入的目标核心，重叠定制必须失败即停。
- 多 librarian 增加一次页面规划往返；该成本仅在并行收录时发生，用于换取确定的写入集合。
- shell 对 Markdown frontmatter 的处理必须限定在本项目定义的简单顶层合同，不能冒充通用 YAML 解析器。
- 跨文件写入无法完全原子化；每个脚本必须先全量预检、逐文件原子替换并支持幂等重跑。
- 将旧 `ingested: true` 迁移为 `integrated: true` 是对旧流程完成语义的继承，不代表重新审计历史内容。
- 无剩余产品决策；具体脚本退出码、受管区标记文本和测试组织方式属于实现选择，但不得改变上述外部合同。

### 里程碑草案

略过：本次为薄需求，用户明确不需要实施计划。

## Implement Plan

略过：本 SPEC 仅整理需求和草案，不展开 Milestone、Task 或施工顺序。
