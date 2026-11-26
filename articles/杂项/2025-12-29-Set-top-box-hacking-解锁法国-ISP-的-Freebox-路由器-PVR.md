---
title: "Set-top box hacking：解锁法国 ISP 的 Freebox（路由器 + PVR）"
source: "39C3"
url: https://media.ccc.de/v/39c3-set-top-box-hacking-freeing-the-freebox
published: 2025-12-29
fetched: 2026-11-26T02:10:22.336Z
category: "杂项"
score: 0
keywords: []
sha256: b87d59b710df71de29976d951d2fd4b77ad06c3fea21aa1b96e575a7cdef502f
bytes: 633
truncated: false
body_mode: notes
kind: practical
status: published
published_at: 2026-11-26T10:10:22.744554+08:00
---

# Set-top box hacking：解锁法国 ISP 的 Freebox（路由器 + PVR）

> 来源：39C3 · 2025-12-29 · [原文](https://media.ccc.de/v/39c3-set-top-box-hacking-freeing-the-freebox)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：运营商定制设备（机顶盒、光猫、路由）长期跑旧内核 + 厂商私有更新通道，启动链与固件校验是主要突破口。
- **价值**：全球有海量运营商定制 CPE 设备，这类“被遗忘的 Linux 盒子”在野暴露面极大；思路与光猫/路由器破解通用。
- **难度**：高 —— 需要固件提取、启动链分析与刷机恢复手段。

Freebox HD 是法国 ISP Free 的机顶盒/录像机，与配套路由器都跑 Linux；演讲分析其启动流程、固件与更新机制，展示如何在这类运营商定制设备上取得控制权。
