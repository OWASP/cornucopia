## Ace: You have invented a new attack of any type

This card is the broadest in the deck. It is an open invitation to think about any threat — novel, cross-cutting, emergent, or highly specific to your app — that is not captured elsewhere in the Cornucopia Mobile deck.

### What does this card ask you to do?

Invent a realistic new threat against any aspect of the mobile app. This might span multiple suits, involve a new attack class, or reflect a threat specific to your app's architecture, user base, or deployment environment.

Consider:

- **Cross-cutting threats:** An attack that requires combining vulnerabilities from multiple suits (e.g., weak authentication + insecure storage + plaintext network + publicly accessible content provider).
- **Emerging technology threats:** New features (edge computing offload, on-device LLMs, AR/VR overlays, blockchain wallet integration) introduce surfaces not covered by existing cards.
- **Operational security threats:** CI/CD pipeline compromise, developer credential theft, store API key abuse — attacks that target the app's delivery mechanism rather than its runtime.
- **Human-factors threats:** Social engineering through the app's support or notification channels; account recovery flows that can be exploited.
- **Threat to the threat-modelling process itself:** What happens if the threat model is out of date? If a new third-party SDK is integrated without review? If a developer bypasses the security review process for a "minor" change?

### How to play this card

1. **Nominate a threat:** Any player proposes any realistic threat against any aspect of the app.
2. **Name the attacker and victim:** What do they want? What do they have access to?
3. **Classify the threat (STRIDE):** All six STRIDE categories are in scope.
4. **Assess likelihood and impact:** What is the realistic probability of this attack? What is the blast radius?
5. **Propose a mitigation:** What change — technical or process — reduces the risk?
6. **Score the card:** A well-formed, novel, plausible threat earns full points.

### Example starting prompts

- "Our app uses an on-device LLM for text summarisation. An attacker sends a prompt injection in a received message that causes the LLM to summarise the message as 'Transfer $500 to attacker.' The user sees the summary, believes it is an instruction, and acts on it."
- "Our CI pipeline signs the production APK with a key stored in the build server's keychain. If an attacker compromises the build server, they can sign a malicious APK with the legitimate production certificate. How does our threat model address build-pipeline security?"
- "A social engineering attack targets the app's customer support channel: the attacker impersonates the user, provides enough information to pass identity verification, and resets the account to an attacker-controlled email. The attack requires no technical exploitation."

## Threat Modeling

### STRIDE

All categories are in scope for this ace card. Document the classification as part of play.

### What can go wrong?

Every app has a threat model. The threat model is never complete. Attacks evolve faster than frameworks, and attackers are not constrained by categories. This card acknowledges that reality and turns it into a team exercise.

### What are we going to do about it?

- Validate the invented threat against current OWASP MASTG, MASVS, and applicable regulatory requirements.
- Document the threat and the agreed mitigation in the team's threat model register.
- Schedule a review of the threat model whenever: a major platform version is released, a new third-party SDK is integrated, a new feature is designed, or a significant incident in the industry affects similar apps.
