---
title: "NonSense: On the (In)security of FPGA Anti-tamper Sensors"
source: "arXiv"
url: http://arxiv.org/abs/2611.17065v1
published: 2026-11-12
fetched: 2026-11-19T12:07:27.218470+08:00
category: "故障注入"
score: 0
keywords: ["fpga", "glitch"]
sha256: 36536f6cc15a8092f2db547ca7babcdc0bb790b188fabf58a1a9c3d0d5bb16f0
bytes: 1353
truncated: false
body_mode: meta
kind: theory
status: published
published_at: 2026-11-19T12:20:43.910308+08:00
---

# NonSense: On the (In)security of FPGA Anti-tamper Sensors

> 来源：arXiv · 2026-11-12 · [原文](http://arxiv.org/abs/2611.17065v1)
> 归档用于安全研究参考；版权归原作者所有。

> ⚠️ 本条为「元数据 + 摘要」归档（论文/PDF/前端渲染页面），完整内容请读原文。

## 收录理由

- **核心**：评估 FPGA 片上防篡改传感器（检测毛刺/电压异常并触发密钥清零）是否真的可靠，并给出绕过思路。
- **价值**：FPGA 常用于航天、军工与高端网络设备；“防护传感器本身可被欺骗”是很少被讨论的失效面。
- **难度**：高 —— 需要理解传感器采样逻辑与毛刺波形设计。

FPGAs are widely used in mission-critical systems, where a successful physical attack can have serious consequences. This makes resilience to such attacks a critical security requirement. To defend against active physical attacks, such as glitching attacks, modern FPGAs rely on on-chip sensors that detect these disturbances and trigger responses, such as key zeroization, before a device is compromised. These sensors are deployed as both hard-IP blocks and soft-IP cores, and their trustworthiness is often taken for granted. In this work, we challenge that assumption and argue that the sensors themselves are a fragile and underexplored attack surface. Drawing on recent results, we show that both the detection and response mechanisms of state-of-the-art sensors can be bypassed without invasive tampering. We further argue that sensor reliability is reduced by factors rarely captured in threat models, including the spatial and frequency-dependent behavior of the system's power delivery network, which can steer a fault to a target while sparing nearby sensors; environmental conditions such as temperature, which shift detection thresholds; and long-term aging, which drifts sensor calibration and may open silent detection gaps. Finally, we propose a set of countermeasures that harden detection and response mechanisms against these effects.
