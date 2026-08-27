## Scenario: You have invented a new attack against “Network & Storage”

### Example

You connect a weather app on a mountain gondola’s Wi-Fi and discover that its server accepts cleartext and negotiates an obsolete TLS version. A nearby observer changes “snow tomorrow” to “free ice cream,” sending you onto the slope with a cone-shaped optimism.

The café connection has let an intermediary rewrite a trusted result while remaining invisible to you. Reject cleartext and deprecated downgrades, and use authenticated TLS so a network stranger cannot quietly read or alter the app’s traffic.


## Threat Modeling

### STRIDE

This scenario is primarily **Tampering**, **Information Disclosure** in STRIDE. The named condition is: You have invented a new attack against “Network & Storage”.

This is an invented Network & Storage attack, as the card asks the players to create one. The team should name the asset, trust boundary, and failure condition before deciding which STRIDE label fits.

The attack path is deliberately hypothetical. Treat the story as a testable assumption, not as a claim that OWASP has catalogued this exact attack.

### What can go wrong?

If You have invented a new attack against “Network & Storage”, the failure is concrete rather than merely theatrical: the app could let an attacker cross the network-&-storage boundary and reach data or capability that this flow should protect. In this card, the practical route includes the invented path still needs a concrete, observable security impact. That can turn a normal user action into unauthorized access, disclosure, alteration, or service disruption; the mapped weakness entries below identify the exact implementation evidence to check.

Mapped weaknesses that sharpen the review:

- No MASWE entry is assigned to this card; this page keeps the attack explicitly invented.

### What are we going to do about it?

Define a focused network-and-storage test for the invented attack: use authenticated TLS, encrypted and integrity-protected storage, least-privilege file access, and explicit validation of every external response before it is persisted or acted on.


Mapped MASTG tests:

- No MASTG test is assigned to this card; define a focused test for the invented attack.

Mapped MASTG best practices:

- No MASTG best practice is assigned; use the narrowest platform control that blocks the attack.

Mapped MASTG knowledge:

- No MASTG knowledge entry is assigned; document the platform behavior discovered during review.
