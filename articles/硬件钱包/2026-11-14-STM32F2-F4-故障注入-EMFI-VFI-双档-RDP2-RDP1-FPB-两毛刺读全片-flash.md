---
title: "STM32F2/F4 故障注入：EMFI/VFI 双档 RDP2→RDP1 + FPB 两毛刺读全片 flash"
source: "Joe Grand / Lennert Wouters (GitHub)"
url: https://github.com/joegrand/stm32-fault-injection
published: 2026-11-14
fetched: 2026-11-19T05:21:54.654Z
category: "硬件钱包"
score: 0
keywords: []
sha256: 1e5f90e33a81d8d79d8848fcdbefbb8109f19a6a11565061fe149668d6319812
bytes: 1219
truncated: false
body_mode: notes
kind: practical
status: published
published_at: 2026-11-19T13:22:06.082437+08:00
---

# STM32F2/F4 故障注入：EMFI/VFI 双档 RDP2→RDP1 + FPB 两毛刺读全片 flash

> 来源：Joe Grand / Lennert Wouters (GitHub) · 2026-11-14 · [原文](https://github.com/joegrand/stm32-fault-injection)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：注入点＝EMFI（ChipSHOUTER，可选 CNC 做 XY 定位）与 VFI（ChipWhisperer 毛刺口打供电）；窗口确定＝notebooks 先做参数表征再做攻击（1 表征 EMFI 坐标×时序、2 表征 bootloader/RDP 时序）；触发＝ChipWhisperer 触发链，bootloader 场景用 UART 帧；判定＝RDP2→1 时 bootloader 对话行为变化、FPB 组合后读出内容与预期一致。
- **价值**：这是 Trezor One/Model T、KeepKey 等硬件钱包主控族的“通用提取流程”，把过去容易变砖的 RDP 攻击做成可重复流水线。
- **难度**：极高 —— 需要芯片座、EMFI/VFI 台架与大量表征实验。

REcon 2026 的三年打磨成果：用 EMFI/VFI 双注入档把 STM32F205/F427 的读保护从 RDP2 降级到 RDP1，再毛刺 bootloader 命令做安全提取，与 FPB（Flash Patch & Breakpoint）攻击组合后仅两个毛刺即可读出全片 flash。

## 方法论启示

- 把 RDP 攻击做成“先表征后攻击”的流水线，是降低变砖率的关键。
- EMFI 与 VFI 双档对照：同一目标上两种通道的成功率/稳定性不同，值得都试。
