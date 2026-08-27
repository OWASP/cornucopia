## Scenario: You have invented a new attack against “Cryptography”

### Example

You are at a farmers’ market when a new attack makes a weighing app accept a basket of rocks as a certified kilogram. The stallholder charges for truffles, while the scale insists it has discovered a very mineral-rich mushroom variety.

The weighing service has accepted an input that changes what the scale certifies, just as a cryptographic boundary can be tricked into forging or revealing protected material. Review unusual inputs and failure paths rather than trusting familiar attack lists.


## Threat Modeling

### STRIDE

This scenario is primarily **Tampering**, **Information Disclosure** in STRIDE. The named condition is: You have invented a new attack against “Cryptography”.

This is an invented Cryptography attack, as the card asks the players to create one. The team should name the asset, trust boundary, and failure condition before deciding which STRIDE label fits.

The attack path is deliberately hypothetical. Treat the story as a testable assumption, not as a claim that OWASP has catalogued this exact attack.

### What can go wrong?

If You have invented a new attack against “Cryptography”, the failure is concrete rather than merely theatrical: the app could let an attacker cross the cryptography boundary and reach data or capability that this flow should protect. In this card, the practical route includes the invented path still needs a concrete, observable security impact. That can turn a normal user action into unauthorized access, disclosure, alteration, or service disruption; the mapped weakness entries below identify the exact implementation evidence to check.

Mapped weaknesses that sharpen the review:

- No MASWE entry is assigned to this card; this page keeps the attack explicitly invented.

### What are we going to do about it?

Turn the invented cryptography attack into a focused test with a measurable impact: use only vetted platform primitives, purpose-specific keys, CSPRNG-generated nonces, and authenticated encryption, and fail closed rather than falling back to plaintext.


Mapped MASTG tests:

- No MASTG test is assigned to this card; define a focused test for the invented attack.

Mapped MASTG best practices:

- No MASTG best practice is assigned; use the narrowest platform control that blocks the attack.

Mapped MASTG knowledge:

- No MASTG knowledge entry is assigned; document the platform behavior discovered during review.
