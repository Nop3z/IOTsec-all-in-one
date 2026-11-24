---
title: "Dennis Giese：扫地机器人安全研究的长期档案"
source: "Dennis Giese"
url: https://dontvacuum.me/
published: 
fetched: 2026-11-24T20:29:01.595391+08:00
category: "机器人"
score: 0
keywords: []
sha256: 886ffdc147a0e6442130f9db8ea0252a59827f28535d67bac008b09e54e69f56
bytes: 4615
truncated: false
body_mode: fulltext
kind: practical
status: published
published_at: 2026-11-24T20:30:46.008546+08:00
---

# Dennis Giese：扫地机器人安全研究的长期档案

> 来源：Dennis Giese · 2024-01-01 · [原文](https://dontvacuum.me/)
> 归档用于安全研究参考；版权归原作者所有。
> 原文未标注发布日期（或为持续维护的资源），本条目日期按归档日期记录。

## 收录理由

- **核心**：作者多年对扫地机器人（小米、Roborock 等）做安全评估的汇总入口：root 方法、云协议分析、传感器与隐私问题、以及给厂商的披露记录。
- **价值**：做机器人安全研究最完整的个人档案，覆盖“固件→云→传感器”三层，可作为该方向的路线图。
- **难度**：中 —— 索引型，按需深入。

Welcome! callsign: KC1KLN
 contact: dgiese[at]dontvacuum.me
twitter: [dgi_DE](https://twitter.com/dgi_DE) (For communication and some announcements)
telegram: [dgiese](https://t.me/dgiese) (I do not provide enduser support here)
 Linkedin: ["dennis-giese"](https://www.linkedin.com/in/dennis-giese/)
 My Youtube channel with my playlist: [My Channel](https://www.youtube.com/channel/UCPbtUQXdhs9RrN0vOQAwVdw)

 I am an independent Security and Privacy researcher.
 My main research interest is the security and privacy of embedded systems and IoT devices. I presented my research at the Chaos Communication Congress, REcon BRX, HITCON, NULLCON, and DEFCON.

 You might know me from my work at [Northeastern University](https://www.neu.edu) in the [Khoury College of Computer Science](https://www.khoury.northeastern.edu/), with Prof. Guevara Noubir as my advisor. I was the teamlead for the [Northeastern University CTF team "NUSEC"](https://nusec.us). I was a TA for CY 5770 "Software Vulnerabilities and Security" (Engin Kirda, Spring 2021), CY 4740 "Network security" (Guevara Noubir, Fall 2022), CS 3740 "Systems Security" (Spring 2023, Kaan Onarlioglu) and CY 5770 "Software Vulnerabilities and Security" (Summer 2023, Kaan Onarlioglu).

---

 [My talks](https://dontvacuum.me/talks/) My 34C3, Recon BRX, HITCON, DEFCON and BeVX talks
 [My papers](https://dontvacuum.me/papers/) My academic papers
 [List of media (interviews, articles, etc) about my projects](https://dontvacuum.me/media.html)
 Some of my projects: [Robot info](https://robotinfo.dev) A comparison of vacuum robots I analyzed
 [IoT teardowns](https://dontvacuum.me/teardowns/) I started a collection of teardown pictures of my devices
 [Dustcloud Repo](https://github.com/dgiese/dustcloud) Repo contains all source codes that are required to run the Dustcloud implementation and to create custom firmware / audio images for your Roborock/Xiaomi robot (v1,s5).
 [Dustcloud-documentation Repo](https://github.com/dgiese/dustcloud-documentation) Repo for Documentation (Photos, Datasheets) of Xiaomi devices
 [Dustbuilder](https://builder.dontvacuum.me) Online tool for creation of custom rooted firmware for your Xiaomi/Roborock vacuum robots.
 [Dustbuilder NEEO](https://builder.dontvacuum.me/neeo.html) Online tool for custom rooted firmware for NEEO Brains. [[More information]](https://twitter.com/dgi_DE/status/1267941534470680577)
 [Flash forensics of crashed rockets](https://dontvacuum.me/rocketflashrecovery/index.html) A story about how I extracted data of a broken flash chip using salt water
 [Security Analysis of the Xiaomi IoT Ecosystem](https://dontvacuum.me/thesis/) My TU Darmstadt Master thesis (2019)
 My other activities: [MIT Rocket Team](http://rocketry.mit.edu/) (as responsible engineer for Radio stuff, fixer of broken PCBs and [forensic guy ;)](https://dontvacuum.me/rocketflashrecovery/index.html)
 [MIT Radio Society](http://w1mx.mit.edu/) (served as Vice President W1XM 2019/2020)
 Former stuff I did / Affiliations: [Northeastern Team in the MITRE eCTF](https://mitrecyberacademy.org/competitions/embedded/) (Me being team captain since 2017, winning in 2019, 2020 and 2021)
 Lockpicking/Physec: I ran some lockpicking and physical security activities at Northeastern University
 [Fachschaft Physik TU Darmstadt](https://www.fachschaft.physik.tu-darmstadt.de/) (The physics student council of the TU Darmstadt)
 [Saturday Morning Physics@TU Darmstadt](http://satmorphy.de/) (helped there between 2011 and 2016)
 [Sportsfreunde der Sperrtechnik Deutschland e.V.](http://www.ssdev.org) (German Lockpicking Society)
 [Studienstiftung des deutschen Volkes](https://www.studienstiftung.de/) (German scholarship foundation of which I received a scholarship)
 [Harvard-MIT Mathematics Tournament](http://hmmt.co/) (served as a Software Officer in 2019/2020)
