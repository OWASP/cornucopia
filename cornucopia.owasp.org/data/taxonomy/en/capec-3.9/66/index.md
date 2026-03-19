# CAPEC™ 66: SQL Injection

## Description

This attack exploits target software that constructs SQL statements based on user input. An attacker crafts input strings so that when the target software constructs SQL statements based on the input, the resulting SQL statement performs actions other than those the application intended. SQL Injection results from failure of the application to appropriately validate input.

Source: [CAPEC™ 66](https://capec.mitre.org/data/definitions/66.html)

## Related ASVS Requirements

ASVS (5.0): [1.2.4](/taxonomy/asvs-5.0/01-encoding-and-sanitization/02-injection-prevention#V1.2.4), [1.3.3](/taxonomy/asvs-5.0/01-encoding-and-sanitization/03-sanitization#V1.3.3), [1.5.1](/taxonomy/asvs-5.0/01-encoding-and-sanitization/05-safe-deserialization#V1.5.1), [1.5.3](/taxonomy/asvs-5.0/01-encoding-and-sanitization/05-safe-deserialization#V1.5.3), [16.3.3](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/03-security-events#V16.3.3), [16.3.4](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/03-security-events#V16.3.4), [16.5.1](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/05-error-handling#V16.5.1), [5.1.1](/taxonomy/asvs-5.0/05-file-handling/01-file-handling-documentation#V5.1.1), [5.2.2](/taxonomy/asvs-5.0/05-file-handling/02-file-upload-and-content#V5.2.2), [5.2.3](/taxonomy/asvs-5.0/05-file-handling/02-file-upload-and-content#V5.2.3), [5.2.5](/taxonomy/asvs-5.0/05-file-handling/02-file-upload-and-content#V5.2.5), [5.3.1](/taxonomy/asvs-5.0/05-file-handling/03-file-storage#V5.3.1), [5.3.2](/taxonomy/asvs-5.0/05-file-handling/03-file-storage#V5.3.2), [5.3.3](/taxonomy/asvs-5.0/05-file-handling/03-file-storage#V5.3.3), [5.4.1](/taxonomy/asvs-5.0/05-file-handling/04-file-download#V5.4.1), [5.4.2](/taxonomy/asvs-5.0/05-file-handling/04-file-download#V5.4.2), [5.4.3](/taxonomy/asvs-5.0/05-file-handling/04-file-download#V5.4.3)
