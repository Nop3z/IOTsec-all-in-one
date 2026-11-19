---
title: "PowerFuzz: Power-Based Black-Box Firmware Fuzzing"
source: "arXiv"
url: http://arxiv.org/abs/2606.24692v1
published: 2026-06-23
fetched: 2026-11-19T12:07:27.218470+08:00
category: "FUZZ"
score: 0
keywords: ["side-channel", "fuzzing", "power"]
sha256: b400a112315cb97bb7cd1dea386b53400419d78601ff2814575e71386780145b
bytes: 1405
truncated: false
body_mode: meta
kind: theory
status: published
published_at: 2026-11-19T12:20:43.910308+08:00
---

# PowerFuzz: Power-Based Black-Box Firmware Fuzzing

> 来源：arXiv · 2026-06-23 · [原文](http://arxiv.org/abs/2606.24692v1)
> 归档用于安全研究参考；版权归原作者所有。

> ⚠️ 本条为「元数据 + 摘要」归档（论文/PDF/前端渲染页面），完整内容请读原文。

## 收录理由

- **核心**：用功耗信号作为黑盒固件的覆盖率代理，实现 PowerFuzz——无需固件、无需调试接口即可做有反馈的 fuzz。
- **价值**：与 Fuzz'EMup 互补（功耗 vs 电磁），说明“物理侧信道可以当覆盖率用”这条路可行。
- **难度**：高 —— 功耗采集的噪声与对齐是主要难点。

Fuzzing is widely used for software and hardware verification, offering an effective alternative to random testing. While gray-box fuzzers benefit from full visibility into the system under test and can leverage execution feedback such as branch coverage, these approaches are not applicable when verifying systems whose firmware or binaries are not publicly available. In such scenarios, obtaining coverage information for guiding the fuzzer becomes infeasible. In this paper, we introduce PowerFuzz, a statistical black-box fuzzing framework that leverages power side-channel measurements as a substitute for binary instrumentation, requiring no internal visibility into the target firmware. A central challenge in black-box firmware fuzzing is determining the executed branches during test execution. To address this challenge, we use power traces to identify branches utilizing a sliding window followed by a growing window full-trace correlation method. This approach also enables the construction of a high-level control-flow graph of the black-box firmware, which we utilize to drive the fuzzer to unexplored execution paths. Extensive evaluation using three embedded hardware platforms and ten firmware benchmarks demonstrates that PowerFuzz can provide branch coverage comparable (within 13.5%) to gray-box fuzzers while significantly outperforming (up to 22%) state-of-the-art black-box fuzzers.
