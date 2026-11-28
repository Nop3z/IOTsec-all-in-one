---
title: "Hacking yourself a satellite：抢救一颗失效的 BEESAT-1"
source: "38C3"
url: https://media.ccc.de/v/38c3-hacking-yourself-a-satellite-recovering-beesat-1
published: 2024-12-28
fetched: 2026-11-28T02:02:29.911Z
category: "卫星安全"
score: 0
keywords: []
sha256: b15ff01e29d226ce3d2187d21e895840ad8a44d6d3d59d6fe538b291d5b5b272
bytes: 715
truncated: false
body_mode: notes
kind: practical
status: published
published_at: 2026-11-28T10:02:30.318728+08:00
---

# Hacking yourself a satellite：抢救一颗失效的 BEESAT-1

> 来源：38C3 · 2024-12-28 · [原文](https://media.ccc.de/v/38c3-hacking-yourself-a-satellite-recovering-beesat-1)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：没有遥测、没有 OTA 的卫星怎么救：从地面站侧推断状态、寻找指令注入路径，最终把新固件送上去。
- **价值**：少见的“在轨系统恢复”实录，等价于对一个无调试接口、无法物理接触的嵌入式设备做盲改固件——对理解航天器更新链与失效模式极有价值。
- **难度**：极高 —— 需要轨道/通信知识与在无法开机的设备上做远程调试。

BEESAT-1 自 2013 年起返回无效遥测、实际不可用，且还将留在轨道上二十年以上；它既没有可用遥测，也没有固件更新能力。团队设法恢复卫星并更新飞行软件，让老硬件跑新实验。
