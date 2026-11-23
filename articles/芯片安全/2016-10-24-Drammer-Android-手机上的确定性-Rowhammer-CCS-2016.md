---
title: "Drammer：Android 手机上的确定性 Rowhammer（CCS 2016）"
source: "VUSec 等"
url: https://arxiv.org/abs/1610.03526
published: 2016-10-24
fetched: 2026-11-23T05:31:26.153Z
category: "芯片安全"
score: 0
keywords: ["rowhammer","spectre"]
sha256: 360abec03222ec3e65c4d8dce9388408062112eadf7005cb76be4baad80c7e33
bytes: 520
truncated: false
body_mode: notes
kind: theory
status: published
published_at: 2026-11-23T13:31:32.371156+08:00
---

# Drammer：Android 手机上的确定性 Rowhammer（CCS 2016）

> 来源：VUSec 等 · 2016-10-24 · [原文](https://arxiv.org/abs/1610.03526)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：关键突破是“内存布局可预测”：移动端也能稳定选中目标物理页，把概率攻击变为可复现攻击。
- **价值**：嵌入式/移动端 Rowhammer 里程碑，说明内存分配器安全属性会决定硬件缺陷能否被利用。
- **难度**：高 —— 需 Android 内核、内存布局分析与大量实验。

Drammer 在 ARM/Android 上实现确定性 Rowhammer：利用物理内存分配器缺陷预测页表映射，定向翻转页表项获得 root。
