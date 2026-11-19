---
title: "Honest to a Fault: Root-Causing Fault Attacks with Pre-Silicon RISC Pipeline Characterization"
source: "arXiv"
url: http://arxiv.org/abs/2503.04846v2
published: 2025-03-05
fetched: 2026-11-19T12:07:27.218470+08:00
category: "故障注入"
score: 0
keywords: ["fault-injection", "risc-v"]
sha256: 0b928ab7556556bf50608d848a656c6abd9c4c91042dd4906f1ce3c364eb978a
bytes: 1106
truncated: false
body_mode: meta
status: published
published_at: 2026-11-19T12:20:43.910308+08:00
---

# Honest to a Fault: Root-Causing Fault Attacks with Pre-Silicon RISC Pipeline Characterization

> 来源：arXiv · 2025-03-05 · [原文](http://arxiv.org/abs/2503.04846v2)
> 归档用于安全研究参考；版权归原作者所有。

> ⚠️ 本条为「元数据 + 摘要」归档（论文/PDF/前端渲染页面），完整内容请读原文。

## 收录理由

- **核心**：在流片前用 RISC-V 流水线特征化来定位故障注入的根因，把物理层扰动与软件层后果对上。
- **价值**：“为什么这个毛刺能跳过这条指令”通常说不清；这篇给出了从流水线到系统软件的因果链分析方法。
- **难度**：高 —— 需要 RTL/仿真与故障模型知识。

Fault injection attacks represent a class of threats that can compromise embedded systems across multiple layers of abstraction, such as system software, instruction set architecture (ISA), microarchitecture, and physical implementation. Early detection of these vulnerabilities and understanding their root causes along with their propagation from the physical layer to the system software is critical to secure the cyberinfrastructure. This present presents a comprehensive methodology for conducting controlled fault injection attacks at the pre-silicon level and an analysis of the underlying system for root-causing behavior. As the driving application, we use the clock glitch attacks in AI/ML applications for critical misclassification. Our study aims to characterize and diagnose the impact of faults within the RISC-V instruction set and pipeline stages, while tracing fault propagation from the circuit level to the AI/ML application software. This analysis resulted in discovering a novel vulnerability through controlled clock glitch parameters, specifically targeting the RISC-V decode stage.
