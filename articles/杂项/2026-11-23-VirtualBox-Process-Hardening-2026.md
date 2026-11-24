---
title: "VirtualBox Process Hardening on Windows 2026 Edition: What’s a Single Bit Between Friends?"
source: "Google Project Zero"
url: https://projectzero.google/2026/11/virtualbox-process-hardening.html
published: 2026-11-23
fetched: 2026-11-24T10:00:10.706300+08:00
category: "杂项"
score: 6.4
keywords: ["kernel", "bypass"]
sha256: 68320e4e10e618188f4d4432adc5cde4c9ba95d47faac7c2c23fca43e18153c9
bytes: 22563
truncated: false
body_mode: fulltext
kind: practical
status: published
published_at: 2026-11-24T10:16:18.753705+08:00
---

# VirtualBox Process Hardening on Windows 2026 Edition: What’s a Single Bit Between Friends?

> 来源：Google Project Zero · 2026-11-23 · [原文](https://projectzero.google/2026/11/virtualbox-process-hardening.html)
> 自动抓取快照，仅供安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：Project Zero 对 VirtualBox 的“进程保护”机制做第二轮研究：2017 年找到三种绕过方式，如今厂商把保护统一收拢到“一个比特位”上，作者继续把这条访问控制链拆开，展示为什么单比特的判断仍然是可绕过的。
- **价值**：少见的“同一条攻击面隔几年再回看”的对比型研究，能直观看到缓解措施**看似收敛实则脆弱**的演进过程；VM 进程保护与宿主用户之间的边界，正好对应边缘设备上“虚拟化隔离能否被宿主用户打穿”的问题。
- **难度**：中高 —— 需要 Windows 内核对象、驱动访问控制与 COM 组件知识，不需要物理接触。

Back in 2017 I did some research into Oracle VirtualBox on Windows. Specifically I focussed on their mechanism to protect their VM processes from the user on the host. The protection was to gate who could open the kernel driver, which might allow for privilege escalation due to the way it was designed. At the time I found 3 ways of bypassing the protection, with an additional issue in COM’s runtime I reported in 2020. These issues were all written up in this post.

Fast forward to 2026 and I decided to look at VirtualBox again to see if much had changed. This time I found 3 new bypasses for protected processes, with an additional bug which was a broken fix for the 2020 bypass breaking due to changes in Windows. more In this blog post I want to focus on one specific issue CVE-2026-87268 which abused a feature of the .NET Framework which, when combined with the implementation of the DLL loader hooks implemented by VirtualBox, permitted a bypass of the checks and allowed me to load arbitrary code into the protected process. Let’s dig into the root cause of the issue in .NET first, before moving on to exploitation in VirtualBox.

### .NET Assembly Loading

The .NET Framework is interesting when it comes to bypassing process hardening as it supports loading assemblies from a memory buffer as long as you stick to only using managed code. This is obviously useful if the hardened process is maintained through verifying what DLLs can or cannot be loaded as it bypasses the traditional image mapping process. As the .NET runtime implementation is Microsoft signed, it’s usually permitted to load by any such checks.

The canonical way to load from a memory buffer is to use the Assembly::Load static method which accepts a byte array. This does require you to run some .NET code first, or find a confused deputy to do the work for you. I used this API method to bypass VirtualBox process hardening back in 2017, I was able to get to the API through the JScript script engine, culminating in me releasing the generic DotNetToJScript tool.

I’d always assumed this was the limit of bootstrapping arbitrary .NET from a memory buffer. If you tried to load a .NET assembly from a file it’d map it as an image section which would hit any DLL hardening checks and block an unsigned and untrusted binary from loading. However, in a “Doh” moment I realized I’d never verified this behavior to be true, thus I decided to take a look.

The most important function to mapping a .NET assembly into memory seems to be PEImageLayout::Map, which is roughly the following in the version 4 of CLR.DLL which implements the runtime:

```
PEImageLayout

*
PEImageLayout
::
Map
(
HANDLE

file
)

{

PEImageLayout
*

image

=

new

MappedImageLayout
(
file
);

if

(
!
image
->
Image
)

{

image

=

new

FlatImageLayout
(
file
);

}

if

(
image
->
Image
)

{

if

(
!
PEDecoder
::
CheckFormat
(
image
->
Image
))

ThrowWin32
(
ERROR_BAD_EXE_FORMAT
);

}

return

image
;

}
```

What is interesting is this code creates a MappedImageLayout object based on the file. If that fails it’ll fall back to using a different object, FlatImageLayout. The names kind of give away what they’re doing, but just to be sure let’s look at the implementations of the constructors:

```
void

MappedImageLayout
::
MappedImageLayout
(
HANDLE

file
)

{

HANDLE

mapping

=

CreateFileMapping
(
file
,

nullptr
,

SEC_IMAGE

|

PAGE_READONLY
);

if

(
mapping
)

{

this
->
Image

=

CLRMapViewOfFileEx
(
mapping
);

}

else

{

if

(
GetLastError
()

!=

ERROR_BAD_EXE_FORMAT
)

ThrowLastError
();

}

DWORD

policy

=

0
;

if

(
EEConfig
::
EnforceCodeIntegrity
()

||

(
SUCCEEDED
(
WldpGetLockdownPolicy
(
nullptr
,

&
policy
,

nullptr
))

&&

!
WLDP_LOCKDOWN_IS_OFF
(
policy
)

&&

!
WLDP_LOCKDOWN_IS_CONFIG_CI
(
policy
))

)

{

ThrowWin32
(
ERROR_BAD_EXE_FORMAT
);

}

// ...

}
```

The constructor for MappedImageLayout uses the CreateFileMapping API to convert the file handle into a section object. The code passes the SEC_IMAGE flag which instructs the kernel to assume the file is a PE executable and build an image section object including mapping in executable memory pages. Any protections which rely on verifying an image’s signature or location can be notified and take appropriate action. However if the CreateFileMapping call fails the code checks if the last error was not ERROR_BAD_EXE_FORMAT and throws ending the load entirely.

An additional check is made here to check if “Code Integrity” is enforced through the Windows Lockdown Policy (WLDP) APIs. This checks for the “Dynamic Code Security” code integrity policy being enabled or if a User Mode Code Integrity (UMCI) policy is enforced. If it is then an error is thrown ending the loading process. We’ll come back to this check when it becomes relevant.

Assuming the mapping fails with the ERROR_BAD_EXE_FORMAT error, then the loading process continues, creating a FlatImageLayout object instead:

```
void

FlatImageLayout
::
FlatImageLayout
(
HANDLE

file
)

{

HANDLE

mapping

=

CreateFileMapping
(
file
,

nullptr
,

PAGE_READONLY
);

if

(
mapping
)

{

this
->
Image

=

CLRMapViewOfFileEx
(
mapping
);

}

else

{

ThrowLastError
();

}

// ...

}

```

This constructor is simpler, it just calls CreateFileMapping without the SEC_IMAGE flag. Therefore the file is mapped into memory as a data only section. There’s no executable pages, but that doesn’t matter for .NET. The final check, back in the first code snippet verifies that the PE file is valid with a call to PEDecoder::CheckFormat, throwing if it’s not valid.

The take away from this is if we can get .NET to load a valid assembly file, but cause the first call to CreateFileMapping to fail with the ERROR_BAD_EXE_FORMAT error we can get it to execute the file from memory. Any protection code which is expecting to check the loaded image section will not see the load and untrusted arbitrary code would be executed.

Note this behavior only seems to work on .NET Framework v4, not the older .NET Framework such as v3.5 and v2. From what I can tell in the earlier frameworks, while this check can be bypassed in the same way and the FlatImageLayout object created, the runtime passes the assembly to the LoadLibrary API later in the loading process where it will fail to load. I didn’t spend much time checking if this was bypassable, as the older .NET Frameworks are no longer installed by default and aren’t even included as optional components in the latest versions of Windows 11. I also didn’t investigate the modern .NET runtimes, v5 and above for similar reasons.

### VirtualBox DLL Loading Hooks

Now that we have a potential route to bypassing a process hardening image checker using .NET let’s dig into how it was exploitable in VirtualBox. The previous blog post described how VirtualBox on Windows adds hooks to the DLL loader in order to prevent untrusted images from loading into the process. The important hook for our purposes is the one attached to the NtCreateSection system call which is called under the hood by CreateFileMapping to create the image section object. The following is the start of the hook function:

```
NTSTATUS

supR3HardenedMonitor_NtCreateSection
(
PHANDLE

phSection
,

ACCESS_MASK

fAccess
,

POBJECT_ATTRIBUTES

pObjAttribs
,

PLARGE_INTEGER

pcbSection
,

ULONG

fProtect
,

ULONG

fAttribs
,

HANDLE

hFile
)

{

bool

const

fExecProt

=

(
fProtect

&

(
PAGE_EXECUTE

|

PAGE_EXECUTE_READ

|

PAGE_EXECUTE_WRITECOPY

|

PAGE_EXECUTE_READWRITE
))

!=

0
;

if

(
hFile

!=

NULL

&&

hFile

!=

INVALID_HANDLE_VALUE
)

{

bool

const

fImage

=

RT_BOOL
(
fAttribs

&

(
SEC_IMAGE

|

SEC_PROTECTED_IMAGE
));

bool

const

fExecMap

=

RT_BOOL
(
fAccess

&

SECTION_MAP_EXECUTE
);

if

(
fImage

||

fExecMap

||

fExecProt
)

{

bool

fCallRealApi
;

NTSTATUS

rcNt

=

supR3HardenedScreenImage
(
hFile
,

fImage
,

true

/*fIgnoreArch*/
,

&
fAccess
,

&
fProtect
,

&
fCallRealApi
,

"NtCreateSection"
,

true

/*fAvoidWinVerifyTrust*/
,

NULL

/*pfQuiet*/
);

if

(
!
NT_SUCCESS
(
rcNt
))

return

rcNt
;

if

(
!
fCallRealApi
)

return

STATUS_TRUST_FAILURE
;

}

}

NTSTATUS

rcNtReal

=

g_pfnNtCreateSectionReal
(
phSection
,

fAccess
,

pObjAttribs
,

pcbSection
,

fProtect
,

fAttribs
,

hFile
);

// ...
```

If the NtCreateSection call requests an executable section, such as via the SEC_IMAGE flag, then the file is passed to the supR3HardenedScreenImage support API which will check if the PE file matches VirtualBox’s loading criteria, only calling the original NtCreateSection system call if that succeeds or the file is not being mapped as executable. Importantly the CreateFileMapping call in FlatImageLayout would not hit the checks as it doesn’t request an image or executable mapping.

In order for CreateFileMapping to set the ERROR_BAD_EXE_FORMAT last error, NtCreateSection needs to return STATUS_INVALID_IMAGE_FORMAT. We have two options for returning this status code, via the return code of supR3HardenedScreenImage or via the call to the original system call. Let’s see if the hardening code can even return this status code?

```
static

NTSTATUS

supR3HardenedScreenImageCalcStatus
(
int

rc
)

{

if

(
rc

==

VERR_LDR_ARCH_MISMATCH
)

return

STATUS_INVALID_IMAGE_FORMAT
;

return

STATUS_TRUST_FAILURE
;

}
```

It turns out that yes, the supR3HardenedScreenImage function can return this error code when mapping an internal error code to the status. Specifically if the error code is VERR_LDR_ARCH_MISMATCH then supR3HardenedScreenImage would return STATUS_INVALID_IMAGE_FORMAT. Therefore, what sets VERR_LDR_ARCH_MISMATCH?

This error is set in the PE parser implementation in VirtualBox, specifically in the rtldrPEOpen API. This is reachable via RTLdrOpenWithReader which is called by the supHardenedWinVerifyImageByHandle function which itself is called by supR3HardenedScreenImage.

To cut a long story short, due to the way the parser is called the VERR_LDR_ARCH_MISMATCH error is returned if the architecture of the PE file doesn’t match the host architecture and yet the PE file contains executable sections. This turns out to be perfect, when you compile a managed code only .NET assembly as AnyCPU, it generates a 32-bit x86 PE file so that it can be run on any system. This is for compatibility, a 64-bit (or ARM64) Windows system can map 32-bit PE files as images, but vice versa is not guaranteed. However, as shown below in the output from the dumpbin utility there’s executable code in the file as indicated by the size of code field in the optional header.

```
C:\>dumpbin /headers DotNetAssembly.dll
Microsoft (R) COFF/PE Dumper Version 14.44.35228.0
Copyright (C) Microsoft Corporation.  All rights reserved.

Dump of file DotNetAssembly.dll

PE signature found

File Type: DLL

FILE HEADER VALUES
             14C machine (x86)
               3 number of sections
        D62E716A time date stamp
               0 file pointer to symbol table
               0 number of symbols
              E0 size of optional header
            2022 characteristics
                   Executable
                   Application can handle large (>2GB) addresses
                   DLL

OPTIONAL HEADER VALUES

10B magic # (PE32)

           48.00 linker version

35CC00 size of code

             600 size of initialized data
               0 size of uninitialized data
```

Therefore to force the image hardening checks to return STATUS_INVALID_IMAGE_FORMAT all we need to do is compile any .NET assembly as AnyCPU and it’ll bypass VirtualBox’s image checks without messing with the file format. Crucially, because the .NET assembly DLL has not been modified, it remains a valid assembly which can be loaded by the FlatImageLayout class and thus get code execution.

The final piece of the puzzle is how to get the assembly DLL loaded into VirtualBox? It’s not sufficient to just cause the DLL to be loaded via LoadLibrary, we need .NET to load the file as an assembly file. This is pretty easy to achieve via COM hijacking. We can write a .NET COM registration to the current user’s hive for a class we know a hardened VirtualBox process will load. Then start a VM, that will load the COM object, which loads the .NET runtime which finally loads our untrusted assembly. You can find a full PoC in the issue tracker.

There is a small caveat, I haven’t mentioned the WLDP check yet. For VirtualBox this check is unlikely to matter, it will only apply if Windows has a configured code integrity policy which enables the Dynamic Code Security or the UMCI options. It’s possible a system could have such a policy which also grants VirtualBox’s own binaries to run but it seems unlikely.

VirtualBox fixed the issue by never returning STATUS_INVALID_IMAGE_FORMAT from the supR3HardenedScreenImageCalcStatus method. They also introduced some new code to make it more difficult to hijack COM objects by using an undocumented global option in COM to disable current user hive lookups.

### Attacking WDAC and Protected Processes

If you’ve read this far you might be wondering if the .NET behavior applies to Windows Code Integrity enforcement in general. For example, both Windows Defender Application Control (WDAC) and protected processes rely on the in-built code integrity mechanism to block untrusted DLLs from loading, are they vulnerable?

Well yes, assuming you can find a way of forcing .NET to use the FlatImageLayout option by getting NtCreateSection to return STATUS_INVALID_IMAGE_FORMAT. In VirtualBox this condition could be induced due to the behavior of the NtCreateSection hook on an unmodified .NET assembly file.

For the built-in code integrity case there’s no user-mode hook to abuse, you only have the call to NtCreateSection. We need to be able to induce the STATUS_INVALID_IMAGE_FORMAT status code from the system call without a) hitting the code integrity check first and b) the resulting image being invalid for .NET to load. The latter issue seemed to be most problematic, it’s likely that the signature validation would only run once the file was verified to be a valid PE image, but if we modify the file too much then .NET would refuse to load it.

