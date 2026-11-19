---
title: "Marking Your Own Homework (Check Point Remote Access VPN IKEv1 Authentication Bypass CVE-2026-50751)"
source: "watchTowr Labs"
url: https://labs.watchtowr.com/marking-your-own-homework-check-point-remote-access-vpn-ikev1-authentication-bypass-cve-2026-50751/
published: 2026-06-12
fetched: 2026-11-19T10:48:37.911925+08:00
category: "防火墙"
score: 6.4
keywords: ["bypass", "check point"]
sha256: 5adb23856935b245b44e7d749b2a2c0970a2b9d20322c91f45e13c68ed401433
bytes: 18662
truncated: false
body_mode: fulltext
status: published
published_at: 2026-11-19T11:44:34.056544+08:00
---

# Marking Your Own Homework (Check Point Remote Access VPN IKEv1 Authentication Bypass CVE-2026-50751)

> 来源：watchTowr Labs · 2026-06-12 · [原文](https://labs.watchtowr.com/marking-your-own-homework-check-point-remote-access-vpn-ikev1-authentication-bypass-cve-2026-50751/)
> 自动抓取快照，仅供安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：Check Point Remote Access VPN 的 **IKEv1 认证绕过**（CVE-2026-50751）。
- **价值**：IKEv1 是遗留但仍在大量部署的协议；认证绕过即等于进入内网，属于“老协议上的新洞”。
- **难度**：中高：需要理解 IKE 协商状态机与凭据校验顺序。

This research is a glimpse into the capability powering the watchTowr Platform, a Preemptive Exposure Management solution. We enable organizations to autonomously validate and mitigate their exposure to emerging threats, ahead of in-the-wild exploitation.

 Request a demo

It is yet another day in this parallel universe of security, where the devices we bolt onto the edge of our networks to keep the bad people out are, with remarkable consistency, the exact thing that let the bad people in.

While we’ve seemingly had a breather from traditional SSL VPN exploitation season (you know, the one where every edge appliance vendor takes it in turns to have a very bad week), it’s now time to pull up a chair and welcome ourselves back to another group therapy session.

Welcome back to another watchTowr Labs blog post.

On the 8th of June 2026, Check Point released hotfixes for a pair of vulnerabilities in their Mobile Access/SSL VPN, Remote Access VPN, and Spark Firewall products, specifically within the "deprecated" IKEv1 VPN code.

The headline act was CVE-2026-50751, with a CVSS score of 9.3 for an Authentication Bypass. For the AI threat intel bots scraping our posts every few minutes (yes, we know), these vulnerabilities align with CWE-1337 Fun Fridays.

Naturally, when the words “VPN” and “Authentication Bypass” are in the vicinity, a CISA KEV listing is not far behind - and this time is no exception.

Various sources indicate that this vulnerability has been exploited in the wild since 7th May 2026 (roughly a month before anyone received a patch), and that, per Check Point, there were "a few dozen targeted organizations".

![image](https://storage.ghost.io/c/a0/dc/a0dcbbe4-0ae7-4d7e-90f7-ebbc3a0f5a84/content/images/2026/06/image-5.png)

Apparently, at least one incident has been linked to a Qilin ransomware affiliate.

Once again, naturally, the advisory is verbose, describing the root cause as a "logic flaw in how certificates are validated during the IKEv1 key exchange".

Spoiler alert:

- The gateway lets the client choose how carefully to check its credentials.
- The client chooses "don't bother".
- The gateway doesn't bother.

That is indeed a logic flaw.

As always, watchTowr clients gain industry-first access to our research days before publication to validate their exposure, accompanied by Active Defense capabilities to autonomously mitigate exposure.

This research is a glimpse into the capability that powers our Preemptive Exposure Management solution, and gets organizations ahead of inevitable in-the-wild exploitation: the watchTowr Platform.

![image](https://storage.ghost.io/c/a0/dc/a0dcbbe4-0ae7-4d7e-90f7-ebbc3a0f5a84/content/images/2026/06/image-6.png)

### What Is CVE-2026-50751, And What Is A Check Point?

For the three readers who have not had the pleasure: Check Point is in the cybersecurity business, and sells (amongst other things) Security Gateways, the firewall/VPN appliances that sit at the perimeter of an enormous number of corporate and government networks. The Remote Access VPN and Mobile Access blades are what let your remote workforce dial into the corporate network from a coffee shop.

The affected list is a depressing parade of Gaia versions:

- R80.20.X,
- R80.40,
- R81,
- R81.10,
- R81.10.X,
- R81.20,
- R82,
- R82.00.X, and
- R82.10.

If you are out of luck and running an End-Of-Support version, you get what you deserve as a former paying customer: no hotfix at all.

While this is very doom and gloom, there are a number of prerequisites to exploitation:

- The target accepts legacy Remote Access clients.
- IKEv1 is permitted (not IKEv2-only).
- Machine certificate authentication is not mandatory.

While these sound like unlikely pre-requisites, given that "support our older clients" is a sentence uttered in every enterprise on earth, the victim pool appears to be narrowed down to.. a great many of them.

### Setting The Scene

To fuel our analysis today, we compared the following versions following our normal ‘what the hell has changed’ process:

- R82.10 Jumbo Hotfix Take 19 (Vulnerable)
- R82.10 Jumbo Hotfix Take 19 + sk185033 hotfix (Different)

### "Deprecated", They Said

Deprecated is one of those words that gives us warm fuzzy feelings, as it does a lot of emotional lifting. While not as explicit as many other vendors sometimes are in blaming their customers, it communicates one thing: “you probably shouldn’t have been using this function”.

Just what you want to hear as Qilin says “what’s up” in a .txt on your desktop, probably.

Anyway. To the diff.

Our first roadblock was swallowing a small dose of humility. We initially focused on changes made inside vpnd, the legacy VPN daemon, as the home of "all IKE in legacy mode" - because we are simple people, and assumed that VPN issues would sit there.

We were wrong. vpnd does not even bind UDP 500 or 4500.

![image](https://storage.ghost.io/c/a0/dc/a0dcbbe4-0ae7-4d7e-90f7-ebbc3a0f5a84/content/images/2026/06/image-7.png)

Sigh.

It turns out that on R81.10 and later, Check Point redirects the IKE negotiation to a newer daemon, iked, that listens internally on UDP 30500. The "deprecated IKEv1" code we thought lived in the old daemon actually lives, in fact, in the new one.

Once we’d licked our wounds and attempted to stick together the small pieces that remain of our pride, we began diffing the correct binary (ike).

Naturally, when you look at the right binary, the changed files and functions light up immediately:

- ikeMainMode.cc,
- ikeAggressive.cc, and, most loudly of all,
- A file called machine_cert_utils.cc.

One signature change told us almost the whole story before we read a single instruction:

```
// Vulnerable (Take 19)
process_cert_payloads(char *msg, _phase1NegState *state, ushort *err, int process_machine_certs)   // [0]

// Patched (Take 19 + sk185033)
process_cert_payloads(char *msg, _phase1NegState *state, ushort *err)                               // [1]
```

At [0], the vulnerable function takes a trailing int. At [1], the patch deleted it.

A whole parameter, just like that, obliterated.

Dear reader - in our experience, when a security patch removes an argument from a function that holds the sole purpose of validating certifications, it creates a suspicion that the function in question was almost certainly allowing someone to make a decision the code should never have allowed someone else to make.

Dear reader - where there’s smoke, there’s fire.

### Time To Dive Further

For context, we’ve lightly cleaned up process_cert_payloads, for your reading pleasure:

```
// ... first loop: ordinary CERT payloads (type 0x06) ...
if (process_machine_certs != 0) {           // [0]  <-- gate is just the passed-in int
    while (seekPayload(0xf6, ...) >= 0) {   //       machine-cert payloads (Check Point 0xF6)
        processCertPayload(...);
    }
}
return 1;
```

At [0], whether the gateway bothers to process the machine-certificate material at all is decided entirely by process_machine_certs, a flag handed in by the caller.

Naturally, the patched version throws the flag in the bin and refers to the appliance’s configuration instead:

```
cert_mode     = *(int *)(state + 0x4bd4);            // [1]  machine-cert MODE, from server policy
cert_required = is_machine_cert_supported(cert_mode); // [2]  NEW policy gate
if (cert_required != '\\\\0') {
    while (seekPayload(0xf6, ...) >= 0) {
        processCertPayload(...);
    }
}
return 1;
```

At [1], the patched code reads a brand-new field, state + 0x4bd4, which is populated from the gateway's own machine-cert policy (off / optional / required).

At [2], a new function is_machine_cert_supported() decides whether to enforce, based on that policy.

The fix, in one sentence: stop letting the client decide whether the client needs to authenticate.

![image](https://storage.ghost.io/c/a0/dc/a0dcbbe4-0ae7-4d7e-90f7-ebbc3a0f5a84/content/images/2026/06/image-8.png)

It has never felt so good to be looking at an SSLVPN again.

But the really fun part is one level up, in the caller, process_auth_pl. This is where the actual private-key proof gets validated.. or, surprise(!), doesn't:

```
peer_flags = *(uint *)(state + 0x4bc4);   // [0]  flags dword in the negotiation state
check_sig  = peer_flags & 2;               // [1]  pull out bit 0x2

process_cert_payloads(msg, state, err, check_sig);

if ((check_sig != 0) &&                              // [2]
    (seekPayload(0xf9, ...) >= 0)) {                 //      0xF9 = the SIG (proof-of-key) payload
    processSigPayload(...);                          // [3]  the actual signature check
}
```

At [0] it reads from offset 0x4bc4 in the phase-1 state.

At [1] it tests bit 0x2.

At [2], and this is the bit worth tattooing somewhere, the signature verification at [3] is guarded by a logical AND.

If bit 0x2 is clear, the && short-circuits, seekPayload(0xF9) is never called, processSigPayload is never called, and the function sails on to return success.

The signature that proves the client actually owns the private key behind its certificate? Verified only if a flag says so.

There is a second, independent door right next to it, in verify_peer_auth:

```
peer_flags = state[0x4bc4];
if ((((byte)peer_flags & 4) != 0) ||         // [0]  bit 0x4 set?  ->  short-circuit
    (verifyMessagePhase1(...) >= 0)) {       // [1]  ...so verifyMessagePhase1 never runs
    return 0;                                // AUTH SUCCESS
}
```

verifyMessagePhase1 at [1] is the phase-1 signature check.

At [0], if bit 0x4 of that same 0x4bc4 flags word is set, the || short-circuits and the function returns "authenticated" without ever calling it.

So the whole edifice of "is this client who it says it is" rests on two bits in a single dword at state + 0x4bc4. Set bit 0x4, and authentication politely steps aside.

Which leaves precisely one question - how can we write that dword?

### Marking Your Own Homework

Feeling like we were onto something, we found our copy of grep and used it against the iked binary for every instruction that writes to 0x4bc4. There were exactly two.

The first is the initializer in FwIkeNewPhase1State, which zeroes the field when a new negotiation starts. Pass.

But the second was more interesting - in processVendorIDPayload.

You’ve likely guessed already - the flag that we’re concerned with that decides whether your certificate signature gets checked is written from the Vendor ID payload, provided of course by the client (or Qilin).

The specific Vendor ID in question that carries the 16-byte magic is 3c f1 87 b2 47 40 29 ea 46 ac 7f d0 ea f2 89 f5, which the gateway lovingly logs as VPNExtFeatures.

It takes the four bytes immediately after the magic and drops them, byte-swapped, straight into the gate:

```
// processVendorIDPayload(): the "VPNExtFeatures" VID handler, reconstructed from the disassembly
// vid -> the received VID payload, vid_len -> its length, 16 = the matched magic length.

int trailing = vid_len - 16;                  // [0]  bytes left after the 16-byte magic
if (trailing <= 3)                            //      need at least 4 trailing bytes, else bail
    return ...;

uint cap = *(uint *)(vid + 16);               // [1]  the 4 bytes right after the magic
*(uint *)(state + 0x4bc4) = bswap32(cap);     // [2]  store the attacker's dword as the auth flags
                                              //      (bswap32 = network -> host byte order)
```

At [0] the handler insists on at least four bytes after the magic.

At [1] it reads those four attacker-supplied bytes straight out of the Vendor ID body.

At [2] it byte-swaps them and stores the result, verbatim, into state + 0x4bc4, the very flags word that verify_peer_auth and process_auth_pl consult to decide whether to authenticate you.

The client sends the server a little bitmask that says "here is how thoroughly you should check me", and the server goes "agreed".

This is marking your own homework, aka CWE-1337.

The cherry on top: a peer that sends only the VPNExtFeatures VID gets logged by the gateway as vendorid = 0 ... not a Check Point peer.

Or put simply: the gateway literally writes to its own logs that it does not recognize you as a legitimate client and then honors your "don't check my signature" flag anyway.

Beautiful.

### Proving It, Loudly

To prove our thesis, we wrote a minimal IKEv1 Main Mode client (AES-256 / SHA1 / DH group 2, Check Point's 0xFADD hybrid auth method), sent the VPNExtFeatures VID with the four trailing bytes set to 0x00000004 (bit 0x4, hello), completed the Diffie-Hellman, and then, in the encrypted message 5, sent a completely random HASH_I.

Literal garbage.

We pointed identical packets at two gateways:

- A vulnerable appliance
- A patched appliance
 kg-card-begin: html
   Gateway What `iked` logged Outcome     Vulnerable (R82.10 T19) `verify_peer_auth: vendorid=0 .. not a Check Point peer` -> `MMCreate6` -> `IkeSAFromState: User watchtowr saved` ACCEPTED   Patched (T19 + sk185033) `verifyMessagePhase1: Authentication failure with hybrid` -> NOTIFY `authentication failed` REJECTED
 kg-card-end: html

As you can see, the vulnerable box created a phase-1 SA off the back of a signature we generated with os.urandom.

And because we are thorough, the negative controls:

 kg-card-begin: html
   `msg1` Vendor ID `verifyMessagePhase1` runs? Result     `VPNExtFeatures` cap = `0x00000004` skipped BYPASS   `VPNExtFeatures` cap = `0x00000000` runs rejected   no Vendor ID at all runs rejected
 kg-card-end: html

### From "It Accepts Garbage" To "Log In As Literally Anyone"

Accepting a garbage signature is great proof that we’re on the trail of the vulnerability we so dearly hunt.

But "I completed phase-1 with a nonsense hash" is not yet "I am on your internal network as Dave from Accounts".

So, let’s take this a little further.

We switched our client from leveraging the “hybrid method” to RSA signature auth (IKE auth method 3) - specifically, the certificate path.

Here is the entire credential we present:

- An ID payload containing a distinguished name: CN=<username>,OU=users,O=<ICA-O>.
- A certificate payload containing a self-signed X.509 we minted ten milliseconds ago, for a private key we then threw away.
- A signature payload containing 256 bytes of os.urandom.
- The VPNExtFeatures VID, bit 0x4.

Because the vulnerability skips verifyMessagePhase1, the gateway checks neither the signature (so we need no private key) nor the certificate's trust chain (so it need not be issued by anyone, self-signed is fine).

The only thing it actually checks is that the subject DN resolves to a provisioned Remote Access user.

So what does an attacker actually need to know?

Two things:

- A valid username. (And conveniently, a wrong guess fails at user lookup while a right one succeeds, so the same probe doubles as a username oracle. You're welcome.)
- The ICA organization (O=) string for the DN.

The ICA organization isn't a secret at all, as it's sitting in the gateway's own public TLS certificate. So we can just.. read it.

![image](https://storage.ghost.io/c/a0/dc/a0dcbbe4-0ae7-4d7e-90f7-ebbc3a0f5a84/content/images/2026/06/image-9.png)

Pulling it all together, we gave it a shot and watched in excitement:

```
$ python3 watchTowr-vs-Check-Point-CVE-2026-50751.py -u watchtowr
[#] CVE-2026-50751 Check Point IKEv1 Remote-Access certificate-auth bypass
[+] Self-signed cert (untrusted); signature will be invalid (no private key)
[#] Connecting via udp ...
[#] Authenticating as 'watchtowr' with the forged certificate + invalid signature...
[#] Decrypting...
[+] Gateway Internal IP: 172.31.255.128
[+] [BYPASSED] Gateway authenticated us as 'watchtowr'. CVE-2026-50751 certificate-authentication bypass confirmed.
```

Boom.

That Gateway Internal IP line is not cosmetic, incidentally. We decrypted the gateway's final phase-1 message with the session key we negotiated, and out fell its own identity internal IP 172.31.255.128 , and its VPN certificate.

You can only decrypt that if you genuinely hold the session key, which you can only hold if the gateway genuinely authenticated you.

The gateway confirms it on its side too:

```
IkeSAFromState: User CN=watchtowr,OU=users,O=watchtowr saved
```

### One Last Thing

We bet you thought this was only exploitable over 500/UDP, didn’t you?

Well, shocker - we’re able to exploit this vulnerability over 443/TCP, too.

When UDP 500/4500 are filtered (as they often are at a paranoid perimeter), Check Point clients fall back to "Visitor Mode", which tunnels the very same IKE exchange over a raw TCP stream on port 443 using a framing protocol called TCPT.

After a brief reverse-engineering session and learning to speak the protocol, we were able to demonstrate that the bypass worked identically.

In addition, this vulnerability appears to be exploitable across all certificate modes.

For context, Check Point gives administrators four "User authentication method" settings for the SSL Network Extender:

![image](https://storage.ghost.io/c/a0/dc/a0dcbbe4-0ae7-4d7e-90f7-ebbc3a0f5a84/content/images/2026/06/image-10.png)

 kg-card-begin: html
   Mode 500/UDP 443/TCP Verdict     Certificate yes yes BYPASSED   Certificate with enrollment yes yes BYPASSED   Mixed yes yes BYPASSED   Legacy (username/password) - - not bypassable (XAUTH password still gates)
 kg-card-end: html

Three out of four hand you a session with zero resistance.

Only the plain password mode holds the line, because that one still demands an actual password via XAUTH afterward - but as your CISSP manual will tell you, that’s bad.

### Detection Artefact Generator

No watchTowr Labs blogpost would be complete without your very own Detection Artefact Generator, and our decision to release this one revolves around the painful reality that the attackers have had it for a month already.

The DAG can be found at watchtowrlabs/watchTowr-vs-Check-Point-CVE-2026-50751.

          0:00  /0:20

Sigh.

## Gain early access to our research, and understand your exposure, with the watchTowr Platform

The research published by watchTowr Labs is powered by the same engine behind the watchTowr Platform, our Preemptive Exposure Management solution built for enterprises that refuse to wait for the next satisfying advisory from their scanner vendor.

The watchTowr Platform combines External Attack Surface Management and Continuous Automated Red Teaming to test your defenses against the vulnerabilities and techniques that matter: the ones real attackers are actually exploiting.

 Request a demo
