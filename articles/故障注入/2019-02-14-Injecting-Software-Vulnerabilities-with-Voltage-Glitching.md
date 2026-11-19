---
title: "Injecting Software Vulnerabilities with Voltage Glitching"
source: "arXiv"
url: http://arxiv.org/abs/1903.08102v1
published: 2019-02-14
fetched: 2026-11-19T12:07:27.218470+08:00
category: "故障注入"
score: 0
keywords: ["fault-injection", "secure-boot"]
sha256: 317197da80f42bc1f265c101aae534194a5fa5171d2d49f9082e3d304fc3d395
bytes: 186
truncated: false
body_mode: meta
kind: theory
status: published
published_at: 2026-11-19T12:20:43.910308+08:00
---

# Injecting Software Vulnerabilities with Voltage Glitching

> 来源：arXiv · 2019-02-14 · [原文](http://arxiv.org/abs/1903.08102v1)
> 归档用于安全研究参考；版权归原作者所有。

> ⚠️ 本条为「元数据 + 摘要」归档（论文/PDF/前端渲染页面），完整内容请读原文。

## 收录理由

- **核心**：用电压毛刺制造 CMOS 时序违例，在一台经过安全加固的消费设备上拿到代码执行，并 dump 出安全启动 ROM。
- **价值**：把“毛刺 → 时序违例 → 跳过校验”这条因果链讲得很清楚，是入门电压毛刺的经典材料。
- **难度**：中高 —— 设备物理接触是前提，但所需设备便宜（ChipWhisperer 级别）。

We show how voltage glitching can cause timing violations in CMOS behavior. Then we attack a real, security hardened, consumer device to gain code execution and dump the secure boot ROM.
