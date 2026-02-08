# CAPEC™ 194: Fake the Source of Data

## Description

An adversary takes advantage of improper authentication to provide data or services under a falsified identity. The purpose of using the falsified identity may be to prevent traceability of the provided data or to assume the rights granted to another individual. One of the simplest forms of this attack would be the creation of an email message with a modified "From" field in order to appear that the message was sent from someone other than the actual sender. The root of the attack (in this case the email system) fails to properly authenticate the source and this results in the reader incorrectly performing the instructed action. Results of the attack vary depending on the details of the attack, but common results include privilege escalation, obfuscation of other attacks, and data corruption/manipulation.

Source: [CAPEC™ 194](https://capec.mitre.org/data/definitions/194.html)

## Related ASVS Requirements

ASVS (5.0): [4.1.3](/taxonomy/asvs-5.0/04-api-and-web-service/01-generic-web-service-security#V4.1.3)
