---
title: "How an Old Bug in Lighttpd Gained New Life in AMI BMC, Including Lenovo and Intel products"
source: "Binarly"
url: https://www.binarly.io/blog/how-an-old-bug-in-lighttpd-gained-new-life-in-ami-bmc-including-lenovo-and-intel-products
published: 2025-11-19
fetched: 2026-11-19T11:35:50.129835+08:00
category: "安全启动"
score: 4.8
keywords: ["bmc"]
sha256: 4591e2ae09e79701f6ba7719fd510ba194d1f5ded797c730e6892c040bb9a126
bytes: 667
truncated: false
body_mode: link-only
status: published
published_at: 2026-11-19T12:20:43.910308+08:00
---

# How an Old Bug in Lighttpd Gained New Life in AMI BMC, Including Lenovo and Intel products

> 来源：Binarly · 2025-11-19 · [原文](https://www.binarly.io/blog/how-an-old-bug-in-lighttpd-gained-new-life-in-ami-bmc-including-lenovo-and-intel-products)
> 自动抓取快照，仅供安全研究参考；版权归原作者所有。

> ⚠️ 原文页面为前端渲染，正文未能完整抓取；此处仅保留摘要，请阅读原文。

## 收录理由

- **核心**：一个老的 Lighttpd 漏洞在 AMI BMC 固件中“重获新生”，影响 Lenovo、Intel 等服务器产品。
- **价值**：BMC 长期复用老旧开源组件，供应链里的“老年组件”是系统性风险；这篇给出了从组件 CVE 到 BMC 可利用的完整路径。
- **难度**：中高 —— 需要固件解包与组件版本比对。

The software supply chain is complicated, and all the issues associated with it are something we haven't dealt with before and require a different mindset and approach. The vulnerability in Lighttpd was discovered and fixed back in 2018, but a CVE was not assigned to this vulnerability, and a fix was delivered silently by project maintainers. Frequently, the software that uses the open-sourced components does not consume every single update coming from OSS maintainers and only watches the critical changes or important security fixes to apply. In reality, it's hard to track every change for security issues without specific security advisories and CVE assigned.
