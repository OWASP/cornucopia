# CAPEC™ 299: TCP SYN Ping

## Description

An adversary uses TCP SYN packets as a means towards host discovery. Typical RFC 793 behavior specifies that when a TCP port is open, a host must respond to an incoming SYN "synchronize" packet by completing stage two of the 'three-way handshake' - by sending an SYN/ACK in response. When a port is closed, RFC 793 behavior is to respond with a RST "reset" packet. This behavior can be used to 'ping' a target to see if it is alive by sending a TCP SYN packet to a port and then looking for a RST or an ACK packet in response.

Source: [CAPEC™ 299](https://capec.mitre.org/data/definitions/299.html)

