---
title: "SIM card technology from A-Z：SIM/eSIM 攻击面全景"
source: "36C3"
url: https://media.ccc.de/v/36c3-10737-sim_card_technology_from_a-z
published: 2019-12-27
fetched: 2026-11-19T05:40:43.175Z
category: "基站"
score: 0
keywords: []
sha256: 1aa58ee1865a60ec91fa839b6d0b30191ec29eb9485f45ddca7487b0b8dd8489
bytes: 686
truncated: false
body_mode: notes
kind: practical
status: published
published_at: 2026-11-19T13:40:51.833712+08:00
---

# SIM card technology from A-Z：SIM/eSIM 攻击面全景

> 来源：36C3 · 2019-12-27 · [原文](https://media.ccc.de/v/36c3-10737-sim_card_technology_from_a-z)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：SIM 是带独立 CPU/OS 的智能卡，OTA 与卡片应用是主要远程攻击面，物理侧则有探针/故障注入。
- **价值**：做 SIM/eSIM 攻击（以及基站侧鉴权研究）的前置知识地图。
- **难度**：低-中 —— 综述型，适合入门。

对 SIM 卡技术做深入技术综述：Java Card 运行时、文件系统、OTA 更新、认证流程，以及这些机制各自带来的攻击面。
