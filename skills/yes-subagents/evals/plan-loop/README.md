# Plan Loop Eval

专门测试 `plan <--> strict` 循环的复杂性膨胀，与具体领域无关。

## 用例

一份留白较多的工程计划（notes-cli 多设备同步，约 120 行），配判级锚（第一用途 + 4 条成功标准 + 非目标 + 不可接受失败形态）。计划刻意留白的部分：

- 冲突判定的时间戳精度、相同时戳处理；
- 状态文件 schema 与部分进度；
- 重试幂等与部分失败回滚；
- 多进程并发锁；
- 测试矩阵与故障注入。

这些留白是审查者最容易要求「补机制」的地方，用于观察是否膨胀。

## 流程

```text
R1 strict（with_skill vs old_skill baseline）
  ↓
lead 处理 findings（with_skill）
  ↓
R2 strict 复审 plan-v2（with_skill）
```

第一轮含 without baseline 对比（旧契约），后续迭代只跑 with。

## 观察指标

- R1：FATAL 是否绑定判级锚；留白与形式缺口是否被判 FATAL；验收合同缺失是否保留 FATAL 资格。
- Lead：是否先分诊；只修真缺陷 FATAL 还是全量修复；新增机制是否声明服务标准；plan-v2 行数与机制增量。
- R2：FATAL 是否较 R1 下降；修正是否引入新的形式完备性要求；是否收敛。

## 运行约定

- 输出目录：`yes-subagents-workspace/iteration-13/<phase>/<config>/outputs/`。
- 旧契约 baseline：`yes-subagents-workspace/iteration-11/skill-snapshot/`。
- 每个 run 另存 `session.md`。
