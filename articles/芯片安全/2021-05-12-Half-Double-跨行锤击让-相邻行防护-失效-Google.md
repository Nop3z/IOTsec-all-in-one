---
title: "Half-Double：跨行锤击让“相邻行防护”失效（Google）"
source: "Google Project Zero"
url: https://arxiv.org/abs/2106.05850
published: 2021-05-12
fetched: 2026-11-23T05:31:26.153Z
category: "芯片安全"
score: 0
keywords: ["rowhammer","spectre"]
sha256: ff482ac4f6c91bf600c459ffbf379728e54f4ddef5b5aca5f12fb73ec7d938a1
bytes: 497
truncated: false
body_mode: notes
kind: theory
status: published
published_at: 2026-11-23T13:31:32.371156+08:00
---

# Half-Double：跨行锤击让“相邻行防护”失效（Google）

> 来源：Google Project Zero · 2021-05-12 · [原文](https://arxiv.org/abs/2106.05850)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：物理机制是“邻居的邻居”耦合：DRAM 耦合效应不是一阶的，防护模型必须覆盖高阶耦合。
- **价值**：Google 亲自下场的研究，推动内存厂商把防护范围从相邻行扩到多行。
- **难度**：极高 —— 需长期实验与内存物理结构理解。

Google 发现只影响隔行的翻转模式：hammer 一行会翻转两行之外的比特（half-double），而现有防护只盯紧邻行，对此完全失效。
