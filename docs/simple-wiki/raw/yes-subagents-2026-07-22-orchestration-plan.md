---
class: material
ingested: true
integrated: true
metadata:
  source_repo: "https://github.com/xxYaOho/skill-subagents"
  source_commit: e427ed6
  source_path: docs/superpowers/plans/2026-07-22-yes-subagents-orchestration.md
---
# Yes Subagents 编排模型优化实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use `yes-subagents` to execute this plan task-by-task. Track every step with the checkbox syntax below.

**Goal:** 按已批准设计重构 Yes Subagents 的编排概念、蜂群调度、飞轮和监察接入规则，并用边界评估证明新契约可执行。

**Architecture:** `skill/SKILL.md` 只持有 Orchestrator 的选择与推进规则；`swarm.md`、`coder.md`、`critic-strict.md`、`critic-gate.md` 分别持有代理自身契约；`evals.json` 用正例、反例和数量边界验证行为。三个里程碑依次建立主编排真源、同步代理契约、补齐评估证据。

**Tech Stack:** Markdown、JSON、Git、Node.js 只读校验

---

## 文件职责

| 文件 | 职责 |
| --- | --- |
| `skill/SKILL.md` | 组合原则、调度形态、飞轮、直接验证与监察路由 |
| `skill/subagents/swarm.md` | 简单、边界明确工作单元的执行契约 |
| `skill/subagents/coder.md` | 需要工程推理的工作单元执行契约 |
| `skill/subagents/critic-strict.md` | 方案、计划和传播性结论的审查契约 |
| `skill/subagents/critic-gate.md` | 已批准计划或直接任务实现的门禁契约 |
| `skill/evals/evals.json` | 正例、反例、数量边界和 BLOCKED 行为评估 |

## 里程碑 1：主编排契约可独立解释

完成后，`SKILL.md` 应能独立回答：是否派子代理、如何组合、采用哪种调度形态、如何运行飞轮、何时直接验证、何时调用 Critic。它不复制 Critic 内部检查清单。

### Task 1：保护现有工作区基线

**Files:**

- Inspect: `skill/SKILL.md`
- Preserve: `skill/.DS_Store`

- [ ] **Step 1：记录当前工作区状态**

Run:

```bash
/opt/homebrew/bin/git status --short
/opt/homebrew/bin/git diff -- skill/SKILL.md
```

Expected:

```text
 M skill/.DS_Store
 M skill/SKILL.md
```

本计划在实施前单独提交，因此执行 Task 1 时不应再出现未跟踪的计划文档。将 `skill/SKILL.md` 当前差异作为实现基线。后续不得恢复或覆盖这些修改；`skill/.DS_Store` 不读、不改、不暂存。

- [ ] **Step 2：确认设计真源**

Run:

```bash
sed -n '1,220p' docs/superpowers/specs/2026-07-22-yes-subagents-orchestration-design.md
```

Expected: 输出包含“概念模型”“调度形态”“飞轮”“直接验证与监察”“Critic 契约”“评估范围”和“验收标准”。

### Task 2：重写 Orchestrator 编排规则

**Files:**

- Modify: `skill/SKILL.md:19`
- Reference: `docs/superpowers/specs/2026-07-22-yes-subagents-orchestration-design.md`

- [ ] **Step 1：更新代理角色摘要**

将角色列表保持为监察、调查、行动三类，并使用以下职责摘要：

```markdown
1. 监察类
   - Critic Strict：审查会被后续决策依赖的方案、计划或结论；完整契约由 `subagents/critic-strict.md` 持有
   - Critic Gate：核验实现是否忠于有效基线、有无回归与契约破坏；完整契约由 `subagents/critic-gate.md` 持有
2. 调查类
   - Quality Auditor：核查存量代码质量与技术债务，不绑定某次具体变更
   - Debugger：复现、定位、给出根因，只诊断不修复
   - Researcher：探索、检索与定位，产出结构化结论而非原始堆砌
3. 行动类
   - Swarm：执行简单、同质、边界明确的工作单元；可单体、普通并行或作为蜂群成员派遣
   - Coder：执行需要跨文件推理、项目约定或需求质疑的工作单元；可单体、普通并行或作为蜂群成员派遣
```

