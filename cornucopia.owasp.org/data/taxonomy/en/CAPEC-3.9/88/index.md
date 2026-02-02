# CAPEC™ 88: OS Command Injection

## Description

In this type of an attack, an adversary injects operating system commands into existing application functions. An application that uses untrusted input to build command strings is vulnerable. An adversary can leverage OS command injection in an application to elevate privileges, execute arbitrary commands and compromise the underlying operating system.

Source: [CAPEC™ 88](https://capec.mitre.org/data/definitions/88.html)

## Related ASVS Requirements

ASVS (5.0): [1.1.1](/taxonomy/asvs-5.0/01-encoding-and-sanitization/01-encoding-and-sanitization-architecture#V1.1.1), [1.1.2](/taxonomy/asvs-5.0/01-encoding-and-sanitization/01-encoding-and-sanitization-architecture#V1.1.2), [1.2.5](/taxonomy/asvs-5.0/01-encoding-and-sanitization/02-injection-prevention#V1.2.5), [1.3.10](/taxonomy/asvs-5.0/01-encoding-and-sanitization/03-sanitization#V1.3.10), [1.3.3](/taxonomy/asvs-5.0/01-encoding-and-sanitization/03-sanitization#V1.3.3), [16.3.3](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/03-security-events#V16.3.3), [16.4.1](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/04-log-protection#V16.4.1), [16.5.1](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/05-error-handling#V16.5.1)
