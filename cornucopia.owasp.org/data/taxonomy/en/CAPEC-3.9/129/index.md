# CAPEC™ 129: Pointer Manipulation

## Description

This attack pattern involves an adversary manipulating a pointer within a target application resulting in the application accessing an unintended memory location. This can result in the crashing of the application or, for certain pointer values, access to data that would not normally be possible or the execution of arbitrary code. Since pointers are simply integer variables, Integer Attacks may often be used in Pointer Attacks.

Source: [CAPEC™ 129](https://capec.mitre.org/data/definitions/129.html)

## Related ASVS Requirements

ASVS (5.0): [1.4.1](/taxonomy/asvs-5.0/01-encoding-and-sanitization/04-memory-string-and-unmanaged-code#V1.4.1), [1.4.2](/taxonomy/asvs-5.0/01-encoding-and-sanitization/04-memory-string-and-unmanaged-code#V1.4.2), [1.4.3](/taxonomy/asvs-5.0/01-encoding-and-sanitization/04-memory-string-and-unmanaged-code#V1.4.3), [16.5.2](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/05-error-handling#V16.5.2), [16.5.3](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/05-error-handling#V16.5.3)
