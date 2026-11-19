---
title: "Trezor 穿壳 EMFI：毛刺 USB 栈长度检查读出 metadata/seed"
source: "Colin O'Flynn"
url: https://colinoflynn.com/2019/03/glitching-trezor-using-emfi-through-the-enclosure/
published: 2019-03-06
fetched: 2026-11-19T05:21:54.654Z
category: "硬件钱包"
score: 0
keywords: []
sha256: 08f3ef298b65ef961c71f778c975666262cdf87ebcf320f78b5b80edb7fbca3b
bytes: 1249
truncated: false
body_mode: notes
status: published
published_at: 2026-11-19T13:22:06.082437+08:00
---

# Trezor 穿壳 EMFI：毛刺 USB 栈长度检查读出 metadata/seed

> 来源：Colin O'Flynn · 2019-03-06 · [原文](https://colinoflynn.com/2019/03/glitching-trezor-using-emfi-through-the-enclosure/)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：注入点＝ChipSHOUTER 探针悬在 Trezor 外壳上方；窗口＝Beagle 480 抓到 USB 请求后 4.2–5.7µs 区间，实测取 4.4µs 偏移；触发＝Beagle 480 在 WinUSB descriptor 请求前两字节触发（主机请求 0xFFFF 长度）；判定＝响应字节数远超正常 0x92，读出的大块数据即包含 seed/metadata。
- **价值**：“毛刺返回值/长度字段”而不是毛刺代码逻辑，思路极通用；且穿壳注入说明“封壳”不构成物理防护，对硬件钱包威胁建模很有价值。
- **难度**：高 —— 需要 USB 分析仪做触发、参数扫描与掉电复位；作者明确拒绝替人恢复遗忘密码。

对 Trezor One 做穿壳 EMFI：几乎所有 USB 栈都有 `*len = MIN(*len, struct_len)` 的长度钳制，毛刺跳过该检查后设备按主机请求的 0xFFFF 返回数据，从而读出 bootloader flash 之后的 metadata（含 recovery seed），全程不拆外壳。

## 方法论启示

- 别只盯代码逻辑：返回值与长度字段的钳制（MIN）同样是高价值毛刺点。
- 封壳不构成物理防护；需要 USB 分析仪做触发 + 掉电复位的兜底流程。
