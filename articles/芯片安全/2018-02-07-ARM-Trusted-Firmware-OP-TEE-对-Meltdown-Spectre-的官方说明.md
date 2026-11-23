---
title: "ARM Trusted Firmware / OP-TEE 对 Meltdown/Spectre 的官方说明"
source: "Linaro / Trusted Firmware"
url: https://raw.githubusercontent.com/Linaro/website/2cff169892eed936388e815811c330bef24f6c34/_posts/previous/2018-02-07-meltdown-spectre-2.md
published: 2018-02-07
fetched: 2026-11-23T05:31:26.153Z
category: "芯片安全"
score: 0
keywords: ["rowhammer","spectre"]
sha256: 1c924abaaf53e86c7fabe0ad5d89a0fb0838964e7af73e5abb3cadd895ba38e1
bytes: 456
truncated: false
body_mode: notes
kind: theory
status: published
published_at: 2026-11-23T13:31:32.371156+08:00
---

# ARM Trusted Firmware / OP-TEE 对 Meltdown/Spectre 的官方说明

> 来源：Linaro / Trusted Firmware · 2018-02-07 · [原文](https://raw.githubusercontent.com/Linaro/website/2cff169892eed936388e815811c330bef24f6c34/_posts/previous/2018-02-07-meltdown-spectre-2.md)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：安全世界与普通世界共享微架构状态，TEE 并非天然免疫，需要显式加屏障。
- **价值**：做 TrustZone/TEE 评估时最实用的参考：告诉你加固加在哪一层。
- **难度**：中 —— 需 ATF/OP-TEE 基础。

Linaro 团队说明 ATF/OP-TEE 生态对 Meltdown/Spectre 的评估：哪些场景受影响、TEE 侧需要哪些加固（如对共享数据访问加 speculation barrier）。
