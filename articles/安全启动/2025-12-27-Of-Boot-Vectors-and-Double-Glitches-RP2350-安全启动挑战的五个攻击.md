---
title: "Of Boot Vectors and Double Glitches：RP2350 安全启动挑战的五个攻击"
source: "39C3"
url: https://media.ccc.de/v/39c3-of-boot-vectors-and-double-glitches-bypassing-rp2350-s-secure-boot
published: 2025-12-27
fetched: 2026-11-26T02:10:22.336Z
category: "安全启动"
score: 0
keywords: []
sha256: d83c5a1a272afe450f47c8489e1b0de4af59bf80b142558590c0886cf8aed6cc
bytes: 648
truncated: false
body_mode: notes
kind: practical
status: published
published_at: 2026-11-26T10:10:22.744554+08:00
---

# Of Boot Vectors and Double Glitches：RP2350 安全启动挑战的五个攻击

> 来源：39C3 · 2025-12-27 · [原文](https://media.ccc.de/v/39c3-of-boot-vectors-and-double-glitches-bypassing-rp2350-s-secure-boot)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：官方挑战的“五个攻击”合集：涵盖启动向量滥用与双毛刺等手法，构成对同一颗芯片安全模型的完整压力测试。
- **价值**：少见的“厂商悬赏 → 多方独立破解 → 公开复盘”闭环，是评估 MCU 安全启动设计缺陷的最佳教材。
- **难度**：极高 —— 涉及物理毛刺与启动链深层机制。

Raspberry Pi 在 2024 年发布 RP2350 并公开悬赏破解其安全启动；挑战于 2025 年 1 月结束，共产生五个由不同研究者发现的攻击。演讲深入 RP2350 的安全架构，逐一讲解这些攻击的技术细节。
