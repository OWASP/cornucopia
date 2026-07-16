## Platform-Aware Review Guidance

**Android (Root Detection)**
- Check for: `su` binary in common paths (`/system/bin/su`, `/system/xbin/su`), build tag (`ro.build.tags == test-keys`), dangerous system apps (SuperUser.apk), writable system partitions.
- `SafetyNet / Play Integrity API`: `MEETS_DEVICE_INTEGRITY` verdict; use server-side verification of the integrity token.
- Detect Magisk: check for Magisk Manager package, `/sbin/.magisk` path, or Magisk's socket interfaces.

**iOS (Jailbreak Detection)**
- Check for: Cydia/Sileo application bundle, writable `/private/`, presence of common Cydia Substrate paths, `sysctl` MIB for sandbox violation, `fork()` success (sandboxed processes cannot fork).
- `DCAppAttestService` (App Attest): server-verified attestation that the device is genuine and unmodified.
- Detect Frida: scan loaded dylibs for Frida agent paths, listen port 27042 check.

**Defensive Strategy**
- Root/jailbreak detection cannot be made absolute; hiding tools specifically counter known detection methods.
- Use detection as a risk signal that triggers server-side additional verification, not as a security boundary.
- Prioritize hardware-backed key storage: keys in Secure Enclave / StrongBox are not extractable even on jailbroken/rooted devices.

**Testing**
- Test on a jailbroken device with A-Bypass / RootCloak enabled; verify the app's core security controls (cryptographic operations) still require authentication.
- Verify the attestation token reaches the server and is verified.

**OWASP Mappings**
- MASVS: RESILIENCE-1
- MASTG: TEST-0045, TEST-0088, TEST-0240, TEST-0241, TEST-0324, TEST-0325
- MASWE: MASWE-0097, MASWE-0100
