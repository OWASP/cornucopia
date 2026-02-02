# CAPEC™ 445: Malicious Logic Insertion into Product Software via Configuration Management Manipulation

## Description

{'p': {'__prefix': 'xhtml', '__text': "An adversary exploits a configuration management system so that malicious logic is inserted into a software products build, update or deployed environment. If an adversary can control the elements included in a product's configuration management for build they can potentially replace, modify or insert code files containing malicious logic. If an adversary can control elements of a product's ongoing operational configuration management baseline they can potentially force clients receiving updates from the system to install insecure software when receiving updates from the server."}}

Source: [CAPEC™ 445](https://capec.mitre.org/data/definitions/445.html)

## Related ASVS Requirements

ASVS (5.0): [13.2.3](/taxonomy/asvs-5.0/13-configuration/02-backend-communication-configuration#V13.2.3), [13.3.1](/taxonomy/asvs-5.0/13-configuration/03-secret-management#V13.3.1), [13.3.2](/taxonomy/asvs-5.0/13-configuration/03-secret-management#V13.3.2), [13.3.3](/taxonomy/asvs-5.0/13-configuration/03-secret-management#V13.3.3), [13.3.4](/taxonomy/asvs-5.0/13-configuration/03-secret-management#V13.3.4), [15.1.1](/taxonomy/asvs-5.0/15-secure-coding-and-architecture/01-secure-coding-and-architecture-documentation#V15.1.1), [15.1.2](/taxonomy/asvs-5.0/15-secure-coding-and-architecture/01-secure-coding-and-architecture-documentation#V15.1.2), [15.2.1](/taxonomy/asvs-5.0/15-secure-coding-and-architecture/02-security-architecture-and-dependencies#V15.2.1), [15.2.4](/taxonomy/asvs-5.0/15-secure-coding-and-architecture/02-security-architecture-and-dependencies#V15.2.4), [15.2.5](/taxonomy/asvs-5.0/15-secure-coding-and-architecture/02-security-architecture-and-dependencies#V15.2.5), [16.3.4](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/03-security-events#V16.3.4)
