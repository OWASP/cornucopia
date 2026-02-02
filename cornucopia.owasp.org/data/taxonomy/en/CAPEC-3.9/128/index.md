# CAPEC™ 128: Integer Attacks

## Description

An attacker takes advantage of the structure of integer variables to cause these variables to assume values that are not expected by an application. For example, adding one to the largest positive integer in a signed integer variable results in a negative number. Negative numbers may be illegal in an application and the application may prevent an attacker from providing them directly, but the application may not consider that adding two positive numbers can create a negative number do to the structure of integer storage formats.

Source: [CAPEC™ 128](https://capec.mitre.org/data/definitions/128.html)

## Related ASVS Requirements

ASVS (5.0): [1.4.1](/taxonomy/asvs-5.0/01-encoding-and-sanitization/04-memory-string-and-unmanaged-code#V1.4.1), [1.4.2](/taxonomy/asvs-5.0/01-encoding-and-sanitization/04-memory-string-and-unmanaged-code#V1.4.2), [16.5.3](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/05-error-handling#V16.5.3)
