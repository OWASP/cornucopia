## Guidance for Novel Resilience Threats

**Common areas for novel attacks**
- New versions of Frida, Magisk, or other tooling that bypass current detection heuristics.
- Attestation protocol edge cases (replay, device-specific bypasses, revocation failures).
- Supply-chain compromise of integrity libraries or signing infrastructure.
- Legitimate platform features (accessibility, MDM, enterprise VPN) enabling new bypass paths.

**Framing the attack**
- What resilience control does the threat bypass?
- What does an attacker gain by bypassing it?
- What is the next security boundary after the bypassed control?

**Mapping to standards**
- MASVS: RESILIENCE-1 through RESILIENCE-4
- MASTG: consult the Resilience test catalogue
- MASWE: check for an existing weakness entry

**OWASP Mappings**
- MASVS: determined by the invented threat
- MASTG: determined by the invented threat
- MASWE: determined by the invented threat
