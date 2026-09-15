## Scenario: Elsa can reduce app users' privacy because the app does not allow for the user to easily manage, delete and modify their data, change privacy settings and re-prompt for consent when more data is required

### Example

Elsa asks a fitness club app to delete an old jogging route and revoke its location permission. The only control offered is a cheerful “manage everything” button that spins forever, while a new coaching feature starts collecting sleep data without asking again.

Users need practical ways to view, change, and remove their information, plus a fresh consent prompt when collection expands. Without those controls, Elsa’s supposed choice is decorative and the app keeps using data she tried to withdraw.


## Threat Modeling

### STRIDE

This scenario is primarily **Tampering** in STRIDE. The named condition is: Elsa can reduce app users' privacy because the app does not allow for the user to easily manage, delete and modify their data, change privacy settings and re-prompt for consent when more data is required.

The mapped threat is described by the card's application-specific condition.

No separate attack-vector text is assigned; derive the path from the mapped threat.

### What can go wrong?

If Elsa can reduce app users' privacy because the app does not allow for the user to easily manage, delete and modify their data, change privacy settings and re-prompt for consent when more data is required, the failure is concrete rather than merely theatrical: the app could let an attacker cross the cornucopia boundary and reach data or capability that this flow should protect. In this card, the practical route includes the invented path still needs a concrete, observable security impact. That can turn a normal user action into unauthorized access, disclosure, alteration, or service disruption; the mapped weakness entries below identify the exact implementation evidence to check.

Mapped weaknesses that sharpen the review:

- MASWE-0076 — Lack of Proper Data Management Controls: This weakness occurs when an app does not provide users with mechanisms specifically designed to manage their personal data, leaving them without adequate options to exercise their rights over their own information.

### What are we going to do about it?

Provide clear controls to view, delete, and correct collected data, honor changed privacy settings, and request consent again when a new purpose or category is introduced; test revocation, deletion, re-consent, and residual-cache behavior.


Mapped MASTG tests:

- No MASTG test is assigned to this card; define a focused test for the invented attack.

Mapped MASTG best practices:

- No MASTG best practice is assigned; use the narrowest platform control that blocks the attack.

Mapped MASTG knowledge:

- No MASTG knowledge entry is assigned; document the platform behavior discovered during review.
