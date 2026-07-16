## Platform-Aware Review Guidance

**Android**
- Self-integrity check: compute SHA-256 of `getApplicationContext().getPackageCodePath()` and compare against an expected value embedded in native code.
- Distribute checks across multiple native functions called from different places in the code; use indirect calls to make the check locations less obvious.
- Combine check with key derivation: `derivedKey = HKDF(masterKey, computedHash)` — if the hash is wrong, the key is wrong, and decryption fails naturally.
- Google Play Integrity API verdict `APP_INTEGRITY` includes binary integrity attestation; verify server-side.

**iOS**
- App Attest provides hardware-rooted attestation verified by Apple's servers; use it to confirm the binary is unmodified.
- Code signature verification is enforced by the OS on non-jailbroken devices.
- On jailbroken devices, integrity check bypass is possible; use attestation-based remote verification as the primary integrity control.

**Testing**
- Patch each integrity check to return `true`; verify that other controls (key derivation, server attestation) still detect the modification.
- Test the Play Integrity API / App Attest failure handling: simulate a failed attestation and verify the app escalates to remote verification.

**OWASP Mappings**
- MASVS: RESILIENCE-2, RESILIENCE-4
- MASTG: TEST-0048, TEST-0050, TEST-0091, TEST-0341, TEST-0354
- MASWE: MASWE-0107
