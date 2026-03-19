# CAPEC™ 40: Manipulating Writeable Terminal Devices

## Description

This attack exploits terminal devices that allow themselves to be written to by other users. The attacker sends command strings to the target terminal device hoping that the target user will hit enter and thereby execute the malicious command with their privileges. The attacker can send the results (such as copying /etc/passwd) to a known directory and collect once the attack has succeeded.

Source: [CAPEC™ 40](https://capec.mitre.org/data/definitions/40.html)

