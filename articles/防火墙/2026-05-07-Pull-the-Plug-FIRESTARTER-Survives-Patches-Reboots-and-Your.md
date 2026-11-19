---
title: "Pull the Plug: FIRESTARTER Survives Patches, Reboots, and Your Incident Response Plan"
source: "Eclypsium"
url: https://eclypsium.com/blog/firestarter-cisco-firewall-backdoor-survives-patches/
published: 2026-05-07
fetched: 2026-11-19T12:19:24.110575+08:00
category: "防火墙"
score: 0
keywords: ["firmware", "implant", "cisco"]
sha256: 354fbc3938f2b223a899eb3f2a3b6513b85d8b48a83b89975c361e64631a3fa4
bytes: 15459
truncated: false
body_mode: fulltext
status: published
published_at: 2026-11-19T12:20:43.910308+08:00
---

# Pull the Plug: FIRESTARTER Survives Patches, Reboots, and Your Incident Response Plan

> 来源：Eclypsium · 2026-05-07 · [原文](https://eclypsium.com/blog/firestarter-cisco-firewall-backdoor-survives-patches/)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：分析植入 Cisco 防火墙的持久化后门 FIRESTARTER：打补丁、重启、常规应急流程之后它依然存在。
- **价值**：“打了补丁就安全”是边界设备最常见的误判；这类引导/固件层植入要求把清点、重装和取证流程一起升级。
- **难度**：高 —— 需要固件层取证与设备镜像比对能力。

Blog

# Pull the Plug: FIRESTARTER Survives Patches, Reboots, and Your Incident Response Plan

By: Paul Asadoorian

Published: May 7, 2026 |Last Updated: May 6, 2026

A Linux backdoor hooks the firewall data plane (LINA) on Cisco ASA and Firepower devices, persists through firmware updates, and only a full power cycle gets rid of it.

## The Patch Is Not the Fix

You patched your Cisco ASA. You rebooted it. Your vulnerability scanner shows green. You closed the ticket. However, the backdoor is still there!

That is the actual operational reality CISA and the United Kingdom’s National Cyber Security Centre (NCSC) put on paper in Malware Analysis Report AR26-113A, published April 23, 2026. The malware is called FIRESTARTER. It is a Linux ELF that runs on Cisco Firepower and Secure Firewall devices, hooks the LINA process, and re-installs itself after every termination signal it receives.

A Quick Note on LINA

LINA is the core data plane process on Cisco firewalls. It handles the actual firewall functionality, including stateful inspection, ACLs, NAT, routing, and VPN termination (including WebVPN). The binary sits at /asa/bin/lina on the device and runs as a userland process on top of Linux.

On Cisco ASA devices, LINA is the whole show. The OS underneath exists to keep LINA running. There is no other inspection engine in the data path. On Cisco FTD (Firepower Threat Defense) devices, the architecture is split into two parts. LINA still does the firewall and VPN work, exactly like on ASA. Snort runs alongside it to handle deep packet inspection, IPS, and application identification. The two processes communicate internally, and traffic flows through both. FIRESTARTER does not care which platform you run. It hooks LINA, and LINA exists on both.

That is why hooking LINA matters. Hook the process that parses WebVPN requests, and you get a covert trigger that arrives as ordinary VPN traffic without requiring a new listener/port.

FIRESTARTER survives reboots, firmware updates, and patches, including those that closed the original CVEs used to install it. The only way to remove it is to physically unplug the device from every power source for at least 1 minute. Redundant power supplies count. Soft reboots do not. If you do not pull the cord, the backdoor stays.

This is the part of the network that almost everyone treats as out of scope for endpoint security tooling. There is no EDR agent on your firewall. There is no XDR telemetry. The device sits at your perimeter, and you trust it. That trust is exactly what threat actors are counting on.

## The Campaign: ArcaneDoor, UAT-4356, and the September 2025 Compromise

FIRESTARTER did not appear in isolation. It is the persistence mechanism for an ongoing intrusion campaign that Cisco Talos tracks as UAT-4356, the same actor cluster behind ArcaneDoor. The original initial access was through two Cisco ASA vulnerabilities patched in September 2025:

 CVETypeCWE[CVE-2025-20333](https://nvd.nist.gov/vuln/detail/CVE-2025-20333)Missing Authorization in Cisco ASA WebVPNCWE-862[CVE-2025-20362](https://nvd.nist.gov/vuln/detail/CVE-2025-20362)Classic Buffer Overflow in Cisco ASACWE-120

CISA published Emergency Directive 25-03 on September 25, 2025, ordering Federal Civilian Executive Branch (FCEB) agencies to identify and remediate compromised Cisco devices. During that response, CISA found a real, in-the-wild FIRESTARTER infection on a Cisco Firepower device running ASA software inside a federal agency.

Note:

Many of the names we have given threat actors, campaigns, and malware targeting Cisco ASA/FTD can be confusing. Below is a brief outline:

- ArcaneDoor: The campaign name (MITRE C0046), not a threat actor or malware reference
- UAT-4356 / STORM-1849: the actual threat actor labels
- LINE DANCER: in-memory shellcode loader for ad-hoc command execution (2024)
- LINE RUNNER: persistent HTTP/Lua implant on ASA (2024)
- RayInitiator: multi-stage bootkit that delivers LINE VIPER (2025)
- LINE VIPER: user-mode shellcode loader, post-exploitation implant (2025)
- FIRESTARTER: ELF backdoor that hooks LINA for long-term persistence (2025, public 2026)

The actor first deployed an implant called LINE VIPER for post-exploitation, used valid VPN credentials from former employee accounts to bypass authentication policies, then installed FIRESTARTER for long-term persistence.

CISA’s report explicitly notes that the actor used FIRESTARTER to redeploy LINE VIPER in March 2026, well after patches were applied. They never had to re-exploit anything as the persistence mechanism did its job.

## What FIRESTARTER Actually Does

The malware sample CISA analyzed was named lina_cs. When lina_cs runs, it copies its own contents from /usr/bin/lina_cs into memory and registers a signal handler, allowing the malware to take action in response to signals (e.g., when the system or user tells the process to restart). It also triggers on runlevel 6, which is the system reboot runlevel on Linux. Which means every time the device shuts down or reboots, FIRESTARTER’s persistence routine fires.

When a termination signal is received or the device reboots, FIRESTARTER reverses the cleanup. It re-creates /opt/cisco/platform/logs/var/log/ if missing, opens /opt/cisco/platform/logs/var/log/svc_samcore.log, and writes a copy of itself to that file. That directory is reboot-persistent. Then it re-stages CSP_MOUNT_LIST, appending shell commands that move the binary back to /usr/bin/lina_cs, set permissions, and execute it in the background:

```
mv /opt/cisco/platform/logs/var/log/svc_samcore.log /usr/bin/lina_cs
chmod 755 /usr/bin/lina_cs
lina_cs &
```

The sequence is straightforward. The device reboots; the boot-time mount script executes the appended commands; FIRESTARTER moves itself out of the log directory back into /usr/bin/; and runs again. Patch the device, update the firmware, reboot, and the boot-time configuration script does the actor’s work for them.

FIRESTARTER works by quietly editing the LINA process in memory. It finds a specific spot inside one of LINA’s loaded libraries and slips in a small piece of code that acts as a trapdoor. Nothing changes on disk, and LINA keeps running normally.

The trapdoor only opens when a very specific WebVPN request comes in, one carrying two secret values that act like a key and a victim ID. If both match, FIRESTARTER drops the next stage of malware straight into LINA’s memory and runs it. That is how the actors redeploy LINE VIPER on a compromised box without having to re-exploit the original Cisco vulnerabilities. It is also worth noting that this whole technique looks a lot like what the RayInitiator bootkit did on Cisco ASA.

## Why Reboots and Patches Do Not Help

Most security teams have a deeply ingrained mental model: patch the CVE, reboot the box, the threat is gone. That model is wrong here for two reasons:

- The persistence file is in a reboot-persistent location: CSP_MOUNT_LIST is a configuration file that the device executes during boot. Modifying it means the malware gets re-run on every boot, no matter how many times you patch. The firmware update does not touch the config partition (where this file lives).

- Soft reboots do not clear running memory the way you think they do: Cisco’s security advisory on this campaign is explicit: a soft reboot does not remove the malware. The injected shellcode and in-memory hooks can survive across reboots on these devices. Only a hard power cycle, with all power sources disconnected for at least one minute, fully clears the state.

If your firewall has redundant power supplies, both must be removed. Otherwise, the device never actually loses power.

## Detecting FIRESTARTER

CISA’s Supplemental Direction for ED 25-03 lays out a specific hunt sequence. Whether you are an FCEB agency or not, the procedure is worth running on any internet-facing ASA or FTD device. CISA also published two YARA rules in AR26-113A. They are also packaged by ThreatHunter.ai into a clean detection bundle. The rules are short, direct, and effective when run against either a core dump or a disk image.

Both rules are designed to work against memory captures. Run them against your core dumps and disk images obtained through Cisco TAC. CISA explicitly recommends getting the disk image through TAC rather than open-source acquisition methods because the actor employs anti-forensic techniques.

If you are hunting beyond YARA, these are the artifacts to look for:

 ArtifactPurpose`/usr/bin/lina_cs`Active FIRESTARTER binary (filename can vary)`/opt/cisco/platform/logs/var/log/svc_samcore.log`Reboot-persistent staging copy of the binary`/opt/cisco/config/platform/rmdb/CSP_MOUNT_LIST`Boot-time mount script with appended persistence commands`/opt/cisco/config/platform/rmdb/CSP_MOUNT_LIST.tmp`Temporary file used during persistence writeModified XML handler in LINA memoryHook target for the WebVPN triggerShellcode block before end of `libstdc++.so` text segmentActive shellcode injection

## Recommendations

For network defenders, here is the concrete action list:

- Inventory every Cisco ASA, Firepower, and Secure Firewall device on your perimeter. Use the device’s first-deployment date and patch history to identify boxes that were online and unpatched between September 25, 2025, and the date you applied the fix.
- Treat any device that was exposed to the internet and unpatched during that window as suspect. Patches addressed the CVEs. They do not remove FIRESTARTER. The persistence is post-patch.
- Run the CISA hunt sequence before you reboot, patch, or reconfigure anything. Capture show checkheaps and show tech-support detail. Generate a core dump and save it off the device.
- Run the CISA YARA rules against the core dump. Both CISA_261290_01 and CISA_261290_02. If either triggers, treat the device as compromised.
- If compromise is confirmed, do not reboot. A soft reboot does not remove FIRESTARTER. Coordinate with CISA (or NCSC for U.K. organizations) before taking the device offline.
- When directed to remove the malware, perform a hard power cycle. Unplug every power source while the device is still running. Leave it disconnected for at least one minute. Reconnect and let it boot. Both redundant power supplies must be unplugged.
- Audit VPN sessions for use of accounts belonging to former employees. The threat actor used valid credentials from inactive accounts to bypass VPN authentication policies. “Disabled” does not mean “removed” in this case.
- Rotate every credential, certificate, and private key stored on a confirmed-compromised device. LINE VIPER, the post-exploitation implant, exposes all configuration elements, including admin credentials, certificates, and private keys.
- Implement TACACS+ over TLS 1.3 for device administration. Not specific to FIRESTARTER, but the recommendation is in CISA’s mitigations because device-admin traffic is a frequent target for credential interception during these campaigns.

## The Bigger Picture

This is what supply chain compromise looks like at the network edge. The actor did not exploit anything novel after September 2025. They did not need new CVEs. They needed a place to hide and found one in the boot-time configuration script of a network appliance that no security team has ever instrumented, because there is no agent running on it.

The Eclypsium platform monitors firmware integrity, boot configuration, and persistent storage on network devices specifically because this category of threat exists. FIRESTARTER is the campaign that is making headlines this month. It will not be the last. The next one will look different and live somewhere else on the same device, and you will need the same kind of visibility to find it.

To learn more about how Eclypsium can help with network device security at the component level, read our white paper: Eradicate Hidden Risks in Network Edge Devices.

## References

- CISA AR26-113A: FIRESTARTER Backdoor Malware Analysis Report
- CISA Emergency Directive 25-03 (V1): Identify and Mitigate Potential Compromise of Cisco Devices
- Supplemental Direction ED 25-03: Core Dump and Hunt Instructions
- Cisco Security Advisory: Continued Evolution of Persistence Mechanism Against Cisco Secure Firewall ASA and Threat Defense
- Cisco Talos: UAT-4356’s Targeting of Cisco Firepower Devices
- ThreatHunter.ai: Pull the Power Cord — FIRESTARTER, AR26-113A, and a Backdoor That Survives Your Patches
- ThreatHunter.ai FIRESTARTER Detection Pack v1 (YARA)
- OpenText Cybersecurity: Analysis Report FIRESTARTER Backdoor
- BleepingComputer: Firestarter malware survives Cisco firewall updates, security patches
- The Hacker News: FIRESTARTER Backdoor Hit Federal Cisco Firepower Device, Survives Security Patches

## Frequently Asked Questions

###

A backdoor on Cisco ASA, Firepower, and FTD firewalls that lets the attacker keep coming back, even after you patch the box.

###

The patches close the door the attacker came in through. They do not remove the attacker if the attacker was already inside. If your firewall was internet-exposed and unpatched between late September 2025 and the day you applied the fix, you should assume the box could have been compromised and run the CISA hunt steps.

###

You will not see it in your SIEM. FIRESTARTER does not generate logs. The reliable way to find it is to capture a core dump and run the CISA YARA rules against it. That is it. Reboot logs, syslog, NetFlow, none of that helps you here.

###

A soft reboot is the trigger. The malware listens for the shutdown signal and uses it to re-stage itself on disk before the box goes down. Every clean reboot re-arms the persistence. The only thing that breaks the cycle is removing power entirely.

###

Pull every power cable. If the device has two power supplies, both come out. Leave it that way for at least a full minute. Then plug it back in. If one cord stays in, the device never actually loses power, and the malware never actually goes away.

###

No. There is no EDR on a Cisco firewall. There is no agent. That is exactly why this category of attack is so attractive to the actor in the first place. The firewall is a trusted black box on your perimeter, and most organizations have zero visibility into what is running inside it.

###

No. CISA found it on a federal box, which is how we got the public report, but the same vulnerabilities and the same backdoor work on any internet-facing Cisco ASA or Firepower device. The UK NCSC put their name on the joint advisory for a reason.

###

You can, and in some cases that is the cleanest answer, especially if you cannot get downtime to do a proper hard power cycle and core dump. Just do not stand up the replacement with the same configuration, the same VPN credentials, and the same admin certificates. The attacker has all of those.

###

Cisco Talos tracks the actor as UAT-4356. Microsoft tracks them as STORM-1849. The campaign is called ArcaneDoor. It is widely assessed to be a state-aligned cyberespionage operation. They have been hitting network edge devices for over two years.

###

If the WebVPN interface does not need to be reachable from the public internet, take it off the public internet. Most of the recent Cisco edge device compromises have come in through WebVPN. If you are not using it, do not expose it.

Tag

ArcaneDoor, ASA, Cisco, Firepower, FIRESTARTER

  Back to Blog
