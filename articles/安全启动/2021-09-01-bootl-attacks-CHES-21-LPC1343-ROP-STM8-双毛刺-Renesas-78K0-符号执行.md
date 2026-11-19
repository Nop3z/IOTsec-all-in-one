---
title: "bootl-attacks（CHES'21）：LPC1343 ROP / STM8 双毛刺 / Renesas 78K0 符号执行制导"
source: "CHES 2021 配套仓库 (GPL-3.0)"
url: https://github.com/janvdherrewegen/bootl-attacks
published: 2021-09-01
fetched: 2026-11-19T05:21:54.654Z
category: "安全启动"
score: 0
keywords: []
sha256: a416fd35b70c30204ea709749648952eba65573843121f4940846d47d8d1eb36
bytes: 1346
truncated: false
body_mode: notes
status: published
published_at: 2026-11-19T13:22:06.082437+08:00
---

# bootl-attacks（CHES'21）：LPC1343 ROP / STM8 双毛刺 / Renesas 78K0 符号执行制导

> 来源：CHES 2021 配套仓库 (GPL-3.0) · 2021-09-01 · [原文](https://github.com/janvdherrewegen/bootl-attacks)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：注入点＝GIAnT Python 移植版（Ztex Spartan-6 FPGA 开源毛刺器），78K0 打 REGC 内核电压脚、STM8 打 VddA/Vdd1；窗口＝STM8 用单/双毛刺三维扫描（option bytes 决定 1 或 2 个毛刺），78K0 用符号执行求路径约束把窗口收窄到 ~100µs；触发＝NRST/RST 复位沿 + bootloader 命令传输边沿；判定＝读保护被绕过、可读出受保护 flash。
- **价值**：“用符号执行/动态分析压缩毛刺搜索空间”的方法论，是目前把硬件毛刺从“碰运气”变成工程流程的代表作；含汽车 MCU 案例。
- **难度**：极高 —— 需要解焊上转接板、FPGA 毛刺器，以及符号执行/二进制分析能力。

《Fill your Boots》的配套代码：用二进制分析（片上动态分析/符号执行）把毛刺参数搜索从指数复杂度压缩到可执行；三个案例分别是 LPC1343 的纯软件 ROP、STM8 首个完整文档化的双毛刺读保护绕过、以及 Renesas 78K0 汽车 bootloader 的符号执行精确制导。
