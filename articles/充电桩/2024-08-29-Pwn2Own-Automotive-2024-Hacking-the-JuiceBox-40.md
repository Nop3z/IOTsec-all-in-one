---
title: "Pwn2Own Automotive 2024: Hacking the JuiceBox 40"
source: "Sector7"
url: https://defion.security/en/research-labs/pwn2own-automotive-2024-hacking-the-juicebox-40/
published: 2024-08-29
fetched: 2026-11-19T11:35:50.129835+08:00
category: "充电桩"
score: 6.0
keywords: ["pwn2own", "automotive"]
sha256: 9b54b6062b7a2e5c116b1f4f856bcf763139f9c1f3154cf4eaf8c731ee1c719e
bytes: 36299
truncated: false
body_mode: fulltext
kind: practical
status: published
published_at: 2026-11-19T11:44:34.056544+08:00
---

# Pwn2Own Automotive 2024: Hacking the JuiceBox 40

> 来源：Sector7 · 2024-08-29 · [原文](https://defion.security/en/research-labs/pwn2own-automotive-2024-hacking-the-juicebox-40/)
> 自动抓取快照，仅供安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：Pwn2Own Automotive 2024 对 **JuiceBox 40** 智能充电桩的攻破过程与利用细节。
- **价值**：与 Autel/ChargePoint 两篇对照阅读，能看清同代充电桩在云-端接口上的共性缺陷。
- **难度**：高：需要理解设备与厂商云之间的信任关系。

Breadcrumb    Meta

Pwn2Own 29 August 2024 · 29 min read

  Title

# Pwn2Own Automotive 2024: Hacking the JuiceBox 40

  Body

During Pwn2Own Automotive 2024 in Tokyo, we demonstrated exploits against three different EV chargers: the Autel MaxiCharger (MAXI US AC W12-L-4G), the ChargePoint Home Flex and the JuiceBox 40 Smart EV Charging Station with WiFi. This is our writeup of the research that we performed on the JuiceBox 40 Smart EV Charging Station. We discovered one vulnerability which has, since the event, been assigned CVE-2024-23938. During the competition, we were able to exploit CVE-2024-23938 to execute arbitrary code on the charger while requiring only network access for practical reasons at the event. However, being within Bluetooth range of the device is sufficient with a few extra steps.

## Background

We were initially uncertain of which targets made the most sense to focus on at Pwn2Own Automotive. EV chargers in particular were a category that none of us had looked into before. Therefore, we undertook an initial online investigation of the available targets and picked those that we deemed most promising.

As a result of that investigation, we were convinced that the JuiceBox 40 was one of the _juiciest_ targets at the event, at least until we had our hands on the rest of the devices we picked. You can check out our other writeups about the Autel MaxiCharger (to be published later) and the ChargePoint Home Flex to get a better idea for why we believe they ended up being _juicier_ than the JuiceBox 40 after all ;)

### Hardware

In terms of hardware, the JuiceBox 40 is relatively straightforward. There are a few main components:

- Silicon Labs WGM160PX22KGA3 application + WiFi processor
- Silicon Labs MGM13S12A Bluetooth/BLE processor
- Atmel ATMega328P MCU - which we suspect is the charging/safety controller
- Atmel M90E36A metering IC

These components were also summarized by ZDI in an exploratory blog post. We annotated one of the images from the post to label and highlight the components mentioned above:

We focused on the software hosted by the WGM160P processor as the main target for the competition and did not delve deeply into the MGM13S12A front. Nonetheless, it caught our interest and we believe that it is an interesting attack surface choice for future research.

## Reconnaissance

During our target assessment for the JuiceBox, we found posts on Reddit regarding issues with the charger and how to fix them using a "remote terminal" that was accessible to devices on the same network as the charger. Additionally, we found YouTube videos of owners documenting fixes and modifications that they have made to the device as well as other posts that contained photos of the internals of other models by the same vendor. For example, a post on iFixit about the JuiceBox EVSE/154411) that explains how to replace a relay in the device gave us hints as to what the main hardware components of the JuiceBox line-up might be. This photo from said article demonstrates the kind of useful information that we were looking for - a large shielded module labelled with "ZENTRI" and "AMW106":

