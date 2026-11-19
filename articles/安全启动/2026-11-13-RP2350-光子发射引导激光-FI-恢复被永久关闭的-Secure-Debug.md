---
title: "RP2350 光子发射引导激光 FI：恢复被永久关闭的 Secure Debug"
source: "Ledger Donjon"
url: https://donjon.ledger.com/blog/rp2350-secure-debug-laser-fault-injection/
published: 2026-11-13
fetched: 2026-11-19T05:21:54.654Z
category: "安全启动"
score: 0
keywords: []
sha256: 6e2d06d7fc1be43b180c9f2fa7e3009c941097a83d4a7b369244392f09d8518b
bytes: 1296
truncated: false
body_mode: notes
kind: practical
status: published
published_at: 2026-11-19T13:22:06.082437+08:00
---

# RP2350 光子发射引导激光 FI：恢复被永久关闭的 Secure Debug

> 来源：Ledger Donjon · 2026-11-13 · [原文](https://donjon.ledger.com/blog/rp2350-secure-debug-laser-fault-injection/)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：注入点＝芯片内 DEBUGEN 各位的存储单元/逻辑（20x 物镜光斑过大无法复现，需 50x）；窗口＝OTP reset 之后、签名固件写 otp_hw->sw_lock[48] 之前，配合 rescue reset；触发＝脚本驱动的迭代脉冲序列（非单沿触发），每脉冲后读 Mem-AP 与 CSW.SDeviceEn 校准；判定＝总线访问恢复 + SDeviceEn=1 + Secure-only DEBUGEN 读出 0xF。
- **价值**：光子发射定位 + 激光翻转的“物理层精确制导”，是目前 RP2350（及类似 Secure Boot 芯片）最前沿的攻击面，也说明永久熔丝锁并非绝对。
- **难度**：极高 —— 作者估算约 25 万美元设备（PEM 红外相机/InGaAs 探测 + 激光台）。

用差分光子发射显微（PEM）定位 RP2350 中 DEBUGEN 寄存器各位的硅片位置，再用 980nm 脉冲激光在两处翻转两位，恢复被 CRIT1.DEBUG_DISABLE 永久关闭的 Secure debug，随后借 rescue reset 在固件收紧软锁前读出 OTP 里的挑战 secret。

## 方法论启示

- 永久熔丝锁不是绝对：先用光子发射定位寄存器位，再激光翻位。
- 空间精度决定成败（20x 光斑不行、50x 可行），设备预算直接决定可行性。
