---
title: "Pwn My Ride：用一个 AirPlay SDK 漏洞越狱 CarPlay 车机"
source: "GOD 2025"
url: https://media.ccc.de/v/god2025-56485-pwn-my-ride-jailbreaking-c
published: 2025-11-26
fetched: 2026-11-28T02:02:29.911Z
category: "车机"
score: 0
keywords: []
sha256: 2af4c82ecc67928a835f0b20e3204307c0a216c80b0dcf9709b8c891e76edb6a
bytes: 633
truncated: false
body_mode: notes
kind: practical
status: published
published_at: 2026-11-28T10:02:30.318728+08:00
---

# Pwn My Ride：用一个 AirPlay SDK 漏洞越狱 CarPlay 车机

> 来源：GOD 2025 · 2025-11-26 · [原文](https://media.ccc.de/v/god2025-56485-pwn-my-ride-jailbreaking-c)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：攻击面是手机与车机之间的投屏协议栈：一个 SDK 级漏洞即可横向覆盖大量车型，属于典型的“协议复用型供应链风险”。
- **价值**：车机安全最现实的一类入口——不需要碰 CAN 总线，从手机投屏通道进入即可；影响面按车型数量级放大。
- **难度**：高 —— 需要 AirPlay/CarPlay 协议逆向与利用开发。

CarPlay 基于 AirPlay，被数十家车厂、上百款车型采用。研究团队在 AirPlay SDK 中发现一个漏洞，用它攻破了所有运行 CarPlay 的设备，实现车机侧的代码执行。
