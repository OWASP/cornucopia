# CAPEC™ 79: Using Slashes in Alternate Encoding

## Description

This attack targets the encoding of the Slash characters. An adversary would try to exploit common filtering problems related to the use of the slashes characters to gain access to resources on the target host. Directory-driven systems, such as file systems and databases, typically use the slash character to indicate traversal between directories or other container components. For murky historical reasons, PCs (and, as a result, Microsoft OSs) choose to use a backslash, whereas the UNIX world typically makes use of the forward slash. The schizophrenic result is that many MS-based systems are required to understand both forms of the slash. This gives the adversary many opportunities to discover and abuse a number of common filtering problems. The goal of this pattern is to discover server software that only applies filters to one version, but not the other.

Source: [CAPEC™ 79](https://capec.mitre.org/data/definitions/79.html)

## Related ASVS Requirements

ASVS (5.0): [1.1.1](/taxonomy/asvs-5.0/01-encoding-and-sanitization/01-encoding-and-sanitization-architecture#V1.1.1), [1.1.2](/taxonomy/asvs-5.0/01-encoding-and-sanitization/01-encoding-and-sanitization-architecture#V1.1.2), [1.2.9](/taxonomy/asvs-5.0/01-encoding-and-sanitization/02-injection-prevention#V1.2.9), [2.1.1](/taxonomy/asvs-5.0/02-validation-and-business-logic/01-validation-and-business-logic-documentation#V2.1.1), [2.2.1](/taxonomy/asvs-5.0/02-validation-and-business-logic/02-input-validation#V2.2.1)
