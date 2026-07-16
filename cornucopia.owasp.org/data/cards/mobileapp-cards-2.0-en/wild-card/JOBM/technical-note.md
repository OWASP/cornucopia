## Technical Note: Mallory can use the app installed on Bob's device maliciously to surveil, spy on, eavesdrop, control remotely, track or otherwise monitor Bob, without consent and/or notification

### Platform Guidance

**Android:** Stalkerware-style abuse often starts with overbroad background permissions, exported receivers, and silent data collection. Keep sensitive capabilities user-visible and revocable.

```kotlin
val foregroundServiceIntent = Intent(this, TrackingService::class.java)
ContextCompat.startForegroundService(this, foregroundServiceIntent)
// Pair with visible disclosure and revocation UI, not stealth.
```

**iOS:** On iOS, constrain background modes, camera/microphone/location usage, and remote control features to consented, obvious user actions.

```swift
guard consent.allows(.locationTracking), appState.userInitiatedTracking else {
throw PrivacyError.missingConsent
}
```

### Relevant Tests

**Legacy Tests:** -
**New Tests:** -

### MASWE Weaknesses

- No direct MASWE mapping is defined for this wildcard card; use it to discuss privacy abuse, surveillanceware, and coerced-monitoring scenarios.
