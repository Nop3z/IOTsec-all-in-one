---
title: "The Forgotten Threat of Voltage Glitching: A Case Study on Nvidia Tegra X2 SoCs"
source: "arXiv"
url: http://arxiv.org/abs/2108.06131v2
published: 2021-08-13
fetched: 2026-11-19T12:07:27.218470+08:00
category: "故障注入"
score: 0
keywords: ["fault-injection", "tegra"]
sha256: 7b152dc84bcf7c0b40075c3766c627cf66f595f45180adf7380a334235b62585
bytes: 1340
truncated: false
body_mode: meta
kind: theory
status: published
published_at: 2026-11-19T12:20:43.910308+08:00
---

# The Forgotten Threat of Voltage Glitching: A Case Study on Nvidia Tegra X2 SoCs

> 来源：arXiv · 2021-08-13 · [原文](http://arxiv.org/abs/2108.06131v2)
> 归档用于安全研究参考；版权归原作者所有。

> ⚠️ 本条为「元数据 + 摘要」归档（论文/PDF/前端渲染页面），完整内容请读原文。

## 收录理由

- **核心**：以 Nvidia Tegra X2 SoC 为例，证明电压毛刺能让处理器跳过安全检查、进入受保护代码路径。
- **价值**：Tegra 广泛用于车机、无人机、边缘设备；文章说明“现代 SoC 也不是天然抗毛刺”。
- **难度**：高 —— 需要定位供电与复位时序，属于硬件动手活。

Voltage fault injection (FI) is a well-known attack technique that can be used to force faulty behavior in processors during their operation. Glitching the supply voltage can cause data value corruption, skip security checks, or enable protected code paths. At the same time, modern systems on a chip (SoCs) are used in security-critical applications, such as self-driving cars and autonomous machines. Since these embedded devices are often physically accessible by attackers, vendors must consider device tampering in their threat models. However, while the threat of voltage FI is known since the early 2000s, it seems as if vendors still forget to integrate countermeasures. This work shows how the entire boot security of an Nvidia SoC, used in Tesla's autopilot and Mercedes-Benz's infotainment system, can be circumvented using voltage FI. We uncover a hidden bootloader that is only available to the manufacturer for testing purposes and disabled by fuses in shipped products. We demonstrate how to re-enable this bootloader using FI to gain code execution with the highest privileges, enabling us to extract the bootloader's firmware and decryption keys used in later boot stages. Using a hardware implant, an adversary might misuse the hidden bootloader to bypass trusted code execution even during the system's regular operation.
