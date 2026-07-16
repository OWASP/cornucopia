## Platform-Aware Review Guidance

**In-App Rights Mechanisms**
- Account deletion: provide a self-service deletion flow in settings; do not require contacting support for deletion.
- Data export: provide a machine-readable (JSON, CSV) export of the user's personal data on request.
- Consent withdrawal: toggling off marketing or analytics consent must stop the relevant data collection within the same session.

**Regulatory Requirements**
- GDPR Article 17 (Right to Erasure): provide a mechanism; respond within 30 days; erasure from backups within 90 days is acceptable with documentation.
- GDPR Article 7(3): withdrawal of consent must be as easy as giving consent.
- CCPA/CPRA: opt-out of sale/sharing of personal information must be one click from the app's homepage or settings.

**Technical Implementation**
- Account deletion: soft-delete with a 30-day window (reversible), then hard-delete including associated PII from all datastores.
- Consent ledger: log all consent events (grant, withdraw, scope, timestamp) in a consent management system.
- Re-consent: when the app's data practices change, present a re-consent modal before proceeding to the new feature.

**Testing**
- Delete a test account and verify PII is removed from all production datastores within the documented timeframe.
- Withdraw a consent and verify the corresponding data collection stops immediately.
- Update the app with a new data use; verify the re-consent flow is presented to existing users.

**OWASP Mappings**
- MASVS: PRIVACY-1, PRIVACY-4
- MASTG: TEST-0024, TEST-0069, TEST-0254, TEST-0255, TEST-0256, TEST-0257, TEST-0360, TEST-0361, TEST-0362, TEST-0363
- MASWE: MASWE-0113, MASWE-0114, MASWE-0115, MASWE-0117
