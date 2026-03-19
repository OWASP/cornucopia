# CAPEC™ 292: Host Discovery

## Description

An adversary sends a probe to an IP address to determine if the host is alive. Host discovery is one of the earliest phases of network reconnaissance. The adversary usually starts with a range of IP addresses belonging to a target network and uses various methods to determine if a host is present at that IP address. Host discovery is usually referred to as 'Ping' scanning using a sonar analogy. The goal is to send a packet through to the IP address and solicit a response from the host. As such, a 'ping' can be virtually any crafted packet whatsoever, provided the adversary can identify a functional host based on its response. An attack of this nature is usually carried out with a 'ping sweep,' where a particular kind of ping is sent to a range of IP addresses.

Source: [CAPEC™ 292](https://capec.mitre.org/data/definitions/292.html)

