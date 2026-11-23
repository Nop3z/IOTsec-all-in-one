---
title: "FACT：固件分析与比较工具（Firmware Analysis and Comparison Tool）"
source: "Fraunhofer FKIE"
url: https://github.com/fkie-cad/FACT_core
published: 2024-01-01
fetched: 2026-11-23T05:25:20.401Z
category: "固件解密"
score: 0
keywords: ["classic"]
sha256: a08e82fa09cbaf95f862ccfd79878919e30e2e739e692bf3e622fe27f82c71ef
bytes: 1146
truncated: false
body_mode: notes
kind: practical
status: published
published_at: 2026-11-23T13:25:28.351751+08:00
---

# FACT：固件分析与比较工具（Firmware Analysis and Comparison Tool）

> 来源：Fraunhofer FKIE · 2024-01-01 · [原文](https://github.com/fkie-cad/FACT_core)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：把“单镜像手工分析”变成“批量、可复现的流水线”，配合 CVE 数据库可以快速找出某批设备中的已知漏洞组件。
- **价值**：固件供应链审计的工程化工具，适合与 BinQL、VulHunt 等“变体/漏洞狩猎”工具搭配使用。
- **难度**：中 —— 需要 Docker 与基本运维能力。

学术机构维护的开源固件分析平台：自动解包、识别组件、做 CVE 匹配与版本对比，适合批量分析一个厂商的固件镜像库。
