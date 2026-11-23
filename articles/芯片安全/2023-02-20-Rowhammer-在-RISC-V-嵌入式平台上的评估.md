---
title: "Rowhammer 在 RISC-V / 嵌入式平台上的评估"
source: "arXiv 2302.09544"
url: https://arxiv.org/abs/2302.09544
published: 2023-02-20
fetched: 2026-11-23T05:31:26.153Z
category: "芯片安全"
score: 0
keywords: ["rowhammer","spectre"]
sha256: f7b98f4e4262d5b06fa4ec47d1500380fc145826898693f9bf64361097a4bf24
bytes: 484
truncated: false
body_mode: notes
kind: theory
status: published
published_at: 2026-11-23T13:31:32.371156+08:00
---

# Rowhammer 在 RISC-V / 嵌入式平台上的评估

> 来源：arXiv 2302.09544 · 2023-02-20 · [原文](https://arxiv.org/abs/2302.09544)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：嵌入式平台缺少 ECC、内存控制器更简单，理论上更易被锤击，但受限于内存容量与分配器行为。
- **价值**：把 Rowhammer 推进到 RISC-V/IoT 生态，最贴近本仓库主题。
- **难度**：高 —— 需板级实验与固件开发。

针对 RISC-V 与嵌入式平台评估 Rowhammer 可行性：讨论小型 SoC 的内存控制器、缓存与保护机制差异，给出该平台攻击成功率的实验结果。
