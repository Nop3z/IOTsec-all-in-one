---
title: "SpyChain: Multi-Vector Supply Chain Attacks on Small Satellite Systems"
source: "arXiv"
url: http://arxiv.org/abs/2510.06535v2
published: 2025-10-08
fetched: 2026-11-19T12:07:27.218470+08:00
category: "卫星安全"
score: 0
keywords: ["satellite", "supply-chain"]
sha256: 2bb4c4f1b95257c419ade0fa5927312a78436a8344fe2d960536a0eb4adc8177
bytes: 1696
truncated: false
body_mode: meta
status: published
published_at: 2026-11-19T12:20:43.910308+08:00
---

# SpyChain: Multi-Vector Supply Chain Attacks on Small Satellite Systems

> 来源：arXiv · 2025-10-08 · [原文](http://arxiv.org/abs/2510.06535v2)
> 归档用于安全研究参考；版权归原作者所有。

> ⚠️ 本条为「元数据 + 摘要」归档（论文/PDF/前端渲染页面），完整内容请读原文。

## 收录理由

- **核心**：SpyChain：针对小型卫星的多向量供应链攻击（COTS 硬件、固件与地面段）。
- **价值**：小卫星大量使用商用现货器件，供应链是它最薄弱的环节；这篇把可行性验证做到了系统级。
- **难度**：高 —— 需要卫星系统知识与多环节植入。

Small satellites are integral to scientific, commercial, and defense missions, but reliance on commercial off-the-shelf (COTS) hardware broadens their attack surface. Although supply chain threats are well studied in other cyber-physical domains, their feasibility and stealth in space systems remain largely unexplored. Prior work has focused on flight software, which benefits from strict security practices and oversight. In contrast, auxiliary COTS components often lack robust assurance yet enjoy comparable access to critical on-board resources, including telemetry, system calls, and the software bus. Despite this privileged access, the insider threat within COTS hardware supply chains has received little attention. In this work, we present SpyChain, the first end-to-end design and implementation of independent and colluding hardware supply chain threats targeting small satellites. Using NASA's satellite simulation (NOS3), we demonstrate that SpyChain can evade testing, exfiltrate telemetry, disrupt operations, and launch Denial of Service (DoS) attacks through covert channels that bypass ground monitoring. Our study traces an escalation from a simple solo component to dynamic, coordinating malware, introducing a taxonomy of stealth across five scenarios. We showcase how implicit trust in auxiliary components enables covert persistence and reveal novel attack vectors, highlighting a new multi-component execution technique that is now incorporated into the SPARTA matrix. Our findings are reinforced by acknowledgment and affirmation from NASA's NOS3 team. Finally, we implement lightweight onboard defenses, including runtime monitoring, to mitigate threats like SpyChain.
