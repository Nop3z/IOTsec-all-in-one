---
title: "Firmware Fat Camp：给固件“减肥”，删掉多余组件缩小攻击面"
source: "30C3"
url: https://media.ccc.de/v/30C3_-_5356_-_en_-_saal_6_-_201312272300_-_firmware_fat_camp_-_angcui
published: 2013-12-27
fetched: 2026-11-27T02:01:28.690Z
category: "固件解密"
score: 0
keywords: []
sha256: 557817a496caa44e7b14add0e1427512bae76a255783f778efb5962d06a1eb4b
bytes: 578
truncated: false
body_mode: notes
kind: practical
status: published
published_at: 2026-11-27T10:01:29.126372+08:00
---

# Firmware Fat Camp：给固件“减肥”，删掉多余组件缩小攻击面

> 来源：30C3 · 2013-12-27 · [原文](https://media.ccc.de/v/30C3_-_5356_-_en_-_saal_6_-_201312272300_-_firmware_fat_camp_-_angcui)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：固件的攻击面大多来自“用不到但一直在跑”的组件；能安全裁剪，就等于从根上减少可被攻击的代码。
- **价值**：少见地从防御/工程角度处理固件攻击面，对做设备加固与固件重制的团队很实用。
- **难度**：高 —— 需要固件依赖分析与裁剪后的可用性验证。

一组自动化技术：从常见嵌入式设备的固件二进制里安全地移除大量不必要的部分，从而大幅缩小设备的攻击面，并现场演示了在真实设备上的效果。
