---
title: "Beyond your cable modem：运营商 CPE 背后的数万终端与号码暴露面"
source: "32C3"
url: https://media.ccc.de/v/32c3-7133-beyond_your_cable_modem
published: 2015-12-27
fetched: 2026-11-27T02:01:28.690Z
category: "杂项"
score: 0
keywords: []
sha256: 091531d2f0cfd344f779d3fb6128664310cef42266ed4b1db21101836d8b11e3
bytes: 645
truncated: false
body_mode: notes
kind: practical
status: published
published_at: 2026-11-27T10:01:29.126372+08:00
---

# Beyond your cable modem：运营商 CPE 背后的数万终端与号码暴露面

> 来源：32C3 · 2015-12-27 · [原文](https://media.ccc.de/v/32c3-7133-beyond_your_cable_modem)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：攻击面不在单台设备，而在运营商对海量 CPE 的集中管理接口与默认配置；一处失守就放大成几十万台。
- **价值**：理解“规模化暴露”是评估运营商/ISP 环境的第一步，也解释了为什么 IoT 僵尸网络能一次扫到海量设备。
- **难度**：中高 —— 需要运营商网络视角与大规模扫描能力（演讲偏分析）。

演讲展示如何在运营商网络里触达数十万台终端设备与大量电话号码：从 CPE 管理面、设备默认配置与运营商侧接口一路看过去，是一份“网络安全的反面教材”。
