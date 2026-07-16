## Platform-Aware Review Guidance

**Android**
- Set `FLAG_SECURE` on all Activities displaying sensitive data:
  `window.setFlags(WindowManager.LayoutParams.FLAG_SECURE, WindowManager.LayoutParams.FLAG_SECURE)`
- Set the flag before `setContentView` to avoid a brief unprotected frame.
- Jetpack Compose: apply the flag in the hosting `Activity`; it covers the entire window.

**iOS**
- Observe `UIApplicationDelegate.applicationWillResignActive(_:)` and add a blurred or opaque overlay view to the key window; remove it in `applicationDidBecomeActive(_:)`.
- SwiftUI: observe the `scenePhase` environment variable and swap to a privacy placeholder when `.inactive`.
- `UITextField.isSecureTextEntry = true` hides keyboard content but does not protect surrounding fields.

**Testing**
- Background the app mid-session, open the app switcher, and photograph or record the preview.
- On Android, run `adb shell screencap` while the app is in the background.
- On a jailbroken iOS device, inspect `/var/mobile/Library/SpringBoard/SnapShots/`.

**OWASP Mappings**
- MASVS: PLATFORM-3, STORAGE-2
- MASTG: TEST-0010, TEST-0059, TEST-0289, TEST-0290, TEST-0291, TEST-0292, TEST-0293, TEST-0294
- MASWE: MASWE-0055
