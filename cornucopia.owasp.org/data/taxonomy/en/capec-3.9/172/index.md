# CAPEC™ 172: Manipulate Timing and State

## Description

An attacker exploits weaknesses in timing or state maintaining functions to perform actions that would otherwise be prevented by the execution flow of the target code and processes. An example of a state attack might include manipulation of an application's information to change the apparent credentials or similar information, possibly allowing the application to access material it would not normally be allowed to access. A common example of a timing attack is a test-action race condition where some state information is tested and, if it passes, an action is performed. If the attacker can change the state between the time that the application performs the test and the time the action is performed, then they might be able to manipulate the outcome of the action to malicious ends.

Source: [CAPEC™ 172](https://capec.mitre.org/data/definitions/172.html)

## Related ASVS Requirements

ASVS (5.0): [16.3.2](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/03-security-events#V16.3.2), [16.3.3](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/03-security-events#V16.3.3), [2.3.1](/taxonomy/asvs-5.0/02-validation-and-business-logic/03-business-logic-security#V2.3.1), [2.3.2](/taxonomy/asvs-5.0/02-validation-and-business-logic/03-business-logic-security#V2.3.2), [2.3.3](/taxonomy/asvs-5.0/02-validation-and-business-logic/03-business-logic-security#V2.3.3), [2.3.4](/taxonomy/asvs-5.0/02-validation-and-business-logic/03-business-logic-security#V2.3.4), [2.3.5](/taxonomy/asvs-5.0/02-validation-and-business-logic/03-business-logic-security#V2.3.5), [8.3.1](/taxonomy/asvs-5.0/08-authorization/03-operation-level-authorization#V8.3.1)
