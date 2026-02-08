# CAPEC™ 71: Using Unicode Encoding to Bypass Validation Logic

## Description

An attacker may provide a Unicode string to a system component that is not Unicode aware and use that to circumvent the filter or cause the classifying mechanism to fail to properly understanding the request. That may allow the attacker to slip malicious data past the content filter and/or possibly cause the application to route the request incorrectly.

Source: [CAPEC™ 71](https://capec.mitre.org/data/definitions/71.html)

## Related ASVS Requirements

ASVS (5.0): [1.1.1](/taxonomy/asvs-5.0/01-encoding-and-sanitization/01-encoding-and-sanitization-architecture#V1.1.1), [1.1.2](/taxonomy/asvs-5.0/01-encoding-and-sanitization/01-encoding-and-sanitization-architecture#V1.1.2), [1.2.9](/taxonomy/asvs-5.0/01-encoding-and-sanitization/02-injection-prevention#V1.2.9), [2.1.1](/taxonomy/asvs-5.0/02-validation-and-business-logic/01-validation-and-business-logic-documentation#V2.1.1), [2.2.1](/taxonomy/asvs-5.0/02-validation-and-business-logic/02-input-validation#V2.2.1)