In short, there was a lot of information to be found. And most interesting of all, there was apparently an open administrative interface that any other device on the network could interact with.

By the end of our little foray, we had the following main takeaways that we could use for further investigation:

- Older versions of the JuiceBox 40 were based on a WiFi module called the AMW106, which was manufactured by Zentri. These versions run ZentriOS.
- Newer versions of the JuiceBox 40 are perhaps based on a successor WiFi module, the WGM160P. These versions run a successor to ZentriOS, called Gecko OS.
- Development modules and kits for both the AMW106 and the WGM160P platforms were easily sourceable from many resellers.
- Both ZentriOS and Gecko OS have a plethora of features (e.g. the remote terminal feature) that seem to be accessible in a production setting on the JuiceBox 40.

Therefore, we pulled the trigger on the JuiceBox 40 as a target, ordered the charger and continued to investigate the threads we found while waiting for the device to arrive from the US.

## Getting closer to the firmware

We started perusing the documentation of both ZentriOS and Gecko OS with a focus on how the update procedure is implemented. Besides getting a better idea of how the platforms function, we also wanted to find a way to download a firmware image if possible. We learned quite a bit from the extensive documentation, with the main points being:

- Both operating systems consist of a core kernel and "built-in plugins" segment, in addition to an optional application that a developer could bundle with a specific build.
- Both systems had a fully-managed device auth{n,z} and updating mechanism in place, backed by Zentri Device Management Service (DMS).
- Both operating systems were designed to function both as a development platforms and add-on turn-key solutions. The latter means that the platform can be used as sort of a "connectivity" add-on in combination with a discrete application processor. This design decision explains the choice of exposing a lot of the features from the core kernel and associated plugins through a command line interface. By providing such a simple interface, the platform becomes easier to integrate with new or even existing designs.

We decided to explore Zentri DMS further, and quickly learned that it was possible to register an account and create test firmware bundles for specific platforms without having to have an actual device. We created a test WGM160P module bundle, and set its firmware version to be with the latest stable base image of Gecko OS which (4.2.7 at the time). Afterwards, we could see a listing of the "files" that constituted the firmware, as well as a JSON file specifying how these files were laid out in internal flash:

With these files in hand, we were able to hit the ground running with vulnerability discovery on the base OS much faster than we initially anticipated.

### Development setup

As a rule of thumb, it is always a good idea to have at least one backup device when diving into a piece of hardware. As Andrew "bunnie" Huang put it:

> My rule is to ideally acquire three: one to totally trash and take apart (so this can literally come from a trash heap); one to tweak and tune; and one to keep pristine, so you have a reference to check your results.

Realistically, we wanted to avoid having to buy a second charger to save (potentially) unnecessary costs. However, it would be quite handy to have a second unit to perform tests on in case something goes wrong. For most of the targets we went after doing so was not financially feasible, except for the JuiceBox 40 - _in a way_. There was another option which we opted for; that is purchasing a WGM160P Starter Kit (SLWSTK6121A). The kit came with a WGM160P development module and a base board that exposed multiple interfaces over a USB connection:

We were able to get it up and running quickly with Gecko OS Studio. In the process of setting it up, we downloaded the SDK targeting Gecko OS 4.2.7 which - of course - came with object files for the core kernel and plugins sections:

```
user@birdie 4.2.7-11064 % find . -name '*.a'
./tools/toolchains/gcc/arm/osx/libgcc.a
./hardware/platforms/gecko_os/wgm160p/libs/gcc/gecko_os_libraries/plugins_core/lib_network_protocols_websocket.a
./hardware/platforms/gecko_os/wgm160p/libs/gcc/gecko_os_libraries/plugins_core/lib_network_util_arp_lock.a
...
./hardware/platforms/gecko_os/wgm160p/libs/gcc/gecko_os_libraries/kernel_shared/gecko_os_kernel_chips_efx32_peripherals_crc.a
./hardware/platforms/gecko_os/wgm160p/libs/gcc/gecko_os_libraries/kernel_shared/gecko_os_kernel_core_dump.a
...
```

