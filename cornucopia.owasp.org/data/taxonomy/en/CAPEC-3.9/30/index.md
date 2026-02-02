# CAPEC™ 30: Hijacking a Privileged Thread of Execution

## Description

An adversary hijacks a privileged thread of execution by injecting malicious code into a running process. By using a privleged thread to do their bidding, adversaries can evade process-based detection that would stop an attack that creates a new process. This can lead to an adversary gaining access to the process's memory and can also enable elevated privileges. The most common way to perform this attack is by suspending an existing thread and manipulating its memory.

Source: [CAPEC™ 30](https://capec.mitre.org/data/definitions/30.html)

## Related ASVS Requirements

ASVS (5.0): [16.3.3](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/03-security-events#V16.3.3), [8.3.3](/taxonomy/asvs-5.0/08-authorization/03-operation-level-authorization#V8.3.3)
