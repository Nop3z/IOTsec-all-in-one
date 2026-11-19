---
title: "Mercedes 防盗器 ECU 过压毛刺：短暂恢复被熔断的 JTAG"
source: "TROOPERS 2025"
url: https://troopers.de/troopers25/talks/et37yq/
published: 2025-06-01
fetched: 2026-11-19T05:21:54.654Z
category: "车机"
score: 0
keywords: []
sha256: 2cc87ec951d3e66bba5c39a0f9b4c1d787437b92cac0dd2ce496eacc79abd108
bytes: 1140
truncated: false
body_mode: notes
status: published
published_at: 2026-11-19T13:22:06.082437+08:00
---

# Mercedes 防盗器 ECU 过压毛刺：短暂恢复被熔断的 JTAG

> 来源：TROOPERS 2025 · 2025-06-01 · [原文](https://troopers.de/troopers25/talks/et37yq/)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：注入点＝MCU 供电轨的过压方向毛刺；窗口＝启动相位中“细微的窗口机会”（演讲未公开具体时序）；触发未公开；判定＝被锁死的 JTAG 短暂可用、可读出部分 flash，但防盗功能仍保持禁用——属于“部分绕过”的中间态。
- **价值**：库里绝大多数案例是把电压往下打，这例提示毛刺可以双向；同时展示了“调试口恢复但功能仍锁”这种罕见的中间态，对判定分级很有参考价值。
- **难度**：极高（且细节未公开）—— 需要 PCB 逆向、隐藏测试点定位与双向毛刺硬件。

对奔驰防盗器 ECU 里的定制安全 MCU 在启动相位施加“过压”毛刺（与常见 crowbar 下压方向相反），让被熔丝和电压/时钟监控封死的 JTAG 短暂恢复可访问，从而提取固件碎片并观察 HSM 内部。

## 方法论启示

- 毛刺是双向的：在“熔丝 + 电压监控”封死的芯片上，过压可能比下压更有效。
- “调试口恢复但功能仍锁”这种部分绕过，要求判定分级，不能只有成功/失败两档。
