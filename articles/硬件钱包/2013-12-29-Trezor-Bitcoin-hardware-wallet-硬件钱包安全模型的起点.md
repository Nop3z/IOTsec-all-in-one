---
title: "Trezor: Bitcoin hardware wallet：硬件钱包安全模型的起点"
source: "30C3"
url: https://media.ccc.de/v/30C3_-_5545_-_en_-_saal_1_-_201312292200_-_trezor_bitcoin_hardware_wallet_-_pavol_stick_rusnak
published: 2013-12-29
fetched: 2026-11-19T05:40:43.175Z
category: "硬件钱包"
score: 0
keywords: []
sha256: b5870f086359cb0ce7e9eaf6259dc896624b75d811b1a606e8b36140592714dc
bytes: 701
truncated: false
body_mode: notes
status: published
published_at: 2026-11-19T13:40:51.833712+08:00
---

# Trezor: Bitcoin hardware wallet：硬件钱包安全模型的起点

> 来源：30C3 · 2013-12-29 · [原文](https://media.ccc.de/v/30C3_-_5545_-_en_-_saal_1_-_201312292200_-_trezor_bitcoin_hardware_wallet_-_pavol_stick_rusnak)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：安全模型：主机不可信，设备只做签名并显示待签内容；信任根在设备固件与用户确认。
- **价值**：理解现代硬件钱包设计取舍的起点文献。
- **难度**：低 —— 设计介绍型。

Trezor 的设计演讲：把“终端被攻破”视为比特币普及的主要障碍，用独立硬件完成签名，私钥不出设备。
