---
class: evidence
ingested: true
integrated: true
metadata:
  source_repo: "https://github.com/xxYaOho/skill-subagents"
  source_commit: e427ed6
  source_path: docs/1018-strict-case/v1/yes-designer-work-loop-v1-report.md
---
# Round 1 审查反馈（critic-strict）

- 审查对象：`v1/yes-designer-work-loop-v1.md`（742 行，2026-10-17 22:13 版）
- 模式：FULL / intensity=high / Round 1（初始审查）
- 结论：`STATUS: FAIL`
- 统计：FATAL 4 / MAJOR 11 / MINOR 7 / UNVERIFIED 8 / ESCALATE 5

---

yes-designer 设计推进工作流草案 — Round 1 / FULL / high 审查
对象：docs/notes/2026-10-17-yes-designer-design-work-loop-draft.md（742 行，2026-10-17 22:13 版；以下行号均指该文件）

## FATAL

**F1 跨会话推进状态没有持久载体，Resume 不成立**
- 证据：Design Map 建议结构只有 Destination / Notes / Decisions so far / Not yet specified / Out of scope（75-97）；切片状态机 8 个状态（435-458）与 blocking edges / Frontier（430、254）在持久工件中没有字段；ENTRY 读取清单（287-293）不含切片或切片状态；slices 目录只存「问题、结论、证据」（540）。
- 失败路径：会话 1 完成 S2 进入 settled 后中断；会话 2 冷启动 ENTRY 只能读到 map 的散文式 Decisions 与各 slice 的结论，无法判断 S3 是 ready-to-build 还是 needs-decision、S4 是否被 S1 阻塞。后果是重做已 settle 切片，或推进仍需 Human 决策的切片，并在 SETTLE 与 map 写入处分叉。
- 受影响决策：本轮是否开工、进入哪个切片、是否需要 Human。违反 37-38「每轮先 Resume，不靠记忆」与 421「状态保存在工件里」。
- 不可延后：实现 ENTRY 时必须自行发明切片状态落点，等于改设计基线。

**F2 冻结门禁没有可校验的工件表示**
- 证据：(a) Baseline / Structure Decisions 只有 decision_status（164、173），未定义谁在何种条件下置为冻结、是否含 Human 批准、断言与冻结版本如何绑定；(b) FREEZE 要求产出 DOM anchors / structural assertions / geometry expectations / pixel oracle / snapshot plan（345-352），但 Baseline schema（149-165）没有这些字段，且与 535「基线（含 regions 与断言数据）」矛盾，其余产物无存放位置；(c)「本切片代码侧唯一权威」的 Structure Decisions（169）在存储布局（532-553）中没有路径；(d) 冻结后谁可写、BUILD 实施者（含 Delegated mode 的 Coder，362）能否改基线未规定。
- 失败路径：A 在 FREEZE 中形成断言但未落盘即中断；B（或另一个 Coder agent）看到 decision_status: draft，无法证明冻结，按自己理解把 inherit 实现为 new；VERIFY 没有可执行断言，STRUCTURAL_CONFORMANCE（472-480）退化为人工目测，直到像素层通过。
- 受影响决策：BUILD 是否开工、DEVIATION 是否必须回 DECIDE、断言是否足以放行。核心命题「artifact-first 与冻结门禁」由此失效。
- 不可延后：门禁的执行体就是断言数据与冻结状态；推迟等于先建一套无法校验的流程，后续修正会作废已产出的基线。

**F3 结构降级由受检主体自判，验收断言自证**
- 证据：DECIDE 未规定手段由谁决定、`new` 需要什么强度证据（332-341）；Human 介入写作「可介入」（341）；偏离出口「记录 DEVIATION 并回到 DECIDE」（365）也由实施者发起；structural assertions 由同一主体在 FREEZE 生成（349）；REVIEW / HUMAN_REVIEW 只覆盖视觉、delta、golden 与「无法可靠判断的视觉问题」（380、389-392）。
- 失败路径：新截图与既有列表页「看起来不同」→ RELATE unknown → SCAN 记一条排除理由 → DECIDE 选 `new`（337）→ FREEZE 按新结构写断言 → BUILD 从零重写 → 三层验收全过 → REVIEW 通过视觉 → SETTLE 把重写写成 golden → 下一轮 inherit 自坏 golden。背景材料 2026-10-16-design-collaboration-architecture.md L10-17 记录的原始失败模式（视觉等效的重复实现通过验收）与 L46（不得因内容不同静默降级为 new）在草案内仍可复现。
- 受影响决策：结构复用判决的批准权、验收断言的作者独立性。
- 不可延后：这是工件的全部历史动因；若 `new`/`independent` 无独立或 Human 强制确认点，后置 Gate（Critic Gate 对照的仍是同一份自造基线）修不回来。