We can write a simple test harness to call NtCreateSection first with the file, then if that fails with STATUS_INVALID_IMAGE_FORMAT call Assembly::Load passing the file path to load and see if that succeeds. From that you could write a fuzzer looking for a suitable modification, or just play with the file format manually.

I found that it was almost trivial to create the right conditions. If you clear the IMAGE_FILE_EXECUTABLE_IMAGE flag in the COFF File Header’s Characteristics flag field then NtCreateSection will fail to load the file as an image section, but it is ignored by .NET when loading the PE file. This single bit change is all you need to load an untrusted .NET assembly.

This is when the WLDP check becomes important. If an enterprise is deploying a WDAC code integrity policy they have probably enabled UMCI or the Dynamic Code Security option which blocks this attack. The Dynamic Code Security option isn’t enabled by default, and as it disables all dynamic code loading in .NET including the byte array version of Assembly::Load it might result in breaking important applications.

However, UMCI is one of the main reasons to deploy a WDAC policy as that restricts what user mode code is allowed to run. Still, I decided to try the attack against an installation of Windows 11 S Mode which does enable UMCI but doesn’t enable Dynamic Code Security.

To test it out I needed force .NET to load the assembly file. For Windows 11 S Mode you can run many of the built-in .NET utilities which take assemblies on the command line. For example, the Assembly Registration Tool can be used to load a .NET assembly and call any register and unregister functions defined by the developer. For example, compile the following code as a .NET assembly adding your own code to UnregisterFunction:

