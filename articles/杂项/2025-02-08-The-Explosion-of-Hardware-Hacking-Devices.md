---
title: "The Explosion of Hardware-Hacking Devices"
source: "Eclypsium"
url: https://eclypsium.com/blog/the-explosion-of-hardware-hacking-devices/
published: 2025-02-08
fetched: 2026-11-19T12:19:24.110575+08:00
category: "杂项"
score: 0
keywords: ["hardware", "tooling", "fault-injection"]
sha256: daaac5fa66f083177f4750c7ce192f277a4ad13ac9a391a8da89a3cb0920b52b
bytes: 16645
truncated: false
body_mode: fulltext
status: published
published_at: 2026-11-19T12:20:43.910308+08:00
---

# The Explosion of Hardware-Hacking Devices

> 来源：Eclypsium · 2025-02-08 · [原文](https://eclypsium.com/blog/the-explosion-of-hardware-hacking-devices/)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：盘点近年硬件攻击设备的爆发：ChipWhisperer 类毛刺台、逻辑分析仪、EMFI 装置、芯片开封与探针台等。
- **价值**：物理攻击的门槛正在快速下降，硬件安全不再是少数实验室的专属；这份清单适合用来评估自己的设备面对什么级别的对手。
- **难度**：中 —— 综述/工具盘点型。

Blog

# The Explosion of Hardware-Hacking Devices

By: Paul Asadoorian

Published: February 7, 2025 |Last Updated: July 28, 2026

Due to the growing popularity of the ESP32 IoT platform adoption by security professionals, this article raises several security concerns addressing firmware attacks that could target this user population and what you can do to protect yourself.

Watch Paul Asadoorian’s Webinar: Hardware Hacking: Tools, Tips & Tricks for Total Domination

Introduced in August 2020 following a $4.8 million Kickstarter campaign, the FlipperZero quickly became one of the most sought-after hacking devices. Touted as a “Swiss-Army Knife” of RF (radio frequency) and other attacks, it spawned a community that grew quickly and appealed to both new and experienced hackers alike.

![image](data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%201600%201170'%3E%3C/svg%3E)

A FlipperZero with the ESP32-based Wi-Fi module in a custom 3D printed enclosure.

Priced at $169 (when the supply was low, they were sold on Amazon for over $200), the FlipperZero caused some controversy. Amazon banned the sale of the devices on their online retail platform, and Canada proposed new legislation to ban them from being sold country-wide. Both bans were primarily fueled by reports that FlipperZeros could be used for nefarious purposes. In the case of Amazon, the FlipperZero was deemed a “card skimming device,” violating their policy prohibiting the sale of “theft devices”. The proposed Canadian ban deemed the device a tool for car theft (The company behind the FlipperZero published a detailed report essentially debunking this claim). Canada has since backed off on FlipperZero bans. However, Amazon still does not allow the sale of FlipperZeros on their site.

Many activities mentioned above, such as FlipperZero’s high price tag compared to similar hardware and a history of availability issues, have led developers and hackers to adopt the ESP32 platform as a FlipperZero alternative. The ESP32 and associated add-ons are being developed to mimic as much of the FlipperZero functionality as possible for a fraction of the price and on hardware platforms that were not in the crosshairs of ridiculous bans (e.g., you can purchase several different types of ESP32-based devices on Amazon, including ones you have to put together yourself and others that come fully functional and assembled already).

Available firmware for the following platforms continues to grow including:

- LiliyGo
- M5Stack
- Cheap Yellow Displays (CYD)

![image](data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%201600%20900'%3E%3C/svg%3E)

Example: A LilyGo T-Embed CC1101 device running the Bruce firmware. The CC1101 allows for Sub-GHz communications, and the hardware supports Wifi (2.4GHz), BLE, IR, and more.

Several firmware platforms exist, ranging in functionality from BadUSB, Sub-GHz communication, IR libraries to interact with over 1,000 devices, Bluetooth and Bluetooth Low Energy (BLE attacks, such as “AppleJuice), and more. Some of the more popular firmware platforms include:

- Bruce
- ESP32-Maurader (The CYD Port is here)
- Evil-M5Project

There are so many firmware options to choose from that developer “bmorcelli” created the M5Stick-Launcher, firmware dedicated to allowing the user to select and boot different firmware distributions directly from the SD card or OTA (Over-The-Air). While the name indicates that only M5Stack devices are supported, several other types of devices have been added, including the CYD.

![image](data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%201600%20900'%3E%3C/svg%3E)

A Cheap Yellow Display running the M5Stick-Launcher firmware. While the name implies this firmware only supports M5Stack devices, it has been ported to several other ESP32 devices. The launcher lets you boot firmware from an SD card or over the air.

I’ve been following this trend closely, as when I attended Shmoocon 2023, it seemed everyone but me had a FlipperZero. I acquired a FlipperZero device and several add-on boards supported via the GPIO pins on the FlipperZero. I quickly moved to purchasing less expensive hardware and experimenting with alternative firmware (some may remember visiting us at GRRcon, where we gave away several M5Stack devices and taught folks how to install various firmware distributions).

## The Shmoocon Talk (2025)

Late last year, two of my favorite hacking companions (Larry Pesce and Bill Swearingen) began working on a project to turn the CYD into a basic Airtag scanner (Github link). While you can scan for Airtags with many different devices (including your Android phone or FlipperZero), their goal was to create an inexpensive project that people could pick up to learn more about BLE, the ESP32, and specifically the CYD that can be purchased for as little as $11. I wanted to learn more about programming the ESP32, specifically for “security research” purposes, as there is a flourishing community of ESP32 enthusiasts who are customizing devices for ESP32Home and a long list of other projects.

![image](data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%20174%20300'%3E%3C/svg%3E)

A CYD (Cheap Yellow Display, USB-C version) running [a fork](https://github.com/pasadoorian/CYD-BLE-Tools) of the Airtag scanner firmware was presented at Shmoocon 2025. The case was 3D printed (Thanks to “dawidlos” for the design: [Download from Makerworld](https://makerworld.com/en/models/890009#profileId-846321)).

Bill Swearingen and Larry Pesce presented “Detecting BLE Trackers for the price of a Gas Station Hot Dog” at Shmoocon 2025 and gave an overview of the CYD platform, BLE, and the basics of how to program them using the Arduino IDE. The talk is here:

   Note: Due to technical difficulties, there was no audio for the first part of the presentation.

Inspired by this talk, I began researching the ESP32 platform and developing the ESP32 Airtag scanner code myself.

## ESP32 Hardware & Firmware

I sought to learn more about the ESP32 platform, including the various development environment options, hardware specifications, and security. Below is a brief overview:

- The company behind ESP32 is Esspressif Systems. They offer various ESP32 chips for IoT applications; the most common configurations include Wifi (2.4GHz) and Bluetooth/BLE.
- The original ESP32 series uses a Tensilica Xtensa 32-bit LX6 microprocessor, and the ESP32-S series has an upgraded Tensilica Xtensa LX7 processor, while newer models (such as the ESP32-C5, sneak preview here) use a RISC-V 32-bit processor.
- For developers, you can compile binaries that run directly from the hardware. However, this requires some heavy lifting and writing much of the code yourself without the assistance of 3rd-party libraries. Depending on your requirements, developers will choose one of the following libraries/development frameworks:

- ESP-IDF – This is the development framework from Espresif Systems. It allows you to control the ESP32 at lower levels, including creating binaries that run directly on the hardware, full multi-tasking code for FreeRTOS, and the ability to customize the bootloader to implement secure boot and/or firmware encryption.
- Arduino – The Arduino IDE is a great place to get started as it builds on top of ESP-IDF and provides developers with a FreeRTOS implementation (single-threaded), the Arduino API, which includes several libraries that make it easier to interface with the hardware, and a complete IDE.
- PlatformIO – PlatformIO is a cross-platform development environment that allows you to manage dependencies and libraries for several boards and microcontrollers. It allows you to work with either Arduino or ESP-IDF, with configurations defined in files called platformio.ini. PlatformIO can also be easily integrated into VSCode. While there is a slight learning curve, I chose this option as VSCode is a nice IDE, and I needed to compile firmware for a few variants of the CYD.
- The ESP32 supports security features as well, including:

- Secure Boot – If you are using the ESP-IDF, you can enable Secure Boot. Remember that once Secure Boot is enabled, it cannot be disabled, as the configuration option is stored in an eFuse. The key(s) is also stored in an eFuse.

- Note: Two versions of Secure Boot for ESP32 exist: Secure Boot V1 (RSA-3072) and Secure Boot V2 (AES-CMAC). The documentation recommends Secure Boot V2 because it is safer and more flexible than Secure Boot V1. Please also note that Secure Boot on the ESP32 platform is an entirely different implementation from UEFI Secure Boot.
- Flash Encryption – This feature also requires the ESP-IDF and uses eFuses to store the key to decrypt the firmware image. A complete tutorial can be found here: ESP32 Flash Encryption. At Blackhat USA 2022, researchers presented Unlimited Results: Breaking Firmware Encryption of ESP32-V,3 including details of security flaws in the platform.

Armed with a bit more knowledge of the platform and a bit of experience developing for the ESP32, my focus shifted towards threat modeling and how to address some of the potential security issues.

## Security & Supply Chain Concerns

## Firmware Flashing

One of my initial concerns was how most people are flashing firmware on devices. Many ESP32 users are security researchers and security professionals, and the most popular (and recommended) method for firmware flashing is a web interface. Relying on the ESP Web Tools project, several of the popular firmware distributions publish a website that flashes your device. The process is simple: connect your device to your computer via USB (putting it in bootloader mode, most commonly by holding the boot button, then plugging in the USB cable), visit the website, select the device and firmware, then select the USB TTY port. The website will flash the firmware for you (Meshtastic, a LoRa WAN firmware distribution, also uses the web flashing method as the devices for LoRa are also ESP32-based).

The security issues with this process are as you imagine and beg questions such as: How do I validate the firmware? How do I detect backdoors in the firmware? I could not find any great solutions. If threat actors want to be evil, an attack path would be to compile firmware with Secure Boot enabled and not provide a valid key or signing process. The device would essentially be bricked since Secure Boot is a one-time enabled feature using an eFuse. Backdoors could also be deployed, potentially using the Wifi interface to communicate with a C2 service if Internet access is available. ESP32 devices could also be backdoored to execute code when connected to computers via USB, as this is common when developing for firmware flashing and when in use for monitoring messages over the USB serial. Security researchers are sometimes targetted by threat actors, including most recently when Github repositories containing source code for PoC exploits were backdoored.

## Supply Chain Analysis

Other potential security issues arise when we wish to validate the firmware source code and determine if there are known vulnerabilities or backdoors either in the code itself or (more commonly) derived from 3rd-party libraries. The development environments, such as PlatformIO, make it easy for developers to get up and running by automatically pulling in the required code libraries. For example, the platformio.ini file contains dependencies defined as:

```
lib_deps =
    bodmer/TFT_eSPI
    SD
    bblanchon/ArduinoJson @ ^7.0.4
```

This is very similar to a Python requirements.txt file. Also defined in the same file is the main development environment, which will also pull in other required libraries and board definitions based on these values:

```
[env]
platform = espressif32
board = esp32dev
framework = arduino
```

Since I am pulling in code from 3rd party sources I may not trust, I set out to validate the code libraries being pulled in automatically. After some research, it was suggested that I first try the inspection feature in PlatformIO. This feature will inspect all source code for performance and analyze static code to flesh out bugs. It did review the source code, including all libraries, with the following results:

![image](data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%201234%20742'%3E%3C/svg%3E)

![image](data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%201238%20389'%3E%3C/svg%3E)

While it did find one potential bug in a 3rd party library and provided me with interesting performance and resource consumption statistics, I was still left wondering what else may be lurking in the supply chain of my firmware.

Further research revealed that Grype is a great option for evaluating the supply chain of your containers and source code and supported C++ (which is what ESP-IDF/Arduino supports). I ran Grype against my project:

![image](data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%201399%20243'%3E%3C/svg%3E)

There is not much luck there either, as Grype may not have the necessary features to support ESP32 development.

## Conclusion

The rapid proliferation of IoT devices and open-source hardware platforms like the ESP32 has democratized security research but has also introduced critical risks. Security researchers and threat actors may use the same tools, and threat actors will continue to target firmware-based devices of all types. From state-sponsored APTs like Volt Typhoon and Velvet Ant, exploiting zero-day vulnerabilities in Cisco NX-OS and F5 load balancers to commodity hardware like the $11 CYD being repurposed for BLE tracking, the attack surface is expanding faster than many organizations can defend.

- Firmware Integrity is Non-Negotiable: Secure Boot and Flash Encryption (e.g., on ESP32 platforms) are essential but not practical in security research and development scenarios, leaving the door open for attackers to attack the firmware supply chain. The Pacific Rim campaign’s UEFI implants on Sophos firewalls underscore how attackers bypass cryptographic checks by tampering with verification binaries.
- Supply Chain Vigilance: Third-party libraries and automated dependency tools (like PlatformIO) introduce hidden risks. Tools like Grype and EMBA can help audit firmware for vulnerabilities, but proactive validation of code sources remains critical.
- Monitor the Unmonitored: Firewalls, load balancers, and consumer routers are now being weaponized for C2 and data exfiltration. Behavioral analysis and firmware-level telemetry (e.g., Eclypsium’s platform) are necessary to detect device anomalies often excluded from traditional security monitoring. For microcontrollers and single-board computers, more diligence and manual inspection are required for security validation.

Defenders and security/network vendors must adopt a “zero trust” mindset for firmware and embedded systems. This means:

- Enabling hardware-rooted security features (Intel Boot Guard, Secure Boot).
- Treating firmware updates with the same urgency as software patches.
- Auditing IoT device configurations to minimize attack vectors (e.g., disabling exposed HTTP/SSH interfaces).

The era of assuming “purpose-built” devices are inherently secure is over. Whether it’s a $5,000 firewall or an $11 ESP32 gadget, every component in your network is a potential target – and securing it requires visibility, rigor, and a willingness to challenge vendor assurances.

## Resources & Further Reading

- Arduino Maestro – A GPT tuned for Arduino development (one of the better ones that I’ve tried and works great, especially for debugging help).
- M5Stick-Launcher – An application launcher for several different ESP32 platforms. Once this firmware is flashed on the device,e you can load firmware at boot time from an SD card or over the air.
- https://github.com/witnessmenow/ESP32-Cheap-Yellow-Display – General information about the CYD, including where to buy, the different hardware variations, and flashing firmware.
- https://github.com/hevnsnt/CYD_ESP32-AirTag-Scanner – The original firmware that was developed for the Shmoocon 2025 talk.
- https://github.com/pasadoorian/CYD-BLE-Tools – This is my fork of the code above, several features were added. This is still in development and should be considered experimental. (Note: this code borrows heavily from https://github.com/bmorcelli/M5Stick-Launcher).

Back to Blog
