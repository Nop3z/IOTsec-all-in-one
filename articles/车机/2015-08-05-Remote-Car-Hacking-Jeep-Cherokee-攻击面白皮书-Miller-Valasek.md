---
title: "Remote Car Hacking：Jeep Cherokee 攻击面白皮书（Miller & Valasek）"
source: "IOActive / Black Hat 2015"
url: https://ioactive.com/wp-content/uploads/2018/05/IOActive_Remote_Car_Hacking-1.pdf
published: 2015-08-05
fetched: 2026-11-23T05:25:20.401Z
category: "车机"
score: 0
keywords: ["classic"]
sha256: 946ccca6ee4a2c1261361c6e91ac850a9f9e4de15011e003bca54eb08891827f
bytes: 1437
truncated: false
body_mode: notes
kind: practical
status: published
published_at: 2026-11-23T13:25:28.351751+08:00
---

# Remote Car Hacking：Jeep Cherokee 攻击面白皮书（Miller & Valasek）

> 来源：IOActive / Black Hat 2015 · 2015-08-05 · [原文](https://ioactive.com/wp-content/uploads/2018/05/IOActive_Remote_Car_Hacking-1.pdf)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：白皮书把“一辆车有多少个远程入口”逐一列出并实测，给出从 telematic 到 CAN 的利用路径；这正是 2015 年 140 万辆 Jeep 召回的源头。
- **价值**：汽车安全的“零号案例”：确立了车联网威胁模型（远程入口 → 网关 → 安全关键总线），后续几乎所有车厂安全评估都以它为模板。
- **难度**：极高 —— 需要拆车、固件逆向与 CAN 总线分析。

Miller 与 Valasek 系统梳理 2014 款 Jeep Cherokee 的远程攻击面：蜂窝（Sprint）、无线电（AM/FM/Satellite）、蓝牙、Wi-Fi 等入口，最终通过车机 → CAN 总线实现远程操控（含 2015 年著名的远程刹车演示）。
