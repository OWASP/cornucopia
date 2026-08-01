# CAPEC™ 162: Manipulating Hidden Fields

## Description

An adversary exploits a weakness in the server's trust of client-side processing by modifying data on the client-side, such as price information, and then submitting this data to the server, which processes the modified data. For example, eShoplifting is a data manipulation attack against an on-line merchant during a purchasing transaction. The manipulation of price, discount or quantity fields in the transaction message allows the adversary to acquire items at a lower cost than the merchant intended. The adversary performs a normal purchasing transaction but edits hidden fields within the HTML form response that store price or other information to give themselves a better deal. The merchant then uses the modified pricing information in calculating the cost of the selected items.

Source: [CAPEC™ 162](https://capec.mitre.org/data/definitions/162.html)

## Related ASVS Requirements

ASVS (5.0): [11.2.1](/taxonomy/asvs-5.0/11-cryptography/02-secure-cryptography-implementation#V11.2.1), [11.3.2](/taxonomy/asvs-5.0/11-cryptography/03-encryption-algorithms#V11.3.2), [11.3.3](/taxonomy/asvs-5.0/11-cryptography/03-encryption-algorithms#V11.3.3), [11.4.1](/taxonomy/asvs-5.0/11-cryptography/04-hashing-and-hash-based-functions#V11.4.1), [15.3.3](/taxonomy/asvs-5.0/15-secure-coding-and-architecture/03-defensive-coding#V15.3.3), [15.3.7](/taxonomy/asvs-5.0/15-secure-coding-and-architecture/03-defensive-coding#V15.3.7), [16.3.2](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/03-security-events#V16.3.2), [16.3.3](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/03-security-events#V16.3.3), [2.2.2](/taxonomy/asvs-5.0/02-validation-and-business-logic/02-input-validation#V2.2.2), [2.3.1](/taxonomy/asvs-5.0/02-validation-and-business-logic/03-business-logic-security#V2.3.1), [2.3.4](/taxonomy/asvs-5.0/02-validation-and-business-logic/03-business-logic-security#V2.3.4), [2.3.5](/taxonomy/asvs-5.0/02-validation-and-business-logic/03-business-logic-security#V2.3.5), [8.3.1](/taxonomy/asvs-5.0/08-authorization/03-operation-level-authorization#V8.3.1)
