---
title: "Cypherock EMFI Board：低成本开源电磁故障注入台架（附 7 款钱包 DUT）"
source: "Cypherock (GPL-3.0)"
url: https://github.com/Cypherock/emfi-board
published: 2026-11-14
fetched: 2026-11-19T05:26:20.405Z
category: "故障注入"
score: 0
keywords: []
sha256: 057def7b71bf9c19c4227b955ed1eae66f4cdd256fc09f0480eb36c37cf24d24
bytes: 1277
truncated: false
body_mode: notes
status: published
published_at: 2026-11-19T13:26:46.419198+08:00
---

# Cypherock EMFI Board：低成本开源电磁故障注入台架（附 7 款钱包 DUT）

> 来源：Cypherock (GPL-3.0) · 2026-11-14 · [原文](https://github.com/Cypherock/emfi-board)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：注入点＝EM 探针贴芯片表面/背面，双 SMA 可翻转脉冲极性；窗口＝3 轴台网格扫描 + 板上 delay generator 调注入时刻，并用可编程电源做 power-cycle 保证初始态；触发＝外部信号直进 IGBT / 经 STM32L4 编程加延迟 / MCU 自产脉冲；判定＝由 DUT 侧串口/调试口观测（工具本身不判定）。
- **价值**：低成本 EMFI 的完整开源方案（含高压安全注意事项），硬件钱包 DUT 板让复现起点大大前移。
- **难度**：中高 —— 高压电路（1kV 元件）需专业防护与打板能力。

## 方法论启示

- EMFI 的门槛主要是“机械定位 + 高压安全”，不是仪器价格。
- 判定要与注入器解耦：注入器只负责打，靶侧负责说“打中了没有”。

开源 EMFI 板：STM32L4 可编程 PWM 升压 + IGBT 开关把电荷砸到自制 EM 探针，配 3 轴位移台做网格扫描；附 7 款硬件钱包常用 MCU 的 DUT 板与 Python 控制脚本。
