---
title: "Silent Subversion: Sensor Spoofing Attacks via Supply Chain Implants in Satellite Systems"
source: "arXiv"
url: http://arxiv.org/abs/2603.10388v1
published: 2026-03-11
fetched: 2026-11-19T12:07:27.218470+08:00
category: "卫星安全"
score: 0
keywords: ["satellite", "spoofing"]
sha256: dabb0e131ddcb122b968fbd7205ff8c590dc0a81a2a256330baaf016f3f392e6
bytes: 1862
truncated: false
body_mode: meta
status: published
published_at: 2026-11-19T12:20:43.910308+08:00
---

# Silent Subversion: Sensor Spoofing Attacks via Supply Chain Implants in Satellite Systems

> 来源：arXiv · 2026-03-11 · [原文](http://arxiv.org/abs/2603.10388v1)
> 归档用于安全研究参考；版权归原作者所有。

> ⚠️ 本条为「元数据 + 摘要」归档（论文/PDF/前端渲染页面），完整内容请读原文。

## 收录理由

- **核心**：Silent Subversion：通过供应链植入对卫星传感器/遥测实施欺骗，使地面站收到伪造数据。
- **价值**：卫星无法现场维修，遥测被污染就等于任务失败；把“供应链植入 + 传感器欺骗”结合是很少见的威胁模型。
- **难度**：高 —— 需要航天器遥测链路与传感器知识。

Spoofing attacks are among the most destructive cyber threats to terrestrial systems, and they become even more dangerous in space, where satellites cannot be easily serviced, and operators depend on accurate telemetry to ensure mission success. When telemetry is compromised, entire spaceborne missions are placed at risk. Prior work on spoofing has largely focused on attacks from Earth, such as injecting falsified uplinks or overpowering downlinks with stronger radios. In contrast, onboard spoofing originating from within the satellite itself remains an underexplored and underanalyzed threat. This vector is particularly concerning given that modern satellites, especially small satellites, rely on modular architectures and globalized supply chains that reduce cost and accelerate development but also introduce hidden risks. This paper presents an end-to-end demonstration of an internal satellite spoofing attack delivered through a compromised vendor-supplied component implemented in NASA's NOS3 simulation environment. Our rogue Core Flight Software application passed integration and generated packets in the correct format and cadence that the COSMOS ground station accepted as legitimate. By undermining both onboard estimators and ground operator views, the attack directly threatens mission integrity and availability, as corrupted telemetry can bias navigation, conceal subsystem failures, and mislead operators into executing harmful maneuvers. These results expose component-level telemetry spoofing as an overlooked supply-chain vector distinct from jamming or external signal injection. We conclude by discussing practical countermeasures-including authenticated telemetry, component attestation, provenance tracking, and lightweight runtime monitoring-and highlight the trade-offs required to secure resource-constrained small satellites.