While we had already found the vulnerability that we based our exploit upon at that point, these files proved quite helpful while developing the exploit. We were able to use them to better understand how the the kernel, plugins and vendor apps are loaded in memory as well as which useful data structures could we reliably locate in memory during exploitation. In addition, having the development kit allowed us to much more easily develop and debug our exploitation steps using the enabled On-Chip Debugging (OCD) interface.

## Vulnerability discovery (CVE-2024-23938)

We started our discovery process by looking for vulnerabilities in the base images that we could acquire from the Zentri DMS platform, instead of waiting until the charger showed up. After all, we knew from the initial assessment that we undertook that a good part of the functionality provided by the base Gecko OS is likely also a part of the viable attack surface on the JuiceBox.

It took only a few days of analysis of the base image before we discovered the vulnerability that would form the basis of our Pwn2Own entry. It was a bug in the Gecko OS system message logging component, which we could trigger at will using the OS's remote terminal feature.

### Gecko OS system messages

Gecko OS, much like many embedded operating systems, provides the basic expected feature set of an operating system like hardware/software interfacing, scheduling and resource management. However, unlike many embedded OSes, Gecko OS offers many high level features because of its design as a turn-key solution for IoT applications. For example, there is a config web UI on top of an onboarding WiFi AP setup component that is used for onboarding the device onto a user's WiFi network. It also provides high level APIs for various application-level functions like HTTP, TLS as well as a TCP client and server implementations and many more which are built into the OS (or one of its subcomponents) in some fashion.

Handling many of these "high level" actions involves many moving parts, and naturally there are some points during these interactions when it makes sense to provide a status update. Said updates might be useful in many forms, including for example in a human readable format for a user or some other parseable text-based format for a secondary application processor. Seemingly for that purpose, Gecko OS contains a system message logging facility which writes customizable messages to whatever logging interface is in use (serial, network, etc.) when certain events occur. There are various message types (and their respective events) which are logged as indicated by the Gecko OS documentation for the `system.msg` variable:

Message NameDefault Valueinitialized[@tReady]stream_closed[@tClosed: @c]stream_failed[@tOpen failed]stream_opened[@tOpened: @c]stream_opening[@tOpening: @h]sleep[@tSleep]wlan_failed[@tJoin failed]wlan_joined[@tAssociated]wlan_joining[@tAssociating to @s]wlan_leave[@tDisassociated]softap_joined[@t@m associated]softap_leave[@t@m disassociated]ethernet_starting[@tEthernet Starting]ethernet_started[@tEthernet Started]ethernet_stopped[@tEthernet Stopped]ethernet_failed[@tEthernet Failed]

These messages can be specified by setting the Gecko OS system.msg variable with the specified message name and the desired message text. For example, to change the initialized message to log "Rise and shine" instead of the default message, one could issue this command:

```
set system.msg initialized "Rise and shine"
```

Additionally, system messages support a small subset of tags to add dynamic information to the logged message. One could think of these system messages as templates, where some parts of the message are string literals and other parts are placeholder variables. Some tags are supported by all message types, like the @t tag for which every instance is replaced with a timestamp. Meanwhile, some tags are only supported by a small selection of message types. For example, the @c tag can be used to print a stream handle, which only makes sense for the stream_closed and stream_opened messages. Here is a listing of the availability of the tags per the Gecko OS documentation:

TagDescriptionTag is available for ...@tTimestampCan be set for all messages, but displays a value only for ethernet messages.@sSSIDWLAN messages@cStream handlestream_closed, stream_opened@hConnection host/portstream_failed, stream_opening@mClient MAC Addresssoftap_joined, softap_leave

Building upon the above, say for example that we want to log a message indicating the connection host/port pair (if any), a static message and a timestamp while a stream is being opened for an HTTP request. To do so, we could issue the command:

```
set system.msg stream_opening "[@t] Connecting to to @h"
```

