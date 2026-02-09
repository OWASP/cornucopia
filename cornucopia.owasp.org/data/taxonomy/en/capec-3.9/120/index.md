# CAPEC™ 120: Double Encoding

## Description

The adversary utilizes a repeating of the encoding process for a set of characters (that is, character encoding a character encoding of a character) to obfuscate the payload of a particular request. This may allow the adversary to bypass filters that attempt to detect illegal characters or strings, such as those that might be used in traversal or injection attacks. Filters may be able to catch illegal encoded strings, but may not catch doubly encoded strings. For example, a dot (.), often used in path traversal attacks and therefore often blocked by filters, could be URL encoded as %2E. However, many filters recognize this encoding and would still block the request. In a double encoding, the % in the above URL encoding would be encoded again as %25, resulting in %252E which some filters might not catch, but which could still be interpreted as a dot (.) by interpreters on the target.

Source: [CAPEC™ 120](https://capec.mitre.org/data/definitions/120.html)

## Related ASVS Requirements

ASVS (5.0): [1.1.1](/taxonomy/asvs-5.0/01-encoding-and-sanitization/01-encoding-and-sanitization-architecture#V1.1.1), [1.1.2](/taxonomy/asvs-5.0/01-encoding-and-sanitization/01-encoding-and-sanitization-architecture#V1.1.2), [1.2.9](/taxonomy/asvs-5.0/01-encoding-and-sanitization/02-injection-prevention#V1.2.9), [16.4.1](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/04-log-protection#V16.4.1), [16.5.1](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/05-error-handling#V16.5.1), [2.1.1](/taxonomy/asvs-5.0/02-validation-and-business-logic/01-validation-and-business-logic-documentation#V2.1.1), [2.2.1](/taxonomy/asvs-5.0/02-validation-and-business-logic/02-input-validation#V2.2.1)
