# CAPEC™ 234: Hijacking a privileged process

## Description

An adversary gains control of a process that is assigned elevated privileges in order to execute arbitrary code with those privileges. Some processes are assigned elevated privileges on an operating system, usually through association with a particular user, group, or role. If an attacker can hijack this process, they will be able to assume its level of privilege in order to execute their own code.

Source: [CAPEC™ 234](https://capec.mitre.org/data/definitions/234.html)

## Related ASVS Requirements

ASVS (5.0): [16.3.3](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/03-security-events#V16.3.3), [8.3.3](/taxonomy/asvs-5.0/08-authorization/03-operation-level-authorization#V8.3.3)
