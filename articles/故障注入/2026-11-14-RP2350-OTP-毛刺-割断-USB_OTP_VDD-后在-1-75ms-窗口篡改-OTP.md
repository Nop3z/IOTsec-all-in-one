---
title: "RP2350 OTP 毛刺：割断 USB_OTP_VDD 后在 ~1.75ms 窗口篡改 OTP"
source: "MKesenheimer"
url: https://mkesenheimer.github.io/blog/glitching-the-rp2350.html
published: 2026-11-14
fetched: 2026-11-19T05:21:54.654Z
category: "故障注入"
score: 0
keywords: []
sha256: e3f91a45b003e85912233497aa9bd3641d4c9dbc2176c3f5e7dc115828741f5b
bytes: 1180
truncated: false
body_mode: notes
status: published
published_at: 2026-11-19T13:22:06.082437+08:00
---

# RP2350 OTP 毛刺：割断 USB_OTP_VDD 后在 ~1.75ms 窗口篡改 OTP

> 来源：MKesenheimer · 2026-11-14 · [原文](https://mkesenheimer.github.io/blog/glitching-the-rp2350.html)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：注入点＝RP2350 的 USB_OTP_VDD 引脚（割线使其浮空后外部施加 3.3V）；窗口＝电流曲线显示 OTP 读取期，定位在复位后约 1.75ms，粗扫 delay 1.7–1.8ms / length 1–5µs 后细扫；触发＝毛刺器复位输出自环（复位沿即 0 点）；判定＝OTP 存储区出现 'c0ffee' 标记并可回读。
- **价值**：2.5% 命中率说明 RP2350 的 OTP 窗口防护很薄；完整给出了“割线—探针—扫参—判据”的低成本复现路径（Pico Glitcher 即可）。
- **难度**：高 —— 需要取下芯片、割线与探针接触，但器材成本低（百元级）。

Pico Glitcher 作者对 38C3“Hacking the RP2350”研究的独立复现：手术刀割断 USB_OTP_VDD 走线后由探针施加电压，在复位后约 1.75ms 的 OTP 读取窗口注入毛刺，约 2.5% 命中率即可写入/篡改 OTP 内容（'c0ffee' 判据）。

## 方法论启示

- 割线让引脚浮空 + 外部施加电压，是绕过片上 LDO/监控的低成本手法。
- 低命中率（2.5%）可以接受，只要判定明确、脚本能自动重试。
