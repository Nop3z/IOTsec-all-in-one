---
title: "Rainbow：Unicorn 指令级侧信道 / 故障注入仿真器（Ledger Donjon）"
source: "Ledger Donjon (LGPL-3.0)"
url: https://github.com/Ledger-Donjon/rainbow
published: 2026-11-14
fetched: 2026-11-19T05:26:20.405Z
category: "故障注入"
score: 0
keywords: []
sha256: 4466d1b622bd51c80c396e2393b3a51f983abc890c29517672a4c4bec4be5307
bytes: 1168
truncated: false
body_mode: notes
status: published
published_at: 2026-11-19T13:26:46.419198+08:00
---

# Rainbow：Unicorn 指令级侧信道 / 故障注入仿真器（Ledger Donjon）

> 来源：Ledger Donjon (LGPL-3.0) · 2026-11-14 · [原文](https://github.com/Ledger-Donjon/rainbow)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：注入点＝仿真级指令/寄存器（skip、位翻转等，见 examples）；窗口＝先 trace 后选点（可与 fi_check 集成，把故障指令映射回源码行）；触发＝仿真事件（地址/循环计数）；判定＝执行流 diff（寄存器/输出差异）。
- **价值**：零硬件成本把固件 FI 预筛一遍，先找出“值得上机”的点，能显著减少物理实验次数。
- **难度**：中 —— 装 Python 包即可，但需要自己定义故障模型与判定。

## 方法论启示

- 仿真不是替代物理攻击，而是把物理攻击的尝试次数降到可接受。
- 同一进程里可同时做 SCA + FI 分析，两个视角互相印证。

基于 Unicorn 的脚本化仿真：一边产出侧信道轨迹（配合 lascar），一边在指令钩子上对任意指令/寄存器施故障——把物理 FI 的判定提前到开发期。
