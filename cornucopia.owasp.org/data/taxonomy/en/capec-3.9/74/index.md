# CAPEC™ 74: Manipulating State

## Description

{'p': [{'__prefix': 'xhtml', '__text': 'The adversary modifies state information maintained by the target software or causes a state transition in hardware. If successful, the target will use this tainted state and execute in an unintended manner.'}, {'__prefix': 'xhtml', '__text': 'State management is an important function within a software application. User state maintained by the application can include usernames, payment information, browsing history as well as application-specific contents such as items in a shopping cart. Manipulating user state can be employed by an adversary to elevate privilege, conduct fraudulent transactions or otherwise modify the flow of the application to derive certain benefits.'}, {'__prefix': 'xhtml', '__text': 'If there is a hardware logic error in a finite state machine, the adversary can use this to put the system in an undefined state which could cause a denial of service or exposure of secure data.'}]}

Source: [CAPEC™ 74](https://capec.mitre.org/data/definitions/74.html)

## Related ASVS Requirements

ASVS (5.0): [16.3.2](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/03-security-events#V16.3.2), [16.3.3](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/03-security-events#V16.3.3), [2.3.1](/taxonomy/asvs-5.0/02-validation-and-business-logic/03-business-logic-security#V2.3.1), [2.3.4](/taxonomy/asvs-5.0/02-validation-and-business-logic/03-business-logic-security#V2.3.4), [2.3.5](/taxonomy/asvs-5.0/02-validation-and-business-logic/03-business-logic-security#V2.3.5), [3.5.7](/taxonomy/asvs-5.0/03-web-frontend-security/05-browser-origin-separation#V3.5.7), [8.3.1](/taxonomy/asvs-5.0/08-authorization/03-operation-level-authorization#V8.3.1)
