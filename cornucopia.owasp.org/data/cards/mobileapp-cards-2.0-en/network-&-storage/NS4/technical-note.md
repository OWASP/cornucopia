## Platform-Aware Review Guidance

**Android**
- `KeyguardManager.isDeviceSecure()` returns `true` if the device has a secure lock screen; gate sensitive features on this check.
- `DevicePolicyManager`: enterprise deployments can enforce screen-lock timeout and minimum password complexity.
- File-based encryption (FBE, default since Android 7): user data in the `DE` (Device Encrypted) storage is protected by the lock screen credential; use `CE` (Credential Encrypted) storage for sensitive app files.
- USB debugging: not controllable by the app directly, but document in the threat model; enterprise MDM can disable it.

**iOS**
- `UIDevice.current.isPasscodeSet` (via LocalAuthentication `LAContext.canEvaluatePolicy`) — check whether a passcode is set.
- iOS enforces data protection classes on files; use `NSFileProtectionCompleteUntilFirstUserAuthentication` or `NSFileProtectionComplete` for sensitive files. `NSFileProtectionNone` should never be used for sensitive data.
- `UIFileSharingEnabled = false` in `Info.plist` — prevents iTunes/Finder file sharing.

**Testing**
- Remove the device PIN and verify the app detects the absence of a screen lock and restricts access to sensitive data.
- Connect a device without ADB authorization prompt (USB debugging on, no lock) and attempt `adb pull /data/data/com.target.app/`; verify the data is inaccessible without device unlock.

**OWASP Mappings**
- MASVS: RESILIENCE-1, STORAGE-1
- MASTG: TEST-0012, TEST-0246, TEST-0247, TEST-0248, TEST-0249
- MASWE: MASWE-0008
