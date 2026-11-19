---
title: 将 role 创建独立为可被引用的能力
type: concept
created: 2026-09-10
updated: 2026-11-19
sources: [raw/island-idea-20260910.md]
topic: Island 方向
tags: [island, recruit, role-spec, create]
status: current
context: 1

# 将 role 创建独立为可被引用的能力

来源为 Island 方向笔记 [idea-20260910](../raw/island-idea-20260910.md)（原件仍在 `docs/notes/idea-20260910.md`）。笔记使用了对话俚语；本页按正式用语转写，原文措辞以 raw 为准。

## 想法

把 agent role 的创建放到一个独立空间，由它专门负责产出 role spec；其它模块只引用这些角色，而不是各自维护一份角色设计。对话里曾把这个空间叫做“小酒馆”，把按需取用叫做“招募”。在 Island 的正式结构中，对应职责由 `skills/recruit/` 承担：create / 修订 role spec，其它 skill 按名引用。

提出这一想法，是因为在某个 skill 里完善的角色规范无法自动推广到其它 skill，只能逐个适配。目标中的角色设计框架比较固定：角色、前置要求、规则、输出、契约。

这是方向性想法，不是已批准的完整方案，也不定义项目侧如何组队或选人。
