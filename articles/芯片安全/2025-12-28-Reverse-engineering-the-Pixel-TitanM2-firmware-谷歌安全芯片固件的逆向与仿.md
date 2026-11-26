---
title: "Reverse engineering the Pixel TitanM2 firmware：谷歌安全芯片固件的逆向与仿真"
source: "39C3"
url: https://media.ccc.de/v/39c3-reverse-engineering-the-pixel-titanm2-firmware
published: 2025-12-28
fetched: 2026-11-26T02:10:22.336Z
category: "芯片安全"
score: 0
keywords: []
sha256: 77c63e01052dfe860e424da7132ce16021c1d0558358d7dbe445effa99356e36
bytes: 654
truncated: false
body_mode: notes
kind: practical
status: published
published_at: 2026-11-26T10:10:22.744554+08:00
---

# Reverse engineering the Pixel TitanM2 firmware：谷歌安全芯片固件的逆向与仿真

> 来源：39C3 · 2025-12-28 · [原文](https://media.ccc.de/v/39c3-reverse-engineering-the-pixel-titanm2-firmware)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：非标准 RISC-V 指令 + 私有外设让常规反汇编失效：作者补全指令语义、建模外设，才能让固件在仿真里跑起来。
- **价值**：安全芯片（TitanM2/T2/SE）是手机与硬件的信任根，公开的固件逆向与仿真方法极少，方法论价值高。
- **难度**：极高 —— 需要 ISA 逆向、Ghidra 插件开发与仿真环境搭建。

TitanM2 是 Pixel 6 以来设备安全的核心，基于改造过的 RISC-V 设计并含大数加速器，谷歌还加了非标准指令。演讲用 Ghidra 逆向其固件并在 Python 中模拟运行，分享过程中遇到的难点。
