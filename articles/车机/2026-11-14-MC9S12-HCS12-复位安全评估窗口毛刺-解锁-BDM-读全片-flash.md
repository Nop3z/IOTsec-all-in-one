---
title: "MC9S12/HCS12 复位安全评估窗口毛刺：解锁 BDM 读全片 flash"
source: "wichers (GitHub, CC0)"
url: https://github.com/wichers/mc9s12-voltage-glitch-attack
published: 2026-11-14
fetched: 2026-11-19T05:21:54.654Z
category: "车机"
score: 0
keywords: []
sha256: 18f327eb1f1e6f865f1c346b2274023288c262ae8df9f52c3fc323036f357933
bytes: 1190
truncated: false
body_mode: notes
status: published
published_at: 2026-11-19T13:22:06.082437+08:00
---

# MC9S12/HCS12 复位安全评估窗口毛刺：解锁 BDM 读全片 flash

> 来源：wichers (GitHub, CC0) · 2026-11-14 · [原文](https://github.com/wichers/mc9s12-voltage-glitch-attack)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：注入点＝MCU 核心电源 VCORE（VCLK 独立供电不参与毛刺）；窗口＝复位后前 150 个总线时钟的安全评估期，先 BKGD 特征化快扫找电压/脉宽甜点、再在窗口内定点扫；触发＝RESET 边沿（USBDM 控复位、Teensy 监视）；判定＝USBDM Connect() 返回 unsecured（rc=33 表示复位超时/时钟不稳）。
- **价值**：汽车级 HCS12 的读保护绕过，完整给出接线图、BOM 与双阶段扫参协议，属于可直接复现的“低成本汽车 MCU”案例。
- **难度**：中高 —— 硬件成本低（Teensy + 模拟开关），但需精确时序与晶振匹配。

MC9S12 在复位后前 150 个总线时钟（2MHz≈75µs）内评估 flash 安全位；用 Teensy 4.1 + 74HC4053 模拟开关对核心电源 VCORE 做精确定时压降，使安全检查失败、BDM 保持 unsecured，再经 USBDM 适配器读出全片 flash。

## 方法论启示

- 汽车 MCU 的安全评估窗口极短（150 总线时钟）：先静态定位，再在邻域细扫。
- 电源域分离（VCORE vs VCLK）是提高毛刺选择性的关键。
