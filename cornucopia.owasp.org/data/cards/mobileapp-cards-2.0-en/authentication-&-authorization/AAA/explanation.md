## Scenario: You have invented a new attack against “Authentication & Authorization”

### Example

You are at a railway station where a kiosk accepts a stranger’s claimed identity because its ticket printer has no idea who is standing at the screen. The stranger selects a first-class sleeper and the machine cheerfully prints a pass for “Captain Sandwich.”

The invented trick works because the station has no dependable sign-in step to challenge the claim. A real app could similarly trust an interaction that never proves the caller’s identity, turning a harmless-looking request into an unauthorized privilege.


## Threat Modeling

### STRIDE

This scenario is primarily **Spoofing** in STRIDE. The named condition is: You have invented a new attack against “Authentication & Authorization”.

The mapped threat is described by the card's application-specific condition.

No separate attack-vector text is assigned; derive the path from the mapped threat.

### What can go wrong?

If You have invented a new attack against “Authentication & Authorization”, the failure is concrete rather than merely theatrical: the app could let an attacker cross the authentication-&-authorization boundary and reach data or capability that this flow should protect. In this card, the practical route includes the invented path still needs a concrete, observable security impact. That can turn a normal user action into unauthorized access, disclosure, alteration, or service disruption; the mapped weakness entries below identify the exact implementation evidence to check.

Mapped weaknesses that sharpen the review:

- No MASWE entry is assigned to this card; this page keeps the attack explicitly invented.

### What are we going to do about it?

Define a focused test for the invented authentication attack: require the server to authenticate and authorize every protected request, bind local credentials to Android Keystore or iOS Keychain controls, and reject tampered deep-link or component data before it reaches a privileged action.


Mapped MASTG tests:

- No MASTG test is assigned to this card; define a focused test for the invented attack.

Mapped MASTG best practices:

- No MASTG best practice is assigned; use the narrowest platform control that blocks the attack.

Mapped MASTG knowledge:

- No MASTG knowledge entry is assigned; document the platform behavior discovered during review.
