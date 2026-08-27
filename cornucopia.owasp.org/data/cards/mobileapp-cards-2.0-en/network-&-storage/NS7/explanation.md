## Scenario: Sam can dump sensitive data from memory because the data is not stored as primitive data types and overwritten with random data after use or because the app's input fields use insecure SDKs to store the data in RAM

### Example

Sam enters a credit-card number into an app whose text field keeps several editable copies in memory. A diagnostic dump later reveals every digit, plus a half-finished note about buying a pony.

Sensitive values should use carefully handled representations and be cleared or overwritten after use where the platform permits. Input widgets and SDKs that retain RAM copies make memory extraction far more rewarding for an attacker.


## Threat Modeling

### STRIDE

This scenario is primarily **Tampering**, **Information Disclosure** in STRIDE. The named condition is: Sam can dump sensitive data from memory because the data is not stored as primitive data types and overwritten with random data after use or because the app's input fields use insecure SDKs to store the data in RAM.

The mapped threat is described by the card's application-specific condition.

No separate attack-vector text is assigned; derive the path from the mapped threat.

### What can go wrong?

If Sam can dump sensitive data from memory because the data is not stored as primitive data types and overwritten with random data after use or because the app's input fields use insecure SDKs to store the data in RAM, the failure is concrete rather than merely theatrical: the app could let an attacker cross the network-&-storage boundary and reach data or capability that this flow should protect. In this card, the practical route includes the invented path still needs a concrete, observable security impact. That can turn a normal user action into unauthorized access, disclosure, alteration, or service disruption; the mapped weakness entries below identify the exact implementation evidence to check.

Mapped weaknesses that sharpen the review:

- No MASWE entry is assigned to this card; this page keeps the attack explicitly invented.

### What are we going to do about it?

Keep secrets out of ordinary immutable strings and insecure keyboard or SDK buffers, prefer memory-safe and secure input APIs, clear mutable buffers immediately after use, and inspect runtime memory to confirm sensitive values are not retained.


Mapped MASTG tests:

- No MASTG test is assigned to this card; define a focused test for the invented attack.

Mapped MASTG best practices:

- No MASTG best practice is assigned; use the narrowest platform control that blocks the attack.

Mapped MASTG knowledge:

- MASTG-KNOW-0051 — Process Memory: Many applications handle sensitive information, provided either by the user, the operating system or the backend. This data is often available in-memory while the user is using the application, as it is needed for the application to...
- MASTG-KNOW-0103 — Process Memory: Analyzing memory can help developers to identify the root causes of problems such as application crashes. However, it can also be used to access to sensitive data. This section describes how to check process' memory for data disclosure.
