---
title: "Don't look up：地球同步卫星上大量敏感链路是明文的"
source: "39C3"
url: https://media.ccc.de/v/39c3-don-t-look-up-there-are-sensitive-internal-links-in-the-clear-on-geo-satellites
published: 2025-12-28
fetched: 2026-11-26T02:10:22.336Z
category: "卫星安全"
score: 0
keywords: []
sha256: 88ca1ad76d1037b33c20dbbdea02befa65643a989af857b69b46e5cf8e489a62
bytes: 703
truncated: false
body_mode: notes
kind: practical
status: published
published_at: 2026-11-26T10:10:22.744554+08:00
---

# Don't look up：地球同步卫星上大量敏感链路是明文的

> 来源：39C3 · 2025-12-28 · [原文](https://media.ccc.de/v/39c3-don-t-look-up-there-are-sensitive-internal-links-in-the-clear-on-geo-satellites)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：攻击面＝卫星链路的物理广播特性 + 运营商未加密：不需要入侵，只要能收就能听，门槛低到一台碟形天线。
- **价值**：卫星安全长期缺乏实测数据，这是少见的“大规模被动监听”实证，直接说明 SATCOM 链路加密缺位的现实风险。
- **难度**：中高 —— 需要卫星接收设备与信号分析能力，但不需要发射/入侵。

研究团队用一台商用卫星天线对准天空，扫描可见的 GEO 卫星通信，发现大量敏感流量以明文广播：关键基础设施、企业与政府内部通信、私人通话与短信，以及机上 Wi-Fi 与移动回传的用户流量。
