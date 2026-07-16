## Technical Note: Juan can bypass jailbreak and root detection and execute administrative functions to bypass integrity checks and access controls and trigger app functionality

### Platform Guidance

**Android:** Treat root detection as a risk signal, combine file, property, and execution checks, and revalidate before privileged operations.

```kotlin
val rooted = listOf("/system/xbin/su", "/system/bin/su").any { File(it).exists() }
if (rooted) lockSensitiveFeatures()
```

**iOS:** Detect jailbreak indicators and pair them with integrity signals before allowing administrative or trust-sensitive features.

```swift
let suspiciousPaths = ["/Applications/Cydia.app", "/bin/bash"]
let jailbroken = suspiciousPaths.contains { FileManager.default.fileExists(atPath: $0) }
```

### Relevant Tests

**Legacy Tests:** MASTG-TEST-0045, MASTG-TEST-0088
**New Tests:** MASTG-TEST-0265, MASTG-TEST-0241

### MASWE Weaknesses

- MASWE-0095: root/jailbreak detection gaps that weaken integrity and access-control assumptions.
