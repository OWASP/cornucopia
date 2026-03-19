# CAPEC™ 487: ICMP Flood

## Description

An adversary may execute a flooding attack using the ICMP protocol with the intent to deny legitimate users access to a service by consuming the available network bandwidth. A typical attack involves a victim server receiving ICMP packets at a high rate from a wide range of source addresses. Additionally, due to the session-less nature of the ICMP protocol, the source of a packet is easily spoofed making it difficult to find the source of the attack.

Source: [CAPEC™ 487](https://capec.mitre.org/data/definitions/487.html)

