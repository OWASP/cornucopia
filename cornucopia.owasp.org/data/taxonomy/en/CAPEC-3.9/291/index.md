# CAPEC™ 291: DNS Zone Transfers

## Description

An attacker exploits a DNS misconfiguration that permits a ZONE transfer. Some external DNS servers will return a list of IP address and valid hostnames. Under certain conditions, it may even be possible to obtain Zone data about the organization's internal network. When successful the attacker learns valuable information about the topology of the target organization, including information about particular servers, their role within the IT structure, and possibly information about the operating systems running upon the network. This is configuration dependent behavior so it may also be required to search out multiple DNS servers while attempting to find one with ZONE transfers allowed.

Source: [CAPEC™ 291](https://capec.mitre.org/data/definitions/291.html)

