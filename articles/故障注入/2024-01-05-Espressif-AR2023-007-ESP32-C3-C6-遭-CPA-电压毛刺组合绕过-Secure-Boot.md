---
title: "Espressif AR2023-007：ESP32-C3/C6 遭 CPA + 电压毛刺组合绕过 Secure Boot 与 Flash 加密"
source: "Espressif"
url: https://www.espressif.com/sites/default/files/advisory_downloads/AR2023-007%20Security%20Advisory%20Concerning%20Bypassing%20Secure%20Boot%20and%20Flash%20Encryption%20using%20CPA%20and%20FI%20attack%20on%20ESP32-C3%20and%20ESP32-C6%20EN.pdf
published: 2024-01-05
fetched: 2026-11-19T05:21:54.654Z
category: "故障注入"
score: 0
keywords: []
sha256: c208a167f18c516b11259c821da586ddf60e39aff5244ea70bba31dd93118be5
bytes: 1559
truncated: false
body_mode: notes
status: published
published_at: 2026-11-19T13:22:06.082437+08:00
---

# Espressif AR2023-007：ESP32-C3/C6 遭 CPA + 电压毛刺组合绕过 Secure Boot 与 Flash 加密

> 来源：Espressif · 2024-01-05 · [原文](https://www.espressif.com/sites/default/files/advisory_downloads/AR2023-007%20Security%20Advisory%20Concerning%20Bypassing%20Secure%20Boot%20and%20Flash%20Encryption%20using%20CPA%20and%20FI%20attack%20on%20ESP32-C3%20and%20ESP32-C6%20EN.pdf)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：注入点＝ROM 执行阶段的电压毛刺（通告未披露具体电源轨）；窗口与触发未公开，仅给出“需精心构造的毛刺”与两步串联的依赖关系；判定＝shellcode 在 Secure Boot 拦截前获得执行、设备机密被提取。厂商确认无软硬件修复，后续 H2/P4/C5 才在硬件里加入毛刺检测与自动复位。
- **价值**：少见由芯片厂商自己确认的“侧信道 + 故障注入”组合攻击；同时说明单点 CPA 只能恢复首块（每块 128B，且每台设备密钥唯一），对评估 ESP32 设备真实性风险很有用。
- **难度**：极高 —— 60 万条轨迹的 CPA + 精确到指令流的毛刺注入，属国家级实验室能力。

厂商官方安全通告：CPA 侧信道恢复第一 flash 块的 XTS-AES 密钥（约 60 万条功耗轨迹、约 5 天），再用电压毛刺在 ROM 代码中打出可控的缓冲区溢出，把攻击者 shellcode 写进首块；下次启动时 CPU 在 Secure Boot 识别篡改并中止之前跳转执行 shellcode，从而外泄设备机密。

## 方法论启示

- 评估固件加密时要同时问“CPA 能读多少”和“毛刺能改什么”，单看一侧会低估风险。
- 厂商通告的四问往往不完整，但它确认的“硬件级不可修补”结论本身就应进威胁模型。
