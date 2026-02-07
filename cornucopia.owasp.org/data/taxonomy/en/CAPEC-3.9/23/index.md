# CAPEC™ 23: File Content Injection

## Description

An adversary poisons files with a malicious payload (targeting the file systems accessible by the target software), which may be passed through by standard channels such as via email, and standard web content like PDF and multimedia files. The adversary exploits known vulnerabilities or handling routines in the target processes, in order to exploit the host's trust in executing remote content, including binary files.

Source: [CAPEC™ 23](https://capec.mitre.org/data/definitions/23.html)

## Related ASVS Requirements

ASVS (5.0): [1.3.4](/taxonomy/asvs-5.0/01-encoding-and-sanitization/03-sanitization#V1.3.4), [1.3.5](/taxonomy/asvs-5.0/01-encoding-and-sanitization/03-sanitization#V1.3.5), [1.3.6](/taxonomy/asvs-5.0/01-encoding-and-sanitization/03-sanitization#V1.3.6), [1.3.7](/taxonomy/asvs-5.0/01-encoding-and-sanitization/03-sanitization#V1.3.7), [1.5.1](/taxonomy/asvs-5.0/01-encoding-and-sanitization/05-safe-deserialization#V1.5.1), [1.5.3](/taxonomy/asvs-5.0/01-encoding-and-sanitization/05-safe-deserialization#V1.5.3), [16.3.3](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/03-security-events#V16.3.3), [16.3.4](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/03-security-events#V16.3.4), [16.5.1](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/05-error-handling#V16.5.1), [5.1.1](/taxonomy/asvs-5.0/05-file-handling/01-file-handling-documentation#V5.1.1), [5.2.2](/taxonomy/asvs-5.0/05-file-handling/02-file-upload-and-content#V5.2.2), [5.2.3](/taxonomy/asvs-5.0/05-file-handling/02-file-upload-and-content#V5.2.3), [5.2.5](/taxonomy/asvs-5.0/05-file-handling/02-file-upload-and-content#V5.2.5), [5.3.1](/taxonomy/asvs-5.0/05-file-handling/03-file-storage#V5.3.1), [5.3.2](/taxonomy/asvs-5.0/05-file-handling/03-file-storage#V5.3.2), [5.3.3](/taxonomy/asvs-5.0/05-file-handling/03-file-storage#V5.3.3), [5.4.1](/taxonomy/asvs-5.0/05-file-handling/04-file-download#V5.4.1), [5.4.2](/taxonomy/asvs-5.0/05-file-handling/04-file-download#V5.4.2), [5.4.3](/taxonomy/asvs-5.0/05-file-handling/04-file-download#V5.4.3)
