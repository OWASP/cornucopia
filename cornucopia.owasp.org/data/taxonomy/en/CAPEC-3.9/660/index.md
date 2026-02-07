# CAPEC™ 660: Root/Jailbreak Detection Evasion via Hooking

## Description

An adversary forces a non-restricted mobile application to load arbitrary code or code files, via Hooking, with the goal of evading Root/Jailbreak detection. Mobile device users often Root/Jailbreak their devices in order to gain administrative control over the mobile operating system and/or to install third-party mobile applications that are not provided by authorized application stores (e.g. Google Play Store and Apple App Store). Adversaries may further leverage these capabilities to escalate privileges or bypass access control on legitimate applications. Although many mobile applications check if a mobile device is Rooted/Jailbroken prior to authorized use of the application, adversaries may be able to "hook" code in order to circumvent these checks. Successfully evading Root/Jailbreak detection allows an adversary to execute administrative commands, obtain confidential data, impersonate legitimate users of the application, and more.

Source: [CAPEC™ 660](https://capec.mitre.org/data/definitions/660.html)

