## Technical Note: Abdullah can bypass authentication by altering the usual process sequence or flow, or by undertaking the process in incorrect order, or by manipulating date and time values used by the app, or by using valid features for unintended purposes

### Platform Guidance

**Android:** Keep the business flow state machine on the server or in signed state, validate timestamps, and reject actions that arrive out of order.

```kotlin
enum class EnrollmentState { STARTED, OTP_VERIFIED, PIN_SET }
require(serverState == EnrollmentState.OTP_VERIFIED)
require(clock.instant() < challengeExpiry)
```

**iOS:** Do not trust client-controlled time or navigation sequence for authorization decisions; make the backend confirm the allowed next step.

```swift
guard flowState == .otpVerified, Date() < challenge.expiry else {
throw FlowError.invalidState
}
```

### Relevant Tests

**Legacy Tests:** MASTG-TEST-0034, MASTG-TEST-0079
**New Tests:** MASTG-TEST-0266

### MASWE Weaknesses

- MASWE-0032, MASWE-0044: workflow manipulation, time abuse, and sequencing weaknesses in authentication journeys.
