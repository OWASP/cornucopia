## Guidance for Novel Cryptography Threats

**Common areas for novel attacks**
- Post-quantum migration: RSA/ECC key exchange, NIST PQC algorithm selection (ML-KEM, ML-DSA).
- Cryptographic protocol composition: is the combination of primitives provably secure, or does it have interaction weaknesses?
- Key lifecycle: rotation, revocation, re-encryption of historical data.
- Side-channel leakage in timing-sensitive native cryptographic operations.
- Algorithm agility: client-specified algorithms, JWT header manipulation.

**Framing the attack**
- Which cryptographic assumption does the attack violate (confidentiality, integrity, authenticity, non-repudiation)?
- What attacker capability is required?
- What is the impact of a successful attack?

**Mapping to standards**
- NIST SP 800-57 (key management), NIST SP 800-131A (algorithm transitions)
- OWASP MASTG Cryptography chapter
- MASWE: check for an existing weakness entry

**OWASP Mappings**
- MASVS: determined by the invented threat
- MASTG: determined by the invented threat
- MASWE: determined by the invented threat
