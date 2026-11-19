---
title: "Qualcomm IPQ40xx QSEE：EMFI 绕过安全范围检查实现任意 NULL 写"
source: "Raelize"
url: https://raelize.com/blog/qualcomm-ipq40xx-breaking-into-qsee-using-fault-injection/
published: 2021-06-07
fetched: 2026-11-19T05:21:54.654Z
category: "故障注入"
score: 0
keywords: []
sha256: bb3702d8e4bdfa56e45444572f5b1be477dd512fd2905c3a800ccafc8780d925
bytes: 1241
truncated: false
body_mode: notes
status: published
published_at: 2026-11-19T13:22:06.082437+08:00
---

# Qualcomm IPQ40xx QSEE：EMFI 绕过安全范围检查实现任意 NULL 写

> 来源：Raelize · 2021-06-07 · [原文](https://raelize.com/blog/qualcomm-ipq40xx-breaking-into-qsee-using-fault-injection/)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：注入点＝拆散热片后 EM 探针直接贴芯片表面；窗口＝先用 U-Boot standalone app 的 add sled + GPIO 围出攻击窗，约 2 万次实验扫全芯片表面、按 G/Y/R/M 分色定位热点并固定探针位置，再对 SMC 调用段做约 5.875µs 的窗口；触发＝GPIO 内存映射寄存器（0x0102f004）边沿；判定＝串口应答从 `AAAA0000…BBBB` 变为 `AAAAffffffee…BBBB`（NULL 真写进 0x87EAB204 并可回读）。
- **价值**：把“先固定空间、再打时序”的表征流程做得很完整，是路由器 SoC 进入安全世界（QSEE）的少见公开案例。
- **难度**：极高 —— 约 30 万次实验、12 小时，需要 EM 台架与精细触发编排。

在 Linksys EA8300 路由器上用 EMFI 打 QSEE（高通 TEE）软件本身：毛刺跳过 SMC handler 里的 is_ree_range 校验，使来自 REE 的指针能写进 secure memory，形成对任意地址的 NULL 写。

## 方法论启示

- 先固定空间、再降维打时序：EM 探针先在芯片表面做 2D 扫描锁定热点，再只扫时间与功率。
- 用 GPIO 围出攻击窗（触发寄存器）是最通用的锚点，比依赖协议时序稳定。
