## Guidance for Any Novel Threat

**Cross-cutting threats**
- When the threat spans multiple MASVS categories, document all relevant mappings.
- Compound vulnerabilities are often harder to mitigate because each individual finding may seem low-severity in isolation.

**Emerging technology**
- On-device LLMs: prompt injection, training data extraction, model inversion.
- AR/VR overlays: UI spoofing via overlay, sensor data exfiltration, mixed-reality phishing.
- Blockchain wallets: private key management, transaction signing authorization, clipboard hijacking for wallet addresses.

**Operational security**
- CI/CD pipeline integrity: signing key protection, dependency verification, artifact signing.
- Developer credentials: phishing, credential stuffing against developer portals, 2FA bypass.

**Process**
- Threat model staleness: schedule regular reviews; treat threat models as living documents.
- Security review bypasses: gate deployment on completed security review for all changes above a defined risk threshold.

**OWASP Mappings**
- MASVS: determined by the invented threat
- MASTG: determined by the invented threat
- MASWE: determined by the invented threat

Do not fabricate references. Document what is known and what is unknown.
