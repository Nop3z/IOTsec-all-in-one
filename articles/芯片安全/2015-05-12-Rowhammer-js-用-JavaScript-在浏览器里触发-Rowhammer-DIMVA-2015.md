---
title: "Rowhammer.js：用 JavaScript 在浏览器里触发 Rowhammer（DIMVA 2015）"
source: "Gruss et al."
url: https://arxiv.org/abs/1505.02573
published: 2015-05-12
fetched: 2026-11-23T05:31:26.153Z
category: "芯片安全"
score: 0
keywords: ["rowhammer","spectre"]
sha256: 0a3bb1e619620616cbbf62bd952c6c74f3b6eeb35ca827fde0d436d4c9684482
bytes: 547
truncated: false
body_mode: notes
kind: theory
status: published
published_at: 2026-11-23T13:31:32.371156+08:00
---

# Rowhammer.js：用 JavaScript 在浏览器里触发 Rowhammer（DIMVA 2015）

> 来源：Gruss et al. · 2015-05-12 · [原文](https://arxiv.org/abs/1505.02573)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：方法学价值在于“把物理攻击搬进沙箱”：用 JIT 与缓存行为放大访问密度，绕过浏览器内存保护。
- **价值**：确立“远程/沙箱内也能打硬件”的威胁模型，后续大量变体沿用它。
- **难度**：中高 —— 需理解缓存/预取与访存调度，但不需要任何特权。

首个纯 JavaScript 的 Rowhammer 实现：通过精心构造的访存序列在浏览器沙箱内触发比特翻转，证明攻击者无需本地权限即可利用硬件缺陷。
