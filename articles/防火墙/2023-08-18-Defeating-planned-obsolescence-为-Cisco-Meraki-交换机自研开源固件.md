---
title: "Defeating planned obsolescence：为 Cisco Meraki 交换机自研开源固件"
source: "camp2023"
url: https://media.ccc.de/v/camp2023-57142-defeating_planned_obsolescence_for_cisco_meraki_switches
published: 2023-08-18
fetched: 2026-11-27T02:01:28.690Z
category: "防火墙"
score: 0
keywords: []
sha256: a14b02c972cc6a0423d88a35d13400e09976f32395d184416c4601e83d78ea75
bytes: 638
truncated: false
body_mode: notes
kind: practical
status: published
published_at: 2026-11-27T10:01:29.126372+08:00
---

# Defeating planned obsolescence：为 Cisco Meraki 交换机自研开源固件

> 来源：camp2023 · 2023-08-18 · [原文](https://media.ccc.de/v/camp2023-57142-defeating_planned_obsolescence_for_cisco_meraki_switches)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：云管设备的“不可用”往往由 License 与云端绑定强制，而不是硬件限制；打通启动链即可脱离厂商控制。
- **价值**：把“计划性淘汰”当作安全与可持续性问题来打，硬件 + 启动链 + 管理面的完整逆向过程很少见。
- **难度**：极高 —— 需要板级分析、启动链逆向与网络系统移植。

Cisco Meraki 交换机是云管理且必须订阅 License 才能使用；演讲者为其多款型号开发自由软件固件，讲解硬件概览、原厂固件与启动流程、交换管理软件，以及过程中遇到的挑战。
