# CAPEC™ 64: Using Slashes and URL Encoding Combined to Bypass Validation Logic

## Description

This attack targets the encoding of the URL combined with the encoding of the slash characters. An attacker can take advantage of the multiple ways of encoding a URL and abuse the interpretation of the URL. A URL may contain special character that need special syntax handling in order to be interpreted. Special characters are represented using a percentage character followed by two digits representing the octet code of the original character (%HEX-CODE). For instance US-ASCII space character would be represented with %20. This is often referred as escaped ending or percent-encoding. Since the server decodes the URL from the requests, it may restrict the access to some URL paths by validating and filtering out the URL requests it received. An attacker will try to craft an URL with a sequence of special characters which once interpreted by the server will be equivalent to a forbidden URL. It can be difficult to protect against this attack since the URL can contain other format of encoding such as UTF-8 encoding, Unicode-encoding, etc.

Source: [CAPEC™ 64](https://capec.mitre.org/data/definitions/64.html)

## Related ASVS Requirements

ASVS (5.0): [1.1.1](/taxonomy/asvs-5.0/01-encoding-and-sanitization/01-encoding-and-sanitization-architecture#V1.1.1), [1.1.2](/taxonomy/asvs-5.0/01-encoding-and-sanitization/01-encoding-and-sanitization-architecture#V1.1.2), [1.2.2](/taxonomy/asvs-5.0/01-encoding-and-sanitization/02-injection-prevention#V1.2.2), [1.2.9](/taxonomy/asvs-5.0/01-encoding-and-sanitization/02-injection-prevention#V1.2.9), [1.5.3](/taxonomy/asvs-5.0/01-encoding-and-sanitization/05-safe-deserialization#V1.5.3), [16.3.3](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/03-security-events#V16.3.3), [2.1.1](/taxonomy/asvs-5.0/02-validation-and-business-logic/01-validation-and-business-logic-documentation#V2.1.1), [2.2.1](/taxonomy/asvs-5.0/02-validation-and-business-logic/02-input-validation#V2.2.1), [5.4.1](/taxonomy/asvs-5.0/05-file-handling/04-file-download#V5.4.1), [5.4.2](/taxonomy/asvs-5.0/05-file-handling/04-file-download#V5.4.2)
