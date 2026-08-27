## Scenario: You have invented a new attack of any type

### Example

You enter a new attack in a museum kiosk: a malformed audio guide makes the exhibit app treat a harmless exhibit label as an instruction to rewrite the curator’s narration. The guide still claims the whales are historically significant, and the curator starts questioning the educational value of interpretive whale noises.

The unchecked guide field has crossed a trust boundary and now influences code outside the exhibit. Validate the guide, isolate its parser, and constrain what it can reach so an unusual payload cannot become an unauthorized operation.


## Threat Modeling

### STRIDE

This scenario is primarily **Tampering**, **Information Disclosure** in STRIDE. The named condition is: You have invented a new attack of any type.

This is an invented Cornucopia attack, as the card asks the players to create one. The team should name the asset, trust boundary, and failure condition before deciding which STRIDE label fits.

The attack path is deliberately hypothetical. Treat the story as a testable assumption, not as a claim that OWASP has catalogued this exact attack.

### What can go wrong?

If You have invented a new attack of any type, the failure is concrete rather than merely theatrical: the app could let an attacker cross the cornucopia boundary and reach data or capability that this flow should protect. In this card, the practical route includes the invented path still needs a concrete, observable security impact. That can turn a normal user action into unauthorized access, disclosure, alteration, or service disruption; the mapped weakness entries below identify the exact implementation evidence to check.

Mapped weaknesses that sharpen the review:

- No MASWE entry is assigned to this card; this page keeps the attack explicitly invented.

### What are we going to do about it?

Turn the invented attack into a focused test with a concrete impact: minimize data and permissions, validate external input and service responses, use secure IPC and memory-safe APIs, and fail closed when consent or integrity checks fail.


Mapped MASTG tests:

- No MASTG test is assigned to this card; define a focused test for the invented attack.

Mapped MASTG best practices:

- No MASTG best practice is assigned; use the narrowest platform control that blocks the attack.

Mapped MASTG knowledge:

- No MASTG knowledge entry is assigned; document the platform behavior discovered during review.
