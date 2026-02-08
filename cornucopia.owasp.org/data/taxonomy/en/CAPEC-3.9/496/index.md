# CAPEC™ 496: ICMP Fragmentation

## Description

An attacker may execute a ICMP Fragmentation attack against a target with the intention of consuming resources or causing a crash. The attacker crafts a large number of identical fragmented IP packets containing a portion of a fragmented ICMP message. The attacker these sends these messages to a target host which causes the host to become non-responsive. Another vector may be sending a fragmented ICMP message to a target host with incorrect sizes in the header which causes the host to hang.

Source: [CAPEC™ 496](https://capec.mitre.org/data/definitions/496.html)

