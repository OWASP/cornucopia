## Platform-Aware Review Guidance

**Android**
- Do not load code from external storage (`Environment.getExternalStorageDirectory()`), world-writable directories, or any path not under `getFilesDir()` in production.
- Use `DexClassLoader` only with classes loaded from the APK itself or from a verified, signed source.
- Detect library injection: compare loaded `.so` paths in `/proc/self/maps` against expected app paths.

**iOS**
- iOS does not allow dynamic code loading from outside the app bundle (without entitlements); this is enforced by the OS. On jailbroken devices, this restriction is lifted.
- Detect dylib injection: enumerate loaded images with `_dyld_get_image_name` and compare against expected app frameworks.

**Cryptographic Controls**
- Perform all encryption within a hardware-backed context (StrongBox / Secure Enclave) where possible to prevent pre/post-encryption hooks.
- Use sealed sender / end-to-end encryption at the application layer so that even if the transport is compromised, the plaintext is not available at intermediate points.

**Testing**
- On a rooted device, hook the encryption function with Frida and log all plaintext inputs; verify the app detects the hook.
- Replace a shared library with a modified version from a writable path; verify the app refuses to load it.
- Review all `DexClassLoader` and `ClassLoader` usage for loading from untrusted sources.

**OWASP Mappings**
- MASVS: CRYPTO-2, NETWORK-1, RESILIENCE-3, STORAGE-1
- MASTG: TEST-0001, TEST-0052
- MASWE: MASWE-0017, MASWE-0096
