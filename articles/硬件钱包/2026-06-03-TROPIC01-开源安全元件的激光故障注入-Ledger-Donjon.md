---
title: "TROPIC01 开源安全元件的激光故障注入（Ledger Donjon）"
source: "Ledger Donjon"
url: https://donjon.ledger.com/blog/tropic01-laser-fault-injection/
published: 2026-06-03
fetched: 2026-11-19T05:40:43.175Z
category: "硬件钱包"
score: 0
keywords: []
sha256: 473944a7171222eaf8806427b15b86c94b4b5edc239f0391d861aad4341acd43
bytes: 718
truncated: false
body_mode: notes
status: published
published_at: 2026-11-19T13:40:51.833712+08:00
---

# TROPIC01 开源安全元件的激光故障注入（Ledger Donjon）

> 来源：Ledger Donjon · 2026-06-03 · [原文](https://donjon.ledger.com/blog/tropic01-laser-fault-injection/)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：开源安全元件的“可审计”不等于“抗物理攻击”；激光 FI 仍是检验信任根的最后一道关。
- **价值**：开源安全元件的首次深度物理评估，对钱包厂商与用户都重要。
- **难度**：极高 —— 需要去封、激光台与固件分析。

对开源架构安全元件 TROPIC01（用于 Trezor Safe 7 等设备）做激光故障注入评估，检验其防护设计与实际抗性。
