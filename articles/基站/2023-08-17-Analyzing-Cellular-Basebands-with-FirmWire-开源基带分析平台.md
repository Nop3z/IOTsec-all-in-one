---
title: "Analyzing Cellular Basebands with FirmWire：开源基带分析平台"
source: "camp2023"
url: https://media.ccc.de/v/camp2023-57330-analyzing_cellular_basebands_with_firmwire
published: 2023-08-17
fetched: 2026-11-19T05:40:43.175Z
category: "基站"
score: 0
keywords: []
sha256: 7fc93dddc1cc35c7fb53baf46b5ec06f0beeb8cef519dcb596bf87d7f6d85d41
bytes: 705
truncated: false
body_mode: notes
status: published
published_at: 2026-11-19T13:40:51.833712+08:00
---

# Analyzing Cellular Basebands with FirmWire：开源基带分析平台

> 来源：camp2023 · 2023-08-17 · [原文](https://media.ccc.de/v/camp2023-57330-analyzing_cellular_basebands_with_firmwire)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：把基带固件放到仿真环境里跑，才能对 OTA 协议处理做规模化测试。
- **价值**：目前最好上手的基带 fuzz 工具，显著降低该方向的研究门槛。
- **难度**：中 —— 会 Python 与基本逆向即可起步。

FirmWire 是开源基带分析平台：加载厂商基带固件、模拟任务调度、对协议栈做动态分析与 fuzz；演讲给出上手实操。
