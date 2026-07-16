## Ace: You have invented a new attack against "Network & Storage"

This card invites your team to explore novel threats against the ways your app transmits and stores data.

### What does this card ask you to do?

Invent a realistic new threat in the Network & Storage domain not already represented by NS2 through NSK. Consider:

- **New sync and cloud storage APIs:** Does the app use a new cloud-sync service, edge-sync feature, or offline-first database? What are the security guarantees of that service, and does the app rely on assumptions that are not guaranteed?
- **Encrypted network protocols:** The app uses QUIC, HTTP/3, or a custom binary protocol. Are TLS-equivalent protections applied? Are certificate validation and pinning implemented for the new protocol stack?
- **Storage at rest — novel surfaces:** Encrypted database libraries (SQLCipher, Realm with encryption), keychain/keystore access from app extensions, Watch apps, or widgets sharing the same storage — are the security properties the same in all contexts?
- **Data residency and sovereignty:** The app's storage backend changes region or provider — does this affect compliance obligations, and is the app aware of where its data is stored?

### How to play this card

1. **Nominate a threat:** One player (or the group) proposes a specific, plausible network or storage threat not covered by other NS cards.
2. **Name the attacker and victim:** What capabilities does the attacker have? What data or functionality are they targeting?
3. **Classify the threat (STRIDE):** Most network/storage attacks involve Information Disclosure or Tampering.
4. **Assess likelihood and impact:** Is this realistic for your app's threat model?
5. **Propose a mitigation:** What change reduces the risk?
6. **Score the card:** A well-formed novel threat earns full points.

### Example starting prompts

- "Our app uses a third-party SDK for offline document sync. The SDK uses its own encryption key stored in the SDK's keychain group. What if the SDK is compromised or its key management is weak?"
- "The app uses a WebSocket connection for real-time updates. The WebSocket's TLS configuration is managed by a third-party library. Is certificate pinning applied to the WebSocket connection?"
- "We recently migrated our API to a GraphQL endpoint. Are the same authentication and TLS checks applied to GraphQL introspection and batch query endpoints?"

## Threat Modeling

### STRIDE

Varies by the invented attack.

### What can go wrong?

Network and storage security controls are often applied to the "main path" but miss alternative data paths: SDKs, sync services, caches, and new protocol stacks. Novel attack paths emerge when attackers probe these secondary paths.

### What are we going to do about it?

- Validate the invented threat against the current OWASP MASTG and MASVS.
- Document the threat and the agreed mitigation in the team's threat model register.
- If genuinely novel, consider contributing to the OWASP MASVS/MASTG project.
