## Platform-Aware Review Guidance

**Android**
- Audit all `Runtime.exec()`, `ProcessBuilder`, and `Runtime.getRuntime().exec()` calls for user-supplied input.
- Replace string-concatenated commands with typed API calls where possible (e.g., use `PackageManager` instead of `pm list packages` via exec).
- Remove diagnostic activities, services, and broadcast receivers from production manifests using product flavors: `debugImplementation` / `releaseImplementation`.

**iOS**
- Avoid `system()`, `popen()`, and `NSTask`/`Process` with untrusted input.
- Deep-link handlers: validate all URL parameters against a strict allowlist before using them in any function call.
- Remove debug URL schemes from the production `Info.plist`.

**Testing**
- Enumerate all deep-link schemes and inject shell metacharacters (`; & | $()`) into every parameter; observe for unexpected process spawning.
- Review production APK/IPA manifests for diagnostic or debug entry points that were not removed.
- Static analysis: grep for `Runtime.exec`, `ProcessBuilder`, `system(`, `popen` with variable arguments.

**OWASP Mappings**
- MASVS: AUTH-1
- MASTG: TEST-0025, TEST-0033, TEST-0078
- MASWE: (see MASVS references above)
