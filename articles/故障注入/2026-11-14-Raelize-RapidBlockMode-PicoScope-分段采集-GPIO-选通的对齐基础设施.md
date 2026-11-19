---
title: "Raelize RapidBlockMode：PicoScope 分段采集 + GPIO 选通的对齐基础设施"
source: "Raelize (GPL-3.0)"
url: https://github.com/raelize/RapidBlockMode
published: 2026-11-14
fetched: 2026-11-19T05:26:20.405Z
category: "故障注入"
score: 0
keywords: []
sha256: 9fe4ce9159b7391dd27ef64ca3c2fb50df541165e783d92b6c624b43cb705ada
bytes: 1224
truncated: false
body_mode: notes
status: published
published_at: 2026-11-19T13:26:46.419198+08:00
---

# Raelize RapidBlockMode：PicoScope 分段采集 + GPIO 选通的对齐基础设施

> 来源：Raelize (GPL-3.0) · 2026-11-14 · [原文](https://github.com/raelize/RapidBlockMode)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：注入点＝本工件不注入，是观测与定窗配套；窗口＝段边界对齐 GPIO26 沿（GPIO_OUTPUT_SET(26,1) 包住 ets_aes_crypt）；触发＝UART 命令帧 + GPIO26 脉冲；判定＝抓到对齐的段落/平均轨迹即成功，攻击判定由上层案例负责。
- **价值**：解决“毛刺窗口定不准”的观测基础设施；把选通信号做进靶固件，是最便宜的硬件对齐手段。
- **难度**：中 —— 需要 PicoScope SDK 与自编靶固件，仅在 Windows 实测。

## 方法论启示

- 观测能力决定注入效率：先解决“看得见”，再解决“打得中”。
- 在靶固件里加一个 GPIO 选通脉冲，比在示波器上找特征对齐更稳定。

把 PicoScope 3206d 的 Rapid Block Mode 用起来：一次触发链抓多段 EM/VCC 波形；配套自定义 ESP32 bootloader 靶（K/L/M 三条串口命令 + GPIO26 选通脉冲），为 EMFI/EM 分析提供对齐锚点。
