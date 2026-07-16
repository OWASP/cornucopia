## Platform-Aware Review Guidance

**Android**
- Runtime certificate check:
  ```kotlin
  val info = packageManager.getPackageInfo(packageName, PackageManager.GET_SIGNATURES)
  val cert = info.signatures[0].toCharsString()
  // Compare against expected signing certificate hash
  ```
- Google Play Integrity API: `integrityManager.requestIntegrityToken()` returns a verdict including `APP_RECOGNITION_VERDICT`; verify `PLAY_RECOGNIZED` server-side.
- `android:installLocation="internalOnly"` prevents installation to SD card, reducing the risk of APK extraction.

**iOS**
- App Attest (`DCAppAttestService`): `attestKey(keyId:clientDataHash:completion:)` produces an attestation that Apple verifies; use it to confirm the app is an unmodified App Store build.
- The App Store code signature is enforced by the OS on non-jailbroken devices; jailbroken device detection is a defence-in-depth.

**Testing**
- Modify the APK (e.g., add a log statement), re-sign with a debug key, and install; verify the app detects the invalid signature and refuses to run.
- Test the Play Integrity API response handling for each verdict category.

**OWASP Mappings**
- MASVS: RESILIENCE-2
- MASTG: TEST-0038, TEST-0081, TEST-0220, TEST-0224, TEST-0225
- MASWE: MASWE-0104, MASWE-0106