And so on. The main limitation is that a system message templates can be at most 32 bytes in length, including a terminating NUL byte. However, since tags denote dynamic data that is likely longer than the space the tag occupies, it is possible for the actual printed message to be much longer than 32 bytes.

### Out of bounds write

Initially, we were looking for "classic" vulnerabilities involving the usual suspects like memcpy calls with attacker controlled data and count; or snprintf calls where the return value is misused. The latter landed us in a routine that seemed to be responsible for applying dynamic data to system message templates and logging the result:

```
void print_system_msg(int msg_id, system_msg_arg *args)
{
  char cVar1;
  char **ppcVar2;
  int iVar3;
  byte *snrpintf_generic_arg;
  char *dst;
  char *template_;
  size_t n;
  uint snprintf_uint_arg;
  byte local_190;
  undefined scratch_buf_2 [35];
  byte scratch_buf_1 [132];
  char formatted_message_buffer [192];
  undefined message_buffer_end [4];
  system_message_entry *message_list;
  char *fmt;
  byte format_tag;

  message_list = (system_message_entry *)system_message_list;
  template_ = message_list[msg_id].message_format;
  if (message_list[msg_id].message_format[0] != '\0') {
    dst = formatted_message_buffer;
    while (cVar1 = *template_, cVar1 != '\0') {
      if (cVar1 == '@') {
        format_tag = template_[1];
        if (format_tag == 'm') {
          ppcVar2 = &args->value2;
          args = (system_msg_arg *)&args->value1;
          FUN_0002a018(*ppcVar2,dst);
          dst = dst + 0x11;
        }
        else if (format_tag < 'n') {
          if (format_tag == 'c') {
            snrpintf_generic_arg = (byte *)args->value2;
            args = (system_msg_arg *)&args->value1;
            fmt = "Running     : %u";
snprintf_into_dst:
            iVar3 = snprintf_signed_checked
                              (dst,(int)(message_buffer_end + -(int)dst),fmt + 0xe,
                               snrpintf_generic_arg);
            dst = dst + iVar3;
          }
          else if (format_tag == 'h') {
            snprintf_uint_arg = args->value1;
            iVar3 = snprintf_signed_checked
                              (dst,(int)(message_buffer_end + -(int)dst),"%s",args->value2);
            args = args + 1;
            dst = dst + iVar3;
            if (snprintf_uint_arg != 0) {
              fmt = dst + 1;
              *dst = ':';
              iVar3 = snprintf_signed_checked
                                (fmt,(int)(message_buffer_end + -(int)fmt),"%u",snprintf_uint_arg);
              dst = fmt + iVar3;
            }
          }
        }
        else {
          if (format_tag == 's') {
            n = args->value1;
            memcpy(scratch_buf_2,args->value2,n);
            local_190 = (byte)n;
            args = args + 1;
            escape_hex(scratch_buf_1,&local_190);
            snrpintf_generic_arg = scratch_buf_1;
            fmt = "Web browser : %s";
            goto snprintf_into_dst;
          }
          if ((format_tag == 't') &&
             (iVar3 = print_timestamp_to_string(scratch_buf_1,1), iVar3 == 0)) {
            memcpy(dst,scratch_buf_1,10);
            dst[0xb] = '|';
            dst[10] = ' ';
            dst[0xc] = ' ';
            memcpy(dst + 0xd,scratch_buf_1 + 0xb,8);
            dst[0x15] = ':';
            dst[0x16] = ' ';
            dst = dst + 0x17;
            *dst = '\0';
          }
        }
        template_ = template_ + 2;
      }
      else {
        *dst = cVar1;
        template_ = template_ + 1;
        dst = dst + 1;
      }
    }
    log_message(formatted_message_buffer,(int)dst - (int)formatted_message_buffer);
  }
  return;
}
```

To summarize what the routine does: it's invoked with a msg_id and a list of arguments that might apply to the message, depending on the type of system message. msg_id is simply an index into a global list of system message templates which is initialized to the default Gecko OS set and stored in a configuration segment in internal flash.

The function reserves a 192-byte stack buffer for the resulting message. Then, it loops over the characters in the template. For each @ character, it checks if it is one of the known template tags and fills it in. Other characters are copied into the result directly. The loop ends when it reaches the end of the template, it never checks how many characters have been written to the result buffer and if that's still in bounds.

