---
title: "SS7: Locate. Track. Manipulate.：信令网上的定位与监听"
source: "31C3"
url: https://media.ccc.de/v/31c3_-_6249_-_en_-_saal_1_-_201412271715_-_ss7_locate_track_manipulate_-_tobias_engel
published: 2014-12-27
fetched: 2026-11-19T05:40:43.175Z
category: "基站"
score: 0
keywords: []
sha256: f9c02d04e77e9e2a8ec96d85c517c592795aadd16d90a3617e2989f4cb665d87
bytes: 804
truncated: false
body_mode: notes
kind: practical
status: published
published_at: 2026-11-19T13:40:51.833712+08:00
---

# SS7: Locate. Track. Manipulate.：信令网上的定位与监听

> 来源：31C3 · 2014-12-27 · [原文](https://media.ccc.de/v/31c3_-_6249_-_en_-_saal_1_-_201412271715_-_ss7_locate_track_manipulate_-_tobias_engel)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：SS7 的“信任互联”模型没有对查询来源做有效鉴别，定位/监听请求可被任意互联方发出。
- **价值**：运营商信令网是最被低估的攻击面，也是基站/核心网安全的第一课。
- **难度**：中 —— 需要 SS7 接入或合作方，但技术门槛低于物理攻击。

通过 SS7 信令网，攻击者可从世界任何地方定位手机（精度可达约 50 米）、绘制移动轨迹、拦截短信与通话，无需接触目标。
