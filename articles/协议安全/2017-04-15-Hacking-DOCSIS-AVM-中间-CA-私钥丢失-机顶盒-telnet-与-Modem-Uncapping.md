---
title: "Hacking DOCSIS：AVM 中间 CA 私钥丢失、机顶盒 telnet 与 Modem Uncapping"
source: "Easterhegg 2017"
url: https://media.ccc.de/v/EH2017-8488-hacking_docsis
published: 2017-04-15
fetched: 2026-11-27T02:01:28.690Z
category: "协议安全"
score: 0
keywords: []
sha256: fad87bd15592a4d62b9879c7285ab3916aa7343d552b461fcdaad17e26a0c406
bytes: 640
truncated: false
body_mode: notes
kind: practical
status: published
published_at: 2026-11-27T10:01:29.126372+08:00
---

# Hacking DOCSIS：AVM 中间 CA 私钥丢失、机顶盒 telnet 与 Modem Uncapping

> 来源：Easterhegg 2017 · 2017-04-15 · [原文](https://media.ccc.de/v/EH2017-8488-hacking_docsis)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：DOCSIS 的信任依赖设备证书与配置文件下发：私钥泄露 + 配置可篡改，就能同时破坏身份与计费两类安全属性。
- **价值**：有线宽带 CPE 是家庭入户的第一台设备，而 DOCSIS 生态的公开研究远少于 Wi-Fi；证书与配置文件这两条线很值得迁移研究。
- **难度**：高 —— 需要 DOCSIS 协议栈与运营商侧配置体系知识。

围绕 DOCSIS（有线电视宽带标准）的实战议题：AVM 的中间 CA 私钥如何丢失、有线盒子上的 telnet 后门如何进入，以及通过配置绕过速率限制（Uncapping）。
