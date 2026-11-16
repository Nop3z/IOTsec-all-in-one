# 📡 IOTsec-all-in-one


本项目致力于 **收集和整理 IoT 安全（IoTsec）相关资料**，分类依据 **设备类型** 或 **技术点**，  
为研究人员、开发者提供有价值的安全研究参考(内容不会太基础)。

# ⭐️催更


📌 **目标**：
- 持续收集 IoT 安全相关资料
- 以 **设备类型** 或 **技术点** 分类整理
- **每周至少更新一次**（1 Week 1 Update）
- 后期对每篇文章 **提炼关键词** 和 **总结核心内容**

## 🤖 自动化周更（Weekly Bot）

每周自动扫描一批高质量安全研究源（公开 RSS/Atom），筛出 **攻击角度新颖** 或 **利用难度极高** 的 IoT / 固件 / 硬件 / 底层安全文章，
下载正文快照归档到 [`articles/`](articles/INDEX.md)，并自动登记到下方对应板块。

- **信息源**：[`tools/sources.json`](tools/sources.json)（可自由增删，含来源可信度权重）
- **礼貌抓取**：全程串行、请求间隔 ≥8s + 随机抖动、遵守 `robots.txt` 与 `Crawl-delay`；不登录、不伪造 Cookie、不绕过任何访问控制或付费墙
- **体积控制**：单篇快照 ≤150 KB，单次下载 ≤5 MB，仓库总量 ≤60 MB，磁盘剩余 <2 GB 自动停止
- **去重**：`data/state.json` 记录已收录 URL，重复文章不会二次下载
- **复审**：候选先落到 `_staging/<周>/`，只有通过复审的才发布进 `articles/`（宁缺毋滥，每周 0~8 篇）

手动跑一次：

```powershell
python tools/crawl.py --days 9 --limit 15   # 抓取 + 打分
python tools/publish.py --list               # 查看本周候选
python tools/publish.py --pick "01,03,05"    # 发布选中条目（自动挂板块 + 写 Log + 重建索引）
```

## 📂 目录

