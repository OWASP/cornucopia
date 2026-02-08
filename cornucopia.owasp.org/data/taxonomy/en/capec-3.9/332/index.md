# CAPEC™ 332: ICMP IP 'ID' Field Error Message Probe

## Description

An adversary sends a UDP datagram having an assigned value to its internet identification field (ID) to a closed port on a target to observe the manner in which this bit is echoed back in the ICMP error message. This allows the attacker to construct a fingerprint of specific OS behaviors.

Source: [CAPEC™ 332](https://capec.mitre.org/data/definitions/332.html)

