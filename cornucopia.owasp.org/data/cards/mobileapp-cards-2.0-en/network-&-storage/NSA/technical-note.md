## Guidance for Novel Network & Storage Threats

**Common areas for novel attacks**
- New transport protocols (QUIC/HTTP3, WebSockets, custom binary protocols): TLS-equivalent protection and certificate validation.
- Third-party storage SDKs (Realm, SQLCipher, Firebase): key management, backup behaviour, and data residency.
- Offline-first databases (sync conflict resolution, replication security).
- Data residency changes affecting regulatory compliance.

**Framing the attack**
- What network path or storage location does the threat exploit?
- What data is at risk and what is the impact of its disclosure or modification?

**Mapping to standards**
- MASVS: NETWORK-1, NETWORK-2, STORAGE-1, STORAGE-2, CRYPTO-2
- MASTG: consult the test catalogue for the closest existing test
- MASWE: check for an existing weakness entry

**OWASP Mappings**
- MASVS: determined by the invented threat
- MASTG: determined by the invented threat
- MASWE: determined by the invented threat
