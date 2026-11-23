---
title: "FragAttacks：Wi-Fi 帧聚合与分片引起的 12 个新漏洞"
source: "Mathy Vanhoef"
url: https://www.fragattacks.com/
published: 2021-05-11
fetched: 2026-11-23T05:25:20.401Z
category: "WIFI安全"
score: 0
keywords: ["classic"]
sha256: 221a06098ef5e375de840324d96e2dea67288c8a5ca22b09c7be43cc7fc01650
bytes: 1295
truncated: false
body_mode: notes
kind: practical
status: published
published_at: 2026-11-23T13:25:28.351751+08:00
---

# FragAttacks：Wi-Fi 帧聚合与分片引起的 12 个新漏洞

> 来源：Mathy Vanhoef · 2021-05-11 · [原文](https://www.fragattacks.com/)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：攻击面是标准里模糊的“分片重组”与“A-MSDU 聚合”规则：实现者对同一帧的语义理解不一致，就产生了可注入的“幽灵包”。
- **价值**：与 KRACK 互补：一个打握手，一个打数据帧；两者都证明**协议规范的含糊处**是最肥沃的漏洞来源（且这些缺陷二十多年没人系统审视）。
- **难度**：中 —— 同样需要近场无线能力，但工具（如自写的 Scapy/fragattacks 脚本）通用性很强。

在 Wi-Fi 帧的**分片与聚合**语义上找到 12 个漏洞（3 个设计缺陷、9 个实现问题），可导致数据包注入、截获与安全机制降级，几乎影响 1997 年以来所有 Wi-Fi 设备。
