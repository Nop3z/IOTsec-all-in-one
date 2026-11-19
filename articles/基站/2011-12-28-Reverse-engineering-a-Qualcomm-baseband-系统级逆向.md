---
title: "Reverse-engineering a Qualcomm baseband：系统级逆向"
source: "28C3"
url: https://media.ccc.de/v/28c3-4735-en-reverse_engineering_a_qualcomm_baseband
published: 2011-12-28
fetched: 2026-11-19T05:40:43.175Z
category: "基站"
score: 0
keywords: []
sha256: f17eb40c9ad10874fb94563c8238c97b6d37c31b5e9e75ece1cd99a1bf166b25
bytes: 748
truncated: false
body_mode: notes
status: published
published_at: 2026-11-19T13:40:51.833712+08:00
---

# Reverse-engineering a Qualcomm baseband：系统级逆向

> 来源：28C3 · 2011-12-28 · [原文](https://media.ccc.de/v/28c3-4735-en-reverse_engineering_a_qualcomm_baseband)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：从固件镜像到任务/协议栈结构的逆向路径，是把基带从黑盒变成可研究目标的关键一步。
- **价值**：后续所有 Qualcomm 基带漏洞研究的方法论源头。
- **难度**：高 —— 需要固件提取、逆向与 ARM/专有 RTOS 知识。

当时已有演讲指出各型号 GSM 协议栈的漏洞，但没人把基带当作完整系统来理解；本演讲展示对 Qualcomm 基带的固件提取、结构分析与系统级逆向。
