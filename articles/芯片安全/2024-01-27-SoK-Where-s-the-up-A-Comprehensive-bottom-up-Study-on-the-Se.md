---
title: "SoK: Where's the \"up\"?! A Comprehensive (bottom-up) Study on the Security of Arm Cortex-M Systems"
source: "arXiv"
url: http://arxiv.org/abs/2401.15289v3
published: 2024-01-27
fetched: 2026-11-19T12:07:27.218470+08:00
category: "芯片安全"
score: 0
keywords: ["cortex-m", "sok"]
sha256: 94e1e7a9c0e3810491fdda30a40a5a3102c37fc54f5cf443e2e4093c58ed46d1
bytes: 1070
truncated: false
body_mode: meta
status: published
published_at: 2026-11-19T12:20:43.910308+08:00
---

# SoK: Where's the "up"?! A Comprehensive (bottom-up) Study on the Security of Arm Cortex-M Systems

> 来源：arXiv · 2024-01-27 · [原文](http://arxiv.org/abs/2401.15289v3)
> 归档用于安全研究参考；版权归原作者所有。

> ⚠️ 本条为「元数据 + 摘要」归档（论文/PDF/前端渲染页面），完整内容请读原文。

## 收录理由

- **核心**：对 Arm Cortex-M 系统做自底向上的安全梳理：硬件特性、软件栈局限、已知攻击与缓解。
- **价值**：Cortex-M 是 IoT MCU 的绝对主力；这份 SoK 相当于“MCU 安全地图”，适合定位研究空白。
- **难度**：中 —— 综述，但覆盖面很广。

Arm Cortex-M processors are the most widely used 32-bit microcontrollers among embedded and Internet-of-Things devices. Despite the widespread usage, there has been little effort in summarizing their hardware security features, characterizing the limitations and vulnerabilities of their hardware and software stack, and systematizing the research on securing these systems. The goals and contributions of this paper are multi-fold. First, we analyze the hardware security limitations and issues of Cortex-M systems. Second, we conducted a deep study of the software stack designed for Cortex-M and revealed its limitations, which is accompanied by an empirical analysis of 1,797 real-world firmware. Third, we categorize the reported bugs in Cortex-M software systems. Finally, we systematize the efforts that aim at securing Cortex-M systems and evaluate them in terms of the protections they offer, runtime performance, required hardware features, etc. Based on the insights, we develop a set of recommendations for the research community and MCU software developers.
