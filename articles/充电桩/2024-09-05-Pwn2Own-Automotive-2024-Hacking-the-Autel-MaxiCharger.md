---
title: "Pwn2Own Automotive 2024: Hacking the Autel MaxiCharger"
source: "Sector7"
url: https://defion.security/en/research-labs/pwn2own-automotive-2024-hacking-the-autel-maxicharger/
published: 2024-09-05
fetched: 2026-11-19T11:35:50.129835+08:00
category: "充电桩"
score: 6.0
keywords: ["pwn2own", "automotive"]
sha256: 257627b349d68833049b8e4f3fe4f61e6efc1353d484b9252a20f751c9b8361d
bytes: 25862
truncated: false
body_mode: fulltext
kind: practical
status: published
published_at: 2026-11-19T11:44:34.056544+08:00
---

# Pwn2Own Automotive 2024: Hacking the Autel MaxiCharger

> 来源：Sector7 · 2024-09-05 · [原文](https://defion.security/en/research-labs/pwn2own-automotive-2024-hacking-the-autel-maxicharger/)
> 自动抓取快照，仅供安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：Pwn2Own Automotive 2024 上对 Autel MaxiCharger 的利用复盘（同系列还覆盖了 ChargePoint Home Flex 与 JuiceBox 40）。
- **价值**：充电桩是“物理接触 + 网络”双面攻击目标，公开的完整利用链很稀缺。
- **难度**：高：需要处理充电桩的固件与云-端通信协议。

Breadcrumb    Meta

Pwn2Own 5 September 2024 · 21 min read

  Title

# Pwn2Own Automotive 2024: Hacking the Autel MaxiCharger

  Body

During Pwn2Own Automotive 2024 in Tokyo, we demonstrated exploits against three different EV chargers: the Autel MaxiCharger (MAXI US AC W12-L-4G), the ChargePoint Home Flex and the JuiceBox 40 Smart EV Charging Station with WiFi. This is our writeup of the research we performed on the Autel MaxiCharger, the bugs we found (CVE-2024-23958, CVE-2024-23959 and CVE-2024-23967) and the exploits we developed. During the competition, we were able to execute arbitrary code on this charger with no other prerequisites than being in range of Bluetooth.

## Background

Of the chargers we looked at, the Autel MaxiCharger had by far the most extensive hardware feature set. Just from the outside, we could already see:

- WiFi
- Ethernet port
- Bluetooth
- 4G LTE connection (with a SIM card slot)
- RFID reader
- LCD touch screen
- RS485
- Undocumented USB-C port next to the SIM card slot

The app also shows a lot of features we didn't see on the other chargers. For example, users can specify the OCPP URL the charger will connect to. It even allows users to set a charger up as a public charger, which means the charger accepts arbitrary RFID charging cards and the owner gets reimbursed for the energy used. This is a very interesting feature to keep in mind.

Inside the charger, we found a lot of nicely labelled test points, including multiple UARTs. We even found some unused internal micro-USB headers on the PCBs, although we didn't try them, so we don't know what data they may carry.

The hardware we did identify includes:

- A GigaDevices GD32F407 as the Charge Control Module (ECC).
- An ESP32-WROOM-32D running the AT firmware, used exclusively for WiFi and Bluetooth.
- An ST Micro STM32F407ZGT6 as the Power Control Module (ECP).
- A Quectel EC25-AFX (4G LTE).
- An LCD controller for which we had firmware (an LCD Control Module, LCD Information Unit, LCD Resources Unit and LCD Languages Unit), but no information on what type of chip.

We are not totally sure all of this is correct: the charger has a lot of functionality, split out over a lot of different components. Many of those were not relevant to our research. For example, we are unsure of the use of the Barrot BR8051A01 chip, identified by ZDI as a bluetooth radio, as everything we've seen suggests the ESP32 handles both WiFi and Bluetooth.

## Obtaining the firmware

Obtaining the firmware was by far the hardest part of hacking this charger.

The first time we turned it on, we paired a phone over Bluetooth and connected the charger to a WiFi network that was capturing all traffic with tcpdump. We initiated a firmware update that was available, but later on we saw that the packet capture had obtained nothing relevant. Apparently, the phone was downloading the update and sending it over Bluetooth to the charger.

We tried again while intercepting the network traffic of the phone with Burp. We determined that the update process works like this:

- The app requests the versions of all firmware components from the main controller of the charger over BLE.
- The app submits this information to Autel's server.
- At any later point, the app can ask the server if there are any updates for that charger.
- If there are any, the server sends back an URL for each component for which an update is available.
- The app downloads the files from those URLs and sends them over BLE to the charger.
- The main controller of the charger sends the update to the right component.

We tried to replicate this, but the URLs we got back were obfuscated. To deobfuscate them, we tried decompiling it or hooking into the app. This turned out way harder than we expected: the code of the mobile apps is obfuscated and the app contains anti-debugging tricks.

Eventually, we gave up with the app and looked a bit more closely at the obfuscated URLs we had gotten back, and noticed that they do look quite close to being base64 encoded. If we base64 decode them, we don't get back readable text, but we can see that some bytes line up with a (pre-signed) Amazon S3 URL:

By guessing some characters (like the "https://" at the start) and comparing the base64 encoded version of the guessed URL with the actual data, we could work out (step by step) that all they did was applying a simple substitution before base64 decoding:

- A ➔ a
- a ➔ A
- B ➔ b
- b ➔ B
- C ➔ c
- c ➔ C
- D ➔ d
- d ➔ D
- E ➔ e
- e ➔ E
- F ➔ f
- f ➔ F
- G ➔ g
- g ➔ G
- 7 ➔ y
- y ➔ 7

With that figured out, we could download the firmware files. To get all the URLs of the firmware for each component, we had to ask the server. As our charger was now on the latest version, it would not reply with any URLs until the next update was available.

For most of the components of the charger, we found we could just submit a lower version number as the current version by subtracting 1 from the minor version to get back the URL for the current version. For one of the components, this didn't work: it was on version 0.00 and we could not submit anything lower. But we had the firmware of the main controller, which was the target we were most interested in.

### Decrypting the firmware

These files were again obfuscated, but also not very well. We could observe a pattern that was repeating every 256 bytes:

This suggests it could be a XOR with a 256 byte key. We made some guesses of what this key could be: we first looked for each offset in the 256-byte blocks which byte value was most common, and then we looked at which 256-block in its entirety was most common. Firmware files quite often contain sections that are filled with just NUL bytes, this way we hoped to determine the XOR value of a NUL byte (at each offset in the key). Both of these methods resulted in almost the same key. XORing the entire file with these keys did not result in a readable file.

Then we tried using subtraction instead of a XOR, which also did not produce a readable file. But there were tiny fragments that were correct, small bits of readable text, or line endings that line up correctly to the end of a string. But when we tried to start from those and guess the characters before or after it, we found that this would corrupt a small fragment a block at a different place in the file. So, it clearly wasn't just adding/subtracting either.

Our next guess was a combination of a addition/subtraction and a XOR. This would mean we were looking for two 256-byte keys. The small correctly decrypted fragments are actually logical for this obfuscation method.

#### Mathematical background

We can explain the occurrence of correctly decrypted bytes for our subtraction attempt mathematically, but feel free to skip this section if you are not interested in that.

Suppose the encryption is applied as (all of this per byte, so modulo 256):

```
ciphertext = (plaintext ^ b) + a
```

Then the ciphertext for a zero byte is just (b ^ 0) + a = b + a. When we subtract this value, we end up with:

```
subtracted = (plaintext ^ b) + a - (b + a)
           = (plaintext ^ b) - b
```

Now we observed that this would end up sometimes equal to plaintext again. When exactly does that happen? Well, for two numbers that do not share any bits (x & y = 0), addition does not trigger any carries, so addition and XOR are equal!

```
x & y = 0 ⇒ x ^ y = x + y
```

So, if plaintext & b == 0, then:

```
subtracted = (plaintext ^ b) - b
           = (plaintext + b) - b = plaintext
```

Thus, at each offset in the 256-byte block, all values that do not share any bits with the corresponding `b` value give the original value back if you subtract the "encrypted" value for zero. For numbers that do share some bits, the difference depends on how many carries the addition/subtraction triggers, which also explained why it was quite common to see a value that was off by 2 (or a different power of 2). For example, the screenshot above shows a number of line endings that are 0b 0a or 0d 06, instead of 0d 0a.

#### Decrypting

As we now had to look for two values per index, a simple frequency analysis wouldn't be enough to recover the values. We could just have tried all 256 * 256 = 65536 options, but as we weren't sure of how to recognize the correct decryption (it was probably not an ELF file), we weren't sure of how to see which of the 65536 files was the right one.

So instead, we started out with our file based on the subtraction of the zero value and started fixing the string literals we saw where we could guess some of the other parts of it, similar to how we filled in the S3 URLs. Each time we made some fixes, we would run a script that would create a new equation for that offset, until at some point we would have a definite solution. Once we have a definite solution, we could fill in more characters of the file, revealing other strings, and so forth. We continued this process until we had found the right values for all 256 offsets.

Many strings can be recognized quite easily. For example, the implementation contains mbedTLS, so strings related to TLS cipher suites and X.509 certificates can be completed quite easily. Longer sentences are also quite easy to fill in by guessing what the message is, although some could be tricky, like not knowing if a string starts with a lower- or uppercase letter and there were quite a few typos in internal debug messages that could mess things up.

All in all, it took us about 2 days to fill in this weird crossword puzzle. In hindsight, finding the right heuristic to determine which of the the 65536 possible decryptions was the most likely correct one might have been faster.

If you want to research an Autel firmware file yourself, we have published our decryption script here:

https://gist.github.com/sector7-nl/3fc815cd2497817ad461bfbd393294cb

## Looking for vulnerabilities

With the firmware files decrypted, we could start looking for vulnerabilities. We had already determined that the charger had no open TCP ports and our packet capture showed only outgoing connections using TLS. Therefore, we decided to focus on Bluetooth instead of the IP attack surface.

### BLE authentication (CVE-2024-23958)

Bluetooth Low Energy (BLE) on this charger is handled by an ESP32 running the ESP-AT firmware. This firmware allows WiFi and BLE to be used by sending commands to the ESP32 over serial. For WiFi, this handles everything WiFi and TCP/IP related on the ESP32, allowing the other side to issue commands like "connect over TCP to host:port". For BLE, commands can be used to start advertising, disconnect a device, etc. The main controller does reassemble BLE packets, to allow payloads larger than the BLE maximum ATT payload size (~500 bytes) to be sent.

To provision the charger, the user needs to use the Autel app to scan a QR code from the manual, which contains the serial number and an 8 digit code. Then, the app submits this information to an Autel server, which gives back an authentication token. This also links the charger to the user's Autel account.

When connecting over BLE to the charger, the device needs to perform a handshake where both the charger and the app pick some random numbers and then a SHA256 hash is calculated. The app hashes the authentication token it has received with the random numbers, but the charger actually computes this authentication token based on a 6 digit token stored on the charger (this is different from the 8 digit token from the manual) and its serial number.

The charger compares the received hash with its computed hash, if they are equal the user is authenticated. If it doesn't match, it goes through the same hash calculation a second time, but instead of using its 6-digit token to compute the (charger specific) authentication token, it uses a hard-coded authentication token stored in the firmware. We are not quite sure what this process is meant for, but the log message when this happens is "authbd succ", so this might be an intentional "backdoor". By extracting that token from the firmware we could authenticate to any charger without knowing the 8 digit code from the manual. Only being in BLE range is enough to get an authenticated connection.

```
void __fastcall authRequest(char *authMsgData, __int16 authMsgLen)
{
  char *v4; // r4
  int *object; // r0
  void **v6; // r0
  unsigned __int8 i; // r5
  unsigned __int8 j; // r5
  unsigned __int8 k; // r0
  int v10; // r1
  int v11; // r0
  unsigned __int8 m; // r0
  unsigned __int8 n; // r5
  char v14; // r0
  char randomNumbers[12]; // [sp+4h] [bp-DCh] BYREF
  char reply[20]; // [sp+10h] [bp-D0h] BYREF
  unsigned __int8 cpAuthData[32]; // [sp+24h] [bp-BCh] BYREF
  unsigned __int8 appAuthData[32]; // [sp+44h] [bp-9Ch] BYREF
  int v19[8]; // [sp+64h] [bp-7Ch] BYREF
  char backdoorPasswordData[36]; // [sp+84h] [bp-5Ch] BYREF
  char passwordHashData[36]; // [sp+A8h] [bp-38h] BYREF

  qmemcpy(reply, (int *)"U\xAA\x11\x00\x00\x00\x00\x00\x00\x00\x01", sizeof(reply));
  qmemcpy(passwordHashData, (int *)&defaultPasswordData, sizeof(passwordHashData));
  qmemcpy(backdoorPasswordData, (int *)&defaultBackdoorPasswordData, sizeof(backdoorPasswordData));
  memset(randomNumbers, 0, sizeof(randomNumbers));
  bzero(appAuthData, 32);
  bzero(cpAuthData, 32);
  qmemcpy(v19, &dword_80ECCD0, sizeof(v19));
  v4 = malloc(101);
  memset(v4, 0, 101u);
  trace("AppAuthenRequest:\r\n");
  if ( authMsgData && authMsgLen == 32 )
  {
    log_msg("A_Ble_Bus", 2, 536, "auth msg\r\n");
    object = (int *)allocate_object(288);
    if ( object )
      dword_2001C2CC = (int)sub_8081E40(object, (char *)v19, 256u);
    else
      dword_2001C2CC = 0;
    memcpy(appAuthData, authMsgData, sizeof(appAuthData));
    get_auth_token(passwordHashData);
    sub_80822E6((unsigned __int8 *)v4, 100u);
    memcpy(randomNumbers, &appRandomNum, 4u);
    memcpy(&randomNumbers[4], &cpRandomNum, 4u);
    retrieveCpAuthData(randomNumbers, passwordHashData, (int)cpAuthData);
    if ( dword_2001C2CC )
    {
      v6 = sub_8081EFA((void **)dword_2001C2CC);
      sub_8014502((unsigned int)v6);
    }
    trace("-------------------------------------------------\r\n");
    trace("appAuthData and cpAuthData::\r\n");
    for ( i = 0; i < 0x20u; ++i )
      trace("0x%x ", appAuthData[i]);
    trace("\r\n");
    for ( j = 0; j < 0x20u; ++j )
      trace("0x%x ", cpAuthData[j]);
    trace("\r\n");
    trace("-------------------------------------------------\r\n");
    for ( k = 0; k < 0x20u; ++k )
    {
      if ( appAuthData[k] != cpAuthData[k] )
        reply[12] = 1;
    }
  }
  else
  {
    reply[12] = 2;
  }
  if ( reply[12] )
  {
    reply[12] = 0;
    retrieveCpAuthData(randomNumbers, backdoorPasswordData, (int)cpAuthData);
    for ( m = 0; m < 0x20u; ++m )
    {
      if ( appAuthData[m] != cpAuthData[m] )
        reply[12] = 1;
    }
    for ( n = 0; n < 0x20u; ++n )
      trace("0x%x ", cpAuthData[n]);
    trace("\r\n");
    if ( reply[12] )
    {
      set_ble_authenticated(0);
      log_msg("A_Ble_Bus", 2, 639, "auth failed, %s.\r\n", v4);
    }
    else
    {
      set_ble_authenticated(1);
      log_msg("A_Ble_Bus", 2, 634, "authbd succ\r\n");
    }
  }
  else
  {
    set_ble_authenticated(1);
    v11 = sub_801726E(dword_2001C5E0, v10);
    log_msg("A_Ble_Bus", 2, 605, "con:step4->authentication succ, %d\r\n", v11);
    dword_2001C5E0 = 0;
  }
  v14 = send_message(reply, 17u);
  if ( !v14 )
    v14 = ble_send_response(ble_connection, reply, 17u);
  if ( v14 )
    log_msg("A_Ble_Bus", 2, 654, "auth ret SD Succ\r\n");
  else
    log_msg("A_Ble_Bus", 2, 658, "auth ret SD Failed.\r\n");
  if ( !is_ble_authenticated() )
  {
    msleep(100);
    ble_disconnect(ble_connection);
  }
  free(v4);
}
```

### Buffer overflow #1 (CVE-2024-23959)

Once we have established an authenticated BLE connection, there are a number of different types of messages we can send. The firmware passes the messages to different functions depending on a 1-byte opcode and 1-byte subcode. Opcode number 3 (based on the long messages likely related to setting a number of parameters related to the actual charging process) contained a stack buffer overflow when called with subcode 0:

```
int __fastcall opcode_3(__int16 subcode, void *packet, unsigned __int16 packet_length)
{
  int result; // r0
  char v7; // r4
  unsigned int i; // r5
  char v9[4]; // [sp+8h] [bp-168h] BYREF
  char v10[28]; // [sp+Ch] [bp-164h] BYREF
  _DWORD v11[5]; // [sp+28h] [bp-148h] BYREF
  int v12[5]; // [sp+3Ch] [bp-134h] BYREF
  char to[60]; // [sp+50h] [bp-120h] BYREF
  char v14[68]; // [sp+8Ch] [bp-E4h] BYREF
  char value[140]; // [sp+D0h] [bp-A0h] BYREF

  bzero(to, 60);
  [...]
  if ( subcode )
  {
    [...]
  }
  else
  {
    qmemcpy(v12, (int *)&byte_80F4234, sizeof(v12));
    send_message(v12, 0x11u);
    memcpy(to, packet, packet_length);
    [...]
```

This handler reserves a 60-byte stack buffer to, while copying into that stack-allocated buffer a BLE packet that can be many times that in size (theoretically up to 65536 bytes). By writing more than 60+68+140 bytes, we are able to overwrite saved registers on the stack, including PC. As there are no stack cookies, ASLR or DEP to deal with here, exploiting this to gain arbitrary code execution took us only about half a day. The only potential source of randomness we had to deal with (although in truth we don't really know how random this actually was) is that the firmware runs multiple RTOS tasks, which means the stack of our current task might not be at a predictable address if the tasks may have been created in a different order due to a timing difference. So instead of hardcoding an address, we used a few ROP gadgets to dynamically obtain the stack address of our current task and then jumped to a bit of shellcode in our BLE packet on the stack.

Writing the right shellcode that would allow us to observe the result was a bit tricky. While we could observe the UART debug logs of the device, this wasn't working all of the time. The device was logging a lot at a high baud rate and sometimes it would log garbage for a while. Eventually we found out that the grounded looking mounting holes weren't actually grounded. (Yeah, discovering this took us longer than finding this vulnerability.)

With our UART properly grounded, we could now observe that our shellcode worked by printing a new custom message to UART.

### Buffer overflow #2 (CVE-2024-23967)

Once we had this exploit, we moved on to other targets, as we still had some other devices which we hadn't hacked yet. But the last few days before we had to leave for Tokyo, it was clear we weren't going to find anything new, so we went back to the Autel MaxiCharger to see if maybe we could find some more obscure bugs instead. In Pwn2Own, only the first successful attempt is guaranteed the full prize money for the given target, further attempts on the same target may get less. Additionally, if the bug is a duplicate with a bug used in an earlier attempt, the winnings decrease further. Therefore, it is a good idea to not pick the most obvious bugs, as those are more likely to collide with other entries.

The authentication bypass was seemingly unavoidable if we went for BLE, but for the buffer overflow we could use something a bit more subtle than a fully controlled memcpy call in a message handler, so we spent some time looking for something else.

The Autel MaxiCharger sets up two connections to the internet: one for OCPP, and one internally called "ACMP" (we assume meaning something like "Autel Cloud Management Protocol"). Just like OCPP, the ACMP connection uses JSON in websockets over HTTPS. While the OCPP URL was configurable from the app, the ACMP URL was not. Despite that, when directly sending BLE messages we could change it to any URL we wanted.

Once that connection was set up, we found that if we sent a message on the ACMP connection to the charger with the following structure:

```
{
    "act": "",
    "seq": "1234",
    "PL": {
        "msgId": "msgId",
        "msgData": [
            {
                "msgH": "10:1:1:1:0",
                "data": "<... data ...>"
            }
        ]
    }
}
```

The value for the data key would be base64-decode into a 1024-byte stack buffer without it validating the length. Again, overflowing into other data on the stack and allowing us to overwrite a saved return address.

```
char *__fastcall sub_808B254(void *a1, char *a2)
{
  [...]
  string v26; // [sp+8h] [bp-4C0h] BYREF
  string data; // [sp+24h] [bp-4A4h] BYREF
  string msgId; // [sp+40h] [bp-488h] BYREF
  string seq; // [sp+5Ch] [bp-46Ch] BYREF
  string act; // [sp+78h] [bp-450h] BYREF
  string v31; // [sp+94h] [bp-434h] BYREF
  char decoded[1024]; // [sp+B0h] [bp-418h] BYREF

  [...]
  v11 = obtain_values_json((int)a1, a2, &act, &seq, &msgId, &data);
  if ( string_compare(&act, "Reboot") )
  {
    [...]
  }
  if ( v11 >= 1 )
  {
    strData = to_cstring(&data);
    trace("strData:%s", strData);
    memset(decoded, 0, sizeof(decoded));
    strData_1 = to_cstring(&data);
    data_base64_decode(strData_1, decoded);
    ...
```

We liked this bug more, because it was a lot less obvious: it doesn't call memcpy, it's not immediately clear that the configured ACMP URL can be changed and it requires combining BLE and an outgoing connection to the internet. We could leave the shellcode essentially the same. With some more room in the shellcode, we did implement writing a custom message to the LCD. While drawing our logo (or maybe even playing Doom) would have been even cooler, it looks like the images the charger shows are actually hard-coded in the LCD controller firmware. That sounded a bit too risky to update, so we left it at writing a message.

## Impact

As with all chargers we looked at, the connectivity functionality is separated from the controller managing the charging process. But in this charger, the charging controller can be updated with a firmware update. As these firmware files do not appear to be signed, on a compromised charger the charging controller could be reprogrammed to function outside of its safety parameters. This might make it possible to damage the charger or the car, or even, by hacking many chargers in the same area, this could have impact on the energy grid. This does depend on how much of the safety checks are still performed by hardware.

In addition, hacking a charger over Bluetooth could allow an attacker pivot to the configured WiFi- or Ethernet-network by proxying connections or stealing the WiFi-password.

But specifically for this charger, recall that this charger can be made public, allowing others to use a standard RFID charging card or tag to charge their car at this charger. In this case, we presume that the company that issued the charging tag pays Autel for the energy used, which will transfer that back to the owner (keeping a percentage as a service fee). But the issuer of the charging card has no information on how much energy was actually charged: there is (typically) no relationship between the car and the charging card issuer, so the car can't communicate to the issuer how much energy was added, only the charger reports to its cloud server how much has been charged. So by hacking a charger (potentially even your own), it would be possible to make it report any amount of energy. This could be used to defraud whoever charges their car at a public charger by reporting a lot more energy than was actually charged.

The public charging functionality means the charger essentially becomes "trusted" hardware for receiving payments. While ATMs and payment terminals have implemented a lot of security measures to defeat attacks (even against people with physical access to the hardware), this charger has trivial vulnerabilities, a backdoor in the authentication functionality and accessible UART or other debug ports internally. That's pretty concerning.

It's unclear to us how widely used this feature currently is. It's mentioned prominently in the mobile app, but almost completely absent on the Autel website. We did find this comment on Reddit from an Autel representative:

> Autel Global here, I checked with a colleague about the specifics and the gist of it was it was planned but put on the back burner for two main reasons. 1) No immediate demand for the function due to things already said in this thread. 2) A little grey legal area where you could potentially be making money off other people and the legislation on that not being clear yet, and potentially illegal. So apologies here if you desired that function with the app. We're pretty receptive to new good ideas so if you have any feedback you can message our account here.

## Patches

According to the advisory from ZDI, the vulnerabilities have been addressed in version v1.35.00. We have had a quick look at the latest firmware and we believe these to be correctly addressed. The backdoor authentication token is gone and the buffer overflows were fixed by adding bounds checks.

## Conclusion

For our research on the Autel MaxiCharger, we spent a lot of time on non-research steps: getting the firmware files, deobfuscating the firmware files and getting a stable UART connection. But once we had those steps finished, finding the vulnerabilities and writing the exploits took only a few hours in total. We managed to find a bypass for the authentication functionality for BLE connections and two stack buffer overflows, for which we used the more subtle one to avoid getting a duplicate submission during the competition.

For the other writeups about Pwn2Own Automotive, see ChargePoint Home Flex and JuiceBox 40 Smart EV Charging Station with WiFi.

  Research → service CTA (category-driven)    Back link

← Back to Research Labs
