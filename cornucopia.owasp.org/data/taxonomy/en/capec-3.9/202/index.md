# CAPEC™ 202: Create Malicious Client

## Description

An adversary creates a client application to interface with a target service where the client violates assumptions the service makes about clients. Services that have designated client applications (as opposed to services that use general client applications, such as IMAP or POP mail servers which can interact with any IMAP or POP client) may assume that the client will follow specific procedures.

Source: [CAPEC™ 202](https://capec.mitre.org/data/definitions/202.html)

## Related ASVS Requirements

ASVS (5.0): [2.2.2](/taxonomy/asvs-5.0/02-validation-and-business-logic/02-input-validation#V2.2.2), [3.1.1](/taxonomy/asvs-5.0/03-web-frontend-security/01-web-frontend-security-documentation#V3.1.1), [3.7.5](/taxonomy/asvs-5.0/03-web-frontend-security/07-other-browser-security-considerations#V3.7.5)