**F4 无设计稿首轮与 FREEZE 强制产物矛盾**
- 证据：FREEZE 要求在 BUILD 前生成 geometry expectations 与 pixel oracle（345-354）；无设计稿路径却规定首轮实现后由 Human 审查，批准后才生成 golden（602-606）。无设计稿来源包含 Human 描述（105、602），不产生任何测量或像素基准。
- 失败路径：Human 只用文字描述新建页面 → READ 得到无测量、无 source anchor 的 regions → FREEZE 无法产出 geometry expectations / pixel oracle；agent 要么停在 FREEZE（该来源不可用），要么写入空 oracle 继续 BUILD，使 GEOMETRY_CONFORMANCE / REGION_PIXEL_DIFF（482-504）在首轮静默失效且无工件记录。
- 受影响决策：FREEZE 是否放行、无设计稿首轮验收范围、该来源能否进入 BUILD。
- 不可延后：这是草案自己声明支持的核心场景；首轮 oracle 规则属冻结门禁定义，不能由实现阶段临时补。

## MAJOR

- **M1 失败回流与重开路径缺失**：状态机无 verifying→building、needs-review→building、needs-info/needs-decision→ready-to-build 的边（435-446）；INTERPRET_FAILED_REGIONS 输出修复方向（506-517）后无合法状态；VERIFY 内 HUMAN_REVIEW（380）与独立 REVIEW（385-392）内容重叠，签署无记录产物。影响：普通返工无法在状态机内表达，断言/基线是否需重新冻结无规则。跟进：补回流与 re-freeze 判据、合并 Human 验收节点、定义验收记录工件。
- **M2 Region 身份与归档键不稳定**：Design Reading 在 .tmp 可再生（543-544），region.id 无跨轮稳定/命名/唯一性规则；golden 路径 regions/*.png（537）不含 screen×state，S3 这类多状态切片会覆盖同名区域；Design Reading.role（117）、Baseline.preserve/delta（160-161）、Structure Decisions.means[].region（180）三处引用无关联规则；dom_anchor 允许 null（119）但无降级规则。影响：区域级回归会错配或退化为整图。跟进：定义含 screen/state 的 region ID 命名空间与三工件关联约束。
- **M3 Baseline 生命周期与审批不对称**：per-slice 基线（414-415）与 scope.routes/features（152-155）是两套归属；共享页面被后续切片修改时旧 baseline/golden 何时失效、由谁 supersede 未定义；SETTLE 无条件「更新 baseline version」（399），仅 golden 替换要求 Human 批准（562），approval.yaml（538）无 schema/校验；thresholds 与 assertions 可被校准/Retro 改（568、616-618），与 724「断言修改与基线版本绑定，由 Human 批准」矛盾。影响：过期 golden 继续当权威，或共享组件回归漏检。跟进：定义 supersede/失效、审批工件 schema、验收标准变更的唯一批准路径。
- **M4 关系/手段词汇三套且无映射**：Sketch 侧 design_relation variant|independent|unknown（背景 adapter note L60），代码侧 relation 为 inherit|independent|unknown（159）；背景 CLASSIFY copy|extend|variant|independent（2026-10-16 L40），DECIDE means 为 copy|reuse|extend|new|blocked|escalated（334-339）；Design Reading 的 preserve/delta（设计域，117）与 Baseline 的 preserve/delta（代码域，160-161）同词异域。影响：同一 packet 不同会话可得到不同 relation/means，或把设计保留误当代码继承。跟进：给出唯一词表与跨工件映射表。
- **M5 来源能力矩阵缺失、fidelity 不约束验收**：适配只覆盖 Sketch / 原型 HTML / 既有页面（191-233），screenshot 与 human-description 无适配步骤；143 声称来源不影响后续 workflow，但 FREEZE 必须产出测量型 oracle；fidelity（217-220）未映射到 VERIFY 对比类型（495-504）；unknowns[].blocks（138-141）没有阻塞 FREEZE 的规则；无设计稿依赖的「源页面快照」（606）无采集/存放。影响：无测量来源时要么跳过视觉层要么误报，未知项被猜测后写进 golden。跟进：来源能力矩阵 + fidelity→验收层映射 + unknown 阻断规则 + 源页面快照工件。
- **M6 像素/几何验收不可判定**：0.1% 差异占比与区域面积无关（24×24 区域预算 0.58px，1440×900 区域预算约 36×36px，573）；5 次截图取 p95 加余量（580-582）把容差设到噪声上界，真实小回归必过；文字主导区域判定权未定义（可自选 0.90，576）；跨区域/整层通过规则缺失；动态内容（相对时间、随机 id、动画、caret、滚动条）无掩码；无 viewport/DPR 矩阵，meta.yaml 记录环境（586-594）但 VERIFY 未要求比对；「阈值外但可接受」差异（525）无 waiver 记录，下一轮重复失败。影响：该层要么误报被 Human 反复覆盖而失去意义，要么假通过放行真实回归。跟进：面积归一阈值、校准样本协议、分类权、汇总规则、动态掩码、viewport 矩阵、环境失配处理、waiver 工件。
- **M7 Human 确认数据存放在可再生层**：原型 fidelity 由 Human 确认（217）并写入 Design Reading，而 Design Reading 位于 .tmp、可清理（543-545、402），ENTRY 不读 readings。影响：下一轮重问 Human 或由 agent 猜测 fidelity，与 555「下一轮需要读取的进 docs/」矛盾。跟进：把 Human 确认结果落入 baseline 或 map。
- **M8 切片规则与示例自相矛盾**：S1 共享组件切片（675）没有 screen/route/region，不满足「每个切片有自己的区域和快照」（417-418）与「纵向切片含状态和验收」（411-412）；S6 交互连线独立成切片（680）违反原则 1 与 6（426-427），且交互实现会改 DOM/动画，使已 settle 的 S2-S5 golden 失效，而状态机无 settled→building 的重开规则。影响：共享组件切片无法独立验收；交互切片使回归基准失效。跟进：定义组件级验收与 settled 切片重开/再冻结规则。
- **M9 待定清单漏项**：仅列 eval fixture（728），但触发矩阵、bootstrap/ENTRY 安装、assertion schema、region 约定、基线取代规则、与 yes-subagents 的消费合同、viewport 矩阵均未定也未列（背景 2026-10-17 adapter note L128、2026-10-16 L135-139 明示其中多项未决）；724 已把「L3 断言」定为已决定却无 L1/L2/L3 定义。影响：Human 可能在认为范围闭合时批准。跟进：补齐已定/待定账本。
- **M10 ENTRY 路由与 bootstrap 未定义**：quick/chart/work/retro（298）无判据；Design Map 创建条件依赖切片数（68-73），而切片在 CHART 内生成（669），CHART 又属于 map loop（237-251）；bootstrap 仅出现一次（555），AGENTS.md ENTRY 规则只在 Retro 中更新（619）。影响：每次开工的第一个决策无判据，新仓库首次接入行为不确定。跟进：定义路由判据、bootstrap 步骤与 chart/map 顺序。
- **M11 并发写共享工件无所有权/合并规则**：map Decisions（400）、catalog（401）、baseline version（399）、golden（398）均为共享可写文件；「每会话一个切片」（259）不阻止两个会话/子代理并行推进不同切片并触碰同一共享组件。影响：last-write-wins 丢决策，组件目录与基线漂移。跟进：定义写权限、锁/合并与版本化规则。

## MINOR

- 外层 SETTLE（246）与内层 SETTLE（394）同名不同义；示例用未定义的 `Resume`（686）替代 ENTRY（285）。
- `language.generation`（131）语义未定义。
- 阈值表同一行出现两个「0.1」（573），易混；L1/L2/L3 无前置定义（724）。
- 「大小适合一个新会话完成」（420-421）无度量，与 259 表述重复。
- Retro 触发写作「可运行」（610），与 SETTLE「若出现流程失效，进入 RETRO」（403）不一致；Retro 无产物位置与有效性验收。
- bbox 阈值未说明测量工具（584 只规定属性读取用 computed style）。
- 示例 Chart 承担 RELATE 与切片边界生成（668-670），外层职责清单（253-259）未列，阶段职责不一致。

## UNVERIFIED

- 阈值与校准数值（0.1%、SSIM 0.95/0.90、p95+余量）无实测数据；仓库无 eval/fixture，无法确认可达成「不误报且能拦住真实回归」。
- pixelmatch 忽略抗锯齿在目标浏览器/字体/DPR 下对文本渲染噪声是否稳定未验证。
- Sketch packet 是否实际输出 design_relation / source_design_anchor / evidence_refs（背景自述 0.2.x 仍需调整）无法核对。
- yes-subagents 角色合同（Researcher/Coder/Coder Plus/Critic Gate）是否接受本草案产物作为输入未核对；角色文件存在不等于消费入口已定义。
- 方式 A（724）在不改项目依赖与 scripts 的前提下运行 grep/AST/浏览器/pixelmatch/SSIM 的环境前提未验证。
- `.tmp/` 是否在真实目标项目被忽略、`docs/island/designer/` 是否与既有文档/CI 冲突未验证；目标仓库仍无 SKILL.md，触发方式无法验证。
- eval 9 项 fixture（730-742）无仓库/数据/通过标准，无法验证能否区分 needs-info/blocked、needs-decision/escalated 与 preserve 拦截。
- 回归 bbox 0px 在字体加载、滚动条、DPR 下是否可达未验证。

## ESCALATE

- 背景材料词汇未同步：2026-10-16 用 CLASSIFY copy|extend|variant|independent 与 IMPLEMENTATION_BASELINE.inheritance，2026-10-17 adapter note 用 design_relation variant|independent|unknown，草案改用 relation/means；后续引用背景会冲突。
- sketch-copilot-plus 的 coordinate.md / implement.md 仍含 standalone 代码实现路径（adapter note L123-124 自述），若 0.2.x 不澄清，接入后可能出现双编排器。
- 触发矩阵、SKILL.md frontmatter（description 触发词、metadata.version）与发布约定不在草案内；「不依赖记忆」依赖 skill 被可靠触发，属后续打包工作。
- 目标仓库 docs/DESIGN.md 为空文件，草案选择 docs/island/designer/；两者定位与仓库文档布局需 Human 定夺。
- 与 yes-subagents issue #1 的验收条目未在草案中对应/关闭，属治理链路问题。

STATUS: FAIL
