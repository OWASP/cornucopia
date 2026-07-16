## Scenario: Victor can patch the app and use it to distribute malicious code because the runtime integrity checks are not strong enough according to what is recommended or the perceived effort of a potential attacker

Consider a scenario where Victor modifies a popular productivity app to include a cryptocurrency miner, re-packages it with the original developer's branding, and distributes it through alternative app stores. The app functions identically to the original. The mining code runs in the background. Users install it believing it is the official app. The app's runtime integrity checks — a simple binary hash check on startup — were NOP-patched in Victor's modified version. The integrity check passed because it was the first thing Victor disabled.

1. Single-point runtime integrity checks are easily disabled by patching the check itself.
2. Repacked apps distributed through alternative stores reach users who believe they are installing the official app.
3. Without attestation (Play Integrity API / App Attest), there is no server-verified proof that the running binary is the official release.

### Example

Victor downloads the production APK, decompiles it, adds a `CryptoMinerService` to the `AndroidManifest.xml`, and patches the startup integrity check to return `true` unconditionally. He signs with his own certificate and distributes via an alternative store. Users who install it see the same icon, name, and functionality as the official app. The mining service uses their CPU and drains their battery. The integrity check was the only gate between the official version and Victor's modified version, and it was patchable.

## Threat Modeling

### STRIDE

This scenario falls under **Tampering** and **Spoofing**.

Victor tampers with the app binary to add malicious functionality and spoofs the official app's identity to distribute the malicious version to users who trust the brand.

### What can go wrong?

- Malicious code (miners, keyloggers, ad fraud, stalkerware) is added to the app and distributed to users.
- Users' devices are used for cryptocurrency mining, DDoS attacks, or ad fraud without their knowledge.
- The official app's brand reputation is damaged by the malicious redistribution.

### What are we going to do about it?

- Use server-side attestation (Play Integrity API / App Attest) to verify the running binary is an unmodified, official release; perform sensitive operations only after a passed attestation.
- Distribute checks throughout the codebase so that patching one check does not defeat all integrity verification.
- Combine integrity checking with key derivation: the correct binary hash is a component of a cryptographic key; an incorrect hash produces a wrong key, which fails on decryption naturally.
- Monitor for unofficial redistributions using app-store monitoring services.
