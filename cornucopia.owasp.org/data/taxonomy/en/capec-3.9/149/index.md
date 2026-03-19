# CAPEC™ 149: Explore for Predictable Temporary File Names

## Description

An attacker explores a target to identify the names and locations of predictable temporary files for the purpose of launching further attacks against the target. This involves analyzing naming conventions and storage locations of the temporary files created by a target application. If an attacker can predict the names of temporary files they can use this information to mount other attacks, such as information gathering and symlink attacks.

Source: [CAPEC™ 149](https://capec.mitre.org/data/definitions/149.html)

## Related ASVS Requirements

ASVS (5.0): [10.2.3](/taxonomy/asvs-5.0/10-oauth-and-oidc/02-oauth-client#V10.2.3), [13.2.2](/taxonomy/asvs-5.0/13-configuration/02-backend-communication-configuration#V13.2.2), [13.4.1](/taxonomy/asvs-5.0/13-configuration/04-unintended-information-leakage#V13.4.1), [13.4.3](/taxonomy/asvs-5.0/13-configuration/04-unintended-information-leakage#V13.4.3), [13.4.7](/taxonomy/asvs-5.0/13-configuration/04-unintended-information-leakage#V13.4.7), [15.2.3](/taxonomy/asvs-5.0/15-secure-coding-and-architecture/02-security-architecture-and-dependencies#V15.2.3), [16.3.2](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/03-security-events#V16.3.2), [8.1.1](/taxonomy/asvs-5.0/08-authorization/01-authorization-documentation#V8.1.1)
