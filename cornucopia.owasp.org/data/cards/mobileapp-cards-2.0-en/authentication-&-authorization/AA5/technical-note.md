## Platform-Aware Review Guidance

**Android**
- Use `BiometricPrompt.CryptoObject` bound to a hardware-backed key (`setIsStrongBoxBacked(true)` where available); bypassing the software check does not give access to the key.
- Detect Frida/Xposed presence: check for `/data/local/tmp/frida-server`, suspicious loaded libraries (`frida`, `xposed`), or anomalous `/proc/self/maps` entries.
- `SafetyNet / Play Integrity API` attest device integrity; fail gracefully (not crash) if attestation fails on non-sensitive operations to avoid DoS.

**iOS**
- Store authentication keys in the Secure Enclave with `kSecAttrTokenIDSecureEnclave` — hardware prevents key extraction regardless of software bypass.
- Detect Substrate / Frida: check for `_logos_meta_method`, `fishhook`, or suspicious `dylib` paths in `_dyld_get_image_name` loops.
- Detect jailbreak indicators: presence of `/usr/bin/cycript`, writable `/private`, Cydia, etc. — treat as a risk signal and escalate to remote re-auth.

**Testing**
- Use objection: `ios authentication bypass` to attempt a bypass; verify the app detects it and refuses to decrypt sensitive data.
- Use jadx/apktool to remove the authentication check from the APK; install and verify the app's cryptographic operations fail without the hardware-backed key.

**OWASP Mappings**
- MASVS: AUTH-2
- MASTG: TEST-0017, TEST-0018, TEST-0064, TEST-0266, TEST-0267, TEST-0327, TEST-0329, TEST-0330
- MASWE: MASWE-0044
