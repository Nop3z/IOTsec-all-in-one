---
title: "ATECC608A 安全元件：两发激光故障读出 PIN hash（Coldcard Mk3 种子可窃）"
source: "SSTIC 2021 / Ledger Donjon"
url: https://www.sstic.org/media/SSTIC2021/SSTIC-actes/defeating_a_secure_element_with_multiple_laser_fau/SSTIC2021-Article-defeating_a_secure_element_with_multiple_laser_fault_injections-heriveaux.pdf
published: 2021-06-01
fetched: 2026-11-19T05:26:20.405Z
category: "故障注入"
score: 0
keywords: []
sha256: 32444253a51f3f6c998b432364519ab374c192b2c5adbe464c5c4e66e24680f8
bytes: 1522
truncated: false
body_mode: notes
kind: theory
status: published
published_at: 2026-11-19T13:26:46.419198+08:00
---

# ATECC608A 安全元件：两发激光故障读出 PIN hash（Coldcard Mk3 种子可窃）

> 来源：SSTIC 2021 / Ledger Donjon · 2021-06-01 · [原文](https://www.sstic.org/media/SSTIC2021/SSTIC-actes/defeating_a_secure_element_with_multiple_laser_fau/SSTIC2021-Article-defeating_a_secure_element_with_multiple_laser_fault_injections-heriveaux.pdf)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：注入点＝背面去封的 ATECC608A，红外脉冲激光 + 20X 物镜（光斑约 3µm，但该漏洞对空间精度不敏感，作者称 <$10k 设备可复现）；窗口＝上电后约 1.3s 的 wake-up/自检段，用电流采样 + 示波器对齐；判定＝读出的数据槽内容为明文（“stick bits to zero”故障模型）。
- **价值**：“多次激光故障组成的利用链”在安全元件上的少见完整案例，直接击穿“密钥不可导出”的假设。
- **难度**：极高 —— 需要去封、激光注入台与大量固件建模工作。

## 方法论启示

- 故障模型一旦确定（stick-to-zero），利用链可以极短——2 发激光就够。
- 安全元件的“不可导出”是行为约束，不是物理约束。

全黑盒评估 ATECC608A：先用功耗 trace 与逐步试探构建固件实现假设，最终在一次命令执行内仅用 2 发激光故障（绕过 data slot 的 IS_SECRET 检查 + 绕过配置 CRC double-check）就明文读出 PIN hash 数据槽，Coldcard Mk3 的种子因此可被窃取。
