## Platform-Aware Review Guidance

**Android (Java/Kotlin)**
- Use `char[]` instead of `String` for passwords and sensitive text; zero with `Arrays.fill(array, '\0')` immediately after use.
- `SecretKeySpec`: clear key material with `key.destroy()` (where supported by the provider).
- Pin entry via `EditText`: extract characters immediately, copy to a `char[]`, clear the `EditText`, and process the `char[]`.
- Avoid `String.format()` or string concatenation with sensitive values; the intermediate strings are not controllable.

**iOS (Swift/Objective-C)**
- Swift `String` is a value type backed by a heap buffer; use `Data` or `UnsafeMutableRawPointer` for sensitive buffers and zero with `data.resetBytes(in: 0..<data.count)`.
- `SecureEnclave`-backed key operations: the key material never leaves the Enclave; only the result of cryptographic operations is in application memory.
- `LAContext` credentials: zero any `String` passed as a `localizedReason` after the prompt returns.

**Testing**
- After a payment or login session, capture a heap dump (`adb shell am dumpheap <pid> dump.hprof`) and search for sensitive patterns.
- Use a memory scanning tool (e.g., Volatility with an Android profile) on a forensics image.
- Review crash report configurations to verify heap dumps or full memory snapshots are not included.

**OWASP Mappings**
- MASVS: STORAGE-2
- MASTG: TEST-0011, TEST-0060
- MASWE: (see MASVS references above)
