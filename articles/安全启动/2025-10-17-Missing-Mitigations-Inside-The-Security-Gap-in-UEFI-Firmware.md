---
title: "Missing Mitigations: Inside The Security Gap in UEFI Firmware"
source: "Binarly"
url: https://www.binarly.io/blog/missing-mitigations-inside-security-gap-uefi-firmware
published: 2025-10-17
fetched: 2026-11-19T11:35:50.129835+08:00
category: "安全启动"
score: 8.0
keywords: ["bypass", "firmware", "uefi"]
sha256: 57f5cc503dca54c81bb317ee8d9a5495f6d9c47253216de238ba6474b2a9a179
bytes: 762
truncated: false
body_mode: link-only
kind: practical
status: published
published_at: 2026-11-19T11:44:34.056544+08:00
---

# Missing Mitigations: Inside The Security Gap in UEFI Firmware

> 来源：Binarly · 2025-10-17 · [原文](https://www.binarly.io/blog/missing-mitigations-inside-security-gap-uefi-firmware)
> 自动抓取快照，仅供安全研究参考；版权归原作者所有。

> ⚠️ 原文页面为前端渲染，正文未能完整抓取；此处仅保留摘要，请阅读原文。

## 收录理由

- **核心**：Binarly 统计大量 UEFI 固件中**缓解措施缺失**的情况（NX、ASLR、栈保护、CFG 等），量化了固件层与操作系统层的安全基线差距。
- **价值**：固件漏洞之所以好打，很大程度是缓解措施缺位；这份统计给出了量化的“为什么”，可直接用于评估目标固件的价值。
- **难度**：中：分析型工作，但对判断“这块固件值不值得挖”极有帮助。

Software mitigations play a critical role in the quest to secure the digital world. Shortly after the discovery and the rise of buffer overflows in the 90s, mitigations were introduced in the software ecosystem and eventually made their way into virtually any piece of software we run on our devices: from browsers to web servers, from OS kernels to userspace applications. Mitigations are typically designed to address one or more classes of vulnerabilities, making their exploitation more difficult. For example, while exploiting a stack overflow without any deployed mitigation is straightforward, the presence of properly implemented stack canaries requires chaining additional vulnerabilities or leveraging more complex techniques to bypass this protection.
