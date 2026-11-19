---
title: "Oops..! I Glitched It Again! How to Multi-Glitch the Glitching-Protections on ARM TrustZone-M"
source: "arXiv"
url: http://arxiv.org/abs/2302.06932v2
published: 2023-02-14
fetched: 2026-11-19T12:07:27.218470+08:00
category: "故障注入"
score: 0
keywords: ["fault-injection", "trustzone"]
sha256: 574f426b4d825f31ced7e98a00a6765dcf2c9e02806d517938f79157b8e2f4f2
bytes: 1792
truncated: false
body_mode: meta
kind: theory
status: published
published_at: 2026-11-19T12:20:43.910308+08:00
---

# Oops..! I Glitched It Again! How to Multi-Glitch the Glitching-Protections on ARM TrustZone-M

> 来源：arXiv · 2023-02-14 · [原文](http://arxiv.org/abs/2302.06932v2)
> 归档用于安全研究参考；版权归原作者所有。

> ⚠️ 本条为「元数据 + 摘要」归档（论文/PDF/前端渲染页面），完整内容请读原文。

## 收录理由

- **核心**：对 ARM TrustZone-M 的“多重毛刺”：连续注入故障绕过针对毛刺的防护措施本身。
- **价值**：很多 MCU 加了毛刺检测/计数器，这篇说明这些防护也能被多次毛刺打穿，对评估 IoT 芯片防护等级很关键。
- **难度**：高 —— 需要在有防护的前提下规划多次故障注入的顺序与时机。

Voltage Fault Injection (VFI), also known as power glitching, has proven to be a severe threat to real-world systems. In VFI attacks, the adversary disturbs the power-supply of the target-device forcing the device to illegitimate behavior. Various countermeasures have been proposed to address different types of fault injection attacks at different abstraction layers, either requiring to modify the underlying hardware or software/firmware at the machine instruction level. Moreover, only recently, individual chip manufacturers have started to respond to this threat by integrating countermeasures in their products. Generally, these countermeasures aim at protecting against single fault injection (SFI) attacks, since Multiple Fault Injection (MFI) is believed to be challenging and sometimes even impractical. In this paper, we present μ-Glitch, the first Voltage Fault Injection (VFI) platform which is capable of injecting multiple, coordinated voltage faults into a target device, requiring only a single trigger signal. We provide a novel flow for Multiple Voltage Fault Injection (MVFI) attacks to significantly reduce the search complexity for fault parameters, as the search space increases exponentially with each additional fault injection. We evaluate and showcase the effectiveness and practicality of our attack platform on four real-world chips, featuring TrustZone-M: The first two have interdependent backchecking mechanisms, while the second two have additionally integrated countermeasures against fault injection. Our evaluation revealed that μ-Glitch can successfully inject four consecutive faults within an average time of one day. Finally, we discuss potential countermeasures to mitigate VFI attacks and additionally propose two novel attack scenarios for MVFI.
