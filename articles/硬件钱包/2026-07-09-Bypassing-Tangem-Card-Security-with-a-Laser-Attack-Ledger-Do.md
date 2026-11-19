---
title: "Bypassing Tangem Card Security with a Laser Attack（Ledger Donjon）"
source: "Ledger Donjon"
url: https://donjon.ledger.com/blog/bypassing-tangem-card-security-with-laser-attack/
published: 2026-07-09
fetched: 2026-11-19T05:40:43.175Z
category: "硬件钱包"
score: 0
keywords: []
sha256: 930a66aa18eedcc89143861791b5f09942806e288fd9906d081497ef0037addd
bytes: 724
truncated: false
body_mode: notes
kind: practical
status: published
published_at: 2026-11-19T13:40:51.833712+08:00
---

# Bypassing Tangem Card Security with a Laser Attack（Ledger Donjon）

> 来源：Ledger Donjon · 2026-07-09 · [原文](https://donjon.ledger.com/blog/bypassing-tangem-card-security-with-laser-attack/)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：卡片形态把安全全押在芯片上，一旦物理防护被绕过，用户没有任何二次确认手段。
- **价值**：卡片钱包是主流形态之一，这类公开的物理攻击案例很少。
- **难度**：极高 —— 需要去封与激光注入设备。

对 Tangem 卡片式硬件钱包做激光攻击：绕开其安全机制，说明“无屏卡片 + 安全芯片”形态在物理攻击下的边界。
