---
title: "ChipShover：EMFI/EM 探针的 XYZ 定位台"
source: "NewAE"
url: https://github.com/newaetech/ChipShover
published: 2026-11-14
fetched: 2026-11-19T05:26:20.405Z
category: "故障注入"
score: 0
keywords: []
sha256: 82b86ba53e166b60710c71755187e7b7dcf0bbdd3b984e7c9e469bb6a40b0105
bytes: 1122
truncated: false
body_mode: notes
kind: practical
status: published
published_at: 2026-11-19T13:26:46.419198+08:00
---

# ChipShover：EMFI/EM 探针的 XYZ 定位台

> 来源：NewAE · 2026-11-14 · [原文](https://github.com/newaetech/ChipShover)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：注入点＝本身不注入，为探针提供亚微米定位；窗口＝坐标-时序联合扫描（Python 编排台架移动 + 注入器触发）；触发＝与所挂注入器的触发链配合；判定＝记录“哪个坐标命中”，作为证据链的一部分。
- **价值**：EM 攻击的可复现性高度依赖坐标记录，这是该环节的标准件；两档精度也给出了预算参考。
- **难度**：中 —— 组装/驱动为主，可与 ChipSHOUTER 等直接对接。

## 方法论启示

- “哪个坐标命中”应当进证据链，而不是只记电参数。
- 空间扫描的精度与成本是线性关系：先明确目标所需精度再选台架。

EMFI/EM 探针的 XYZ 定位系统：步进电机台（中精度 156.25nm 步距/约 3µm 误差；低精度 781.25nm/50–100µm）+ Marlin 固件 + Python 接口，50×50mm 标准接位挂载注入器/探头。
