---
title: "Seeing is Not Believing：打破机器人的物理-数字信任边界"
source: "arXiv"
url: https://arxiv.org/abs/2609.08280
published: 2026-09-01
fetched: 2026-11-19T05:40:43.175Z
category: "机器人"
score: 0
keywords: []
sha256: d0c808559477a0547a7ed3de2de4809b4907ff3ca60a2a60c08f03472d84d056
bytes: 723
truncated: false
body_mode: notes
status: published
published_at: 2026-11-19T13:40:51.833712+08:00
---

# Seeing is Not Believing：打破机器人的物理-数字信任边界

> 来源：arXiv · 2026-09-01 · [原文](https://arxiv.org/abs/2609.08280)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：攻击目标是“证据链”而非控制流：让日志/遥测与实际动作不一致，可绕过审计与安全监控。
- **价值**：提出了机器人安全的新判定维度——物理行为与数字证据的一致性。
- **难度**：中高 —— 需要 ROS 2 内部机制与验证器设计知识。

揭示 ROS 2 中的严重缺陷：仅修改一个环境变量，攻击者就能让机器人的物理行为与其执行证据脱钩，从而骗过下游验证器。
