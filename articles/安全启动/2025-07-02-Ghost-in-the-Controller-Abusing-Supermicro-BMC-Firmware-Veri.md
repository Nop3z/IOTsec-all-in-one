---
title: "Ghost in the Controller: Abusing Supermicro BMC Firmware Verification"
source: "Binarly"
url: https://www.binarly.io/blog/ghost-in-the-controller-abusing-supermicro-bmc-firmware
published: 2025-07-02
fetched: 2026-11-19T11:35:50.129835+08:00
category: "安全启动"
score: 8.4
keywords: ["bypass", "firmware", "bmc"]
sha256: 11aa79c7d3a10b88b645a82f19e5f38425418a22a8c853441b6db19bcb62a247
bytes: 227
truncated: false
body_mode: link-only
kind: practical
status: published
published_at: 2026-11-19T11:44:34.056544+08:00
---

# Ghost in the Controller: Abusing Supermicro BMC Firmware Verification

> 来源：Binarly · 2025-07-02 · [原文](https://www.binarly.io/blog/ghost-in-the-controller-abusing-supermicro-bmc-firmware)
> 自动抓取快照，仅供安全研究参考；版权归原作者所有。

> ⚠️ 原文页面为前端渲染，正文未能完整抓取；此处仅保留摘要，请阅读原文。

## 收录理由

- **核心**：Binarly 分析 Supermicro BMC 固件的**签名校验绕过**（CVE-2024-10237），攻击者可在操作系统之下获得持久控制。
- **价值**：把“固件签名校验可被绕过”从理论落到具体产品，是固件供应链审计的典型案例。
- **难度**：高：需要理解 BMC 固件的校验与刷写流程。

Binarly REsearch has investigated alarming vulnerabilities in Supermicro BMC firmware, including a critical signature verification bypass (CVE-2024-10237). These issues provide attackers persistent control beneath the OS level.
