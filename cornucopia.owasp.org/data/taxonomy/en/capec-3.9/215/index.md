# CAPEC™ 215: Fuzzing for application mapping

## Description

An attacker sends random, malformed, or otherwise unexpected messages to a target application and observes the application's log or error messages returned. The attacker does not initially know how a target will respond to individual messages but by attempting a large number of message variants they may find a variant that trigger's desired behavior. In this attack, the purpose of the fuzzing is to observe the application's log and error messages, although fuzzing a target can also sometimes cause the target to enter an unstable state, causing a crash.

Source: [CAPEC™ 215](https://capec.mitre.org/data/definitions/215.html)

## Related ASVS Requirements

ASVS (5.0): [13.2.2](/taxonomy/asvs-5.0/13-configuration/02-backend-communication-configuration#V13.2.2), [13.4.2](/taxonomy/asvs-5.0/13-configuration/04-unintended-information-leakage#V13.4.2), [13.4.6](/taxonomy/asvs-5.0/13-configuration/04-unintended-information-leakage#V13.4.6), [16.2.5](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/02-general-logging#V16.2.5), [16.4.2](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/04-log-protection#V16.4.2), [16.5.1](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/05-error-handling#V16.5.1), [2.4.1](/taxonomy/asvs-5.0/02-validation-and-business-logic/04-anti-automation#V2.4.1)
