# CAPEC™ 290: Enumerate Mail Exchange (MX) Records

## Description

An adversary enumerates the MX records for a given via a DNS query. This type of information gathering returns the names of mail servers on the network. Mail servers are often not exposed to the Internet but are located within the DMZ of a network protected by a firewall. A side effect of this configuration is that enumerating the MX records for an organization my reveal the IP address of the firewall or possibly other internal systems. Attackers often resort to MX record enumeration when a DNS Zone Transfer is not possible.

Source: [CAPEC™ 290](https://capec.mitre.org/data/definitions/290.html)

