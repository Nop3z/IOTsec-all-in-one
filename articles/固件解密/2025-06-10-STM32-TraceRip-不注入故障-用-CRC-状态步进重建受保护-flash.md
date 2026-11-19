---
title: "STM32-TraceRip：不注入故障，用 CRC 状态步进重建受保护 flash"
source: "HWIO USA 2025 / Marcus Engineering"
url: https://hardwear.io/wp-content/uploads/2026/03/TraceRip-Hardwear.pdf
published: 2025-06-10
fetched: 2026-11-19T05:26:20.405Z
category: "固件解密"
score: 0
keywords: []
sha256: 078604990230bf0d64cc360d16b4fc7c80572cf88df4d4f404f9d1dd5b64cc89
bytes: 1420
truncated: false
body_mode: notes
kind: practical
status: published
published_at: 2026-11-19T13:26:46.419198+08:00
---

# STM32-TraceRip：不注入故障，用 CRC 状态步进重建受保护 flash

> 来源：HWIO USA 2025 / Marcus Engineering · 2025-06-10 · [原文](https://hardwear.io/wp-content/uploads/2026/03/TraceRip-Hardwear.pdf)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：注入点＝无毛刺，物理接触只是常规 SWD + 供电控制；窗口＝延时扫描（断电→复位→等精确 delay→触发一次总线读制造 HardFault 冻结 CPU→读寄存器/SRAM→delay 递增）；触发＝无外部信号，纯软件时序；判定＝重建出的 flash 与已知明文比对（CRC 校验通过）。
- **价值**：补上“非毛刺”这一格：当 FI 被缓解时，把“状态泄露”当侧信道往往更稳定、更隐蔽。
- **难度**：高 —— 单次捕获 50 小时级，需要高度自动化的框架与耐心。

## 方法论启示

- 故障注入不是唯一出路：寄存器/中间状态泄露可能比注入更稳定。
- 把“读一次寄存器”变成高精度时序采样，就能做状态重建。

RDP Level 1 下 SWD 只能读 SRAM 时：用精确延时复位 + 寄存器现场快照，步进观察启动期 CRC-over-flash 的中间状态，从 r0（CRC 累加器）/r2（地址）/r4（剩余位）等寄存器序列反推明文 flash 字节，最终恢复 100% 应用区（单次完整捕获约 2.5 天，需 3–5 次补洞）。
