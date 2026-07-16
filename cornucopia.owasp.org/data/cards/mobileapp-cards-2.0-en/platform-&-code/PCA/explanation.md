## Ace: You have invented a new attack against "Platform & Code"

This card invites your team to step off the scripted threat list and think creatively about the platform surface your app exposes.

### What does this card ask you to do?

Invent a realistic new threat in the Platform & Code domain that is not already represented by PC2 through PCK. Think about:

- **Emerging APIs:** What OS feature introduced in the last year does the app use without fully understanding its security implications? (App Clips, Live Activities, Interactive Widgets, CarPlay extensions, visionOS scenes)
- **Side channels:** Can an attacker infer sensitive app state from CPU utilisation, network traffic timing, screen brightness changes, or sensor readings?
- **Build and supply chain:** Could a CI plugin, code-generation template, or obfuscation tool introduce a backdoor or insecure default into the compiled binary?
- **New IPC surfaces:** Does the app share state with a wearable companion, a TV app, or a browser extension? Do those channels apply the same access controls as the main app?

### How to play this card

1. **Nominate a threat:** One player (or the group) proposes a specific, plausible scenario not covered by other PC cards.
2. **Name the attacker and victim:** Who has what capabilities? What do they want?
3. **Classify the threat (STRIDE):** Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, or Elevation of Privilege?
4. **Assess likelihood and impact:** Is this realistic for your app's threat model?
5. **Propose a mitigation:** What design, code, or configuration change reduces the risk?
6. **Score the card:** A well-formed novel threat earns full points.

### Example starting prompts

- "Our analytics SDK bundles its own WebView. What if that WebView has a vulnerability our app's controls don't cover?"
- "Our new home-screen widget shares a database DAO with the main app. What if the widget's data endpoint doesn't apply the same access controls?"
- "What if a malicious accessibility service reads every field in our app without triggering any permission prompt visible to the user?"

## Threat Modeling

### STRIDE

Varies by the invented attack. Document the classification as part of play.

### What can go wrong?

Platform APIs evolve faster than security guidance. An attack class that does not exist today may appear next year as researchers publish new techniques. Threat modeling must be a living exercise, revisited with each major platform release.

### What are we going to do about it?

- Validate the invented threat against the current OWASP MASTG and MASVS to check whether existing guidance already covers it.
- If genuinely novel, consider contributing it to the OWASP MASVS/MASTG project as a new weakness candidate.
- Document the threat and the agreed mitigation in the team's threat model register.
