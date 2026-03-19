# CAPEC™ 274: HTTP Verb Tampering

## Description

An attacker modifies the HTTP Verb (e.g. GET, PUT, TRACE, etc.) in order to bypass access restrictions. Some web environments allow administrators to restrict access based on the HTTP Verb used with requests. However, attackers can often provide a different HTTP Verb, or even provide a random string as a verb in order to bypass these protections. This allows the attacker to access data that should otherwise be protected.

Source: [CAPEC™ 274](https://capec.mitre.org/data/definitions/274.html)

