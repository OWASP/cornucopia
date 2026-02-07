# CAPEC™ 80: Using UTF-8 Encoding to Bypass Validation Logic

## Description

This attack is a specific variation on leveraging alternate encodings to bypass validation logic. This attack leverages the possibility to encode potentially harmful input in UTF-8 and submit it to applications not expecting or effective at validating this encoding standard making input filtering difficult. UTF-8 (8-bit UCS/Unicode Transformation Format) is a variable-length character encoding for Unicode. Legal UTF-8 characters are one to four bytes long. However, early version of the UTF-8 specification got some entries wrong (in some cases it permitted overlong characters). UTF-8 encoders are supposed to use the "shortest possible" encoding, but naive decoders may accept encodings that are longer than necessary. According to the RFC 3629, a particularly subtle form of this attack can be carried out against a parser which performs security-critical validity checks against the UTF-8 encoded form of its input, but interprets certain illegal octet sequences as characters.

Source: [CAPEC™ 80](https://capec.mitre.org/data/definitions/80.html)

## Related ASVS Requirements

ASVS (5.0): [1.1.1](/taxonomy/asvs-5.0/01-encoding-and-sanitization/01-encoding-and-sanitization-architecture#V1.1.1), [1.1.2](/taxonomy/asvs-5.0/01-encoding-and-sanitization/01-encoding-and-sanitization-architecture#V1.1.2), [1.2.9](/taxonomy/asvs-5.0/01-encoding-and-sanitization/02-injection-prevention#V1.2.9), [2.1.1](/taxonomy/asvs-5.0/02-validation-and-business-logic/01-validation-and-business-logic-documentation#V2.1.1), [2.2.1](/taxonomy/asvs-5.0/02-validation-and-business-logic/02-input-validation#V2.2.1)
