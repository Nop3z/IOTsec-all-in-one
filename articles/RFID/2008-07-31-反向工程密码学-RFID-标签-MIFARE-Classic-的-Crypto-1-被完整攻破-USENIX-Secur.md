---
title: "反向工程密码学 RFID 标签：MIFARE Classic 的 Crypto-1 被完整攻破（USENIX Security 2008）"
source: "USENIX Security 2008"
url: https://www.usenix.org/legacy/event/sec08/tech/nohl.html
published: 2008-07-31
fetched: 2026-11-23T05:25:20.401Z
category: "RFID"
score: 0
keywords: ["classic"]
sha256: 5f6a06993f557d0edacd34ed2c291b84d802850669e55356348c981417f57001
bytes: 1368
truncated: false
body_mode: notes
kind: practical
status: published
published_at: 2026-11-23T13:25:28.351751+08:00
---

# 反向工程密码学 RFID 标签：MIFARE Classic 的 Crypto-1 被完整攻破（USENIX Security 2008）

> 来源：USENIX Security 2008 · 2008-07-31 · [原文](https://www.usenix.org/legacy/event/sec08/tech/nohl.html)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：从“磨掉封装看门阵列”开始，把一颗广泛用于门禁/公交卡的安全芯片彻底拆解；Crypto-1 的弱点使只读/克隆成为可能。
- **价值**：RFID 安全研究的奠基之作：它证明了**物理逆向可以击穿“安全靠保密”的密码设计**，也直接推动 MIFARE 生态换代。
- **难度**：极高 —— 需要芯片剥离、光学显微与逻辑分析，属于硬件逆向的硬核案例。

Nohl、Evans、Starbug、Plötz 对 NXP MIFARE Classic 标签做硬件层逆向：物理剥离芯片、读出加密逻辑，重建 Crypto-1 算法并给出可实用的卡片认证绕过方法。
