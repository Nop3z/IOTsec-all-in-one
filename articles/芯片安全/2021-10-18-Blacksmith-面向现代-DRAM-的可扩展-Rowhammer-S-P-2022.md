---
title: "Blacksmith：面向现代 DRAM 的可扩展 Rowhammer（S&P 2022）"
source: "Google"
url: https://arxiv.org/abs/2110.09101
published: 2021-10-18
fetched: 2026-11-23T05:31:26.153Z
category: "芯片安全"
score: 0
keywords: ["rowhammer","spectre"]
sha256: de0dec80d9f3533cea09f7fa3c045b49d228aeb3bcaea1324bea9fc76667d299
bytes: 510
truncated: false
body_mode: notes
kind: theory
status: published
published_at: 2026-11-23T13:31:32.371156+08:00
---

# Blacksmith：面向现代 DRAM 的可扩展 Rowhammer（S&P 2022）

> 来源：Google · 2021-10-18 · [原文](https://arxiv.org/abs/2110.09101)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：核心是“非均匀、带频率成分”的锤击波形：不同芯片敏感度不同，自动搜索让攻击可扩展。
- **价值**：当前研究现状参考点：Rowhammer 已从单一模式演进到针对芯片定制波形。
- **难度**：极高 —— 需自建测试平台与大量样片实验。

Blacksmith 提出基于频率的 hammer 模式，针对不同 DRAM 芯片自动搜索有效访问模式，在 DDR4 等设备上实现可靠翻转并绕过先进防护。
