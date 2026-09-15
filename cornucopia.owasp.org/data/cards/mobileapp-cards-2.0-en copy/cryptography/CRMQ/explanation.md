## Scenario: Simon can bypass hashing and encryption functions because they are custom and/or inadequately implemented

### Example

Simon writes a custom “secure hash” that reverses the password and adds a smiley face. A colleague tests it with `password` and receives the same digest as `drowssap`, proving the algorithm has more personality than security.

Custom hashing and encryption frequently omit collision resistance, key protection, or safe edge-case handling. Standard, reviewed primitives and libraries prevent a home-grown shortcut from becoming the app’s weakest lock.


## Threat Modeling

### STRIDE

This scenario is primarily **Spoofing** in STRIDE. The named condition is: Simon can bypass hashing and encryption functions because they are custom and/or inadequately implemented.

The mapped threat is described by the card's application-specific condition.

No separate attack-vector text is assigned; derive the path from the mapped threat.

### What can go wrong?

If Simon can bypass hashing and encryption functions because they are custom and/or inadequately implemented, the failure is concrete rather than merely theatrical: the app could let an attacker cross the cryptography boundary and reach data or capability that this flow should protect. In this card, the practical route includes the invented path still needs a concrete, observable security impact. That can turn a normal user action into unauthorized access, disclosure, alteration, or service disruption; the mapped weakness entries below identify the exact implementation evidence to check.

Mapped weaknesses that sharpen the review:

- No MASWE entry is assigned to this card; this page keeps the attack explicitly invented.

### What are we going to do about it?

Remove custom hashing and encryption code and delegate to reviewed platform or established-library implementations with approved parameters; test known vectors, key handling, integrity checks, and failure behavior instead of trusting bespoke code.


Mapped MASTG tests:

- No MASTG test is assigned to this card; define a focused test for the invented attack.

Mapped MASTG best practices:

- No MASTG best practice is assigned; use the narrowest platform control that blocks the attack.

Mapped MASTG knowledge:

- MASTG-KNOW-0068 — Cryptographic Third-Party libraries: There are various third-party libraries available, such as:
