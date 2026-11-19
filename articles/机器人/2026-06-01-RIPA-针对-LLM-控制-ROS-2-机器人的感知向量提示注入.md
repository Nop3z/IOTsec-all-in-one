---
title: "RIPA：针对 LLM 控制 ROS 2 机器人的感知向量提示注入"
source: "arXiv"
url: https://arxiv.org/abs/2606.28649
published: 2026-06-01
fetched: 2026-11-19T05:40:43.175Z
category: "机器人"
score: 0
keywords: []
sha256: 2c2660e67aea3e06df68ae7ce04796f9918c30132df47b96b3c94bee88b09661
bytes: 718
truncated: false
body_mode: notes
status: published
published_at: 2026-11-19T13:40:51.833712+08:00
---

# RIPA：针对 LLM 控制 ROS 2 机器人的感知向量提示注入

> 来源：arXiv · 2026-06-01 · [原文](https://arxiv.org/abs/2606.28649)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：攻击面从“协议/固件”上移到“感知 → 模型 → 动作”链路；默认 ROS 2 无鉴权放大了影响。
- **价值**：具身智能时代的机器人新攻击面：不打代码，打模型的输入语义。
- **难度**：中 —— 需要 ROS 2 与 LLM 控制栈知识。

在默认未启用 DDS 安全（SROS2 认证/加密）的 ROS 2 部署上，通过传感数据里的提示注入操纵 LLM 控制层，让机器人执行攻击者意图的动作。
