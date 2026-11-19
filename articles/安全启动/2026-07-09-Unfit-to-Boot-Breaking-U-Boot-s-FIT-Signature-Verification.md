---
title: "Unfit to Boot: Breaking U-Boot's FIT Signature Verification"
source: "Binarly"
url: https://www.binarly.io/blog/unfit-to-boot-breaking-u-boots-fit-signature-verification
published: 2026-07-09
fetched: 2026-11-19T10:48:37.911925+08:00
category: "安全启动"
score: 10.4
keywords: ["bypass", "firmware", "u-boot", "bootloader"]
sha256: b151a9b0a141b1bca625e3733edf34f7135c1bd0af55f85229025b2947c5d562
bytes: 811
truncated: false
body_mode: link-only
status: published
published_at: 2026-11-19T11:44:34.056544+08:00
---

# Unfit to Boot: Breaking U-Boot's FIT Signature Verification

> 来源：Binarly · 2026-07-09 · [原文](https://www.binarly.io/blog/unfit-to-boot-breaking-u-boots-fit-signature-verification)
> 自动抓取快照，仅供安全研究参考；版权归原作者所有。

> ⚠️ 原文页面为前端渲染，正文未能完整抓取；此处仅保留摘要，请阅读原文。

## 收录理由

- **核心**：Binarly 在 U-Boot 的 **FIT（Flattened Image Tree）签名校验**里发现 6 个新漏洞，最早影响 v2013.07 稳定版，从 DoS 到处理不可信 FIT 镜像时的任意代码执行。
- **价值**：FIT 是大量设备的信任根入口，拿下它等于绕过后续所有启动阶段的校验——“一次利用、全链失效”。
- **难度**：高：要构造合法但语义畸形的 FIT 结构，并绕过镜像哈希/签名解析的各种边界条件。

The Binarly Research team has identified six new security vulnerabilities within U-Boot’s FIT (Flattened Image Tree) Signature Verification mechanism, a critical component for maintaining the Root of Trust in firmware. These flaws, affecting stable releases dating back to v2013.07, range from denial-of-service (DoS) conditions to potential arbitrary code execution during the processing of untrusted FIT images. This blog post details the technical nature of these vulnerabilities, demonstrating how they can be exploited, and discusses the coordinated disclosure process with the U-Boot maintainers that resulted in upstream patches. Understanding these risks is essential for firmware security, as compromising the initial bootloader can bypass security checks for all subsequent stages of the boot chain.
