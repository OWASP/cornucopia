## Scenario: Luis can cause the app to act on falsified protected data because it does not verify that data received from external services is authentic and unaltered

### Example

Luis imports a train ticket from an external booking service. The app displays a forged “platform 0” instruction from an unverified response, sending him to a maintenance shed where the only express service is a broom.

Data from external services must be authenticated and checked for alteration before it influences decisions. Without that verification, falsified protected data can steer users or change app behavior.


## Threat Modeling

### STRIDE

This scenario is primarily **Tampering**, **Elevation of Privilege**, **Denial of Service** in STRIDE. The named condition is: Luis can cause the app to act on falsified protected data because it does not verify that data received from external services is authentic and unaltered.

The mapped threat is described by the card's application-specific condition.

No separate attack-vector text is assigned; derive the path from the mapped threat.

### What can go wrong?

If Luis can cause the app to act on falsified protected data because it does not verify that data received from external services is authentic and unaltered, the failure is concrete rather than merely theatrical: the app could let an attacker cross the cornucopia boundary and reach data or capability that this flow should protect. In this card, the practical route includes the invented path still needs a concrete, observable security impact. That can turn a normal user action into unauthorized access, disclosure, alteration, or service disruption; the mapped weakness entries below identify the exact implementation evidence to check.

Mapped weaknesses that sharpen the review:

- No MASWE entry is assigned to this card; this page keeps the attack explicitly invented.

### What are we going to do about it?

Verify authenticity, integrity, freshness, and expected schema for every response from an external service before using protected data; require TLS certificate validation and signed or MACed high-value responses, and test tampering and replay.


Mapped MASTG tests:

- No MASTG test is assigned to this card; define a focused test for the invented attack.

Mapped MASTG best practices:

- No MASTG best practice is assigned; use the narrowest platform control that blocks the attack.

Mapped MASTG knowledge:

- MASTG-KNOW-0012 — Key Generation: The Android SDK allows you to specify how a key should be generated, and under which circumstances it can be used. Android 6.0 (API level 23) introduced the `KeyGenParameterSpec` class that can be used to ensure the correct key usage in...
- MASTG-KNOW-0066 — CryptoKit: Apple CryptoKit was released with iOS 13 and is built on top of Apple's native cryptographic library corecrypto which is FIPS 140-2 validated. The Swift framework provides a strongly typed API interface, has effective memory management,...