- [ ] **Step 2：用四维模型替换模式式派遣原则**

在角色列表之后建立以下结构：

```markdown
## 编排原则

### 组合

组合是所有任务都具备的基础编排能力，不是可选模式。根据目标组合调查、行动和监察职责，可串行，也可并行。简单一次性任务仍由主代理直接完成。

### 调度形态

- 1 个工作单元：单体派遣。
- 2–3 个独立工作单元：普通并行或组合派遣。
- 至少 4 个独立工作单元：考虑蜂群调度。

蜂群按任务所需的独立工作单元总数判断；重试、返工和分批不增加成员计数。并发不足时分批运行仍属于同一次蜂群。工作单元形成依赖链时改为串行，不再视为蜂群。

蜂群不绑定代理类型。简单、同质单元优先使用 `swarm`；需要工程推理的单元使用 `coder`；调查或监察代理也可组成蜂群。每个成员必须有明确职责、输入边界和输出契约。

### 飞轮

飞轮遵循“产出 → 验证 → 修正 → 再验证 → 停止”。单次飞轮最多修正 10 轮；初始产出、蜂群分批和代理重试不计入修正轮次。
```

- [ ] **Step 3：建立直接验证与监察路由**

用以下原则替换宽泛的视觉豁免和“所有产出必须审查”表述：

```markdown
### 直接验证与监察

优先使用与产出最接近、可重复的直接验证，例如真实渲染、浏览器交互、自动化测试、类型检查、构建、契约测试或基准测试。直接验证足以覆盖主要风险时，不为流程完整追加监察。

直接验证无法覆盖隐藏风险时，再选择监察代理：

- 方案、计划或会被后续决策依赖的结论使用 `critic-strict`。
- 存在实现忠实度、回归、契约或隐藏正确性风险时使用 `critic-gate`。

监察补充直接验证的盲区，不能替代测试、构建或真实渲染。完整审查契约由对应 subagent 文件持有。

典型边界：

- 视觉修改在真实页面或截图足以验收时跳过监察。
- 性能、数据、状态、接口、安全或无障碍语义存在隐藏风险时接入监察。
- 有自动化测试不代表自动豁免监察；测试可能未覆盖关键风险。
- 改动量大不代表必须接入监察；大量可直接验收的视觉修改仍可跳过监察。
```

- [ ] **Step 4：将现有流程改写为飞轮语义**

保留“讨论 → 实施 → 完成”和“行动 ↔ 确认 → 完成”两条参考流程，但执行以下精确调整：

```text
循环式 / 循环派遣 / 迭代轮次  -> 飞轮 / 修正轮次
组合式派遣                     -> 组合原则
完成必须等于 Critic PASS       -> 完成等于直接验证满足验收标准，或所需监察 PASS
实现默认搭配 critic-gate       -> 仅在直接验证后仍有剩余风险时搭配 critic-gate
```

保留以下现有规则：审查与产出分离、等待审查结果再修改、PASS 即停、BLOCKED 可由 Orchestrator 补全一次、阶段结束等待用户确认、Handoff。

- [ ] **Step 5：验证里程碑 1**

Run:

```bash
rg -n "组合是所有任务|至少 4 个独立工作单元|飞轮遵循|直接验证足以|有自动化测试不代表|改动量大不代表" skill/SKILL.md
rg -n "循环式|组合式|所有.*必须.*critic|完成 = 对应子代理" skill/SKILL.md
```

Expected: 第一条命令匹配全部六项新规则；第二条命令无输出。

- [ ] **Step 6：里程碑 1 门禁**

派遣 `critic-gate`，输入已批准设计中与 `SKILL.md` 相关的验收标准、当前 `skill/SKILL.md` 和差异。要求检查概念分层、双写真源、原有规则保留情况。只有 `STATUS: PASS` 后进入里程碑 2。

## 里程碑 2：代理契约与主编排规则一致

完成后，`swarm` 和 `coder` 均可成为蜂群成员；两个 Critic 的输入契约支持主技能声明的路由，且内部无旧前提冲突。

### Task 3：解除执行代理与调度形态的绑定

**Files:**

- Modify: `skill/subagents/swarm.md:3`
- Modify: `skill/subagents/coder.md:3`

- [ ] **Step 1：更新 `swarm` 定义**

将 description 改为：

```yaml
description: >
  Focused executor for simple, well-defined, self-contained work units. Use alone, in ordinary parallel dispatch, or as a member of a swarm when many independent units share the same narrow contract. Each unit needs an assigned file set or scope. Returns a concise result.
```

将正文中“默认与 sibling 并行”的假设改为条件表达：当它作为并行或蜂群成员运行时，边界不得与其他成员重叠。保留最小修改、验证、禁止破坏性操作和 `STATUS: DONE | BLOCKED`。

- [ ] **Step 2：更新 `coder` 定义**

将 description 改为：

```yaml
description: >
  Implementation specialist for work units that need cross-file reasoning, project conventions, or requirement challenge. Use alone, in ordinary parallel dispatch, or as a member of a swarm when complex units are independent and have non-overlapping boundaries. Writes and verifies code, then returns the change and decisions.
```

保留 Coder 的工程判断、需求质疑、最小修改和验证职责。增加一条边界规则：作为并行或蜂群成员时，发现共享文件、共享状态或前后依赖必须返回 `BLOCKED`，不得自行扩大范围。

- [ ] **Step 3：验证执行代理定义**

Run:

```bash
rg -n "Use alone, in ordinary parallel dispatch, or as a member of a swarm" skill/subagents/swarm.md skill/subagents/coder.md
rg -n "Serial implementation|NOT for many independent|that is swarm" skill/subagents/coder.md
```

Expected: 第一条命令在两个文件均匹配；第二条命令无输出。

### Task 4：扩展 Critic Strict 契约

**Files:**

- Modify: `skill/subagents/critic-strict.md:3`

- [ ] **Step 1：扩展输入与前置条件**

description 和 PRECONDITION 必须明确接受：

```text
需要被后续决策依赖的 proposal、plan、report 或 research conclusion，以及该产出的目标。
```

缺少产出或目标时返回 `STATUS: BLOCKED`，不得补造。

- [ ] **Step 2：按产出类型分支检查**

在 Operating rules 中建立两个分支：

```markdown
- Proposal / plan：攻击根假设、失败场景、阶段边界和可验证里程碑。
- Report / research conclusion：核验证据来源、证据与结论的对应关系、推理缺口和传播风险。
```

公共规则继续检查规模、并发、错误路径、可逆性、隐藏耦合和成本。里程碑缺失仅能对多阶段计划构成 FATAL，不得用于报告或调研结论。

- [ ] **Step 3：同步输出语义**

将 `ESCALATE: concerns outside plan review` 改为 `ESCALATE: concerns outside this artifact review`。保留 FATAL、MAJOR、MINOR、UNVERIFIED、ESCALATE 和 `STATUS: PASS | FAIL | BLOCKED`。

### Task 5：扩展 Critic Gate 契约

**Files:**

- Modify: `skill/subagents/critic-gate.md:3`

- [ ] **Step 1：建立两类互斥基线**

description、开场说明和 PRECONDITION 必须共同表达：

```markdown
1. 如果存在已批准计划，必须使用该计划当前节点及其验收标准。
2. 仅在不存在已批准计划时，才使用用户直接任务的明确目标、约束和验收标准。
```

执行者不得选择更宽松的基线。直接任务缺少可验证验收标准时返回 `STATUS: BLOCKED`，指出缺失项及提供者。

- [ ] **Step 2：保持门禁范围**

