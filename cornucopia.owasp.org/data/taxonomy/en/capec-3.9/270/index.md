# CAPEC™ 270: Modification of Registry Run Keys

## Description

An adversary adds a new entry to the "run keys" in the Windows registry so that an application of their choosing is executed when a user logs in. In this way, the adversary can get their executable to operate and run on the target system with the authorized user's level of permissions. This attack is a good way for an adversary to run persistent spyware on a user's machine, such as a keylogger.

Source: [CAPEC™ 270](https://capec.mitre.org/data/definitions/270.html)

