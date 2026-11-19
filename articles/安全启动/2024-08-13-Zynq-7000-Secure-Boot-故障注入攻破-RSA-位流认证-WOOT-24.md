---
title: "Zynq-7000 Secure Boot：故障注入攻破 RSA 位流认证（WOOT'24）"
source: "USENIX WOOT 2024"
url: https://www.usenix.org/conference/woot24/presentation/ravi
published: 2024-08-13
fetched: 2026-11-19T05:21:54.654Z
category: "安全启动"
score: 0
keywords: []
sha256: b2aa94f5e6629775dc7f983fd0eea8a1fd41753464a36c6ef79bc3c2163cc684
bytes: 984
truncated: false
body_mode: notes
status: published
published_at: 2026-11-19T13:22:06.082437+08:00
---

# Zynq-7000 Secure Boot：故障注入攻破 RSA 位流认证（WOOT'24）

> 来源：USENIX WOOT 2024 · 2024-08-13 · [原文](https://www.usenix.org/conference/woot24/presentation/ravi)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：注入点＝BootROM 的 RSA 验签环节（论文级细节需读原文）；判定＝RSA 认证被绕过且位流可恢复。官方 artifact 仓库仅含 README，实现细节在论文 PDF。
- **价值**：FPGA SoC 的安全启动把 RSA 验签作为唯一信任根，这例说明“验签算法本身就是高价值毛刺靶”，对评估 FPGA/SoC 安全启动有直接意义。
- **难度**：极高 —— 需要 BootROM 时序定位与可复现的故障注入台架。

论文《Achilles Heel in Secure Boot: Breaking RSA Authentication and Bitstream Recovery from Zynq-7000 SoC》：对 Zynq-7000 的 BootROM RSA 验证环节做故障注入，绕过位流认证并恢复加密位流内容。
