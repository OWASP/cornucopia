# CAPEC™ 598: DNS Spoofing

## Description

An adversary sends a malicious ("NXDOMAIN" ("No such domain") code, or DNS A record) response to a target's route request before a legitimate resolver can. This technique requires an On-path or In-path device that can monitor and respond to the target's DNS requests. This attack differs from BGP Tampering in that it directly responds to requests made by the target instead of polluting the routing the target's infrastructure uses.

Source: [CAPEC™ 598](https://capec.mitre.org/data/definitions/598.html)

