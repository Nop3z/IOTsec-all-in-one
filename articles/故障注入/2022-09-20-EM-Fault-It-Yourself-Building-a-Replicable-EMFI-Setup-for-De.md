---
title: "EM-Fault It Yourself: Building a Replicable EMFI Setup for Desktop and Server Hardware"
source: "arXiv"
url: http://arxiv.org/abs/2209.09835v1
published: 2022-09-20
fetched: 2026-11-19T12:07:27.218470+08:00
category: "故障注入"
score: 0
keywords: ["emfi", "setup"]
sha256: 566d3412fc88f5f1fa2cd6057378eb9660f085602c7ec76aa705da531d01c2ad
bytes: 1445
truncated: false
body_mode: meta
status: published
published_at: 2026-11-19T12:20:43.910308+08:00
---

# EM-Fault It Yourself: Building a Replicable EMFI Setup for Desktop and Server Hardware

> 来源：arXiv · 2022-09-20 · [原文](http://arxiv.org/abs/2209.09835v1)
> 归档用于安全研究参考；版权归原作者所有。

> ⚠️ 本条为「元数据 + 摘要」归档（论文/PDF/前端渲染页面），完整内容请读原文。

## 收录理由

- **核心**：完整公开一套可复现的 EMFI 实验装置（线圈、驱动、定位、同步），面向桌面与服务器硬件。
- **价值**：EMFI 论文大多不写装置细节，这篇把“怎么搭”讲全了，是复现和入门的关键拼图。
- **难度**：中 —— 工程量大但门槛可控。

EMFI has become a popular fault injection (FI) technique due to its ability to inject faults precisely considering timing and location. Recently, ARM, RISC-V, and even x86 processing units in different packages were shown to be vulnerable to electromagnetic fault injection (EMFI) attacks. However, past publications lack a detailed description of the entire attack setup, hindering researchers and companies from easily replicating the presented attacks on their devices. In this work, we first show how to build an automated EMFI setup with high scanning resolution and good repeatability that is large enough to attack modern desktop and server CPUs. We structurally lay out all details on mechanics, hardware, and software along with this paper. Second, we use our setup to attack a deeply embedded security co-processor in modern AMD systems on a chip (SoCs), the AMD Secure Processor (AMD-SP). Using a previously published code execution exploit, we run two custom payloads on the AMD-SP that utilize the SoC to different degrees. We then visualize these fault locations on SoC photographs allowing us to reason about the SoC's components under attack. Finally, we show that the signature verification process of one of the first executed firmware parts is susceptible to EMFI attacks, undermining the security architecture of the entire SoC. To the best of our knowledge, this is the first reported EMFI attack against an AMD desktop CPU.
