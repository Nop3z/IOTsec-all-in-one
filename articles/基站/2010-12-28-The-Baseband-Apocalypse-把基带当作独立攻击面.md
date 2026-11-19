---
title: "The Baseband Apocalypse：把基带当作独立攻击面"
source: "27C3"
url: https://media.ccc.de/v/27c3-4090-en-baseband_apocalypse
published: 2010-12-28
fetched: 2026-11-19T05:40:43.175Z
category: "基站"
score: 0
keywords: []
sha256: 3609e323b625498b13e3adcfa77a67bac529a0e751a6fbe1145f64aa1bb6ee35
bytes: 828
truncated: false
body_mode: notes
status: published
published_at: 2026-11-19T13:40:51.833712+08:00
---

# The Baseband Apocalypse：把基带当作独立攻击面

> 来源：27C3 · 2010-12-28 · [原文](https://media.ccc.de/v/27c3-4090-en-baseband_apocalypse)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：基带是独立于 AP 的第二个处理器 + 专有 RTOS + 完整协议栈，攻击面包括 OTA 协议解析、SIM/AT 接口与固件更新。
- **价值**：基带安全研究的起点之一，确立了“手机里有两个可被远程攻击的操作系统”这一认知。
- **难度**：中高 —— 需要对蜂窝协议栈与嵌入式固件有整体理解。

应用处理器的 OS 正在被厂商加固（DEP、代码签名），但跑在独立基带上的 GSM 协议栈长期缺乏同等保护；演讲从系统角度给出基带的攻击场景与研究方法。
