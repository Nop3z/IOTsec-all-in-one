---
title: "Systematic Security Analysis of the Iridium Satellite Radio Link"
source: "arXiv"
url: http://arxiv.org/abs/2603.12062v1
published: 2026-03-12
fetched: 2026-11-19T12:07:27.218470+08:00
category: "卫星安全"
score: 0
keywords: ["iridium", "radio"]
sha256: dbf12d72caaa660b61c72abbe2ac7b72e12f201a95f2b563515c45589ccbd3b3
bytes: 1524
truncated: false
body_mode: meta
status: published
published_at: 2026-11-19T12:20:43.910308+08:00
---

# Systematic Security Analysis of the Iridium Satellite Radio Link

> 来源：arXiv · 2026-03-12 · [原文](http://arxiv.org/abs/2603.12062v1)
> 归档用于安全研究参考；版权归原作者所有。

> ⚠️ 本条为「元数据 + 摘要」归档（论文/PDF/前端渲染页面），完整内容请读原文。

## 收录理由

- **核心**：对 Iridium 卫星链路做系统性安全分析：协议私有、缺少公开审查，作者逆向并验证了链路层安全问题。
- **价值**：Iridium 服务 250 万+ 用户，覆盖政府/航空/海事；对私有卫星协议做公开安全分析非常罕见。
- **难度**：极高 —— 需要 SDR、私有协议逆向与链路层实验。

The Iridium Low Earth Orbit (LEO) satellite constellation remains a unique provider of global communications for critical industries, governments, and private users, serving over 2.5 million active subscribers despite recent market competition. In contrast to terrestrial wireless standards such as 3GPP, Iridium protocol specifications are proprietary and have not undergone rigorous, public, and systematic security evaluation. In this work, we present the first comprehensive security analysis of Iridium authentication and radio link protocols. We reverse engineer Iridium SIM-based authentication mechanism and demonstrate that the secret key can be extracted from the SIM card, enabling full device cloning and impersonation attacks. Leveraging a month-long dataset of Iridium up- and downlink satellite traffic, we further show that nearly all signaling and radio communication protocols currently in use lack encryption, resulting in the exposure of sensitive information in cleartext over the air such as login credentials and large volumes of personal data. Finally, we develop custom software-defined radio (SDR) tools to carry out spoofing and jamming attacks, revealing that modestly equipped adversaries can inject falsified messages or disrupt the Iridium service locally due to the absence of source authentication. Our findings uncover systemic vulnerabilities in the Iridium radio link and highlight the urgent need for users of critical applications to transition to more secure communication radio links.
