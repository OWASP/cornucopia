# CAPEC™ 546: Incomplete Data Deletion in a Multi-Tenant Environment

## Description

An adversary obtains unauthorized information due to insecure or incomplete data deletion in a multi-tenant environment. If a cloud provider fails to completely delete storage and data from former cloud tenants' systems/resources, once these resources are allocated to new, potentially malicious tenants, the latter can probe the provided resources for sensitive information still there.

Source: [CAPEC™ 546](https://capec.mitre.org/data/definitions/546.html)

## Related ASVS Requirements

ASVS (5.0): [15.2.3](/taxonomy/asvs-5.0/15-secure-coding-and-architecture/02-security-architecture-and-dependencies#V15.2.3)
