---
title: "ROS 安全：机器人操作系统的攻击面权威分析（vandersanden/Dieber 等，2017）"
source: "arXiv 1709.08826"
url: https://arxiv.org/abs/1709.08826
published: 2017-09-01
fetched: 2026-11-23T05:25:20.401Z
category: "机器人"
score: 0
keywords: ["classic"]
sha256: f158c4b2abbd7b9b2c4fcea2962feb1c056bda26f78c2cbe3f55e168aa31906d
bytes: 1275
truncated: false
body_mode: notes
kind: practical
status: published
published_at: 2026-11-23T13:25:28.351751+08:00
---

# ROS 安全：机器人操作系统的攻击面权威分析（vandersanden/Dieber 等，2017）

> 来源：arXiv 1709.08826 · 2017-09-01 · [原文](https://arxiv.org/abs/1709.08826)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：ROS1 的通信完全信任网络内节点，攻击者只要能接入同一网络即可伪造传感器消息或控制指令；文中给出攻击分类与缓解建议。
- **价值**：机器人安全的基础文献，也是后来 SROS2/ROS2 DDS 安全机制的出发点；读它可以理解“为什么机器人网络必须默认加密与认证”。
- **难度**：低-中 —— 直接在 ROS 环境复现，几乎不需要硬件。

对 ROS1 生态做系统性安全分析：节点间无认证的发布/订阅、明文传输、无访问控制的参数服务器，使攻击者可注入消息、劫持机器人控制。
