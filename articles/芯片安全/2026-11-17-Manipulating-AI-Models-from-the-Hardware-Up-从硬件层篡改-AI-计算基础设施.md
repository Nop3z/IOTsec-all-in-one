---
title: "Manipulating AI Models from the Hardware Up：从硬件层篡改 AI 计算基础设施"
source: "Eclypsium"
url: https://eclypsium.com/events/manipulating-ai-models-from-the-hardware-up/
published: 2026-11-17
fetched: 2026-11-24T02:16:14.963Z
category: "芯片安全"
score: 0
keywords: []
sha256: 8d0a785534d42faf3b3171a965259a5af3548e8eda2c0680b75dccf9532ddb25
bytes: 893
truncated: false
body_mode: notes
kind: practical
status: published
published_at: 2026-11-24T10:16:18.753705+08:00
---

# Manipulating AI Models from the Hardware Up：从硬件层篡改 AI 计算基础设施

> 来源：Eclypsium · 2026-11-17 · [原文](https://eclypsium.com/events/manipulating-ai-models-from-the-hardware-up/)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：研究者展示一条从硬件层入手、篡改 AI 模型而不留下可见 IOC 的攻击链——把攻击点放在“模型之下”。
- **价值**：AI 基础设施正被大量部署到边缘（推理盒子、带 NPU 的摄像头与网关），而硬件/固件层的可信度几乎没人审计；这是该方向少见的公开链条。
- **难度**：高 —— 需要硬件/固件层访问与对推理栈的理解。

对 AI 计算基础设施的硬件层攻击链研究：攻击者在操作系统与模型层之下动手，使模型被篡改但常规检测看不到任何 IOC。
