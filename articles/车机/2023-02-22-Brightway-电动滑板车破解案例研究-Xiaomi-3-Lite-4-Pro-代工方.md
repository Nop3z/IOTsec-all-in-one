---
title: "Brightway 电动滑板车破解案例研究（Xiaomi 3 Lite / 4 Pro 代工方）"
source: "RoboCoffee"
url: https://robocoffee.de/?p=436
published: 2023-02-22
fetched: 2026-11-24T20:29:01.595391+08:00
category: "车机"
score: 0
keywords: []
sha256: b5181b46c454e6a4cab65ed5287992d117db7d5ea6f1344c534e378a42decb44
bytes: 24021
truncated: false
body_mode: fulltext
kind: practical
status: published
published_at: 2026-11-24T20:30:46.008546+08:00
---

# Brightway 电动滑板车破解案例研究（Xiaomi 3 Lite / 4 Pro 代工方）

> 来源：RoboCoffee · 2023-02-22 · [原文](https://robocoffee.de/?p=436)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：Brightway 为 Xiaomi 与 NAVEE 代工滑板车；作者对其 BLE 协议与固件做完整分析，找到可绕过锁车与限速限制的路径，并给出自定义固件的实现方式。
- **价值**：以“代工厂”为切入点的供应链视角——同一套 BLE/固件实现被多个品牌复用，打穿一家等于覆盖多个型号。
- **难度**：中高 —— 需要逆向 BLE 协议与 MCU 固件。

.entry-header

![image](https://robocoffee.de/wp-content/uploads/2023/03/IMG_20230222_141256-768x1024.jpg)

Xiaomi 3 Lite dashboard with attached SWD and UART wires

## Choose your character!

Brightway (Brightway Innovation Intelligent Technology (Suzhou) Co., Ltd.) produces scooters for the NAVEE and Xiaomi brand. The latest additions to the Xiaomi portfolio are the Electric Scooter 3 Lite, 4, 4 Pro and 4 Ultra. With exception of the 4 Pro, all are produced by Brightway. If you’re hearing the name Brightway for the first time and want to learn more about every Xiaomi scooter released, check out my previous blog post.

The cheapest Xiaomi/Brightway model is the 3 Lite. It costs almost the same as the Xiaomi/Ninebot Mi 1S, but has somewhat weaker specs, such as a 5200mAh instead of a 7650mAh battery. So what’s the point of buying this seemingly inferior scooter? Well… it’s security research! By studying the inner workings of the 3 Lite, both from a hardware and a software standpoint, we can shed a light onto how serious Brightway takes security in their scooters.

In this blog post, I will be dismantling my newly bought 3 Lite scooter. After an initial introduction, I’m giving insights into the pairing and activation procedure, after which I describe the available registers, the command and message format and the structure of the serial numbers. It follows a detailed description of all the hardware and respective SOC memory layouts, after which I look at the UART and BLE protocols. Lastly, I will talk about the obvious security flaws discovered in the 3 Lite and how this relates to all other new Xiaomi scooter models.

## Intro

In this section, I’ll be giving a short overview over the essential scooter components, for those of you who are not familiar with previous Xiaomi models or electric scooters in general.

Even though riding the scooter is possible without any app whatsoever, Xiaomi requires you to watch a training video and prove that your the legitimate owner of the vehicle. Only after this is done, restrictions imposed upon speed and such are lifted. Apart from that, an app is helpful for reading or controlling scooter parameters (more in section „Info registers“).

![image](https://robocoffee.de/wp-content/uploads/2023/03/explainer_escooter3-1.png)

Diagram showing all components involved in the scooter communication, based on the latest Xiaomi specification

Several components are involved in the communication between your phone and the scooter. The communication process is the following:

- Create secure channel between the app on your phone and the scooter BLE module, which for Xiaomi scooters is located within the dashboard.
- Send commands from app to scooter over the secure BLE channel.
- Pass commands designated to the electronic speed controller (ESC) or battery management system (BMS) via UART bus.
Commands can have different targets: the dashboard (BLE) itself, ESC or BMS.
- Pass responses, packed into commands, back to the user over the secure BLE channel.

To ensure device security, each one of these components and pathways needs to be secure.

## Pairing process

Xiaomi started rolling out a stronger bonding mechanism with the 3 Lite and 4 Pro models. For connecting with the scooter, you have to download the Xiaomi Mi Home app. After scanning for scooters and selecting your 3 Lite scooter, the app asks for the camera permission. Now, you scan a QR code that’s printed on top of a sticker that covers the dashboard. After the QR code is verified by the app backend server, you’re connected. A button press is no longer required.

The QR code is stored in the app and can be viewed while being connected to the scooter. The app tells you to take a screenshot of the QR code in case you lose the original one.

Usage note: Every time you remove the scooter from the app and re-add it, you have to scan the QR code. However, the verification fails unless you do a BLE hard-reset first (throttle + 5x button press).

## Activation

When you first turn on the 3 Lite it will constantly beep and be speed-limited to 10 km/h. Just like with previous (Xiaomi/Ninebot) models, you have to activate it. The activation button becomes available after watching the usual introduction video in the Mi Home app.

I’m greeted by a firmware update dialog immediately after connecting to the scooter. This update is not mandatory and the dialog can be dismissed.

![image](https://robocoffee.de/wp-content/uploads/2023/02/image-3.png)

Mi Home app offering firmware update for 3 Lite

## Info registers

At this point, I will refer to the Mi Home scooter app as the „Brightway plugin“. The way Mi Home works is that it provides an API which vendors can use to integrate their hardware, as a plugin. Now, since the 3 Lite is produced by Brightway, their plugin looks and feels different from the Ninebot plugin some us of are used to. Nonetheless, the provided functionality and available information is equivalent. By looking into the Brightway plugin script source code, we can locate all register addresses with their respective functions (typos included [sic]).

 AddressFunction00BACTH_REPORT01DRIVE_MDOE02BATTERY_LEVEL03REMAINING_MILEAGE04FAULT05CURRENT_MILEAGE06AVERAGE_SPEED07LOCK08CRUISE_CONTROL09TAIL_LIGHT_ALWAYS_ON0AENERGY_RECOVERY_INTENSITY
[Weak=1E, Middle=3C, Strong=5A]0BTOTAL_MILEAGE0CRUNNING_STATUS0DRECENT_DRIVING_LOG0EDRIVING_Duration0FTOP_SPEED10BATTERY_STATUS11BATTERY_TEMPERATURE12BATTERY_DATE_OF_MANUFACTURE13BATTERY_SN14BMS_FIRMWARE_VERSION15SERIAL_NUMBER16FIRMWARE_VERSION17SCOOTER_TEMPERATURE18RESUME_TO_DEFAULT_SETTING19REMAINING_BATTERY1ABATTERY_VOLTAGE1BBATTERY_CURRENT1CBATTERY_POWER1DLOCK_WARNIING1EMILEAGE_UNIT1FACTIVATION_DATE [4 bytes]20OOB_CODE21CHECK_TIRE_DATERegisters described in the plugin JSON

## Command and package format

The Brightway plugin script gives further insight into the command types and how a package is defined.

 TypeCommand01WRITE02COMMAND03READ11MCU_WRITE_RESPOND12MCU_COMMAND_RESPOND13MCU_READ_RESPOND14MCU_REPORTCommand types

A package consists of DATA plus the checksum of DATA. A custom function is used to calculate the checksum. DATA is defined as follows:
DATA = TYPE + ADDRESS + REST + LEN + PAYLOAD

- TYPE is a command type (see table)
- ADDRESS is a register address (see table)
- REST is the number of packages remaining, in the case where multiple packages have to be send
- LEN is the length of the PAYLOAD
- PAYLOAD is the actual hex values to transmit

Both the command sent to the scooter and the commands received follow this format specification.

## Serial numbers

Brightway scooters have a 20-character SN format:
5-digit prefix + '/' + 14-character suffix.

The SN prefix is used to identify different regions. The following table shows all known prefixes for the 3 Lite (valid prefixes start with a ‚3‘) and their restrictions.

 SN PrefixRegionBacklightOnCruiseControlSpeed37707DE❌❌❌37713??❌❌❌37708??✅❌❌37712??✅❌❌37701??❌✅✅37714??❌✅✅OthersGlobal✅✅✅All 3 Lite SN regions with their restrictions
✅: No restriction
❌: Restricted

SNs are stored on MCU (ref. 0x93FC in EEC0130, 0x23f14 in image) but read and processed by BLE (ref. 0x1e63e in MCU0214).

## BLE Encryption / Decryption

The 3 Lite broadcasts the BLE device name „dreame.scooter.epro“. The naming choice isn’t surprising: in my last blog post I explained the relation between Brightway and Dreame.

![image](https://robocoffee.de/wp-content/uploads/2023/03/image-10-1024x606.png)

NrfConnect showing the 3 Lite BLE broadcast data

The 3 Lite provides a BLE GATT service for authentication and another service for TX/RX and broadcasting the button press using the followings UUIDs:

- Service: 00000101-0065-6C62-2E74-6F696D2E696D
- TX/RX: 00000100-0065-6C62-2E74-6F696D2E696D
- Button: 00000102-0065-6C62-2E74-6F696D2E696D

For BLE authentication the Brightway plugin uses MIOT BLE SecurityLock: encryptMessage() and not encryptMessageWithToken(). What’s the difference, you ask?

- encryptMessage() uses MIOTBluetooth.encryptMessageXiaoMiBLE() -> securityChipEncrypt() [Same as StandardAuthEncrypt()] -> ECDH with secp256r1 curve (we know this crypto)
- encryptMessageWithToken() uses MIOTBluetooth.miotBleEncrypt() -> miotBleEncrypt() -> BLECipher (MixA, MixB, old crypto)

We already know the type of encryption/decryption scheme used. What’s new is the call of the function securityChipEncrypt(). Wait, what… Security chip? Very interesting! A BLE packet sniff reveals an exchange of certificates, likely related to the QR code. Further, memory footprints contains records of a 7-step authentication process involving the secure chip. This is a noticeable divergence from previous authentication methods.

Unverified: Since the QR code is used for bonding, it likely contains data which can only be decoded by the Mi Home app. This data could be the certificate (public key) that is transmitted in the key-exchange.

## Hardware breakdown

The following section identifies all ICs used by the manufacturer. This is a necessary step for the examining device security and the potential for modification.

Starting with the dashboard, it has the label „P2185_Display_V2.0 211126“ printed on it. The dashboard looks almost identical to the „P2223_Display_V1.0.1 20220111“ of the NAVEE S65. Luckily for us, both boards expose them SWD ports! The P2223 has all SWD pins labeled, the P2185 has not (but, it’s easy to find out). Check the image below for the correct SWD pin assignment.

![image](https://robocoffee.de/wp-content/uploads/2023/02/image-13-826x1024.png)

P2185 („3 Lite“): SWD pins identified

![image](https://robocoffee.de/wp-content/uploads/2023/02/image-7.png)

P2223 (NAVEE S65): [[Source](https://fccid.io/2A4GZ-S655001B/Internal-Photos/Internal-photos-5956907.pdf)] reveals a lot of internal information

We already observed the app code hinting at the existence of a secure chip. When first examining the hardware, I could not find any such chip. Only with the help of my microscope and zooming into one of the small ICs on the dashboard I could locate a component that turned out the be the legendary „MJA1“ secure chip!

![image](https://robocoffee.de/wp-content/uploads/2023/02/image-1.png)

Dashboard comes with a MJA1 secure chip – I’m probably the first person posting a photo of this special Xiaomi component! VendorPart numberFunctionXiaomi/RealtekMHCB05P-IB module with RTL8762C chipBLE MeshXiaomiMJA1 HCIWSecure chip?????? (hidden underneath display)20-Pin Display driver ICDashboard components

As for the ESC, the part numbers are difficult to read, since the board is potted in a thick layer of transparent encapsulation resin (too thick to be conformal coating). Nevertheless, I could identify all but one component with my microscope, by using its integrated light source past the reflective layer.

 VendorPart NumberFunctionLinkosemiLKS32MC081C8T8Motor control unitThinkisemiP55NF061N-channel power MOSETSilan (SL)[SD4931](https://xonstorage.blob.core.windows.net/pdf/silan_sd4931_xonjuly20_20_link.pdf)Current mode PWM controllerSamwinSW062R08E8T6x N-channel enhanced mode MOSFET???IDR??ID200??N428M7RV????Controller (ESC) components

![image](https://robocoffee.de/wp-content/uploads/2023/02/image-2.png)

The only ESC component I could not identify

## This SoCs!

Having identified all hardware components, it took me quite some time to gather the relevant documents and get a clear understanding of the SoC characteristics. This section lists the specs and the memory mapping table of each SoC.

 TypeSOCFamilyArchRAMROMFlashBLERTL8762C (MHCB05P)Cortex-M4ARMv7-M128KB384KB512KBMCULKS32MC08xCortex-M0ARMv6-M8KB1KB64KBSOC specs: MCU has limited resources – logic is handled by BLE! AreaStart addressEnd addressSizeFunctionROM0x00x5 FFFF384KBBootloader, BT-Stack, Flash driverRAM (Data)0x20 00000x21 BFFF112KBRAM code> ROM Data0x20 00000x20 2FFF12KBVariables of ROM> Main Stack0x20 30000x20 37FF2KBMSP> Patch RAM10x20 38000x20 7BFF17KBVariables/RAM code of Patch> APP/Data RAM0x20 7C000x21 7FFF65KBVariables/RAM code of APP + Data heap> Patch RAM20x21 80000x21 BFFF16KBOptional, same as Patch RAM1RAM (Cache)0x21 C0000x21 FFFF12KBSpeed up SPI Flash R/WSPI Flash (Cached)0x80 00000x9F FFFF512KBWith cache (faster)> Reserved0x80 00000x80 0FFFReserved> OEM Header0x80 10000x80 1FFFConfig: BT address, AES Key, flash layout> OTA Bank 0––Data and code> OTA Bank 1––Same as Bank 0> FTL––Access flash with logic address> OTA Temp––OTA backup> APP Defined––User definedMemory mapping: RTL8762C AreaStart addressEnd addressFLASH (NVR)0x00x3FFFLASH (MAIN)0x00xFFFFRAM0x2000 00000x2000 1FFFSYS CTRL0x4000 00000x4000 03FFFLASH CTRL0x4000 04000x4000 07FFMemory mapping: LKS32MC08x

## UART

The bus between dashboard and controller is no longer realized by a single-wire (1-wire) UART, like in previous Xiaomi scooter models. The 3 Lite downright uses the standard UART mode: one wire for TX, one wire for RX. The MCU-UART is configured as follows: baudrate = 19200, data length = 8 bit, stop bit len = 1 bit, LSB, even parity, check disabled, multi-drop disabled.

Curiously, my recordings do not contain messages, but pulses with three possible state values.

 ValueMeaning20floating(F)30low(L)65high(H)UART protocol: only three different values

A single pulse follows the pattern: F[H|L][H|L]

In reality, only two of the four possible combinations are used: FLL, FHL. We can conclude that FLL translates to „0“ and FHL translates to „1“. I visualized the sampled data using a tool called binocle, which helps identifying recurring patterns.

![image](https://robocoffee.de/wp-content/uploads/2023/03/image-3.png)

Commands send via UART-TX, visualized with binocle

![image](https://robocoffee.de/wp-content/uploads/2023/03/image-7.png)

Data received via UART-RX, visualized with binocle

At the time of conducting the experiments and recording the UART transmission, I didn’t know about the correct parameter stated in the first paragraph. For recording the data, I used a higher baudrate than specified by the MCU. Please leave a comment, if you can verify seeing similar values and patterns in your recording with the correct baudrate set.

If we assume these captures to be accurate, then it means that both the BLE and MCU have a buffer to store incoming packets and then translate them back to messages, as defined in the „Commands and message format“ section.

## 3 Lite: Security oversights

Both the dashboard and controller board expose debugging pins (SWD). These have been left active and allow connection via OpenOCD. I quickly discovered the first security oversight by Brightway: the manufacturer left the content of both SOCs unprotected! I was able to generate full dumps of both BLE and MCU firmware, without any special measures, following the memory mapping tables laid out above.

The second oversight is that the firmware update (OTA) files for both the BLE (called „EEC“) and MCU come unencrypted, meaning that they can be decompiled without further measures. Analysis of these files allowed me draw some of the conclusions in this blog post, e.g., about the UART configuration. I could further observe that the MCU firmware, being very limited in size, contains almost no logic and that its main purpose is motor control.

Last year, Xiaomi introduced firmware signing to secure the BLE firmware from tampering. The BLE/EEC firmware for 3 Lite is signed in accordance to this new Xiaomi standard. However, the MCU firmware is not! This could potentially allow altering the content of the update (OTA) file before passing it to the BLE. This has the hard requirement of having the authentication and update procedure fully reverse-engineered.

What’s strange about the MCU firmware OTA file is that it’s almost three times larger than the MCU flash size. Next to the MCU flash/app content, this file contains one large code section of what seems to be executable DFU loader code and another section of what seems to be executable post-installation / setup code. Should it prove to be correct that the MCU OTA file is packed with executable code that the BLE willingly executes, one could try injecting their own code. This has a potential to defeat every security measure mentioned so far, but also serious implications for the scooter safety. But again, proving this would require full knowledge of the authentication and update process.

While the authentication process (pairing with QR code, secure key exchange) doesn’t seem to have any obvious flaws, Brightway has left room for debugging and possible modification of the scooter. It is a misunderstanding that authentication with a secure chip provides absolute security. It’s main safety mechanism is to prevent tampering with the device of someone else, because we don’t have the QR code (certificate) to pair with that (secure chip). The secure chip doesn’t prevent you from hacking your own scooter. This is how it should be!

## 3 Lite: Custom firmware?

The Realtek BLE module uses SPI to communicate with the flash. The (unsurprising) fact is that this module doesn’t allow writing bytes to the memory-mapped flash directly. The RTL8762C SoC comes with a feature called block protect and the manual states the following regarding write protection: „The protected flash zone can’t be written and erased. If necessary, user can unlock flash first, and then write or erase, finally lock the flash to the previous level.“ Realtek provides both an API for reading and writing to flash and tools for programming. This means that flashing a custom firmware to the BLE module is just a matter of figuring out the correct programming procedure!

As for the MCU: If you’re familiar with the flash controller in STM32, the LKS32 MCU isn’t too different. It has a register for enabling the programming mode, a register for the address to program and a register for the data to be written to that address. In my tests, writing single bytes (words) using the LKS32 flash controller was unsuccessful (also, writing single bytes to the memory-mapped flash didn’t succeed). Based on hints in the manual, it’s very likely that a prior erasure of the flash region to be written to is necessary!

#### BLE custom firmware

Up to this point, everything I did so far was non-destructive. In order to not risk bricking my newly brought scooter and keeping the factory settings intact, I bought a much cheaper Xiaomi device that comes with the exact same BLE module for experimentation. Both devices contain the exact same ROM image and there’s no setting (so called „eFuse“) in EEPROM that might potentially disable flashing. Therefore, the process and outcome of flashing the scooter BLE module is expected to be exactly the same.

I was able to erase the existing firmware from the BLE module and flash a modified 3 Lite BLE firmware back to it. My modification, for demonstration, is simply changing the device name from „dreame.scooter.epro“ to „dreame.scooter.nono“ . This shows that a 3 Lite custom firmware could very much be possible, in theory!

![image](https://robocoffee.de/wp-content/uploads/2023/03/image-13-1024x783.png)

Successfully flashed back modified firmware to Xiaomi BLE module with device name altered

#### MCU custom firmware

Custom firmware can be flashed to LKS32MC081 MCU without limitations using the SWD port. After flashing the original 3 Lite MCU firmware, I was able to erase and reprogram the chip with a modified original firmware.

## What about other new Xiaomi models?

Thanks to internal FCC documents we can tell that the hardware of the Xiaomi/Brightway 3 Lite and the Xiaomi/Brightway 4 (non-Pro) model look similar. The MCU has the same amount of pins and we can make out exposed SWD pads. Overall, the board design, including caps and connectors, looks familiar. Chances are, that the 4 Ultra comes with the hardware described in this post.

The Xiaomi/Ninebot 4 Pro, like all other other new Xiaomi scooter models, uses the same BLE module as the 3 Lite, as disclosed by a Bluetooth certification. This means that the 4 Pro uses the same BLE stack and Xiaomi core libraries for authentication. As for the controller, the 4 Pro uses a STM32 based board in the tradition of previous Ninebot scooters; the STM32 MCU is well established in the scooter modding community.

![image](https://robocoffee.de/wp-content/uploads/2023/03/IMG_20230222_093011-461x1024.jpg)

Xiaomi/Brightway 3 Lite: MCU with 48 pins underneath blue cap

![image](https://robocoffee.de/wp-content/uploads/2023/03/mi4esc-1-edited.png)

Xiaomi/Brightway 4: [[Source](https://fccid.io/2A4GZ-M403001B/Internal-Photos/Photos-internal-5981160.pdf)] shows MCU, also with 48 pins, blue cap and SWD pads

In a nutshell, the new Xiaomi models could be pwned as follows:

For 3 Lite + 4 + 4 Ultra, the easy way would be to modify the existing MCU firmware and flash it via SWD. The hard way would be developing and flashing a custom BLE firmware for the (Realtek) BLE module that bypasses the secure chip, with a custom MCU OTA flashing procedure.

For the 4 Pro, there is no easy way at this time. A possible way is to develop and flash a custom ESC firmware for the STM32 board. This firmware could be based, for example, on the OpenSource SmartESC firmware. The hard way would involve a custom BLE firmware, just like for the other models (same BLE module).

## Summary

In this research, I had an extensive look at the hardware, software and security implemented by Brightway, the new Xiaomi scooter supplier, by examining their 3 Lite scooter model. I could fully dump both the BLE and MCU flash content, get a glimpse at the OTA procedure and the command & communication protocol used by in the 3 Lite.

My conclusion is that Brightway scooters, at the example of the 3 Lite, are secure from hostile takeover by a third party, thanks to the use BLE authentication using the secure chip, but open for your own modifications!

I have shown that both chips can be (re-)programmed through the respective (enabled) SWD port: I was able to flash a modified 3 Lite BLE to an identical Xiaomi BLE module, which suggests that BLE custom firmware is possible on the actual device. I was also able to flash (and re-flash) the original 3 Lite MCU firmware to an identical LKS32 MCU, which suggestes that MCU custom firmware is possible.

At the time of writing, I could not discover any security exploits that would warrant a notification of the manufacturer. As for the security flaws, such as missing encryption and read-out protection of the firmware files, I assume that the manufacturer is well aware thereof. Please understand that I will not go into detail of the exact flashing procedures. Further, the question how regional restrictions such as speed limits can be removed are not the scope of my research.

 .entry-content

 .post-inner

 .section-inner   .pagination-single

 .post