There are a few things that are interesting about how this routine handles the different tags, so we will zoom into the relevant parts one by one and dissect what goes wrong. To start, let's look at the most glaring issue, specifically while handling the @t tag for timestamps:

```
if ((format_tag == 't') && (iVar3 = print_timestamp_to_string(scratch_buf_1,1), iVar3 == 0)) {
    memcpy(dst,scratch_buf_1,10);
    dst[0xb] = '|';
    dst[10] = ' ';
    dst[0xc] = ' ';
    memcpy(dst + 0xd,scratch_buf_1 + 0xb,8);
    dst[0x15] = ':';
    dst[0x16] = ' ';
    dst = dst + 0x17;
    *dst = '\0';
}
```

In the snippet above, the routine first writes the current time to a scratch buffer, then memcpys the contents a few times to the location addressed by dst while writing a bit of formatting characters. Afterwards, it simply increments dst by 17h/23d positions and writes a NUL byte. At no point does it check that it wrote past the limit of formatted_message_buffer.

Given that the messages can be 31 characters at most of usable text, and the @t tag uses 2 characters each, we can use at most 15 @t tags in a message. If we do that, and given that each @t tag produces 23 bytes of output, that means that we can write 23 * 15 = 345 bytes of text using just these 15 @t tags. 345 is quite a bit larger than 192, meaning that we can easily go out of bounds of the output stack-allocated buffer and into saved registers and higher stack frames.

Another peculiarity in the implementation of this routine is how the replacement values are passed in through the args parameter. This parameter is expected to be an array of values that will be used to replace placeholder tags other than @t in the message template. There is no correlation between the provided args array and the expected matching tag, so there is an implicit ordering of occurrence of arguments and tags specified in the template. Once an argument is used, the function moves on to the next element in the array and so on. This could be fine, because of the way that tags that are specific to a particular message type are not allowed in combination with any other tags besides @t. Nonetheless, there is a functional issue when multiple occurrences of the same tag are present. The caller does not provide multiple instances of the same argument as well to match the number of tags used in a template. This peculiarity is significant as it provided a key ingredient for our exploit technique, which we cover later on.

### Controlling saved PC

Looking at the stack layout, the buffer that the routine writes into is exactly 232 bytes away from the saved PC. With a bit of math, it's clear that all we have to do is use 10 @t tags resulting in 230 bytes followed by 2 literals before we start overwriting the saved PC. This allowed us to overwrite the PC with arbitrary data except for the literal @/40h and NUL bytes, since those indicate the end of the message and aren't written by the subroutine to formatted_message_buffer.

Normally, this might not be much of an issue, since we could perhaps string together a chain of ROP gadgets to make it work assuming that we can write enough data to the stack after the saved PC. However, we were limited to only 31 bytes and the 10 @t tags plus the 2 literals already used up 22, so we were only left with 9. This means we could fully overwrite PC and just a single additional saved register. This seemed highly restrictive and would require a very specific ROP gadget, and we also wanted to avoid having to tune the exploit to a specific build if we could avoid it.

### Pivoting to configuration section

After some more investigation, we came up with another path. Specifically, we realized that Gecko OS has one variable that allows us to write 16 arbitrary bytes at a very predictable location on flash (which is also memory mapped as an executable region). By changing the device's configuration encryption key, the system.security_key variable, we can store 16 bytes of shellcode in the configuration section in flash. The location of this section can either begin at 0x2000 or 0x5000, which switches on every change to the device configuration. It is likely that these switches are done to regulate the wear on flash, and we had to work around it for our final exploit but it is essentially a 50% chance of success on the first try and a 100% chance on the next so we decided that the odds are good enough.

However, we ran into another issue. In order to write a value of 0x2XXX or 0x5XXX to saved PC on the stack, the first two most significant bytes must be NUL. This was not the case for any of the code running on the device, as all of the executable code started at sections that were mapped at locations where the 2nd MSB is not NUL. Additionally, the function writes no NUL bytes while processing the template except for when the @t tag is used. We could theoretically use the @t tag to partially overwrite PC and set its 2nd MSB to NUL, but it would not be possible to set PC to be in the desired range using that tag either.

