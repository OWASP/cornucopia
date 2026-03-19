# CAPEC™ 636: Hiding Malicious Data or Code within Files

## Description

Files on various operating systems can have a complex format which allows for the storage of other data, in addition to its contents. Often this is metadata about the file, such as a cached thumbnail for an image file. Unless utilities are invoked in a particular way, this data is not visible during the normal use of the file. It is possible for an attacker to store malicious data or code using these facilities, which would be difficult to discover.

Source: [CAPEC™ 636](https://capec.mitre.org/data/definitions/636.html)

## Related ASVS Requirements

ASVS (5.0): [1.2.3](/taxonomy/asvs-5.0/01-encoding-and-sanitization/02-injection-prevention#V1.2.3), [16.3.3](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/03-security-events#V16.3.3), [16.3.4](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/03-security-events#V16.3.4), [5.1.1](/taxonomy/asvs-5.0/05-file-handling/01-file-handling-documentation#V5.1.1), [5.2.2](/taxonomy/asvs-5.0/05-file-handling/02-file-upload-and-content#V5.2.2), [5.3.1](/taxonomy/asvs-5.0/05-file-handling/03-file-storage#V5.3.1), [5.3.2](/taxonomy/asvs-5.0/05-file-handling/03-file-storage#V5.3.2), [5.4.1](/taxonomy/asvs-5.0/05-file-handling/04-file-download#V5.4.1), [5.4.2](/taxonomy/asvs-5.0/05-file-handling/04-file-download#V5.4.2), [5.4.3](/taxonomy/asvs-5.0/05-file-handling/04-file-download#V5.4.3)
