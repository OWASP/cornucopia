## Technical Note: Sean can reverse engineer the app because the code obfuscation isn't strong enough according to what is recommended or the perceived effort of a potential attacker

### Platform Guidance

**Android:** Use R8/ProGuard with rules that actually obfuscate sensitive paths while preserving the parts you must keep for reflection.

```kotlin
-keepclassmembers class * {
@android.webkit.JavascriptInterface <methods>;
}
-obfuscationdictionary obfuscation.txt
```

**iOS:** Swift symbol stripping and release optimization help, but keep in mind obfuscation supports security; it does not replace it.

```swift
SWIFT_OPTIMIZATION_LEVEL = -Owholemodule
STRIP_SWIFT_SYMBOLS = YES
```

### Relevant Tests

**Legacy Tests:** MASTG-TEST-0051, MASTG-TEST-0093
**New Tests:** MASTG-TEST-0264, MASTG-TEST-0240

### MASWE Weaknesses

- MASWE-0094: insufficient obfuscation and easy reconstruction of sensitive client logic.
