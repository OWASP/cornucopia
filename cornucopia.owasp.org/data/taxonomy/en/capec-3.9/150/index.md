# CAPEC™ 150: Collect Data from Common Resource Locations

## Description

An adversary exploits well-known locations for resources for the purposes of undermining the security of the target. In many, if not most systems, files and resources are organized in a default tree structure. This can be useful for adversaries because they often know where to look for resources or files that are necessary for attacks. Even when the precise location of a targeted resource may not be known, naming conventions may indicate a small area of the target machine's file tree where the resources are typically located. For example, configuration files are normally stored in the /etc director on Unix systems. Adversaries can take advantage of this to commit other types of attacks.

Source: [CAPEC™ 150](https://capec.mitre.org/data/definitions/150.html)

## Related ASVS Requirements

ASVS (5.0): [13.2.2](/taxonomy/asvs-5.0/13-configuration/02-backend-communication-configuration#V13.2.2), [13.4.1](/taxonomy/asvs-5.0/13-configuration/04-unintended-information-leakage#V13.4.1), [13.4.2](/taxonomy/asvs-5.0/13-configuration/04-unintended-information-leakage#V13.4.2), [13.4.3](/taxonomy/asvs-5.0/13-configuration/04-unintended-information-leakage#V13.4.3), [13.4.4](/taxonomy/asvs-5.0/13-configuration/04-unintended-information-leakage#V13.4.4), [13.4.5](/taxonomy/asvs-5.0/13-configuration/04-unintended-information-leakage#V13.4.5), [13.4.6](/taxonomy/asvs-5.0/13-configuration/04-unintended-information-leakage#V13.4.6), [13.4.7](/taxonomy/asvs-5.0/13-configuration/04-unintended-information-leakage#V13.4.7), [15.2.3](/taxonomy/asvs-5.0/15-secure-coding-and-architecture/02-security-architecture-and-dependencies#V15.2.3), [16.4.2](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/04-log-protection#V16.4.2)
