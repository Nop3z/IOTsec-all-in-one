---
title: "TRRespass：用锤击“多行”打穿 TRR 缓解（S&P 2020）"
source: "Frattaroli et al."
url: https://arxiv.org/abs/1908.03026
published: 2020-08-01
fetched: 2026-11-23T05:31:26.153Z
category: "芯片安全"
score: 0
keywords: ["rowhammer","spectre"]
sha256: 85b93685cd28e358beedab32bdc0197308f2ede6501717eadf1d183bc8623f5b
bytes: 478
truncated: false
body_mode: notes
kind: theory
status: published
published_at: 2026-11-23T13:31:32.371156+08:00
---

# TRRespass：用锤击“多行”打穿 TRR 缓解（S&P 2020）

> 来源：Frattaroli et al. · 2020-08-01 · [原文](https://arxiv.org/abs/1908.03026)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：TRR 只追踪有限数量 aggressor，hammer 行数超过追踪表容量就会漏检。
- **价值**：“缓解不等于修复”的典型反例，推动 DDR5 RFM 等新防护思路。
- **难度**：高 —— 需精确内存布局与长时间实验。

DRAM 厂商用 Target Row Refresh（TRR）缓解 Rowhammer；TRRespass 证明只要同时锤击更多行（many-sided hammering），TRR 即可被绕过，且在多款主流内存上有效。
