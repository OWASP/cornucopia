## Scenario: You have invented a new attack against “Platform and Code”

### Example

You are at a county fair when a brand-new trick makes the ticket scanner app accept a barcode that launches an unapproved prize-control screen. The screen awards every visitor a pony, although the fair has only one plastic pony and a very worried treasurer.

The scanner has allowed an untrusted barcode to reach a prize-control function that should belong only to fair staff. Validate inputs, constrain reachable functionality, and keep security decisions independent of untrusted components.


## Threat Modeling

### STRIDE

This scenario is primarily **Tampering**, **Information Disclosure** in STRIDE. The named condition is: You have invented a new attack against “Platform and Code”.

The mapped threat is described by the card's application-specific condition.

No separate attack-vector text is assigned; derive the path from the mapped threat.

### What can go wrong?

If You have invented a new attack against “Platform and Code”, the failure is concrete rather than merely theatrical: the app could let an attacker cross the platform-&-code boundary and reach data or capability that this flow should protect. In this card, the practical route includes the invented path still needs a concrete, observable security impact. That can turn a normal user action into unauthorized access, disclosure, alteration, or service disruption; the mapped weakness entries below identify the exact implementation evidence to check.

Mapped weaknesses that sharpen the review:

- No MASWE entry is assigned to this card; this page keeps the attack explicitly invented.

### What are we going to do about it?

Turn the invented platform attack into a focused test with an observable impact: use least-privilege components, explicit IPC contracts, safe parsing, memory-safe APIs, and platform integrity checks, then fail closed on invalid input.


Mapped MASTG tests:

- No MASTG test is assigned to this card; define a focused test for the invented attack.

Mapped MASTG best practices:

- No MASTG best practice is assigned; use the narrowest platform control that blocks the attack.

Mapped MASTG knowledge:

- No MASTG knowledge entry is assigned; document the platform behavior discovered during review.
