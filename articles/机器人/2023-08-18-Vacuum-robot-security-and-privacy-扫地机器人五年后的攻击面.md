---
title: "Vacuum robot security and privacy：扫地机器人五年后的攻击面"
source: "camp2023"
url: https://media.ccc.de/v/camp2023-57158-vacuum_robot_security_and_privacy
published: 2023-08-18
fetched: 2026-11-19T05:40:43.175Z
category: "机器人"
score: 0
keywords: []
sha256: eaae1653d3baaa18b359698fb2935d72142d7d3b03f266652762919920b193ba
bytes: 728
truncated: false
body_mode: notes
status: published
published_at: 2026-11-19T13:40:51.833712+08:00
---

# Vacuum robot security and privacy：扫地机器人五年后的攻击面

> 来源：camp2023 · 2023-08-18 · [原文](https://media.ccc.de/v/camp2023-57158-vacuum_robot_security_and_privacy)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：传感器（激光/摄像头/超声）既能建图也能侧写室内环境；云连接让攻击者可远程触达。
- **价值**：消费级机器人最贴近真实家庭的攻击面分析。
- **难度**：中 —— 需要拆机与云端接口分析。

五年前用“笨传感器”定位用户的方法，如今被现实超越：现代扫地机器人带多摄像头、激光雷达与云端连接，隐私与攻击面同步放大。
