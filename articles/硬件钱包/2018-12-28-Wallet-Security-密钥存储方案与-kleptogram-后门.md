---
title: "Wallet Security：密钥存储方案与“kleptogram”后门"
source: "35C3"
url: https://media.ccc.de/v/35c3-9492-wallet_security
published: 2018-12-28
fetched: 2026-11-19T05:40:43.175Z
category: "硬件钱包"
score: 0
keywords: []
sha256: bcd88a2d5655c9d665fd7aa34f372866569be4f73cde3dbd5b78b017932dfd81
bytes: 707
truncated: false
body_mode: notes
status: published
published_at: 2026-11-19T13:40:51.833712+08:00
---

# Wallet Security：密钥存储方案与“kleptogram”后门

> 来源：35C3 · 2018-12-28 · [原文](https://media.ccc.de/v/35c3-9492-wallet_security)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：威胁不只来自漏洞，也来自实现者主动植入的隐蔽通道；硬件钱包需要可验证的固件与流程。
- **价值**：从供应链与后门角度审视钱包安全，补上“漏洞视角”之外的一半。
- **难度**：中 —— 概念与方案对比为主。

比较不同加密货币密钥存储方式，重点讨论“kleptogram”类密码学后门：看起来正常的实现里藏有只有作者能利用的泄密通道。
