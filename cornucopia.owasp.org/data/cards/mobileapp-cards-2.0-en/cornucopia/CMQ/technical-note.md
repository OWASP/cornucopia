## Platform-Aware Review Guidance

**Android**
- Google Play Integrity API: `integrityManager.requestIntegrityToken(nonce)` returns a signed verdict; `APP_INTEGRITY` confirms the binary matches the Play Store version.
- Verify the attestation token server-side using Google's public key; do not trust a client-side attestation result.
- Signing certificate check: `PackageManager.getPackageInfo(packageName, GET_SIGNATURES)` — verify the signing certificate hash matches the expected value.

**iOS**
- App Attest (`DCAppAttestService`): hardware-rooted attestation verified by Apple's servers.
- App Store code signature enforcement: effective on non-jailbroken devices; jailbreak detection is a defence-in-depth.

**Distribution Monitoring**
- Register your app's package name and developer identity with major APK search sites.
- Use brand-protection services to scan for unofficial redistributions.
- Set up Google Play Alerts for your package name on third-party stores.

**Testing**
- Modify the APK binary, resign, and install; verify the app detects the integrity violation via attestation.
- Test the Play Integrity API verdict handling for each verdict category.

**OWASP Mappings**
- MASVS: CODE-4, RESILIENCE-2, RESILIENCE-4
- MASTG: TEST-0002, TEST-0047, TEST-0048, TEST-0050, TEST-0090, TEST-0091, TEST-0338, TEST-0341, TEST-0354, TEST-0387
- MASWE: MASWE-0105, MASWE-0107
