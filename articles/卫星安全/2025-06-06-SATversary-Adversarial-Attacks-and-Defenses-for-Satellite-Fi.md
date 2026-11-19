---
title: "SATversary: Adversarial Attacks and Defenses for Satellite Fingerprinting"
source: "arXiv"
url: http://arxiv.org/abs/2506.06119v2
published: 2025-06-06
fetched: 2026-11-19T12:07:27.218470+08:00
category: "卫星安全"
score: 0
keywords: ["fingerprinting", "adversarial"]
sha256: cc105c97db372f6a34bfdb63690aeb2281926a4e93f0e4d382fcd5f53e662c68
bytes: 1907
truncated: false
body_mode: meta
kind: theory
status: published
published_at: 2026-11-19T12:20:43.910308+08:00
---

# SATversary: Adversarial Attacks and Defenses for Satellite Fingerprinting

> 来源：arXiv · 2025-06-06 · [原文](http://arxiv.org/abs/2506.06119v2)
> 归档用于安全研究参考；版权归原作者所有。

> ⚠️ 本条为「元数据 + 摘要」归档（论文/PDF/前端渲染页面），完整内容请读原文。

## 收录理由

- **核心**：SATversary：针对“卫星发射源指纹识别”这类物理层认证的对抗攻击与防御。
- **价值**：指纹识别被当作卫星链路的新防线，这篇说明基于 ML 的指纹同样可被对抗样本欺骗。
- **难度**：高 —— 需要物理层信号与 ML 攻防。

Due to the increasing threat of attacks on satellite systems, novel countermeasures have been developed to provide additional security. Among these, there has been a particular interest in transmitter fingerprinting, which authenticates transmitters by looking at characteristics expressed in the physical layer signal. These systems rely heavily upon statistical methods and machine learning, and are therefore vulnerable to a range of attacks. The severity of this threat in a fingerprinting context is currently not well understood. In this paper we evaluate a range of attacks against satellite fingerprinting, building on previous works by looking at attacks optimized to target the fingerprinting system for maximal impact. We design optimized jamming, dataset poisoning, and spoofing attacks, evaluating them in the real world against the SatIQ fingerprinting system designed to authenticate Iridium transmitters, and using a wireless channel emulator to achieve realistic channel conditions. We show that an optimized jamming signal can cause a 50% error rate with attacker-to-victim ratios as low as -30dB (far less power than traditional jamming techniques), and demonstrate successful spoofing attacks, with an attacker successfully removing their own transmitter's fingerprint from messages. We also present a viable dataset poisoning attack, enabling persistent message spoofing by altering stored data to include the fingerprint of the attacker's transmitter. Finally, we show that a model trained to optimize spoofing attacks can also be used to detect spoofing and replay attacks, even when it has never seen the attacker's transmitter before. This technique works even when the training dataset includes only a single transmitter, enabling fingerprinting to be used to protect small constellations and even individual satellites, providing additional protection where it is needed the most.