```
using

System
;

using

System.Runtime.InteropServices
;

public

class

ComClass

{

[
ComUnregisterFunction
]

public

static

void

UnregisterFunction
(
Type

t
)

{

//Insert code here.

}

}
```

Modify the resulting assembly to remove the IMAGE_FILE_EXECUTABLE_IMAGE flag. You don’t need to fix up anything else like the image checksum, a hex editor is all you need to change a single bit. Then you can pass the path to the modified assembly DLL to the RegAsm executable from the .NET runtime directory. Note, you should pass the /unregister option to run the UnregisterFunction, as unregistering doesn’t require administrator privileges.

```
C:\Windows\Microsoft.NET\Framework64\v4.0.30319\regasm.exe c:\path\to\assembly.dll /unregister
```

In theory this should have failed, but it didn’t. The modified assembly was loaded into memory and executed arbitrary code even with UMCI enabled. It turns out that the WLDP check is wrong, at least if only UMCI is enabled. It’s checking that the policy flags are not equal to the WLDP_LOCKDOWN_CONFIG_CI flag set, which represents:

```
WLDP_LOCKDOWN_DEFINED_FLAG |
   WLDP_LOCKDOWN_CONFIG_CI_FLAG |
   WLDP_LOCKDOWN_UMCIENFORCE_FLAG
```

