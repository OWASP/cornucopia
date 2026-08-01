# CAPEC™ 331: ICMP IP Total Length Field Probe

## Description

An adversary sends a UDP packet to a closed port on the target machine to solicit an IP Header's total length field value within the echoed 'Port Unreachable" error message. This type of behavior is useful for building a signature-base of operating system responses, particularly when error messages contain other types of information that is useful identifying specific operating system responses.

Source: [CAPEC™ 331](https://capec.mitre.org/data/definitions/331.html)

