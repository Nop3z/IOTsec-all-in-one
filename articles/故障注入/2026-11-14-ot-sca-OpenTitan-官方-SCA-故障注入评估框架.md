---
title: "ot-sca：OpenTitan 官方 SCA + 故障注入评估框架"
source: "lowRISC (Apache-2.0)"
url: https://github.com/lowRISC/ot-sca
published: 2026-11-14
fetched: 2026-11-19T05:26:20.405Z
category: "故障注入"
score: 0
keywords: []
sha256: 7a9ca785c80a69ccd1e8cb687658aa376d944b81aced0e35427282bc711a36a0
bytes: 1207
truncated: false
body_mode: notes
kind: practical
status: published
published_at: 2026-11-19T13:26:46.419198+08:00
---

# ot-sca：OpenTitan 官方 SCA + 故障注入评估框架

> 来源：lowRISC (Apache-2.0) · 2026-11-14 · [原文](https://github.com/lowRISC/ot-sca)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：注入点＝EMFI 探针（ChipShover 控坐标）或 Husky 电压通道；窗口＝配置文件驱动的参数扫描（脉冲最小步长 1 时钟≈20ns，宽度=repeat×20ns，延迟=ext_offset×20ns，并计入 Husky/ChipShouter 的固定硬件延迟）；触发＝目标固件在关键操作处发出的 IO4 上升沿；判定＝按 FI 特征化结果统计。
- **价值**：开源安全芯片的“参考攻击基准”，可直接作为自家设备的安全测试基线。
- **难度**：高 —— 需要 CW310 FPGA 板与完整台架。

## 方法论启示

- 把攻击参数扫描脚本化、CI 化，才能把“能不能被打”变成可回归的测试项。
- 固定硬件延迟必须计入参数：否则不同工具链的结果无法对齐。

lowRISC 官方框架：ChipWhisperer Husky + ChipShouter（EMFI）+ ChipShover XYZ，或 Husky 电压毛刺，对 Ibex RISC-V、OTBN、AES/KMAC、OTP 等做自动化故障参数扫描与特征化。
