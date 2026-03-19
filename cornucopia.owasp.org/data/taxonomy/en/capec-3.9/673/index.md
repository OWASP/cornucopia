# CAPEC™ 673: Developer Signing Maliciously Altered Software

## Description

{'p': [{'__prefix': 'xhtml', '__text': 'Software produced by a reputable developer is clandestinely infected with malicious code and then digitally signed by the unsuspecting developer, where the software has been altered via a compromised software development or build process prior to being signed. The receiver or user of the software has no reason to believe that it is anything but legitimate and proceeds to deploy it to organizational systems.'}, {'__prefix': 'xhtml', '__text': 'This attack differs from CAPEC-206, since the developer is inadvertently signing malicious code they believe to be legitimate and which they are unware of any malicious modifications.'}]}

Source: [CAPEC™ 673](https://capec.mitre.org/data/definitions/673.html)

## Related ASVS Requirements

ASVS (5.0): [15.1.1](/taxonomy/asvs-5.0/15-secure-coding-and-architecture/01-secure-coding-and-architecture-documentation#V15.1.1), [15.1.2](/taxonomy/asvs-5.0/15-secure-coding-and-architecture/01-secure-coding-and-architecture-documentation#V15.1.2), [15.1.4](/taxonomy/asvs-5.0/15-secure-coding-and-architecture/01-secure-coding-and-architecture-documentation#V15.1.4), [15.1.5](/taxonomy/asvs-5.0/15-secure-coding-and-architecture/01-secure-coding-and-architecture-documentation#V15.1.5), [15.2.1](/taxonomy/asvs-5.0/15-secure-coding-and-architecture/02-security-architecture-and-dependencies#V15.2.1), [15.2.4](/taxonomy/asvs-5.0/15-secure-coding-and-architecture/02-security-architecture-and-dependencies#V15.2.4), [15.2.5](/taxonomy/asvs-5.0/15-secure-coding-and-architecture/02-security-architecture-and-dependencies#V15.2.5), [16.3.4](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/03-security-events#V16.3.4)
