---
title: "Don't Ruck Us Too Hard：攻破 Ruckus 无线 AP 与控制器（3 个 pre-auth RCE）"
source: "36C3"
url: https://media.ccc.de/v/36c3-10816-don_t_ruck_us_too_hard_-_owning_ruckus_ap_devices
published: 2019-12-28
fetched: 2026-11-27T02:01:28.690Z
category: "防火墙"
score: 0
keywords: []
sha256: 5213960b37e35e4e1570863fc03afa38e342f24e259156b63feabbfea2282469
bytes: 580
truncated: false
body_mode: notes
kind: practical
status: published
published_at: 2026-11-27T10:01:29.126372+08:00
---

# Don't Ruck Us Too Hard：攻破 Ruckus 无线 AP 与控制器（3 个 pre-auth RCE）

> 来源：36C3 · 2019-12-28 · [原文](https://media.ccc.de/v/36c3-10816-don_t_ruck_us_too_hard_-_owning_ruckus_ap_devices)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：企业 Wi-Fi 控制器/AP 的管理面长期暴露在内网，串起多个小问题就能拼出 pre-auth RCE。
- **价值**：企业无线设备是“内网入口里的入口”，这类多漏洞组合的公开复盘对评估 AP/AC 设备很有价值。
- **难度**：高 —— 需要固件逆向与多漏洞组合利用。

对 Ruckus 接入点与无线控制器的漏洞研究，最终拿到 3 个不同的未认证远程代码执行；利用链用到信息泄露、认证绕过、命令注入、路径穿越、栈溢出与任意文件读写。