继续依次检查 Fidelity、Regression、Contracts、Correctness、Leftovers。将仅适用于批准计划的措辞改为中性的 `baseline`，并保留“不得重开架构”；若基线本身可疑，只在 ESCALATE 记录，不影响门禁判定。

- [ ] **Step 3：修正文档错误**

将 `ollow-ups` 改为 `follow-ups`。

- [ ] **Step 4：验证里程碑 2**

Run:

```bash
rg -n "report|research conclusion|Proposal / plan|Report / research conclusion" skill/subagents/critic-strict.md
rg -n "approved plan|direct user task|acceptance criteria|baseline" skill/subagents/critic-gate.md
rg -n "Scope is the PLAN|after a plan has already passed|architecture and plan were already validated|ollow-ups" skill/subagents/critic-strict.md skill/subagents/critic-gate.md
```

Expected: 前两条命令匹配新契约；第三条命令无输出。

- [ ] **Step 5：里程碑 2 门禁**

派遣 `critic-gate`，输入批准设计、里程碑 1 已通过的主技能、四个 subagent 文件和差异。检查主技能路由能否满足每个 PRECONDITION，以及旧的串行、计划专属前提是否清除。只有 `STATUS: PASS` 后进入里程碑 3。

## 里程碑 3：评估覆盖边界与反例

完成后，JSON 可解析，每项新规则至少有一个真实用户式 prompt，正反例可以区分机械调度与风险判断。

### Task 6：扩展评估集

**Files:**

- Modify: `skill/evals/evals.json:38`

- [ ] **Step 1：补强现有单体派遣用例**

修改 ID 3 的 `expected_output`，明确要求：

```text
识别为单个排查工作单元，单体派遣 debugger；不使用普通并行或蜂群。Debugger 给出根因和修复建议。
```

- [ ] **Step 2：保留现有 5 个用例并增加以下用例**

新增 ID 6–16，使用以下 `eval_name` 和预期行为：

| ID | eval_name | Prompt 核心 | expected_output 核心 |
| --- | --- | --- | --- |
| 6 | `three-units-ordinary-parallel` | 三个独立模块做同类小修改 | 普通并行，不称为蜂群 |
| 7 | `four-simple-units-swarm` | 四个独立图标文件做机械替换 | 使用至少四个 `swarm` 成员组成蜂群 |
| 8 | `four-complex-units-coder-swarm` | 四个独立插件模块分别做跨文件兼容修复 | 使用 `coder` 作为蜂群成员，明确不重叠边界 |
| 9 | `mixed-research-swarm` | 仓库内五份指定文档需要独立核验 | 调查代理可组成蜂群并汇总；每个成员获得具体文件边界 |
| 10 | `bulk-visual-direct-verification` | 大量按钮、输入框和排版调整 | 真实渲染直接验收，不因改动量大追加 Critic |
| 11 | `frontend-performance-residual-risk` | 优化列表渲染性能和数据缓存 | 基准/测试后仍评估隐藏风险，并接入相应 Critic |
| 12 | `backend-direct-verification-sufficient` | 小型纯函数修复，验收标准与测试充分 | 直接验证满足后停止，不机械追加 Critic |
| 13 | `backend-tests-insufficient` | 事务幂等改动已有单元测试但未覆盖并发 | 测试不构成自动豁免，接入 `critic-gate` |
| 14 | `swarm-batched-counting` | 六个单元、并发仅三个、其中一个重试 | 仍是六成员蜂群，分批和重试不增加成员数 |
| 15 | `strict-report-branch` | 正式调研报告将作为后续决策依据 | `critic-strict` 按证据与推理链审查，不要求里程碑 |
| 16 | `gate-direct-task-blocked` | 直接实现任务没有可验证验收标准 | `critic-gate` 返回 BLOCKED，不虚构基线 |

每个对象继续使用现有字段：`id`、`eval_name`、`prompt`、`expected_output`、`files`。Prompt 必须写成真实用户请求，expected_output 必须明确代理选择、验证方式和停止条件。

