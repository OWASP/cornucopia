## Platform-Aware Review Guidance

**Android**
- Enable `minifyEnabled true` and configure comprehensive ProGuard rules.
- Add string encryption for hardcoded secrets using a ProGuard-compatible string-obfuscation library.
- Move security-critical logic to native code compiled with symbol stripping.
- Static analysis of the release APK: decompile with jadx and review any remaining readable class names or string constants.

**iOS**
- Swift binaries retain some type metadata even in release builds; this is a known limitation.
- LLVM obfuscation passes (e.g., Hikari/LLVM-Obfuscator) can be applied for high-security apps.
- `strings YourApp.app/YourApp | grep -i "api\|key\|secret\|token"` — verify no sensitive strings are readable from the binary.

**All Platforms**
- The primary defence against credential extraction is not to put secrets in the binary in the first place.
- Anti-analysis controls (obfuscation, string encryption) raise the cost of reverse engineering but cannot be made absolute.
- Document the threat model and the acceptable effort threshold.

**OWASP Mappings**
- MASVS: RESILIENCE-3, RESILIENCE-4
- MASTG: TEST-0048, TEST-0091
- MASWE: MASWE-0092
