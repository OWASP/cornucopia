## Guidance for Novel Authentication & Authorization Threats

**Common areas for novel attacks**
- New OS authentication APIs introduced in recent versions (e.g., Android Credential Manager, iOS Passkeys / FIDO2).
- Cross-device trust (wearable → phone authentication, Handoff/Continuity on iOS).
- JWT / OAuth 2.0 implementation errors: algorithm confusion, missing audience/issuer validation, non-revocable refresh tokens.
- Behavioural biometrics: passive authentication — is the trust model clearly defined and implemented?

**Framing the attack**
- What attacker capability is required?
- What is the authentication bypass chain?
- Can you write a proof-of-concept?

**Mapping to standards**
- MASVS: AUTH-1, AUTH-2, or AUTH-3 depending on the attack
- MASTG: consult the MASTG test catalogue for the closest existing test
- MASWE: check for an existing weakness entry; propose one if none exists

**OWASP Mappings**
- MASVS: determined by the invented threat
- MASTG: determined by the invented threat
- MASWE: determined by the invented threat

Do not fabricate references.
