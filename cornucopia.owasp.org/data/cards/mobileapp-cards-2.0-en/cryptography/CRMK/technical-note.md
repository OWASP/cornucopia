## Platform-Aware Review Guidance

**Android**
- AES-GCM: `cipher.doFinal(ciphertext)` throws `AEADBadTagException` on authentication failure — this exception cannot be overridden by hooking `doFinal` to return a boolean, because the exception propagation itself would need to be suppressed.
- `MessageDigest.isEqual()`: a constant-time comparison; hookable, but hooking it is harder to suppress cleanly. Prefer AEAD modes over separate MAC verification.
- Detect Frida: check for `/data/local/tmp/frida-server`, unusual named pipes, and `frida` in `/proc/self/maps`.

**iOS**
- `CryptoKit.AES.GCM.open(_:using:)` throws on authentication failure; the throw must be caught and suppressed for the bypass to work — this is detectable.
- Secure Enclave signature verification: `SecKeyVerifySignature` — the verification is performed in hardware; the result propagation through the software stack is hookable but requires more sophisticated attack.
- Detect Frida/Substrate: scan `_dyld_get_image_name` for known injection library paths.

**Testing**
- Hook the MAC/signature verification function with Frida and override the result; verify the app's AEAD exception is not suppressible (i.e., the app throws before the override is effective).
- Test with Frida: override `AEADBadTagException` suppression and verify the app still rejects the data (ideally by crashing or returning an error).

**OWASP Mappings**
- MASVS: CODE-4, CRYPTO-1, CRYPTO-2
- MASTG: TEST-0014, TEST-0061, TEST-0062
- MASWE: MASWE-0016
