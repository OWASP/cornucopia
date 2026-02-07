# CAPEC™ 319: IP (DF) 'Don't Fragment Bit' Echoing Probe

## Description

This OS fingerprinting probe tests to determine if the remote host echoes back the IP 'DF' (Don't Fragment) bit in a response packet. An attacker sends a UDP datagram with the DF bit set to a closed port on the remote host to observe whether the 'DF' bit is set in the response packet. Some operating systems will echo the bit in the ICMP error message while others will zero out the bit in the response packet.

Source: [CAPEC™ 319](https://capec.mitre.org/data/definitions/319.html)

