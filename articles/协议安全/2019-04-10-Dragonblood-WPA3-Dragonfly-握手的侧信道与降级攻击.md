---
title: "Dragonblood：WPA3 Dragonfly 握手的侧信道与降级攻击"
source: "Mathy Vanhoef / Eyal Ronen"
url: https://wpa3.mathyvanhoef.com/
published: 2019-04-10
fetched: 2026-11-23T05:25:20.401Z
category: "协议安全"
score: 0
keywords: ["classic"]
sha256: 2b38dfd04eb59a119319b90d3b19812d4535a67077d2079f82264fdc5f49d0c8
bytes: 1221
truncated: false
body_mode: notes
kind: practical
status: published
published_at: 2026-11-23T13:25:28.351751+08:00
---

# Dragonblood：WPA3 Dragonfly 握手的侧信道与降级攻击

> 来源：Mathy Vanhoef / Eyal Ronen · 2019-04-10 · [原文](https://wpa3.mathyvanhoef.com/)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：WPA3 为防离线爆破而设计的 SAE 握手，反而因为**时间与内存访问的可观测差异**泄露口令信息——安全设计引入了新的侧信道。
- **价值**：极好的“安全改进本身引入新攻击面”案例，对评估任何“抗离线暴力”协议（PAKE）都有直接参考价值。
- **难度**：中高 —— 需要精确的计时/缓存测量与 802.11 接入能力。

WPA3-SAE 的 Dragonfly 握手存在多个问题：基于计时与缓存的分区预言机可让攻击者验证字典中的口令、进而离线暴力；另有降级攻击可将设备拉回 WPA2。
