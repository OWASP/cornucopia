## Scenario: Elsa can reduce app users' privacy because the app does not allow users to easily manage, delete, or modify their data, change privacy settings, or re-prompt for consent when more data is required

Consider a scenario where Elsa wants to delete her account on a fitness app. She navigates to settings, then account settings, then privacy settings, then finds a small-print "contact us to delete" instruction. She emails the address. Three weeks later she has received no response. The app continues to use her data. Elsa's right to erasure (GDPR Article 17) is technically offered — you can ask — but effectively denied by the process.

1. Privacy rights that require contacting support and waiting weeks are not "easily manageable."
2. Consent that cannot be withdrawn easily is not valid ongoing consent under GDPR.
3. Permission management buried in system settings rather than the app itself creates friction that discourages users from exercising their rights.

### Example

Elsa later finds the app has added a new feature that requires sharing her location data with third-party advertisers. The app's update notes say "we've added new features." There is no re-consent prompt for the expanded data use. Elsa's original consent did not cover this use. The app silently began sending her location to advertisers without asking. The legal requirement for re-consent when purposes change is clear; the implementation was not.

## Threat Modeling

### STRIDE

This scenario falls under **Information Disclosure** and involves privacy rights violations.

Users whose rights are not effectively exercisable suffer harms to autonomy, trust, and — depending on the data — real-world consequences from data sharing they cannot control.

### What can go wrong?

- Users cannot delete their accounts or data; data is retained beyond the user's intent.
- Consent for new data uses is not sought; expanded collection proceeds without authorisation.
- Privacy settings changes are not applied promptly or at all.
- Regulatory fines and enforcement actions for failure to implement data subject rights.

### What are we going to do about it?

- Implement in-app account deletion that takes effect within a reasonable timeframe (24–72 hours for user-visible deletion; 30 days for permanent erasure including backups).
- Provide accessible privacy settings that allow toggling of non-essential data collection and marketing communications.
- Implement re-consent flows when new data uses are introduced that were not covered by the original consent.
- Log and fulfil data subject requests within regulatory timeframes (GDPR: 30 days; CCPA: 45 days).
