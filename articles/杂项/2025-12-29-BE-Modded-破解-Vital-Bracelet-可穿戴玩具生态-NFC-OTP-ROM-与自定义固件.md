---
title: "BE Modded：破解 Vital Bracelet 可穿戴玩具生态（NFC、OTP ROM 与自定义固件）"
source: "39C3"
url: https://media.ccc.de/v/39c3-be-modded-exploring-and-hacking-the-vital-bracelet-ecosystem
published: 2025-12-29
fetched: 2026-11-26T02:10:22.336Z
category: "杂项"
score: 0
keywords: []
sha256: 9b14a068a4432967de0ad175bd25e2a073da45408e49bfeb07a004fb42859381
bytes: 631
truncated: false
body_mode: notes
kind: practical
status: published
published_at: 2026-11-26T10:10:22.744554+08:00
---

# BE Modded：破解 Vital Bracelet 可穿戴玩具生态（NFC、OTP ROM 与自定义固件）

> 来源：39C3 · 2025-12-29 · [原文](https://media.ccc.de/v/39c3-be-modded-exploring-and-hacking-the-vital-bracelet-ecosystem)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：小众可穿戴设备的完整破解链：冷门 MCU 架构 → OTP ROM 读取 → 绕过安全 → 刷自定义固件。
- **价值**：“低价值玩具”往往防护最弱、资料最少，是练习完整硬件破解链的最佳标的；NFC 交互部分对门禁/支付类设备也有借鉴。
- **难度**：高 —— 需要冷门架构逆向与 OTP 读取手段。

Vital Bracelet 是 2021–2024 年在售的互动健身玩具生态：手环硬件、记忆卡内容与 NFC 通信的 App。演讲从冷门 CPU 架构讲到对外交互，覆盖 OTP ROM dump、安全绕过与自定义固件。
