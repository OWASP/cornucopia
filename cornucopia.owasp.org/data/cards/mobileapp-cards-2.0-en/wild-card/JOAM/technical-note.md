## Platform-Aware Review Guidance

**Regulatory Landscape (reference only; verify current requirements)**
- GDPR (EU): data residency, lawful basis, data subject rights, breach notification (72 hours).
- CCPA/CPRA (California): right to know, right to delete, right to opt-out, sensitive personal information.
- HIPAA (US healthcare): PHI protection, minimum necessary principle, breach notification.
- PCI-DSS (payment card): cardholder data protection, access control, logging.
- PSD2 (EU payment services): strong customer authentication, open banking API security.
- DPDPA (India), PDPA (Thailand), PIPA (South Korea): emerging regional frameworks.

**Compliance-Critical Data Flows**
- Data residency: verify cloud region selection is not attacker-influenceable; pin region configuration server-side with integrity verification.
- Consent management: store consent records in an append-only, integrity-verified log; never allow deletion of a consent event.
- Retention and deletion: automated scheduled jobs; verify execution with a monitoring check that alerts on failures.

**Technical Controls for Compliance Integrity**
- Sign all policy and configuration fetched from remote sources; verify the signature before applying.
- Implement audit logging for all compliance-critical events (consent changes, data exports, deletion requests, cross-border transfers).
- Regularly test compliance controls (deletion schedules, data subject request workflows) in production-equivalent environments.

**Threat-Modelling Integration**
- Add a compliance column to the threat model register: for each threat, assess whether a successful attack would produce a regulatory violation.
- Review the threat model when: regulations are updated, a new data type is introduced, a new jurisdiction is served, or a new third-party processor is engaged.

**OWASP Mappings**
- MASVS: PRIVACY-3, PRIVACY-4
- MASTG: TEST-0004, TEST-0318, TEST-0319
- MASWE: MASWE-0111, MASWE-0112, MASWE-0115
