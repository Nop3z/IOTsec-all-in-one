---
title: "Android’s pKVM Becomes First Globally Certified Software to Achieve Prestigious SESIP Level 5 Security Certification"
source: "Google Security Blog"
url: http://security.googleblog.com/2025/08/Android-pKVM-Certified-SESIP-Level-5.html
published: 2025-08-13
fetched: 2026-11-19T12:02:12.663918+08:00
category: "杂项"
score: 6.3
keywords: ["hypervisor", "iot", "hypervisor"]
sha256: 5d06eeef08903911339c25116860a951ed3d4f6cd60e7242ad633648b295277b
bytes: 3414
truncated: false
body_mode: fulltext
status: published
published_at: 2026-11-19T12:20:43.910308+08:00
---

# Android’s pKVM Becomes First Globally Certified Software to Achieve Prestigious SESIP Level 5 Security Certification

> 来源：Google Security Blog · 2025-08-13 · [原文](http://security.googleblog.com/2025/08/Android-pKVM-Certified-SESIP-Level-5.html)
> 自动抓取快照，仅供安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：Android 的 pKVM（受保护的 KVM）成为首个拿到 SESIP Level 5 认证的软件组件，说明基于虚拟化的隔离正在进入移动信任根。
- **价值**：对评估“设备级隔离”是否可信很有用：认证范围、威胁模型与残留风险都写清楚了。
- **难度**：中 —— 认证与架构说明，偏防御。

Android Security

# Android’s pKVM Becomes First Globally Certified Software to Achieve Prestigious SESIP Level 5 Security Certification

Aug 12, 2025

 |

  Share Dropdown Menu

- x.com
- Facebook
- LinkedIn
- Mail
-

Dave Kleidermacher

VP Engineering, Android Security & Privacy

Share Dropdown Menu

Share

- x.com
- Facebook
- LinkedIn
- Mail
-

article text

Today marks a watershed moment and new benchmark for open-source security and the future of consumer electronics. Google is proud to announce that protected KVM (pKVM), the hypervisor that powers the Android Virtualization Framework, has officially achieved [SESIP Level 5 certification](https://trustcb.com/download/?wpdmdl=5353). This makes pKVM the first software security system designed for large-scale deployment in consumer electronics to meet this assurance bar.
Supporting Next-Gen Android FeaturesThe implications for the future of secure mobile technology are profound. With this level of security assurance, Android is now positioned to securely support the next generation of high-criticality isolated workloads. This includes vital features, such as on-device AI workloads that can operate on ultra-personalized data, with the highest assurances of privacy and integrity.This certification required a hands-on evaluation by [Dekra](https://www.dekra.com/en/product-testing-and-certification-programs/), a globally recognized cybersecurity certification lab, which conducted an evaluation against the [TrustCB SESIP scheme](https://trustcb.com/iot/sesip/), compliant to [EN-17927](https://www.nen.nl/en/nen-en-17927-2023-en-317686). Achieving Security Evaluation Standard for IoT Platforms (SESIP) Level 5 is a landmark because it incorporates AVA_VAN.5, the highest level of vulnerability analysis and penetration testing under the ISO 15408 (Common Criteria) standard. A system certified to this level has been evaluated to be resistant to highly skilled, knowledgeable, well-motivated, and well-funded attackers who may have insider knowledge and access.This certification is the cornerstone of the next-generation of Android’s multi-layered security strategy. Many of the TEEs (Trusted Execution Environments) used in the industry have not been formally certified or have only achieved lower levels of security assurance. This inconsistency creates a challenge for developers looking to build highly critical applications that require a robust and verifiable level of security. The certified pKVM changes this paradigm entirely. It provides a single, open-source, and exceptionally high-quality firmware base that all device manufacturers can build upon.Looking ahead, Android device manufacturers will be required to use isolation technology that meets this same level of security for various security operations that the device relies on. Protected KVM ensures that every user can benefit from a consistent, transparent, and verifiably secure foundation.
A Collaborative EffortThis achievement represents just one important aspect of the immense, multi-year dedication from the Linux and KVM developer communities and multiple engineering teams at Google developing pKVM and [AVF](https://source.android.com/docs/core/virtualization). We look forward to seeing the open-source community and Android ecosystem continue to build on this foundation, delivering a new era of high-assurance mobile technology for users.

Posted in:
