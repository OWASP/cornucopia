# CAPEC™ 285: ICMP Echo Request Ping

## Description

An adversary sends out an ICMP Type 8 Echo Request, commonly known as a 'Ping', in order to determine if a target system is responsive. If the request is not blocked by a firewall or ACL, the target host will respond with an ICMP Type 0 Echo Reply datagram. This type of exchange is usually referred to as a 'Ping' due to the Ping utility present in almost all operating systems. Ping, as commonly implemented, allows a user to test for alive hosts, measure round-trip time, and measure the percentage of packet loss.

Source: [CAPEC™ 285](https://capec.mitre.org/data/definitions/285.html)

