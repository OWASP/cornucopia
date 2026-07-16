## Guidance for Novel Platform & Code Threats

**Framing the attack surface**
- Which OS API, SDK, or platform feature does the threat exploit?
- Is the feature documented with security guidance in the platform developer reference?
- Does the MASTG "Mobile App Attack Surface" section cover it?

**Describing the exploit chain**
- What attacker capability is required (same-device app, network access, physical access)?
- What is the full exploitation chain: how does the attacker reach the vulnerable code and what is the impact?

**Validating the threat**
- Can you write a proof-of-concept, even a prototype, to confirm the threat is realistic?
- Are there CVEs, academic papers, or conference talks addressing related techniques?

**Mapping to standards**
- MASVS category: PLATFORM, CODE, STORAGE, AUTH, NETWORK, CRYPTO, PRIVACY, or RESILIENCE?
- MASTG test: does an existing test apply, or would a new one be needed?
- MASWE: is there an existing weakness entry, or should one be proposed?

**OWASP Mappings**
- MASVS: determined by the invented threat
- MASTG: determined by the invented threat
- MASWE: determined by the invented threat

Do not fabricate references. If no specific MASTG test or MASWE entry exists for the invented threat, note this explicitly and consider contributing one to the project.
