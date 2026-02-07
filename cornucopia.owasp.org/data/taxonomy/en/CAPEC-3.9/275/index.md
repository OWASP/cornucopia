# CAPEC™ 275: DNS Rebinding

## Description

An adversary serves content whose IP address is resolved by a DNS server that the adversary controls. After initial contact by a web browser (or similar client), the adversary changes the IP address to which its name resolves, to an address within the target organization that is not publicly accessible. This allows the web browser to examine this internal address on behalf of the adversary.

Source: [CAPEC™ 275](https://capec.mitre.org/data/definitions/275.html)

