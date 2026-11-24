---
title: "Signal K Server 认证链断在“读文件”这一步：一个 ../ 读走 JWT 密钥"
source: "先知社区"
url: https://xz.aliyun.com/news/93323
published: 2026-11-13
fetched: 2026-11-24T02:16:14.963Z
category: "协议安全"
score: 0
keywords: []
sha256: ffffb08bd7f5c0b1168d2c727ac3a313a6683d0508a4582cc7a44862681fa18f
bytes: 989
truncated: false
body_mode: notes
kind: practical
status: published
published_at: 2026-11-24T10:16:18.753705+08:00
---

# Signal K Server 认证链断在“读文件”这一步：一个 ../ 读走 JWT 密钥

> 来源：先知社区 · 2026-11-13 · [原文](https://xz.aliyun.com/news/93323)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：船载数据服务端 Signal K v2.33.0 的读接口把路径参数直接拼进文件路径，四层 `..%2F` 即可爬回配置根、读出 security.json 中的 JWT 密钥，进而伪造任意会话。
- **价值**：典型的“网关类 IoT 服务端”漏洞：NMEA 2000 网关、AIS、海图都汇聚于此，拿下它等于接管整条船上数据链；复现环境与版本差异也写得很清楚。
- **难度**：中 —— 路径穿越不难，难在理解它为什么在多个版本间仍存在。

Signal K Server（船用 NMEA/AIS 数据服务端）的路径穿越复现：v2.33.0 读接口未规范化路径，`..%2F` 四层即可读配置根下的 security.json，窃取 JWT 签名密钥后伪造会话。
