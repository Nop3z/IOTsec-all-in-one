---
title: "Investigating the Iridium Satellite Network：用 SDR 监听铱星网络"
source: "38C3"
url: https://media.ccc.de/v/38c3-investigating-the-iridium-satellite-network
published: 2024-12-27
fetched: 2026-11-28T02:02:29.911Z
category: "卫星安全"
score: 0
keywords: []
sha256: e8b93fc8dd739356cb54c88f3f2e6dbcc5de47fc5afdb14526ee4e6e6d6c3c11
bytes: 651
truncated: false
body_mode: notes
kind: practical
status: published
published_at: 2026-11-28T10:02:30.318728+08:00
---

# Investigating the Iridium Satellite Network：用 SDR 监听铱星网络

> 来源：38C3 · 2024-12-27 · [原文](https://media.ccc.de/v/38c3-investigating-the-iridium-satellite-network)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：攻击面＝卫星下行链路的可监听性：用 SDR + gr-iridium 一类工具即可捕获并解析铱星的突发信号，进而还原短消息/寻呼/数据业务。
- **价值**：铱星协议私有且覆盖全球，公开研究极少；这是目前最完整的“从零开始监听铱星”的实战路径。
- **难度**：高 —— 需要 SDR 硬件、信号处理与私有协议逆向。

铱星（Iridium）卫星电话网络一直在演进，研究工具也比 32C3 时代强得多。演讲深入监听铱星的技术细节：新发现的服务、信号结构、解码流程与可用的软硬件工具链。
