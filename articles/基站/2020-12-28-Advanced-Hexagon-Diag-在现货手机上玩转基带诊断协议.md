---
title: "Advanced Hexagon Diag：在现货手机上玩转基带诊断协议"
source: "rC3 2020"
url: https://media.ccc.de/v/rc3-11397-advanced_hexagon_diag
published: 2020-12-28
fetched: 2026-11-19T05:40:43.175Z
category: "基站"
score: 0
keywords: []
sha256: 86be79ce9caca96f4cb0bd9bbf48a9d7e4e91f2d4aa929e1092c6948f9053377
bytes: 733
truncated: false
body_mode: notes
kind: practical
status: published
published_at: 2026-11-19T13:40:51.833712+08:00
---

# Advanced Hexagon Diag：在现货手机上玩转基带诊断协议

> 来源：rC3 2020 · 2020-12-28 · [原文](https://media.ccc.de/v/rc3-11397-advanced_hexagon_diag)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：DIAG 是基带里的“调试后门”协议：拿到它就能读基带日志、注入命令，是研究基带行为的实用入口。
- **价值**：把“基带黑盒”变成可观测对象，成本远低于做完整固件提取。
- **难度**：高 —— 需要理解 Qualcomm 私有协议与手机侧配置。

对 Qualcomm DIAG 诊断协议的研究现状、在 Hexagon 基带中的现代实现、以及如何在市售手机上获取日志与控制通道。
