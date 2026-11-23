---
title: "Remote Attack to Tesla Model S：从 Wi-Fi 到 CAN 总线的远程控制（KeenLab 2016）"
source: "Tencent KeenLab"
url: https://keenlab.tencent.com/en/2016/09/19/Keen-Security-Lab-of-Tencent-Car-Hacking-Research-Remote-Attack-to-Tesla-Cars/
published: 2016-09-19
fetched: 2026-11-23T05:25:20.401Z
category: "车机"
score: 0
keywords: ["classic"]
sha256: 4e7c691b9f001c269ca6b26be79a48f46791b904450fa9c7094cef32a09c50e6
bytes: 1532
truncated: false
body_mode: notes
kind: practical
status: published
published_at: 2026-11-23T13:25:28.351751+08:00
---

# Remote Attack to Tesla Model S：从 Wi-Fi 到 CAN 总线的远程控制（KeenLab 2016）

> 来源：Tencent KeenLab · 2016-09-19 · [原文](https://keenlab.tencent.com/en/2016/09/19/Keen-Security-Lab-of-Tencent-Car-Hacking-Research-Remote-Attack-to-Tesla-Cars/)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：攻击链清晰展示“远程入口（浏览器/Wi-Fi）→ 车机 Linux → 以太网网关 → CAN”，难点集中在**跨域网关穿越**与车辆状态约束下的稳定控制。
- **价值**：车联网安全的里程碑：第一次把“远程、无接触、可影响行驶”的完整链条公之于众，也直接推动了整车厂的网关隔离设计。
- **难度**：极高 —— 需要整车/台架、车机固件逆向与 CAN 协议知识。

科恩实验室通过中控娱乐系统上的浏览器入口远程攻入 Tesla Model S：选装 Wi-Fi 上网后，利用漏洞拿到车机代码执行，再横向穿过网关控制 CAN 总线，实现行驶中刹车、车门与中控的远程操控。
