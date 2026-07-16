## Platform-Aware Review Guidance

**Android**
- Review `AndroidManifest.xml` for every `<uses-permission>` declaration; map each to a specific feature in a permission register.
- Use `android:maxSdkVersion` to withdraw permissions that are no longer needed on newer API levels.
- Prefer the Photo Picker (`ActivityResultContracts.PickVisualMedia`) over `READ_EXTERNAL_STORAGE`.
- Use `ACCESS_COARSE_LOCATION` instead of `ACCESS_FINE_LOCATION` where street-level accuracy is sufficient.
- Detect merged SDK permissions: `./gradlew :app:processDebugMergedManifest`

**iOS**
- Every `NS*UsageDescription` key in `Info.plist` must have a clear, functional justification.
- Prefer `PHAuthorizationStatusLimited` (limited photo access, iOS 14+) over full photo library access.
- For location, declare `NSLocationWhenInUseUsageDescription` and request Always only when a background feature strictly requires it.
- App Store review checks that declared usage matches the actual feature; misleading descriptions risk rejection.

**Testing**
- Run `aapt dump permissions <apk>` or use MobSF to enumerate all declared permissions.
- Install the app with all permissions denied; verify all core features still function correctly.
- On iOS, review the Privacy Report (Settings → Privacy & Security → App Privacy Report) to see which permissions were actually exercised during testing.

**OWASP Mappings**
- MASVS: PLATFORM-1, PRIVACY-1
- MASTG: TEST-0024, TEST-0069, TEST-0254, TEST-0255, TEST-0256, TEST-0257, TEST-0360, TEST-0361, TEST-0362, TEST-0363
- MASWE: MASWE-0117
