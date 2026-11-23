---
title: "Spectre 与嵌入式处理器：Cortex-A/M 与 RISC-V 的系统性评估"
source: "arXiv 2002.06639"
url: https://arxiv.org/abs/2002.06639
published: 2020-02-15
fetched: 2026-11-23T05:31:26.153Z
category: "芯片安全"
score: 0
keywords: ["rowhammer","spectre"]
sha256: 1962eb642a3ee15326ef0aa7bb197fe58f73edefe8e15623e30009ba6ea8b758
bytes: 498
truncated: false
body_mode: notes
kind: theory
status: published
published_at: 2026-11-23T13:31:32.371156+08:00
---

# Spectre 与嵌入式处理器：Cortex-A/M 与 RISC-V 的系统性评估

> 来源：arXiv 2002.06639 · 2020-02-15 · [原文](https://arxiv.org/abs/2002.06639)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：给出“哪些嵌入式核可能受影响、哪些天生免疫”的对照，并分析资源受限设备上攻防实际代价。
- **价值**：最贴近本仓库主题的一篇：把 Meltdown/Spectre 从桌面 CPU 拉回嵌入式 SoC。
- **难度**：中 —— 综述型，读它比读单个 PoC 更建全貌。

系统评估 Spectre 家族在不同嵌入式处理器上的适用性，对比乱序与顺序核、不同缓存层级与可信执行环境的影响。
