---
title: "Inside KeyDrift: Analyzing historical UAT-11473 activity on Cisco SD-WAN"
source: "Talos Intelligence"
url: https://blog.talosintelligence.com/uat-11473-keydrift/
published: 2026-10-29
fetched: 2026-11-16T22:15:04.746781+08:00
category: "防火墙"
score: 4.8
keywords: ["bypass", "in the wild", "sd-wan", "cisco"]
sha256: 0536c8308a0ee683823234257953c88b21e09378996e2448648b221bea285cb2
bytes: 14756
truncated: false
body_mode: fulltext
kind: practical
status: published
published_at: 2026-11-16T22:16:27.064129+08:00
---

# Inside KeyDrift: Analyzing historical UAT-11473 activity on Cisco SD-WAN

> 来源：Talos Intelligence · 2026-10-29 · [原文](https://blog.talosintelligence.com/uat-11473-keydrift/)
> 自动抓取快照，仅供安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：Talos 复盘 UAT-11473 针对 Cisco SD-WAN Catalyst Controller 的长期活动，利用 CVE-2026-20127 认证绕过拿到控制器权限并部署 KeyDrift 后门。
- **价值**：SD-WAN 控制器是“网络的中枢”，拿下它等于接管整张企业网；文中给出攻击者历史 TTP 与后门分析，属于高价值边缘设备威胁情报。
- **难度**：中高。认证绕过本身门槛不高，但要在控制器上维持长期隐蔽访问、并规避企业侧检测。

# Inside KeyDrift: Analyzing historical UAT-11473 activity on Cisco SD-WAN

By  Cisco Talos

  Wednesday, October 28, 2026 17:32

Threat Advisory   APT   malware

- Cisco Talos has identified UAT-11473, a highly sophisticated advanced persistent threat (APT) actor, who exploited CVE-2026-20127, an authentication bypass vulnerability in Cisco SD-WAN Catalyst Controller instances to bypass authentication and gain unauthorized access to affected systems.
- UAT-11473 then installed a custom malware framework we track as “KeyDrift” consisting of multiple components geared towards collecting sensitive keying information, acting as backdoors and intermediate command-and-control (C2) hosts.
- Observed targeting spans across space and satellite services, defense and aerospace technology, and policy research.

Talos assesses with high confidence that UAT-11473’s operating infrastructure overlaps considerably with Volt Typhoon’s “Silent Train” covert access network.

KeyDrift is a custom malware framework that is designed to operate in Cisco SD-WAN controller environments. Talos assesses with high confidence that the framework is designed to provide long-term persistent access and automated exfiltration of sensitive keying material. KeyDrift operates inside SD-WAN control-plane processes and is capable of intercepting decrypted control traffic, extracting control-session metadata and data-plane keying material, and staging or transmitting the collected material using encrypted records.

The framework's primary component is PolyFlame, a memory-resident module deployed through modified runit service paths. PolyFlame is injected into legitimate running vdaemon processes, and it can also masquerade as a packed “aaamgrd” loader variant. Once resident, PolyFlame interposes socket, DTLS, and runtime-linker behavior through functions such as recvfrom, sendto, getpeername, dlopen, dlsym, mprotect, and “/proc/%d/maps” parsing. This gives KeyDrift access to SD-WAN control-plane traffic from inside legitimate controller daemon execution rather than through a conventional endpoint beacon.

LittleFilch, another component of the KeyDrift framework, provides the collection and exfiltration capability identified in the framework. The module hooks “SSL_read” inside vdaemon, inspects decrypted control-plane buffers, extracts keying material for a list of predefined edge nodes, and stages the data locally in encrypted format for exfiltration.

Talos assesses with high confidence that KeyDrift's intended operational purpose is Cisco SD-WAN control-plane collection: persistent controller residence, in-band traffic access, key-material extraction from decrypted control messages, and encrypted staging or exfiltration of the recovered material. Observed variations of the KeyDrift modules and deployment mechanisms suggest active development of the framework’s capabilities.

## KeyDrift analysis

KeyDrift uses Cisco SD-WAN runit service paths as its primary execution anchor. In the PolyFlame sshd deployment, the actor modifies the service run script, remounts /rootfs.rw executable, launches a malicious script “conf_sshd” in the background, and then starts the legitimate sshd service. The loader script enumerates running vdaemon PIDs, records them in “/tmp/system-vdaemon”, and invokes the injector component “rsshd” to inject PolyFlame (“libdssl.so”) into each process.

Recovered conf_sshd logic uses the same control flow across reviewed samples:

![image](https://storage.ghost.io/c/af/a0/afa04ee3-414f-4481-8d23-7e7c146f192e/content/images/2026/10/data-src-image-f3958e3d-b846-45c7-8526-550bb5a4c34d.png)

Figure 1. conf_sshd control flow logic.

### Runit launchers

The observed sshd runit launcher preserves normal Cisco SD-WAN sshd startup logic while adding two malicious lines before service execution, which remount “/rootfs.rw” executable and background execution of conf_sshd, which then drives rsshd injection into vdaemon.

![image](https://storage.ghost.io/c/af/a0/afa04ee3-414f-4481-8d23-7e7c146f192e/content/images/2026/10/data-src-image-52ca1586-b9e0-4a7c-8767-e8f362f8371a.png)

Figure 2. conf_sshd execution logic.

The recovered aaamgr runit launcher from an affected vBond appliance uses a parallel service-wrapper pattern, but it executes the packed aaamgrd PolyFlame loader directly. The deletion of the writable-overlay PAM configurations for sshd and login before remounting “/rootfs.rw” executable if part of the legitimate script, along with the invocation of the aaamgrd daemon via Python:

![image](https://storage.ghost.io/c/af/a0/afa04ee3-414f-4481-8d23-7e7c146f192e/content/images/2026/10/data-src-image-7c670c4f-818e-478d-aa59-705b8c657f16.png)

Figure 3. aamgrd daemon launch.

### PolyFlame

PolyFlame is the primary operational module in the KeyDrift framework. PolyFlame operates at the socket and DTLS control-plane layer. PolyFlame serves two primary purposes:

- Command execution via a TinyShell-styled backdoor
- Intermediate C2 that can forward commands to and from the C2 to other peers

PolyFlame is primarily injected into the vdaemon process, providing operational obfuscation and access to all in-process state: DTLS session keys, vEdge topology, OMP routes, and policy tables. No hardcoded IPv4 addresses, binding ports, callback domains, URLs, host headers, or polling interval were recovered from the analyzed PolyFlame samples. PolyFlame is designed for in-band control or tasking over Cisco SD-WAN control-plane traffic rather than a conventional fixed external beacon.

This implant is meant to serve as a hook of the recvfrom() API call. The original recvfrom is replaced by a malicious subroutine in the vdaemon process. When recvfrom is called in the vdaemon process, the malicious subroutine will first execute the real/legitimate recvfrom() API to obtain the C2 IP address info for communicating with it in the future.

PolyFlame’s time check

The recvd data from the C2 consists of the MD5 value of a specific DATE. PolyFlame will calculate the local time on the device in format “%Y-%m-%d" and calculate its MD5 hash. If the MD5 calculated by the device does not match with the one sent by the C2, the implant will stop further execution. Otherwise, the implant then uses an “administrative code” from the C2 and performs an action.

PolyFlame’s tasking

PolyFlame contains an administrative mode that processes the admin code sent by the C2, that defines operations — it's one of the first flags checked in the backdoor:

- Code = 1: Generate random bytes and send to C2. This is likely a check-in beacon or heartbeat for the C2.
- Code = 2: Set implant type to backdoor (TinyShell) or intermediate C2.
- Code = 3: Set up the command handler for the intermediate C2.
- Any other code value: Check the implant type flag currently set. Based on the implant type flag, either send the accompanying data to TinyShell or the intermediate C2 component for processing.

PolyFlame’s command execution

PolyFlame contains a backdoor that matches the capabilities of TinyShell: file read, file write, and arbitrary command execution, but not interactive shell. This backdoor component’s implementation is quite similar to TinyShell, but the command codes differ. PolyFlame handles the following command codes:

- Code = 0x100: Execute command using “/bin/sh -c <command>”
- Code = 0x200: Write file to disk.
- Code = 0x300: Read file from disk and send to the C2.

PolyFlame as an intermediate C2 component

The intermediate C2 component is a one-to-many handler (somewhat like a one-to-many multiplexer) — meaning the implant can connect to only one C2 but can connect to many peers who can be served by the intermediate C2 component. Similar to the TinyShell-backdoor component, the intermediate C2 component also accepts and processes specific command codes from the C2:

- Code = 0x403: Create a thread to connect to the specified peer IP. Make a new connection and keep socket alive until specified.
- Code = 0x404: Send data recvd from the C2 to a connected peer.
- Code = 0x405: Remove a peer from the list of active connections.
- Code = 0x407: Send a response recvd from a peer, back to the C2.
- Code = 0x408: Set a specific value in memory.

PolyFlame variant: aaamgrd

Talos has observed a distinct PolyFlame variant that masquerades as the aaamgr service. The legitimate Cisco aaamgr component is a Python package; it does not normally appear as a compiled ELF runit service. This PolyFlame variant is executed by a malicious runit service under “/etc/sv/aaamgr/” with aaamgrd and a modified run launcher.

aaamgrd is a statically linked ELF64 executable with no section headers, a single RWE loader segment, and an RC4-encrypted embedded ELF payload. The loader uses direct syscalls including ptrace, fork, wait4, kill, tgkill, mmap, and mprotect. It performs an anti-debug check by deobfuscating /proc/%d/status and TracerPid: and exits if a tracer is present.

The observed staging sequence was:

![image](https://storage.ghost.io/c/af/a0/afa04ee3-414f-4481-8d23-7e7c146f192e/content/images/2026/10/data-src-image-193cbc38-3101-41e5-9403-3f9f37045501.png)

Figure 4. PolyFlame staging sequence.

Note that in addition to the implant execution staging, there are also indications of timestomping.

### LittleFilch: libcommon.so TLS interception module

LittleFilch is a control-session interception module positioned to collect data-plane keying material from control sessions visible to the injected vSmart process.

LittleFilch installs an SSL_read hook inside vdaemon. The hook calls the original SSL_read, then processes returned buffers only when the returned size is greater than 0x18F, the first decrypted byte is 0x07, and three marker patterns are checked for presence. These marker bytes are followed by the actual artifacts that LittleFilch aims to record:

 kg-card-begin: html
   Marker bytes   Parsed field   Length   Notes     40 03 06   Public IP   4 bytes   vEdge public / transport IP     40 0C 04   Peer system-IP   4 bytes   vEdge OMP system-IP     05 01 0C 06 40   Binary key field   32 (0x20) bytes   Assessed OMP-distributed AES-256 IPsec data-plane key material
 kg-card-end: html

LittleFilch records the extracted keying material and RSA-encrypts it before writing the output to “/var/tmp/vdaemon.bin”. It can then send the encrypted content over UDP in a DTLS 1.2 application-data style record.

![image](https://storage.ghost.io/c/af/a0/afa04ee3-414f-4481-8d23-7e7c146f192e/content/images/2026/10/data-src-image-69528025-48de-45df-b696-7ca8ef881e0f.png)

Figure 5. Keying material recording format used by LittleFilch.

LittleFilch expects its configuration file — located at “/var/tmp/vdaemon.conf” — to contain two host port lines: one local bind IP/port and one remote destination IP/port. It deletes “/var/tmp/vdaemon.conf” after reading it. Talos has not been able to recover the “vdaemon.conf” file.

## KeyDrift components

 kg-card-begin: html
   Component   Primary hook/surface   Observed scope   Confirmed function     PolyFlame libdssl.so   Socket / DTLS / runtime linker interposition inside vdaemon   Multiple affected controller roles   In-band control-plane interception and tasking; exact command format unresolved     rsshd   Ptrace injection   Multiple affected controller roles   Injects libdssl.so into vdaemon by PID     conf_sshd   Shell-based PID enumeration   Multiple affected controller roles   Locates vdaemon PIDs and records injection output     Trojanized run   Runit service launcher   Multiple affected controller roles   Remounts overlay executable and launches injector chain     Packed aaamgrd   Packed loader, direct syscalls, anti-debug   Affected vBond appliance evidence   Decrypts and runs embedded PolyFlame payload; tampers with PAM configs     LittleFilch libcommon.so   OpenSSL SSL_read hook   Affected vSmart process evidence   Extracts control-session identifiers and assessed data-plane key material from decrypted control traffic     vdaemon.bin   Encrypted staging file   Affected vSmart process evidence   Stores RSA-encrypted LittleFilch telemetry records     vdaemon.conf   Runtime endpoint config   Affected vSmart process evidence   Supplies local and remote UDP endpoint configuration; deleted after read
 kg-card-end: html

## MITRE ATT&CK techniques

 kg-card-begin: html
   Technique   ID   Notes     Process Injection: Ptrace System Calls   T1055.008   rsshd injects libdssl.so into vdaemon by PID     Hijack Execution Flow: Dynamic Linker Hijacking   T1574.006   PolyFlame uses dlsym(RTLD_NEXT, ...), dlopen, and runtime interposition     Boot or Logon Initialization Scripts   T1037   Modified runit service scripts launch KeyDrift components     Create or Modify System Process   T1543   Malicious service paths under etc/sv/sshd/ and etc/sv/aaamgr/     Masquerade Task or Service   T1036.004   sshd and aaamgr service-name masquerading     Unix Shell   T1059.004   conf_sshd and recovered operator staging commands     Software Packing   T1027.002   aaamgrd uses packed embedded ELF payload     System Checks   T1497.001   aaamgrd checks TracerPid before unpacking     Timestomp   T1070.006   touch --reference= and chmod --reference= staging commands copied reference file metadata     Network Sniffing   T1040   PolyFlame and LittleFilch intercept SD-WAN control-plane traffic     Encrypted Channel: Symmetric Cryptography   T1573.001   PolyFlame AES implementation; aaamgrd RC4 packer; LittleFilch RSA-encrypted records
 kg-card-end: html

## Recommendations

Cisco has released patches for CVE-2026-20127 and published a hardening guide for Cisco Catalyst SD-WAN deployments available here. Organizations are strongly advised to prioritize the application of these patches and follow the guidance provided.

Following the identification of UAT-11473 activity, Talos strongly recommends that organizations monitor their systems for indicators of post-compromise activity. Should any signs of unauthorized activity be detected, organizations should immediately activate their incident response frameworks. Contact the Cisco Technical Assistance Center (TAC) for support by initiating a TAC request.

## Coverage

Snort SIDs are already available for CVE-2026-20127: 65938, 65958.

Snort SIDs for the malicious artifacts illustrated in this blog:

- Snort v2: 67387 through 67416
- Snort v3: 7:44 through 7:73

### Integrated Coverage

##### Network Security

   Cisco Talos
 Network Intrusion Prevention

##### Web Security

   Cisco Talos
 Web Filtering

Read more about Cisco Talos Intelligence Integrations in our data sheet on Cisco.com.

##### Share this post

-
-
-
-
-
