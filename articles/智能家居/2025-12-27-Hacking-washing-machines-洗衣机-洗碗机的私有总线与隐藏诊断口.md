---
title: "Hacking washing machines：洗衣机/洗碗机的私有总线与隐藏诊断口"
source: "39C3"
url: https://media.ccc.de/v/39c3-hacking-washing-machines
published: 2025-12-27
fetched: 2026-11-26T02:10:22.336Z
category: "智能家居"
score: 0
keywords: []
sha256: 8d8daa8d3b6643f2d6f72008f594e044b1f71ed48c06d08035a38fd2b655bfe6
bytes: 692
truncated: false
body_mode: notes
kind: practical
status: published
published_at: 2026-11-26T10:10:22.744554+08:00
---

# Hacking washing machines：洗衣机/洗碗机的私有总线与隐藏诊断口

> 来源：39C3 · 2025-12-27 · [原文](https://media.ccc.de/v/39c3-hacking-washing-machines)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：攻击面＝家电内部私有总线 + 出厂诊断口：厂商用私有协议连接主控与电机/传感器，诊断口常年保留且无鉴权。
- **价值**：家电是家里数量最多、却最少被安全审计的设备；总线与诊断口的做法在同类产品中高度相似，可横向迁移。
- **难度**：中高 —— 需要拆机、逻辑分析仪抓总线与协议逆向。

两台知名厂商家用电器（洗衣机、洗碗机、烘干机）的内部究竟怎么通信，公开资料几乎为零。演讲深入其私有总线系统、隐藏的诊断接口，并讨论如何在不依赖厂商云的情况下把家电接入自有系统。
