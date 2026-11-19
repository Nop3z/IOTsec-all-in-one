---
title: "Why Secure Elements make a crucial difference：安全元件与钱包设计取舍"
source: "Ledger"
url: https://www.ledger.com/why-secure-elements-make-a-crucial-difference-to-hardware-wallet-security
published: 2025-01-01
fetched: 2026-11-19T05:40:43.175Z
category: "硬件钱包"
score: 0
keywords: []
sha256: 816891dbd22c821b51ba72d954fbb634fc41e70e4ad3c83e918024ed490a1289
bytes: 800
truncated: false
body_mode: notes
status: published
published_at: 2026-11-19T13:40:51.833712+08:00
---

# Why Secure Elements make a crucial difference：安全元件与钱包设计取舍

> 来源：Ledger · 2025-01-01 · [原文](https://www.ledger.com/why-secure-elements-make-a-crucial-difference-to-hardware-wallet-security)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：SE 提供独立的安全域与物理防护，但固件与供应链仍是攻击面；设计要在可审计性与防护强度之间平衡。
- **价值**：理解钱包厂商威胁模型与工程约束的第一手材料（注意其厂商立场）。
- **难度**：低 —— 科普/设计说明型。

厂商视角说明安全元件（SE）在硬件钱包中的作用：密钥隔离、PIN 校验、物理防护，以及不同产品在“安全 vs 成本/开源”上的取舍。