### 🔹 设备类型 
- [🌐 Openwrt](#openwrt)
- [📷 摄像头安全](#摄像头)
- [🚁 无人机安全](#无人机)
- [🛡️ 防火墙安全](#防火墙)
- [📡 基站安全](#基站)
- [🔥 防火墙安全](#防火墙)
- [📠 打印机安全](#打印机)
- [⚡ 充电桩安全](#充电桩)
- [🚗 车机安全](#车机)
- [⚠️ 智能家居安全](#智能家居)
- [🛰️ 卫星安全](#卫星安全)
- [📺 机器人安全](#机器人)
- [📱 芯片安全](#芯片安全)
- [🔑 RFID](#rfid)
- [🌐 WIFI安全](#wifi安全)
- [📦 FUZZ](#fuzz)
- [📜协议安全](#协议安全)
- [🖥️硬件钱包](#硬件钱包)

### 🔹 技术点
- [🚀 绕过 ASLR](#ASLR)
- [💉 故障注入](#故障注入)
- [🔑 安全启动](#安全启动)
- [📜 固件解密](#固件解密)
  
### 🔹 其他
- [🖥️ 虚拟机镜像](#虚拟机镜像)
- [📦 杂项](#杂项)
- [📥 固件下载](#固件下载)

# Log

<details>
<summary>点击查看更新记录</summary>

<details>
<summary>3/2/2025</summary>

>修改了原仓库名 
增加了固件解密
摄像头
Openwrt
无人机
防火墙
智能音箱
基站
打印机
安全启动
车机
绕过ASLR板块 

>后续会增加ROP
太空安全
无线电安全
故障注入
RTOS
FUZZ
CTF
QiLing板块
......

对于路由器我是真的不想写了 挺多的:(

</details>

<details>
<summary>3/9/2025</summary>

>更新

新增四篇摄像头相关文章、两篇无人机漏洞挖掘、一篇Luci系统漏洞挖掘 以及新添加了Contributors板块
哎我去怎么这周那么少 我是不是有些文章看了忘收藏了:(

</details>

<details>
<summary>3/17/2025</summary>

>更新
新增五篇无人机相关内容，两篇绕过ASLR，一篇故障注入

因为最近搞无人机搞得比较多 所以无人机相关的添加的比较多

希望能学学其他的丰富一下其他板块


</details>

<details>
<summary>3/30/2025</summary>

>更新
更新了挺多文章了 最近生病了所以上周没更 可能有些文章遗漏了 如果有好文章可以推荐给我

喵喵喵


</details>

<details>
<summary>4/7/2025</summary>

>更新
喵喵喵又过一周 随便水了几篇文章


</details>

<details>
<summary>4/14/2025</summary>

>更新
好累喵


</details>

<details>
<summary>4/21/2025</summary>

>更新
这周更新好少


</details>





</details>

<details>
<summary>11/16/2026</summary>

>更新
- [Pre-Auth RCE in Zyxel GS1900 Exploited in the Wild as a Zero-Day](articles/防火墙/2026-11-03-Pre-Auth-RCE-in-Zyxel-GS1900-Exploited-in-the-Wild-as-a-Zero.md)  —— 防火墙 板块
- [Additional Ivanti Connect Secure zero-days exploited in the wild (CVE-2026-111357, CVE-2026-118527)](articles/防火墙/2026-11-02-Additional-Ivanti-Connect-Secure-zero-days-exploited-in-the.md)  —— 防火墙 板块
- [Inside KeyDrift: Analyzing historical UAT-11473 activity on Cisco SD-WAN](articles/防火墙/2026-10-29-Inside-KeyDrift-Analyzing-historical-UAT-11473-activity-on-C.md)  —— 防火墙 板块
- [Two Oracles to Get One Key: A tale of recovering a symmetric key from an encrypt-only firmware update scheme](articles/固件解密/2026-11-10-Two-Oracles-to-Get-One-Key-A-tale-of-recovering-a-symmetric.md)  —— 固件解密 板块
- [Barracuda Networks is your new best friend (Barracuda Email Security Gateway Pre-Auth Remote Root RCE CVE-2026-116606 / CVE-2026-111560)](articles/防火墙/2026-11-06-Barracuda-Networks-is-your-new-best-friend-Barracuda-Email-S.md)  —— 防火墙 板块
- [潜伏16年的UEFI漏洞：开机那几秒，你的所有防线都还没上线](articles/安全启动/2026-11-05-潜伏16年的UEFI漏洞-开机那几秒-你的所有防线都还没上线.md)  —— 安全启动 板块
- [BinQL: a CodeQL extension for binary formats](articles/杂项/2026-11-13-BinQL-a-CodeQL-extension-for-binary-formats.md)  —— 杂项 板块
- [Snapshotting our way to CVE-2026-9539](articles/FUZZ/2026-10-27-Snapshotting-our-way-to-CVE-2026-9539.md)  —— FUZZ 板块


</details>
</details>

# 虚拟机镜像

<details>

<summary>暂时木有</summary>

考虑是否制作中,有点费时间(

</details>

# 固件下载

<details>

<summary>点我点我</summary>

- 🛠️ [TENDA 固件下载](https://www.tenda.com.cn/download/default.html)  
- 🛠️ [迅捷固件下载](https://service.fastcom.com.cn/download-list.html#0)  
- 🛠️ [TP-LINK 固件下载（国内）](https://resource.tp-link.com.cn/?&productorlist=1&filterClass=[4])  
- 🛠️ [TP-LINK 固件下载（国外）](https://www.tp-link.com/us/support/download/)  
- 🛠️ [水星固件下载](https://service.mercurycom.com.cn/download-list.html)  
- 🛠️ [艾泰固件下载](https://www.utt.com.cn/downloadcenter.php)  
- 🛠️ [锐捷固件下载](https://www.ruijie.com.cn/fw/rj-first-2321/)  
- 🛠️ [DLINK 固件下载](https://support.dlink.com/resource/products/)  
- 🛠️ [NETGEAR 固件下载](http://support.netgear.cn/download.asp)  
- 🛠️ [SOFTPEDIA 驱动下载](https://drivers.softpedia.com/)  
- 🛠️ [DrayTek 固件下载](https://www.draytek.com/support/resources/routers#version)  
- 🛠️ [iptime 固件下载](https://iptime.com/iptime/?page_id=126)  
- 🛠️ [ubiquiti 固件下载](https://ui.com.cn/download/releases/firmware)  
- 🛠️ [grandstream 固件下载](https://www.grandstream.com/support/firmware)  
- 🛠️ [peplink 固件下载](https://www.peplink.com/support/downloads/)  
- 🛠️ [avm 固件下载](https://www.anthemav.com/support/latest-software.php)  
- 🛠️ [axis 固件下载](https://www.axis.com/support/device-software)
- 🛠️ [海康威视固件下载](https://www.hiksemitech.com/en/hiksemi/support/download.html)

</details>


# 固件解密


<details>
<summary>点我点我</summary>

- 🛠️ [DrayTek 固件解密分析](https://www.hexacon.fr/slides/hexacon_draytek_2022_final.pdf)  
- 🛠️ [D-Link 固件漏洞分析](https://bbs.kanxue.com/thread-281043.htm)  
- 🛠️ [D-Link 固件漏洞研究](https://wzt.ac.cn/2019/09/18/D-Link_BUG/)  
- 🛠️ [D-Link 固件解密脚本](https://github.com/0xricksanchez/dlink-decrypt)  
- 🛠️ [SonicOS 固件解密分析（2024）](https://wzt.ac.cn/2024/09/05/sonicwall_dec2/)  
- 🛠️ [SonicOS 固件解密分析（2022）](https://wzt.ac.cn/2022/02/08/sonicwall_dec1/)  
- 🛠️ [Linksys 固件漏洞分析](https://www.anquanke.com/post/id/246659)  
- 🛠️ [D-Link DIR3060 固件解密分析（Part 1）](https://0x00sec.org/t/breaking-the-d-link-dir3060-firmware-encryption-static-analysis-of-the-decryption-routine-part-2-1/22099)  
- 🛠️ [D-Link DIR3060 固件解密分析（Part 2）](https://0x00sec.org/t/breaking-the-d-link-dir3060-firmware-encryption-static-analysis-of-the-decryption-routine-part-2-2/22260)  
- 🛠️ [Lexmark 固件漏洞分析](https://haxx.in/posts/wtm-wtf/)  
- 🛠️ [TP-Link C210 固件安全启动分析](https://watchfulip.github.io/28-12-24/tp-link_c210_v2.html)  
- 🛠️ [乐鑫芯片 Flash 加密破解](https://courk.cc/breaking-flash-encryption-of-espressif-parts#breaking-flash-encryption-of-espressif-parts)
- 🛠️ [使用机器学习解密固件](https://something.fromnothing.blog/posts/something-from-nothing/)
- 🛠️ [摄像头逆向分析之旅-程序还原](https://blog.nsfocus.net/lot-flash/)
- 📜 [Two Oracles to Get One Key: A tale of recovering a symmetric key from an encrypt-only firmware update scheme](articles/固件解密/2026-11-10-Two-Oracles-to-Get-One-Key-A-tale-of-recovering-a-symmetric.md) · [原文](https://www.ioactive.com/two-oracles-recovering-aes-firmware-key/)
</details>

# 摄像头

<details>

<summary>我收集的少 别骂我</summary>

- 🔗 [TPLink-Tapo CVE-2021-4045](https://github.com/hacefresko/CVE-2021-4045)
- 🔍 [TPLink-Tapo 漏洞分析](https://pwner.gg/blog/2024-01-05-tp-link-tapo-c100)
- 🌐 [TPLink-Tapo C2000](https://drmnsamoliu.github.io/index.html)
- 🔥 [TPLink-Tapo C2000](https://www.hacefresko.com/posts/tp-link-tapo-c200-unauthenticated-rce)
- 🎯 [Exploiting a Chinese camera for fun CVE-2024–48214]([深入剖析路由器FOTA固件升级流程：从解包到逆向分析](https://medium.com/%40shenhavmor/exploiting-a-chinese-camera-for-fun-cve-2024-48214-2d56848870c2))
- 📌 [TPLink-Tapo C310](https://sizeof.cat/post/tp-link-tapo-c310-camera/)
</details>

# Openwrt

<details>
<summary>点我点我</summary>

- 🛠️ [Ruijie 漏洞分析](https://bbs.kanxue.com/thread-277386.htm)  

- 📄 [小米路由器 Root 技术研究](https://blog.thalium.re/posts/rooting-xiaomi-wifi-routers/)
- 🛠️ [浅析LuCI系统的漏洞挖掘技术](https://mp.weixin.qq.com/s/kBOfQhNHZCFNNzu_euLIgA)

</details>

# 无人机

<details>
<summary>点我点我</summary>

- 📄 [无人机安全简介](https://payatu.com/blog/flying-securely-an-introduction-to-drone-security/)  
- 🧩 [DJI Mavic 3 固件研究（Part 1）](https://www.nozominetworks.com/blog/dji-mavic-3-drone-research-part-1-firmware-analysis)  
- 🔍 [DJI Mavic 3 固件研究（Part 2）](https://www.nozominetworks.com/blog/dji-mavic-3-drone-research-part-2-vulnerability-analysis)  
- ⚠️ [DJI RM500 遥控器提权漏洞](https://icanhack.nl/blog/dji-rm500-privilege-escalation/)  
- 📊 [针对 DJI 无人机的安全研究（NDSS 2023）](https://www.ndss-symposium.org/wp-content/uploads/2023/02/ndss2023_f217_paper.pdf)  
- 🎯 [无人机常见攻击方式](https://www.anquanke.com/post/id/82761)
- 🔧 [DroneSploit 渗透测试框架](https://github.com/dhondta/dronesploit)  
- 📡 [通过 Wireshark 解析无人机数据包](https://hackernoon.com/lang/zh/%E5%A6%82%E4%BD%95%E4%BD%BF%E7%94%A8%E6%95%B0%E6%8D%AE%E5%8C%85%E8%A7%A3%E5%89%96%E4%BD%BF%E7%94%A8-wireshark-%E5%AF%B9%E6%97%A0%E4%BA%BA%E6%9C%BA%E8%BF%9B%E8%A1%8C%E9%80%86%E5%90%91%E5%B7%A5%E7%A8%8B)
- 📈 [绿盟 2023 无人机安全报告](https://book.yunzhan365.com/tkgd/ghoo/mobile/index.html)  
- 📉 [绿盟 2024 无人机安全报告](https://book.yunzhan365.com/tkgd/gmpv/mobile/index.html)
- 🚁 [某无人机APP逆向分析](https://v5le0n9.github.io/posts/ac4cb042.html)
- 🔍 [某无人机漏洞挖掘](https://v5le0n9.github.io/posts/8a5081f6.html)
- 📡 [315晚会报道的无人机是怎么被劫持的？](https://security.tencent.com/index.php/blog/msg/103)
- 🔐 [几种小型UAV安全漏洞研究](https://ndxb.imu.edu.cn/__local/8/16/3D/02E8C65FA6BC939DC5776397BCE_8849FAC7_67446D.pdf)
- 🎯 [针对基于mavlink协议的无人机进行攻击](https://mp.weixin.qq.com/s/HfFqgQcgOyA_rmb3UFXhww)
- 🛡️ [无人机mavlink中间人攻击](https://mp.weixin.qq.com/s/gfzdWSlzBkc14fvG1n36Cg)
- 🧑‍💻 [无人机MAVLINK协议安全剖析](https://mp.weixin.qq.com/s/WEivJpxTBSVcmAa5QvvDxQ)
- 🎯 [攻防速写｜击穿DJI大疆控制设备的致命漏洞](https://www.ctfiot.com/232771.html)
- 🔍 [基于模糊测试的多旋翼无人机微小型无人机漏洞分析](https://xz.aliyun.com/course-view?id=11)
</details>

# 防火墙
<details>
<summary>点我点我</summary>

- ⚠️ [FortiOS 关键漏洞分析（2025）](https://www.akamai.com/blog/security-research/2025-february-fortinet-critical-vulnerabilities)  
- 🎯 [Ivanti CVE-2025-0282 RCE 利用分析](https://labs.watchtowr.com/exploitation-walkthrough-and-techniques-ivanti-connect-secure-rce-cve-2025-0282/)
- 🧩 [PAN-OS 完整攻击链分析](https://www.horizon3.ai/attack-research/disclosures/palo-alto-expedition-from-n-day-to-full-compromise/)  
- 🔓 [Palo Alto路径混淆认证绕过漏洞](https://slcyber.io/blog/nginx-apache-path-confusion-to-auth-bypass-in-pan-os/)  
- 📱 [Palo Alto 分析报告](https://mp.weixin.qq.com/s?__biz=MjM5NTc2MDYxMw==&mid=2458589341&idx=1&sn=c57db95a9d3d5f4d3d5993b9e4d2398e&chksm=b058fa0e9bed1058d3630a5e1eb6e07af731a0dd15a60c93ffc6f651afe5d8d410438491fea3&mpshare=1&scene=2&srcid=0208LPPhzgrDbMTj76w5Y3S0&sharer_shareinfo=d134b3645062ee3043dfb811bdfe2842&sharer_shareinfo_first=d134b3645062ee3043dfb811bdfe2842#rd)
- ⚠️ [Check Point CVE-2024-24919 分析](https://labs.watchtowr.com/check-point-wrong-check-point-cve-2024-24919/)
- 🎯 [CVE-2025-22457](https://attackerkb.com/topics/0ybGQIkHzR/cve-2025-22457/rapid7-analysis)
- 🛡️ [Pre-Auth RCE in Zyxel GS1900 Exploited in the Wild as a Zero-Day](articles/防火墙/2026-11-03-Pre-Auth-RCE-in-Zyxel-GS1900-Exploited-in-the-Wild-as-a-Zero.md) · [原文](https://www.binarly.io/blog/zyxel-gs1900-rce-cve-2026-107441)
- 🛡️ [Additional Ivanti Connect Secure zero-days exploited in the wild (CVE-2026-111357, CVE-2026-118527)](articles/防火墙/2026-11-02-Additional-Ivanti-Connect-Secure-zero-days-exploited-in-the.md) · [原文](https://www.rapid7.com/blog/post/etr-additional-ivanti-connect-secure-zero-days-exploited-in-the-wild-cve-2026-111357-cve-2026-118527)
- 🛡️ [Inside KeyDrift: Analyzing historical UAT-11473 activity on Cisco SD-WAN](articles/防火墙/2026-10-29-Inside-KeyDrift-Analyzing-historical-UAT-11473-activity-on-C.md) · [原文](https://blog.talosintelligence.com/uat-11473-keydrift/)
- 🛡️ [Barracuda Networks is your new best friend (Barracuda Email Security Gateway Pre-Auth Remote Root RCE CVE-2026-116606 / CVE-2026-111560)](articles/防火墙/2026-11-06-Barracuda-Networks-is-your-new-best-friend-Barracuda-Email-S.md) · [原文](https://labs.watchtowr.com/barracuda-networks-is-your-new-best-friend-barracuda-email-security-gateway-pre-auth-remote-root-rce-cve-2026-116606-cve-2026-111560/)
</details>


# 基站
<details>
<summary>点我点我 等我学会再来添加好吧 我太菜了:(</summary>

- 🛠️ [NextEPC 漏洞分析](https://cellularsecurity.org/ransacked)  
- ⚠️ [使用用户设备对 5G 基站进行攻击](https://www.trendmicro.com/en_gb/research/23/i/attacks-on-5g-infrastructure-from-users-devices.html)
- 🔓[攻防速写｜我们拆了一台Starlink星链终端](https://mp.weixin.qq.com/s/QsLyWHp1zb89Gq7aXgWZwA)
</details>

# 打印机
<details>
<summary>点我点我</summary>

- 🛠️ [通过三个步骤入侵打印机](https://www.crowdstrike.com/en-us/blog/how-to-compromise-a-printer-in-3-simple-steps/)  
- ⚠️ [Sharp MFP 17 漏洞分析](https://pierrekim.github.io/blog/2024-06-27-sharp-mfp-17-vulnerabilities.html#pre-auth-memory-corruption)  
- 🔓 [Xerox WorkCentre 未授权 RCE 漏洞](https://swarm.ptsecurity.com/inside-xerox-workcentre-two-unauthenticated-rces/)

</details>

# 安全启动
<details>
<summary>点我点我 因为菜 所以少:(</summary>

- 🛠️ [TP-Link C210 安全启动分析](https://watchfulip.github.io/28-12-24/tp-link_c210_v2.html)
- 🧩 [U-Boot 逆向分析（Part 1）](https://www.shielder.com/blog/2022/03/reversing-embedded-device-bootloader-u-boot-p.1/)  
- 🔍 [U-Boot 逆向分析（Part 2）](https://www.shielder.com/blog/2022/03/reversing-embedded-device-bootloader-u-boot-p.2/)
- 🔑 [潜伏16年的UEFI漏洞：开机那几秒，你的所有防线都还没上线](articles/安全启动/2026-11-05-潜伏16年的UEFI漏洞-开机那几秒-你的所有防线都还没上线.md) · [原文](https://www.anquanke.com/post/id/316426)

</details>

# 充电桩
<details>
<summary>点我点我</summary>

- 🛠️ [从蓝牙入侵充电桩](https://www.youtube.com/watch?v=8gNhfR1YZGA)  
- ⚠️ [破解 Autel MaxiCharger](https://sector7.computest.nl/post/2024-08-pwn2own-automotive-autel-maxicharger/)
- 🧩 [CHARX 充电桩漏洞分析（Part 1）](https://blog.ret2.io/2024/07/17/pwn2own-auto-2024-charx-bugs/)  
- 🔍 [CHARX 充电桩漏洞利用（Part 2）](https://blog.ret2.io/2024/07/24/pwn2own-auto-2024-charx-exploit/)
</details>

# 车机
<details>
<summary>点我点我</summary>

- 🛠️ [大众 MMX 车机漏洞分析](https://sector7.computest.nl/post/2018-07-mib/)  
- 📄 [腾讯科恩实验室对奔驰梅赛德斯车机研究](https://keenlab.tencent.com/en/whitepapers/Mercedes_Benz_Security_Research_Report_Final.pdf)
- ⚠️ [Asia-25-Evdokimov-Remote-Exploitation-of-Nissan-Leaf](https://i.blackhat.com/Asia-25/Asia-25-Evdokimov-Remote-Exploitation-of-Nissan-Leaf.pdf)
</details>

# 绕过ASLR
<details>
<summary>为什么要单独开个ASLR呢 因为很多栈溢出都因为ASLR导致无法RCE</summary>

- 🛠️ [使用栈上gadget绕过 ASLR](https://www.anquanke.com/post/id/180252)  
- 🎯 [修改 sendsize 触发 DNS 查询泄露地址](https://claroty.com/team82/research/pwn2own-wan-to-lan-exploit-showcase?ref=blog.exploits.club)  
- 🔓 [通过文件包含漏洞绕过 ASLR](https://modzero.com/en/blog/roping-our-way-to-rce/)
- 💻 [How CVE-2015-7547 (GLIBC getaddrinfo) Can Bypass ASLR](💻)
- 🗄️ [wp-armis-cdpwn-aslr-bypass-en](https://media.armis.com/image/upload/v1679440790/PDFs/wp-armis-cdpwn-aslr-bypass-en.pdf)
- 🔍 [CVE-2025-22457](https://attackerkb.com/topics/0ybGQIkHzR/cve-2025-22457/rapid7-analysis)
</details>

# 故障注入

<details>
<summary>艹,我不会</summary>

- 🛠️ [Fault Injection – Down the Rabbit Hole](https://security.humanativaspa.it/fault-injection-down-the-rabbit-hole/)

</details>

# 智能家居

<details>
<summary>点我点我</summary>

- 📄 [谷歌智能音箱安全分析](https://security.tencent.com/index.php/blog/msg/141)
- 🛠️ [Pwning Millions of Smart Weighing Machines with API and Hardware Hacking](https://spaceraccoon.dev/pwning-millions-smart-weighing-machines-api-hardware-hacking/)
- 💻 [https://www.synacktiv.com/en/publications/hack-the-channel-a-deep-dive-into-dvb-receiver-security](https://www.synacktiv.com/en/publications/hack-the-channel-a-deep-dive-into-dvb-receiver-security)

</details>

# RFID

<details>
<summary>点我点我</summary>

- 📄 [身边的智能卡安全么？——IC卡安全性初探](https://xz.aliyun.com/news/8265?time__1311=YqUxg7iQoDqQqGNKQrDnBCFG%3D%3DMGO3rD&u_atoken=2605ac6da9572677f351f83015d5ebad&u_asig=1a0c399817433461047984986e0046)
- 🎭 [IC卡加密方式和基本常识](https://mp.weixin.qq.com/s/MC_gsU3lbOUfmkfKK_0RTQ)
- 🖥️ [RFID 射频卡安全梳理](https://stdio.io/1345)
- 🔒 [MIFARE Classic: exposing the static encrypted nonce variant](https://eprint.iacr.org/2024/1275.pdf)
- 🔍 [逆向破解南京大学纯 CPU SAK28 FM1208 NFC 校园卡](https://blog.lyc8503.net/post/reverse-nju-cpu-card/)
</details>


# 杂项

<details>
<summary>点我点我</summary>

- 🧩 [浅析 CGI 与 Lighttpd 之间的调用过程](https://www.iotsec-zone.com/article/319)  
- 📚 [史上最全 U-Boot 命令解析](https://cloud.tencent.com/developer/article/2102295)  
- 🛠️ [通过 WIFI 修改加热器固件](https://blog.includesecurity.com/2025/02/replacing-a-space-heater-firmware-over-wifi/)
- 📄 [Brushing Up on Hardware Hacking Part 2 - SPI, UART, Pulseview, and Flashrom](https://voidstarsec.com/blog/brushing-up-part-2)
- 🛠️ [嵌入式设备后门与shellcode生成工具](https://bbs.kanxue.com/thread-275619.htm)
- 🗄️ [IOT设备常见配置文件加解密分析总结](https://mp.weixin.qq.com/s/vik2Xp459afeV0e3xcihHQ)
- 💻 [How CVE-2015-7547 (GLIBC getaddrinfo) Can Bypass ASLR](https://mp.weixin.qq.com/s/AEOc49tz_WlDABXucmVPNw)
- 🛠️[DrayTek再现未授权RCE漏洞：CVE-2024-12987复现分析](https://think-awesome.com/download_unitree_report)
- 📚 [智能网联汽车信息安全测试白皮书](https://report.secbug.cc/2025%E6%99%BA%E8%83%BD%E7%BD%91%E8%81%94%E6%B1%BD%E8%BD%A6%E4%BF%A1%E6%81%AF%E5%AE%89%E5%85%A8%E6%B5%8B%E8%AF%95%E7%99%BD%E7%9A%AE%E4%B9%A6.pdf)
- 💻 [企业安全设备漏洞研究](https://drive.google.com/file/d/1W6kVh6zJ-R61WR69xX7V02mmESTuwPJO/view)
- 📄 [深入剖析路由器FOTA固件升级流程：从解包到逆向分析](https://xz.aliyun.com/news/17402?time__1311=eqUxn7DQG%3DekD%2Fb043aDBDRxQqiKN%3D3x&u_atoken=410984a321fcdb00f210c49c794f8cb1&u_asig=1a0c380917440179029383912e00f0)
- 🗄️ [Secure Hardware Design](https://shd.mit.edu/home/)
- 🧩 [VxWorks固件系统研究技术总结二](https://mp.weixin.qq.com/s/SnooEM6NLLPIz8u2t4_MOw)
- 📦 [BinQL: a CodeQL extension for binary formats](articles/杂项/2026-11-13-BinQL-a-CodeQL-extension-for-binary-formats.md) · [原文](https://blog.thalium.re/posts/binql-a-codeql-extension-for-binary-formats/)
</details>

# 机器人

<details>
<summary>点我点我</summary>

- 🔍 [宇树GO1机器人分析](https://think-awesome.com/download_unitree_report)

</details>

# FUZZ

<details>
<summary>点我点我</summary>

- 🧩[RV130X Firmware Analysis](https://raffo24.github.io/hardware%20hacking/FirmwareAnalysis/)
- 📦 [Snapshotting our way to CVE-2026-9539](articles/FUZZ/2026-10-27-Snapshotting-our-way-to-CVE-2026-9539.md) · [原文](http://blog.quarkslab.com/snapshotting-our-way-to-cve-2026-9539.html)

</details>

# WIFI安全

<details>
<summary>点我点我</summary>

- 🛠️[无线网络（WI-FI）保护协议标准WPA2漏洞综合分析报告](https://www.antiy.com/response/krack.html)

</details>

# 协议安全

<details>
<summary>点我点我</summary>

- 🔍 [DNSpooq系列漏洞分析与复现](https://www.venustech.com.cn/new_type/aqldfx/20210201/22352.html)
- 🌐 [Bluetooth-Attacks-CVE-2025-27840](https://github.com/demining/Bluetooth-Attacks-CVE-2025-27840)
- 🛠️ [无线电安全攻防之蓝牙协议栈技术初探](https://mp.weixin.qq.com/s/OTSwW2E1BRHYuGg1XxAC8g)

</details>

# 硬件钱包

<details>
<summary>艹,我不会</summary>

- 🗄️ [攻防速写｜假如捡到 Web3 硬件钱包的人是黑客](https://mp.weixin.qq.com/s/FYDgYG9UCTgwc7KxAdIjjw)

</details>

# 芯片安全

<details>
<summary>点我点我</summary>

- 📚 [Last barrier destroyed, or compromise of Fuse Encryption Key for Intel Security Fuses](https://swarm.ptsecurity.com/last-barrier-destroyed-or-compromise-of-fuse-encryption-key-for-intel-security-fuses/)

</details>

## Contributors

<div align="center">

  <a href="https://www.cnblogs.com/ve1kcon">
    <img src="https://pic1.imgdb.cn/item/67cdb235066befcec6e23553.jpg" alt="ve1kcon" width="100" height="100">
  </a>
  
  <a href="https://github.com/glkfc">
    <img src="https://pic1.imgdb.cn/item/67cdb48c066befcec6e235c8.jpg" alt="jfkk" width="100" height="100">
  </a>
  


</div>

