---
title: "Signed and Dangerous: BYOVD Attacks on Secure Boot"
source: "Binarly"
url: https://www.binarly.io/blog/signed-and-dangerous-byovd-attacks-on-secure-boot
published: 2025-09-10
fetched: 2026-11-19T11:35:50.129835+08:00
category: "安全启动"
score: 8.4
keywords: ["firmware", "secure boot", "uefi"]
sha256: dfd969603729db05505d06bf7dc80a41c76b5e5390631d54a330577ad47aedeb
bytes: 328
truncated: false
body_mode: link-only
kind: practical
status: published
published_at: 2026-11-19T11:44:34.056544+08:00
---

# Signed and Dangerous: BYOVD Attacks on Secure Boot

> 来源：Binarly · 2025-09-10 · [原文](https://www.binarly.io/blog/signed-and-dangerous-byovd-attacks-on-secure-boot)
> 自动抓取快照，仅供安全研究参考；版权归原作者所有。

> ⚠️ 原文页面为前端渲染，正文未能完整抓取；此处仅保留摘要，请阅读原文。

## 收录理由

- **核心**：Binarly 分析 Secure Boot 信任模型里被签名的 UEFI 模块规模：现代平台通常信任约 1500 个签名模块，部分构建超过 4000 个；这些合法签名的驱动可被用来关闭安全机制（BYOVD）。
- **价值**：BYOVD 是绕开 Secure Boot/内核防护的主流手法，文章把“信任面到底有多大”量化了出来。
- **难度**：中高：利用现成签名驱动，但需要理解 Windows/UEFI 的加载与防护机制。

The Binarly REsearch team conducted an analysis of signed UEFI modules and the findings show the true scale of the attack surface hidden inside Secure Boot's trust model. Across thousands of firmware images, we found that modern platforms typically trust approximately 1,500 signed modules, with some builds peaking above 4,000.
