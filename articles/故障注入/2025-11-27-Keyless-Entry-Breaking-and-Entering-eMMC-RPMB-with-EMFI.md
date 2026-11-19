---
title: "Keyless Entry: Breaking and Entering eMMC RPMB with EMFI"
source: "arXiv"
url: http://arxiv.org/abs/2511.22340v1
published: 2025-11-27
fetched: 2026-11-19T12:07:27.218470+08:00
category: "故障注入"
score: 0
keywords: ["emfi", "emmc"]
sha256: c19e39de42f9c66d6f5950dbca21c4a264c65efab163350685756d6f8c52edef
bytes: 641
truncated: false
body_mode: meta
kind: theory
status: published
published_at: 2026-11-19T12:20:43.910308+08:00
---

# Keyless Entry: Breaking and Entering eMMC RPMB with EMFI

> 来源：arXiv · 2025-11-27 · [原文](http://arxiv.org/abs/2511.22340v1)
> 归档用于安全研究参考；版权归原作者所有。

> ⚠️ 本条为「元数据 + 摘要」归档（论文/PDF/前端渲染页面），完整内容请读原文。

## 收录理由

- **核心**：用电磁故障注入（EMFI）攻破 eMMC 的 RPMB 认证：让“只能读写受保护分区”的存储失去完整性保证。
- **价值**：RPMB 被广泛用于存放设备密钥/回滚计数（手机、车机、IoT），被攻破意味着防回滚与密钥存储失效；这个角度很新。
- **难度**：高 —— 需要精确的 EMFI 位置与时序，且要对三家不同 eMMC 复现。

The Replay Protected Memory Block (RPMB) in modern storage systems provides a secure area where data integrity is ensured by authentication. This block is used in digital devices to store pivotal information that must be safeguarded against modification by potential attackers. This paper targets the authentication scheme of the RPMB in three different eMMCs from a major manufacturer. A glitch was injected by sending an electromagnetic pulse to the target chip. RPMB authentication was successfully glitched and the information stored in two target eMMCs was overwritten with arbitrary data, without affecting the integrity of other data.