Despite this apparent dead end, we did not want to drop this vulnerability yet. So, we decided to take a bit of time to conjure up a usable exploitation path.

### Using every bit of machinery

After a few hours of going back and forth between the drawing board and the subroutine's functionality, we managed to come up with a way to increase our PC control. In order to do so, we had to use a number of side effects in the way that the subroutine handled different tags and some subtle side effects caused by the functions that it called.

#### Host/connection tag

What if we could somehow go out of bounds, write a NUL byte using the @t tag at a desired location, then move the dst pointer _back_? Then we can write an arbitrary literal followed by a NUL byte. But is that possible?

The answer turned out to be yes, by using a combination of the host/connection tag @h and the @t tag. Here's the code section for handling @h:

```
else if (format_tag == 'h') {
    snprintf_uint_arg = args->value1;
    iVar3 = snprintf_signed_checked
                        (dst,(int)(message_buffer_end + -(int)dst),"%s",args->value2);
    args = args + 1;
    dst = dst + iVar3;
    if (snprintf_uint_arg != 0) {
        fmt = dst + 1;
        *dst = ':';
        iVar3 = snprintf_signed_checked
                        (fmt,(int)(message_buffer_end + -(int)fmt),"%u",snprintf_uint_arg);
        dst = fmt + iVar3;
    }
}
```

Recall that dst is a pointer to the current position in the output string and message_buffer_end is right after the end of the ouptut string buffer. The code is straightforward, snprintf is called to write a string value to dst with a maximum length of message_buffer_end - dst. Afterwards, the return value of snprintf, which is - for a POSIX-compliant implementation - how many bytes it would have written if the buffer was large enough is added indiscriminately to dst. On its own, this already sounds like a vulnerability, what if the provided string args->value2 was much larger than the length of the buffer? And more importantly, what if we hit the condition where dst > message_buffer_end, as is the case if we abuse the vulnerability in handling the @t parameter?

It turns out that this implementation of snprintf is a bit different:

```
int snprintf_signed_checked(char *dst,int maxn,char *fmt,...)
{
  undefined4 *puVar1;
  int res;
  // ...

  puVar1 = (undefined4 *)DAT_20000984;
  if (maxn < 0) {
    res = -1;
    *puVar1 = 0x8b;
  }
  else {
    // ...
  }
  return res;
}
```

If the provided maxn argument is a negative number, then it returns -1 and sets some error code without performing any other actions. There is no error handling in print_system_msg for this condition! In fact, after the @h tag is processed in the case where dst is already out of bounds of the buffer, the final result is that dst is decremented! Additionally, if dst is still within bounds but the provided replacement value is larger than the buffer size, then this snprintf implementation behaves in the expected way and will return the number of bytes it would have written, meaning that dst will be incremented of bounds. The latter case is particularly interesting because it means that even if stack canaries were enabled, exploitation would still be possible.

### Putting it all together

We're finally there, a usable exploitation path that allows us to use parts of the configuration segment as shellcode storage. Here is the PoC that we came up with:

```
set system.msg stream_opening @t@t@t@t@h@t@h@hAB
```

where A and B are the lower bytes of the address of the next stage in the configuration segment. We would trigger the exploit chain by making an HTTP request using the http_head command with a "domain" name of a specific size:

```
http_head aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
```

Once the request is triggered, Gecko OS will emit a stream_opening system log message which eventually will make its way to print_system_msg. The changes in the stack frame of the routine as it processes the log message is shown in the diagram below:

## Exploitation

Armed with a vulnerability and an exploitation path, we set out to develop our exploit chain. It turned out that having the WGM160P devkit proved incredibly useful, because of a couple of reasons. Firstly, we were able to easily deploy and test different scenarios using Gecko OS Studio to our test module. Secondly, and perhaps most importantly, we were able to debug our exploit code at various stages by simply inspecting the side effects through SWD on the test module. The latter was something that could not be (easily) done with production modules, such as the one used in the JuiceBox, because those are locked down.

