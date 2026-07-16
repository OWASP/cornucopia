## Platform-Aware Review Guidance

**Android**
- Emulator heuristics: check `Build.FINGERPRINT.startsWith("generic")`, `Build.PRODUCT` contains "sdk", `Build.HARDWARE` contains "goldfish" or "ranchu", IMEI is all zeros.
- Sensor availability: emulators often lack real sensor data (accelerometer, gyroscope near-zero values, no battery variation).
- Google Play Integrity API: `MEETS_DEVICE_INTEGRITY` verdict indicates a physical, certified Android device; `MEETS_VIRTUAL_INTEGRITY` indicates a virtual environment.
- Combine heuristics with server-side attestation for higher confidence.

**iOS**
- Simulators: `TARGET_OS_SIMULATOR` compile-time flag identifies the iOS Simulator (Xcode only, not a threat model concern for production).
- Jailbroken devices are a more relevant threat than simulators on iOS for production apps.
- App Attest: validates the device is a genuine Apple device; attestation tokens are verified server-side via Apple's attestation service.

**Note on false positives**
- Emulator detection heuristics can produce false positives on legitimate testing devices or virtual machines used by enterprise MDM.
- Document acceptable false-positive rates and have a manual review path for edge cases.

**Testing**
- Run the app in the Android Emulator and verify the detection mechanism identifies the virtual environment.
- Test the Play Integrity API response handling for virtual environment verdicts.

**OWASP Mappings**
- MASVS: RESILIENCE-1
- MASTG: TEST-0049, TEST-0092, TEST-0351, TEST-0367
- MASWE: MASWE-0098, MASWE-0099
