---
title: "SatBleed: Security of Commoditized Communication Modules in Satellites"
source: "arXiv"
url: http://arxiv.org/abs/2610.06258v1
published: 2026-10-05
fetched: 2026-11-19T12:07:27.218470+08:00
category: "卫星安全"
score: 0
keywords: ["satellite", "satcom"]
sha256: 1cd3579a39d3f120521bd924ffc9633c594554a5c5a62cd8db621e4173e0ab5d
bytes: 1231
truncated: false
body_mode: meta
status: published
published_at: 2026-11-19T12:20:43.910308+08:00
---

# SatBleed: Security of Commoditized Communication Modules in Satellites

> 来源：arXiv · 2026-10-05 · [原文](http://arxiv.org/abs/2610.06258v1)
> 归档用于安全研究参考；版权归原作者所有。

> ⚠️ 本条为「元数据 + 摘要」归档（论文/PDF/前端渲染页面），完整内容请读原文。

## 收录理由

- **核心**：SatBleed：分析卫星中被商品化采购的通信模块（COM 子系统）的安全问题。
- **价值**：通信子系统长期在线、默认被信任，是卫星里最像“IoT 设备”的部分；这个切入点很新。
- **难度**：高 —— 需要 SATCOM 硬件与协议分析能力。

Substantial reduction in launch and manufacturing costs has resulted in the accelerated deployment of small satellite missions, with commercial off-the-shelf (COTS) components becoming the prevailing standard for specific subsystems. However, this modular architecture introduces critical security risks, most notably in the Communication Subsystem (COM), which is continuously exposed by design and implicitly trusted as the entry point for command and control. We construct a tailored threat taxonomy for attacks targeting the COM subsystem and analyze representative COM systems from various vendors. Our findings uncover severe vulnerabilities across firmware, protocols, and architectural designs. This work presents the first in-depth security evaluation of widely deployed COTS COM modules employed in small satellites, identifying vulnerabilities affecting dozens of missions. To assess the real-world impact, we correlate our discoveries with open-source telemetry data, inferring at least 28 vulnerable missions in orbit that are susceptible to hostile takeover. Our work reveals that satellite COM subsystems form an attractive and dangerously neglected attack surface, necessitating urgent attention from the community.
