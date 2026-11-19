---
title: "Trezor / KeepKey 硬件钱包安全分析（CVUT 学位论文）"
source: "CVUT 2020"
url: https://dspace.cvut.cz/bitstream/handle/10467/88181/F8-BP-2020-Kozak-Lukas-thesis.pdf
published: 2020-06-01
fetched: 2026-11-19T05:40:43.175Z
category: "硬件钱包"
score: 0
keywords: []
sha256: 80f195a24e9daca8f5304aec43aacb67876b1399f5d865abd9f87be73f90643e
bytes: 691
truncated: false
body_mode: notes
kind: theory
status: published
published_at: 2026-11-19T13:40:51.833712+08:00
---

# Trezor / KeepKey 硬件钱包安全分析（CVUT 学位论文）

> 来源：CVUT 2020 · 2020-06-01 · [原文](https://dspace.cvut.cz/bitstream/handle/10467/88181/F8-BP-2020-Kozak-Lukas-thesis.pdf)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：把硬件钱包的物理攻击（毛刺/供应链）与软件问题放在同一框架下评估。
- **价值**：学术视角的硬件钱包威胁模型，适合作为研究入口。
- **难度**：中 —— 论文阅读 + 基础硬件知识。

系统梳理 Trezor One/Model T 与 KeepKey 的攻击面：供应链攻击、电压毛刺故障攻击、固件与调试接口，并给出实验。
