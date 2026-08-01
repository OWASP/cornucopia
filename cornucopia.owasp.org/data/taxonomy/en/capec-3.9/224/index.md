# CAPEC™ 224: Fingerprinting

## Description

An adversary compares output from a target system to known indicators that uniquely identify specific details about the target. Most commonly, fingerprinting is done to determine operating system and application versions. Fingerprinting can be done passively as well as actively. Fingerprinting by itself is not usually detrimental to the target. However, the information gathered through fingerprinting often enables an adversary to discover existing weaknesses in the target.

Source: [CAPEC™ 224](https://capec.mitre.org/data/definitions/224.html)

## Related ASVS Requirements

ASVS (5.0): [13.2.2](/taxonomy/asvs-5.0/13-configuration/02-backend-communication-configuration#V13.2.2), [13.4.2](/taxonomy/asvs-5.0/13-configuration/04-unintended-information-leakage#V13.4.2), [13.4.4](/taxonomy/asvs-5.0/13-configuration/04-unintended-information-leakage#V13.4.4), [13.4.5](/taxonomy/asvs-5.0/13-configuration/04-unintended-information-leakage#V13.4.5), [13.4.6](/taxonomy/asvs-5.0/13-configuration/04-unintended-information-leakage#V13.4.6), [13.4.7](/taxonomy/asvs-5.0/13-configuration/04-unintended-information-leakage#V13.4.7), [15.2.3](/taxonomy/asvs-5.0/15-secure-coding-and-architecture/02-security-architecture-and-dependencies#V15.2.3), [17.1.1](/taxonomy/asvs-5.0/17-webrtc/01-turn-server#V17.1.1), [4.3.2](/taxonomy/asvs-5.0/04-api-and-web-service/03-graphql#V4.3.2)
