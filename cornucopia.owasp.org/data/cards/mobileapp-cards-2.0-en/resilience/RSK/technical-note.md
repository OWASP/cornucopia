## Platform-Aware Review Guidance

**Android**
- Distribute protection checks in multiple locations in the codebase; do not consolidate in one easily-targeted class.
- Obfuscate protection class and method names with ProGuard; use string obfuscation for detection strings.
- Implement protection checks in native code with symbol stripping to increase analysis difficulty.
- Use Play Integrity API for a server-verifiable, hardware-rooted integrity check that cannot be subverted by hooking.

**iOS**
- Use App Attest for server-verifiable attestation; it is verified by Apple's servers, not by on-device code.
- Distribute checks using Swift computed properties and lazy initializers spread across multiple files.
- Obfuscate check results: instead of `isJailbroken = true`, corrupt a key derivation input.

**Architectural Principle**
- Anti-tampering and anti-debugging controls are deterrents, not security boundaries.
- The primary security boundary must be hardware-backed key storage; resilience controls raise the cost of attacking that boundary.
- Document this distinction in the threat model; do not rely on resilience controls as the last line of defence for cryptographic keys or credentials.

**OWASP Mappings**
- MASVS: RESILIENCE-4
- MASTG: TEST-0046, TEST-0089
- MASWE: MASWE-0102, MASWE-0103
