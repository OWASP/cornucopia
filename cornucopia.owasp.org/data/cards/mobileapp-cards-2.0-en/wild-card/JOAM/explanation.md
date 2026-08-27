## Scenario: Starr can influence, alter or affect the app so that it no longer complies with legal, regulatory, contractual or other mandates

### Example

Starr runs a town-hall bake sale whose receipt printer quietly changes the allergen notice after a third-party plug-in edits the compliance template. The cupcakes are labeled “nut-free-ish,” a phrase that satisfies nobody except the printer.

An app can lose legal, regulatory, or contractual compliance when untrusted influence changes its mandated behavior. Controls must protect policy-relevant configuration and verify that required notices and processes remain intact.


## Threat Modeling

### STRIDE

This scenario is primarily **Tampering**, **Repudiation** in STRIDE. The named condition is: Starr can influence, alter or affect the app so that it no longer complies with legal, regulatory, contractual or other mandates. This is a wildcard application attack: the story is an invented exercise, while the mapped control is still tested against the stated compliance impact.

The mapped threat is described by the card's application-specific condition.

No separate attack-vector text is assigned; derive the path from the mapped threat.

### What can go wrong?

If Starr can influence, alter or affect the app so that it no longer complies with legal, regulatory, contractual or other mandates, the failure is concrete rather than merely theatrical: the app could let an attacker cross the wild-card boundary and reach data or capability that this flow should protect. In this card, the practical route includes the invented path still needs a concrete, observable security impact. That can turn a normal user action into unauthorized access, disclosure, alteration, or service disruption; the mapped weakness entries below identify the exact implementation evidence to check.

Mapped weaknesses that sharpen the review:

- No MASWE entry is assigned to this card; this page keeps the attack explicitly invented.

### What are we going to do about it?

Define a focused compliance test for each mandated notice, consent, retention, and audit control, protect policy configuration from tampering, and verify the released app still presents the required behavior after dependency and platform changes.


Mapped MASTG tests:

- No MASTG test is assigned to this card; define a focused test for the invented attack.

Mapped MASTG best practices:

- MASTG-BEST-0003 — Comply with Privacy Regulations and Best Practices: Recommendations from CWE-359.

Mapped MASTG knowledge:

- No MASTG knowledge entry is assigned; document the platform behavior discovered during review.
