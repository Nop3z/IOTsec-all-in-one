---
title: "Hoermann BiSecur：AES-128 双向无线门控被攻破"
source: "34C3"
url: https://media.ccc.de/v/34c3-9029-uncovering_vulnerabilities_in_hoermann_bisecur
published: 2017-12-28
fetched: 2026-11-28T02:02:29.911Z
category: "协议安全"
score: 0
keywords: []
sha256: 1a06d898848f70be4f9a4199779153676b1d8295a99e45457854af0797342826
bytes: 632
truncated: false
body_mode: notes
kind: practical
status: published
published_at: 2026-11-28T10:02:30.318728+08:00
---

# Hoermann BiSecur：AES-128 双向无线门控被攻破

> 来源：34C3 · 2017-12-28 · [原文](https://media.ccc.de/v/34c3-9029-uncovering_vulnerabilities_in_hoermann_bisecur)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：加密本身没问题，问题在协议层的重放/状态同步与实现细节：双向握手给了攻击者可利用的确定性。
- **价值**：无线门控是物理安全的入口（车库门 = 家的入口）；这是“强加密 + 弱协议”的经典案例，对 IoT 门锁/门禁类设备评估极有参考价值。
- **难度**：高 —— 需要射频抓包、协议逆向与密码学基础。

Hoermann BiSecur 是双向无线门控/车库门控制系统，厂商宣传“和网银一样安全”。演讲拆解其 AES-128 加密信号与双向协议，找出可复现的绕过方式。
