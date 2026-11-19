---
title: "Fake Kernel Threads Are Hiding Backdoors on Linux Servers and Appliances"
source: "Eclypsium"
url: https://eclypsium.com/blog/linux-malware-fake-kernel-threads/
published: 2026-10-20
fetched: 2026-11-19T12:19:24.110575+08:00
category: "杂项"
score: 0
keywords: ["linux", "backdoor", "appliance"]
sha256: 922959deedf1970e848e7f3191aa54cfe09d3a92508c27d48a985c8e781b9a76
bytes: 15053
truncated: false
body_mode: fulltext
status: published
published_at: 2026-11-19T12:20:43.910308+08:00
---

# Fake Kernel Threads Are Hiding Backdoors on Linux Servers and Appliances

> 来源：Eclypsium · 2026-10-20 · [原文](https://eclypsium.com/blog/linux-malware-fake-kernel-threads/)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：发现恶意软件伪装成内核线程（fake kthread）潜伏在 Linux 服务器与网络设备中，用常规 ps/top 难以分辨。
- **价值**：网络设备与 IoT 网关大多是 Linux；这类“看起来像内核线程”的后门是设备取证的盲区，对应急响应很实用。
- **难度**：中高 —— 需要内核层取证与线程行为基线。

Blog

# Fake Kernel Threads Are Hiding Backdoors on Linux Servers and Appliances

By: Paul Asadoorian

Published: October 20, 2026

Attackers keep disguising malware as Linux kernel worker processes, but careful checks will expose the disguise

On September 5, 2026, Sansec, a security firm that investigates attacks on online stores, reported that attackers were exploiting a zero-day in Magento and Adobe Commerce to install a backdoor written in Rust. The vulnerability is tracked as CVE-2026-75650 and is rated Critical, with a CVSS score of 10.0. Early versions of the backdoor ran under the name [kworker/u:8:0], which is meant to look like one of the Linux kernel’s own worker threads.

Two days later, researchers reported Tengu, a bot modeled on the Mirai botnet malware, which overwrites its process name with a random kworker/%d:%d value. In July, an incident responder found a Go command-and-control (C2) agent running as [kworker/7:2] on a breached OpenCart store, next to a script that dumped the store’s customer order table.

The disguise works because a Linux system runs dozens of real kernel threads with numbered names, and an administrator reading a process list has no reason to notice if there’s an extra. The disguise only goes as deep as the name, because a program running in user space cannot reproduce the properties of a real kernel thread without a kernel rootkit, so defenders can check for those properties instead of chasing each new malware name or hash.

Who should act: detection engineering should add the checks below to Linux servers and to any appliance that exposes a process list, and report back which systems the check cannot run on. Incident response teams should take over if this yields any hits. Network and appliance administrators should find out which of their devices give them a full process listing at all. A device without a process list makes an implant like this harder to find.

## Why a fake kernel thread blends in

The Linux kernel does a lot of background work in threads that live entirely inside kernel memory. The `kworker` threads process queued work for drivers and subsystems, and others such as `ksoftirqd`, `kswapd`, `migration`, and the `rcu_` family handle deferred interrupt work, memory reclaim, moving tasks between processors, and synchronization. Because these threads have no command line, ps displays their names in square brackets, for example `[kworker/0:1]`.

Malware can emulate that appearance in two ways. It can overwrite its own argv[0], which changes what `ps aux` and `/proc/PID/cmdline` show, or it can call `prctl(PR_SET_NAME)`, which changes the short process name stored in `/proc/PID/comm`. Some families do both. MITRE ATT&CK, the public catalog of attacker techniques maintained by MITRE, tracks this under Masquerading as T1036.004, Masquerade Task or Service.

None of this is new, but the continued recurrence of this established technique makes it worth another look. Especially given the rising number of exploitation attempts targeting Linux-based infrastructure devices. The United Kingdom’s National Cyber Security Centre (NCSC) documented in its February 2022 analysis of Cyclops Blink, a malware family attributed to the Sandworm group, that the implant “renames its running process to masquerade as a Linux kernel thread.” In June 2024, Trend Micro reported that the Linux version of the Noodle remote access trojan (RAT) spoofs its process name by overwriting `argv`, using code that matches the older Rekoobe backdoor.

## Where this masquerading technique has showed up in 2026

 Malware or campaignWhat it hitName it usedReported byStyleSmuggler backdoorMagento and Adobe Commerce stores, through [CVE-2026-75650](https://nvd.nist.gov/vuln/detail/CVE-2026-75650)`[kworker/u:8:0]`in early samples; `fc-cache` and `chronyd` in later ones[Sansec](https://sansec.io/research/stylesmuggler-0day), September 5, 2026Tengu botLinux servers, routers, and embedded devicesA random `kworker/%d:%d`valueReverser.Space, as reported by [GBHackers](https://gbhackers.com/tengu-mirai-style-linux-bot/), September 7, 2026Go C2 agent (`watchdogd`)An OpenCart online store`[kworker/7:2]`[K.K. Bourdakos](https://kbourdakos.gr/articles/ghost-process-go-c2-agent-opencart-breach.html), July 3, 2026Linux Noodle RATLinux servers, typically after a web shellSpoofed process names (specific names not published)[GBHackers](https://gbhackers.com/noodle-rat-backdoor/amp/), September 16, 2026, citing Trend Micro

According to Cyberpress’s summary of the Sansec findings, StyleSmuggler malware samples observed on September 6 had already switched from the `kworker` name to `fc-cache`, one day after Sansec’s report. A detection that keys on the name `[kworker/u:8:0]` stopped matching new infections within a day. The second detail is that kworker/u:8:0 is not a name the kernel would ever produce. Kernel workers that are not tied to a single processor are named kworker/u followed by a pool number, a colon, and a worker number, as in kworker/u8:2. The attacker’s version has no number after the u and an extra colon, so a simple check on the name format flags it.

Cyclops Blink also came back this year. On September 9, 2026, Cisco Talos, Cisco’s threat intelligence group, reported that a cluster it tracks as UAT-11823, which overlaps in tooling with Sandworm, deployed a Cyclops Blink variant on Cisco Secure Firewall Management Center (FMC), the appliance that manages fleets of Cisco firewalls. The actors gained access via CVE-2026-20079, a Critical authentication bypass (CVSS 10.0) that grants root access to the appliance’s underlying operating system. Talos does not say whether this variant still renames itself as a kernel thread. The 2022 version did, so if you run FMC, the checks below are relevant to you, with the caveat that this is an inference based on the malware’s history, not something Talos reported.

## What an impostor kernel thread can’t fake

A real kernel thread has properties that a user-space program can’t reproduce without loading code into the kernel. Every malware sample in the table above runs in user space, so each of these properties gives you a way to catch it regardless of what it calls itself.

 PropertyReal kernel threadUser-space impostorParent process`kthreadd`, process identifier (PID) 2Anything else, often PID 1 or a shell`/proc/PID/exe`Does not resolveResolves to the binary on disk, or shows (`deleted`) if the file was removedMemory (`VSZ` and `RSS` columns in `ps`)Both 0Non-zero`/proc/PID/cmdline`EmptyUsually populatedKernel-thread flag (`PF_KTHREAD`)SetClearNetwork socketsNever owns oneOften owns oneOwnerrootWhichever account launched it

Two name checks also work on a plain-text process listing where none of the metadata is available. The first is the name format problem described above. The second is that a real `/proc/PID/comm` value never contains a literal `[` character. The brackets come from `ps` when it displays a process with an empty command line, so a process whose own name includes a bracket put it there itself.

The OpenCart case shows how these properties look in practice. Bourdakos noticed that `[kworker/7:2]` was running as the hosting account rather than `root`, reported about 724 megabytes of virtual memory and 12 megabytes resident when a real kernel thread reports zero, showed a process state of `Sl` (consistent with a multi-threaded Go program) instead of the I state of an idle kernel worker, and had started at 04:07, the same time the attacker dropped the web shell. Searching the process list for the real binary name, `watchdogd`, returned nothing.

![image](data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%20807%20581'%3E%3C/svg%3E)

An example of the masquerading technique discussed in this post, as detected by Eclypsium: the platform flagged the ENDLESSDOORS backdoor, an implant that hides as a kworker process, because the process posing as a kworker was not a real kernel thread.

## Hunting for fake kernel threads on Linux systems

Detection engineering can run these checks today on any Linux host where they have a root shell. The first is a quick visual pass:

```
ps -eo pid,ppid,user,stat,vsz,rss,comm,args | grep -E '\[(kworker|ksoftirqd|kswapd|migration|rcu_)'
```

Real kernel threads show a parent of `2`, a user of `root`, and zeros in the `VSZ` and `RSS` columns. Anything else in this output deserves a closer look. Compare the `comm` and `args` columns as well. A process that only overwrote argv[0] still shows its real name in `comm` while `args` shows the disguise, and that mismatch alone is enough to flag it.

The second check is a script that tests the strongest single property, whether the process has an executable file behind it:

```
#!/bin/bash
# Run as root. Flags processes that present a kernel-thread name
# but are backed by an executable file.
pattern='^\[?(kworker|ksoftirqd|kswapd|migration|rcu_)'
for d in /proc/[0-9]*; do
  pid=${d#/proc/}
  comm=$(cat "$d/comm" 2>/dev/null)
  args=$(tr '\0' ' ' < "$d/cmdline" 2>/dev/null)
  if [[ $comm =~ $pattern || $args =~ $pattern ]]; then
    exe=$(readlink "$d/exe" 2>/dev/null)
    if [[ -n $exe ]]; then
      ppid=$(awk '/^PPid:/{print $2}' "$d/status")
      echo "SUSPECT pid=$pid ppid=$ppid comm='$comm' args='$args' exe=$exe"
    fi
  fi
done
```

The script checks both `comm` and the command line, so it catches either renaming method. Run it as `root`. Without root, `readlink` fails on other users’ processes and the script silently misses them. A `SUSPECT` line means a process is claiming a kernel-thread name while running from a file on disk, which a real kernel thread never does. Hand that PID to incident response before anyone kills it.

A few cautions if you extend this logic into a production rule:

- Keep the name list to names only the kernel uses. Ordinary daemons such as `chronyd` and `fc-cache` rename themselves for legitimate reasons, so StyleSmuggler’s later names will not fit this check and need hash or behavior-based detection instead.
- If you add a parent-process test, exclude PID 2 itself. `kthreadd`‘s own parent is PID 0, so a naive “parent must be 2” rule fires on every healthy host.
- Do not test whether `/proc/PID/cmdline` or /proc/PID/maps is empty by checking the file size. The proc filesystem reports a size of 0 for both files whether they hold data or not. Read the contents instead.
- Keep in mind that an attacker who has deployed a kernel-level rootkit can do a much better job at hiding processes and will evade these detections.

## Network appliances are where this check gets hard

Firewalls, firewall managers, remote-access gateways, and similar appliances often run Linux underneath, but most do not give the administrator a root shell or a full process listing. Also, in most cases, you cannot install an EDR agent on them. The Cyclops Blink deployment on FMC is a Linux implant, delivered as an Executable and Linkable Format (ELF) binary according to Talos, on exactly this kind of device.

Network and appliance administrators should ask each vendor whether there is a supported way to pull a process listing that includes the PID, parent PID, memory use, and executable path. The useful result is a list of which appliances support it and which do not. On devices that do, detection engineering can apply the same checks. On devices that do not, you will not see this technique through process data and need other evidence, such as file integrity and outbound connections, to find it.

## What to do if you find one

Incident response should own any confirmed hit. Before killing the process, preserve what is only available while it runs:

```
mkdir -p /root/ir
cp /proc/PID/exe /root/ir/PID.bin            # works even if the file was deleted
ls -l /proc/PID/cwd                          # working directory
tr '\0' '\n' < /proc/PID/environ             # environment variables
ss -tunap | grep "pid=PID,"                  # network connections
```

Then look for the persistence these families used. StyleSmuggler relied on a cron job that restarts the implant twice an hour. The OpenCart attacker added an `@reboot` cron entry and a second cron job that restarted the binary every 5 minutes. Tengu installs a systemd service described as “System Helper Service,” along with SysV init scripts, OpenWrt `procd` entries, cron `@reboot`jobs, and `/etc/rc.local`. Talos lists /etc/init.d/ scripts as a Cyclops Blink persistence capability. Removing the process without removing the persistence brings it back.

Close the entry point too. For StyleSmuggler, that means Adobe’s hotfix in Adobe security bulletin APSB26-146. Patching stops new infections through that vulnerability and does not remove an implant that is already installed, so do both. In the e-commerce cases, also assume customer data on the host was exposed until you can show otherwise. The OpenCart attacker deployed an endpoint that exported the entire order table, including customer names, addresses, and payment details.

## Frequently Asked Questions

###

No. A typical Linux host runs dozens of real kernel threads. They become suspicious when they have a parent other than PID 2, non-zero memory, or an executable file behind them.

###

It can, if the agent runs on the host and the vendor ships a rule for it, as Elastic does. EDR agents generally cannot run on closed network appliances, which is where the visibility gap is largest.

###

A kernel rootkit can alter what the `proc` filesystem reports. The examples in this post all run in user space, which is why the property checks work against them.

###

No. Patching stops new infections through that vulnerability. An implant that is already installed keeps running and keeps its persistence until someone removes it.

###

Every Linux system runs many `kworker` threads with numbered names that change between boots, so one more entry does not stand out in a long process list.

## Sources

- Sansec: StyleSmuggler, Magento and Adobe Commerce zero-day remote code execution flaw (CVE-2026-75650) under active attack
- Tenable: StyleSmuggler (CVE-2026-75650) frequently asked questions
- Cyberpress: Hackers exploit StyleSmuggler Magento and Adobe Commerce zero-day
- Adobe security bulletin APSB26-146
- National Vulnerability Database: CVE-2026-75650
- GBHackers: Tengu Mirai-style Linux bot hides as kernel worker
- K.K. Bourdakos: A Go C2 agent disguised as a Linux kernel thread
- Trend Micro: Noodle RAT, reviewing the new backdoor used by Chinese-speaking groups
- GBHackers: Noodle RAT backdoor
- Cisco Talos: Ongoing exploitation of Cisco Secure Firewall Management Center
- National Vulnerability Database: CVE-2026-20079
- NCSC: Cyclops Blink malware analysis report
- MITRE ATT&CK: T1036.004, Masquerade Task or Service
- Elastic detection rule: Executable Masquerading as Kernel Process

Tag

Detection Engineering, Linux, Malware, Network Devices, Threat Hunting

  Back to Blog
