---
title: "Chipolo 蓝牙追踪器：FI 绕调试锁 → 固件逆向 → 蓝牙栈 RCE"
source: "38C3 / Nicolas Oberli"
url: https://media.ccc.de/v/38c3-from-fault-injection-to-rce-analyzing-a-bluetooth-tracker
published: 2024-12-27
fetched: 2026-11-19T05:21:54.654Z
category: "智能家居"
score: 0
keywords: []
sha256: 37066d8630ad25a2d266f5f1b2923bd4c866ecbdc102a0b06b4d20d98eb324a1
bytes: 1100
truncated: false
body_mode: notes
kind: practical
status: published
published_at: 2026-11-19T13:22:06.082437+08:00
---

# Chipolo 蓝牙追踪器：FI 绕调试锁 → 固件逆向 → 蓝牙栈 RCE

> 来源：38C3 / Nicolas Oberli · 2024-12-27 · [原文](https://media.ccc.de/v/38c3-from-fault-injection-to-rce-analyzing-a-bluetooth-tracker)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：注入点/窗口/触发均未在摘要中披露（演讲需看录像）；判定＝调试锁定被绕过、可从被锁芯片中提取固件；后续链条＝逆向弱加密认证（可对任意设备完成认证）+ 蓝牙栈溢出 → RCE。
- **价值**：罕见的“FI → 固件 → 协议/栈漏洞 → 无线 RCE”完整链条，说明物理层一次性投入可以撬开整条无线攻击面。
- **难度**：极高 —— FI 拆锁 + 无符号固件逆向 + 蓝牙协议栈利用三件事叠加。

用故障注入绕过 Dialog/Renesas DA14580 的调试锁定（演讲者称该芯片“此前从未被攻破”），提取被锁固件；再逆向出弱加密认证与蓝牙栈缓冲区溢出，最终拿到蓝牙远程代码执行，漏洞被定性为不可修补。

## 方法论启示

- 一次物理投入可以撬开整条无线攻击面：FI 拆调试锁 → 固件 → 协议栈 RCE。
- 对“从未被破”的芯片，先系统性逆向固件比盲试参数更划算。
