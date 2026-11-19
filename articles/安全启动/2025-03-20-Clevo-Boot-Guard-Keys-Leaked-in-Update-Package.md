---
title: "Clevo Boot Guard Keys Leaked in Update Package"
source: "Binarly"
url: https://www.binarly.io/blog/clevo-boot-guard-keys-leaked-in-update-package
published: 2025-03-20
fetched: 2026-11-19T11:35:50.129835+08:00
category: "安全启动"
score: 4.0
keywords: ["uefi"]
sha256: d2fe734c180def0e758feb9d2cc925f6d5cd97b0a759f970065633f46f2e143d
bytes: 324
truncated: false
body_mode: link-only
status: published
published_at: 2026-11-19T12:20:43.910308+08:00
---

# Clevo Boot Guard Keys Leaked in Update Package

> 来源：Binarly · 2025-03-20 · [原文](https://www.binarly.io/blog/clevo-boot-guard-keys-leaked-in-update-package)
> 自动抓取快照，仅供安全研究参考；版权归原作者所有。

> ⚠️ 原文页面为前端渲染，正文未能完整抓取；此处仅保留摘要，请阅读原文。

## 收录理由

- **核心**：Clevo 在固件更新包里泄露了 Intel Boot Guard 密钥，等于把整条启动信任链的签名能力交了出去。
- **价值**：密钥管理事故比单个漏洞更致命：拿到 Boot Guard 密钥就能签出“合法”的恶意固件。
- **难度**：中 —— 拿到密钥后利用门槛不高，但发现过程需要固件包审计。

Over the past few years, the Binarly Research team has led the way in documenting security problems haunting the entire UEFI ecosystem. We presented our discoveries at major security conferences like OffensiveCon, Black Hat, LABScon and RE//verse to share data and collaborate with the industry to secure the UEFI ecosystem.
