---
title: "Smart vacuum cleaners as remote wiretapping devices：QNX 扫地机的窃听"
source: "eh19"
url: https://media.ccc.de/v/eh19-157-smart-vacuum-cleaners-as-remote-wiretapping-devices
published: 2019-04-21
fetched: 2026-11-19T05:40:43.175Z
category: "机器人"
score: 0
keywords: []
sha256: 8220368fd1a4bac04c20af35b97a4aa58dcb5dc7644fc606f04f96dbf8fcc6b7
bytes: 753
truncated: false
body_mode: notes
kind: practical
status: published
published_at: 2026-11-19T13:40:51.833712+08:00
---

# Smart vacuum cleaners as remote wiretapping devices：QNX 扫地机的窃听

> 来源：eh19 · 2019-04-21 · [原文](https://media.ccc.de/v/eh19-157-smart-vacuum-cleaners-as-remote-wiretapping-devices)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：云连接 + 传感器 = 物理世界的隐私采集器；固件漏洞让攻击者越过厂商云直接控制设备。
- **价值**：把“IoT 隐私风险”从抽象担忧变成可复现的技术链路。
- **难度**：中高 —— 需要固件分析与云端接口逆向。

对 Neato Botvac Connected 做固件级利用：设备跑 QNX、带激光扫描与麦克风，攻击者可控制其传感器把扫地机变成远程窃听/建图设备。
