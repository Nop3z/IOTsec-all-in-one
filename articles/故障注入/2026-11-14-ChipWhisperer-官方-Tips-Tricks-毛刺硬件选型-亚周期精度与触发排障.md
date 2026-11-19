---
title: "ChipWhisperer 官方 Tips & Tricks：毛刺硬件选型、亚周期精度与触发排障"
source: "NewAE (Apache-2.0)"
url: https://github.com/newaetech/cw_tips_tricks
published: 2026-11-14
fetched: 2026-11-19T05:26:20.405Z
category: "故障注入"
score: 0
keywords: []
sha256: 1b1c6c369db262cd609a4dc706f0c4136535e046f190c27edad7fc2c9fd36f26
bytes: 1444
truncated: false
body_mode: notes
status: published
published_at: 2026-11-19T13:26:46.419198+08:00
---

# ChipWhisperer 官方 Tips & Tricks：毛刺硬件选型、亚周期精度与触发排障

> 来源：NewAE (Apache-2.0) · 2026-11-14 · [原文](https://github.com/newaetech/cw_tips_tricks)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：注入点＝CW 采集卡的 glitch_lp/glitch_hp 两路 crowbar（LP 更快更窄，HP 适合大电流目标）；窗口＝官方立场“不必知道每条采样对应哪条指令”，移动 trigger_high 观察轨迹平移 + 插 NOP 做时间标记即可；亚周期精度＝CLKGEN 走 EXTCLK 并倍频，使毛刺起止可按目标周期的分数调。
- **价值**：把“为什么打不中”拆成可逐项排查的工程问题（电源能力、触发抖动、时间换算、稳压器吸收），是入门与排障的权威参考。
- **难度**：低-中 —— 读文档 + 按图配置即可，不需要新建硬件。

## 方法论启示

- 先确认注入能力（管型/电源）与触发抖动，再谈参数扫描，否则扫参是在噪声里找信号。
- 内部 LDO 会“吃掉”毛刺：可外接略高电压把稳压器压到关断，或直接改注入点。

ChipWhisperer 官方文档里与故障注入直接相关的 7 篇：HP/LP crowbar 选管、Nano 毛刺-ADC 时间换算（glitch_time = 47.3 + ext_offset/16）、毛刺精度倍增、Husky UART 触发排障、毛刺可视化、指令与采样对应、内部稳压器处理。