One of the main selling points of the platform is that the entire update cycle and device auth{n,z} parameters are managed by the vendor, who in turn allows application designers to manage these through Zentri DMS. However, that means that production units really do not need any form debuggability, making it a safe (and more secure) bet to simply disable all unnecessary interfaces from the get go.

Besides that, there were no mitigations to speak of to hinder exploit development, so getting control flow control was a straightforward task. What made the development process a bit more involved is the number of stages that we were forced to use as well as limitations to testing on the device itself.

### Testing on production

Regardless of the lack of JTAG/SWD on production modules, we needed to test our exploit chain against the device prior to the event to make sure that it actually works. Naturally, we ran into hiccups due to interactions between the deployed application code on the device and the OS which is not represented in our development setup. However, we were able to find a way to give us a bit of insight into what was happening so we could adjust as needed.

Gecko OS provides a mechanism for reporting operational faults, such as hard faults. If a fault handler is triggered, it stores the values of a few key registers to flash then reboots to a sane state. These faults can be listed by using the `faults_print` command:

```
0: Hard Fault Exception, PC:0x42424242 LR:0x0003F8AB HFSR:0x40000000 CFSR:0x00000001 MMFAR:0x00000000 BFAR:0x00000000
1: Hard Fault Exception, PC:0x000123A0 LR:0x00077C6B HFSR:0x40000000 CFSR:0x00008200 MMFAR:0x00000000 BFAR:0x400AE2C2
2: Hard Fault Exception, PC:0x000123A0 LR:0x00077C6B HFSR:0x40000000 CFSR:0x00008200 MMFAR:0x00000000 BFAR:0x400AE2C2
3: Hard Fault Exception, PC:0x000123A0 LR:0x00077C6B HFSR:0x40000000 CFSR:0x00008200 MMFAR:0x00000000 BFAR:0x400AE2C2
4: Hard Fault Exception, PC:0x000123A0 LR:0x00077C6B HFSR:0x40000000 CFSR:0x00008200 MMFAR:0x00000000 BFAR:0x400AE2C2
5: Hard Fault Exception, PC:0x000123A0 LR:0x00077C6B HFSR:0x40000000 CFSR:0x00008200 MMFAR:0x00000000 BFAR:0x400AE2C2
6: Hard Fault Exception, PC:0x000123A0 LR:0x00077C6B HFSR:0x40000000 CFSR:0x00008200 MMFAR:0x00000000 BFAR:0x400AE2C2
7: Hard Fault Exception, PC:0x000123A0 LR:0x00077C6B HFSR:0x40000000 CFSR:0x00008200 MMFAR:0x00000000 BFAR:0x400AE2C2
```

These listings provided just enough information for us to proceed with our exploit development on the JuiceBox. Well, that is until we ran into safe mode.

### "Rejuicing" the JuiceBox, or how do we leave Safe Mode?

Safe Mode is, in a nutshell, a recovery mechanism implemented by Gecko OS for when the system is consistently misbehaving. By default, it is triggered when 8 faults have occurred. When the system is in safe mode, most of the features are disabled including WiFi connectivity and there is a limited number of commands available through a serial interface.

Of course, while developing our exploit we ended up inadvertently dropping into safe mode. This could have been avoided if we had used the `faults_reset` command before the 8 fault limit had been reached, but we were not aware of safe mode at the time.

Nonetheless, we had to somehow exit safe mode and return to the unsafe^W normal mode of operation. One problem, however, is that the serial port used to interact with safe mode is by default hooked up to the Atmel ATMega328P charging controller as a communication channel between both processors. What that meant for us is that as long as the Atmel controller is running, we're unable to issue the necessary commands to exit safe mode on the WGM160P.

So we had to disable the Atmel chip, and in order to do so we went for the simple solution of holding its nRESET pin low. Thereby putting it in programming mode and keeping the serial port clear for us to issue the necessary commands:

### Staging the exploit

Our final exploit uses three stages in total:

