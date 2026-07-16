## Technical Note: Timur can change the code of the production release because the code of the application has not been properly signed using a valid production certificate

### Platform Guidance

**Android:** Sign release builds with the production certificate only inside the trusted release pipeline and reject unsigned or debug-signed artifacts.

```kotlin
signingConfigs {
release {
    storeFile file(System.getenv("ANDROID_KEYSTORE"))
    storePassword System.getenv("ANDROID_KEYSTORE_PASSWORD")
}
}
```

**iOS:** Use distribution certificates in the release process, keep them in secure CI secrets, and verify signature trust before distribution.

```swift
CODE_SIGN_STYLE = Manual
CODE_SIGN_IDENTITY = Apple Distribution
```

### Relevant Tests

**Legacy Tests:** MASTG-TEST-0038, MASTG-TEST-0081
**New Tests:** MASTG-TEST-0226, MASTG-TEST-0353, MASTG-TEST-0387

### MASWE Weaknesses

- MASWE-0089, MASWE-0103: code-signing integrity and production release authenticity.
