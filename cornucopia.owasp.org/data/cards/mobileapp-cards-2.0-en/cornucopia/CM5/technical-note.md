## Technical Note: Debarghaya can reduce app users' privacy because the app repurpose personal information (e.g. device IDs, IP addresses, behavioral patterns) collected for security concerns in order to cater for commercial interests without consent

### Platform Guidance

**Android:** Do not quietly reuse device identifiers, IP history, or fraud telemetry for marketing, personalization, or monetization without explicit consent and governance.

```kotlin
if consentStore.allows(.marketingReuse) {
analytics.send(marketingPayload)
}
```

**iOS:** Separate security telemetry from commercial analytics in both storage and policy so one dataset does not moonlight as the other.

```swift
guard consent.marketingReuse == true else { return }
marketingClient.send(payload)
```

### Relevant Tests

**Legacy Tests:** -
**New Tests:** MASTG-TEST-0256, MASTG-TEST-0360

### MASWE Weaknesses

- MASWE-0111, MASWE-0117: purpose-limitation failures for personal data originally collected for security.
