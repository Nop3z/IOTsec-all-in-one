---
title: "ESP32 OTP Transfer EMFI：打 eFuse→shadow 寄存器的纯硬件搬运窗口"
source: "Raelize"
url: https://raelize.com/blog/espressif-systems-esp32-glitching-otp-transfer/
published: 2023-03-10
fetched: 2026-11-19T05:26:20.405Z
category: "故障注入"
score: 0
keywords: []
sha256: 28b532f62185090ab8d975264a51270e0c041961a4000968ec09949d6c4bf33f
bytes: 1382
truncated: false
body_mode: notes
kind: practical
status: published
published_at: 2026-11-19T13:26:46.419198+08:00
---

# ESP32 OTP Transfer EMFI：打 eFuse→shadow 寄存器的纯硬件搬运窗口

> 来源：Raelize · 2023-03-10 · [原文](https://raelize.com/blog/espressif-systems-esp32-glitching-otp-transfer/)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：注入点＝EM 探针贴芯片表面，目标是 OTP PHY→shadow 的搬运电路；窗口＝以复位为锚的 ≈1.25ms 起、以 UART 首条打印收窄到 ≈969µs，block0 越靠前的位要在窗口越早处打；触发＝复位沿（此时还没有任何 UART 输出，无软件触发可用）；判定＝靶应用逐 word 打印 shadow 寄存器（0x3FF5A000…），任一 bit 变化即成功。
- **价值**：纯硬件功能窗口是最“干净”的毛刺靶：不受软件触发抖动影响，且位级腐坏可直接改安全配置。
- **难度**：极高 —— 需要 EM 台架、约 6 万~16 万次实验与严格的时序对齐。

## 方法论启示

- 没有软件锚反而是优势：纯硬件段窗口稳定，复位沿就是最好的触发。
- 位级腐坏比“控制流劫持”更隐蔽：改的是安全配置本身。

不打代码流，而是打 SoC 启动早期把 eFuse 搬到 shadow 寄存器的“OTP Transfer”纯硬件窗口，实现 shadow 寄存器内容的位级腐坏（可关 Secure Boot/读保护位），并演示读出 Secure Boot Key。
