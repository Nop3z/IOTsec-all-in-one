---
title: "Spectre-BHB：分支历史缓冲区污染（ARM 白皮书）"
source: "ARM"
url: https://developer.arm.com/-/media/Arm%20Developer%20Community/PDF/Security%20Update%2008%20March%202022/Spectre-BHB%20White%20Paper%20v1.6.pdf
published: 2022-03-08
fetched: 2026-11-23T05:31:26.153Z
category: "芯片安全"
score: 0
keywords: ["rowhammer","spectre"]
sha256: f3ce6db0563fab67cad7366689c49d833f8e2aaec388debbe23f770bb24f7cf3
bytes: 548
truncated: false
body_mode: notes
kind: theory
status: published
published_at: 2026-11-23T13:31:32.371156+08:00
---

# Spectre-BHB：分支历史缓冲区污染（ARM 白皮书）

> 来源：ARM · 2022-03-08 · [原文](https://developer.arm.com/-/media/Arm%20Developer%20Community/PDF/Security%20Update%2008%20March%202022/Spectre-BHB%20White%20Paper%20v1.6.pdf)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：BHB 是跨特权级共享的微架构状态，不随上下文切换清空，可在用户态/内核态甚至 VM 间传递攻击。
- **价值**：ARM 平台最有代表性的 Spectre 演进；手机、车机、路由器 SoC 评估必读。
- **难度**：中高 —— 需理解分支预测单元与推测窗口。

ARM 官方白皮书：攻击者可跨上下文污染分支历史缓冲区（BHB），使推测执行跳向攻击者选定的 gadget 泄露受害者推测状态；覆盖 Cortex-A 各代与缓解建议。
