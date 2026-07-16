## Platform-Aware Review Guidance

**Android**
- Default ProGuard: renames identifiers but does not obfuscate strings or control flow.
- String obfuscation: use a library such as StringFog, DexGuard (commercial), or implement a custom annotation processor.
- Add ProGuard rules to remove debug log calls, retain required framework class names, and apply aggressive optimisation.
- Control flow obfuscation: R8 applies some optimisations; commercial tools (DexGuard, iXGuard) apply stronger transformations.
- Verify obfuscation: run `jadx --no-debug-info release.apk` and review the result for readable security logic.

**iOS**
- LLVM-based obfuscation passes can be applied as a build step.
- Swift and Objective-C type metadata is partially visible in release builds; this is a platform limitation.
- Strip all debug symbols and export maps from the release build.
- `strings YourApp | grep -E "^[A-Za-z0-9+/]{20,}"` — check for unobfuscated Base64-encoded secrets.

**Effectiveness Assessment**
- Obfuscation raises the cost of reverse engineering but cannot make it impossible.
- The appropriate obfuscation strength depends on the value of the protected assets and the likely attacker's capability.
- For high-value assets, combine obfuscation with hardware-backed key storage so that the secret is never in the binary.

**OWASP Mappings**
- MASVS: RESILIENCE-3
- MASTG: TEST-0051, TEST-0093, TEST-0368, TEST-0369, TEST-0391
- MASWE: MASWE-0089, MASWE-0090, MASWE-0091
