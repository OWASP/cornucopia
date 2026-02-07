# CAPEC™ 261: Fuzzing for garnering other adjacent user/sensitive data

## Description

An adversary who is authorized to send queries to a target sends variants of expected queries in the hope that these modified queries might return information (directly or indirectly through error logs) beyond what the expected set of queries should provide.

Source: [CAPEC™ 261](https://capec.mitre.org/data/definitions/261.html)

## Related ASVS Requirements

ASVS (5.0): [15.3.1](/taxonomy/asvs-5.0/15-secure-coding-and-architecture/03-defensive-coding#V15.3.1), [15.3.2](/taxonomy/asvs-5.0/15-secure-coding-and-architecture/03-defensive-coding#V15.3.2), [15.3.3](/taxonomy/asvs-5.0/15-secure-coding-and-architecture/03-defensive-coding#V15.3.3), [15.3.5](/taxonomy/asvs-5.0/15-secure-coding-and-architecture/03-defensive-coding#V15.3.5), [15.3.6](/taxonomy/asvs-5.0/15-secure-coding-and-architecture/03-defensive-coding#V15.3.6), [15.3.7](/taxonomy/asvs-5.0/15-secure-coding-and-architecture/03-defensive-coding#V15.3.7), [16.3.3](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/03-security-events#V16.3.3), [16.5.1](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/05-error-handling#V16.5.1)