Unfortunately this is exactly the flag setting returned by WldpGetLockdownPolicy on Windows 11 S Mode. Therefore the check passes and loading continues which then bypasses UMCI enforcement.

For protected processes on a default installation of Windows the WLDP check doesn’t even come into play. Realistically, .NET should also check for protected status but it doesn’t. It should also be pointed out that you can only exploit Protected Process Light (PPL) processes. The original Protected Process (PP) requires DLLs to have page hashes in their authenticode signature, which the .NET runtime DLLs lack. Thus .NET fails to load, and we can’t reach the vulnerable code.

For protected processes you can again abuse COM hijacking again. I found that WerSecureFault.exe loads a COM object during runtime, so by hijacking that registration and using the modified .NET DLL I could get arbitrary code as PPL at the TCB level without needing administrator privileges.

## Reporting to Microsoft

Once I’d worked out how to abuse this behavior I wondered if it needs to be submitted to Microsoft for fixing. According to the MSRC Security Servicing Criteria any PPL bypass is not in scope. WDAC is a supported security boundary, however to quote the security goal, “Only executable code, including scripts run by enlightened Windows script hosts, that conforms to the device’s policy can run…” This could be interpreted as, if there is a policy that can be enabled to prevent the code from running, then it’s not eligible for fixing.

