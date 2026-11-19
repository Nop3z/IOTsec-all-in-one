---
title: "One Glitch to Rule Them All: Fault Injection Attacks Against AMD's Secure Encrypted Virtualization"
source: "arXiv"
url: http://arxiv.org/abs/2108.04575v4
published: 2021-08-10
fetched: 2026-11-19T12:07:27.218470+08:00
category: "故障注入"
score: 0
keywords: ["fault-injection", "sev"]
sha256: 5b1e6c6f97905085fa8ad79e47b5f8ad75a33c68e15a9ca3c56ee695fe1ee877
bytes: 1505
truncated: false
body_mode: meta
kind: theory
status: published
published_at: 2026-11-19T12:20:43.910308+08:00
---

# One Glitch to Rule Them All: Fault Injection Attacks Against AMD's Secure Encrypted Virtualization

> 来源：arXiv · 2021-08-10 · [原文](http://arxiv.org/abs/2108.04575v4)
> 归档用于安全研究参考；版权归原作者所有。

> ⚠️ 本条为「元数据 + 摘要」归档（论文/PDF/前端渲染页面），完整内容请读原文。

## 收录理由

- **核心**：通过电压毛刺攻击 AMD Secure Processor（AMD-SP），进而攻破 SEV 加密虚拟机——绕过 SEV 的隔离承诺。
- **价值**：云上机密计算的核心卖点是 SEV，而物理毛刺把它降级；对“硬件信任根可被物理扰动手撕开”是标志性案例。
- **难度**：高 —— 需要精确的毛刺时序与对 AMD-SP 固件流程的理解。

AMD Secure Encrypted Virtualization (SEV) offers protection mechanisms for virtual machines in untrusted environments through memory and register encryption. To separate security-sensitive operations from software executing on the main x86 cores, SEV leverages the AMD Secure Processor (AMD-SP). This paper introduces a new approach to attack SEV-protected virtual machines (VMs) by targeting the AMD-SP. We present a voltage glitching attack that allows an attacker to execute custom payloads on the AMD-SPs of all microarchitectures that support SEV currently on the market (Zen 1, Zen 2, and Zen 3). The presented methods allow us to deploy a custom SEV firmware on the AMD-SP, which enables an adversary to decrypt a VM's memory. Furthermore, using our approach, we can extract endorsement keys of SEV-enabled CPUs, which allows us to fake attestation reports or to pose as a valid target for VM migration without requiring physical access to the target host. Moreover, we reverse-engineered the Versioned Chip Endorsement Key (VCEK) mechanism introduced with SEV Secure Nested Paging (SEV-SNP). The VCEK binds the endorsement keys to the firmware version of TCB components relevant for SEV. Building on the ability to extract the endorsement keys, we show how to derive valid VCEKs for arbitrary firmware versions. With our findings, we prove that SEV cannot adequately protect confidential data in cloud environments from insider attackers, such as rogue administrators, on currently available CPUs.
