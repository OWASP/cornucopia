## Technical Note: Garth can reduce app users' privacy because the app is not transparent about the app's data collection and usage in a concise, easily accessible and understandable way

### Platform Guidance

**Android:** Present collection and processing notices in context, before the data is captured, and keep the wording tied to what the code actually does.

```kotlin
showPrivacyNotice(
title = "Why we need location",
summary = "Used only to show nearby ATMs during active sessions."
)
```

**iOS:** Make privacy disclosures concise, localized, and reachable from the screen where the user grants access, not buried in a novel-shaped settings page.

```swift
privacyLabel.text = "We use location only to show nearby branches during active use."
```

### Relevant Tests

**Legacy Tests:** -
**New Tests:** MASTG-TEST-0206, MASTG-TEST-0318, MASTG-TEST-0362

### MASWE Weaknesses

- MASWE-0108, MASWE-0113: transparency and notice weaknesses around personal-data collection and use.
