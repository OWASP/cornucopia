# CAPEC™ 227: Sustained Client Engagement

## Description

An adversary attempts to deny legitimate users access to a resource by continually engaging a specific resource in an attempt to keep the resource tied up as long as possible. The adversary's primary goal is not to crash or flood the target, which would alert defenders; rather it is to repeatedly perform actions or abuse algorithmic flaws such that a given resource is tied up and not available to a legitimate user. By carefully crafting a requests that keep the resource engaged through what is seemingly benign requests, legitimate users are limited or completely denied access to the resource.

Source: [CAPEC™ 227](https://capec.mitre.org/data/definitions/227.html)

## Related ASVS Requirements

ASVS (5.0): [13.1.2](/taxonomy/asvs-5.0/13-configuration/01-configuration-documentation#V13.1.2), [13.1.3](/taxonomy/asvs-5.0/13-configuration/01-configuration-documentation#V13.1.3), [13.2.6](/taxonomy/asvs-5.0/13-configuration/02-backend-communication-configuration#V13.2.6), [15.4.3](/taxonomy/asvs-5.0/15-secure-coding-and-architecture/04-safe-concurrency#V15.4.3), [15.4.4](/taxonomy/asvs-5.0/15-secure-coding-and-architecture/04-safe-concurrency#V15.4.4), [16.3.3](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/03-security-events#V16.3.3), [16.5.2](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/05-error-handling#V16.5.2), [2.3.2](/taxonomy/asvs-5.0/02-validation-and-business-logic/03-business-logic-security#V2.3.2), [2.4.1](/taxonomy/asvs-5.0/02-validation-and-business-logic/04-anti-automation#V2.4.1), [2.4.2](/taxonomy/asvs-5.0/02-validation-and-business-logic/04-anti-automation#V2.4.2), [4.2.5](/taxonomy/asvs-5.0/04-api-and-web-service/02-http-message-structure-validation#V4.2.5)
