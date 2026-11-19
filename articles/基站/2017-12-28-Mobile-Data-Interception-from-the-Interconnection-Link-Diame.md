---
title: "Mobile Data Interception from the Interconnection Link：Diameter 也能被滥用"
source: "34C3"
url: https://media.ccc.de/v/34c3-8879-mobile_data_interception_from_the_interconnection_link
published: 2017-12-28
fetched: 2026-11-19T05:40:43.175Z
category: "基站"
score: 0
keywords: []
sha256: 3f082a6712d543f7eb0536c8a0035150bc99606be0b0fda478cab37efbeb60d9
bytes: 797
truncated: false
body_mode: notes
status: published
published_at: 2026-11-19T13:40:51.833712+08:00
---

# Mobile Data Interception from the Interconnection Link：Diameter 也能被滥用

> 来源：34C3 · 2017-12-28 · [原文](https://media.ccc.de/v/34c3-8879-mobile_data_interception_from_the_interconnection_link)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：Diameter 的互联信任模型与 SS7 同源；攻击者可从运营商互联点进入并截取用户面/控制面数据。
- **价值**：直接证伪“上了 4G 就更安全”的假设，对评估运营商网络暴露面很重要。
- **难度**：中高 —— 需要运营商互联环境与协议栈知识。

LTE 的 Diameter 协议被认为是 SS7 的更安全继任者，但演讲展示从互联链路仍可拦截移动数据：信任边界与消息鉴权同样存在问题。
