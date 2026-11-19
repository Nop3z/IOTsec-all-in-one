---
title: "Skynet Starter Kit：Unitree 机器人生态的端到端攻破（39C3）"
source: "39C3"
url: https://media.ccc.de/v/39c3-skynet-starter-kit-from-embodied-ai-jailbreak-to-remote-takeover-of-humanoid-robots
published: 2025-12-28
fetched: 2026-11-19T05:40:43.175Z
category: "机器人"
score: 0
keywords: []
sha256: adef54d49344434a00b206889c8e52bb56af52d3f796e6c8c12f0bf49bc04388
bytes: 867
truncated: false
body_mode: notes
status: published
published_at: 2026-11-19T13:40:51.833712+08:00
---

# Skynet Starter Kit：Unitree 机器人生态的端到端攻破（39C3）

> 来源：39C3 · 2025-12-28 · [原文](https://media.ccc.de/v/39c3-skynet-starter-kit-from-embodied-ai-jailbreak-to-remote-takeover-of-humanoid-robots)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：攻击面横跨短距无线、云服务与 AI 控制层；一旦拿到控制链路，就能下发任意动作。
- **价值**：当下最完整的人形机器人攻击链案例，覆盖从协议到 AI 行为层。
- **难度**：极高 —— 需要多协议无线电、云端与机器人控制栈的综合能力。

对 Unitree 机器人生态做系统安全评估：在蓝牙、LoRa 无线电、WebRTC 与云管理服务等多个通道上发现并利用漏洞，实现对人形机器人的远程接管，并演示“具身 AI 越狱”。
