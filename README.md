# 📡 IOTsec-all-in-one


本项目致力于 **收集和整理 IoT 安全（IoTsec）相关资料**，分类依据 **设备类型** 或 **技术点**，  
为研究人员、开发者提供有价值的安全研究参考。

📌 **目标**：
- 持续收集 IoT 安全相关资料
- 以 **设备类型** 或 **技术点** 分类整理
- **每周至少更新一次**（1 Week 1 Update）
- 后期对每篇文章 **提炼关键词** 和 **总结核心内容**



## 📂 目录

### 🔹 设备类型 
- [🖥️ 虚拟机镜像](#虚拟机镜像)
- [🌐 Openwrt](#openwrt)
- [📷 摄像头安全](#摄像头)
- [🚁 无人机安全](#无人机)
- [🛡️ 防火墙安全](#防火墙)
- [🎙️ 智能音箱安全](#智能音箱)
- [📡 基站安全](#基站)
- [🔥 防火墙安全](#防火墙)
- [📠 打印机安全](#打印机)
- [⚡ 充电桩安全](#充电桩)
- [🚗 车机安全](#车机)

### 🔹 技术点
- [🚀 绕过 ASLR](#ASLR)
- [💉 故障注入](#故障注入)
- [🔑 安全启动](#安全启动)
- [📜 固件解密](#固件解密)
- 
### 🔹 其他
- [📦 杂项](#杂项)
- [📥 固件下载](#固件下载)

# Log

<details>
<summary>点击展示记录</summary>

# 3/2/2025 
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

# 虚拟机镜像

<details>

<summary>暂时木有</summary>

考虑是否制作中,有点费时间(

</details>

# 固件下载

<details>

<summary>点我点我</summary>

TENDA https://www.tenda.com.cn/download/default.html

迅捷 https://service.fastcom.com.cn/download-list.html#0

TP-LINK https://resource.tp-link.com.cn/?&productorlist=1&filterClass=[4]

TP-LINK(国外)https://www.tp-link.com/us/support/download/

水星 https://service.mercurycom.com.cn/download-list.html

艾泰 https://www.utt.com.cn/downloadcenter.php

锐捷 https://www.ruijie.com.cn/fw/rj-first-2321/

DLINK https://support.dlink.com/resource/products/

NETGEAR http://support.netgear.cn/download.asp

SOFTPEDIA https://drivers.softpedia.com/

DrayTek https://www.draytek.com/support/resources/routers#version

海康威视 https://www.hiksemitech.com/en/hiksemi/support/download.html

iptime https://iptime.com/iptime/?page_id=126

ubiquiti https://ui.com.cn/download/releases/firmware

grandstream https://www.grandstream.com/support/firmware

peplink https://www.peplink.com/support/downloads/

avm https://www.anthemav.com/support/latest-software.php

axis https://www.axis.com/support/device-software

</details>


# 固件解密


<details>
<summary>点我点我</summary>

DrayTek https://www.hexacon.fr/slides/hexacon_draytek_2022_final.pdf

DLINK   https://bbs.kanxue.com/thread-281043.htm

Dlink   https://wzt.ac.cn/2019/09/18/D-Link_BUG/

Dlink解密脚本 https://github.com/0xricksanchez/dlink-decrypt

SonicOS https://wzt.ac.cn/2024/09/05/sonicwall_dec2/

SonicOS https://wzt.ac.cn/2022/02/08/sonicwall_dec1/

Linksys https://www.anquanke.com/post/id/246659

Dlink https://0x00sec.org/t/breaking-the-d-link-dir3060-firmware-encryption-static-analysis-of-the-decryption-routine-part-2-1/22099

Dlink https://0x00sec.org/t/breaking-the-d-link-dir3060-firmware-encryption-static-analysis-of-the-decryption-routine-part-2-2/22260

Lexmark https://haxx.in/posts/wtm-wtf/

Tp-Link https://watchfulip.github.io/28-12-24/tp-link_c210_v2.html

乐鑫 https://courk.cc/breaking-flash-encryption-of-espressif-parts#breaking-flash-encryption-of-espressif-parts



</details>

# 摄像头

<details>

<summary>我收集的少 别骂我</summary>

TPLink-Tapo https://github.com/hacefresko/CVE-2021-4045
TPLink-Tapo https://pwner.gg/blog/2024-01-05-tp-link-tapo-c100

- 🔗 [TPLink-Tapo CVE-2021-4045](https://github.com/hacefresko/CVE-2021-4045)
- 🔍 [TPLink-Tapo 漏洞分析](https://pwner.gg/blog/2024-01-05-tp-link-tapo-c100)

</details>

# Openwrt

<details>
<summary>点我点我</summary>

Ruijie https://bbs.kanxue.com/thread-277386.htm
Xiaomi https://blog.thalium.re/posts/rooting-xiaomi-wifi-routers/

</details>

# 无人机

<details>
<summary>点我点我</summary>

无人机安全简介 https://payatu.com/blog/flying-securely-an-introduction-to-drone-security/
DJI 固件研究1 https://www.nozominetworks.com/blog/dji-mavic-3-drone-research-part-1-firmware-analysis
DJI 固件研究2 https://www.nozominetworks.com/blog/dji-mavic-3-drone-research-part-2-vulnerability-analysis
DJI RM500遥控器提权 https://icanhack.nl/blog/dji-rm500-privilege-escalation/
针对DJI无人机的安全研究 https://www.ndss-symposium.org/wp-content/uploads/2023/02/ndss2023_f217_paper.pdf
无人机常见攻击方式 https://www.anquanke.com/post/id/82761
DroneSploit框架 https://github.com/dhondta/dronesploit
通过Wireshark解析数据包对无人机进行逆向 https://hackernoon.com/lang/zh/%E5%A6%82%E4%BD%95%E4%BD%BF%E7%94%A8%E6%95%B0%E6%8D%AE%E5%8C%85%E8%A7%A3%E5%89%96%E4%BD%BF%E7%94%A8-wireshark-%E5%AF%B9%E6%97%A0%E4%BA%BA%E6%9C%BA%E8%BF%9B%E8%A1%8C%E9%80%86%E5%90%91%E5%B7%A5%E7%A8%8B
绿盟2023无人机安全报告 https://book.yunzhan365.com/tkgd/ghoo/mobile/index.html
绿盟2024无人机安全报告 https://book.yunzhan365.com/tkgd/gmpv/mobile/index.html

</details>

# 防火墙
<details>
<summary>点我点我</summary>

Fortios https://www.akamai.com/blog/security-research/2025-february-fortinet-critical-vulnerabilities
Ivanti https://labs.watchtowr.com/exploitation-walkthrough-and-techniques-ivanti-connect-secure-rce-cve-2025-0282/
Palo Alto https://www.horizon3.ai/attack-research/disclosures/palo-alto-expedition-from-n-day-to-full-compromise/
Palo Alto https://slcyber.io/blog/nginx-apache-path-confusion-to-auth-bypass-in-pan-os/
Palo Alto https://mp.weixin.qq.com/s?__biz=MjM5NTc2MDYxMw==&mid=2458589341&idx=1&sn=c57db95a9d3d5f4d3d5993b9e4d2398e&chksm=b058fa0e9bed1058d3630a5e1eb6e07af731a0dd15a60c93ffc6f651afe5d8d410438491fea3&mpshare=1&scene=2&srcid=0208LPPhzgrDbMTj76w5Y3S0&sharer_shareinfo=d134b3645062ee3043dfb811bdfe2842&sharer_shareinfo_first=d134b3645062ee3043dfb811bdfe2842#rd
Chekc Point https://labs.watchtowr.com/check-point-wrong-check-point-cve-2024-24919/

</details>

# 智能音箱

<details>
<summary>点我点我 这个我也收集的少 别骂我</summary>

谷歌智能音箱 https://security.tencent.com/index.php/blog/msg/141

</details>

# 基站
<details>
<summary>点我点我 等我学会再来添加好吧 我太菜了:(</summary>

NextEPC https://cellularsecurity.org/ransacked
使用用户设备对5G基站进行攻击 https://www.trendmicro.com/en_gb/research/23/i/attacks-on-5g-infrastructure-from-users-devices.html

</details>

# 打印机
<details>
<summary>点我点我</summary>

通过三个步骤入侵打印机 https://www.crowdstrike.com/en-us/blog/how-to-compromise-a-printer-in-3-simple-steps/
sharp https://pierrekim.github.io/blog/2024-06-27-sharp-mfp-17-vulnerabilities.html#pre-auth-memory-corruption
Xerox https://swarm.ptsecurity.com/inside-xerox-workcentre-two-unauthenticated-rces/

</details>

# 安全启动
<details>
<summary>点我点我 因为菜 所以少:(</summary>

TP-Link C210安全启动分析 https://watchfulip.github.io/28-12-24/tp-link_c210_v2.html
U-Boot逆向1 https://www.shielder.com/blog/2022/03/reversing-embedded-device-bootloader-u-boot-p.1/
U-Boot逆向2 https://www.shielder.com/blog/2022/03/reversing-embedded-device-bootloader-u-boot-p.2/

</details>

# 充电桩
<details>
<summary>点我点我</summary>

从蓝牙入侵充电桩 https://www.youtube.com/watch?v=8gNhfR1YZGA
破解Autel MaxiCharger https://sector7.computest.nl/post/2024-08-pwn2own-automotive-autel-maxicharger/
CHARX充电桩研究1 https://blog.ret2.io/2024/07/17/pwn2own-auto-2024-charx-bugs/
CHARX充电桩研究2 https://blog.ret2.io/2024/07/24/pwn2own-auto-2024-charx-exploit/

</details>

# 车机
<details>
<summary>点我点我</summary>

大众MMX https://sector7.computest.nl/post/2018-07-mib/
腾讯科恩实验室对奔驰梅赛德斯车机研究 https://keenlab.tencent.com/en/whitepapers/Mercedes_Benz_Security_Research_Report_Final.pdf

</details>

# 绕过ASLR
<details>
<summary>为什么要单独开个ASLR呢 因为很多栈溢出都因为ASLR导致无法RCE</summary>

使用堆喷技术绕过ASLR https://www.anquanke.com/post/id/180252
修改sendsize触发DNS查询来泄露地址 https://claroty.com/team82/research/pwn2own-wan-to-lan-exploit-showcase?ref=blog.exploits.club
通过文件包含漏洞绕过ASLR https://modzero.com/en/blog/roping-our-way-to-rce/

</details>

# 故障注入

<details>
<summary>艹,我不会<summary>

</details>


# 杂项

<details>
<summary>点我点我</summary>

浅析cgi与lighttpd之间的调用过程 https://www.iotsec-zone.com/article/319
史上最全U-Boot命令 https://cloud.tencent.com/developer/article/2102295
通过WIFI修改加热器固件 https://blog.includesecurity.com/2025/02/replacing-a-space-heater-firmware-over-wifi/

</details>






