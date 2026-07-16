## Platform-Aware Review Guidance

**Android**
- Audit all `Class.forName()`, `ClassLoader.loadClass()`, and `Intent.setClassName()` calls; verify the class name is not derived from `SharedPreferences`, extras, or external storage.
- Remove debug classes from release builds using ProGuard rules or product flavors.
- Validate all values read from `SharedPreferences` and external storage with strict type and value checks before use.
- If configuration files must be used, compute and verify an HMAC over the file content before applying it.

**iOS**
- `NSClassFromString()` with untrusted input is dangerous; restrict usage to compile-time constants.
- `NSKeyedUnarchiver` with `requiresSecureCoding = false` is a deserialization risk; use `requiresSecureCoding = true` and an `NSSecureCoding` allowlist.
- Validate all values read from `UserDefaults` with strict type assertions before use.

**Testing**
- On a rooted device, modify `SharedPreferences` / `UserDefaults` values to unexpected class names and observe app behaviour.
- Static analysis: grep for `Class.forName`, `ClassLoader.loadClass`, `NSClassFromString` with variable arguments.
- Review all data read from shared preferences and external storage that influences control flow.

**OWASP Mappings**
- MASVS: CODE-4, STORAGE-1
- MASTG: TEST-0002
- MASWE: MASWE-0082
