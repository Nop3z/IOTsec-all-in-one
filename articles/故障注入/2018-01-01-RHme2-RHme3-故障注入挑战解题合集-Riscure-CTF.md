---
title: "RHme2 / RHme3 故障注入挑战解题合集（Riscure CTF）"
source: "Riscure / 社区 writeups"
url: https://github.com/Riscure/Rhme-2016
published: 2018-01-01
fetched: 2026-11-19T05:26:20.405Z
category: "故障注入"
score: 0
keywords: []
sha256: 27fd182f59bde5c651e313d24f854d2408ac991a75657518dfa803801954009c
bytes: 1172
truncated: false
body_mode: notes
kind: practical
status: published
published_at: 2026-11-19T13:26:46.419198+08:00
---

# RHme2 / RHme3 故障注入挑战解题合集（Riscure CTF）

> 来源：Riscure / 社区 writeups · 2018-01-01 · [原文](https://github.com/Riscure/Rhme-2016)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：注入点＝时钟或 VCC 毛刺（HydraRHME2 / ChipWhisperer / Glitch Module）；窗口＝Glitch Explorer 扫 offset（如 -49%~30% 步进 1%）或示波器辅助定位；触发＝Target IO1/IO2 串口沿；判定＝输出从循环 “Lock” 变为含 “FLAG”。
- **价值**：最好的毛刺入门题集：参数、脚本、判定都被公开过，适合把工具链完整跑通再上真实设备。
- **难度**：低-中 —— 有现成参数与 writeup，主要成本是搭台架。

## 方法论启示

- 先用 CTF 靶把工具链跑通，再上真实设备，是省时间的路径。
- 公开参数只是起点：同一型号不同批次仍需重扫。

Riscure 两届嵌入式硬件 CTF 的公开解题资料：RHme2 四道 FI 挑战（Fiesta/Finetuning/Fiasco/Revenge）+ RHme3 benzinegate，逐题给出注入点、窗口、触发与判定（offset/width/repeat 参数都有公开答案）。
