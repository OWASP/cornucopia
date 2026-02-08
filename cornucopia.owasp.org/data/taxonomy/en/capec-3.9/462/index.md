# CAPEC™ 462: Cross-Domain Search Timing

## Description

An attacker initiates cross domain HTTP / GET requests and times the server responses. The timing of these responses may leak important information on what is happening on the server. Browser's same origin policy prevents the attacker from directly reading the server responses (in the absence of any other weaknesses), but does not prevent the attacker from timing the responses to requests that the attacker issued cross domain.

Source: [CAPEC™ 462](https://capec.mitre.org/data/definitions/462.html)

