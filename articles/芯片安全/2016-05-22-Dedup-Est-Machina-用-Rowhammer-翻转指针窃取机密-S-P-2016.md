---
title: "Dedup Est Machina：用 Rowhammer 翻转指针窃取机密（S&P 2016）"
source: "Bosman et al."
url: https://arxiv.org/abs/1610.02829
published: 2016-05-22
fetched: 2026-11-23T05:31:26.153Z
category: "芯片安全"
score: 0
keywords: ["rowhammer","spectre"]
sha256: 5e515021d2e453eadd32b9011aa2f58a145c56da34f43bdc461b091bfe343f84
bytes: 478
truncated: false
body_mode: notes
kind: theory
status: published
published_at: 2026-11-23T13:31:32.371156+08:00
---

# Dedup Est Machina：用 Rowhammer 翻转指针窃取机密（S&P 2016）

> 来源：Bosman et al. · 2016-05-22 · [原文](https://arxiv.org/abs/1610.02829)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：比特翻转的利用不靠打乱数据，而靠改指针：偏移一位就能构造类型混淆与任意地址读写。
- **价值**：把硬件故障与内存安全漏洞对接的代表作，嵌入式场景同样适用。
- **难度**：高 —— 需精确目标对象布局与翻转可控性。

通过 Rowhammer 翻转内存中指针低位比特，让无害对象指针改指攻击者控制的内存，在真实软件中获得任意读/写。
