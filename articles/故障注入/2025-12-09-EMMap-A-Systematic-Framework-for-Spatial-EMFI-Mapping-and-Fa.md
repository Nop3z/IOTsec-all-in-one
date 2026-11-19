---
title: "EMMap: A Systematic Framework for Spatial EMFI Mapping and Fault Classification on Microcontrollers"
source: "arXiv"
url: http://arxiv.org/abs/2512.09049v1
published: 2025-12-09
fetched: 2026-11-19T12:07:27.218470+08:00
category: "故障注入"
score: 0
keywords: ["emfi", "mapping"]
sha256: 5a89a7f0e52b0bac36d74f5784f1e3c32812e4e69a8c0450a7c1ec62fd6df574
bytes: 955
truncated: false
body_mode: meta
status: published
published_at: 2026-11-19T12:20:43.910308+08:00
---

# EMMap: A Systematic Framework for Spatial EMFI Mapping and Fault Classification on Microcontrollers

> 来源：arXiv · 2025-12-09 · [原文](http://arxiv.org/abs/2512.09049v1)
> 归档用于安全研究参考；版权归原作者所有。

> ⚠️ 本条为「元数据 + 摘要」归档（论文/PDF/前端渲染页面），完整内容请读原文。

## 收录理由

- **核心**：提出平台无关的 EMFI 空间敏感度测绘与故障分类框架（EMMap），用于系统化定位芯片上的毛刺敏感点。
- **价值**：把“靠运气找毛刺点”变成可重复的测绘流程，对做 MCU/IoT 芯片评估很实用。
- **难度**：中高 —— 需要搭建 XY 位移平台与自动化采集。

Electromagnetic Fault Injection (EMFI) is a powerful technique for inducing bit flips and instruction-level perturbations on microcontrollers, yet existing literature lacks a unified methodology for systematically mapping spatial sensitivity and classifying resulting fault behaviors. Building on insights from O'Flynn and Kuhnapfel et al., we introduce a platform-agnostic framework for Spatial EMFI Mapping and Fault Classification, aimed at understanding how spatial probe position influences fault outcomes. We present pilot experiments on three representative microcontroller targets including the Xtensa LX6 (ESP32) and two ChipWhisper boards not as definitive evaluations, but as illustrative demonstrations of how the proposed methodology can be applied in practice. These preliminary observations motivate a generalized and reproducible workflow that researchers can adopt when analyzing EMFI susceptibility across diverse embedded architectures.
