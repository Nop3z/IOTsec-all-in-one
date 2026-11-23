---
title: "Thunderstrike：MacBook EFI 固件 bootkit 与 Thunderbolt 攻击面"
source: "Trammell Hudson"
url: https://trmm.net/Thunderstrike/
published: 2014-12-29
fetched: 2026-11-23T05:25:20.401Z
category: "安全启动"
score: 0
keywords: ["classic"]
sha256: 777f39a3d59293d8a43aeeabb774fed03c237c4a939733e696f874fff62cc51b
bytes: 1263
truncated: false
body_mode: notes
kind: practical
status: published
published_at: 2026-11-23T13:25:28.351751+08:00
---

# Thunderstrike：MacBook EFI 固件 bootkit 与 Thunderbolt 攻击面

> 来源：Trammell Hudson · 2014-12-29 · [原文](https://trmm.net/Thunderstrike/)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：攻击点在上电到操作系统之间：Option ROM 由固件直接加载执行，而当时几乎没有任何完整性校验；随后可进一步刷写 EFI/SPI。
- **价值**：Apple 平台启动链攻击的开山之作，直接促成了后来的 BootROM/EFI 加固；读它与后续 Checkra1n/SecureROM 系列能看清启动链对抗的演进。
- **难度**：极高 —— 需要硬件改写（Thunderbolt 设备)、EFI 编程与固件刷写。

用 Thunderbolt 扩展设备的 Option ROM 在 macOS 启动前执行任意 EFI 代码，并可写入 MacBook 的固件（含 SPI Flash），实现持久化的 EFI bootkit——最初的 Thunderstrike 攻击。
