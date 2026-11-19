---
title: "Sucking dust and cutting grass：逆向机器人并绕过安全机制"
source: "37C3"
url: https://media.ccc.de/v/37c3-11943-sucking_dust_and_cutting_grass_reversing_robots_and_bypassing_security
published: 2023-12-27
fetched: 2026-11-19T05:40:43.175Z
category: "机器人"
score: 0
keywords: []
sha256: c999deaf5eb591da8e460b48c410a17389dfc8cb97487db76030e33afb457f27
bytes: 790
truncated: false
body_mode: notes
kind: practical
status: published
published_at: 2026-11-19T13:40:51.833712+08:00
---

# Sucking dust and cutting grass：逆向机器人并绕过安全机制

> 来源：37C3 · 2023-12-27 · [原文](https://media.ccc.de/v/37c3-11943-sucking_dust_and_cutting_grass_reversing_robots_and_bypassing_security)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：同一套“固件提取 → 绕签名/校验 → 接管”的路径可以跨品类复用；割草机器人还叠加了户外与地理围栏风险。
- **价值**：展示了机器人固件研究的可迁移性，是 IoT 机器人逆向的实战参考。
- **难度**：高 —— 需要固件逆向与硬件调试。

把对 Roborock、Dreame、Xiaomi 扫地机器人的研究扩展到割草机器人等新品类：固件提取、安全启动绕过与云端控制链路。
