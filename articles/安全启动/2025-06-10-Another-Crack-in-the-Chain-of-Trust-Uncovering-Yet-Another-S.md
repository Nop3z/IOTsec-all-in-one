---
title: "Another Crack in the Chain of Trust: Uncovering (Yet Another) Secure Boot Bypass"
source: "Binarly"
url: https://www.binarly.io/blog/another-crack-in-chain-of-trust-secure-boot-bypass
published: 2025-06-10
fetched: 2026-11-19T11:35:50.129835+08:00
category: "安全启动"
score: 8.4
keywords: ["bypass", "secure boot", "uefi"]
sha256: ab82b68afedb4d7e73e46aa4090bcf597e6fc13cf5042786c9a4c79c33a31941
bytes: 137
truncated: false
body_mode: link-only
kind: practical
status: published
published_at: 2026-11-19T12:20:43.910308+08:00
---

# Another Crack in the Chain of Trust: Uncovering (Yet Another) Secure Boot Bypass

> 来源：Binarly · 2025-06-10 · [原文](https://www.binarly.io/blog/another-crack-in-chain-of-trust-secure-boot-bypass)
> 自动抓取快照，仅供安全研究参考；版权归原作者所有。

> ⚠️ 原文页面为前端渲染，正文未能完整抓取；此处仅保留摘要，请阅读原文。

## 收录理由

- **核心**：Binarly 发现 CVE-2025-3052：影响大多数 UEFI 设备的 Secure Boot 绕过，可在操作系统加载前执行未签名代码。
- **价值**：覆盖面极广的启动链漏洞——受影响的是“几乎所有 UEFI 设备”，而不是某个厂商型号。
- **难度**：高 —— 需要理解 Secure Boot 变量与固件校验流程。

Binarly uncovers CVE-2025-3052: a Secure Boot bypass affecting most UEFI devices, enabling attackers to run unsigned code before OS load.
