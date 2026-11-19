---
title: "RP2350 预算级激光故障注入（Glasgow + DEF CON 33 Playground）"
source: "courk (MIT/GPL-3.0)"
url: https://github.com/courk/rp2350-lfi
published: 2026-11-14
fetched: 2026-11-19T05:26:20.405Z
category: "故障注入"
score: 0
keywords: []
sha256: e080c0d7983225907ad7be2a41b0bacc931fb5e06f42d1828c8e80996cb51fed
bytes: 1245
truncated: false
body_mode: notes
status: published
published_at: 2026-11-19T13:26:46.419198+08:00
---

# RP2350 预算级激光故障注入（Glasgow + DEF CON 33 Playground）

> 来源：courk (MIT/GPL-3.0) · 2026-11-14 · [原文](https://github.com/courk/rp2350-lfi)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：注入点＝RP2350 die 背面红外激光脉冲（相机成像 + XYZ 台定位）；窗口＝由配套 writeup 静态分析 QSPI 镜像组织确定签名校验相关位置，playground 在此基础上半自动扫描；触发＝Glasgow 数字侧控制链；判定＝状态监控（固件行为/镜像校验结果）。
- **价值**：预算级激光 FI 的完整工具链；“vanilla/patched 双镜像对照”是很聪明的工程技巧，能快速区分打偏与打中。
- **难度**：高 —— 需要去封/背面照射、激光与精密台架。

## 方法论启示

- 用双镜像对照做判定，能快速把“打偏”和“打中”分开。
- 激光 FI 的可达性正在快速下降：预算级设备也能做。

配套代码：Glasgow Interface Explorer 配置 QSPI flash 内容（vanilla/patched 双镜像）、激光控制、目标固件加载与状态监控；playground 为 DEF CON 33 演示台（Pi 控 XYZ 台/红外照明/相机/激光能量与脉冲）。
