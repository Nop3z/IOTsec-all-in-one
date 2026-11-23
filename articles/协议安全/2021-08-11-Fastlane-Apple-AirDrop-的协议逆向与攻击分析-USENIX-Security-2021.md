---
title: "Fastlane：Apple AirDrop 的协议逆向与攻击分析（USENIX Security 2021）"
source: "USENIX Security 2021"
url: https://www.usenix.org/conference/usenixsecurity21/presentation/stute
published: 2021-08-11
fetched: 2026-11-23T05:25:20.401Z
category: "协议安全"
score: 0
keywords: ["classic"]
sha256: 94b48b52664f2717c75d2002d5173b64c5560decce1c426f597bd1b5c9939974
bytes: 1362
truncated: false
body_mode: notes
kind: practical
status: published
published_at: 2026-11-23T13:25:28.351751+08:00
---

# Fastlane：Apple AirDrop 的协议逆向与攻击分析（USENIX Security 2021）

> 来源：USENIX Security 2021 · 2021-08-11 · [原文](https://www.usenix.org/conference/usenixsecurity21/presentation/stute)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：AirDrop 用私有 AWDL + 私有无线协议，文中给出了**从空口抓包到完整协议重建**的方法，并指出依赖“接触即信任”的认证模型缺陷。
- **价值**：近场私有协议逆向的完整范例；对蓝牙/Wi-Fi 组合类设备（IoT 配网、隔空投送、近场支付）的安全评估很有借鉴意义。
- **难度**：高 —— 需要 AWDL 专用抓包、私有协议逆向与密码学分析能力。

首个对 Apple AirDrop 协议的系统性逆向与安全分析：作者逆向私有发现协议与传输流程，发现可被利用的认证/隐私问题，并给出改进建议与开源替代方案。
