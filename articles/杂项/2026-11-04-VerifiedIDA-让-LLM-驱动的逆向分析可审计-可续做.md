---
title: "VerifiedIDA：让 LLM 驱动的逆向分析可审计、可续做"
source: "SentinelOne Labs"
url: https://www.sentinelone.com/labs/verifiedida-making-llm-driven-reverse-engineering-inspectable-continuable-and-reproducible/
published: 2026-11-04
fetched: 2026-11-24T02:16:14.965Z
category: "杂项"
score: 0
keywords: []
sha256: 0fa72f2ae1518d25cfed7960f669b80b3fc2e540c2254849fe154a8e23785bcc
bytes: 969
truncated: false
body_mode: notes
kind: practical
status: published
published_at: 2026-11-24T10:16:18.753705+08:00
---

# VerifiedIDA：让 LLM 驱动的逆向分析可审计、可续做

> 来源：SentinelOne Labs · 2026-11-04 · [原文](https://www.sentinelone.com/labs/verifiedida-making-llm-driven-reverse-engineering-inspectable-continuable-and-reproducible/)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：用 LLM + IDA 做逆向时，把每一步结论绑定到可复核的证据（反编译片段、交叉引用），使分析过程可审计、可续做、可复现。
- **价值**：固件逆向正在快速被 AI 辅助工具改造，而“结论不可信/不可复现”是最大障碍；这套方法是把 LLM 逆向落地的关键一环。
- **难度**：中 —— 工具链集成，理解逆向流程即可上手。

VerifiedIDA 方法：让 LLM 驱动的二进制逆向分析可检查、可中断续做、可复现——每个结论都关联到 IDA 中的具体证据，避免“AI 说这里有漏洞”式黑箱结论。
