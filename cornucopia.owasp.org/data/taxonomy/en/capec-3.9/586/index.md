# CAPEC™ 586: Object Injection

## Description

An adversary attempts to exploit an application by injecting additional, malicious content during its processing of serialized objects. Developers leverage serialization in order to convert data or state into a static, binary format for saving to disk or transferring over a network. These objects are then deserialized when needed to recover the data/state. By injecting a malformed object into a vulnerable application, an adversary can potentially compromise the application by manipulating the deserialization process. This can result in a number of unwanted outcomes, including remote code execution.

Source: [CAPEC™ 586](https://capec.mitre.org/data/definitions/586.html)

## Related ASVS Requirements

ASVS (5.0): [1.2.2](/taxonomy/asvs-5.0/01-encoding-and-sanitization/02-injection-prevention#V1.2.2), [1.3.2](/taxonomy/asvs-5.0/01-encoding-and-sanitization/03-sanitization#V1.3.2), [1.3.8](/taxonomy/asvs-5.0/01-encoding-and-sanitization/03-sanitization#V1.3.8), [16.3.3](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/03-security-events#V16.3.3), [2.1.1](/taxonomy/asvs-5.0/02-validation-and-business-logic/01-validation-and-business-logic-documentation#V2.1.1), [2.2.1](/taxonomy/asvs-5.0/02-validation-and-business-logic/02-input-validation#V2.2.1), [2.2.2](/taxonomy/asvs-5.0/02-validation-and-business-logic/02-input-validation#V2.2.2), [5.4.1](/taxonomy/asvs-5.0/05-file-handling/04-file-download#V5.4.1), [5.4.2](/taxonomy/asvs-5.0/05-file-handling/04-file-download#V5.4.2)
