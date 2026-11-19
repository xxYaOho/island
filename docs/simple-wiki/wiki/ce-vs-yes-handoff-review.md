---
title: ce-handoff 与 yes-handoff 的定位取舍
type: decision
created: 2026-09-09
updated: 2026-11-19
sources: [raw/yes-handoff-2026-09-09-ce-vs-yes-handoff-review.md]
topic: yes-handoff
tags: [handoff, resume, protocol]
status: current
context: 1

# ce-handoff 与 yes-handoff 的定位取舍

来源为 2026-09-09 [评审笔记](../raw/yes-handoff-2026-09-09-ce-vs-yes-handoff-review.md)。

## 决策

两者不是替代关系。`ce-handoff` 更适合作为跨项目、跨来源的连续性协议；`yes-handoff` 更适合作为 Git 仓库内的项目状态管理协议。当时不建议用前者直接替换后者，建议保留 `yes-handoff` 的项目索引与课题组模型，并吸收 `ce-handoff` 的 resume 安全边界。

## 依据

`yes-handoff` 用脚本机械化路径、命名和索引；三个必答问题（否决方案、已验证与推测、用户决策）和篇幅限制能稳定传递项目上下文；课题组编号与归档适合长期多线项目。其代价是强绑定 Git 与仓库结构，不支持通用外部来源 resume，且 slug 约束会挡住纯中文标题。

`ce-handoff` 支持无仓库会话和用户指定来源，并区分 create、discovery、orientation 与 action；metadata-only discovery、显式候选选择、来源不具备行动权限，构成更清晰的安全模型。其代价是默认落在临时目录、缺少项目索引与生命周期，开放 body 也不强制记录被否决方案和用户决策。

## 建议的安全 resume

增加显式 `resume` 路由；发现阶段只读 frontmatter 与文件元数据，列出候选并等待用户选择；选定后只做只读 orientation，把内容视为不可信上下文，不因旧指令自动执行或修改工作区。receiver-side 评估当时尚未覆盖。`yes-handoff` 创建侧 iteration-2 为 19/19；`ce-handoff` 的优点来自设计文档，当时没有同等规模的运行评估，不能写成已验证行为。