- [ ] **Step 3：验证 JSON 与覆盖范围**

Run:

```bash
node -e "const x=require('./skill/evals/evals.json'); if(x.evals.length!==16) throw new Error('expected 16 evals'); const ids=x.evals.map(v=>v.id); if(new Set(ids).size!==16) throw new Error('duplicate ids'); console.log('16 evals, unique ids')"
rg -n "普通并行|蜂群|直接验证|critic-gate|critic-strict|BLOCKED|重试" skill/evals/evals.json
```

Expected:

```text
16 evals, unique ids
```

第二条命令应覆盖全部边界关键词。

### Task 7：完成整体门禁

**Files:**

- Verify: `skill/SKILL.md`
- Verify: `skill/subagents/swarm.md`
- Verify: `skill/subagents/coder.md`
- Verify: `skill/subagents/critic-strict.md`
- Verify: `skill/subagents/critic-gate.md`
- Verify: `skill/evals/evals.json`

- [ ] **Step 1：运行静态检查**

Run:

```bash
/opt/homebrew/bin/git diff --check
node -e "JSON.parse(require('fs').readFileSync('skill/evals/evals.json','utf8')); console.log('evals valid')"
rg -n "循环式|组合式|Serial implementation|NOT for many independent|Scope is the PLAN|after a plan has already passed|architecture and plan were already validated|ollow-ups" skill
```

Expected: `git diff --check` 无输出；Node 输出 `evals valid`；最终 `rg` 无输出。

- [ ] **Step 2：确认用户改动与范围**

Run:

```bash
/opt/homebrew/bin/git status --short
/opt/homebrew/bin/git diff --stat
/opt/homebrew/bin/git diff -- skill/SKILL.md skill/subagents/swarm.md skill/subagents/coder.md skill/subagents/critic-strict.md skill/subagents/critic-gate.md skill/evals/evals.json
```

Expected: 只出现六个目标文件和原有未处理的 `skill/.DS_Store`；设计与计划文档已经分别提交，不应作为未跟踪文件出现。`skill/SKILL.md` 的原有快速开始、视觉豁免意图和上下文卫生内容应被保留或由已批准的新规则明确取代，不得静默丢失。

- [ ] **Step 3：运行行为评估**

按 `skill/evals/evals.json` 运行 with-skill 行为评估。至少检查每个输出是否明确包含 expected_output 中的调度形态、代理类型、验证方式和停止条件。若当前仓库没有自动 runner，使用独立子代理抽样 ID 3、6、7、8、10、11、12、13、14、15、16。评估结论保留在当前会话，并连同具体通过、失败证据传给最终 `critic-gate`；不新增评估结果文件，不扩大六个实现文件范围。不得把“JSON 可解析”当作行为通过。

- [ ] **Step 4：最终 Critic Gate**

派遣 `critic-gate`，输入已批准设计、完整实施差异、静态检查结果和行为评估结果。重点检查：

```text
- 主技能与 subagent 契约是否双写或冲突
- 蜂群是否仍被 swarm 独占
- Coder 是否可作为蜂群成员且边界安全
- 直接验证是否真正优先于机械监察
- 有测试和改动量两个反例是否生效
- 两类 Critic PRECONDITION 是否可满足
- 原有阶段确认、PASS 即停、BLOCKED、Handoff 是否保留
```

只有 `STATUS: PASS` 后才可完成实施。

- [ ] **Step 5：提交实现**

在确认六个目标文件的最终差异包含并保留 `skill/SKILL.md` 既有相关修改后，暂存六个目标文件，不暂存 `skill/.DS_Store`：

```bash
/opt/homebrew/bin/git add skill/SKILL.md skill/subagents/swarm.md skill/subagents/coder.md skill/subagents/critic-strict.md skill/subagents/critic-gate.md skill/evals/evals.json
/opt/homebrew/bin/git commit -m "feat(skill): refine subagent orchestration"
```

Expected: 一个原子实现提交；`skill/.DS_Store` 仍保持未暂存。
