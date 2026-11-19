---
title: "Supporting Rowhammer research to protect the DRAM ecosystem"
source: "Google Security Blog"
url: http://security.googleblog.com/2025/09/supporting-rowhammer-research-to.html
published: 2025-09-16
fetched: 2026-11-19T12:02:12.663918+08:00
category: "芯片安全"
score: 8.3
keywords: ["rowhammer", "rowhammer", "dram"]
sha256: 47425472c89f6f26339b495963ba5cea640d70c68955a743c955354d09b608bf
bytes: 10951
truncated: false
body_mode: fulltext
status: published
published_at: 2026-11-19T12:20:43.910308+08:00
---

# Supporting Rowhammer research to protect the DRAM ecosystem

> 来源：Google Security Blog · 2025-09-16 · [原文](http://security.googleblog.com/2025/09/supporting-rowhammer-research-to.html)
> 自动抓取快照，仅供安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：Google 公开支持 Rowhammer 研究：从 DRAM 生态、攻击面到缓解措施的推进，并给出研究资源与硬件采购建议。
- **价值**：Rowhammer 是少数“纯软件触发硬件故障”的漏洞族；DRAM 型号、ECC 策略直接决定设备抗性，对做硬件选型的团队很实用。
- **难度**：中高 —— 需要精确的访存模式与平台知识，但不需要物理接触。

Security

# Supporting Rowhammer research to protect the DRAM ecosystem

Sep 15, 2025

 |

  Share Dropdown Menu

- x.com
- Facebook
- LinkedIn
- Mail
-

Daniel Moghimi

Share Dropdown Menu

Share

- x.com
- Facebook
- LinkedIn
- Mail
-

article text

Rowhammer is a complex class of vulnerabilities across the industry. It is a hardware vulnerability in DRAM where repeatedly accessing a row of memory can cause bit flips in adjacent rows, leading to data corruption. This can be exploited by attackers to gain unauthorized access to data, escalate privileges, or cause denial of service. Hardware vendors have deployed various mitigations, such as [ECC](https://www.jedec.org/category/keywords/ecc) and Target Row Refresh (TRR) for DDR5 memory, to mitigate Rowhammer and enhance DRAM reliability. However, the resilience of those mitigations against sophisticated attackers remains an open question.To address this gap and help the ecosystem with deploying robust defenses, Google has supported academic research and developed test platforms to analyze DDR5 memory. Our effort has led to the discovery of new attacks and a deeper understanding of Rowhammer on the current DRAM modules, helping to forge the way for further, stronger mitigations.

What is Rowhammer? [Rowhammer](https://dl.acm.org/doi/abs/10.1145/2678373.2665726) exploits a vulnerability in DRAM. DRAM cells store data as electrical charges, but these electric charges leak over time, causing data corruption. To prevent data loss, the memory controller periodically refreshes the cells. However, if a cell discharges before the refresh cycle, its stored bit may corrupt. Initially considered a reliability issue, it has been leveraged by security researchers to demonstrate privilege escalation attacks. By repeatedly accessing a memory row, an attacker can cause bit flips in neighboring rows. An adversary can exploit Rowhammer via:Reliably cause bit flips by repeatedly accessing adjacent DRAM rows.Coerce other applications or the OS into using these vulnerable memory pages.Target security-sensitive code or data to achieve privilege escalation.Or simply corrupt system’s memory to cause denial of service. Previous work has repeatedly demonstrated the possibility of such attacks from software [[Revisiting rowhammer](https://ieeexplore.ieee.org/abstract/document/9138944/), [Are we susceptible to rowhammer?](https://ieeexplore.ieee.org/abstract/document/9152654/), [Drammer](https://dl.acm.org/doi/abs/10.1145/2976749.2978406), [Flip feng shui](https://www.usenix.org/conference/usenixsecurity16/technical-sessions/presentation/razavi), [Jolt](https://eprint.iacr.org/2022/1669)]. As a result, defending against Rowhammer is required for secure isolation in multi-tenant environments like the cloud.

Rowhammer Mitigations The primary approach to mitigate Rowhammer is to detect which memory rows are being aggressively accessed and refreshing nearby rows before a bit flip occurs. TRR is a common example, which uses a number of counters to track accesses to a small number of rows adjacent to a potential victim row. If the access count for these aggressor rows reaches a certain threshold, the system issues a refresh to the victim row. TRR can be incorporated within the DRAM or in the host CPU.However, this mitigation is not foolproof. For example, the [TRRespass](https://ieeexplore.ieee.org/abstract/document/9152631) attack showed that by simultaneously hammering multiple, non-adjacent rows, TRR can be bypassed. Over the past couple of years, more sophisticated attacks [[Half-Double](https://www.usenix.org/conference/usenixsecurity22/presentation/kogler-half-double), [Blacksmith](https://www.research-collection.ethz.ch/bitstream/handle/20.500.11850/525008/4/2021275594.pdf)] have emerged, introducing more efficient attack patterns. In response, one of our efforts was to collaborate with [JEDEC](https://www.jedec.org/), external researchers, and experts to define the [PRAC](https://www.jedec.org/news/pressreleases/jedec-updates-jesd79-5c-ddr5-sdram-standard-elevating-performance-and-security) as a new mitigation that deterministically detects Rowhammer by tracking all memory rows. However, current systems equipped with DDR5 lack support for PRAC or other robust mitigations. As a result, they rely on probabilistic approaches such as ECC and enhanced TRR to reduce the risk. While these measures have mitigated older attacks, their overall effectiveness against new techniques was not fully understood until our recent [findings](https://comsec.ethz.ch/phoenix).

Challenges with Rowhammer Assessment Mitigating Rowhammer attacks involves making it difficult for an attacker to reliably cause bit flips from software. Therefore, for an effective mitigation, we have to understand how a determined adversary introduces memory accesses that bypass existing mitigations. Three key information components can help with such an analysis:How the improved TRR and in-DRAM ECC work.How memory access patterns from software translate into low-level DDR commands.(Optionally) How any mitigations (e.g., ECC or TRR) in the host processor work.The first step is particularly challenging and involves reverse-engineering the proprietary in-DRAM TRR mechanism, which varies significantly between different manufacturers and device models. This process requires the ability to issue precise DDR commands to DRAM and analyze its responses, which is difficult on an off-the-shelf system. Therefore, specialized test platforms are essential.The second and third steps involve analyzing the DDR traffic between the host processor and the DRAM. This can be done using an off-the-shelf interposer, a tool that sits between the processor and DRAM. A crucial part of this analysis is understanding how a live system translates software-level memory accesses into the DDR protocol.The third step, which involves analyzing host-side mitigations, is sometimes optional. For example, host-side ECC (Error Correcting Code) is enabled by default on servers, while host-side TRR has only been implemented in some CPUs.

Rowhammer testing platformsFor the first challenge, we partnered with Antmicro to develop two specialized, open-source FPGA-based Rowhammer test platforms. These platforms allow us to conduct in-depth testing on different types of DDR5 modules.[DDR5 RDIMM Platform:](https://antmicro.com/blog/2022/08/extending-the-open-source-rowhammer-testing-framework-to-ddr5/) A new DDR5 Tester board to meet the hardware requirements of Registered DIMM (RDIMM) memory, common in server computers.[SO-DIMM Platform:](https://antmicro.com/blog/2024/02/versatile-so-dimm-lpddr5-rowhammer-testing-platform/) A version that supports the standard SO-DIMM pinout compatible with off-the-shelf DDR5 SO-DIMM memory sticks, common in workstations and end-user devices.Antmicro designed and manufactured these [open-source platforms](https://github.com/antmicro/rowhammer-tester) and we worked closely with them, and researchers from ETH Zurich, to test the applicability of these platforms for analyzing off-the-shelf memory modules in RDIMM and SO-DIMM forms.

Antmicro DDR5 RDIMM FPGA test platform in action.

![Antmicro black development board with a Samsung RAM memory module installed, a small central cooling fan and connecting cables on top.](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEj_gVyZNNM5VDayDqZdu0oTgJlszT_po_A7Fku8jToBlYJsNyu3KxoX6KopaNiwm2VjxhlxoXGYVbVEbX_9fkVUh54zV5tfVn2ZrMi2bUZ8zveOYAbzVgfAg1KliqaNgdkp9-iYwAvoaHPqv2x1UallmAEC_D71V9B-pSdJn3yhxRo5HT24qBpftZJC2NIi/w446-h294/Screenshot%202025-09-12%20at%204.47.13%E2%80%AFPM.png)

Phoenix Attacks on DDR5In collaboration with researchers from ETH, we applied the new Rowhammer test platforms to evaluate the effectiveness of current in-DRAM DDR5 mitigations. Our findings, detailed in the recently co-authored "[Phoenix](https://comsec.ethz.ch/phoenix)” research paper, reveal that we successfully developed custom attack patterns capable of bypassing enhanced TRR (Target Row Refresh) defense on DDR5 memory. We were able to create a novel self-correcting refresh synchronization attack technique, which allowed us to perform the first-ever Rowhammer privilege escalation exploit on a standard, production-grade desktop system equipped with DDR5 memory. While this experiment was conducted on an off-the-shelf workstation equipped with recent AMD Zen processors and SK Hynix DDR5 memory, we continue to investigate the applicability of our findings to other hardware configurations.Lessons learned We showed that current mitigations for Rowhammer attacks are not sufficient, and the issue remains a widespread problem across the industry. They do make it more difficult “but not impossible” to carry out attacks, since an attacker needs an in-depth understanding of the specific memory subsystem architecture they wish to target.Current mitigations based on TRR and ECC rely on probabilistic countermeasures that have insufficient entropy. Once an analyst understands how TRR operates, they can craft specific memory access patterns to bypass it. Furthermore, current ECC schemes were not designed as a security measure and are therefore incapable of reliably detecting errors.Memory encryption is an alternative countermeasure for Rowhammer. However, our current assessment is that without cryptographic integrity, it offers no valuable defense against Rowhammer. More research is needed to develop viable, practical encryption and integrity solutions.Path forwardGoogle has been a leader in JEDEC standardization efforts, for instance with [PRAC](https://google.com/url?q=https://www.jedec.org/news/pressreleases/jedec-updates-jesd79-5c-ddr5-sdram-standard-elevating-performance-and-security&sa=D&source=docs&ust=1757029496975020&usg=AOvVaw1AVBpnQbJ_M_QYxPq8bfE3), a fully approved standard to be supported in upcoming versions of [DDR5](https://www.jedec.org/news/pressreleases/jedec-updates-jesd79-5c-ddr5-sdram-standard-elevating-performance-and-security)/[LPDDR6](https://www.jedec.org/news/pressreleases/jedec%C2%AE-releases-new-lpddr6-standard-enhance-mobile-and-ai-memory-performance). It works by accurately counting the number of times a DRAM wordline is activated and alerts the system if an excessive number of activations is detected. This close coordination between the DRAM and the system gives PRAC a reliable way to address Rowhammer. In the meantime, we continue to evaluate and improve other countermeasures to ensure our workloads are resilient against Rowhammer. We collaborate with our academic and industry partners to improve analysis techniques and test platforms, and to share our findings with the broader ecosystem.Want to learn more?“Phoenix: Rowhammer Attacks on DDR5 with Self-Correcting Synchronization” will be presented at [IEEE Security & Privacy 2026](https://www.ieee-security.org/TC/SP2026/) in San Francisco, CA (MAY 18-21, 2026).

Posted in:
