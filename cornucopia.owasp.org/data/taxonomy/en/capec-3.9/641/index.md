# CAPEC™ 641: DLL Side-Loading

## Description

An adversary places a malicious version of a Dynamic-Link Library (DLL) in the Windows Side-by-Side (WinSxS) directory to trick the operating system into loading this malicious DLL instead of a legitimate DLL. Programs specify the location of the DLLs to load via the use of WinSxS manifests or DLL redirection and if they aren't used then Windows searches in a predefined set of directories to locate the file. If the applications improperly specify a required DLL or WinSxS manifests aren't explicit about the characteristics of the DLL to be loaded, they can be vulnerable to side-loading.

Source: [CAPEC™ 641](https://capec.mitre.org/data/definitions/641.html)

