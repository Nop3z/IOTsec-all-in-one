---
title: "Iridium Pager Hacking：逆向铱星寻呼系统的始末"
source: "31C3"
url: https://media.ccc.de/v/31c3_-_6236_-_en_-_saal_1_-_201412281645_-_iridium_pager_hacking_-_sec_-_schneider
published: 2014-12-28
fetched: 2026-11-28T02:02:29.911Z
category: "卫星安全"
score: 0
keywords: []
sha256: da203468f61c5909123842cb836170cb87b5de9c8b0f27f86cf4da3ac14ba94d
bytes: 541
truncated: false
body_mode: notes
kind: practical
status: published
published_at: 2026-11-28T10:02:30.318728+08:00
---

# Iridium Pager Hacking：逆向铱星寻呼系统的始末

> 来源：31C3 · 2014-12-28 · [原文](https://media.ccc.de/v/31c3_-_6236_-_en_-_saal_1_-_201412281645_-_iridium_pager_hacking_-_sec_-_schneider)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：寻呼业务把消息明文/弱加密地广播到全球，只要捕获下行信号就能还原内容；协议逆向从物理层一路做到应用层。
- **价值**：卫星通信监听领域的经典起点；配合 38C3 的新进展一起看，能看到十年间工具与认知的演进。
- **难度**：高 —— 需要 SDR 与私有协议逆向。

对铱星寻呼系统做完整逆向的记录：从空口信号捕获、协议结构分析到消息解码，是铱星监听研究的早期奠基性工作。
