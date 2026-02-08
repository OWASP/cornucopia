# CAPEC™ 65: Sniff Application Code

## Description

An adversary passively sniffs network communications and captures application code bound for an authorized client. Once obtained, they can use it as-is, or through reverse-engineering glean sensitive information or exploit the trust relationship between the client and server. Such code may belong to a dynamic update to the client, a patch being applied to a client component or any such interaction where the client is authorized to communicate with the server.

Source: [CAPEC™ 65](https://capec.mitre.org/data/definitions/65.html)

## Related ASVS Requirements

ASVS (5.0): [12.1.1](/taxonomy/asvs-5.0/12-secure-communication/01-general-tls-security-guidance#V12.1.1), [12.1.2](/taxonomy/asvs-5.0/12-secure-communication/01-general-tls-security-guidance#V12.1.2), [12.1.3](/taxonomy/asvs-5.0/12-secure-communication/01-general-tls-security-guidance#V12.1.3), [12.1.4](/taxonomy/asvs-5.0/12-secure-communication/01-general-tls-security-guidance#V12.1.4), [12.1.5](/taxonomy/asvs-5.0/12-secure-communication/01-general-tls-security-guidance#V12.1.5), [12.2.1](/taxonomy/asvs-5.0/12-secure-communication/02-https-communication-with-external-facing-services#V12.2.1), [12.2.2](/taxonomy/asvs-5.0/12-secure-communication/02-https-communication-with-external-facing-services#V12.2.2), [12.3.1](/taxonomy/asvs-5.0/12-secure-communication/03-general-service-to-service-communication-security#V12.3.1), [12.3.2](/taxonomy/asvs-5.0/12-secure-communication/03-general-service-to-service-communication-security#V12.3.2), [12.3.3](/taxonomy/asvs-5.0/12-secure-communication/03-general-service-to-service-communication-security#V12.3.3), [12.3.4](/taxonomy/asvs-5.0/12-secure-communication/03-general-service-to-service-communication-security#V12.3.4), [12.3.5](/taxonomy/asvs-5.0/12-secure-communication/03-general-service-to-service-communication-security#V12.3.5)
