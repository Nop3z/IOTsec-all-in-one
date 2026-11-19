---
title: "SPHINCS+ 故障攻击与对策（TCHES 2023 官方 artifact）"
source: "TCHES 2023 (CRAPL)"
url: https://github.com/AymericGenet/SPHINCSplus-FA
published: 2023-06-01
fetched: 2026-11-19T05:26:20.405Z
category: "故障注入"
score: 0
keywords: []
sha256: 7c29e0d30b7da2f28962bbea2eae5a33350d423ee0d07743719881278693dce4
bytes: 1149
truncated: false
body_mode: notes
kind: practical
status: published
published_at: 2026-11-19T13:26:46.419198+08:00
---

# SPHINCS+ 故障攻击与对策（TCHES 2023 官方 artifact）

> 来源：TCHES 2023 (CRAPL) · 2023-06-01 · [原文](https://github.com/AymericGenet/SPHINCSplus-FA)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：注入点＝ChipWhisperer 毛刺口（logs 显示 width=20、offset=-4、ext=0 量级）；窗口＝evaluation 按故障模型枚举 + 实测用 GlitchController 扫参；触发＝SimpleSerial 固件串口命令帧；判定＝签名输出/验证结果与理论预测一致。
- **价值**：后量子签名在硬件上同样怕故障——“PQC 不等于免疫 FI”，对新算法落地前的评估很关键。
- **难度**：高 —— 需要读论文 + 复现仿真与实测两套流程。

## 方法论启示

- 新算法上设备前，应同时评估侧信道与故障两类物理攻击。
- 理论故障模型 + 实测参数扫描两条腿走路，结论才站得住。

对哈希签名 SPHINCS+ 的故障注入攻击与对策：理论分析 + 对策设计 + ChipWhisperer 实测三件套（attack/ 攻击脚本、evaluation/ 论文表格复现、experimentation/ 实测）。
