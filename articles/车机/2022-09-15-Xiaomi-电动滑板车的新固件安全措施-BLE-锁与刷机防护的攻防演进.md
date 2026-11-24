---
title: "Xiaomi 电动滑板车的新固件安全措施：BLE 锁与刷机防护的攻防演进"
source: "RoboCoffee"
url: https://robocoffee.de/?p=193
published: 2022-09-15
fetched: 2026-11-24T20:29:01.595391+08:00
category: "车机"
score: 0
keywords: []
sha256: d86a3ab7e655cc44e4f508b89265d714612388e488290d8a75a8543e5f7b77bd
bytes: 13279
truncated: false
body_mode: fulltext
kind: practical
status: published
published_at: 2026-11-24T20:30:46.008546+08:00
---

# Xiaomi 电动滑板车的新固件安全措施：BLE 锁与刷机防护的攻防演进

> 来源：RoboCoffee · 2022-09-15 · [原文](https://robocoffee.de/?p=193)
> 归档用于安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：作者以自有的 Xiaomi Mi 1S 电动滑板车为对象，追踪厂商逐步加码的固件防护（固件签名、BLE 认证、防降级），并给出各代防护的实际绕过/失效方式。
- **价值**：少见地以“同一产品线的防护演进”为主线，能看到厂商加固与破解之间真实的拉锯；对评估电动滑板车/共享出行设备的固件信任链非常直接。
- **难度**：中高 —— 需要 BLE 抓包与固件提取，但不需要开壳。

.entry-header

![image](https://robocoffee.de/wp-content/uploads/2022/04/IMG_20220421_104750-1024x576.jpg)

Xiaomi Mi 1S dashboard with attached SWD Debugger (four wires, left) and UART sniffer (two wires, right)

Updated 2022-04-21: Added main picture, added in-depth details with references, added appendix, updated inaccurate paragraph on ESC firmware

Chinese tech giant Xiaomi started rolling out new security measures to counter illegal modification of their device’s firmware. I own a Xiaomi Mi 1S Electric Scooter and can tell that this product is affected. Out of personal curiosity I wanted to have a look…

## OTA firmware updates

To inspect device firmware one doesn’t necessarily need access to the hardware (as demonstrated in the main picture) – intercepting the chip’s flashing process is much more convenient!

Today, the firmware of most electronic devices is updated „over-the-air“ (OTA). Meaning, the firmware file is no longer downloaded and installed by the user manually, but rather through an automated process. With OTA updates the user usually never gets to see the actual firmware.

Because firmware is subject to copyright laws the user no longer runs into the legal risk of accidentally sharing the file. On the downside, the user never gets to see the content of the installed files. After all, the firmware could contain code meant to spy on you or worse – you would never find out. Or could you?

## Capturing firmware files

Every update procedure involves downloading a file which is then installed onto the device. Just because these steps are invisible to the user it doesn’t mean that they don’t happen. The easiest way to capture the file is by sniffing network traffic. Another way is to access the filesystem or dump the RAM of the application used to perform the update.

The Xiaomi electric scooters actually come with three firmware files, one for each component: battery management system (BMS), electronic speed controller (ESC) and the dashboard BLE chip:

![image](https://robocoffee.de/wp-content/uploads/2022/04/image.png)

Retrieved firmware files

Simply observing the new firmware filenames one can see that the BLE firmware file is now equipped with a _signed appendix and ESC firmware starts with an EC_. With a brief look into the file contents one finds the same two certificates attached to the file ends:

![image](https://robocoffee.de/wp-content/uploads/2022/04/image-10.png)

New data found appended to firmware
– Green: Identifier (with 4-byte checksum)
– Yellow: Root certificate
– Red: App certificate
– Blue: Signature

## ECDSA-with-SHA256

Running the attached certificates through openssl reveals the first one to be a root certificate (Mijia Root), the second one to be an application level certificate (Mijia Open) and the underlying cryptographic algorithm: ecdsa-with-SHA256.

![image](https://robocoffee.de/wp-content/uploads/2022/04/image-2.png)

Application level certificate including EC public key and digital signature

The Elliptic Curve Digital Signature Algorithm (ECDSA) uses public-key cryptography to validate the authenticity of the message/data. In public-key cryptography a pair of keys is generated: a private key and a public key. In Elliptic Curve cryptography (ECC) this pair is generated from (geometric/mathematical) elliptic curves. This is far more secure than lets say prime numbers in RSA.

SHA256 is a hash algorithm designed by the NSA. Meaning, no one besides the NSA can produce the data from the hash :). SHA256 produces a hash of 256 bit length for any input message/data.

## Data signing and validation with ECDSA

In order to sign (or encrypt) data in public-key infrastructure a key pair is needed. Naturally, for ECDSA an EC key pair with private and public key is generated before all else.

To calculate the EC signature following three steps are then ran:

- Calculate SHA256 of firmware data
- Choose random number (the „nonce“, must be secure!!) to generate a point on the selected ECC curve (here: prime256v1)
- Calculate the signature using nonce, selected point, private key and hash

(To keep this post simple, formulas have been omitted and steps simplified.)

For signature validation, the public key is used to retrieve the original file hash back from digital signature. This file hash is than compared to the hash of the received data to tell whether the same data, which was signed, is received, or if it has been tampered with.

![image](https://robocoffee.de/wp-content/uploads/2022/04/image-4.png)

Source: https://www.segger.com/products/security-iot/emsecure/variations/emsecure-ecdsa/

Back to our case: To validate the signed firmware files you can use my script from the appendix. It first separates the (application level) certificate and data signature (signature bytes follow after the last certificate) from the firmware data, and then runs openssl to verify the signature against the firmware data given the public key from the certificate. In short: Running the command bash verify.sh <firmware_file> will give you the message „Verified OK“ if the file was correctly signed.

Using this method, the verification for both captured firmware files succeeds. We can conclude that the firmware itself must be doing a similar verification.

## BLE_signed: A deep dive

We already know that the new BLE firmware is signed, but it’s also not encrypted. This means it can be disassembled and analyzed!

It’s easy to find out that the section containing the certificates (at the end of the file) is referenced from within the flash procedure [1]. And if a certain condition is not fulfilled the flash procedure never finalizes [2]. Based on the previous examinations of signature verification there’s reason to believe that the function involved in this condition compares the file hash of the received data against the original file hash calculated from the signature and public key contained in the certificate [3].

Furthermore, hints to a new flash procedure can be found in the BLE firmware [5]: It contains a whole new set of functions that (together with previously mentioned function for signature verification) are all situated in a block in the beginning of the firmware [4], indicating a newly added library. This new procedure is structurally similar to the existing flash procedure and it intercepts all flash commands designated to the ESC [6]. Scary stuff!

References (ESC_BLE_V1.5.7)

- 0x7794
- 0x3670
- 0xd9d0 & 0xda42
- 0x404 to 0x6f4
- 0xcda4
- 0x3d4e

## EC_ESC: More insights

The ESC firmware can be decrypted in the same way as previous firmware files (after truncating the certificates), but the BLE firmware now acts as a gatekeeper: By monitoring the UART communication between dashboard (BLE) and controller (ESC) we observe that when performing the ESC update… nothing happens! Only after 50% progress the transmission of data from BLE to ESC starts (an excerpt of the new UART log can be found in the appendix). Previously, flash commands designated to the ESC where simply passed through the BLE.

Observing this behavior we can bridge a logical gap: The new flash procedure found in the BLE firmware (see last paragraph in previous section) is responsible for the memory management of all intercepted packets! Only after a full transfer and verification the procedure is finalized. Since both BLE and ESC firmware come with the same public key and a unique signature, the verification procedure must follow the same principle.

We summarize the new flash procedure for ESC firmware as follows:

- ESC flash commands get intercepted by BLE
- BLE writes firmware data into own flash!
- Using the same procedure as before the signature of the data is verified
- If verification succeeds the data is passed on to the ESC

## Conclusion

The new security measures are on-par with today’s security standards. BLE firmware is signed using ECC and signatures only pass validation if they’re signed using the correct private key.

Xiaomi seems to have taken security concerns from users and authorities seriously. Instead of simply swapping out keys, new security features with signed firmware files have been implemented.

These measures can be seen as secure given the following context:

- A secure random number generator to generate the nonce for the signature. If a static nonce was used it could allow an attacker to recover the EC private key, like in the PlayStation 3 hack.
- The firmware is secure against buffer overflows or other memory exploitation techniques. If an attacker finds a way to modify the memory or memory address of the stored public key a different key pair could be used to sign the data.

## Appendix

split.py – Python script to split firmware file into data, certificate and signature (root certificate omitted):

```
import sys

if __name__ == "__main__":
    filename = sys.argv[1]
    with open(filename, 'rb') as f:
        data = f.read()

        pattern = b"\x2d\x2d\x2d\x2d\x2d"
        i = data.find(pattern, 0xdfff)
        if i == -1:
            i = data.find(pattern)
        fw, appendix = data[:i], data[i:]

        i_s = appendix.rfind(pattern)
        i_ce = appendix.rfind(pattern, 0, i_s)
        i_cs = appendix.rfind(pattern, 0, i_ce)
        sign = appendix[len(pattern)+1+i_s:]
        cert = appendix[len(pattern)+1+i_cs:i_ce]

        with open(filename + ".data", 'wb') as outf:
            outf.write(fw)
        with open(filename + ".cert", 'wb') as outf:
            outf.write("-----BEGIN CERTIFICATE-----\n".encode())
            outf.write(cert)
            outf.write("-----END CERTIFICATE-----\n".encode())
        with open(filename + ".sign", 'wb') as outf:
            outf.write(sign)
```

verify.sh – Bash script to verify the firmware against the appended signature and public key:

```
# 1. split BLE_signed into three parts: data + certs + signature
python split.py $1

# 2. extract pub_key from cert
openssl x509 -in "$1.cert" -noout -pubkey -out "$1.pub"

# 3. verify data using pub_key and signature
openssl dgst -verify "$1.pub" -keyform PEM -sha256 -signature "$1.sign" -binary "$1.data"
```

UART log showing delayed start of ESC flash process:

```
... (after ~50% progress) ...
55aa0320017f025aff
55aa0423017fc16b2cfe
55aa0320017f025aff
55aa0423017fc16b2cfe
55aa04200270010068ff
55aa032302700166ff
55aa06200700006e000064ff
55aa062061b20202292475fe
55aa0320017f025aff

55aa02
2307
00d3ff
55aa042301b202081bff
55aa0423017fc16b2cfe
55aa82200800774019f6456798d91633253245117bb42fda8615773a193048ac6ca5e7887a    +++9c234555c92c4a4d859272586ced17e9870a2595f14d09fc57ac2a3f458ec2747a67a43    +++d9cb848dee0e60a61e37f77007626122be78bb9bb75f1f47eab43db66f791e5e4c83c5c    +++944f892ab056f19d0fe2a4c2a7949a9cb53aba77e15fa3cdd454f8bf

55aa02
2308
00d2ff
55aa82200801b54e0814f03f3514412eb5d248c0df64b01510b93f9bebdada5ffb5bd2e137    +++b0503272551b249e5e5cb65df0d6258ef2588c50e45658f5afc81993f69f843eeb124d0    +++f5ef52ef9391fd54ca3f0f766812e4a768539741a3ed3a667411f6397e84f667095cf38    +++1cfdc4e946fba41ae24cb996340d0b6faf9c43cc62aa8e3a4bcc39c0
...
```

 .entry-content

 .post-inner

 .section-inner   .pagination-single

## 5 Antworten auf „Exploring Xiaomi’s new firmware security measures“

 .comments-title

 .comments-header

.comment-meta

Spot on with this write-up, I truly believe this site needs much more attention. I’ll probably be returning to read more, thanks for the advice!

 .comment-content

 .comment-body

 #comment-##

.comment-meta

Good blog post. I definitely love this website. Stick with it!

 .comment-content

 .comment-body

 #comment-##

.comment-meta

Not everything in the article is completely accurate. There are more wrong statements. But it’s nicely written and it’s definitely a great start to understanding the new protection.

 .comment-content

 .comment-body

 #comment-##

.comment-meta

Glad to be one of several visitants on this awing internet site : D.

 .comment-content

 .comment-body

 #comment-##

.comment-meta

Thanks a lot for the blog article. really Great.

 .comment-content

 .comment-body

 #comment-##

 .comments-inner

 comments

Kommentare sind geschlossen.

 #respond

 .comments-wrapper

 .post
