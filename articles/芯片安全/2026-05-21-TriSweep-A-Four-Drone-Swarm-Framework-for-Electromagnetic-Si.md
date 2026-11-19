---
title: "TriSweep: A Four-Drone Swarm Framework for Electromagnetic Side-Channel Analysis"
source: "arXiv"
url: http://arxiv.org/abs/2605.22709v1
published: 2026-05-21
fetched: 2026-11-19T12:07:27.218470+08:00
category: "芯片安全"
score: 0
keywords: ["side-channel", "em", "drone"]
sha256: bfe02ab479b90f9107d63326696f0293517a93fe1fed95c807e5e7334e2e2be1
bytes: 1322
truncated: false
body_mode: meta
status: published
published_at: 2026-11-19T12:20:43.910308+08:00
---

# TriSweep: A Four-Drone Swarm Framework for Electromagnetic Side-Channel Analysis

> 来源：arXiv · 2026-05-21 · [原文](http://arxiv.org/abs/2605.22709v1)
> 归档用于安全研究参考；版权归原作者所有。

> ⚠️ 本条为「元数据 + 摘要」归档（论文/PDF/前端渲染页面），完整内容请读原文。

## 收录理由

- **核心**：提出四旋翼无人机编队做**远距离电磁侧信道分析**（0.25–1.5 m），用三架采集机分工覆盖不同频段/掩码。
- **价值**：传统 SCA 假设探针贴得很近；空中平台把威胁模型推到“隔空侧信道”，对部署在野外的设备是新风险。
- **难度**：高 —— 需要无人机平台、天线阵列与信号同步。

Electromagnetic (EM) side-channel analysis traditionally assumes a stationary, close-proximity probe - a threat model that underestimates aerial adversaries. TriSweep is a simulation framework that designs and evaluates a four-drone swarm architecture for autonomous standoff EM-SCA of embedded microcontrollers at 0.25-1.5 m. Three spatially specialized collector drones - Anchor (full-spectrum), Mask Probe (mask-register loading leakage), and Cipher Probe (masked SubBytes output leakage) - feed a stationary Accumulator drone that performs coherent combining (+4.8 dB SNR gain) and second-order mask cancellation via a centered product of the two spatially separated leakage streams. Evaluated against three real ANSSI ASCAD datasets (ATmega8515 masked AES-128 and 50/100-sample desynchronized variants), the framework achieves a simulated key rank of 18 +/- 1.7 (five-seed) at 0.25 m on the primary masked dataset. Profiling-trace cross-correlation alignment reduces single-drone rank from 89 to 21 on the 100-sample-jitter variant, demonstrating compensation for drone hover vibration. A two-channel CNN in the Accumulator converges to a loss of 0.454 (vs. random baseline 5.545) and improves rank on desynchronized datasets. No physical hardware has been fabricated; prototype construction is the planned next step.
