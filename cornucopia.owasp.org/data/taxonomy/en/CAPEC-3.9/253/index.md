# CAPEC™ 253: Remote Code Inclusion

## Description

The attacker forces an application to load arbitrary code files from a remote location. The attacker could use this to try to load old versions of library files that have known vulnerabilities, to load malicious files that the attacker placed on the remote machine, or to otherwise change the functionality of the targeted application in unexpected ways.

Source: [CAPEC™ 253](https://capec.mitre.org/data/definitions/253.html)

## Related ASVS Requirements

ASVS (5.0): [1.3.10](/taxonomy/asvs-5.0/01-encoding-and-sanitization/03-sanitization#V1.3.10), [1.3.11](/taxonomy/asvs-5.0/01-encoding-and-sanitization/03-sanitization#V1.3.11), [1.3.2](/taxonomy/asvs-5.0/01-encoding-and-sanitization/03-sanitization#V1.3.2), [1.3.3](/taxonomy/asvs-5.0/01-encoding-and-sanitization/03-sanitization#V1.3.3), [1.3.4](/taxonomy/asvs-5.0/01-encoding-and-sanitization/03-sanitization#V1.3.4), [1.3.5](/taxonomy/asvs-5.0/01-encoding-and-sanitization/03-sanitization#V1.3.5), [1.3.6](/taxonomy/asvs-5.0/01-encoding-and-sanitization/03-sanitization#V1.3.6), [1.3.7](/taxonomy/asvs-5.0/01-encoding-and-sanitization/03-sanitization#V1.3.7), [1.3.8](/taxonomy/asvs-5.0/01-encoding-and-sanitization/03-sanitization#V1.3.8), [1.5.3](/taxonomy/asvs-5.0/01-encoding-and-sanitization/05-safe-deserialization#V1.5.3), [16.3.3](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/03-security-events#V16.3.3), [16.3.4](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/03-security-events#V16.3.4), [16.5.1](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/05-error-handling#V16.5.1), [5.1.1](/taxonomy/asvs-5.0/05-file-handling/01-file-handling-documentation#V5.1.1), [5.2.2](/taxonomy/asvs-5.0/05-file-handling/02-file-upload-and-content#V5.2.2), [5.3.1](/taxonomy/asvs-5.0/05-file-handling/03-file-storage#V5.3.1), [5.3.2](/taxonomy/asvs-5.0/05-file-handling/03-file-storage#V5.3.2), [5.3.3](/taxonomy/asvs-5.0/05-file-handling/03-file-storage#V5.3.3), [5.4.3](/taxonomy/asvs-5.0/05-file-handling/04-file-download#V5.4.3)
