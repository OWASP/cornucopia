# CAPEC™ 11: Cause Web Server Misclassification

## Description

An attack of this type exploits a Web server's decision to take action based on filename or file extension. Because different file types are handled by different server processes, misclassification may force the Web server to take unexpected action, or expected actions in an unexpected sequence. This may cause the server to exhaust resources, supply debug or system data to the attacker, or bind an attacker to a remote process.

Source: [CAPEC™ 11](https://capec.mitre.org/data/definitions/11.html)

## Related ASVS Requirements

ASVS (5.0): [13.4.1](/taxonomy/asvs-5.0/13-configuration/04-unintended-information-leakage#V13.4.1), [13.4.7](/taxonomy/asvs-5.0/13-configuration/04-unintended-information-leakage#V13.4.7), [16.3.2](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/03-security-events#V16.3.2), [16.3.3](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/03-security-events#V16.3.3)
