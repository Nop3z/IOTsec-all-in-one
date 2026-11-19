---
title: "Hacking Robots Before Skynet（技术附录）：工业与协作机器人的攻击面"
source: "IOActive"
url: https://www.ioactive.com/wp-content/uploads/pdfs/Hacking-Robots-Before-Skynet-Technical-Appendix.pdf
published: 2017-07-01
fetched: 2026-11-19T05:40:43.175Z
category: "机器人"
score: 0
keywords: []
sha256: e6e7baed576be7e66a9a7d3e91eff5114df83473f537343817d422ff567b0ca3
bytes: 828
truncated: false
body_mode: notes
status: published
published_at: 2026-11-19T13:40:51.833712+08:00
---

# Hacking Robots Before Skynet（技术附录）：工业与协作机器人的攻击面

> 来源：IOActive · 2017-07-01 · [原文](https://www.ioactive.com/wp-content/uploads/pdfs/Hacking-Robots-Before-Skynet-Technical-Appendix.pdf)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：机器人控制器普遍缺乏认证与完整性校验，攻击者可直接改写运动程序；部分厂商的 SDK/服务默认开放。
- **价值**：机器人安全的开创性研究，第一次系统说明“网络漏洞 → 物理伤害”的路径。
- **难度**：中高 —— 需要机器人控制器/工业协议知识。

对多款工业/协作机器人做安全评估的技术附录：认证缺失、明文协议、可远程下发的运动指令，以及可利用的具体接口。
