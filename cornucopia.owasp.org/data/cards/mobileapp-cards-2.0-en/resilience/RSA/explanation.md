## Ace: You have invented a new attack against "Resilience"

This card invites your team to think creatively about novel threats to the app's resilience — its ability to detect, resist, and respond to attacks in hostile environments.

### What does this card ask you to do?

Invent a realistic new threat in the Resilience domain not already represented by RS2 through RSK. Consider:

- **New attack tooling:** A new dynamic analysis or exploitation tool has been released that bypasses a class of existing resilience controls. How would it affect this app?
- **Side-channel leakage from resilience controls themselves:** Does an anti-debugging check change the app's observable behaviour in a way that itself leaks information (e.g., timing differences, error messages)?
- **Attestation protocol weaknesses:** Are there scenarios where the Play Integrity API or App Attest verdict can be replayed, forged, or falsely obtained?
- **Supply-chain compromise of resilience libraries:** The RASP or integrity-check library is compromised upstream. How would this affect the app?
- **Legitimate tools used maliciously:** Screen readers, accessibility services, and MDM profiles are legitimate — can they be used to bypass resilience controls in ways the threat model did not consider?

### How to play this card

1. **Nominate a threat:** Propose a specific, plausible resilience bypass not covered by other RS cards.
2. **Name the attacker and victim:** What capabilities does the attacker have?
3. **Classify the threat (STRIDE):** Resilience attacks often involve Tampering or Elevation of Privilege.
4. **Assess likelihood and impact:** Is this realistic for your app's threat model?
5. **Propose a mitigation:** What change reduces the risk?
6. **Score the card:** A well-formed novel threat earns full points.

### Example starting prompts

- "A new version of Frida bypasses all current `_dyld` injection detection methods. How does this change our threat model?"
- "An enterprise MDM profile installs a trusted CA and enables USB debugging by policy. How does this affect our certificate pinning and anti-debugging assumptions?"
- "The Play Integrity API introduces a bug where a specific device model always returns `MEETS_DEVICE_INTEGRITY` even when rooted. How would we detect and respond to this?"

## Threat Modeling

### STRIDE

Varies by the invented attack.

### What can go wrong?

Resilience controls are in an ongoing arms race with attacker tooling. A control that is effective today may be bypassed by new tooling next quarter. The threat model must be reviewed with each major tool release and OS version.

### What are we going to do about it?

- Validate the invented threat against the current OWASP MASTG and MASVS.
- Document the threat and the agreed mitigation in the team's threat model register.
- Review whether the invented threat changes the risk rating of any other Resilience card.
