## Technical Note: Ricardo can extract data stored by the app on a stolen or decommissioned device  because it does not enforce device access security policies (e.g. PIN protected locking, app-/os-version, USB debug deactivation, device encryption and rooting)

### Platform Guidance

**Android:** Use device policy or application policy checks when the threat model requires a locked and encrypted device, and block operation when posture is unsafe.

```kotlin
val km = getSystemService(KeyguardManager::class.java)
val dm = getSystemService(DevicePolicyManager::class.java)
require(km.isDeviceSecure && dm.storageEncryptionStatus == DevicePolicyManager.ENCRYPTION_STATUS_ACTIVE)
```

**iOS:** On iOS, rely on Data Protection classes and app policy to ensure data remains unavailable until the device is unlocked.

```swift
let attributes: [FileAttributeKey: Any] = [
.protectionKey: FileProtectionType.complete
]
try FileManager.default.setAttributes(attributes, ofItemAtPath: filePath)
```

### Relevant Tests

**Legacy Tests:** MASTG-TEST-0012
**New Tests:** MASTG-TEST-0202, MASTG-TEST-0306, MASTG-TEST-0303

### MASWE Weaknesses

- MASWE-0003: device access policy and local storage exposure on lost or decommissioned devices.
