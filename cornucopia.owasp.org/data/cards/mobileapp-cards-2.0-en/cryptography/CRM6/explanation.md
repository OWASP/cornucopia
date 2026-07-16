## Scenario: Kouti can extract sensitive data because the cryptographic key is hardcoded or stored insecurely in local, internal, or external storage

Consider a scenario where Kouti decompiles the app and finds a string constant `private static final String KEY = "MyS3cr3tK3y1234!"`. This is the AES key used to encrypt all stored user data. The key is in the APK. The APK is downloadable from the Play Store. Kouti decrypts every user's data. The encryption was correct. The key management was not.

1. Hardcoded keys in the APK/IPA binary are extractable by static analysis.
2. Keys stored in `SharedPreferences`, `NSUserDefaults`, or unprotected files on internal storage are accessible on rooted/jailbroken devices.
3. Keys derived from static values (app name, package name, user ID) are predictable.

### Example

Kouti uses jadx to decompile the app and searches for `AES`, `Cipher`, and `Key` in the decompiled source. She finds:
```java
private static final byte[] KEY = "th1s1sth3k3y1234".getBytes();
Cipher c = Cipher.getInstance("AES/CBC/PKCS5Padding");
c.init(Cipher.ENCRYPT_MODE, new SecretKeySpec(KEY, "AES"));
```
She copies the key, decrypts the captured ciphertext from a backup, and reads all stored user data. The encryption algorithm was standard. The key storage was not.

## Threat Modeling

### STRIDE

This scenario falls under **Information Disclosure**.

A hardcoded or insecurely stored key is equivalent to no key at all for an attacker who can access the app binary or device storage. All data encrypted with the exposed key is retroactively compromised.

### What can go wrong?

- All data encrypted with the hardcoded key is decryptable by anyone who decompiles the app.
- A key stored in `SharedPreferences` or an unprotected file is readable by any app with root access.
- Key rotation is impossible for hardcoded keys; all historical data is permanently compromised.

### What are we going to do about it?

- Generate cryptographic keys using the platform's hardware-backed keystore: Android `KeyStore`, iOS Secure Enclave.
- Never hardcode cryptographic keys, passwords, or key-derivation inputs in source code or configuration files.
- For keys that must be distributed (e.g., server public keys), pin the public key in the binary — it is not secret — and use asymmetric encryption.
- For symmetric keys that must be derived: use PBKDF2 or Argon2 with a user-provided password and a hardware-bound salt; never use a static salt.
