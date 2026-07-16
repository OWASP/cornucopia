## Ace: You have invented a new attack against "Authentication & Authorization"

This card is an invitation to go beyond the documented attack catalogue. Authentication and authorization are among the most actively researched areas of mobile security, and new bypass techniques emerge with each OS release, new hardware feature, and novel application pattern.

### What does this card ask you to do?

Invent a realistic new threat in the Authentication & Authorization domain that is not already represented by AA2 through AAK. Consider:

- **New biometric APIs:** Passive biometric authentication (face unlock during use, behavioural biometrics) — what trust assumptions does the app make about continuous authentication, and are they valid?
- **Cross-device authentication:** The app allows a paired wearable to authenticate the phone — what happens if the wearable is compromised or borrowed?
- **Delegated authentication:** The app accepts tokens from a third-party identity provider — are the token validation rules (audience, issuer, algorithm) implemented correctly on both client and server?
- **Federated logout:** A user logs out of the identity provider — does the app's session end, or does it continue with a locally cached token?
- **Push-notification authentication:** An OTP or approval notification is sent to the device — what if the device has been registered by an attacker who socially engineered the user?

### How to play this card

1. **Nominate a threat:** One player (or the group) proposes a specific, plausible authentication or authorization bypass not covered by other AA cards.
2. **Name the attacker and victim:** Who has what capabilities? What do they want?
3. **Classify the threat (STRIDE):** Most auth attacks are Spoofing or Elevation of Privilege.
4. **Assess likelihood and impact:** Is this realistic for your app's threat model?
5. **Propose a mitigation:** What design, code, or configuration change reduces the risk?
6. **Score the card:** A well-formed novel threat earns full points.

### Example starting prompts

- "What if an attacker registers their device with the push-notification authentication service before the real user, and the real user never checks which devices are registered?"
- "Our app trusts the OS-level 'user is authenticated' signal from Android Work Profile. What if the work profile authentication policy is weaker than our app requires?"
- "We allow login via a social provider. What if the social provider issues tokens with an algorithm we accept but that is weaker than we think (e.g., 'none' algorithm accepted)?"

## Threat Modeling

### STRIDE

Varies by the invented attack. Document the STRIDE classification as part of play.

### What can go wrong?

Authentication and authorization vulnerabilities allow attackers to impersonate users and access data or functionality they are not entitled to. Novel attack paths often arise from the intersection of new platform features and application assumptions that were valid when the app was written but are no longer valid.

### What are we going to do about it?

- Validate the invented threat against the current OWASP MASTG and MASVS.
- Document the threat and the agreed mitigation in the team's threat model register.
- If the threat is genuinely novel, consider contributing it to the OWASP MASVS/MASTG project.
