---
title: "Have you patched? Are you sure? The story of the sticky Supermicro BMC bugs"
source: "Binarly"
url: https://www.binarly.io/blog/have-you-patched--are-you-sure--the-story-of-the-sticky-supermicro-bmc-bugs
published: 2026-01-26
fetched: 2026-11-19T11:35:50.129835+08:00
category: "安全启动"
score: 8.8
keywords: ["bypass", "firmware", "bmc"]
sha256: 3ae750afafa46649c5e1213fcc96b9b6543048eb2806816821ed67670f3a8914
bytes: 389
truncated: false
body_mode: link-only
status: published
published_at: 2026-11-19T11:44:34.056544+08:00
---

# Have you patched? Are you sure? The story of the sticky Supermicro BMC bugs

> 来源：Binarly · 2026-01-26 · [原文](https://www.binarly.io/blog/have-you-patched--are-you-sure--the-story-of-the-sticky-supermicro-bmc-bugs)
> 自动抓取快照，仅供安全研究参考；版权归原作者所有。

> ⚠️ 原文页面为前端渲染，正文未能完整抓取；此处仅保留摘要，请阅读原文。

## 收录理由

- **核心**：Eclypsium 追踪 Supermicro BMC 固件漏洞“补了但没补干净”——同一批缺陷以新 CVE 复活，继续影响已打补丁的设备。
- **价值**：BMC 位于操作系统之下、带外可管理，是服务器上最隐蔽的持久化位置；“补丁不彻底”也是供应链安全最真实的常态。
- **难度**：中高：单个 CVE 门槛不一，但隐蔽性与影响面都很大。

After repeatedly bypassing Supermicro's BMC firmware validation fixes, we detail CVE-2025-12006 and CVE-2025-12007 — the latest in a year-long chain of vulnerabilities that allowed persistent arbitrary code execution through manipulated firmware update images. We walk through each bypass technique, analyze the final patches, and assess whether these critical issues are truly resolved.
