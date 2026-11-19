---
title: "SiliconToaster：开源 0–1000V 电磁故障注入发生器（Ledger Donjon）"
source: "Ledger Donjon (GPL-3.0)"
url: https://github.com/Ledger-Donjon/silicon-toaster
published: 2026-11-14
fetched: 2026-11-19T05:26:20.405Z
category: "故障注入"
score: 0
keywords: []
sha256: 480f80246cddb1f9a3f7042c1dfeeae351b80ffe5113c118fe06d4fd82b8d2b0
bytes: 1199
truncated: false
body_mode: notes
kind: practical
status: published
published_at: 2026-11-19T13:26:46.419198+08:00
---

# SiliconToaster：开源 0–1000V 电磁故障注入发生器（Ledger Donjon）

> 来源：Ledger Donjon (GPL-3.0) · 2026-11-14 · [原文](https://github.com/Ledger-Donjon/silicon-toaster)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：注入点＝EM 线圈对 IC 施加电磁脉冲（板级），双插座切极性；窗口＝固件 + tool.py 控制时序，先用 calibrate.py/校准日志把“电压 ↔ 能量”定标；触发＝GUI/串口指令；判定＝由靶侧统计多次注入的结果。
- **价值**：商用 EMFI 注入器的开源替代，而且公开了校准方法——这决定了参数能否跨设备复现。
- **难度**：高 —— 自制高压板 + Rust 固件烧录 + FTDI EEPROM 配置。

## 方法论启示

- 注入强度必须校准（电压↔能量），否则“同一参数”在不同台架上完全不可比。
- 多次注入能力是统计式判定的前提：单次命中可能只是噪声。

ChipSHOUTER 的开源对照件：软件可编程 0–1000V、1J 储能、支持多次注入、双插座线圈极性选择、纯 USB 供电；含 Rust 固件、Python GUI 与电压-能量校准脚本/日志。
