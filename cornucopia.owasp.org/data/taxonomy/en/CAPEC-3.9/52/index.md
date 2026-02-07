# CAPEC™ 52: Embedding NULL Bytes

## Description

An adversary embeds one or more null bytes in input to the target software. This attack relies on the usage of a null-valued byte as a string terminator in many environments. The goal is for certain components of the target software to stop processing the input when it encounters the null byte(s).

Source: [CAPEC™ 52](https://capec.mitre.org/data/definitions/52.html)

## Related ASVS Requirements

ASVS (5.0): [1.2.10](/taxonomy/asvs-5.0/01-encoding-and-sanitization/02-injection-prevention#V1.2.10), [2.1.1](/taxonomy/asvs-5.0/02-validation-and-business-logic/01-validation-and-business-logic-documentation#V2.1.1), [2.2.1](/taxonomy/asvs-5.0/02-validation-and-business-logic/02-input-validation#V2.2.1), [5.4.2](/taxonomy/asvs-5.0/05-file-handling/04-file-download#V5.4.2)
