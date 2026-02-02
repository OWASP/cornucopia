# CAPEC™ 640: Inclusion of Code in Existing Process

## Description

The adversary takes advantage of a bug in an application failing to verify the integrity of the running process to execute arbitrary code in the address space of a separate live process. The adversary could use running code in the context of another process to try to access process's memory, system/network resources, etc. The goal of this attack is to evade detection defenses and escalate privileges by masking the malicious code under an existing legitimate process. Examples of approaches include but not limited to: dynamic-link library (DLL) injection, portable executable injection, thread execution hijacking, ptrace system calls, VDSO hijacking, function hooking, reflective code loading, and more.

Source: [CAPEC™ 640](https://capec.mitre.org/data/definitions/640.html)

