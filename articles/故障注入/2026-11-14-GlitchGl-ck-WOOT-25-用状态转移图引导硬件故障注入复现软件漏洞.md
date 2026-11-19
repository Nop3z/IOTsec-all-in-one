---
title: "GlitchGlück（WOOT'25）：用状态转移图引导硬件故障注入复现软件漏洞"
source: "USENIX WOOT 2025 (Apache-2.0)"
url: https://github.com/Secure-Embedded-Systems/woot2025-GlitchGluck
published: 2026-11-14
fetched: 2026-11-19T05:26:20.405Z
category: "故障注入"
score: 0
keywords: []
sha256: 65504353111f648a949fa0a01d4cf1b590a96f3cf903dd31a7ea3226bdd41cd8
bytes: 1300
truncated: false
body_mode: notes
kind: practical
status: published
published_at: 2026-11-19T13:26:46.419198+08:00
---

# GlitchGlück（WOOT'25）：用状态转移图引导硬件故障注入复现软件漏洞

> 来源：USENIX WOOT 2025 (Apache-2.0) · 2026-11-14 · [原文](https://github.com/Secure-Embedded-Systems/woot2025-GlitchGluck)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：注入点＝RTL 仿真级（非物理毛刺），在 testbench 中对指定 RTL 状态做故障操作；窗口＝由 DSTG 指引（rtl-demo 演示状态记录与建图）；触发＝仿真状态；判定＝目标软件漏洞显现（溢出触发/指令复制/PIN 绕过）。
- **价值**：在流片前、无硬件时就能回答“毛刺能造成什么软件后果”，把故障注入从碰运气变成状态空间搜索。
- **难度**：高 —— 需要 RTL 仿真环境与对目标设计的理解。

## 方法论启示

- 故障注入的“引导”与 fuzz 的覆盖率引导同源：目标状态明确，搜索才有效。
- 仿真级先跑通“会造成什么后果”，再决定值不值得上物理台架。

在 RTL 仿真 testbench 中记录扫描状态、生成动态状态转移图（DSTG），用图搜索定位能把执行引向特定软件错误状态的注入点；三个案例：OpenMSP430 缓冲区溢出、Ibex 指令复制、PicoRV32 PIN 校验绕过。
