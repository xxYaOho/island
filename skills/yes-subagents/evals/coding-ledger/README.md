# Coding Ledger Evaluation Package

本包验证 yes-subagents 的 coding workflow 如何消费已批准的早期设计，并分别推进薄计划与厚计划。领域 fixture 是“本地账本导入银行 CSV，真实目标是稳定对账”。

本包当前状态：**已准备，未运行**。

## 评估问题

1. Step 1 是否把冻结的 Decision/Draft 转成正确厚度的施工计划，完成 self-review，并交给 fresh strict 审查。
2. Step 2 是否在新线程中只消费批准计划与 PASS 凭证，不重复 Step 1。
3. 薄计划是否由施工 Orchestrator 自己实施，并由独立 `critic-gate` 完成最终 gate。
4. 厚计划是否按 Milestone 各派一次 `coder-plus`，由同一施工 Orchestrator 持续 gate。
5. Coder Plus 是否默认自己实施，只在收益明确时分派边界独立且不提交的叶子，并统一整合、原子提交和验证整个 Milestone。
6. Gate 是否审查 Milestone 最终状态并在 PASS 后推进，而没有把 commit 误作验收凭证。
7. 完成已验证交付所需的全树 token 与费用是多少。

本包不重新测试 go-spec 的需求发现和 Draft 设计质量，也不做 with-skill/without-skill A/B。

## 角色

- **Human**：冻结本包，安排 fresh Eval Host，最终阅读 REPORT 并决定是否修改 skill。
- **Eval Host**：唯一能读取 `host/` 与 `oracle/` 的评估主持者。准备隔离工作区、派遣阶段线程、采集证据、运行验证器并填写 REPORT；不替被测线程作计划或施工决策。
- **Step 1 Plan Orchestrator**：读取某一 case 的 Decision/Draft 和 fixture，生成执行层，完成 self-review，并按当前技能完成独立计划审查。
- **Step 2 Construction Orchestrator**：fresh 线程，只读取批准计划、PASS 凭证、未阻断事项和对应 repo；按当前 coding workflow 实施。
- **Reviewer / Executor leaves**：由被测 Orchestrator 按 yes-subagents 合同决定。Eval Host 不指定某个叶子角色必须出现。

## 信息边界

Eval Host 可以读取全包。任何被测线程只获得 `manifest.json` 为该阶段列出的 `visible_inputs`，不得获得包根路径，也不得读取：

- `host/TRUTH_CARD.md`
- `host/RUBRIC.md`
- `host/observation-schema.json`
- `host/REPORT_TEMPLATE.md`
- `oracle/`
- 其他 case 的材料
- 其他阶段的 transcript

Step 1 可以读取冻结的 Decision、Draft、对应 fixture 副本、go-spec 与 yes-subagents。Step 2 只能读取该 case 的 repo 副本，以及 Step 1 产出的批准计划、切片、最终 strict PASS 凭证和未阻断事项。

## 运行顺序

```text
prepare
  ├─ P-thin  -> E-thin
  └─ P-thick -> E-thick（同一线程依次推进 M1、M2）
collect -> verify -> report
```

薄、厚是两条独立流水线，可以分开运行。每条流水线内部必须顺序执行。`E-thick-M1` 与 `E-thick-M2` 是同一个 E-thick 会话中的两个观察点，不创建两个施工 Orchestrator。

1. Eval Host 运行 `python3 scripts/doctor.py`，确认包本身有效。
2. Eval Host 运行 `python3 scripts/prepare.py RUN_ROOT`，生成薄、厚两个隔离 repo 和 artifact 目录。
3. 按 `manifest.json` 派遣 P-thin 与 P-thick。不得把隐藏材料写入派遣 prompt。
4. 仅当对应 Step 1 获得 fresh strict 的最终 `STATUS: PASS`，才建立该 case 的 Step 2 handoff。
5. 分别派遣 fresh E-thin 和 E-thick。E-thick 必须在同一会话内依次推进 M1、M2。
6. 每个阶段结束立即记录线程 ID、父子关系、起止时间、token 和工件路径。token 缺失时记 `null`，不可填 `0`。
7. 运行 `python3 scripts/verify.py --case thin RUN_ROOT/thin/repo`、`--case thick-m1`、`--case thick-m2` 获取业务验证证据。
8. 按 `host/RUBRIC.md` 判定、按 `host/observation-schema.json` 记录事实，再据 `host/REPORT_TEMPLATE.md` 编写 REPORT。

## 判定层

- **业务正确性**：由黑盒 verifier 与 fixture diff 判断。
- **流程合规性**：由 transcript 中的线程、派遣、输入与 gate 证据判断。
- **裁量观察**：记录 Coder Plus 是否分派、为何分派、上下文是否值得；不以指定角色是否出现判 PASS。
- **运行有效性**：供应商失败、超时、transcript 缺失、fixture 污染或隐藏材料泄漏均标记 INVALID，不进入 skill PASS/FAIL。

## 输出

建议运行目录：

```text
RUN_ROOT/
├── thin/
│   ├── repo/
│   ├── upstream/
│   └── artifacts/{P-thin,E-thin}/
├── thick/
│   ├── repo/
│   ├── upstream/
│   └── artifacts/{P-thick,E-thick}/
└── host/
    ├── observations.json
    ├── timings.json
    ├── verification/
    └── REPORT.md
```

不要在评估运行中修补 skill 或重写 fixture。发现问题原样入 REPORT，待 Human 与 skill 维护者讨论后另开修改轮次。
