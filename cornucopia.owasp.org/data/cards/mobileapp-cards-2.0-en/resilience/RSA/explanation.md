## Scenario: You have invented a new attack against “Resilience”

### Example

You are at a community theatre when an invented trick makes the ticket app treat the usher’s prop flashlight as a privileged control. One blink changes every seat to “reserved for ghosts,” and the box office has to apologize to an empty row.

The flashlight has become an unexpected control for a sensitive ticket operation. Resilience measures should limit what an odd input or runtime condition can influence, even when the path is not in the usual exploit catalog.


## Threat Modeling

### STRIDE

This scenario is primarily **Tampering**, **Information Disclosure** in STRIDE. The named condition is: You have invented a new attack against “Resilience”.

This is an invented Resilience attack, as the card asks the players to create one. The team should name the asset, trust boundary, and failure condition before deciding which STRIDE label fits.

The attack path is deliberately hypothetical. Treat the story as a testable assumption, not as a claim that OWASP has catalogued this exact attack.

### What can go wrong?

If You have invented a new attack against “Resilience”, the failure is concrete rather than merely theatrical: the app could let an attacker cross the resilience boundary and reach data or capability that this flow should protect. In this card, the practical route includes the invented path still needs a concrete, observable security impact. That can turn a normal user action into unauthorized access, disclosure, alteration, or service disruption; the mapped weakness entries below identify the exact implementation evidence to check.

Mapped weaknesses that sharpen the review:

- No MASWE entry is assigned to this card; this page keeps the attack explicitly invented.

### What are we going to do about it?

Define a focused resilience test for the invented attack: remove production debug artifacts, verify signatures and provenance, use proportionate attestation and tamper responses, and ensure sensitive operations fail safely when the environment is untrusted.


Mapped MASTG tests:

- No MASTG test is assigned to this card; define a focused test for the invented attack.

Mapped MASTG best practices:

- No MASTG best practice is assigned; use the narrowest platform control that blocks the attack.

Mapped MASTG knowledge:

- No MASTG knowledge entry is assigned; document the platform behavior discovered during review.
