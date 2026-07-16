## Platform-Aware Review Guidance

**Data Governance**
- Maintain a data inventory that records: data element, collection purpose(s), legal basis, retention period, access controls, and sharing arrangements.
- Enforce purpose limitation technically: security data and commercial data should be in separate datastores with separate access controls; cross-access should require a change-control process.
- Advertising SDKs: do not pass fraud-detection signals or device fingerprints to advertising SDKs; configure them to use only consent-based identifiers.

**Identifier Management**
- Prefer ephemeral, resettable identifiers (Android Advertising ID with user ability to reset; iOS IDFA with ATT consent) for advertising.
- For fraud detection: use server-side fraud signals where possible rather than persistent device fingerprints.
- Hashed device IDs are still personal data under GDPR if they can be linked back to an individual; treat them as such.

**Regulatory References**
- GDPR Article 5(1)(b): purpose limitation principle.
- GDPR Article 6: legal basis for each processing purpose.
- CCPA/CPRA: sensitive personal information restrictions.

**OWASP Mappings**
- MASVS: PRIVACY-2, PRIVACY-4
- MASTG: (see MASVS references above)
- MASWE: MASWE-0109, MASWE-0110
