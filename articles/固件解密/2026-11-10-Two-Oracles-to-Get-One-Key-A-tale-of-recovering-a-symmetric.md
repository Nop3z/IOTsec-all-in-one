---
title: "Two Oracles to Get One Key: A tale of recovering a symmetric key from an encrypt-only firmware update scheme"
source: "IOActive"
url: https://www.ioactive.com/two-oracles-recovering-aes-firmware-key/
published: 2026-11-10
fetched: 2026-11-16T22:13:50.975181+08:00
category: "固件解密"
score: 4.4
keywords: ["firmware"]
sha256: db2c198d859e824d8a7c17ef5b54c06035d1a8d21c9119009e552590a40faf44
bytes: 6436
truncated: false
body_mode: fulltext
kind: practical
status: published
published_at: 2026-11-16T22:16:27.064129+08:00
---

# Two Oracles to Get One Key: A tale of recovering a symmetric key from an encrypt-only firmware update scheme

> 来源：IOActive · 2026-11-10 · [原文](https://www.ioactive.com/two-oracles-recovering-aes-firmware-key/)
> 自动抓取快照，仅供安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：只凭“加密固件更新”这一个接口，用两个 oracle 拿回固件 AES 密钥：先利用设备对 RSA 密文的“是否超过模数”这一位信息做二分，恢复从未公开的 RSA 公钥模数；再对 PKCS#1 v1.5 做 Bleichenbacher padding oracle，解出固件加密密钥。
- **价值**：攻击角度非常新颖——不需要泄露私钥、不需要物理接触，泄露一位 yes/no 就能把“只加密不验签”的固件更新通道掀开。属于典型的设计层密码学缺陷。
- **难度**：极高。要求对 RSA 填充、模数恢复、设备错误行为差异都有精确控制；但一旦成立，影响是“拿到固件加密密钥”，可离线解包后续所有固件。

.entry-header

div class="entry-image"> </div

Can an RSA public key be recovered if it’s never published? Yes, if the system leaks whether a submitted value exceeds the modulus. That yes/no signal allows a binary search that recovers the modulus in roughly one query per key bit, and with the standard exponent of 65537, the full public key follows.

Why does recovering the public key matter? It enables a Bleichenbacher padding oracle attack against PKCS#1 v1.5, which here recovered the AES key used to encrypt the firmware.

One of the most satisfying moments in vulnerability research is when you find a way around a show-stopper and manage to fully compromise a system. This post covers a specific situation I was investigating a few years ago: a device so well-secured that its only remaining remote attack vector was the firmware update mechanism. Yet within hours, I’d recovered the full AES key the system relied on. What follows is the technique I used to do it.

It was a kind of “weird” setup. The system shipped its firmware as an encrypted binary blob. Specifically, an RSA hybrid (envelope) encrypted blob that combined an AES-encrypted payload with the corresponding AES key encrypted via public-key crypto. It carried the magic Salted__, so I knew OpenSSL was being used somewhere in the toolchain.

The manufacturer had chosen to use public/private key cryptography in an unusual way: the private key was kept inside the device, and the public key was never published, they kept it to themselves. I guess they’d probably thought this design was secure because it behaves like one that has two secret keys: one to encrypt the AES key, and the other to decrypt it.

In practice, however, the system leaked some errors through its update API, which let me discover the padding it used. I was pretty happy to see that padding was PKCS#1 v1.5, the mode that is vulnerable to a padding oracle attack. The only problem: to actually mount that attack, you need the public key. Why? Because it holds both the exponent and the modulus, which are necessary to carry out the right calculations while mounting the padding attack. Except in this case, the public key was never published.

After submitting multiple modifications of the encrypted firmware looking for edge cases, I noticed the system returned a different error when I submitted some specific malformed messages. Reproducing a similar setup offline, I worked out that it was complaining about the submitted data being too large for the modulus. But wait, what does that actually mean?

## The modulus, and why it matters

An RSA public key is really just two integers, written (n, e). The exponent e is almost always 65537 (0x10001), it’s OpenSSL’s default and is also, for practical purposes, fixed. The modulus n is the product of two secret primes, n = p · q, and its bit length is the key size. Encryption itself is a single modular exponentiation:

```
c = m^e mod n          # m = padded message, c = ciphertext
```

Because every operation is reduced modulo n, OpenSSL first checks that the number you submit is smaller than n. Anything equal to or larger than the modulus cannot be a valid RSA block, so it is rejected before the private-key operation with a specific error data too large for modulus error. In other words, for any value c I chose, the endpoint was telling me whether c >= n: a yes/no comparison against the one number the vendor was trying to keep secret.

Using this oracle on the update API, I came up with a simple method to recover the modulus of the key pair. And since the exponent that OpenSSL uses is known, solving for n meant I could fully reconstruct the public key.

## Recovering the modulus with a binary search

The key observation is that the comparation “is c >= n?” is false for every value below the modulus, and true for everything at or above it. Therefore, the smallest value the oracle calls “too large” is the modulus itself. Using an implementation similar to the below pseudocode, I started quering the oracle with values. If the system returned an error, I would move to the lower half. If it passed the filter, I’d move to the upper half, get the middle value, and then query again. I did this until I could narrow it down to the exact byte that would return an error but the same value minus 1 would pass the filter.

```
lo = 2**(bits-1)          # a real modulus has its top bit set
hi = 2**bits - 1
while hi - lo > 1:
    mid = (lo + hi) / 2
    if too_large(mid):    # oracle: is mid >= n ?
        hi = mid
    else:
        lo = mid
n = hi                    # the smallest 'too large' value is n itself
```

Figure 1. Aa binary search over the k-bit range converges on n in about k queries, one per bit.

![Figure 2. Flow Diagram of the queries used to recover the actual modulus. The flow begins with the most significant byte and then moves to the next one, continuing until we have fully recovered the modulus.](https://www.ioactive.com/wp-content/uploads/2026/11/Figure-1-728x1024.png)

Figure 2. Flow Diagram of the queries used to recover the actual modulus. The flow begins with the most significant byte and then moves to the next one, continuing until we have fully recovered the modulus.

## The second oracle: Bleichenbacher on the padding

In the final step, we’re essentially turning the padding check into a second oracle. You submit chosen multiples of the captured ciphertext, and for each one, the endpoint tells you whether the decrypted block begins with the valid 00 02 header of a well-formed v1.5 block. Every “valid” answer confines the unknown plaintext to a narrower numeric interval; iterating the construction shrinks that interval, multiple by multiple, until a single value is left.

Note that this attack doesn’t reveal the actual private key but the plaintext it’s trying to protect. In this specific scheme, the RSA block actually wraps the AES firmware key itself. So, the plaintext Bleichenbacher recovers is not some intermediate secret, it’s the exact symmetric key I’d been after from the start.

I did not reinvent the wheel here: I simply followed Dennis Yurichev’s clear reference write-up of the attack, then adapted my implementation to match this device’s padding oracle error.

- Bleichenbacher Attack
- Cryptography
- Embedded Security
- firmware security
- hardware security
- Padding Oracle
- rsa

 .entry-content