I had assumed that the WLDP check was as designed and it was really the Dynamic Code Policy that was disabling this behavior. Therefore I decided not to report it, presenting it at the 2026 44Con conference instead.

However, after discussing the issue with some .NET developers they were clear that although enabling Dynamic Code Policy blocked the bypass that was by accident and not the intended purpose of the policy. They asked me to submit it to MSRC. Unfortunately by this point, late September 2026, I’d already publicly disclosed therefore it was treated as a zero day, CVE-2026-108398, and was fixed in October 2026, less than a month after reporting.

The fix was to correct the WLDP check to the following:

```
DWORD

policy

=

0
;

if

(
EEConfig
::
EnforceCodeIntegrity
()

||

(
SUCCEEDED
(
WldpGetLockdownPolicy
(
nullptr
,

&
policy
,

nullptr
))

&&

!
WLDP_LOCKDOWN_IS_OFF
(
policy
)

&&

WLDP_LOCKDOWN_IS_ENFORCE
(
policy
))

)

{

ThrowWin32
(
ERROR_BAD_EXE_FORMAT
);

}
```

The use of WLDP_LOCKDOWN_IS_ENFORCE specifically checks for UMCI being enabled and disabling loading from memory. However this wouldn’t change the behavior in PPL therefore that should still be bypassable.

## Conclusions

As with my previous research into VirtualBox’s process hardening on Windows I was able to reuse the bypass to exploit the built in code integrity features of Windows. In this case the .NET code tried to adhere to policy but the developers just made a mistake.

Unfortunately the behavior made me assume that it wouldn’t meet MSRC’s security servicing criteria and so the vulnerability wasn’t initially reported. While the criteria are useful, in cases like this where the expected behavior is unclear it can mean a real issue might not get reported. I’d like to thank the .NET team for getting a fix out so quickly.
