---
title: "Linux 内核视角的 Spectre 缓解与状态检查"
source: "kernel.org 文档"
url: https://www.kernel.org/doc/html/latest/admin-guide/hw-vuln/spectre.html
published: 2018-01-04
fetched: 2026-11-23T05:31:26.153Z
category: "芯片安全"
score: 0
keywords: ["rowhammer","spectre"]
sha256: ebcfeec571047743157535c34c5315565c8bcbfbaf2465b2d19ccb4ba9c3b67e
bytes: 476
truncated: false
body_mode: notes
kind: theory
status: published
published_at: 2026-11-23T13:31:32.371156+08:00
---

# Linux 内核视角的 Spectre 缓解与状态检查

> 来源：kernel.org 文档 · 2018-01-04 · [原文](https://www.kernel.org/doc/html/latest/admin-guide/hw-vuln/spectre.html)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：判断一台设备实际处于什么防护状态，看它最准：spectre_v2 状态、MSR 设置与内核开关都在此。
- **价值**：设备安全评估/加固时判断“是否启用缓解、代价多大”的第一手资料。
- **难度**：低 —— 文档阅读即可，实用价值高。

Linux 官方文档系统说明 Spectre 家族成因、变体、默认缓解与可调参数，包含运行时缓解状态检查与性能影响。
