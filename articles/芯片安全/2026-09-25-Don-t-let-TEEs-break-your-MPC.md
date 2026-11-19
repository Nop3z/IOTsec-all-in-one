---
title: "Don't let TEEs break your MPC"
source: "Trail of Bits"
url: https://blog.trailofbits.com/2026/09/25/dont-let-tees-break-your-mpc/
published: 2026-09-25
fetched: 2026-11-19T12:02:12.663918+08:00
category: "芯片安全"
score: 4.0
keywords: ["tee", "attestation"]
sha256: f448ba705755950bfd32d12e2bea96e6714e23dfd062bb9fea0ac39942c381e8
bytes: 18693
truncated: false
body_mode: fulltext
kind: practical
status: published
published_at: 2026-11-19T12:20:43.910308+08:00
---

# Don't let TEEs break your MPC

> 来源：Trail of Bits · 2026-09-25 · [原文](https://blog.trailofbits.com/2026/09/25/dont-let-tees-break-your-mpc/)
> 自动抓取快照，仅供安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：阈值签名/MPC 越来越多地跑在 TEE 里，Trail of Bits 分析 TEE 的威胁模型（回滚、侧信道、共模故障）如何在组合架构中破坏 MPC 的安全保证。
- **价值**：硬件钱包与托管服务几乎都是“TEE + MPC”架构，这类组合安全分析很少见，能直接指导设计取舍。
- **难度**：中高 —— 需要 MPC 协议与 TEE 威胁模型两边的知识。

Page content

Threshold signature schemes, a form of multi-party computation (MPC) that lets a set of parties sign together without any one of them holding the key, are increasingly deployed inside trusted execution environments (TEEs). The combination is intended to amplify security for sensitive computations: MPC distributes trust across multiple independent parties, while TEEs root trust in the hardware manufacturer and its attestation infrastructure. But subtle issues can arise when running an MPC protocol inside a TEE without accounting for the untrusted host: for example, a malicious host could roll back the filesystem state after a threshold signer deletes a used pre-signature, causing the signer to reuse their nonce share and disclose their private key share.

So is this combination worth it? Provided you treat the TEE as a defense-in-depth layer rather than a substitute for a sound protocol, the answer is yes. This blog post discusses what TEE attestation can and can’t fix in MPC deployments, explores the pitfalls we see most often in audits, and covers best practices, such as incorporating strong attestation processes and binding them to the MPC parties’ identities.

## MPC: Security that depends on participant behavior

Before diving into how TEEs and MPC interact, we need to understand what MPC means and what security guarantees it offers. MPC is a cryptographic technique that allows multiple parties to jointly compute a function over their private inputs without revealing those inputs to each other.

The security of MPC protocols depends critically on assumptions about participant behavior. The cryptographic literature uses two primary security models:

Semi-honest (honest-but-curious) security: In this model, all participants follow the protocol exactly as specified, but they may try to learn additional information from the messages they receive during the protocol execution. Participants can try to learn more than they should, but they don’t deviate from the protocol specification.

Malicious security: This stronger model assumes participants may deviate arbitrarily from the protocol. A malicious participant might send incorrectly computed values, use wrong inputs, abort the protocol at strategic moments, and behave in ways designed to compromise security or learn private information.

This distinction is important in the context of TEEs. If a TEE attestation can cryptographically guarantee that all parties are running the correct protocol implementation, it effectively elevates semi-honest protocols to provide malicious security guarantees (at least against certain classes of attacks, as we’ll discuss later). But before delving into the details, let’s discuss how TEEs work.

## TEEs: Three core security guarantees

TEEs are secure areas within a processor that provide hardware-based protection for code and data, even from privileged software like operating systems or hypervisors. TEEs offer three core security guarantees:

Confidentiality: Data and code are encrypted in memory and accessible only from within the TEE. This ensures that even privileged system software cannot inspect the contents of the secure computation.

Integrity: The data and code are protected from tampering. Any attempt to modify the TEE’s memory or execution state from outside should be detected.

Attestation: Remote parties can cryptographically verify what code is running in the TEE. This allows external verifiers to gain assurance about the computation being performed and the legitimacy of the TEE without trusting the host system.

This last property is particularly crucial for building distributed systems with TEEs.

### How TEE attestation works

The attestation mechanism is at the heart of TEE security. When a TEE is manufactured, it’s provisioned with a private key and a corresponding certificate that chains back to a root certificate held by a trust anchor (typically the manufacturer).

When an attestation is requested, the TEE takes measurements (cryptographic hashes of the TEE software, configuration, and hardware state). These measurements are bundled into a “quote” (a manifest of these cryptographic hashes), which the TEE then signs with its private key.

To verify these attestations, a number of checks need to be performed. However, the checks necessary in the verification process aren’t uniformly defined and are somewhat vendor-specific. For instance, Intel’s TDX documentation states:

> TD Quote Verification is the process by which a TD Quote is verified in a remote attestation flow. This verification can be done by any party and the checks performed are defined by this party.

This places significant responsibility on developers, who might not fully understand what checks are required to ensure the security of the TEE deployment.

At a minimum, a proper verification process requires:

- Verifying the quote signature
- Verifying the certificate chain back to the trusted root
- Verifying the actual measurements against known-good values (often stored in binary transparency logs)

This means deploying TEE-based systems involves not just cryptographic verification but also reproducible builds and binary transparency infrastructure. The measurements in the attestation quote are simply hashes; they don’t inherently indicate whether the code is correct or malicious. To verify that the TEE is running the intended software, what is required is a trusted source of reference measurements. Reproducible builds ensure that anyone can compile the same source code and arrive at identical binaries (and thus identical measurements). Binary transparency logs provide a tamper-evident record of what measurements correspond to what software versions, allowing verifiers to check that the TEE is running legitimate, audited code rather than a compromised variant. This piece is often overlooked in TEE deployments.

## The trust model clash

Here’s where things get interesting. Multi-party computation is fundamentally about distributing trust among multiple participants. No single party should be able to compromise the computation. TEEs, in contrast, centralize trust in the hardware manufacturer that controls the root certificate.

Another important threat model shift to consider is the fundamental inversion of traditional security assumptions in TEEs. Historically, we trusted the host operating system and built our security models on that foundation. TEEs flip this on its head: they’re virtualized environments where the guest (the code running inside the TEE) is trusted, but the host system is explicitly considered untrusted and potentially malicious.

This shift creates new attack surfaces that didn’t exist in traditional computing models. While the TEE protects the guest environment from the host, the host still controls critical operations like I/O, memory management, and CPU scheduling. The host can deny service, manipulate timing, or attempt rollback attacks, leading to subtle breaks of MPC protocols.

![“Figure showing decentralized vs. centralized trust model shift”](https://blog.trailofbits.com/2026/09/25/dont-let-tees-break-your-mpc/tee-mpc-figure1_hu_dedf906638555a09.webp)

Figure 1: Decentralized vs. centralized trust model shift

## What TEEs can (and can’t) fix in MPC deployments

Combining these technologies can be beneficial, but one must be careful about the security claims that can be made. The security gains are real only if the TEE implementation is sound and the attestation process verifies the right properties. When TEEs attest to incomplete measurements or fail to verify critical components, the attestation provides false assurance. The actual security posture may even be weakened by the added complexity.

In an attempt to narrow down what TEEs can fix in MPC implementations, we’ve identified the common categories of MPC issues we frequently encounter in security audits:

- Ambiguous encoding in hash functions (e.g., “YOLO” is not a valid hash construction)
- Misbehaving participants
- Missing parameters in Fiat-Shamir transforms (e.g., Coordinated disclosure of vulnerabilities affecting Girault, Bulletproofs, and PlonK)
- Missing input validation (e.g., Breaking the shared key in threshold signature schemes)
- Side-channel attacks
- Protocol-level issues (e.g., Friends don’t let friends reuse IVs)

Arguably, if TEEs were perfectly secure, they could effectively mitigate the first four categories. When attestation and measurement processes are correctly implemented, each party gains cryptographic assurance about what code the other parties are running. This is powerful: if a party can verify that all other participants are running the exact protocol implementation expected (with no modifications or protocol deviations), then they know other participants will follow the protocol correctly and won’t misbehave by sending malformed messages. Essentially, correct attestation eliminates entire classes of implementation vulnerabilities by ensuring protocol compliance on both the sender and receiver sides. However, perfect security doesn’t exist in practice. Real-world TEE implementations have vulnerabilities, attestation processes can be incomplete or incorrectly verified, and the adversarial host environment introduces attack surfaces that are not traditional to MPC deployments.

## A cautionary tale: Rollback attacks with threshold signatures in TEEs

Consider threshold signature schemes, which often use pre-signature optimizations. In Schnorr or ECDSA threshold signatures, participants can precompute nonce commitments independently of the message, speeding up the online signing phase. These precomputed nonce commitments are called pre-signatures, and the reuse of a pre-signature value by a participant leads to the leak of their private share (akin to how nonce reuse in traditional Schnorr and ECDSA signatures leads to private key recovery).

It might be tempting to run such an MPC protocol inside a TEE enclave to mitigate these types of attacks. But subtle issues can arise. In some implementations, signers store pre-signatures to disk and delete them after use (to limit the possibility of reuse). If that application were deployed to a TEE in a trust model where the host is potentially malicious, the host could roll back the filesystem state after the signer deletes a pre-signature file. When the TEE later fetches the pre-signature contained in that file, the signer essentially reuses their nonce share, which leads to a disclosure of the private key share. This is also discussed in the blog post A trail of flipping bits.

## Common TEE pitfalls

Beyond the rollback issue, several other pitfalls frequently appear:

Incomplete attestation measurements: The security of TEE attestation hinges on measuring the right things. An attestation quote contains hashes of code and data, but project developers determine what gets measured and what gets excluded. If critical components aren’t included in the measurements, an attacker can modify those components without detection. This is particularly risky because the attestation appears cryptographically valid, but it’s attesting to an incomplete picture of the execution environment. For example, installing tools in an enclave from remote sources at runtime (e.g., using curl) pulls in code that was never measured; an attacker gaining access to that source can substitute their own and gain code execution inside the enclave.

A real-world example demonstrates this risk: a vulnerability in Meta’s WhatsApp Private Inference revealed that the attestation process didn’t include certain configuration files, enabling an attacker to inject malicious shared libraries with the LD_PRELOAD environment variable, potentially compromising the TEE while maintaining a valid attestation quote.

Missing verifications: The attestation process requires multiple verification steps, each critical to the security guarantee. Verifiers must check the quote signature, validate the certificate chain back to the manufacturer’s root certificate, confirm that the measurements match expected values, etc. Skipping any of these steps breaks the security model. Because verification procedures vary across TEE vendors and aren’t always well-documented, implementations sometimes omit crucial checks.

Lack of hardening: A TEE protects whatever runs inside it, including components that may not be needed. Redundant kernel drivers, overly permissive kernel config flags, stray ACPI table entries, unnecessary systemd services and timers, and weak entropy sources all increase the attack surface inside the trust boundary. Trim the image down to what the project requires, harden what remains, and measure it. For platform-specific guidance, see our notes on the AWS Nitro Enclaves attack surface.

Data availability and backups: Enclaves have limited persistent storage, so backups and recovery data typically live outside the trust boundary. Authenticated encryption provides confidentiality and integrity but not freshness, so a malicious host can serve a stale backup to force a rollback, as discussed earlier in our threshold signature example. More concretely, one recurring failure is a guest trusting attacker-controlled metadata that lives on disk: the disclosure of several vulnerabilities in LUKS2 disk encryption for confidential VMs shows that a malleable, unvalidated LUKS2 header lets an attacker with disk write access swap in a null cipher, leaving the guest reading and writing secrets on an effectively unencrypted volume.

Side-channel and physical attacks: Because the untrusted host controls the TEE’s execution environment, it can perform various side-channel attacks to extract information about the guest’s computation. These can leak sensitive information and break a TEE’s confidentiality guarantees. Similarly, researchers regularly publish physical attacks on TEE hardware. For example, the recent “TEE fail” attack allows an attacker to break the security guarantees of Intel TDX and AMD SEV-SNP by using a memory interposition device that lets them physically inspect all memory traffic inside a DDR5 server. The more recent DDRop attack goes even further: an interposer costing under $200 silently drops DDR5 writes, so the processor keeps reading stale data that still decrypts correctly, breaking the integrity of Intel TDX, Scalable SGX, and AMD SEV-SNP. Memory encryption without freshness fails the same way disk state does in the rollback example above.

Centralization risks: When MPC aims to distribute trust but TEEs centralize it in the manufacturer and its attestation infrastructure, the security goals of the protocol may be undermined. If all parties in an MPC protocol run their TEE nodes on the same TEE vendor’s hardware or if they use the same cloud provider, trust becomes centralized in that provider (for example, by way of the attestation chaining back to that vendor-operated root of trust).

Insecure defaults: Be aware of some of the limitations that vendor-provided verification tools have. For example, Intel tools allow known-vulnerable firmware versions to pass the remote attestation process for one year after public disclosure. Users might want to implement their own security version number validation on top of the defaults to enforce stricter deadlines.

## Best practices for combining TEEs and MPC

If you’re building systems that combine these technologies, consider these recommendations:

Implement strong attestation processes: Bind attestations to the identities of MPC parties and verify them comprehensively. This means not just checking that an attestation is valid but also confirming that the specific party you expect to be running the code is actually the one presenting the attestation.

Terminate peer-to-peer communications inside TEEs: This provides end-to-end protection for party communications. By establishing TLS or other encrypted channels directly between TEEs (with endpoints inside the secure enclaves), you prevent the untrusted host from observing or tampering with protocol messages.

Perform comprehensive verification of the attestation and measurements: Refer to your specific TEE vendor’s documentation for the necessary checks to be performed, and ensure every verification step is implemented correctly, tested, and reviewed.

Write constant-time code: This helps prevent timing side-channel attacks. Even within a TEE, timing variations in your cryptographic operations can leak information to a host performing careful measurements. Use constant-time implementations for all security-critical operations processing secrets.

Consult vendor-specific guidance: Each TEE platform has unique characteristics, limitations, and recommended practices. Vendor documentation often includes details about platform-specific threats. Stay current with security advisories and updates, as TEE security is an active research area with new vulnerabilities regularly discovered. Follow best practices documentation, like our guidance for AWS Nitro Enclaves.

Use multiple TEE vendors: For defense in depth, consider running MPC protocols on TEEs from different manufacturers (and/or cloud providers) to avoid centralizing trust in a single vendor. While admittedly challenging in practice since it requires additional operational complexity, this diversity can be essential for high-security applications where trust distribution is critical.

## Layered trust beats either layer alone

Combining MPC and TEEs is not automatic security, but when done correctly, it represents a defense-in-depth strategy that’s stronger than either technology alone. TEEs can effectively mitigate several categories of MPC vulnerabilities by cryptographically guaranteeing correct protocol execution. Meanwhile, MPC’s distributed trust model reduces the impact of TEE manufacturer centralization and may provide security even if individual TEE instances are compromised.

However, this benefit only materializes when both layers are correctly implemented. New vulnerabilities can emerge from their interaction, as we saw with the rollback attack example. Successful deployment requires following established best practices, implementing thorough attestation verification, and carefully reviewing the implementation and deployment procedure.

The intersection of these technologies represents the cutting edge of secure computation, but only if we approach it with a clear understanding of the tradeoffs involved. If you’re deploying MPC on TEEs, our cryptography team reviews these exact systems, so get in touch!
