---
title: "压电打火机 EMFI 打 DRAM 总线：笔记本 Linux 提权 root"
source: "David Buchanan"
url: https://www.da.vidbuchanan.co.uk/blog/dram-emfi.html
published: 2024-10-07
fetched: 2026-11-19T05:21:54.654Z
category: "芯片安全"
score: 0
keywords: []
sha256: e6180aa59040b26225314a74bbba706df2b2bb3d558a137bfe1c2e57f24d2063
bytes: 1223
truncated: false
body_mode: notes
status: published
published_at: 2026-11-19T13:22:06.082437+08:00
---

# 压电打火机 EMFI 打 DRAM 总线：笔记本 Linux 提权 root

> 来源：David Buchanan · 2024-10-07 · [原文](https://www.da.vidbuchanan.co.uk/blog/dram-emfi.html)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：注入点＝SODIMM DQ 数据线（打的是总线传输而非存储内容，与 Rowhammer 本质不同）；窗口＝几乎没有时序控制，改用“占用率饱和”——让目标访问占满总线，使随机异步毛刺几乎必然落在可利用访问上；触发＝无（手指按压打火机）；判定＝spray 中出现非 victim 对象指针（任意读写原语），最终内核提权成功。
- **价值**：把 EMFI 从实验室台架拉低到“打火机级别”，并给出“提高目标访问占比”这一通用替代方案，对无触发/异步毛刺场景极有启发。
- **难度**：中 —— 器材极其便宜，但需要精确的对象布局设计与大量重试。

在 SODIMM 的一条数据线上焊“天线”（15Ω + 导线），用普通压电打火机在旁边放电即可稳定翻转特定位：先打 CPython bytes 对象指针获得任意读写，再打 Linux 内核，全程零专用设备拿到 root。
