## Scenario: Starr can influence, alter, or affect the app so that it no longer complies with legal, regulatory, contractual, or other mandates

Consider a scenario where Starr is a sophisticated actor — a competitor, an activist, or a regulator — who wants to create compliance failures in the target app. Starr does not need to hack the app. She modifies data the app relies on (a configuration file, a third-party API response, a policy setting) to cause the app to process data in a way that violates a data residency requirement, a consent record, or a transaction reporting obligation. The app was compliant when it shipped. Starr made it non-compliant without touching the source code.

Alternatively, Starr is a threat to an app that has simply not kept pace with regulatory change. The app was compliant two years ago. The regulation has since been updated. The app has not.

### Example

Starr discovers that the app stores user data in a cloud region that is automatically selected based on a configuration value fetched from a remote endpoint. She performs a man-in-the-middle attack on the configuration fetch and substitutes a region that is outside the EU for users who consented to EU-only data storage. The app stores the data in the attacker-specified region. The GDPR data residency requirement is now violated for every user whose data was redirected. The app's legal team receives a regulator's inquiry. The technical cause was a single unvalidated configuration value.

## Threat Modeling

### STRIDE

This scenario falls under **Tampering** and covers a distinct harm category: regulatory non-compliance.

Regulatory compliance is often a property of the system as a whole — not just the app but also its configuration, data flows, and dependencies. Tampering with any of these can produce non-compliance without any single "hack."

### What can go wrong?

- Data residency requirements are violated by manipulating cloud-region configuration.
- Consent records are modified or lost, making previously lawful processing unlawful.
- Transaction reporting obligations are disrupted by injecting or deleting records.
- The app processes special-category data (health, biometric, financial) without the required legal basis because a consent flag was manipulated.
- Regulatory deadlines (data retention deletion schedules, breach notification windows) are missed because automated processes are interfered with.

### What are we going to do about it?

- Treat compliance-critical configuration values as security-sensitive: sign and integrity-verify all policy configuration fetched from remote sources.
- Implement compliance monitoring: automated checks that verify data residency, consent record integrity, and retention schedule execution.
- Include regulatory requirements in the threat model: identify which threats could cause compliance failures and prioritize mitigations accordingly.
- Conduct regular compliance audits and update the threat model when regulations change.
- Apply defence-in-depth: multiple independent controls for critical compliance properties, so that manipulation of one control does not alone produce non-compliance.
