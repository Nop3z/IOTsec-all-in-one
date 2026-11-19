---
title: "Fuzz'EMup: Leveraging EM Side-Channel Emanation to Guide Black-Box Embedded Firmware Fuzzing"
source: "arXiv"
url: http://arxiv.org/abs/2607.16487v1
published: 2026-07-17
fetched: 2026-11-19T12:07:27.218470+08:00
category: "FUZZ"
score: 0
keywords: ["side-channel", "fuzzing", "firmware"]
sha256: 2d4fb02e352b498e3654f07db8e90448c543a2b3097974da799ed9e1cfee7026
bytes: 1299
truncated: false
body_mode: meta
status: published
published_at: 2026-11-19T12:20:43.910308+08:00
---

# Fuzz'EMup: Leveraging EM Side-Channel Emanation to Guide Black-Box Embedded Firmware Fuzzing

> 来源：arXiv · 2026-07-17 · [原文](http://arxiv.org/abs/2607.16487v1)
> 归档用于安全研究参考；版权归原作者所有。

> ⚠️ 本条为「元数据 + 摘要」归档（论文/PDF/前端渲染页面），完整内容请读原文。

## 收录理由

- **核心**：固件既不能提取也不能插桩时，用**电磁侧信道泄漏**作为覆盖率反馈来引导黑盒 fuzz。
- **价值**：给“闭源固件怎么 fuzz”提供了新反馈通道，直接补上了 IoT 固件 fuzz 最缺的一环。
- **难度**：高 —— 需要稳定的 EM 采集与泄漏-覆盖映射。

As IoT and embedded devices proliferate across various domains, securing their firmware has become critical. Fuzzing offers a systematic approach to uncovering vulnerabilities in firmware, and coverage feedback can improve its effectiveness by guiding exploration. However, many devices make coverage information impossible to obtain by preventing firmware extraction, instrumentation, or accurate emulation; in such cases, testers are left with only inefficient black-box fuzzing. In this paper, we present an approach that leverages electromagnetic (EM) side-channel emanations to guide firmware fuzzing in purely black-box settings. However, turning raw EM measurements into reliable guidance is challenging: EM traces are noisy, and timing jitter causes corresponding features in different traces to shift in time. We address these challenges by combining frequency band selection based on the activity-to-idle signal contrast with dynamic time warping to align per-input traces and detect sustained divergence, while maintaining scalability by organizing executions in a tree structure based on their divergence times. We evaluate our approach on four real firmware targets and demonstrate that EM-derived feedback enhances path exploration, yielding higher code coverage than unguided fuzzing.