- An initial 16-byte shellcode kickstarter which is stored in the configuration section as the system.security_key, which is responsible for triggering the next stage.
- A larger second stage shellcode block which is stored in the system messages themselves with the exception of the one we need for the exploit! These are stored in the kernel data memory region and are referenced by a static location that can be reached by the first stage. Additionally, the only limitation to shellcode in this stage is that it cannot contain neither NUL bytes nor @ signs as those may not match the allowed tags for a given message. This stage is responsible for reading and executing the final payload.
- Finally - the payload, which is saved as a file on the device's flash file system. This is done by simply using the remote terminal to download a file and store it to flash at the setup stage of the exploit chain.

Out of all the exploits which we had prepared before going to the event, this was by far the most complex and had the highest number of moving parts. So we spent a good amount of time making sure that it was as reliable as possible prior to our flight to Tokyo.

## Avoiding collisions?

One important point that we kept in mind is that we should aim for vulnerabilities that aren't so immediately obvious. We believed that this vulnerability was not as low hanging as other vulnerabilities might be. Our reasoning is that by focusing on the base OS, instead of aiming for vulnerabilities in the vendor-provided application code might net us vulnerabilities that other teams would not focus as much on.

Our attempt against the JuiceBox was the third out of a total of six attempts targeting the JuiceBox. One of the first two attempts failed, so we were hopeful that our odds of colliding had shrunk considerably.

But, Lady Luck had a different plan for us. It would so happen that the first successful attempt targeting the JuiceBox used the exact same vulnerability. This situation had triggered us to rethink our exploit for another target, the ChargePoint Home Flex, and we decided to spend a sleepless night in order to find a completely new set of vulnerabilities during the event. You can read more about that side quest in our writeup about the ChargePoint Home Flex.

## Impact

In terms of the design, the JuiceBox's charging controller is separated from the connectivity processor. Therefore, it is likely that damage to the charging process is minimal. However, we have not investigated the serial protocol between the connectivity processor and the charging controller sufficiently to rule out the potential for physical/electrical damage completely.

Additionally, the BLE service exposed by the Bluetooth module provides a secondary interface to the Gecko OS command line, which makes it possible to gain access to the credentials for the WiFi network that the device is onboarded to. This can be done by mounting a deauth attack, which will cause the JuiceBox to reboot and enter configuration mode, re-enabling the BLE service. Since the BLE connection requires no authentication, an attacker could use it to retrieve the credentials to the WiFi network and let the device reconnect. After which, it would be possible for them to exploit the charger to gain a stealthy foothold in the network or mount further attacks on other devices in the same network.

## Patch

Silicon Labs has published a security advisory regarding all the vulnerabilities in Gecko OS that were used in Pwn2Own Automotive. As of the time of writing of this article, the advisory simply states that no fix will be made available, quoting the advisory:

> Gecko OS is in end of life (EOL) status so no fix will be offered.

In theory, the use of a microcontroller combined with an RTOS that has all the essential functionality built-in, with an online platform that can be used to manage and OTA update the devices sounds great. However, the support period becomes limited to how long that platform vendor is willing to keep maintaining the platform. Switching to a different platform or applying patches to a proprietary OS is almost impossible for such devices. This example highlights one of the major issues with IoT security, which is that the support window for software could end much earlier than the expected lifespan of the hardware. And sometimes, as in this case, such an issue is not always due to the device vendor. It can also occur due to third-parties that constitute a critical part of the software supply chain for a piece of equipment.

## Conclusion

Our research on the JuiceBox took us through a few twists which resulted in an involved exploit chain that rested on one main vulnerability and a number of functionality abuse steps. Additionally, we had to work around limitations to testing on the device, for which we made full use of dev kits as a way to greatly simplify the exploit development stage. Finally, we were able to successfully demonstrate our exploit at the event while (unluckily) colliding with the one successful attempt targeting the device before ours.

For the other writeups about Pwn2Own Automotive, see ChargePoint Home Flex and Autel MaxiCharger (MAXI US AC W12-L-4G).

  Research → service CTA (category-driven)    Back link

← Back to Research Labs
