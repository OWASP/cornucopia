# CAPEC™ 318: IP 'ID' Echoed Byte-Order Probe

## Description

This OS fingerprinting probe tests to determine if the remote host echoes back the IP 'ID' value from the probe packet. An attacker sends a UDP datagram with an arbitrary IP 'ID' value to a closed port on the remote host to observe the manner in which this bit is echoed back in the ICMP error message. The identification field (ID) is typically utilized for reassembling a fragmented packet. Some operating systems or router firmware reverse the bit order of the ID field when echoing the IP Header portion of the original datagram within an ICMP error message.

Source: [CAPEC™ 318](https://capec.mitre.org/data/definitions/318.html)

