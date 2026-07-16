## Scenario: Elizabeth can reduce app users' privacy because the app sends too much personal data without the user's consent to downstream services that are outside the user's control

Consider a scenario where Elizabeth is a privacy researcher. She proxies the traffic from a popular social media app and observes it sending her precise GPS coordinates to four different third-party advertising SDKs with every API call. The app's privacy policy mentions "we may share data with partners for advertising purposes." Elizabeth is sharing her real-time location with advertisers she has never heard of, in countries with different privacy laws, without ever being asked for explicit consent for this specific use. The privacy policy covered it in one sentence.

1. Third-party SDKs embedded in apps transmit user data to their own servers, often without the developer's detailed awareness.
2. Bundled advertising and analytics SDKs send detailed device fingerprints, location, and behavioural data to servers outside the developer's control.
3. Data minimization — sending only the minimum data needed for each purpose — is a regulatory requirement that is often not implemented.

### Example

Elizabeth finds the app sends `{"device_id": "...", "location": {"lat": ..., "lng": ...}, "user_id": "...", "session_duration": ..., "screen_views": [...]}` to `analytics.thirdparty.com` on every screen view. The user consented to "analytics to improve the app." They did not consent to sharing precise location, session behaviour, and screen-view history with a third party that aggregates it with data from thousands of other apps to build a detailed profile. The consent was too vague to cover the actual data sharing.

## Threat Modeling

### STRIDE

This scenario falls under **Information Disclosure**.

Personal data is transmitted to third parties beyond what the user was informed about or agreed to, violating their reasonable expectations of privacy and likely their regulatory rights.

### What can go wrong?

- Sensitive user data (location, health indicators, financial activity signals) is transmitted to advertising networks.
- Third-party SDKs are compromised and used to exfiltrate data from all apps that embed them.
- Data shared with third parties is combined with other datasets to re-identify pseudonymous users.
- Regulatory action for sending personal data to third countries without adequate safeguards (GDPR Chapter V).

### What are we going to do about it?

- Audit every third-party SDK for what data it collects and transmits; document this in the data inventory.
- Obtain specific, granular consent for each category of data sharing with each type of third party.
- Apply data minimization: send only the data each SDK needs for its stated purpose; configure SDKs to disable optional data collection.
- Review third-party SDK privacy policies and data processing agreements before integration.
