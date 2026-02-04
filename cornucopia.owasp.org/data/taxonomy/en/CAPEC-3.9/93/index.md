# CAPEC™ 93: Log Injection-Tampering-Forging

## Description

This attack targets the log files of the target host. The attacker injects, manipulates or forges malicious log entries in the log file, allowing them to mislead a log audit, cover traces of attack, or perform other malicious actions. The target host is not properly controlling log access. As a result tainted data is resulting in the log files leading to a failure in accountability, non-repudiation and incident forensics capability.

Source: [CAPEC™ 93](https://capec.mitre.org/data/definitions/93.html)

## Related ASVS Requirements

ASVS (5.0): [1.2.3](/taxonomy/asvs-5.0/01-encoding-and-sanitization/02-injection-prevention#V1.2.3), [1.2.4](/taxonomy/asvs-5.0/01-encoding-and-sanitization/02-injection-prevention#V1.2.4), [16.3.3](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/03-security-events#V16.3.3), [16.4.1](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/04-log-protection#V16.4.1), [16.5.1](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/05-error-handling#V16.5.1)
