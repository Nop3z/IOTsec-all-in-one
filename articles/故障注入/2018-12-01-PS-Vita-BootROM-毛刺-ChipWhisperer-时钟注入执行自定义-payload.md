---
title: "PS Vita BootROM 毛刺：ChipWhisperer 时钟注入执行自定义 payload"
source: "TeamMolecule (GitHub, MIT)"
url: https://github.com/TeamMolecule/petite-mort
published: 2018-12-01
fetched: 2026-11-19T05:21:54.654Z
category: "故障注入"
score: 0
keywords: []
sha256: c80864dcecae3a8a5d20d7345846acf26756f1f219dedf589f873acfeeaaa149
bytes: 1112
truncated: false
body_mode: notes
status: published
published_at: 2026-11-19T13:22:06.082437+08:00
---

# PS Vita BootROM 毛刺：ChipWhisperer 时钟注入执行自定义 payload

> 来源：TeamMolecule (GitHub, MIT) · 2018-12-01 · [原文](https://github.com/TeamMolecule/petite-mort)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：注入点＝由 CW extclkgen 供给的 Vita 外部时钟（clock 注入）；窗口＝以 extclkgen 周期为单位的 offset×width 扫描，脚本内已预置已知可用参数；触发＝MMC 流量空闲超时 / 手动 / tzpwn 自动引导三类；判定＝UART 出现 payload 输出（size-check 变体还要求 MBR 特定偏移满足阈值）。
- **价值**：把游戏机 BootROM 级攻击的脚本与参数公开出来，是“clock 注入 + 多触发变体”的完整样本。
- **难度**：高 —— 需要拆机供时钟、ChipWhisperer 与较老的 Python2 工具链。

用 ChipWhisperer 毛刺 PS Vita 的 BootROM：绕过引导早期的大小检查/异常向量保护，让自定义 payload 在 BootROM 阶段执行；仓库给出 6 个脚本对应同一攻击的不同触发变体，含“双毛刺”串联。

## 方法论启示

- 时钟注入与电压注入要分开评估：有些 BootROM 对时钟沿更敏感。
- 多触发变体（流量空闲/手动/自动引导）能显著提高复现成功率。
