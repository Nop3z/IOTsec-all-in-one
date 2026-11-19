# IoT Security All-in-One

IoT / 固件 / 硬件 / 底层安全研究资料库。只收**有研究价值**的内容：**攻击角度新颖**，或**利用难度极高**。
每周自动更新，正文快照归档在 [articles/INDEX.md](articles/INDEX.md)。

## 索引

<!-- INDEX:START -->

**设备与场景**

| 板块 | 篇 | 板块 | 篇 | 板块 | 篇 |
|:--|--:|:--|--:|:--|--:|
| [Openwrt](#openwrt) | 4 | [摄像头](#摄像头) | 6 | [无人机](#无人机) | 19 |
| [车机](#车机) | 6 | [充电桩](#充电桩) | 7 | [基站](#基站) | 3 |
| [防火墙](#防火墙) | 22 | [卫星安全](#卫星安全) | 10 | [打印机](#打印机) | 4 |
| [智能家居](#智能家居) | 7 | [机器人](#机器人) | 1 | [芯片安全](#芯片安全) | 14 |
| [RFID](#rfid) | 5 | [WIFI安全](#wifi安全) | 1 | [协议安全](#协议安全) | 3 |
| [硬件钱包](#硬件钱包) | 3 | [FUZZ](#fuzz) | 4 | | |

**技术专题**

| 板块 | 篇 | 板块 | 篇 |
|:--|--:|:--|--:|
| [安全启动](#安全启动) | 22 | [固件解密](#固件解密) | 15 |
| [故障注入](#故障注入) | 38 | [绕过ASLR](#绕过aslr) | 5 |

**资源与归档**

| 板块 | 篇 | 板块 | 篇 | 板块 | 篇 |
|:--|--:|:--|--:|:--|--:|
| [固件下载](#固件下载) | 18 | [虚拟机镜像](#虚拟机镜像) | 0 | [杂项](#杂项) | 19 |
| [文章快照](articles/INDEX.md) | 121 | [更新日志](#更新日志) | - | [收录标准](#收录标准) | - |

<!-- INDEX:END -->

## 最新归档

<!-- LATEST:START -->
| 日期 | 板块 | 文章 |
|:--|:--|:--|
| 2026-11-14 | 车机 | [MC9S12/HCS12 复位安全评估窗口毛刺：解锁 BDM 读全片 flash](articles/车机/2026-11-14-MC9S12-HCS12-复位安全评估窗口毛刺-解锁-BDM-读全片-flash.md) |
| 2026-11-14 | 芯片安全 | [GA100 数据中心 GPU PWMVID 电压毛刺实验台](articles/芯片安全/2026-11-14-GA100-数据中心-GPU-PWMVID-电压毛刺实验台.md) |
| 2026-11-14 | 硬件钱包 | [STM32F2/F4 故障注入：EMFI/VFI 双档 RDP2→RDP1 + FPB 两毛刺读全片 flash](articles/硬件钱包/2026-11-14-STM32F2-F4-故障注入-EMFI-VFI-双档-RDP2-RDP1-FPB-两毛刺读全片-flash.md) |
| 2026-11-14 | 智能家居 | [Apple AirTag（nRF52832）电压毛刺解锁 APPROTECT 并转储固件](articles/智能家居/2026-11-14-Apple-AirTag-nRF52832-电压毛刺解锁-APPROTECT-并转储固件.md) |
| 2026-11-14 | 故障注入 | [把故障注入仿真塞进开发流（Ledger Donjon：rust_fi + Rainbow + CI）](articles/故障注入/2026-11-14-把故障注入仿真塞进开发流-Ledger-Donjon-rust_fi-Rainbow-CI.md) |
| 2026-11-14 | 故障注入 | [ot-sca：OpenTitan 官方 SCA + 故障注入评估框架](articles/故障注入/2026-11-14-ot-sca-OpenTitan-官方-SCA-故障注入评估框架.md) |
| 2026-11-14 | 故障注入 | [findus / fault-injection-library：Pico Glitcher 软件框架 + 12 个 MCU 靶项目](articles/故障注入/2026-11-14-findus-fault-injection-library-Pico-Glitcher-软件框架-12-个-MCU-靶.md) |
| 2026-11-14 | 故障注入 | [SiliconToaster：开源 0–1000V 电磁故障注入发生器（Ledger Donjon）](articles/故障注入/2026-11-14-SiliconToaster-开源-0-1000V-电磁故障注入发生器-Ledger-Donjon.md) |
<!-- LATEST:END -->

全部归档见 [articles/INDEX.md](articles/INDEX.md)。

## Openwrt

> 路由器与固件层面的漏洞挖掘、Root 与固件升级链

- [Ruijie 漏洞分析](https://bbs.kanxue.com/thread-277386.htm)
- [小米路由器 Root 技术研究](https://blog.thalium.re/posts/rooting-xiaomi-wifi-routers/)
- [浅析 LuCI 系统的漏洞挖掘技术](https://mp.weixin.qq.com/s/kBOfQhNHZCFNNzu_euLIgA)
- [Vulnerability REsearch using VulHunt](articles/Openwrt/2026-02-20-Vulnerability-REsearch-using-VulHunt.md) · [原文](https://www.binarly.io/blog/vulnerability-research-using-vulhunt)

## 摄像头

> IPC / NVR 类设备的认证绕过与 RCE

- [TPLink-Tapo CVE-2021-4045](https://github.com/hacefresko/CVE-2021-4045)
- [TPLink-Tapo 漏洞分析](https://pwner.gg/blog/2024-01-05-tp-link-tapo-c100)
- [TPLink-Tapo C2000](https://drmnsamoliu.github.io/index.html)
- [TP-Link Tapo C200 未授权 RCE](https://www.hacefresko.com/posts/tp-link-tapo-c200-unauthenticated-rce)
- [Exploiting a Chinese camera for fun（CVE-2024-48214）](https://medium.com/%40shenhavmor/exploiting-a-chinese-camera-for-fun-cve-2024-48214-2d56848870c2)
- [TPLink-Tapo C310](https://sizeof.cat/post/tp-link-tapo-c310-camera/)

## 无人机

> 固件、协议、APP 与遥控链路

- [无人机安全简介](https://payatu.com/blog/flying-securely-an-introduction-to-drone-security/)
- [DJI Mavic 3 固件研究（Part 1）](https://www.nozominetworks.com/blog/dji-mavic-3-drone-research-part-1-firmware-analysis)
- [DJI Mavic 3 固件研究（Part 2）](https://www.nozominetworks.com/blog/dji-mavic-3-drone-research-part-2-vulnerability-analysis)
- [DJI RM500 遥控器提权漏洞](https://icanhack.nl/blog/dji-rm500-privilege-escalation/)
- [针对 DJI 无人机的安全研究（NDSS 2023）](https://www.ndss-symposium.org/wp-content/uploads/2023/02/ndss2023_f217_paper.pdf)
- [无人机常见攻击方式](https://www.anquanke.com/post/id/82761)
- [DroneSploit 渗透测试框架](https://github.com/dhondta/dronesploit)
- [通过 Wireshark 解析无人机数据包](https://hackernoon.com/lang/zh/%E5%A6%82%E4%BD%95%E4%BD%BF%E7%94%A8%E6%95%B0%E6%8D%AE%E5%8C%85%E8%A7%A3%E5%89%96%E4%BD%BF%E7%94%A8-wireshark-%E5%AF%B9%E6%97%A0%E4%BA%BA%E6%9C%BA%E8%BF%9B%E8%A1%8C%E9%80%86%E5%90%91%E5%B7%A5%E7%A8%8B)
- [绿盟 2023 无人机安全报告](https://book.yunzhan365.com/tkgd/ghoo/mobile/index.html)
- [绿盟 2024 无人机安全报告](https://book.yunzhan365.com/tkgd/gmpv/mobile/index.html)
- [某无人机APP逆向分析](https://v5le0n9.github.io/posts/ac4cb042.html)
- [某无人机漏洞挖掘](https://v5le0n9.github.io/posts/8a5081f6.html)
- [315晚会报道的无人机是怎么被劫持的？](https://security.tencent.com/index.php/blog/msg/103)
- [几种小型UAV安全漏洞研究](https://ndxb.imu.edu.cn/__local/8/16/3D/02E8C65FA6BC939DC5776397BCE_8849FAC7_67446D.pdf)
- [针对基于mavlink协议的无人机进行攻击](https://mp.weixin.qq.com/s/HfFqgQcgOyA_rmb3UFXhww)
- [无人机mavlink中间人攻击](https://mp.weixin.qq.com/s/gfzdWSlzBkc14fvG1n36Cg)
- [无人机MAVLINK协议安全剖析](https://mp.weixin.qq.com/s/WEivJpxTBSVcmAa5QvvDxQ)
- [攻防速写｜击穿DJI大疆控制设备的致命漏洞](https://www.ctfiot.com/232771.html)
- [基于模糊测试的小型多旋翼无人机漏洞分析](https://xz.aliyun.com/course-view?id=11)

## 车机

> 车机、ECU、CAN 总线与整车攻击面

- [大众 MMX 车机漏洞分析](https://sector7.computest.nl/post/2018-07-mib/)
- [腾讯科恩实验室对奔驰梅赛德斯车机研究](https://keenlab.tencent.com/en/whitepapers/Mercedes_Benz_Security_Research_Report_Final.pdf)
- [Black Hat Asia 2025：日产 Leaf 远程利用](https://i.blackhat.com/Asia-25/Asia-25-Evdokimov-Remote-Exploitation-of-Nissan-Leaf.pdf)
- [Automotive HSMs - Architectural Challenges and Security Implications](articles/车机/2026-08-25-Automotive-HSMs-Architectural-Challenges-and-Security-Implic.md) · [原文](http://arxiv.org/abs/2608.25216v1)
- [Mercedes 防盗器 ECU 过压毛刺：短暂恢复被熔断的 JTAG](articles/车机/2025-06-01-Mercedes-防盗器-ECU-过压毛刺-短暂恢复被熔断的-JTAG.md) · [原文](https://troopers.de/troopers25/talks/et37yq/)
- [MC9S12/HCS12 复位安全评估窗口毛刺：解锁 BDM 读全片 flash](articles/车机/2026-11-14-MC9S12-HCS12-复位安全评估窗口毛刺-解锁-BDM-读全片-flash.md) · [原文](https://github.com/wichers/mc9s12-voltage-glitch-attack)

## 充电桩

> EVSE 与 OCPP 相关研究

- [从蓝牙入侵充电桩](https://www.youtube.com/watch?v=8gNhfR1YZGA)
- [破解 Autel MaxiCharger](https://sector7.computest.nl/post/2024-08-pwn2own-automotive-autel-maxicharger/)
- [CHARX 充电桩漏洞分析（Part 1）](https://blog.ret2.io/2024/07/17/pwn2own-auto-2024-charx-bugs/)
- [CHARX 充电桩漏洞利用（Part 2）](https://blog.ret2.io/2024/07/24/pwn2own-auto-2024-charx-exploit/)
- [Pwn2Own Automotive 2024: Hacking the Autel MaxiCharger](articles/充电桩/2024-09-05-Pwn2Own-Automotive-2024-Hacking-the-Autel-MaxiCharger.md) · [原文](https://defion.security/en/research-labs/pwn2own-automotive-2024-hacking-the-autel-maxicharger/)
- [Pwn2Own Automotive 2024: Hacking the JuiceBox 40](articles/充电桩/2024-08-29-Pwn2Own-Automotive-2024-Hacking-the-JuiceBox-40.md) · [原文](https://defion.security/en/research-labs/pwn2own-automotive-2024-hacking-the-juicebox-40/)
- [Pwn2Own Automotive 2024: Hacking the ChargePoint Home Flex (and their cloud...)](articles/充电桩/2024-08-08-Pwn2Own-Automotive-2024-Hacking-the-ChargePoint-Home-Flex-an.md) · [原文](https://defion.security/en/research-labs/pwn2own-automotive-2024-hacking-the-chargepoint-home-flex-and-their-cloud/)

## 基站

> 4G/5G 基站与核心网

- [NextEPC 漏洞分析](https://cellularsecurity.org/ransacked)
- [使用用户设备对 5G 基站进行攻击](https://www.trendmicro.com/en_gb/research/23/i/attacks-on-5g-infrastructure-from-users-devices.html)
- [Bringing Rust to the Pixel Baseband](articles/基站/2026-04-10-Bringing-Rust-to-the-Pixel-Baseband.md) · [原文](http://security.googleblog.com/2026/04/bringing-rust-to-pixel-baseband.html)

## 防火墙

> VPN / 防火墙 / 安全设备

- [FortiOS 关键漏洞分析（2025）](https://www.akamai.com/blog/security-research/2025-february-fortinet-critical-vulnerabilities)
- [Ivanti CVE-2025-0282 RCE 利用分析](https://labs.watchtowr.com/exploitation-walkthrough-and-techniques-ivanti-connect-secure-rce-cve-2025-0282/)
- [PAN-OS 完整攻击链分析](https://www.horizon3.ai/attack-research/disclosures/palo-alto-expedition-from-n-day-to-full-compromise/)
- [Palo Alto路径混淆认证绕过漏洞](https://slcyber.io/blog/nginx-apache-path-confusion-to-auth-bypass-in-pan-os/)
- [Palo Alto 分析报告](https://mp.weixin.qq.com/s?__biz=MjM5NTc2MDYxMw==&mid=2458589341&idx=1&sn=c57db95a9d3d5f4d3d5993b9e4d2398e&chksm=b058fa0e9bed1058d3630a5e1eb6e07af731a0dd15a60c93ffc6f651afe5d8d410438491fea3&mpshare=1&scene=2&srcid=0208LPPhzgrDbMTj76w5Y3S0&sharer_shareinfo=d134b3645062ee3043dfb811bdfe2842&sharer_shareinfo_first=d134b3645062ee3043dfb811bdfe2842#rd)
- [Check Point CVE-2024-24919 分析](https://labs.watchtowr.com/check-point-wrong-check-point-cve-2024-24919/)
- [CVE-2025-22457](https://attackerkb.com/topics/0ybGQIkHzR/cve-2025-22457/rapid7-analysis)
- [Pre-Auth RCE in Zyxel GS1900 Exploited in the Wild as a Zero-Day](articles/防火墙/2026-11-03-Pre-Auth-RCE-in-Zyxel-GS1900-Exploited-in-the-Wild-as-a-Zero.md) · [原文](https://www.binarly.io/blog/zyxel-gs1900-rce-cve-2026-107441)
- [Additional Ivanti Connect Secure zero-days exploited in the wild (CVE-2026-111357, CVE-2026-118527)](articles/防火墙/2026-11-02-Additional-Ivanti-Connect-Secure-zero-days-exploited-in-the.md) · [原文](https://www.rapid7.com/blog/post/etr-additional-ivanti-connect-secure-zero-days-exploited-in-the-wild-cve-2026-111357-cve-2026-118527)
- [Inside KeyDrift: Analyzing historical UAT-11473 activity on Cisco SD-WAN](articles/防火墙/2026-10-29-Inside-KeyDrift-Analyzing-historical-UAT-11473-activity-on-C.md) · [原文](https://blog.talosintelligence.com/uat-11473-keydrift/)
- [Barracuda Networks is your new best friend (Barracuda Email Security Gateway Pre-Auth Remote Root RCE CVE-2026-116606 / CVE-2026-111560)](articles/防火墙/2026-11-06-Barracuda-Networks-is-your-new-best-friend-Barracuda-Email-S.md) · [原文](https://labs.watchtowr.com/barracuda-networks-is-your-new-best-friend-barracuda-email-security-gateway-pre-auth-remote-root-rce-cve-2026-116606-cve-2026-111560/)
- [PHP2Shell Exploitation on Check Point Gateway](articles/防火墙/2026-11-12-PHP2Shell-Exploitation-on-Check-Point-Gateway.md) · [原文](https://research.checkpoint.com/2026/php2shell-exploitation-on-check-point-gateway/)
- [Active Exploitation of May 2026 PAN-OS CVE-2026-0257 (Updated October 20)](articles/防火墙/2026-10-21-Active-Exploitation-of-May-2026-PAN-OS-CVE-2026-0257-Updated.md) · [原文](https://unit42.paloaltonetworks.com/active-exploitation-of-pan-os-cve-2026-0257/)
- [Here We Go Again (Citrix NetScaler DTLS Preauth Memory Overflow CVE-2026-88772)](articles/防火墙/2026-09-29-Here-We-Go-Again-Citrix-NetScaler-DTLS-Preauth-Memory-Overfl.md) · [原文](https://labs.watchtowr.com/here-we-go-again-citrix-netscaler-dtls-preauth-memory-overflow-cve-2026-88772/)
- [Oh Look, The Foot Gun Went Off Again (Citrix NetScaler PreAuth Command Injection CVE-2026-88771)](articles/防火墙/2026-09-28-Oh-Look-The-Foot-Gun-Went-Off-Again-Citrix-NetScaler-PreAuth.md) · [原文](https://labs.watchtowr.com/oh-look-the-foot-gun-went-off-again-citrix-netscaler-preauth-command-injection-cve-2026-88771/)
- [Is This A Joke? In The Auth Header? (F5 BIG-IP UnAuth Heap-Overflow to RCE CVE-2026-94127)](articles/防火墙/2026-09-24-Is-This-A-Joke-In-The-Auth-Header-F5-BIG-IP-UnAuth-Heap-Over.md) · [原文](https://labs.watchtowr.com/is-this-a-joke-in-the-auth-header-f5-big-ip-unauth-heap-overflow-to-rce-cve-2026-94127/)
- [You’re Back In The Room (Citrix NetScaler Pre-Auth RCE CVE-2026-8452(?))](articles/防火墙/2026-08-14-You-re-Back-In-The-Room-Citrix-NetScaler-Pre-Auth-RCE-CVE-20.md) · [原文](https://labs.watchtowr.com/youre-back-in-the-room-citrix-netscaler-pre-auth-rce-cve-2026-8452/)
- [CitrixBleed To Infinity And Beyond (Citrix NetScaler Pre-Auth Memory Overread CVE-2026-8451)](articles/防火墙/2026-07-01-CitrixBleed-To-Infinity-And-Beyond-Citrix-NetScaler-Pre-Auth.md) · [原文](https://labs.watchtowr.com/citrixbleed-to-infinity-and-beyond-citrix-netscaler-pre-auth-memory-overread-cve-2026-8451/)
- [Marking Your Own Homework (Check Point Remote Access VPN IKEv1 Authentication Bypass CVE-2026-50751)](articles/防火墙/2026-06-12-Marking-Your-Own-Homework-Check-Point-Remote-Access-VPN-IKEv.md) · [原文](https://labs.watchtowr.com/marking-your-own-homework-check-point-remote-access-vpn-ikev1-authentication-bypass-cve-2026-50751/)
- [More Evidence That Words Don't Mean What We Thought They Meant (Ivanti Sentry Pre-Auth OS Command Injection CVE-2026-10520)](articles/防火墙/2026-06-10-More-Evidence-That-Words-Don-t-Mean-What-We-Thought-They-Mea.md) · [原文](https://labs.watchtowr.com/more-evidence-that-words-dont-mean-what-we-thought-they-meant-ivanti-sentry-pre-auth-os-command-injection-cve-2026-10520/)
- [Ruckus Unleashed: Multiple vulnerabilities exploited](articles/防火墙/2025-07-21-Ruckus-Unleashed-Multiple-vulnerabilities-exploited.md) · [原文](https://defion.security/en/research-labs/ruckus-unleashed-multiple-vulnerabilities-exploited/)
- [Pull the Plug: FIRESTARTER Survives Patches, Reboots, and Your Incident Response Plan](articles/防火墙/2026-05-07-Pull-the-Plug-FIRESTARTER-Survives-Patches-Reboots-and-Your.md) · [原文](https://eclypsium.com/blog/firestarter-cisco-firewall-backdoor-survives-patches/)

## 卫星安全

> 卫星终端与 GNSS

- [攻防速写｜我们拆了一台Starlink星链终端](https://mp.weixin.qq.com/s/QsLyWHp1zb89Gq7aXgWZwA)
- [Glitched on Earth by Humans: A Black-Box Security Evaluation of the SpaceX Starlink User Terminal](articles/卫星安全/2022-08-11-Glitched-on-Earth-by-Humans-A-Black-Box-Security-Evaluation.md) · [原文](https://i.blackhat.com/USA-22/Wednesday/US-22-Wouters-Glitched-On-Earth.pdf)
- [SATCOM Terminals: Hacking by Air, Sea, and Land](articles/卫星安全/2014-08-06-SATCOM-Terminals-Hacking-by-Air-Sea-and-Land.md) · [原文](https://www.blackhat.com/docs/us-14/materials/us-14-Santamarta-SATCOM-Terminals-Hacking-By-Air-Sea-And-Land-WP.pdf)
- [SpyChain: Multi-Vector Supply Chain Attacks on Small Satellite Systems](articles/卫星安全/2025-10-08-SpyChain-Multi-Vector-Supply-Chain-Attacks-on-Small-Satellit.md) · [原文](http://arxiv.org/abs/2510.06535v2)
- [SatBleed: Security of Commoditized Communication Modules in Satellites](articles/卫星安全/2026-10-05-SatBleed-Security-of-Commoditized-Communication-Modules-in-S.md) · [原文](http://arxiv.org/abs/2610.06258v1)
- [Systematic Security Analysis of the Iridium Satellite Radio Link](articles/卫星安全/2026-03-12-Systematic-Security-Analysis-of-the-Iridium-Satellite-Radio.md) · [原文](http://arxiv.org/abs/2603.12062v1)
- [JANUS: Denial-of-Service Attack Against Beam Hopping in LEO Satellite Networks](articles/卫星安全/2026-09-17-JANUS-Denial-of-Service-Attack-Against-Beam-Hopping-in-LEO-S.md) · [原文](http://arxiv.org/abs/2609.19977v1)
- [Silent Subversion: Sensor Spoofing Attacks via Supply Chain Implants in Satellite Systems](articles/卫星安全/2026-03-11-Silent-Subversion-Sensor-Spoofing-Attacks-via-Supply-Chain-I.md) · [原文](http://arxiv.org/abs/2603.10388v1)
- [Updated Standard for Secure Satellite Communications: Analysis of Satellites, Attack Vectors, Existing Standards, and Enterprise and Security Architectures](articles/卫星安全/2023-10-29-Updated-Standard-for-Secure-Satellite-Communications-Analysi.md) · [原文](http://arxiv.org/abs/2310.19105v1)
- [SATversary: Adversarial Attacks and Defenses for Satellite Fingerprinting](articles/卫星安全/2025-06-06-SATversary-Adversarial-Attacks-and-Defenses-for-Satellite-Fi.md) · [原文](http://arxiv.org/abs/2506.06119v2)

## 打印机

> MFP 类设备的多漏洞面

- [通过三个步骤入侵打印机](https://www.crowdstrike.com/en-us/blog/how-to-compromise-a-printer-in-3-simple-steps/)
- [Sharp MFP 17 漏洞分析](https://pierrekim.github.io/blog/2024-06-27-sharp-mfp-17-vulnerabilities.html#pre-auth-memory-corruption)
- [Xerox WorkCentre 未授权 RCE 漏洞](https://swarm.ptsecurity.com/inside-xerox-workcentre-two-unauthenticated-rces/)
- [CVE-2024-0244 – A heap buffer overflow in the Canon MF753Cdw printer](articles/打印机/2026-09-24-CVE-2024-0244-A-heap-buffer-overflow-in-the-Canon-MF753Cdw-p.md) · [原文](https://www.thezdi.com/blog/2026/9/23/cve-2024-0244-a-heap-buffer-overflow-in-the-canon-mf753cdw-printer)

## 智能家居

> 智能音箱、称重设备、DVB 等消费级设备

- [谷歌智能音箱安全分析](https://security.tencent.com/index.php/blog/msg/141)
- [Pwning Millions of Smart Weighing Machines with API and Hardware Hacking](https://spaceraccoon.dev/pwning-millions-smart-weighing-machines-api-hardware-hacking/)
- [Hack the Channel：DVB 接收机安全深度分析](https://www.synacktiv.com/en/publications/hack-the-channel-a-deep-dive-into-dvb-receiver-security)
- [Flicker and fall: rooting the Philips Hue Bridge both remotely and wirelessly](articles/智能家居/2026-06-08-Flicker-and-fall-rooting-the-Philips-Hue-Bridge-both-remotel.md) · [原文](https://blog.thalium.re/posts/rooting-the-philips-hue-bridge-remotely-and-wirelessly/)
- [Streaming Zero-Fi Shells to Your Smart Speaker](articles/智能家居/2025-06-11-Streaming-Zero-Fi-Shells-to-Your-Smart-Speaker.md) · [原文](https://blog.ret2.io/2025/06/11/pwn2own-soho-2024-sonos-exploit/)
- [Apple AirTag（nRF52832）电压毛刺解锁 APPROTECT 并转储固件](articles/智能家居/2026-11-14-Apple-AirTag-nRF52832-电压毛刺解锁-APPROTECT-并转储固件.md) · [原文](https://github.com/ensingerphilipp/airtag-glitch-dump-improved)
- [Chipolo 蓝牙追踪器：FI 绕调试锁 → 固件逆向 → 蓝牙栈 RCE](articles/智能家居/2024-12-27-Chipolo-蓝牙追踪器-FI-绕调试锁-固件逆向-蓝牙栈-RCE.md) · [原文](https://media.ccc.de/v/38c3-from-fault-injection-to-rce-analyzing-a-bluetooth-tracker)

## 机器人

> 机器人本体与控制链路

- [宇树GO1机器人分析](https://think-awesome.com/download_unitree_report)

## 芯片安全

> SoC / 微码 / 熔丝密钥

- [Last barrier destroyed, or compromise of Fuse Encryption Key for Intel Security Fuses](https://swarm.ptsecurity.com/last-barrier-destroyed-or-compromise-of-fuse-encryption-key-for-intel-security-fuses/)
- [Bypassing Android Hardware Attestation from the Analyst's Chair](articles/芯片安全/2026-08-11-Bypassing-Android-Hardware-Attestation-from-the-Analyst-s-Ch.md) · [原文](http://blog.quarkslab.com/bypassing-android-hardware-attestation.html)
- [Black Box Probing: a Security Analysis of Xiaomi's MJA1 Secure Chip](articles/芯片安全/2026-06-18-Black-Box-Probing-a-Security-Analysis-of-Xiaomi-s-MJA1-Secur.md) · [原文](http://blog.quarkslab.com/black-box-probing-a-security-analysis-of-xiaomis-mja1-secure-chip.html)
- [TriSweep: A Four-Drone Swarm Framework for Electromagnetic Side-Channel Analysis](articles/芯片安全/2026-05-21-TriSweep-A-Four-Drone-Swarm-Framework-for-Electromagnetic-Si.md) · [原文](http://arxiv.org/abs/2605.22709v1)
- [Side-Channel Attacks on RISC-V Processors: Current Progress, Challenges, and Opportunities](articles/芯片安全/2021-06-16-Side-Channel-Attacks-on-RISC-V-Processors-Current-Progress-C.md) · [原文](http://arxiv.org/abs/2106.08877v1)
- [SoK: Where's the "up"?! A Comprehensive (bottom-up) Study on the Security of Arm Cortex-M Systems](articles/芯片安全/2024-01-27-SoK-Where-s-the-up-A-Comprehensive-bottom-up-Study-on-the-Se.md) · [原文](http://arxiv.org/abs/2401.15289v3)
- [One Exploit to Rule them All? On the Security of Drop-in Replacement and Counterfeit Microcontrollers](articles/芯片安全/2020-08-21-One-Exploit-to-Rule-them-All-On-the-Security-of-Drop-in-Repl.md) · [原文](http://arxiv.org/abs/2008.09710v1)
- [Hardware Security Evaluation of MAX 10 FPGA](articles/芯片安全/2019-10-11-Hardware-Security-Evaluation-of-MAX-10-FPGA.md) · [原文](http://arxiv.org/abs/1910.05086v1)
- [BugWhisperer: Fine-Tuning LLMs for SoC Hardware Vulnerability Detection](articles/芯片安全/2025-05-28-BugWhisperer-Fine-Tuning-LLMs-for-SoC-Hardware-Vulnerability.md) · [原文](http://arxiv.org/abs/2505.22878v1)
- [Supporting Rowhammer research to protect the DRAM ecosystem](articles/芯片安全/2025-09-16-Supporting-Rowhammer-research-to-protect-the-DRAM-ecosystem.md) · [原文](http://security.googleblog.com/2025/09/supporting-rowhammer-research-to.html)
- [Further Hardening Android GPUs](articles/芯片安全/2025-12-10-Further-Hardening-Android-GPUs.md) · [原文](http://security.googleblog.com/2025/12/further-hardening-android-gpus.html)
- [Don't let TEEs break your MPC](articles/芯片安全/2026-09-25-Don-t-let-TEEs-break-your-MPC.md) · [原文](https://blog.trailofbits.com/2026/09/25/dont-let-tees-break-your-mpc/)
- [GA100 数据中心 GPU PWMVID 电压毛刺实验台](articles/芯片安全/2026-11-14-GA100-数据中心-GPU-PWMVID-电压毛刺实验台.md) · [原文](https://github.com/kate-land/ga100vfi)
- [压电打火机 EMFI 打 DRAM 总线：笔记本 Linux 提权 root](articles/芯片安全/2024-10-07-压电打火机-EMFI-打-DRAM-总线-笔记本-Linux-提权-root.md) · [原文](https://www.da.vidbuchanan.co.uk/blog/dram-emfi.html)

## RFID

> NFC / MIFARE / 智能卡

- [身边的智能卡安全么？——IC卡安全性初探](https://xz.aliyun.com/news/8265?time__1311=YqUxg7iQoDqQqGNKQrDnBCFG%3D%3DMGO3rD&u_atoken=2605ac6da9572677f351f83015d5ebad&u_asig=1a0c399817433461047984986e0046)
- [IC卡加密方式和基本常识](https://mp.weixin.qq.com/s/MC_gsU3lbOUfmkfKK_0RTQ)
- [RFID 射频卡安全梳理](https://stdio.io/1345)
- [MIFARE Classic: exposing the static encrypted nonce variant](https://eprint.iacr.org/2024/1275.pdf)
- [逆向破解南京大学纯 CPU SAK28 FM1208 NFC 校园卡](https://blog.lyc8503.net/post/reverse-nju-cpu-card/)

## WIFI安全

> 802.11 协议层漏洞

- [无线网络（WI-FI）保护协议标准WPA2漏洞综合分析报告](https://www.antiy.com/response/krack.html)

## 协议安全

> 蓝牙、无线电与通用协议栈

- [DNSpooq系列漏洞分析与复现](https://www.venustech.com.cn/new_type/aqldfx/20210201/22352.html)
- [Bluetooth-Attacks-CVE-2025-27840](https://github.com/demining/Bluetooth-Attacks-CVE-2025-27840)
- [无线电安全攻防之蓝牙协议栈技术初探](https://mp.weixin.qq.com/s/OTSwW2E1BRHYuGg1XxAC8g)

## 硬件钱包

> Web3 硬件钱包的攻击面

- [攻防速写｜假如捡到 Web3 硬件钱包的人是黑客](https://mp.weixin.qq.com/s/FYDgYG9UCTgwc7KxAdIjjw)
- [Trezor 穿壳 EMFI：毛刺 USB 栈长度检查读出 metadata/seed](articles/硬件钱包/2019-03-06-Trezor-穿壳-EMFI-毛刺-USB-栈长度检查读出-metadata-seed.md) · [原文](https://colinoflynn.com/2019/03/glitching-trezor-using-emfi-through-the-enclosure/)
- [STM32F2/F4 故障注入：EMFI/VFI 双档 RDP2→RDP1 + FPB 两毛刺读全片 flash](articles/硬件钱包/2026-11-14-STM32F2-F4-故障注入-EMFI-VFI-双档-RDP2-RDP1-FPB-两毛刺读全片-flash.md) · [原文](https://github.com/joegrand/stm32-fault-injection)

## FUZZ

> 固件与二进制 fuzz 方法

- [RV130X Firmware Analysis](https://raffo24.github.io/hardware%20hacking/FirmwareAnalysis/)
- [Snapshotting our way to CVE-2026-9539](articles/FUZZ/2026-10-27-Snapshotting-our-way-to-CVE-2026-9539.md) · [原文](http://blog.quarkslab.com/snapshotting-our-way-to-cve-2026-9539.html)
- [Fuzz'EMup: Leveraging EM Side-Channel Emanation to Guide Black-Box Embedded Firmware Fuzzing](articles/FUZZ/2026-07-17-Fuzz-EMup-Leveraging-EM-Side-Channel-Emanation-to-Guide-Blac.md) · [原文](http://arxiv.org/abs/2607.16487v1)
- [PowerFuzz: Power-Based Black-Box Firmware Fuzzing](articles/FUZZ/2026-06-23-PowerFuzz-Power-Based-Black-Box-Firmware-Fuzzing.md) · [原文](http://arxiv.org/abs/2606.24692v1)

## 安全启动

> Secure Boot / U-Boot / UEFI 启动链

- [TP-Link C210 安全启动分析](https://watchfulip.github.io/28-12-24/tp-link_c210_v2.html)
- [U-Boot 逆向分析（Part 1）](https://www.shielder.com/blog/2022/03/reversing-embedded-device-bootloader-u-boot-p.1/)
- [U-Boot 逆向分析（Part 2）](https://www.shielder.com/blog/2022/03/reversing-embedded-device-bootloader-u-boot-p.2/)
- [潜伏16年的UEFI漏洞：开机那几秒，你的所有防线都还没上线](articles/安全启动/2026-11-05-潜伏16年的UEFI漏洞-开机那几秒-你的所有防线都还没上线.md) · [原文](https://www.anquanke.com/post/id/316426)
- [Can AI Hack Firmware? Evaluating LLMs on UEFI Vulnerability Discovery](articles/安全启动/2026-08-12-Can-AI-Hack-Firmware-Evaluating-LLMs-on-UEFI-Vulnerability-D.md) · [原文](https://www.binarly.io/blog/uefi-vulnerability-discovery-ai)
- [Hidden beneFITs: Bypassing Signature Verification in U-Boot SPL](articles/安全启动/2026-08-06-Hidden-beneFITs-Bypassing-Signature-Verification-in-U-Boot-S.md) · [原文](https://www.binarly.io/blog/signature-verification-bypass-in-u-boot-spl)
- [Fit for Detection: Hunting U-Boot Vulnerabilities at Scale](articles/安全启动/2026-07-16-Fit-for-Detection-Hunting-U-Boot-Vulnerabilities-at-Scale.md) · [原文](https://www.binarly.io/blog/hunting-u-boot-at-scale)
- [Unfit to Boot: Breaking U-Boot's FIT Signature Verification](articles/安全启动/2026-07-09-Unfit-to-Boot-Breaking-U-Boot-s-FIT-Signature-Verification.md) · [原文](https://www.binarly.io/blog/unfit-to-boot-breaking-u-boots-fit-signature-verification)
- [Have you patched? Are you sure? The story of the sticky Supermicro BMC bugs](articles/安全启动/2026-01-26-Have-you-patched-Are-you-sure-The-story-of-the-sticky-Superm.md) · [原文](https://www.binarly.io/blog/have-you-patched--are-you-sure--the-story-of-the-sticky-supermicro-bmc-bugs)
- [Missing Mitigations: Inside The Security Gap in UEFI Firmware](articles/安全启动/2025-10-17-Missing-Mitigations-Inside-The-Security-Gap-in-UEFI-Firmware.md) · [原文](https://www.binarly.io/blog/missing-mitigations-inside-security-gap-uefi-firmware)
- [Signed and Dangerous: BYOVD Attacks on Secure Boot](articles/安全启动/2025-09-10-Signed-and-Dangerous-BYOVD-Attacks-on-Secure-Boot.md) · [原文](https://www.binarly.io/blog/signed-and-dangerous-byovd-attacks-on-secure-boot)
- [Ghost in the Controller: Abusing Supermicro BMC Firmware Verification](articles/安全启动/2025-07-02-Ghost-in-the-Controller-Abusing-Supermicro-BMC-Firmware-Veri.md) · [原文](https://www.binarly.io/blog/ghost-in-the-controller-abusing-supermicro-bmc-firmware)
- [UEFI Bootkit Hunting: In-Depth Search for Unique Code Behavior](articles/安全启动/2025-03-13-UEFI-Bootkit-Hunting-In-Depth-Search-for-Unique-Code-Behavio.md) · [原文](https://www.binarly.io/blog/uefi-bootkit-hunting-in-depth-search-for-unique-code-behavior)
- [CVE-2024-36435 Deep-Dive: The Year's Most Critical BMC Security Flaw](articles/安全启动/2024-09-26-CVE-2024-36435-Deep-Dive-The-Year-s-Most-Critical-BMC-Securi.md) · [原文](https://www.binarly.io/blog/cve-2024-36435-deep-dive-critical-bmc-security-flaw)
- [Another Crack in the Chain of Trust: Uncovering (Yet Another) Secure Boot Bypass](articles/安全启动/2025-06-10-Another-Crack-in-the-Chain-of-Trust-Uncovering-Yet-Another-S.md) · [原文](https://www.binarly.io/blog/another-crack-in-chain-of-trust-secure-boot-bypass)
- [Broken Trust: Fixed Supermicro BMC Bug Gains a New Life in Two New Vulnerabilities](articles/安全启动/2025-09-24-Broken-Trust-Fixed-Supermicro-BMC-Bug-Gains-a-New-Life-in-Tw.md) · [原文](https://www.binarly.io/blog/broken-trust-fixed-supermicro-bmc-bug-gains-new-life)
- [How an Old Bug in Lighttpd Gained New Life in AMI BMC, Including Lenovo and Intel products](articles/安全启动/2025-11-19-How-an-Old-Bug-in-Lighttpd-Gained-New-Life-in-AMI-BMC-Includ.md) · [原文](https://www.binarly.io/blog/how-an-old-bug-in-lighttpd-gained-new-life-in-ami-bmc-including-lenovo-and-intel-products)
- [Clevo Boot Guard Keys Leaked in Update Package](articles/安全启动/2025-03-20-Clevo-Boot-Guard-Keys-Leaked-in-Update-Package.md) · [原文](https://www.binarly.io/blog/clevo-boot-guard-keys-leaked-in-update-package)
- [LogoFAIL Exploited to Deploy Bootkitty, the first UEFI bootkit for Linux](articles/安全启动/2024-11-29-LogoFAIL-Exploited-to-Deploy-Bootkitty-the-first-UEFI-bootki.md) · [原文](https://www.binarly.io/blog/logofail-exploited-deploy-bootkitty-first-uefi-bootkit-linux)
- [Zynq-7000 Secure Boot：故障注入攻破 RSA 位流认证（WOOT'24）](articles/安全启动/2024-08-13-Zynq-7000-Secure-Boot-故障注入攻破-RSA-位流认证-WOOT-24.md) · [原文](https://www.usenix.org/conference/woot24/presentation/ravi)
- [bootl-attacks（CHES'21）：LPC1343 ROP / STM8 双毛刺 / Renesas 78K0 符号执行制导](articles/安全启动/2021-09-01-bootl-attacks-CHES-21-LPC1343-ROP-STM8-双毛刺-Renesas-78K0-符号执行.md) · [原文](https://github.com/janvdherrewegen/bootl-attacks)
- [RP2350 光子发射引导激光 FI：恢复被永久关闭的 Secure Debug](articles/安全启动/2026-11-13-RP2350-光子发射引导激光-FI-恢复被永久关闭的-Secure-Debug.md) · [原文](https://donjon.ledger.com/blog/rp2350-secure-debug-laser-fault-injection/)

## 固件解密

> 加密固件解包与密钥恢复

- [DrayTek 固件解密分析](https://www.hexacon.fr/slides/hexacon_draytek_2022_final.pdf)
- [D-Link 固件漏洞分析](https://bbs.kanxue.com/thread-281043.htm)
- [D-Link 固件漏洞研究](https://wzt.ac.cn/2019/09/18/D-Link_BUG/)
- [D-Link 固件解密脚本](https://github.com/0xricksanchez/dlink-decrypt)
- [SonicOS 固件解密分析（2024）](https://wzt.ac.cn/2024/09/05/sonicwall_dec2/)
- [SonicOS 固件解密分析（2022）](https://wzt.ac.cn/2022/02/08/sonicwall_dec1/)
- [Linksys 固件漏洞分析](https://www.anquanke.com/post/id/246659)
- [D-Link DIR3060 固件解密分析（Part 1）](https://0x00sec.org/t/breaking-the-d-link-dir3060-firmware-encryption-static-analysis-of-the-decryption-routine-part-2-1/22099)
- [D-Link DIR3060 固件解密分析（Part 2）](https://0x00sec.org/t/breaking-the-d-link-dir3060-firmware-encryption-static-analysis-of-the-decryption-routine-part-2-2/22260)
- [Lexmark 固件漏洞分析](https://haxx.in/posts/wtm-wtf/)
- [乐鑫芯片 Flash 加密破解](https://courk.cc/breaking-flash-encryption-of-espressif-parts#breaking-flash-encryption-of-espressif-parts)
- [使用机器学习解密固件](https://something.fromnothing.blog/posts/something-from-nothing/)
- [摄像头逆向分析之旅-程序还原](https://blog.nsfocus.net/lot-flash/)
- [Two Oracles to Get One Key: A tale of recovering a symmetric key from an encrypt-only firmware update scheme](articles/固件解密/2026-11-10-Two-Oracles-to-Get-One-Key-A-tale-of-recovering-a-symmetric.md) · [原文](https://www.ioactive.com/two-oracles-recovering-aes-firmware-key/)
- [STM32-TraceRip：不注入故障，用 CRC 状态步进重建受保护 flash](articles/固件解密/2025-06-10-STM32-TraceRip-不注入故障-用-CRC-状态步进重建受保护-flash.md) · [原文](https://hardwear.io/wp-content/uploads/2026/03/TraceRip-Hardwear.pdf)

## 故障注入

> 电压毛刺、EMFI 等物理攻击

- [Fault Injection – Down the Rabbit Hole](https://security.humanativaspa.it/fault-injection-down-the-rabbit-hole/)
- [Glitch in the Sky: Exploiting Voltage Fault Injection in UAV Flight Controllers](articles/故障注入/2026-04-17-Glitch-in-the-Sky-Exploiting-Voltage-Fault-Injection-in-UAV.md) · [原文](http://arxiv.org/abs/2604.16699v1)
- [One Glitch to Rule Them All: Fault Injection Attacks Against AMD's Secure Encrypted Virtualization](articles/故障注入/2021-08-10-One-Glitch-to-Rule-Them-All-Fault-Injection-Attacks-Against.md) · [原文](http://arxiv.org/abs/2108.04575v4)
- [Oops..! I Glitched It Again! How to Multi-Glitch the Glitching-Protections on ARM TrustZone-M](articles/故障注入/2023-02-14-Oops-I-Glitched-It-Again-How-to-Multi-Glitch-the-Glitching-P.md) · [原文](http://arxiv.org/abs/2302.06932v2)
- [Injecting Software Vulnerabilities with Voltage Glitching](articles/故障注入/2019-02-14-Injecting-Software-Vulnerabilities-with-Voltage-Glitching.md) · [原文](http://arxiv.org/abs/1903.08102v1)
- [Physical and Software Based Fault Injection Attacks Against TEEs in Mobile Devices: A Systemisation of Knowledge](articles/故障注入/2024-11-22-Physical-and-Software-Based-Fault-Injection-Attacks-Against.md) · [原文](http://arxiv.org/abs/2411.14878v1)
- [The Forgotten Threat of Voltage Glitching: A Case Study on Nvidia Tegra X2 SoCs](articles/故障注入/2021-08-13-The-Forgotten-Threat-of-Voltage-Glitching-A-Case-Study-on-Nv.md) · [原文](http://arxiv.org/abs/2108.06131v2)
- [Keyless Entry: Breaking and Entering eMMC RPMB with EMFI](articles/故障注入/2025-11-27-Keyless-Entry-Breaking-and-Entering-eMMC-RPMB-with-EMFI.md) · [原文](http://arxiv.org/abs/2511.22340v1)
- [NonSense: On the (In)security of FPGA Anti-tamper Sensors](articles/故障注入/2026-11-12-NonSense-On-the-In-security-of-FPGA-Anti-tamper-Sensors.md) · [原文](http://arxiv.org/abs/2611.17065v1)
- [EM-Fault It Yourself: Building a Replicable EMFI Setup for Desktop and Server Hardware](articles/故障注入/2022-09-20-EM-Fault-It-Yourself-Building-a-Replicable-EMFI-Setup-for-De.md) · [原文](http://arxiv.org/abs/2209.09835v1)
- [EMMap: A Systematic Framework for Spatial EMFI Mapping and Fault Classification on Microcontrollers](articles/故障注入/2025-12-09-EMMap-A-Systematic-Framework-for-Spatial-EMFI-Mapping-and-Fa.md) · [原文](http://arxiv.org/abs/2512.09049v1)
- [Honest to a Fault: Root-Causing Fault Attacks with Pre-Silicon RISC Pipeline Characterization](articles/故障注入/2025-03-05-Honest-to-a-Fault-Root-Causing-Fault-Attacks-with-Pre-Silico.md) · [原文](http://arxiv.org/abs/2503.04846v2)
- [Google Wifi Pro Glitching from Root to EL3 (Part 1: Characterization)](articles/故障注入/2026-05-01-Google-Wifi-Pro-Glitching-from-Root-to-EL3-Part-1-Characteri.md) · [原文](https://raelize.com/blog/google-wifi-pro-glitching-from-root-to-el3-part-1-characterization/)
- [Google Wifi Pro Glitching from Root to EL3 (Part 3: Arbitrary Code Execution)](articles/故障注入/2026-05-20-Google-Wifi-Pro-Glitching-from-Root-to-EL3-Part-3-Arbitrary.md) · [原文](https://raelize.com/blog/google-wifi-pro-glitching-from-root-to-el3-part-3-arbitrary-code-exec/)
- [setresuid(⚡): Glitching Google's TV Streamer from adb to Root](articles/故障注入/2026-04-01-setresuid-Glitching-Google-s-TV-Streamer-from-adb-to-Root.md) · [原文](https://raelize.com/blog/setresuid-glitching-google-tv-streamer-from-adb-to-root/)
- [AI-FI: Giving Claude Code Glitch Skills for Bypassing Secure Boot](articles/故障注入/2026-06-01-AI-FI-Giving-Claude-Code-Glitch-Skills-for-Bypassing-Secure.md) · [原文](https://raelize.com/blog/ai-fi-giving-claude-code-glitch-skills-for-bypassing-secure-boot/)
- [Triple Exploit Chain with Laser Fault Injection on a Secure Element](articles/故障注入/2024-10-01-Triple-Exploit-Chain-with-Laser-Fault-Injection-on-a-Secure.md) · [原文](https://hardwear.io/talks/triple-exploit-chain-with-laser-fault-injection-on-a-secure-element/)
- [ESP32 全安全模式双毛刺：绕过 Secure Boot 并读出 FEK/SBK（CVE-2019-15894 / CVE-2019-17391）](articles/故障注入/2019-09-01-ESP32-全安全模式双毛刺-绕过-Secure-Boot-并读出-FEK-SBK-CVE-2019-15894-CVE.md) · [原文](https://limitedresults.com/results/pwn-the-esp32-secure-boot)
- [Espressif AR2023-007：ESP32-C3/C6 遭 CPA + 电压毛刺组合绕过 Secure Boot 与 Flash 加密](articles/故障注入/2024-01-05-Espressif-AR2023-007-ESP32-C3-C6-遭-CPA-电压毛刺组合绕过-Secure-Boot.md) · [原文](https://www.espressif.com/sites/default/files/advisory_downloads/AR2023-007%20Security%20Advisory%20Concerning%20Bypassing%20Secure%20Boot%20and%20Flash%20Encryption%20using%20CPA%20and%20FI%20attack%20on%20ESP32-C3%20and%20ESP32-C6%20EN.pdf)
- [Qualcomm IPQ40xx QSEE：EMFI 绕过安全范围检查实现任意 NULL 写](articles/故障注入/2021-06-07-Qualcomm-IPQ40xx-QSEE-EMFI-绕过安全范围检查实现任意-NULL-写.md) · [原文](https://raelize.com/blog/qualcomm-ipq40xx-breaking-into-qsee-using-fault-injection/)
- [PS Vita BootROM 毛刺：ChipWhisperer 时钟注入执行自定义 payload](articles/故障注入/2018-12-01-PS-Vita-BootROM-毛刺-ChipWhisperer-时钟注入执行自定义-payload.md) · [原文](https://github.com/TeamMolecule/petite-mort)
- [RP2350 OTP 毛刺：割断 USB_OTP_VDD 后在 ~1.75ms 窗口篡改 OTP](articles/故障注入/2026-11-14-RP2350-OTP-毛刺-割断-USB_OTP_VDD-后在-1-75ms-窗口篡改-OTP.md) · [原文](https://mkesenheimer.github.io/blog/glitching-the-rp2350.html)
- [findus / fault-injection-library：Pico Glitcher 软件框架 + 12 个 MCU 靶项目](articles/故障注入/2026-11-14-findus-fault-injection-library-Pico-Glitcher-软件框架-12-个-MCU-靶.md) · [原文](https://github.com/MKesenheimer/fault-injection-library)
- [ChipWhisperer 官方 Tips & Tricks：毛刺硬件选型、亚周期精度与触发排障](articles/故障注入/2026-11-14-ChipWhisperer-官方-Tips-Tricks-毛刺硬件选型-亚周期精度与触发排障.md) · [原文](https://github.com/newaetech/cw_tips_tricks)
- [Raelize RapidBlockMode：PicoScope 分段采集 + GPIO 选通的对齐基础设施](articles/故障注入/2026-11-14-Raelize-RapidBlockMode-PicoScope-分段采集-GPIO-选通的对齐基础设施.md) · [原文](https://github.com/raelize/RapidBlockMode)
- [GlitchGlück（WOOT'25）：用状态转移图引导硬件故障注入复现软件漏洞](articles/故障注入/2026-11-14-GlitchGl-ck-WOOT-25-用状态转移图引导硬件故障注入复现软件漏洞.md) · [原文](https://github.com/Secure-Embedded-Systems/woot2025-GlitchGluck)
- [Rainbow：Unicorn 指令级侧信道 / 故障注入仿真器（Ledger Donjon）](articles/故障注入/2026-11-14-Rainbow-Unicorn-指令级侧信道-故障注入仿真器-Ledger-Donjon.md) · [原文](https://github.com/Ledger-Donjon/rainbow)
- [ot-sca：OpenTitan 官方 SCA + 故障注入评估框架](articles/故障注入/2026-11-14-ot-sca-OpenTitan-官方-SCA-故障注入评估框架.md) · [原文](https://github.com/lowRISC/ot-sca)
- [Cypherock EMFI Board：低成本开源电磁故障注入台架（附 7 款钱包 DUT）](articles/故障注入/2026-11-14-Cypherock-EMFI-Board-低成本开源电磁故障注入台架-附-7-款钱包-DUT.md) · [原文](https://github.com/Cypherock/emfi-board)
- [SiliconToaster：开源 0–1000V 电磁故障注入发生器（Ledger Donjon）](articles/故障注入/2026-11-14-SiliconToaster-开源-0-1000V-电磁故障注入发生器-Ledger-Donjon.md) · [原文](https://github.com/Ledger-Donjon/silicon-toaster)
- [ChipShover：EMFI/EM 探针的 XYZ 定位台](articles/故障注入/2026-11-14-ChipShover-EMFI-EM-探针的-XYZ-定位台.md) · [原文](https://github.com/newaetech/ChipShover)
- [ESP32 EMFI 绕 Secure Boot（CVE-2020-13629 / 15048 系列）](articles/故障注入/2020-07-24-ESP32-EMFI-绕-Secure-Boot-CVE-2020-13629-15048-系列.md) · [原文](https://raelize.com/blog/espressif-systems-esp32-bypassing-sb-using-emfi/)
- [ESP32 OTP Transfer EMFI：打 eFuse→shadow 寄存器的纯硬件搬运窗口](articles/故障注入/2023-03-10-ESP32-OTP-Transfer-EMFI-打-eFuse-shadow-寄存器的纯硬件搬运窗口.md) · [原文](https://raelize.com/blog/espressif-systems-esp32-glitching-otp-transfer/)
- [RP2350 预算级激光故障注入（Glasgow + DEF CON 33 Playground）](articles/故障注入/2026-11-14-RP2350-预算级激光故障注入-Glasgow-DEF-CON-33-Playground.md) · [原文](https://github.com/courk/rp2350-lfi)
- [ATECC608A 安全元件：两发激光故障读出 PIN hash（Coldcard Mk3 种子可窃）](articles/故障注入/2021-06-01-ATECC608A-安全元件-两发激光故障读出-PIN-hash-Coldcard-Mk3-种子可窃.md) · [原文](https://www.sstic.org/media/SSTIC2021/SSTIC-actes/defeating_a_secure_element_with_multiple_laser_fau/SSTIC2021-Article-defeating_a_secure_element_with_multiple_laser_fault_injections-heriveaux.pdf)
- [SPHINCS+ 故障攻击与对策（TCHES 2023 官方 artifact）](articles/故障注入/2023-06-01-SPHINCS-故障攻击与对策-TCHES-2023-官方-artifact.md) · [原文](https://github.com/AymericGenet/SPHINCSplus-FA)
- [RHme2 / RHme3 故障注入挑战解题合集（Riscure CTF）](articles/故障注入/2018-01-01-RHme2-RHme3-故障注入挑战解题合集-Riscure-CTF.md) · [原文](https://github.com/Riscure/Rhme-2016)
- [把故障注入仿真塞进开发流（Ledger Donjon：rust_fi + Rainbow + CI）](articles/故障注入/2026-11-14-把故障注入仿真塞进开发流-Ledger-Donjon-rust_fi-Rainbow-CI.md) · [原文](https://github.com/Ledger-Donjon/fault_injection_checks_demo)

## 绕过ASLR

> 信息泄露、ROP 与地址随机化绕过

- [使用栈上gadget绕过 ASLR](https://www.anquanke.com/post/id/180252)
- [修改 sendsize 触发 DNS 查询泄露地址](https://claroty.com/team82/research/pwn2own-wan-to-lan-exploit-showcase?ref=blog.exploits.club)
- [通过文件包含漏洞绕过 ASLR](https://modzero.com/en/blog/roping-our-way-to-rce/)
- [How CVE-2015-7547 (GLIBC getaddrinfo) Can Bypass ASLR](https://mp.weixin.qq.com/s/AEOc49tz_WlDABXucmVPNw)
- [Armis：CDPwn 漏洞链如何绕过 ASLR](https://media.armis.com/image/upload/v1679440790/PDFs/wp-armis-cdpwn-aslr-bypass-en.pdf)

## 固件下载

> 厂商固件官方下载入口

- [TENDA 固件下载](https://www.tenda.com.cn/download/default.html)
- [迅捷固件下载](https://service.fastcom.com.cn/download-list.html#0)
- [TP-LINK 固件下载（国内）](https://resource.tp-link.com.cn/?&productorlist=1&filterClass=%5B4%5D)
- [TP-LINK 固件下载（国外）](https://www.tp-link.com/us/support/download/)
- [水星固件下载](https://service.mercurycom.com.cn/download-list.html)
- [艾泰固件下载](https://www.utt.com.cn/downloadcenter.php)
- [锐捷固件下载](https://www.ruijie.com.cn/fw/rj-first-2321/)
- [DLINK 固件下载](https://support.dlink.com/resource/products/)
- [NETGEAR 固件下载](http://support.netgear.cn/download.asp)
- [SOFTPEDIA 驱动下载](https://drivers.softpedia.com/)
- [DrayTek 固件下载](https://www.draytek.com/support/resources/routers#version)
- [iptime 固件下载](https://iptime.com/iptime/?page_id=126)
- [ubiquiti 固件下载](https://ui.com.cn/download/releases/firmware)
- [grandstream 固件下载](https://www.grandstream.com/support/firmware)
- [peplink 固件下载](https://www.peplink.com/support/downloads/)
- [AVM（Fritz!Box）固件下载](https://avm.de/service/downloads/)
- [axis 固件下载](https://www.axis.com/support/device-software)
- [海康威视固件下载](https://www.hiksemitech.com/en/hiksemi/support/download.html)

## 虚拟机镜像

> 可直接复现的固件/仿真镜像

暂无，欢迎通过 PR 补充。

## 杂项

> 逆向工具、白皮书与其他资料

- [浅析 CGI 与 Lighttpd 之间的调用过程](https://www.iotsec-zone.com/article/319)
- [史上最全 U-Boot 命令解析](https://cloud.tencent.com/developer/article/2102295)
- [通过 WIFI 修改加热器固件](https://blog.includesecurity.com/2025/02/replacing-a-space-heater-firmware-over-wifi/)
- [Brushing Up on Hardware Hacking Part 2 - SPI, UART, Pulseview, and Flashrom](https://voidstarsec.com/blog/brushing-up-part-2)
- [嵌入式设备后门与shellcode生成工具](https://bbs.kanxue.com/thread-275619.htm)
- [IOT设备常见配置文件加解密分析总结](https://mp.weixin.qq.com/s/vik2Xp459afeV0e3xcihHQ)
- [智能网联汽车信息安全测试白皮书](https://report.secbug.cc/2025%E6%99%BA%E8%83%BD%E7%BD%91%E8%81%94%E6%B1%BD%E8%BD%A6%E4%BF%A1%E6%81%AF%E5%AE%89%E5%85%A8%E6%B5%8B%E8%AF%95%E7%99%BD%E7%9A%AE%E4%B9%A6.pdf)
- [企业安全设备漏洞研究](https://drive.google.com/file/d/1W6kVh6zJ-R61WR69xX7V02mmESTuwPJO/view)
- [深入剖析路由器FOTA固件升级流程：从解包到逆向分析](https://xz.aliyun.com/news/17402?time__1311=eqUxn7DQG%3DekD%2Fb043aDBDRxQqiKN%3D3x&u_atoken=410984a321fcdb00f210c49c794f8cb1&u_asig=1a0c380917440179029383912e00f0)
- [Secure Hardware Design](https://shd.mit.edu/home/)
- [VxWorks固件系统研究技术总结二](https://mp.weixin.qq.com/s/SnooEM6NLLPIz8u2t4_MOw)
- [BinQL: a CodeQL extension for binary formats](articles/杂项/2026-11-13-BinQL-a-CodeQL-extension-for-binary-formats.md) · [原文](https://blog.thalium.re/posts/binql-a-codeql-extension-for-binary-formats/)
- [Exploiting the Synology DiskStation with Null-byte Writes](articles/杂项/2025-04-23-Exploiting-the-Synology-DiskStation-with-Null-byte-Writes.md) · [原文](https://blog.ret2.io/2025/04/23/pwn2own-soho-2024-diskstation/)
- [Deep dip teardown of tubeless insulin pump](articles/杂项/2017-09-18-Deep-dip-teardown-of-tubeless-insulin-pump.md) · [原文](http://arxiv.org/abs/1709.06026v1)
- [Lessons from the Hardware Hacking Competitions: Verification Techniques, Findings, and Insights](articles/杂项/2026-08-23-Lessons-from-the-Hardware-Hacking-Competitions-Verification.md) · [原文](http://arxiv.org/abs/2608.22202v1)
- [Your KVM is the Weak Link: How $30 Devices Can Own Your Entire Network](articles/杂项/2026-03-17-Your-KVM-is-the-Weak-Link-How-30-Devices-Can-Own-Your-Entire.md) · [原文](https://eclypsium.com/blog/your-kvm-is-the-weak-link-how-30-dollar-devices-can-own-your-entire-network/)
- [Fake Kernel Threads Are Hiding Backdoors on Linux Servers and Appliances](articles/杂项/2026-10-20-Fake-Kernel-Threads-Are-Hiding-Backdoors-on-Linux-Servers-an.md) · [原文](https://eclypsium.com/blog/linux-malware-fake-kernel-threads/)
- [The Explosion of Hardware-Hacking Devices](articles/杂项/2025-02-08-The-Explosion-of-Hardware-Hacking-Devices.md) · [原文](https://eclypsium.com/blog/the-explosion-of-hardware-hacking-devices/)
- [Android’s pKVM Becomes First Globally Certified Software to Achieve Prestigious SESIP Level 5 Security Certification](articles/杂项/2025-08-13-Android-s-pKVM-Becomes-First-Globally-Certified-Software-to.md) · [原文](http://security.googleblog.com/2025/08/Android-pKVM-Certified-SESIP-Level-5.html)

## 更新日志

<details>
<summary>展开查看（最新在上）</summary>

### 2026-11-19 · 2026-W52

- [findus / fault-injection-library：Pico Glitcher 软件框架 + 12 个 MCU 靶项目](articles/故障注入/2026-11-14-findus-fault-injection-library-Pico-Glitcher-软件框架-12-个-MCU-靶.md) —— 故障注入
- [ChipWhisperer 官方 Tips & Tricks：毛刺硬件选型、亚周期精度与触发排障](articles/故障注入/2026-11-14-ChipWhisperer-官方-Tips-Tricks-毛刺硬件选型-亚周期精度与触发排障.md) —— 故障注入
- [Raelize RapidBlockMode：PicoScope 分段采集 + GPIO 选通的对齐基础设施](articles/故障注入/2026-11-14-Raelize-RapidBlockMode-PicoScope-分段采集-GPIO-选通的对齐基础设施.md) —— 故障注入
- [GlitchGlück（WOOT'25）：用状态转移图引导硬件故障注入复现软件漏洞](articles/故障注入/2026-11-14-GlitchGl-ck-WOOT-25-用状态转移图引导硬件故障注入复现软件漏洞.md) —— 故障注入
- [Rainbow：Unicorn 指令级侧信道 / 故障注入仿真器（Ledger Donjon）](articles/故障注入/2026-11-14-Rainbow-Unicorn-指令级侧信道-故障注入仿真器-Ledger-Donjon.md) —— 故障注入
- [ot-sca：OpenTitan 官方 SCA + 故障注入评估框架](articles/故障注入/2026-11-14-ot-sca-OpenTitan-官方-SCA-故障注入评估框架.md) —— 故障注入
- [Cypherock EMFI Board：低成本开源电磁故障注入台架（附 7 款钱包 DUT）](articles/故障注入/2026-11-14-Cypherock-EMFI-Board-低成本开源电磁故障注入台架-附-7-款钱包-DUT.md) —— 故障注入
- [SiliconToaster：开源 0–1000V 电磁故障注入发生器（Ledger Donjon）](articles/故障注入/2026-11-14-SiliconToaster-开源-0-1000V-电磁故障注入发生器-Ledger-Donjon.md) —— 故障注入
- [ChipShover：EMFI/EM 探针的 XYZ 定位台](articles/故障注入/2026-11-14-ChipShover-EMFI-EM-探针的-XYZ-定位台.md) —— 故障注入
- [ESP32 EMFI 绕 Secure Boot（CVE-2020-13629 / 15048 系列）](articles/故障注入/2020-07-24-ESP32-EMFI-绕-Secure-Boot-CVE-2020-13629-15048-系列.md) —— 故障注入
- [ESP32 OTP Transfer EMFI：打 eFuse→shadow 寄存器的纯硬件搬运窗口](articles/故障注入/2023-03-10-ESP32-OTP-Transfer-EMFI-打-eFuse-shadow-寄存器的纯硬件搬运窗口.md) —— 故障注入
- [RP2350 预算级激光故障注入（Glasgow + DEF CON 33 Playground）](articles/故障注入/2026-11-14-RP2350-预算级激光故障注入-Glasgow-DEF-CON-33-Playground.md) —— 故障注入
- [ATECC608A 安全元件：两发激光故障读出 PIN hash（Coldcard Mk3 种子可窃）](articles/故障注入/2021-06-01-ATECC608A-安全元件-两发激光故障读出-PIN-hash-Coldcard-Mk3-种子可窃.md) —— 故障注入
- [SPHINCS+ 故障攻击与对策（TCHES 2023 官方 artifact）](articles/故障注入/2023-06-01-SPHINCS-故障攻击与对策-TCHES-2023-官方-artifact.md) —— 故障注入
- [RHme2 / RHme3 故障注入挑战解题合集（Riscure CTF）](articles/故障注入/2018-01-01-RHme2-RHme3-故障注入挑战解题合集-Riscure-CTF.md) —— 故障注入
- [STM32-TraceRip：不注入故障，用 CRC 状态步进重建受保护 flash](articles/固件解密/2025-06-10-STM32-TraceRip-不注入故障-用-CRC-状态步进重建受保护-flash.md) —— 固件解密
- [把故障注入仿真塞进开发流（Ledger Donjon：rust_fi + Rainbow + CI）](articles/故障注入/2026-11-14-把故障注入仿真塞进开发流-Ledger-Donjon-rust_fi-Rainbow-CI.md) —— 故障注入

### 2026-11-19 · 2026-W51

- [ESP32 全安全模式双毛刺：绕过 Secure Boot 并读出 FEK/SBK（CVE-2019-15894 / CVE-2019-17391）](articles/故障注入/2019-09-01-ESP32-全安全模式双毛刺-绕过-Secure-Boot-并读出-FEK-SBK-CVE-2019-15894-CVE.md) —— 故障注入
- [Espressif AR2023-007：ESP32-C3/C6 遭 CPA + 电压毛刺组合绕过 Secure Boot 与 Flash 加密](articles/故障注入/2024-01-05-Espressif-AR2023-007-ESP32-C3-C6-遭-CPA-电压毛刺组合绕过-Secure-Boot.md) —— 故障注入
- [Apple AirTag（nRF52832）电压毛刺解锁 APPROTECT 并转储固件](articles/智能家居/2026-11-14-Apple-AirTag-nRF52832-电压毛刺解锁-APPROTECT-并转储固件.md) —— 智能家居
- [GA100 数据中心 GPU PWMVID 电压毛刺实验台](articles/芯片安全/2026-11-14-GA100-数据中心-GPU-PWMVID-电压毛刺实验台.md) —— 芯片安全
- [Qualcomm IPQ40xx QSEE：EMFI 绕过安全范围检查实现任意 NULL 写](articles/故障注入/2021-06-07-Qualcomm-IPQ40xx-QSEE-EMFI-绕过安全范围检查实现任意-NULL-写.md) —— 故障注入
- [Trezor 穿壳 EMFI：毛刺 USB 栈长度检查读出 metadata/seed](articles/硬件钱包/2019-03-06-Trezor-穿壳-EMFI-毛刺-USB-栈长度检查读出-metadata-seed.md) —— 硬件钱包
- [STM32F2/F4 故障注入：EMFI/VFI 双档 RDP2→RDP1 + FPB 两毛刺读全片 flash](articles/硬件钱包/2026-11-14-STM32F2-F4-故障注入-EMFI-VFI-双档-RDP2-RDP1-FPB-两毛刺读全片-flash.md) —— 硬件钱包
- [Mercedes 防盗器 ECU 过压毛刺：短暂恢复被熔断的 JTAG](articles/车机/2025-06-01-Mercedes-防盗器-ECU-过压毛刺-短暂恢复被熔断的-JTAG.md) —— 车机
- [Chipolo 蓝牙追踪器：FI 绕调试锁 → 固件逆向 → 蓝牙栈 RCE](articles/智能家居/2024-12-27-Chipolo-蓝牙追踪器-FI-绕调试锁-固件逆向-蓝牙栈-RCE.md) —— 智能家居
- [PS Vita BootROM 毛刺：ChipWhisperer 时钟注入执行自定义 payload](articles/故障注入/2018-12-01-PS-Vita-BootROM-毛刺-ChipWhisperer-时钟注入执行自定义-payload.md) —— 故障注入
- [Zynq-7000 Secure Boot：故障注入攻破 RSA 位流认证（WOOT'24）](articles/安全启动/2024-08-13-Zynq-7000-Secure-Boot-故障注入攻破-RSA-位流认证-WOOT-24.md) —— 安全启动
- [bootl-attacks（CHES'21）：LPC1343 ROP / STM8 双毛刺 / Renesas 78K0 符号执行制导](articles/安全启动/2021-09-01-bootl-attacks-CHES-21-LPC1343-ROP-STM8-双毛刺-Renesas-78K0-符号执行.md) —— 安全启动
- [RP2350 光子发射引导激光 FI：恢复被永久关闭的 Secure Debug](articles/安全启动/2026-11-13-RP2350-光子发射引导激光-FI-恢复被永久关闭的-Secure-Debug.md) —— 安全启动
- [RP2350 OTP 毛刺：割断 USB_OTP_VDD 后在 ~1.75ms 窗口篡改 OTP](articles/故障注入/2026-11-14-RP2350-OTP-毛刺-割断-USB_OTP_VDD-后在-1-75ms-窗口篡改-OTP.md) —— 故障注入
- [MC9S12/HCS12 复位安全评估窗口毛刺：解锁 BDM 读全片 flash](articles/车机/2026-11-14-MC9S12-HCS12-复位安全评估窗口毛刺-解锁-BDM-读全片-flash.md) —— 车机
- [压电打火机 EMFI 打 DRAM 总线：笔记本 Linux 提权 root](articles/芯片安全/2024-10-07-压电打火机-EMFI-打-DRAM-总线-笔记本-Linux-提权-root.md) —— 芯片安全

### 2026-11-19 · 2026-W50

- [Glitch in the Sky: Exploiting Voltage Fault Injection in UAV Flight Controllers](articles/故障注入/2026-04-17-Glitch-in-the-Sky-Exploiting-Voltage-Fault-Injection-in-UAV.md) —— 故障注入
- [One Glitch to Rule Them All: Fault Injection Attacks Against AMD's Secure Encrypted Virtualization](articles/故障注入/2021-08-10-One-Glitch-to-Rule-Them-All-Fault-Injection-Attacks-Against.md) —— 故障注入
- [Oops..! I Glitched It Again! How to Multi-Glitch the Glitching-Protections on ARM TrustZone-M](articles/故障注入/2023-02-14-Oops-I-Glitched-It-Again-How-to-Multi-Glitch-the-Glitching-P.md) —— 故障注入
- [Injecting Software Vulnerabilities with Voltage Glitching](articles/故障注入/2019-02-14-Injecting-Software-Vulnerabilities-with-Voltage-Glitching.md) —— 故障注入
- [Physical and Software Based Fault Injection Attacks Against TEEs in Mobile Devices: A Systemisation of Knowledge](articles/故障注入/2024-11-22-Physical-and-Software-Based-Fault-Injection-Attacks-Against.md) —— 故障注入
- [The Forgotten Threat of Voltage Glitching: A Case Study on Nvidia Tegra X2 SoCs](articles/故障注入/2021-08-13-The-Forgotten-Threat-of-Voltage-Glitching-A-Case-Study-on-Nv.md) —— 故障注入
- [Keyless Entry: Breaking and Entering eMMC RPMB with EMFI](articles/故障注入/2025-11-27-Keyless-Entry-Breaking-and-Entering-eMMC-RPMB-with-EMFI.md) —— 故障注入
- [NonSense: On the (In)security of FPGA Anti-tamper Sensors](articles/故障注入/2026-11-12-NonSense-On-the-In-security-of-FPGA-Anti-tamper-Sensors.md) —— 故障注入
- [EM-Fault It Yourself: Building a Replicable EMFI Setup for Desktop and Server Hardware](articles/故障注入/2022-09-20-EM-Fault-It-Yourself-Building-a-Replicable-EMFI-Setup-for-De.md) —— 故障注入
- [EMMap: A Systematic Framework for Spatial EMFI Mapping and Fault Classification on Microcontrollers](articles/故障注入/2025-12-09-EMMap-A-Systematic-Framework-for-Spatial-EMFI-Mapping-and-Fa.md) —— 故障注入
- [Honest to a Fault: Root-Causing Fault Attacks with Pre-Silicon RISC Pipeline Characterization](articles/故障注入/2025-03-05-Honest-to-a-Fault-Root-Causing-Fault-Attacks-with-Pre-Silico.md) —— 故障注入
- [TriSweep: A Four-Drone Swarm Framework for Electromagnetic Side-Channel Analysis](articles/芯片安全/2026-05-21-TriSweep-A-Four-Drone-Swarm-Framework-for-Electromagnetic-Si.md) —— 芯片安全
- [Fuzz'EMup: Leveraging EM Side-Channel Emanation to Guide Black-Box Embedded Firmware Fuzzing](articles/FUZZ/2026-07-17-Fuzz-EMup-Leveraging-EM-Side-Channel-Emanation-to-Guide-Blac.md) —— FUZZ
- [PowerFuzz: Power-Based Black-Box Firmware Fuzzing](articles/FUZZ/2026-06-23-PowerFuzz-Power-Based-Black-Box-Firmware-Fuzzing.md) —— FUZZ
- [Side-Channel Attacks on RISC-V Processors: Current Progress, Challenges, and Opportunities](articles/芯片安全/2021-06-16-Side-Channel-Attacks-on-RISC-V-Processors-Current-Progress-C.md) —— 芯片安全
- [SoK: Where's the "up"?! A Comprehensive (bottom-up) Study on the Security of Arm Cortex-M Systems](articles/芯片安全/2024-01-27-SoK-Where-s-the-up-A-Comprehensive-bottom-up-Study-on-the-Se.md) —— 芯片安全
- [One Exploit to Rule them All? On the Security of Drop-in Replacement and Counterfeit Microcontrollers](articles/芯片安全/2020-08-21-One-Exploit-to-Rule-them-All-On-the-Security-of-Drop-in-Repl.md) —— 芯片安全
- [Automotive HSMs - Architectural Challenges and Security Implications](articles/车机/2026-08-25-Automotive-HSMs-Architectural-Challenges-and-Security-Implic.md) —— 车机
- [Deep dip teardown of tubeless insulin pump](articles/杂项/2017-09-18-Deep-dip-teardown-of-tubeless-insulin-pump.md) —— 杂项
- [Hardware Security Evaluation of MAX 10 FPGA](articles/芯片安全/2019-10-11-Hardware-Security-Evaluation-of-MAX-10-FPGA.md) —— 芯片安全
- [Lessons from the Hardware Hacking Competitions: Verification Techniques, Findings, and Insights](articles/杂项/2026-08-23-Lessons-from-the-Hardware-Hacking-Competitions-Verification.md) —— 杂项
- [BugWhisperer: Fine-Tuning LLMs for SoC Hardware Vulnerability Detection](articles/芯片安全/2025-05-28-BugWhisperer-Fine-Tuning-LLMs-for-SoC-Hardware-Vulnerability.md) —— 芯片安全
- [Glitched on Earth by Humans: A Black-Box Security Evaluation of the SpaceX Starlink User Terminal](articles/卫星安全/2022-08-11-Glitched-on-Earth-by-Humans-A-Black-Box-Security-Evaluation.md) —— 卫星安全
- [SATCOM Terminals: Hacking by Air, Sea, and Land](articles/卫星安全/2014-08-06-SATCOM-Terminals-Hacking-by-Air-Sea-and-Land.md) —— 卫星安全
- [SpyChain: Multi-Vector Supply Chain Attacks on Small Satellite Systems](articles/卫星安全/2025-10-08-SpyChain-Multi-Vector-Supply-Chain-Attacks-on-Small-Satellit.md) —— 卫星安全
- [SatBleed: Security of Commoditized Communication Modules in Satellites](articles/卫星安全/2026-10-05-SatBleed-Security-of-Commoditized-Communication-Modules-in-S.md) —— 卫星安全
- [Systematic Security Analysis of the Iridium Satellite Radio Link](articles/卫星安全/2026-03-12-Systematic-Security-Analysis-of-the-Iridium-Satellite-Radio.md) —— 卫星安全
- [JANUS: Denial-of-Service Attack Against Beam Hopping in LEO Satellite Networks](articles/卫星安全/2026-09-17-JANUS-Denial-of-Service-Attack-Against-Beam-Hopping-in-LEO-S.md) —— 卫星安全
- [Silent Subversion: Sensor Spoofing Attacks via Supply Chain Implants in Satellite Systems](articles/卫星安全/2026-03-11-Silent-Subversion-Sensor-Spoofing-Attacks-via-Supply-Chain-I.md) —— 卫星安全
- [Updated Standard for Secure Satellite Communications: Analysis of Satellites, Attack Vectors, Existing Standards, and Enterprise and Security Architectures](articles/卫星安全/2023-10-29-Updated-Standard-for-Secure-Satellite-Communications-Analysi.md) —— 卫星安全
- [SATversary: Adversarial Attacks and Defenses for Satellite Fingerprinting](articles/卫星安全/2025-06-06-SATversary-Adversarial-Attacks-and-Defenses-for-Satellite-Fi.md) —— 卫星安全
- [Google Wifi Pro Glitching from Root to EL3 (Part 1: Characterization)](articles/故障注入/2026-05-01-Google-Wifi-Pro-Glitching-from-Root-to-EL3-Part-1-Characteri.md) —— 故障注入
- [Google Wifi Pro Glitching from Root to EL3 (Part 3: Arbitrary Code Execution)](articles/故障注入/2026-05-20-Google-Wifi-Pro-Glitching-from-Root-to-EL3-Part-3-Arbitrary.md) —— 故障注入
- [setresuid(⚡): Glitching Google's TV Streamer from adb to Root](articles/故障注入/2026-04-01-setresuid-Glitching-Google-s-TV-Streamer-from-adb-to-Root.md) —— 故障注入
- [AI-FI: Giving Claude Code Glitch Skills for Bypassing Secure Boot](articles/故障注入/2026-06-01-AI-FI-Giving-Claude-Code-Glitch-Skills-for-Bypassing-Secure.md) —— 故障注入
- [Triple Exploit Chain with Laser Fault Injection on a Secure Element](articles/故障注入/2024-10-01-Triple-Exploit-Chain-with-Laser-Fault-Injection-on-a-Secure.md) —— 故障注入
- [Pull the Plug: FIRESTARTER Survives Patches, Reboots, and Your Incident Response Plan](articles/防火墙/2026-05-07-Pull-the-Plug-FIRESTARTER-Survives-Patches-Reboots-and-Your.md) —— 防火墙
- [Your KVM is the Weak Link: How $30 Devices Can Own Your Entire Network](articles/杂项/2026-03-17-Your-KVM-is-the-Weak-Link-How-30-Devices-Can-Own-Your-Entire.md) —— 杂项
- [Fake Kernel Threads Are Hiding Backdoors on Linux Servers and Appliances](articles/杂项/2026-10-20-Fake-Kernel-Threads-Are-Hiding-Backdoors-on-Linux-Servers-an.md) —— 杂项
- [The Explosion of Hardware-Hacking Devices](articles/杂项/2025-02-08-The-Explosion-of-Hardware-Hacking-Devices.md) —— 杂项
- [Supporting Rowhammer research to protect the DRAM ecosystem](articles/芯片安全/2025-09-16-Supporting-Rowhammer-research-to-protect-the-DRAM-ecosystem.md) —— 芯片安全
- [Further Hardening Android GPUs](articles/芯片安全/2025-12-10-Further-Hardening-Android-GPUs.md) —— 芯片安全
- [Android’s pKVM Becomes First Globally Certified Software to Achieve Prestigious SESIP Level 5 Security Certification](articles/杂项/2025-08-13-Android-s-pKVM-Becomes-First-Globally-Certified-Software-to.md) —— 杂项
- [Don't let TEEs break your MPC](articles/芯片安全/2026-09-25-Don-t-let-TEEs-break-your-MPC.md) —— 芯片安全
- [Another Crack in the Chain of Trust: Uncovering (Yet Another) Secure Boot Bypass](articles/安全启动/2025-06-10-Another-Crack-in-the-Chain-of-Trust-Uncovering-Yet-Another-S.md) —— 安全启动
- [Broken Trust: Fixed Supermicro BMC Bug Gains a New Life in Two New Vulnerabilities](articles/安全启动/2025-09-24-Broken-Trust-Fixed-Supermicro-BMC-Bug-Gains-a-New-Life-in-Tw.md) —— 安全启动
- [How an Old Bug in Lighttpd Gained New Life in AMI BMC, Including Lenovo and Intel products](articles/安全启动/2025-11-19-How-an-Old-Bug-in-Lighttpd-Gained-New-Life-in-AMI-BMC-Includ.md) —— 安全启动
- [Clevo Boot Guard Keys Leaked in Update Package](articles/安全启动/2025-03-20-Clevo-Boot-Guard-Keys-Leaked-in-Update-Package.md) —— 安全启动
- [LogoFAIL Exploited to Deploy Bootkitty, the first UEFI bootkit for Linux](articles/安全启动/2024-11-29-LogoFAIL-Exploited-to-Deploy-Bootkitty-the-first-UEFI-bootki.md) —— 安全启动
- [Vulnerability REsearch using VulHunt](articles/Openwrt/2026-02-20-Vulnerability-REsearch-using-VulHunt.md) —— Openwrt

### 2026-11-19 · 2026-W48

- [PHP2Shell Exploitation on Check Point Gateway](articles/防火墙/2026-11-12-PHP2Shell-Exploitation-on-Check-Point-Gateway.md) —— 防火墙
- [Active Exploitation of May 2026 PAN-OS CVE-2026-0257 (Updated October 20)](articles/防火墙/2026-10-21-Active-Exploitation-of-May-2026-PAN-OS-CVE-2026-0257-Updated.md) —— 防火墙
- [Here We Go Again (Citrix NetScaler DTLS Preauth Memory Overflow CVE-2026-88772)](articles/防火墙/2026-09-29-Here-We-Go-Again-Citrix-NetScaler-DTLS-Preauth-Memory-Overfl.md) —— 防火墙
- [Oh Look, The Foot Gun Went Off Again (Citrix NetScaler PreAuth Command Injection CVE-2026-88771)](articles/防火墙/2026-09-28-Oh-Look-The-Foot-Gun-Went-Off-Again-Citrix-NetScaler-PreAuth.md) —— 防火墙
- [CVE-2024-0244 – A heap buffer overflow in the Canon MF753Cdw printer](articles/打印机/2026-09-24-CVE-2024-0244-A-heap-buffer-overflow-in-the-Canon-MF753Cdw-p.md) —— 打印机
- [Is This A Joke? In The Auth Header? (F5 BIG-IP UnAuth Heap-Overflow to RCE CVE-2026-94127)](articles/防火墙/2026-09-24-Is-This-A-Joke-In-The-Auth-Header-F5-BIG-IP-UnAuth-Heap-Over.md) —— 防火墙
- [You’re Back In The Room (Citrix NetScaler Pre-Auth RCE CVE-2026-8452(?))](articles/防火墙/2026-08-14-You-re-Back-In-The-Room-Citrix-NetScaler-Pre-Auth-RCE-CVE-20.md) —— 防火墙
- [Can AI Hack Firmware? Evaluating LLMs on UEFI Vulnerability Discovery](articles/安全启动/2026-08-12-Can-AI-Hack-Firmware-Evaluating-LLMs-on-UEFI-Vulnerability-D.md) —— 安全启动
- [Bypassing Android Hardware Attestation from the Analyst's Chair](articles/芯片安全/2026-08-11-Bypassing-Android-Hardware-Attestation-from-the-Analyst-s-Ch.md) —— 芯片安全
- [Hidden beneFITs: Bypassing Signature Verification in U-Boot SPL](articles/安全启动/2026-08-06-Hidden-beneFITs-Bypassing-Signature-Verification-in-U-Boot-S.md) —— 安全启动
- [Fit for Detection: Hunting U-Boot Vulnerabilities at Scale](articles/安全启动/2026-07-16-Fit-for-Detection-Hunting-U-Boot-Vulnerabilities-at-Scale.md) —— 安全启动
- [Unfit to Boot: Breaking U-Boot's FIT Signature Verification](articles/安全启动/2026-07-09-Unfit-to-Boot-Breaking-U-Boot-s-FIT-Signature-Verification.md) —— 安全启动
- [CitrixBleed To Infinity And Beyond (Citrix NetScaler Pre-Auth Memory Overread CVE-2026-8451)](articles/防火墙/2026-07-01-CitrixBleed-To-Infinity-And-Beyond-Citrix-NetScaler-Pre-Auth.md) —— 防火墙
- [Black Box Probing: a Security Analysis of Xiaomi's MJA1 Secure Chip](articles/芯片安全/2026-06-18-Black-Box-Probing-a-Security-Analysis-of-Xiaomi-s-MJA1-Secur.md) —— 芯片安全
- [Marking Your Own Homework (Check Point Remote Access VPN IKEv1 Authentication Bypass CVE-2026-50751)](articles/防火墙/2026-06-12-Marking-Your-Own-Homework-Check-Point-Remote-Access-VPN-IKEv.md) —— 防火墙
- [More Evidence That Words Don't Mean What We Thought They Meant (Ivanti Sentry Pre-Auth OS Command Injection CVE-2026-10520)](articles/防火墙/2026-06-10-More-Evidence-That-Words-Don-t-Mean-What-We-Thought-They-Mea.md) —— 防火墙
- [Flicker and fall: rooting the Philips Hue Bridge both remotely and wirelessly](articles/智能家居/2026-06-08-Flicker-and-fall-rooting-the-Philips-Hue-Bridge-both-remotel.md) —— 智能家居
- [Bringing Rust to the Pixel Baseband](articles/基站/2026-04-10-Bringing-Rust-to-the-Pixel-Baseband.md) —— 基站
- [Have you patched? Are you sure? The story of the sticky Supermicro BMC bugs](articles/安全启动/2026-01-26-Have-you-patched-Are-you-sure-The-story-of-the-sticky-Superm.md) —— 安全启动
- [Missing Mitigations: Inside The Security Gap in UEFI Firmware](articles/安全启动/2025-10-17-Missing-Mitigations-Inside-The-Security-Gap-in-UEFI-Firmware.md) —— 安全启动
- [Signed and Dangerous: BYOVD Attacks on Secure Boot](articles/安全启动/2025-09-10-Signed-and-Dangerous-BYOVD-Attacks-on-Secure-Boot.md) —— 安全启动
- [Ruckus Unleashed: Multiple vulnerabilities exploited](articles/防火墙/2025-07-21-Ruckus-Unleashed-Multiple-vulnerabilities-exploited.md) —— 防火墙
- [Ghost in the Controller: Abusing Supermicro BMC Firmware Verification](articles/安全启动/2025-07-02-Ghost-in-the-Controller-Abusing-Supermicro-BMC-Firmware-Veri.md) —— 安全启动
- [Streaming Zero-Fi Shells to Your Smart Speaker](articles/智能家居/2025-06-11-Streaming-Zero-Fi-Shells-to-Your-Smart-Speaker.md) —— 智能家居
- [Exploiting the Synology DiskStation with Null-byte Writes](articles/杂项/2025-04-23-Exploiting-the-Synology-DiskStation-with-Null-byte-Writes.md) —— 杂项
- [UEFI Bootkit Hunting: In-Depth Search for Unique Code Behavior](articles/安全启动/2025-03-13-UEFI-Bootkit-Hunting-In-Depth-Search-for-Unique-Code-Behavio.md) —— 安全启动
- [CVE-2024-36435 Deep-Dive: The Year's Most Critical BMC Security Flaw](articles/安全启动/2024-09-26-CVE-2024-36435-Deep-Dive-The-Year-s-Most-Critical-BMC-Securi.md) —— 安全启动
- [Pwn2Own Automotive 2024: Hacking the Autel MaxiCharger](articles/充电桩/2024-09-05-Pwn2Own-Automotive-2024-Hacking-the-Autel-MaxiCharger.md) —— 充电桩
- [Pwn2Own Automotive 2024: Hacking the JuiceBox 40](articles/充电桩/2024-08-29-Pwn2Own-Automotive-2024-Hacking-the-JuiceBox-40.md) —— 充电桩
- [Pwn2Own Automotive 2024: Hacking the ChargePoint Home Flex (and their cloud...)](articles/充电桩/2024-08-08-Pwn2Own-Automotive-2024-Hacking-the-ChargePoint-Home-Flex-an.md) —— 充电桩

### 2026-11-16 · 2026-W47

- 重启仓库：新增 8 篇 IoT / 固件 / 边缘设备研究快照（每篇附「核心 / 价值 / 难度」收录理由）
- 新增 `tools/crawl.py` 与 `tools/publish.py`，此后每周一自动抓取 → 复审 → 归档 → 推送

### 2025-03 ~ 2025-04

- 2025-03-02：建立仓库与分类（固件解密、摄像头、OpenWrt、无人机、防火墙、智能音箱、基站、打印机、安全启动、车机、绕过 ASLR）
- 2025-03-09：补充摄像头、无人机、LuCI 漏洞挖掘，新增 Contributors
- 2025-03-17：补充无人机、绕过 ASLR、故障注入
- 2025-03-30 / 04-07 / 04-14 / 04-21：常规补更（原记录较简略）

</details>

## 收录标准

- **收**：攻击角度新颖 —— 新攻击面、新利用链、反直觉的设计/协议缺陷
- **收**：利用难度极高 —— ASLR/堆布局、竞态、物理接触、侧信道与毛刺、Secure Boot 绕过、baseband、固件密钥恢复
- **不收**：新闻通稿、厂商补丁公告、营销/榜单/趋势、纯 Web 应用层、CTF writeup

## 自动更新

每周一 10:00 自动执行 `tools/crawl.py` → 复审 → `tools/publish.py`（移动快照、挂到对应板块、写更新日志、重建索引）。
抓取全程串行、请求间隔 ≥8s、遵守 `robots.txt`，不登录、不绕过任何访问控制或付费墙；
单篇快照 ≤150KB、单次下载 ≤5MB、仓库总量 ≤60MB。信息源与参数见 [tools/sources.json](tools/sources.json)。

## 贡献

欢迎 PR 补充文章，请附一句「为什么值得收」。

## Contributors

<div align="center">

  <a href="https://www.cnblogs.com/ve1kcon">
    <img src="https://pic1.imgdb.cn/item/67cdb235066befcec6e23553.jpg" alt="ve1kcon" width="100" height="100">
  </a>
  <a href="https://github.com/glkfc">
    <img src="https://pic1.imgdb.cn/item/67cdb48c066befcec6e235c8.jpg" alt="jfkk" width="100" height="100">
  </a>

</div>
