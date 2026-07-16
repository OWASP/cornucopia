## Technical Note: Carlos can reverse engineer the app because the anti-reverse engineering controls aren't strong enough according to what is recommended or the perceived effort of a potential attacker

### Platform Guidance

**Android:** Raise reverse-engineering cost with shrinking, string handling discipline, native boundary review, and secret minimization rather than magic amulets.

```kotlin
buildTypes {
release {
    minifyEnabled true
    shrinkResources true
    proguardFiles getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro"
}
}
```

**iOS:** Strip symbols, avoid embedding secret material, and separate trust decisions from client-only logic that reverse engineers can map in one lunch break.

```swift
STRIP_SWIFT_SYMBOLS = YES
DEAD_CODE_STRIPPING = YES
```

### Relevant Tests

**Legacy Tests:** MASTG-TEST-0048, MASTG-TEST-0091
**New Tests:** MASTG-TEST-0263, MASTG-TEST-0220

### MASWE Weaknesses

- MASWE-0093, MASWE-0107: reverse-engineering resistance and exposure of logic or secrets through build artefacts.
