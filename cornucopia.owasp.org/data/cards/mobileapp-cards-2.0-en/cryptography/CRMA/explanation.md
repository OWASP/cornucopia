## Ace: You have invented a new attack against "Cryptography"

This card invites your team to explore novel cryptographic threats specific to your app's design and threat model.

### What does this card ask you to do?

Invent a realistic new threat in the Cryptography domain not already represented by CRM2 through CRMK. Consider:

- **Post-quantum preparedness:** Your app uses RSA or ECC for key exchange. CRQC (Cryptographically Relevant Quantum Computers) are not yet available, but what happens when they are? Is your app's key exchange algorithm quantum-resistant?
- **Protocol-level issues:** Your app implements a custom authentication protocol using standard primitives. Is the protocol composition secure? (Many protocols composed of secure primitives are themselves insecure.)
- **Key lifecycle gaps:** Your app rotates encryption keys, but what happens to data encrypted with an old key after rotation? Is it re-encrypted, or does the old key persist indefinitely as a "legacy" key?
- **Side-channel leakage in native code:** Timing, power, or electromagnetic emanations from native cryptographic operations — relevant for high-security on-device operations.
- **Cryptographic agility failures:** Your app allows the client to specify the algorithm. What happens if the client requests a weak or deprecated algorithm?

### How to play this card

1. **Nominate a threat:** Propose a specific, plausible cryptographic vulnerability not covered by other CRM cards.
2. **Name the attacker and victim:** What cryptographic assumption do they violate?
3. **Classify the threat (STRIDE):** Cryptographic attacks most often result in Information Disclosure.
4. **Assess likelihood and impact:** Is this realistic for your app's threat model and expected attacker capabilities?
5. **Propose a mitigation:** What design or implementation change reduces the risk?
6. **Score the card:** A well-formed novel threat earns full points.

### Example starting prompts

- "Our app uses ECDH for key exchange. What if the server or client sends a malicious point not on the curve (invalid curve attack)? Does our implementation validate the point?"
- "Our app stores encrypted data and supports key rotation. When a user changes their PIN, is the old key securely destroyed, or does it persist in the KeyStore under the old alias?"
- "Our app accepts the hash algorithm as a parameter in a JWT header. What if an attacker substitutes `none` or `HS256` for `RS256` (algorithm confusion attack)?"

## Threat Modeling

### STRIDE

Varies by the invented attack. Most cryptographic attacks result in Information Disclosure or Spoofing.

### What can go wrong?

Cryptographic protocols and implementations have subtle failure modes that are not always visible in code review. Novel attack research regularly reveals weaknesses in apparently secure implementations. Threat modeling must keep pace with published research.

### What are we going to do about it?

- Validate the invented threat against current NIST SP 800-series guidance and OWASP MASTG.
- Consider engaging a specialist cryptographic reviewer for complex protocol designs.
- Document the threat and the agreed mitigation in the team's threat model register.
