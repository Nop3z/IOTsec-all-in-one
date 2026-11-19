---
title: "Broken Trust: Fixed Supermicro BMC Bug Gains a New Life in Two New Vulnerabilities"
source: "Binarly"
url: https://www.binarly.io/blog/broken-trust-fixed-supermicro-bmc-bug-gains-new-life
published: 2025-09-24
fetched: 2026-11-19T11:35:50.129835+08:00
category: "安全启动"
score: 6.0
keywords: ["firmware", "bmc"]
sha256: c69373975395973ebf78a7f0ca7e234838187fa177c0eb3e02a2d031a799fe28
bytes: 387
truncated: false
body_mode: link-only
kind: practical
status: published
published_at: 2026-11-19T12:20:43.910308+08:00
---

# Broken Trust: Fixed Supermicro BMC Bug Gains a New Life in Two New Vulnerabilities

> 来源：Binarly · 2025-09-24 · [原文](https://www.binarly.io/blog/broken-trust-fixed-supermicro-bmc-bug-gains-new-life)
> 自动抓取快照，仅供安全研究参考；版权归原作者所有。

> ⚠️ 原文页面为前端渲染，正文未能完整抓取；此处仅保留摘要，请阅读原文。

## 收录理由

- **核心**：此前已修复的 Supermicro BMC 漏洞以两个新 CVE 复活：同一处缺陷换个入口又能绕过校验。
- **价值**：“补丁不彻底”在 BMC 固件里反复出现；这篇给出了同一个 bug 家族被反复利用的完整时间线。
- **难度**：高 —— 需要 BMC 固件校验与 Web 接口两层的分析。

In a previous blog post, we detailed three Supermicro BMC firmware vulnerabilities that were originally found by the NVIDIA Offensive Security Research Team and disclosed earlier this year. All these issues were related to the BMC firmware update process and could be exploited by an attacker with administrative access to the BMC operating system who uploaded a specially crafted image.
