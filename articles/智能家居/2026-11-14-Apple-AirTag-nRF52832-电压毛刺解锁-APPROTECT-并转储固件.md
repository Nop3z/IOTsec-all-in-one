---
title: "Apple AirTag（nRF52832）电压毛刺解锁 APPROTECT 并转储固件"
source: "ensingerphilipp (GitHub)"
url: https://github.com/ensingerphilipp/airtag-glitch-dump-improved
published: 2026-11-14
fetched: 2026-11-19T05:21:54.654Z
category: "智能家居"
score: 0
keywords: []
sha256: 0a1e8bfa4043873761b926ee02fc0cb43085a1d069f922339cb2296b1e5f9794
bytes: 1165
truncated: false
body_mode: notes
status: published
published_at: 2026-11-19T13:22:06.082437+08:00
---

# Apple AirTag（nRF52832）电压毛刺解锁 APPROTECT 并转储固件

> 来源：ensingerphilipp (GitHub) · 2026-11-14 · [原文](https://github.com/ensingerphilipp/airtag-glitch-dump-improved)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：注入点＝AirTag nRF52832 的 VDD 测试点，BSS123 N-MOS 做 crowbar，需焊桥两路正电；触发＝1.8V→3.3V 电平转换后监视 NRF_VDD 上电沿（阈值用电位器调至 CMOS 逻辑电平）；判定＝openocd 能连上 SWD（APPROTECT 已解除），再用 nrfjprog/openocd 转储。
- **价值**：把一颗消费级追踪器从“黑盒”变成可 dump 固件的研究目标，硬件改造细节完整，适合作为 nRF52 系列 APPROTECT 攻击的模板。
- **难度**：高 —— 需要拆机、超细线焊接与参数扫描，但工具链（Pico + MOSFET）成本很低。

stacksmashing airtag-glitcher 的全文档改良版：Pico 固件管理毛刺时序与脉宽，Jupyter 扫 delay，openocd 检测 SWD 调试是否解锁，随后读取 AirTag 全部固件；附完整接线、焊点温度、1.8V→3.3V 电平转换与 MOSFET 选型。
