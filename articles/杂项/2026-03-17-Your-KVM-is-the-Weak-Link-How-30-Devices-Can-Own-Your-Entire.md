---
title: "Your KVM is the Weak Link: How $30 Devices Can Own Your Entire Network"
source: "Eclypsium"
url: https://eclypsium.com/blog/your-kvm-is-the-weak-link-how-30-dollar-devices-can-own-your-entire-network/
published: 2026-03-17
fetched: 2026-11-19T12:19:24.110575+08:00
category: "杂项"
score: 0
keywords: ["kvm", "bmc", "ipmi"]
sha256: 237b45462b9f6b08d544be77f555f1311fe4ebe11b7b81a6be254f2b5159cbf6
bytes: 22230
truncated: false
body_mode: fulltext
kind: practical
status: published
published_at: 2026-11-19T12:20:43.910308+08:00
---

# Your KVM is the Weak Link: How $30 Devices Can Own Your Entire Network

> 来源：Eclypsium · 2026-03-17 · [原文](https://eclypsium.com/blog/your-kvm-is-the-weak-link-how-30-dollar-devices-can-own-your-entire-network/)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：低价的 IP-KVM（约 30 美元级）常被部署在机房/实验室，固件与管理接口缺乏加固，可被用来横向控制整张网络。
- **价值**：IP-KVM 在资产清单里常被当成“运维配件”而非“联网设备”，但它拥有带外键鼠与电源控制权，等于服务器的影子后门。
- **难度**：中 —— 攻击面在 Web 管理面与固件，门槛不高但影响极大。

Blog

# Your KVM is the Weak Link: How $30 Devices Can Own Your Entire Network

By: Paul Asadoorian, Reynaldo Vasquez Garcia

Published: March 17, 2026 |Last Updated: July 1, 2026

[Watch The Webinar](https://info.eclypsium.com/ondemand-vulnerable-kvms-give-attackers-remote-access)

9 vulnerabilities across 4 vendors turn low-cost IP-KVMs into attack platforms

## Compromise the KVM, Compromise Everything

Compromising a KVM device gives an attacker the equivalent of physical access to every machine connected to it. Not “kind of like” physical access. Actual keyboard, video, and mouse control, at the BIOS level, below the operating system, below EDR, below every security control you have deployed. An attacker may also use the USB drive and CD image emulation feature to boot the system from removable media, thereby proving the ability to access the OS file systems directly and/or install a new OS. This is an attack surface that security teams consistently overlook.

Consider what physical access to a system enables: BadUSB attacks that inject keystrokes as if a human were typing, booting from removable media to bypass disk encryption, entering BIOS setup to disable Secure Boot, and bypassing lock screens. Many of these low-cost KVM devices use BadUSB functionality (Linux USB Gadgets) to emulate keyboard and mouse input. An attacker does not need to deploy their own Rubber Ducky to inject keystrokes. The KVM that the user is already connected to does the job.

The timing of this research is not accidental. The FBI recently visited tech YouTuber Jeff Geerling specifically to discuss security concerns around KVM devices. Microsoft’s Cyberattacks Series report documents DPRK remote workers using IP-KVM devices such as PiKVM to plug directly into target machines, enabling remote physical control of employer-provided corporate laptops. The SANS Internet Storm Center has published warnings about the risks of OOB access via IP KVM devices. These are not theoretical concerns. This device class is actively being exploited and scrutinized.

## What Are IP-KVMs and Why Should You Care

A KVM (Keyboard, Video, Mouse) switch lets you control multiple computers with a single set of peripherals. Traditional KVM switches required physical presence, but IP-KVM devices add network connectivity, allowing remote access to the target machine’s keyboard, video output, and mouse input over the network. This includes access at the BIOS level, even when the operating system has crashed or is not installed (provided the required options and hardware are configured for the IP-KVM).

Enterprise environments have relied on KVM-over-IP solutions from vendors like Raritan, Avocent, and ATEN for years. These are rack-mounted, multi-port systems designed for data center management, typically costing hundreds to thousands of dollars. But a new wave of low-cost, single-port IP-KVM devices has flooded the market: the JetKVM, Sipeed NanoKVM, GL-iNet Comet (RM-1), and Angeet/Yeeso devices. These devices cost between $30 and $100 and appeal to homelabbers, small IT shops, MSPs, and, increasingly, enterprises seeking per-machine out-of-band access.

The use cases span every vertical. Enterprise data centers and colocation facilities use IP-KVMs for remote server management. Industrial and OT environments deploy them to manage HMI machines in hazardous zones. Healthcare facilities use them for systems in imaging suites and research labs that cannot be easily rebooted. Government and defense installations rely on them for mission-critical servers where physical access requires escorts and approvals. And Shodan data tells a concerning story: in June 2025, RunZero identified 404 of these devices exposed directly to the Internet. By January 2026, Eclypsium learned that the number had grown to 1,611. The market is flooded with low-cost devices, but these easy-to-obtain solutions come with severe security vulnerabilities.

## Previous Research and Red Flags

We are not the first to raise concerns about this device class. Tom’s Hardware reported on a hidden, undocumented microphone discovered inside the Sipeed NanoKVM. Researchers at grumpygoose.io published a detailed analysis of the TinyPilot KVM, including a companion post on unemployfuscation techniques found in KVM firmware. PT Security documented vulnerabilities in ATEN International switches, a leading enterprise KVM vendor. Jeff Geerling’s blog includes a thorough review of the JetKVM, and @apalrdsadventures on YouTube has published several security-focused reviews of KVM devices. RunZero published a solid blog on OOB P1 IP-KVM exposure and device fingerprinting.

Eclypsium’s research team set out to perform a systematic security assessment across multiple vendors.

## Vulnerability Overview

Eclypsium researchers Reynaldo Vasquez Garcia and Paul Asadoorian discovered 9 vulnerabilities across 4 KVM vendors, spanning 7 distinct vulnerability classes. The common themes are damning: missing firmware signature validation, no brute-force protection, broken access controls, and exposed debug interfaces. These are fundamental security hygiene failures. Broken access control has been at the top of the OWASP Top 10 for years. It is a known, common issue type whose risks continue to be passed along to the buyers of these products.

 VendorProductCVEVulnerabilityCVSS 3.1Patch StatusGL.iNetComet RM-1[CVE-2026-32290](https://nvd.nist.gov/vuln/detail/CVE-2026-32290)GL.iNet Comet KVM insufficient verification of firmware authenticity4.2[Fixed in v1.8.2](https://www.gl-inet.com/en-us/blogs/security-updates/security-advisories-vulnerabilities-and-cves-apr-15-2026)GL.iNetComet RM-1[CVE-2026-32291](https://nvd.nist.gov/vuln/detail/CVE-2026-32291)GL.iNet Comet KVM UART root access7.6[Fixed in v1.8.2](https://www.gl-inet.com/en-us/blogs/security-updates/security-advisories-vulnerabilities-and-cves-apr-15-2026)GL.iNetComet RM-1[CVE-2026-32292](https://nvd.nist.gov/vuln/detail/CVE-2026-32292)GL.iNet Comet KVM insufficient brute-force protection5.3[Fixed in v1.8.2](https://www.gl-inet.com/en-us/blogs/security-updates/security-advisories-vulnerabilities-and-cves-apr-15-2026)GL.iNetComet RM-1[CVE-2026-32293](https://nvd.nist.gov/vuln/detail/CVE-2026-32293)GL.iNet Comet KVM Insecure Initial Provisioning via Unauthenticated Cloud Connection3.1[Fixed in v1.8.2](https://www.gl-inet.com/en-us/blogs/security-updates/security-advisories-vulnerabilities-and-cves-apr-15-2026)Angeet/YeesoES3 KVM[CVE-2026-32297](https://nvd.nist.gov/vuln/detail/CVE-2026-32297)Angeet ES3 KVM unauthenticated file9.8No fix availableAngeet/YeesoES3 KVM[CVE-2026-32298](https://nvd.nist.gov/vuln/detail/CVE-2026-32298)Angeet ES3 KVM OS command injection8.8No fix availableSipeedNanoKVM[CVE-2026-32296](https://nvd.nist.gov/vuln/detail/CVE-2026-32296)Sipeed NanoKVM configuration endpoint exposure5.4Fixed in NanoKVM v2.3.1 and NanoKVM Pro 1.2.4JetKVMJetKVM[CVE-2026-32294](https://nvd.nist.gov/vuln/detail/CVE-2026-32294)JetKVM insufficient update verification6.7Fixed in version 0.5.4JetKVMJetKVM[CVE-2026-32295](https://nvd.nist.gov/vuln/detail/CVE-2026-32295)JetKVM insufficient rate limiting7.3Fixed in version 0.5.4

## Detailed Vulnerability Breakdown

![image](data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%20813%20442'%3E%3C/svg%3E)

Photo Credit: [https://www.gl-inet.com/products/gl-rm1/](https://www.gl-inet.com/products/gl-rm1/)

### GL.iNet RM-1

Update: GL.iNet has informed Eclypsium that the vulnerability issues referenced in this article have been addressed. They have also released relevant fixes and published remediation details in its security advisory. Users are encouraged to review the advisory and update affected devices according to GL.iNet’s guidance.

The GL.iNet Comet RM-1 was the first device we assessed and also the one with the most findings: four distinct vulnerabilities. GL-iNet is primarily known for its travel routers, and the RM-1 represents its entry into the KVM market.

CVE-2026-32290 – GL.iNet Comet KVM insufficient verification of firmware authenticity

The firmware update mechanism relies solely on a self-contained MD5 hash for validation. The final 16 bytes of the firmware file contain an MD5 hash of the preceding content. That is the entire verification mechanism.

Since the hash is embedded in the firmware file itself, an attacker can modify the firmware, recalculate the MD5, and append the new hash. The device will accept the modified firmware as legitimate because the hash correctly matches the modified content. There is no cryptographic signature from GL.iNet, no public key embedded in the device, and no out-of-band verification. An attacker with access to the web interface (or who chains the brute-force vulnerability below) can upload arbitrary firmware.

- Researcher: Reynaldo Vasquez Garcia
- Remediation: [Fixed in v1.8.2](https://www.gl-inet.com/en-us/blogs/security-updates/security-advisories-vulnerabilities-and-cves-apr-15-2026)

CVE-2026-32291 – GL.iNet Comet KVM UART root access

The UART (serial) interface on the RM-1 provides unauthenticated root-level access. Connect to the exposed UART pins on the board, and the system presents boot logs followed by a root shell. No credentials required. No login prompt. Physical access equals root.

While this requires physical access to the device, it completely bypasses all network-facing authentication controls. The UART interface bypasses the web interface login, SSH authentication, and any other access-control path. For devices deployed in shared spaces, colocation facilities, or anywhere with imperfect physical security, this is a direct path to compromise.

- Researcher: Reynaldo Vasquez Garcia
- Remediation: [Fixed in v1.8.2](https://www.gl-inet.com/en-us/blogs/security-updates/security-advisories-vulnerabilities-and-cves-apr-15-2026)

CVE-2026-32292 – GL-iNet Comet KVM insufficient brute-force protection

The web server login endpoint implements no rate limiting. An attacker can submit thousands of password guesses per second with no delays, no failed-attempt tracking, and no account lockout. Making this worse, the same password set for the web interface is also used for SSH access by default. Brute-force the web login, and you get SSH credentials for free.

- Researcher: Reynaldo Vasquez Garcia
- Remediation: [Fixed in v1.8.2](https://www.gl-inet.com/en-us/blogs/security-updates/security-advisories-vulnerabilities-and-cves-apr-15-2026)

CVE-2026-32293 – GL-iNet Comet KVM Insecure Initial Provisioning via Unauthenticated Cloud Connection

During initial boot, the RM-1 contacts a cloud endpoint to retrieve its client and CA certificates. The communication is encrypted, but the device does not verify the certificates it receives. An attacker in a man-in-the-middle position can intercept this connection and serve fraudulent certificates. The device accepts them without validation, causing it to fail authentication with the legitimate MQTT broker. This results in a persistent denial-of-service attack and a complete break in the chain of trust.

- Researcher: Reynaldo Vasquez Garcia
- Remediation: [Fixed in v1.8.2](https://www.gl-inet.com/en-us/blogs/security-updates/security-advisories-vulnerabilities-and-cves-apr-15-2026)

![image](data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%201616%201124'%3E%3C/svg%3E)

Photo credit: [https://a.co/d/05gHkcmv](https://a.co/d/05gHkcmv)

### Angeet/Yeeso ES3 KVM

The Angeet (also sold under the Yeeso brand) ES3 KVM had two vulnerabilities that chain together into a devastating pre-authentication remote code execution path. These were disclosed on December 16, 2025.

CVE-2026-32297 – Angeet ES3 KVM unauthenticated file

This is the highest severity finding in our research. The vendor management binary “Databridge” exposes an /upload endpoint on port 8888 with no authentication or authorization checks. An unauthenticated attacker with network access can write arbitrary files to the device.

By overwriting configuration files or system binaries, an attacker can manipulate the device’s behavior, gain unauthorized access, and use the KVM as a pivot point to compromise any target machine connected to it. This vulnerability alone warrants immediate network isolation of any deployed Angeet ES3 device.

- Researcher: Reynaldo Vasquez Garcia
- Remediation: Angeet/Yeeso has committed to fixing, but has not provided a timeline.

CVE-2026-32298 – Angeet ES3 KVM OS command injection

The `cfg.lua` configuration script does not sanitize user input. On line 36, user-supplied variables are passed directly into an `os.execute()` call:

```
-- cfg.lua line 36 (simplified)
os.execute(user_supplied_value)
```

An attacker who chains the arbitrary file write vulnerability above to overwrite configuration files can inject commands that execute with root privileges. The result is a complete pre-auth-to-post-auth RCE chain. Network access to port 8888 is all that is needed.

- Researcher: Reynaldo Vasquez Garcia
- Remediation: Angeet/Yeeso has committed to fixing, but has not provided a timeline.

![image](data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%20710%20328'%3E%3C/svg%3E)

Photo credit: [https://wiki.sipeed.com/hardware/en/kvm/NanoKVM/introduction.html](https://wiki.sipeed.com/hardware/en/kvm/NanoKVM/introduction.html)

### Sipeed NanoKVM

The NanoKVM, a tiny RISC-V-based KVM device popular in the homelab community, had a broken access control issue with multiple exploitation paths. This was disclosed on December 8, 2025, and is the only finding in our research that has been fully patched.

CVE-2026-32296 – Sipeed NanoKVM configuration endpoint exposure

The WiFi configuration endpoint`/api/network/wifi` fails to enforce authentication. Due to a server-side misconfiguration, this endpoint is exposed without requiring any user authentication or authorization. This single flaw enables three distinct attack scenarios:

- Deauthentication Attack: An attacker can modify the device’s saved Wi-Fi network configuration, forcing the NanoKVM to disconnect from its current network and connect to an attacker-controlled Wi-Fi network. Once on the attacker’s network, all traffic can be intercepted or manipulated.
- Memory Exhaustion DoS: An attacker can craft a request to this endpoint that exhausts the system’s memory, causing the device to terminate the KVM process to free resources. This results in a complete service outage.
- Network Hijacking: By pointing the NanoKVM at an attacker-controlled access point, the attacker gains a man-in-the-middle position on all subsequent traffic, including any updates or management communications.

- Researcher: Reynaldo Vasquez Garcia
- Remediation: Fixed in NanoKVM 2.3.6 and NanoKVM Pro 1.2.14

![image](data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%202500%202500'%3E%3C/svg%3E)

Photo credit: [https://jetkvm.com/products/jetkvm](https://jetkvm.com/products/jetkvm)

### JetKVM

JetKVM is arguably the most popular device in the low-cost IP-KVM space, having raised over $5 million on Kickstarter. It is open source, actively developed, and widely deployed. We found two vulnerabilities that were disclosed on January 13, 2025.

CVE-2026-32294 – JetKVM insufficient update verification

The JetKVM OTA update mechanism relies solely on SHA-256 hash verification. While SHA-256 is a stronger hash than GL-iNet’s MD5, the fundamental problem remains the same: there are no cryptographic signatures (Ed25519, RSA, or ECDSA) to verify the authenticity of updates. The hash and the update binary are retrieved from the same server, so if an attacker compromises the update server or performs a man-in-the-middle attack, they control both the firmware and the hash.

The update process works as follows:

- Device sends a GET request to https://api.jetkvm.com/releases?deviceId=xxx
- Server responds with JSON containing download URLs and SHA-256 hashes:

```
{
  "appHash": "a1b2c3...",
  "appUrl": "https://cdn/.../jetkvm_app",
  "systemHash": "d4e5f6...",
  "systemUrl": "https://cdn/.../system.tar"
}
```

- Device downloads the binary to `/userdata/jetkvm/jetkvm_app.update.unverified`
- The device computes the SHA-256 hash and compares it to the server-provided hash
- If hashes match, the .unverified suffix is removed
- On reboot, the `RkLunch.sh` script moves`jetkvm_app.update` to `bin/jetkvm_app`

The critical gap: `RkLunch.sh`performs no verification before replacing the running application’s binary. Any file named `jetkvm_app.update` is blindly accepted and executed on the next boot. If an attacker can write to `/userdata/jetkvm/`, the game is over.

- Researcher: Paul Asadoorian
- Remediation: JetKVM has published a fix in version 0.5.4.

Note: The Eclypsium team would like to recognize the JetKVM team for their efforts in implementing this feature and hopes that other companies follow suit by implementing firmware signature validation, as it is an important security measure.

CVE-2026-32295 – JetKVM insufficient rate limiting

The JetKVM authentication system provides zero protection against brute-force attacks. The login endpoint accepts unlimited authentication attempts with no delays, no tracking of failed attempts, and no account lockout. The authentication model compounds the problem:

- There is no username, only a single password
- There are no password complexity requirements
- Users can set weak or even empty passwords
- The only protection is the computational cost of bcrypt verification

An attacker can submit thousands of password guesses per second, limited only by network latency and bcrypt hashing time. For any user who sets a weak password (and with no complexity requirements, many will), compromise is straightforward.

- Researcher: Paul Asadoorian
- Remediation: JetKVM has published a fix in version 0.5.4.

## Common Weakness Patterns

Step back and look at these findings across all four devices, and the patterns are striking. Three out of four devices lack firmware signature verification entirely. Two devices have no brute-force protection on their login endpoints. Multiple devices ship with authentication disabled by default, requiring the user to enable it after deployment. TLS certificate validation is absent or broken (in some cases, JetKVM implements TLS correctly). Debug interfaces provide unauthenticated root access.

These are not exotic zero-days requiring months of reverse engineering. These are fundamental security controls that any networked device should implement. Input validation. Authentication. Cryptographic verification. Rate limiting. We are looking at the same class of failures that plagued early IoT devices a decade ago, but now on a device class that provides the equivalent of physical access to everything it connects to.

The vendor responses ranged from responsive (JetKVM and Sipeed issued patches for all vulnerabilities) to concerning (GL-iNet has “no planned fix” for firmware signing and UART authentication, and Angeet/Yeeso has not committed to fixing the reported vulnerabilities). Some of these devices may never be adequately secured, which means the security burden falls entirely on the operators deploying them.

## Why Vulnerable KVMs Matter

A compromised KVM is not like a compromised IoT device sitting on your network. It is a direct, silent channel to every machine it controls. An attacker on a KVM device can:

- Inject keystrokes as if physically typing, deploying malware, or exfiltrating data through the target machine’s own keyboard input
- Boot from removable media to bypass disk encryption, Secure Boot, and any OS-level security control
- Access BIOS/UEFI settings to disable security features, modify boot order, or install persistent implants
- Bypass lock screens and access systems as if standing in front of them
- Remain invisible to host-based security tools: EDR, AV, and host firewalls never see the KVM because it operates below the OS.

The stealth-and-persistence angle is particularly concerning. KVM devices run their own Linux stack. An attacker who compromises the KVM can hide tools and backdoors on the device itself, consistently re-infecting host systems even after remediation. Since some firmware updates lack signature verification on most of these devices, a supply-chain attacker could tamper with the firmware at distribution time and have it persist indefinitely.

## Mitigation Guidance

If you have KVM devices deployed, or are planning a deployment, take the following steps immediately:

- Enable strong authentication: Use strong, unique passwords. Enable MFA where supported. Do not leave authentication disabled after initial setup.
- Network isolation: Place KVM devices on a dedicated management VLAN. Never expose them directly to the Internet. Use Tailscale, WireGuard, or another VPN for remote access.
- Device inventory: Scan your environment for KVM devices you may not be aware of. Use Shodan queries like title:JetKVM, title:NanoKVM, or title:GLKVM to check for external exposure.
- Apply firmware updates: Ensure devices are running the latest firmware. For NanoKVM, update to v2.3.1 or later. For GL-iNet RM-1, update to v1.7.2 or later.
- Use secure protocols: Enable TLS for web management interfaces. Ensure SSH is enabled and properly configured.
- Monitor for anomalies: Watch for unexpected network traffic to/from KVM devices, particularly outbound connections to unknown endpoints.
- Eclypsium platform: Eclypsium customers can upload firmware and binaries from KVM devices for scanning to detect known vulnerabilities.

Audit your KVM deployments. Know what you have, where it is, and what firmware it is running. These devices are the keys to your kingdom, and right now, too many of them are hanging on the network with the door wide open.

If you would like to get more information on this topic, be sure to register for our webinar on April 16th: Vulnerable KVMs Give Attackers Remote Access: New Threat Research

Tag

Firmware, IoT Security, KVM, supply chain, Vulnerability

  Back to Blog
