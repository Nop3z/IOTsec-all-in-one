---
title: "findus / fault-injection-library：Pico Glitcher 软件框架 + 12 个 MCU 靶项目"
source: "MKesenheimer (GPL-3.0)"
url: https://github.com/MKesenheimer/fault-injection-library
published: 2026-11-14
fetched: 2026-11-19T05:26:20.405Z
category: "故障注入"
score: 0
keywords: []
sha256: 53a754b03e225b5eb187a6cffd6cd5af07f1de300c8d00869b9cd4644bcef2ee
bytes: 1376
truncated: false
body_mode: notes
kind: practical
status: published
published_at: 2026-11-19T13:26:46.419198+08:00
---

# findus / fault-injection-library：Pico Glitcher 软件框架 + 12 个 MCU 靶项目

> 来源：MKesenheimer (GPL-3.0) · 2026-11-14 · [原文](https://github.com/MKesenheimer/fault-injection-library)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：注入点＝板载毛刺管直打 VCC/GLITCH（crowbar），v2+ 支持四档电压快速切换；窗口＝在上下界内随机滚动（文档称比顺序扫描更快命中热点），Database + 热图做粗扫到细扫；触发＝复位沿或 UART 字节；判定＝由靶侧串口/调试口输出。
- **价值**：把毛刺从“跑一次”变成“参数空间工程化”：命中参数落库、热图可视化、脚本化重放，是预算级 FI 台架最实用的起点。
- **难度**：中 —— 需要基本焊接/接线与 MCU 知识，硬件成本百元级。

## 方法论启示

- 参数空间的“记录与可视化”比单次命中更有价值——命中参数不落库就无法复现。
- 先随机大范围滚动、再对热区细扫，通常比顺序扫参更快。

Pico Glitcher 配套的 Python 故障注入框架：随机滚动 delay×length 参数空间、Database 落盘 + 本地 web 热图、复位/UART 触发、断电重启、多路复用与遗传优化；自带 12 个已验证靶项目（含 STM8 bootloader ROP、nRF52832 AirTag dump）。
