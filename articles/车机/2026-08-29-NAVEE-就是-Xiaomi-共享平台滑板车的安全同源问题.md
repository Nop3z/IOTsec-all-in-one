---
title: "NAVEE 就是 Xiaomi：共享平台滑板车的安全同源问题"
source: "RoboCoffee"
url: https://robocoffee.de/?p=1015
published: 2026-08-29
fetched: 2026-11-24T20:29:01.595391+08:00
category: "车机"
score: 0
keywords: []
sha256: 90bdeab4aa35526f88e5eac47c917374e1f44338b78a788b58b0f4f264b85310
bytes: 9076
truncated: false
body_mode: fulltext
kind: practical
status: published
published_at: 2026-11-24T20:30:46.008546+08:00
---

# NAVEE 就是 Xiaomi：共享平台滑板车的安全同源问题

> 来源：RoboCoffee · 2026-08-29 · [原文](https://robocoffee.de/?p=1015)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：Xiaomi 并不自产滑板车，而是由 Ninebot、LEQI、Brightway 等代工；作者证明 NAVEE 与 Xiaomi 车型共享同一套安全实现，因此对一款车的破解可平移到另一品牌。
- **价值**：典型的“贴牌不改代码”供应链风险案例——安全评估若按品牌划分，就会漏掉同源设备。
- **难度**：中 —— 以对比与验证为主。

.entry-header

```
Disclaimer: Educational research only. Modifying your e-scooter can be dangerous and may be illegal where you live. Also: reading this post may cause involuntary eye-rolling at firmware that still sends speed limits in cleartext.
```

If you followed this blog, you’ll know that Xiaomi doesn’t make scooters. It sources the scooters from manufacturers like Ninebot, LEQI and Brightway. A while back I investigated security in new Xiaomi scooters and ran case studies on two Brightway scooters: the 3Lite and 4 Pro (2nd gen)y.

Brightway doesn’t only produce scooters for Xiaomi but also for the brand „NAVEE“ – though, newer NAVEE models seem to come from another company called „SPACEWALKER PTE. LTD.“. Anyway, it was about to time that we looked into one of those NAVEE scooters, as we expect similar hardware, but different executation.

## „WAIT, ISN’T THIS JUST A 4 PRO 2ND GEN?“

I decided to get myself a used NAVEE V40i (Pro) on the German Craigslist (Kleinanzeigen). Right after getting it back home, I ripped out the organs and placed them on a stick to „experiment on“.

![image](https://robocoffee.de/wp-content/uploads/2026/08/image-edited.png)

NAVEE V40i „scooter on a stick“

As it turns out, the NAVEE V40i uses the EXACT same controller hardware as the 4 Pro (2nd gen): same MCU, same readout protection, same attack vector to dump the chip, and also, same flash layout, same REMAP trick, same DFU handshake, but… a different APP image (of course) and different IAP flashing sequence! Interesting…

![image](https://robocoffee.de/wp-content/uploads/2024/10/4pro2nd_4-1024x461.jpg)

Xiaomi 4 Pro (2nd gen)

![image](https://robocoffee.de/wp-content/uploads/2026/08/image-1-edited-1024x682.png)

NAVEE V40i NAVEE vs. Xiaomi: same controller hardware

The motor silicon is a EastSoft FS026R7L, Cortex-M0, 128 KiB flash @ 0x08000000. OTA packages are unencrypted. No openssl verify. No Mijia cert appendix.

 0x8000000Bootloader: IAP + DFU engine0x8003000App: FOC, limits, UART hub, …0x801FC00„Please reboot into IAP“ flagFlash map of NAVEE V40: same as 4 Pro (2nd gen)

## AI-assisted reverse-engineering speedrun

Because of their great similarity, all the hacking techniques used in the 4 Pro (2nd gen) reverse engineering could be applied in this project. Back in the day, I used to spend months, with endless sleepless nights, tinkering on one problem. Nowadays, we can use an AI agent to boost every step in the hacking process.

For this scooter specifically, it took me two days from tear-down to a working BLE flasher. AI has made things so easy that I wonder how manufacturers will keep up with their device or IT system security. The mouse and cat race has gotten 100 times faster and currently the mice are everywhere…

Day 1:

- SWD dump
- Rev firmware
- Patch ESC
- Sniff UART
- Formalize DFU protocol
- Create flasher
- Flash via UART

Day 2:

- HCI Sniff
- Rev BLE protocol
- Create / update flasher
- BLE DFU with sniffed key
- Rev Cloud API
- Key from Cloud API
- Full BLE flasher

Btw, in the process of development, I find it helpful to use AI for generating documentation. This is the save point for the current and future projects!

![image](https://robocoffee.de/wp-content/uploads/2026/08/Screenshot-from-2026-08-29-22-14-48-1024x627.png)

AI-generated documentation FTW

Disclaimer: I still write my blog posts without AI. The post might not be optimized for engagement, but these are still my words. I hate nothing more than AI generated shitposts and articles filled with em-dashes, emojis and hyper-enthusiasm. Ok, what’s maybe worse is those kids who forward their shitty request to AI, let it do some magic computation, and copy the answer verbatim over to Discord or GitHub, without checking anything: „here’s how you can do it, it works 100%, just needs testing“.

## Dashboard security? Nah, thanks …

We skipped talking about the dashboard and BLE module for a very specific reason: it’s mostly just a relay for UART commands.

![image](https://robocoffee.de/wp-content/uploads/2026/08/Screenshot-from-2026-08-30-14-35-19-1024x769.png)

NAVEE V40 has same BLE chip as all new Xiaomi scooters

I didn’t tear down the dashboard this time, but FCC documents reveal all we need to know: we’re dealing with a XMB1R / RTL8762C chip, presumably packaged in the MHCB05PB module (which is also a Brightway product). This module has been used across all new Xiaomi models and, due to a secure chip, encrypted BLE channel and firmware signing, made BLE based firmware flashing virtually impossible (*).

![image](https://robocoffee.de/wp-content/uploads/2026/08/image-3-1024x819.png)

AI is great for memes tho

None of those security features can be found in this NAVEE branded scooter: BLE communication is unencrypted and firmware isn’t signed. Since the module is used across all of the Brightway-made NAVEE models, this applies to a large number of scooters. This leads to one question: If both Xiaomi and NAVEE scooter use the same hardware, why is one secure and the other not? My theory is that the security was designed and licensed by Xiaomi exclusively (and isn’t available to other vendors), since at the core of it the Xiaomi MJ1A secure chip is used.

Anyway, there’s not much to explore here. A simple BLE sniff is enough to completely reverse the auth / handshake, DFU and command protocol and create a fully functioning flasher.

(*) Whoever claims otherwise is full of shit. If you come across any videos that demonstrate phone based flashing it’s 100% fake. Point of reference: flashing takes at last half a minute.

## BLE auth and NAVEE Cloud API

One piece of the puzzle remains: before the dash keeps a long-lived BLE session open, the phone has to complete a handshake. That handshake uses a shared key table and an id the dash checks before it will even issue a challenge.

The key side of things is straightforward. Phone and dash each hold the same key table and at the start they agree on which entry to use. The chosen key is used to transform a challenge, such that the dash can verify the response. But the catch is that you only get a challenge after you supply an id the dash accepts, as visualized in this high-level sequence diagram:

![image](https://robocoffee.de/wp-content/uploads/2026/08/diagram-1788110279544-1024x903.png)

Vehicle bind, handshake and key storage

I spent an hour or two chasing where that id comes from, expecting a device-specific derivation or some extra algorithm. There isn’t one (**), which fits the design philosophy perfectly: “Security? Nah, thanks…”. Anyway, the more interesting question is what the dash does with it: when does it store that id and how does it decide later requests are allowed?

The answer is the bind flow, when a user first pairs the scooter with the app. During bind, the dash writes this id into BLE NVM. After
that, opening a session is mostly routine: pick a key index, complete the challenge–response, and the BLE link becomes a UART relay, forwarding traffic between the phone and the ESC MCU. Does that last part sound familiar? That’s exactly what BLE did on early Ninebot and „Xiaomi made by Ninebot“ scooters, before encryption showed up.

(**) Without naming the exact format: the id is tied to your NAVEE account, not baked into the hardware. So a successful wireless flash path assumes you can sign into that account, at least once, to establish bind.

## Bottom-line

AI gave everyone the means to nuke anything. If you want to make a secure system, you have to have secure components! There’s longer any way around it. Implement firmware signing (server side), store keys on secure chips, encrypt traffic. One doesn’t have to lock everything down, but these steps alone are enough to prevent abuse.

To my surprise, NAVEE not only kept the dashboard communication and firmware unencrypted, but also the API traffic: we can follow the process of binding and unbinding devices (and everything else) in clear text. And the mechanism supposed to secure the BLE session, involving keys and an id, turned out to be hot air.

![image](https://robocoffee.de/wp-content/uploads/2026/08/image-4.png)

 .entry-content

 .post-inner

 .section-inner   .pagination-single

 .post
