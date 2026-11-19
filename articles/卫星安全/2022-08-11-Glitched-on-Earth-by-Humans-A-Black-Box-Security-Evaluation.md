---
title: "Glitched on Earth by Humans: A Black-Box Security Evaluation of the SpaceX Starlink User Terminal"
source: "Black Hat USA 2022"
url: https://i.blackhat.com/USA-22/Wednesday/US-22-Wouters-Glitched-On-Earth.pdf
published: 2022-08-11
fetched: 2026-11-19T12:07:27.218470+08:00
category: "卫星安全"
score: 0
keywords: ["starlink", "fault-injection", "satcom"]
sha256: 41ac0e33a33622d7137e02131048d0850376f65e67a7680fe0ae7ba64e3453ba
bytes: 239
truncated: false
body_mode: meta
status: published
published_at: 2026-11-19T12:20:43.910308+08:00
---

# Glitched on Earth by Humans: A Black-Box Security Evaluation of the SpaceX Starlink User Terminal

> 来源：Black Hat USA 2022 · 2022-08-11 · [原文](https://i.blackhat.com/USA-22/Wednesday/US-22-Wouters-Glitched-On-Earth.pdf)
> 归档用于安全研究参考；版权归原作者所有。

> ⚠️ 本条为「元数据 + 摘要」归档（论文/PDF/前端渲染页面），完整内容请读原文。

## 收录理由

- **核心**：对 Starlink 用户终端（Dishy）做黑盒评估：用电压毛刺让安全启动校验出错，从而在终端上运行自定义代码，并进一步分析终端的启动链与固件保护。
- **价值**：卫星互联网终端的公开攻击案例极少，这是最经典的一篇；它把“消费级 SATCOM 设备”从“黑盒终端”变成可研究的硬件目标。
- **难度**：极高 —— 需要拆机、定位毛刺点、反复试验时序，属于硬件+固件的复合工作。

KU Leuven (COSIC) 对 SpaceX Starlink 用户终端做黑盒安全评估：通过电压故障注入绕过安全启动，从而在终端上执行自定义代码。该工作首次公开证明消费级卫星互联网终端可被物理攻破。
