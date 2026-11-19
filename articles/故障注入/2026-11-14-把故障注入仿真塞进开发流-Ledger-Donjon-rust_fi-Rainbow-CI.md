---
title: "把故障注入仿真塞进开发流（Ledger Donjon：rust_fi + Rainbow + CI）"
source: "Ledger Donjon"
url: https://github.com/Ledger-Donjon/fault_injection_checks_demo
published: 2026-11-14
fetched: 2026-11-19T05:26:20.405Z
category: "故障注入"
score: 0
keywords: []
sha256: 8a9e8bed86d1ef0917fa04111d10c2abe1317a1c9760f7f3679c28e6cfe2952f
bytes: 1243
truncated: false
body_mode: notes
kind: practical
status: published
published_at: 2026-11-19T13:26:46.419198+08:00
---

# 把故障注入仿真塞进开发流（Ledger Donjon：rust_fi + Rainbow + CI）

> 来源：Ledger Donjon · 2026-11-14 · [原文](https://github.com/Ledger-Donjon/fault_injection_checks_demo)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：注入点＝仿真级（Rainbow Unicorn 钩子）对 PIN 校验函数的每条指令做单故障；窗口＝遍历全指令空间；触发＝仿真断言/指令事件；判定＝断言被故障骗过即失败点（faulted vs 预期 diff）。
- **价值**：让“这个函数抗不抗故障”变成一条命令——故障注入从研究课题走向日常工程实践。
- **难度**：中 —— Rust + Python 环境，按 README 几步即可跑。

## 方法论启示

- FI 的最终形态是 CI：每次提交都跑一遍故障扫描，把问题挡在流片前。
- 抗故障类型（fault_hardened）把“防御”变成可复用的库，而不是一次性补丁。

用自定义 assert_eq! 宏（rust_fi）+ Rainbow 仿真 + fi_check.py 自动对所有 test_fi_* 函数做单故障扫描，addr2line 把故障指令映射回 Rust 源码行；VS Code 任务一键跑“全部/安全函数”，fault_hardened/ 提供抗故障类型作对照。
