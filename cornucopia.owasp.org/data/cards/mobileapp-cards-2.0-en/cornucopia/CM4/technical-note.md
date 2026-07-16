## Technical Note: Elizabeth can reduce app users' privacy because the app sends too much personal data without the user's consent to downstream services that are outside the user's control

### Platform Guidance

**Android:** Minimize fields sent to downstream services, strip optional identifiers, and request explicit consent before forwarding personal data.

```kotlin
val payload = mapOf(
"branchId" to branchId,
"coarseLocation" to location.toGridCell()
)
```

**iOS:** Design APIs so the client can send the minimum useful data rather than the entire user object wearing every identifier it owns.

```swift
struct AnalyticsPayload: Encodable {
let event: String
let coarseRegion: String
}
```

### Relevant Tests

**Legacy Tests:** -
**New Tests:** MASTG-TEST-0255, MASTG-TEST-0281

### MASWE Weaknesses

- MASWE-0110, MASWE-0115: over-collection and sharing of personal data without informed consent.
