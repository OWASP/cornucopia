## Technical Note: Anant can perform sensitive operations without additional authentication because authentication requirements are too weak or missing

### Platform Guidance

**Android:** Require step-up authentication for transfers, account changes, and other high-risk actions even if a session already exists.

```kotlin
if (riskEngine.requiresStepUp(action = "wire_transfer")) {
navigator.openReauthentication()
return
}
submitTransfer()
```

**iOS:** Model risk-based or transaction-based reauthentication explicitly instead of assuming a warm session is still good enough after a long pause.

```swift
guard session.isFreshForSensitiveAction else {
presentReauthentication()
return
}
```

### Relevant Tests

**Legacy Tests:** MASTG-TEST-0064
**New Tests:** MASTG-TEST-0330

### MASWE Weaknesses

- MASWE-0031, MASWE-0043: missing or weak additional authentication before sensitive operations.
