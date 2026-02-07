# CAPEC™ 83: XPath Injection

## Description

An attacker can craft special user-controllable input consisting of XPath expressions to inject the XML database and bypass authentication or glean information that they normally would not be able to. XPath Injection enables an attacker to talk directly to the XML database, thus bypassing the application completely. XPath Injection results from the failure of an application to properly sanitize input used as part of dynamic XPath expressions used to query an XML database.

Source: [CAPEC™ 83](https://capec.mitre.org/data/definitions/83.html)

## Related ASVS Requirements

ASVS (5.0): [1.2.7](/taxonomy/asvs-5.0/01-encoding-and-sanitization/02-injection-prevention#V1.2.7), [16.3.3](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/03-security-events#V16.3.3), [16.3.4](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/03-security-events#V16.3.4), [16.5.1](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/05-error-handling#V16.5.1)
