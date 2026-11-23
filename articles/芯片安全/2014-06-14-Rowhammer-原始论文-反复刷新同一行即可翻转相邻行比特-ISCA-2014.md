---
title: "Rowhammer 原始论文：反复刷新同一行即可翻转相邻行比特（ISCA 2014）"
source: "Kim et al., ISCA 2014"
url: https://users.ece.cmu.edu/~yoonguk/papers/kim-isca14.pdf
published: 2014-06-14
fetched: 2026-11-23T05:31:26.153Z
category: "芯片安全"
score: 0
keywords: ["rowhammer","spectre"]
sha256: 765b181405aad7090b83b7dd9048d0160a2b4a956d4b05f815dad42c164363d3
bytes: 695
truncated: false
body_mode: notes
kind: theory
status: published
published_at: 2026-11-23T13:31:32.371156+08:00
---

# Rowhammer 原始论文：反复刷新同一行即可翻转相邻行比特（ISCA 2014）

> 来源：Kim et al., ISCA 2014 · 2014-06-14 · [原文](https://users.ece.cmu.edu/~yoonguk/papers/kim-isca14.pdf)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：攻击面是 DRAM 物理特性本身：纯访存模式即可制造比特翻转，绕过所有软件层保护；论文给出“hammer 多少次能翻转”的量化结论。
- **价值**：十年硬件漏洞研究的起点，Drammer、Rowhammer.js、TRRespass 等都建立在它之上。
- **难度**：中 —— 纯软件触发，但需要选定内存布局与足够长的 hammer 时间。

Kim 等人证明 DRAM 单元电荷会因频繁访问相邻行而泄漏：在同一行反复 hammer，就能让相邻行的比特从 0 翻 1、1 翻 0，无需任何软件漏洞。论文给出可复现实验方法，并讨论 DDR3 上可达到的翻转率与物理原因。
