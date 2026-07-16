## Technical Note: Sherif can influence or alter controls against reverse engineering and runtime protection and can therefore bypass them

### Platform Guidance

**Android:** Assume the attacker will target your protections directly: validate configuration, detect hook frameworks, and let the server revoke trust when protections disappear.

```kotlin
val hookingArtifacts = listOf("frida", "xposed")
if (runningProcesses().any { name -> hookingArtifacts.any(name::contains) }) {
reportTamperAndLock()
}
```

**iOS:** Protect anti-tamper configuration with signatures and move final trust decisions off-device whenever you can.

```swift
if dylibScanner.loadedImages().contains(where: { $0.contains("Frida") }) {
throw IntegrityError.instrumented
}
```

### Relevant Tests

**Legacy Tests:** MASTG-TEST-0046, MASTG-TEST-0089
**New Tests:** MASTG-TEST-0325, MASTG-TEST-0261

### MASWE Weaknesses

- MASWE-0098: bypass of anti-reverse-engineering and runtime-protection controls themselves.
