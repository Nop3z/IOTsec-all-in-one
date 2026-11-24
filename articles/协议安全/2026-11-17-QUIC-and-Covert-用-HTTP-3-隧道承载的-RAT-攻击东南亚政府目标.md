---
title: "QUIC and Covert：用 HTTP/3 隧道承载的 RAT 攻击东南亚政府目标"
source: "Unit 42"
url: https://unit42.paloaltonetworks.com/category/high-profile-threats/
published: 2026-11-17
fetched: 2026-11-24T02:16:14.965Z
category: "协议安全"
score: 0
keywords: []
sha256: cf72b443ef9a5babfe8b9af122e63348475e10b62e6fad72ca7aecb359d69c7f
bytes: 821
truncated: false
body_mode: notes
kind: practical
status: published
published_at: 2026-11-24T10:16:18.753705+08:00
---

# QUIC and Covert：用 HTTP/3 隧道承载的 RAT 攻击东南亚政府目标

> 来源：Unit 42 · 2026-11-17 · [Unit 42 高危威胁栏目](https://unit42.paloaltonetworks.com/category/high-profile-threats/)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：攻击者把 RAT 的 C2 塞进 HTTP/3（QUIC）流量里，利用 UDP 与加密特性绕过传统基于 TCP/HTTP 的检测。
- **价值**：QUIC 正快速进入设备固件（IoT 网关、摄像头云端连接），而多数设备侧检测只解析 TCP；这是固件网络栈层面的现实威胁样本。
- **难度**：中高 —— 需要 QUIC 协议与流量分析基础。

针对东南亚政府目标的攻击活动：RAT 的 C2 走 HTTP/3（QUIC）隧道，利用 UDP + 加密流量规避传统检测，对只解析 TCP 的设备与网关形成盲区。
