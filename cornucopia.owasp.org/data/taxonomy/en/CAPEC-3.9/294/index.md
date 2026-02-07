# CAPEC™ 294: ICMP Address Mask Request

## Description

An adversary sends an ICMP Type 17 Address Mask Request to gather information about a target's networking configuration. ICMP Address Mask Requests are defined by RFC-950, "Internet Standard Subnetting Procedure." An Address Mask Request is an ICMP type 17 message that triggers a remote system to respond with a list of its related subnets, as well as its default gateway and broadcast address via an ICMP type 18 Address Mask Reply datagram. Gathering this type of information helps the adversary plan router-based attacks as well as denial-of-service attacks against the broadcast address.

Source: [CAPEC™ 294](https://capec.mitre.org/data/definitions/294.html)

