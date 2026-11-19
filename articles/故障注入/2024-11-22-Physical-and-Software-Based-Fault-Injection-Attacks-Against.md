---
title: "Physical and Software Based Fault Injection Attacks Against TEEs in Mobile Devices: A Systemisation of Knowledge"
source: "arXiv"
url: http://arxiv.org/abs/2411.14878v1
published: 2024-11-22
fetched: 2026-11-19T12:07:27.218470+08:00
category: "故障注入"
score: 0
keywords: ["fault-injection", "tee"]
sha256: 8de567768d5c1f6cb1796ae1ad9be92d66d50f7e5bd17e3c8b13a7e6e33cd8d2
bytes: 1681
truncated: false
body_mode: meta
kind: theory
status: published
published_at: 2026-11-19T12:20:43.910308+08:00
---

# Physical and Software Based Fault Injection Attacks Against TEEs in Mobile Devices: A Systemisation of Knowledge

> 来源：arXiv · 2024-11-22 · [原文](http://arxiv.org/abs/2411.14878v1)
> 归档用于安全研究参考；版权归原作者所有。

> ⚠️ 本条为「元数据 + 摘要」归档（论文/PDF/前端渲染页面），完整内容请读原文。

## 收录理由

- **核心**：系统化梳理移动设备 TEE（可信执行环境）面临的物理与软件故障注入攻击（EMFI 等）。
- **价值**：TEE 是手机支付/生物识别的信任根；这份 SoK 把攻击面、案例与方法论集中到一处，适合当索引读。
- **难度**：中 —— 综述性质，但覆盖了 EMFI 的实际参数与实验条件。

Trusted Execution Environments (TEEs) are critical components of modern secure computing, providing isolated zones in processors to safeguard sensitive data and execute secure operations. Despite their importance, TEEs are increasingly vulnerable to fault injection (FI) attacks, including both physical methods, such as Electromagnetic Fault Injection (EMFI), and software-based techniques. This survey examines these FI methodologies, exploring their ability to disrupt TEE operations and expose vulnerabilities in devices ranging from smartphones and IoT systems to cloud platforms. The study highlights the evolution and effectiveness of non-invasive techniques, such as EMFI, which induce faults through electromagnetic disturbances without physical modifications to hardware, making them harder to detect and mitigate. Real-world case studies illustrate the significant risks posed by these attacks, including unauthorised access, privilege escalation, and data corruption. In addition, the survey identifies gaps in existing TEE security architectures and emphasises the need for enhanced countermeasures, such as dynamic anomaly detection and updated threat models. The findings underline the importance of interdisciplinary collaboration to address these vulnerabilities, involving researchers, manufacturers, and policymakers. This survey provides actionable insights and recommendations to guide the development of more robust TEE architectures in mobile devices, fortify FI resilience, and shape global security standards. By advancing TEE security, this research aims to protect critical digital infrastructure and maintain trust in secure computing systems worldwide.
