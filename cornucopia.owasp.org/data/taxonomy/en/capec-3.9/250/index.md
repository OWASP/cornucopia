# CAPEC™ 250: XML Injection

## Description

An attacker utilizes crafted XML user-controllable input to probe, attack, and inject data into the XML database, using techniques similar to SQL injection. The user-controllable input can allow for unauthorized viewing of data, bypassing authentication or the front-end application for direct XML database access, and possibly altering database information.

Source: [CAPEC™ 250](https://capec.mitre.org/data/definitions/250.html)

## Related ASVS Requirements

ASVS (5.0): [1.2.7](/taxonomy/asvs-5.0/01-encoding-and-sanitization/02-injection-prevention#V1.2.7), [1.3.4](/taxonomy/asvs-5.0/01-encoding-and-sanitization/03-sanitization#V1.3.4), [1.3.5](/taxonomy/asvs-5.0/01-encoding-and-sanitization/03-sanitization#V1.3.5), [1.3.7](/taxonomy/asvs-5.0/01-encoding-and-sanitization/03-sanitization#V1.3.7), [1.5.1](/taxonomy/asvs-5.0/01-encoding-and-sanitization/05-safe-deserialization#V1.5.1), [1.5.2](/taxonomy/asvs-5.0/01-encoding-and-sanitization/05-safe-deserialization#V1.5.2), [1.5.3](/taxonomy/asvs-5.0/01-encoding-and-sanitization/05-safe-deserialization#V1.5.3), [16.3.3](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/03-security-events#V16.3.3), [16.3.4](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/03-security-events#V16.3.4), [16.5.1](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/05-error-handling#V16.5.1)
