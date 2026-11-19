---
title: "JANUS: Denial-of-Service Attack Against Beam Hopping in LEO Satellite Networks"
source: "arXiv"
url: http://arxiv.org/abs/2609.19977v1
published: 2026-09-17
fetched: 2026-11-19T12:07:27.218470+08:00
category: "卫星安全"
score: 0
keywords: ["leo", "dos"]
sha256: f9f721b39052930d7c22c319655363e5dc0d6c734af03ccdedc8e8fb04f6e55b
bytes: 1571
truncated: false
body_mode: meta
status: published
published_at: 2026-11-19T12:20:43.910308+08:00
---

# JANUS: Denial-of-Service Attack Against Beam Hopping in LEO Satellite Networks

> 来源：arXiv · 2026-09-17 · [原文](http://arxiv.org/abs/2609.19977v1)
> 归档用于安全研究参考；版权归原作者所有。

> ⚠️ 本条为「元数据 + 摘要」归档（论文/PDF/前端渲染页面），完整内容请读原文。

## 收录理由

- **核心**：JANUS：针对 LEO 卫星“波束跳变（beam hopping）”调度机制的拒绝服务攻击。
- **价值**：低轨星座靠波束调度分配稀缺资源；攻击调度逻辑即可造成区域性服务降级，属于新型空间网络攻击面。
- **难度**：高 —— 需要理解波束调度与链路预算。

Low Earth orbit (LEO) satellite networks are increasingly used to provide global connectivity. However, each satellite has limited resources that need to be allocated according to demand, which varies geographically and over time. Beam hopping addresses this challenge by dividing a satellite's service area into geographic cells. Rather than illuminating every cell simultaneously, it dynamically assigns available beams to a selected subset based on demand. This reliance on observed traffic demand as an input to beam-selection decisions creates a new attack surface whose security implications have received little attention. In this paper, we present JANUS, a novel targeted denial-of-service attack against beam-hopping systems in LEO networks. We show that a small botnet of compromised terminals can inject legitimate user traffic into carefully selected non-victim cells to manipulate the beam-hopping scheduler's view of demand. This manipulation alters beam-allocation decisions and redirects service away from the targeted victim area. We evaluate JANUS across different system configurations, schedulers, attack horizons, and attacker-knowledge settings to characterize the attack's effectiveness, required resources, and resulting service disruption over time. Against a rank-based KMAX scheduler, JANUS achieves complete service denial for up to approximately 95% of evaluated victims. Against DRL, JANUS can exclude the victim from approximately 92% of scheduling decisions. Finally, we evaluate mitigation strategies that reduce the attack effectiveness.
