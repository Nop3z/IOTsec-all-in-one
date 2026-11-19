---
title: "UEFI Bootkit Hunting: In-Depth Search for Unique Code Behavior"
source: "Binarly"
url: https://www.binarly.io/blog/uefi-bootkit-hunting-in-depth-search-for-unique-code-behavior
published: 2025-03-13
fetched: 2026-11-19T11:35:50.129835+08:00
category: "安全启动"
score: 6.4
keywords: ["novel", "uefi"]
sha256: dcaadf935e7d0fca851a6f89f173527fc1c0757fbd71d85c2b0d716ffbd915dd
bytes: 493
truncated: false
body_mode: link-only
status: published
published_at: 2026-11-19T11:44:34.056544+08:00
---

# UEFI Bootkit Hunting: In-Depth Search for Unique Code Behavior

> 来源：Binarly · 2025-03-13 · [原文](https://www.binarly.io/blog/uefi-bootkit-hunting-in-depth-search-for-unique-code-behavior)
> 自动抓取快照，仅供安全研究参考；版权归原作者所有。

> ⚠️ 原文页面为前端渲染，正文未能完整抓取；此处仅保留摘要，请阅读原文。

## 收录理由

- **核心**：Binarly 提出基于**独特代码行为**的 UEFI bootkit 检测方法：从已知 bootkit 提炼特征、生成 hunt 规则，再用于发现未知样本。
- **价值**：bootkit 检测是防御侧最薄弱的环节；这套“行为特征 + 规则生成”的方法可直接用于固件取证与应急。
- **难度**：高：需要理解 UEFI 执行环境与恶意组件的行为差异。

In this blog post, the Binarly REsearch team introduces a novel methodology for detecting UEFI bootkits by analyzing their unique code behaviors. By starting from an in-depth analysis of known bootkits, we identify features that can be used for generically detecting bootkits and build rules that we used for hunting new unknown bootkits. Then, we show how these rules can be even further improved, by leveraging advanced static analysis techniques, semantic detection and ML-based clustering.
