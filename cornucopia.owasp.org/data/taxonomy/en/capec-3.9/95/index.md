# CAPEC™ 95: WSDL Scanning

## Description

This attack targets the WSDL interface made available by a web service. The attacker may scan the WSDL interface to reveal sensitive information about invocation patterns, underlying technology implementations and associated vulnerabilities. This type of probing is carried out to perform more serious attacks (e.g. parameter tampering, malicious content injection, command injection, etc.). WSDL files provide detailed information about the services ports and bindings available to consumers. For instance, the attacker can submit special characters or malicious content to the Web service and can cause a denial of service condition or illegal access to database records. In addition, the attacker may try to guess other private methods by using the information provided in the WSDL files.

Source: [CAPEC™ 95](https://capec.mitre.org/data/definitions/95.html)

## Related ASVS Requirements

ASVS (5.0): [16.3.2](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/03-security-events#V16.3.2), [16.3.3](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/03-security-events#V16.3.3), [8.3.1](/taxonomy/asvs-5.0/08-authorization/03-operation-level-authorization#V8.3.1)
