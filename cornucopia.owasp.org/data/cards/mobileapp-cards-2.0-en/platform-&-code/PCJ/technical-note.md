## Technical Note: Johan can modify or expose sensitive data by exploiting weaknesses in the SDK or third party libraries because updates to the app and platform are not enforced or do not patch known software vulnerabilities

### Platform Guidance

**Android:** Pin dependency versions, reject vulnerable SDK releases in CI, and fail builds when SBOM or dependency scans flag known issues.

```kotlin
dependencies {
implementation("com.squareup.okhttp3:okhttp:4.12.0")
}

configurations.all {
resolutionStrategy.failOnVersionConflict()
}
```

**iOS:** Use Swift Package Manager or CocoaPods with locked versions, review advisory feeds, and remove abandoned libraries before they become a surprise co-maintainer.

```swift
// Package.resolved should be committed
.package(url: "https://github.com/realm/realm-swift.git", exact: "10.54.0")
```

### Relevant Tests

**Legacy Tests:** MASTG-TEST-0036, MASTG-TEST-0042, MASTG-TEST-0080, MASTG-TEST-0085
**New Tests:** MASTG-TEST-0272, MASTG-TEST-0392, MASTG-TEST-0275

### MASWE Weaknesses

- MASWE-0078, MASWE-0086: outdated libraries, insecure SDK use, and dependency governance gaps.
