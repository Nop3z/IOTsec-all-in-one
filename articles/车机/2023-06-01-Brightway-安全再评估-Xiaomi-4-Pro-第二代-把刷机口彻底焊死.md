---
title: "Brightway 安全再评估：Xiaomi 4 Pro（第二代）把刷机口彻底焊死"
source: "RoboCoffee"
url: https://robocoffee.de/?p=897
published: 2023-06-01
fetched: 2026-11-25T10:08:36.552560+08:00
category: "车机"
score: 0
keywords: []
sha256: e8ac517e807b3b0fbdeae07c5c699ff74b056f03cca6d724e110d55f2cdd66a4
bytes: 10265
truncated: false
body_mode: fulltext
kind: practical
status: published
published_at: 2026-11-25T10:09:26.107023+08:00
---

# Brightway 安全再评估：Xiaomi 4 Pro（第二代）把刷机口彻底焊死

> 来源：RoboCoffee · 2023-06-01 · [原文](https://robocoffee.de/?p=897)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：作者拿 Brightway 最新代工机型 Xiaomi 4 Pro（第二代）复查安全实践，发现厂商把原本开放的体系（3 Lite、4、4 Lite）升级成“最不欢迎改机的设备”：固件签名、读保护、调试口封堵全线收紧。
- **价值**：与同系列早期文章对照，是完整的“厂商加固升级 → 破解成本上升”实证；对企业评估产品线安全水位很有参考价值。
- **难度**：高 —— 需要在防护升级后重新找入口。

.entry-header

It’s been a while since my last blog post Hacking Brightway scooters: A case study. I’ve picked up their most recent scooter, the Xiaomi 4 Pro (2nd gen) to see what’s changed in Brightway’s security practices. And, spoiler alert, they really did step up their game! Brightway evolved an open system (3 Lite, 4, 4 Lite, …) into the most modding-unfriendly device one can imagine. Unfortunately, also at the cost of performing repair and maintenance.

## BLE access: „Please enter password“

![image](https://robocoffee.de/wp-content/uploads/2024/10/4pro2nd_6-edited.jpg)

Connecting SWD, but this time, to no avail

Brightway has secured the BLE chip, which is the heart of the dashboard, from external access that would normally be possible via SWD. Any access attempt from the DP (debug port) is denied. According to the manual, the SWD can be locked down with a password that is stored in an „eFuse“ (=EEPROM). In addition to that, an encryption key for encrypting the firmware can be stored in the eFuse. I don’t know if that’s the case here, but certainly the password mechanism is in place. The password has to be sent via HCI UART to the chip using a special programming tool (Windows). SWIO / SWCLK / TX / RX pins are exposed as pads at the bottom of the front side of the dashboard module.

Without knowing the password, the DP cannot be unlocked. This path will not be explored any further because of time constraints … and because I don’t like Windows.

## MCU access: New security layers

![image](https://robocoffee.de/wp-content/uploads/2024/10/4pro2nd_1-461x1024.jpg)

![image](https://robocoffee.de/wp-content/uploads/2024/10/4pro2nd_2_censored-461x1024.jpg)

![image](https://robocoffee.de/wp-content/uploads/2024/10/4pro2nd_3-461x1024.jpg)

![image](https://robocoffee.de/wp-content/uploads/2024/10/4pro2nd_4-1024x461.jpg)

![image](https://robocoffee.de/wp-content/uploads/2024/10/4pro2nd_5-1024x461.jpg)

 4 Pro (2nd gen): Attaching the debugger is a hassle

Unlike before, the controller (MCU) is no longer easily programmable. Here’s a list of new measures undertaken by the manufacturer to secure the device against tampering:

- Bottom lid glued directly to the battery with double-sided tape: Removing the lid risks tearing the blue plastic cover encasing the battery. Safety hazard no. 1.
- Controller trapped inside a plastic box: The controller is hardly accessible due to a black plastic box enclosing it. While the box can be unscrewed, the controller is trapped inside. Only after removing the sealing at each side the cables are given more leeway, allowing the controller to be pulled out just so slightly. Since the main capacitor is charged with 50V or so, fiddling inside the box to remove all connectors gives us safety hazard no. 2.
- Controller dipped in conformal coating: The amount of acrylic(?) material to seal the PCB used is mind boggling. It’s clear that this isn’t just water protection, but also tamper / maintenance protection. Repairing this controller likely involves these two steps: 1. dispose of the controller 2. install a new sample.
- MCU SWD pins not exposed: At least the top part of the PCB does not have any traces leading to the SWD pins of the MCU. This underscores my theory that this controller was never meant to be maintained after production.
- MCU underneath main cap: The MCU is stationed right below the biggest capacitor on the board, which carries significant charge. The cap has to be bent up to access the MCU.
Caution: Don’t touch without discharging! Expect a big spark upon bridging the legs with a screwdriver (my method). Better use a resistor for discharging.
- MCU Read-Protection (RDP): It’s not possible to read out the flash of the controller due to read-out protection. The SWD pins on the chip are enabled and debugging is possible, which means RDP Level 1 is in place.
- Firmware checksum verification: Custom bootloader code that calculates the checksum over all firmware bytes and denies updating / booting if its checksum doesn’t match. Modification is not possible without internal knowledge of this function and the location of the checksum bytes.

## Moddin-de-firmwhere

Even though RDP Level 1 is in place, the firmware can be extracted using a specially crafted attack. I’m not going to disclose how, but let me say it’s a known tactic.

The firmware in fact consists of two firmwares: DFU bootloader and main firmware (incl. bootloader). Depending on the flash configuration, either one or the other is mapped to memory location 0x0. Upon entering DFU mode, e.g. when updating the firmware, the DFU bootloader starting at flash address 0x8000000 is mapped to 0x0 and the controller is restarted to boot that code. After a successful program attempt, the firmware starting at address 0x8003000 is mapped to 0x0 and the controller is restarted to boot up the firmware.

There’s also the usual user data section, containing board serial number (SN) and scooter SN… but also a special 16 byte UID, which will be important in a short moment!

![image](https://robocoffee.de/wp-content/uploads/2024/10/image.png)

Flash dump of 4 Pro 2nd gen showing three sections: DFU bootloader, main firmware and user data

There are two possible ways to load firmware to the controller: SWD (relatively easy) or using the DFU process (hard). The first one is interesting, but we’ll dig deeper into the second approach.

## DFU over UART

When I first tried to reverse engineer the UART protocol implemented by Brightway I failed miserably. This time I didn’t! A standard two-wire UART (TX+RX) implementation running at baudrate 19200 (8 bit, 1 stop bit, no parity) is used. With that said, sniffing the UART traffic is straight-forward to understand the messaging protocol.

I’ve recorded the messages exchanged during a firmware update to replicate the DFU process, which can be outlined as follows:

- Mutual authenticatiion
- DFU writes / Sending firmware packets
- DFU verification
- DFU completion (restart)

Step 1 is arguably the most difficult one to hack due to the custom key derivation and verification. You remember the special 16 byte UID mentioned before? Turns out, this UID is used to generate a shared key in a key-derivation process. A series of custom routines scramble this UID into a longer byte sequence (the shared key), which is then used to scramble a random 16 byte challenge sent by the other party and return the 16 byte scrambled response. Since both parties scramble in the same deterministic way, the expected response is calculated in advance and checked against. If this confuses you: the figure below explains it better.

![image](https://robocoffee.de/wp-content/uploads/2024/10/image-2.png)

Mutual authentication between BLE (Alice) and MCU (Bob) using the UID to derive the shared key

When sending firmware packets, the checksum of the packet and the checksum of each data chunk is included as part of the message. However, the chunks / packets themselves are transferred unencrypted, i.e. they’re not encrypted using the shared key. Either way, it wouldn’t increase security by much, since the same update file can be acquired from the mobile device as well and more easily.

## Additional security measures

- Security by obscurity: The MCU found in this scooter model is an unicorn, a Mew glitch, in the far-east outskirts of MCU manufacturing. With no data sheet or whatsoever available, as a researcher, one has to go trial and error mode and use every bit of information gathered from related components.
- Firmware signing and verification in the BLE module: Like with all recent Xiaomi scooter models, it’s not possible to send a modified firmware to the BLE to due signature verification. Since all use the same certs, all firmware files are signed using the same private key by Xiaomi, regardless of the model.
- Bad code / shitty compilers: The MCU firmware assembler code, especially motor control, is hard to read due to code redundancies and missing code encapsulation. There seems to be a „one function to rule them all“ mantra overshadowing the programmers ambition to deliver a functioning system.

## Conclusion

Brightway has learned from their past and locked down both BLE and MCU as the essential components to the integrity of the scooter. A) Access to the BLE is secured by a password. B) Access to the MCU flash is secured by RDP Level 1.

In addition to the known firmware signing, specific measures have been implemented to prevent installation of (modified) firmware. A) The initiation of the DFU process is secured with a shared key and a custom key-derivation function. B) Modified firmware (with wrong checksum) is rejected by the MCU’s DFU bootloader.
Obscure component choices and bad programming habits further enhance the security.

Yet, there’s one glaring problem that overshadows all aspects of added security: Brightway has created a scooter that is impossible to repair. The way the controller is installed into the chassis is extremely maintenance-unfriendly. Since spare parts are practically unavailable for most Brightway scooter models, including this one, buyers with an expired warranty and a malfunctioning controller have little option other than selling the entire scooter for parts.

 .entry-content

 .post-inner

 .section-inner   .pagination-single

 .post
