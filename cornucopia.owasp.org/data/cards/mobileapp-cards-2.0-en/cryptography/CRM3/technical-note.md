## Technical Note: Emery can access data because it has been obfuscated rather than using an approved cryptographic function

### Platform Guidance

**Android:** Do not call Base64, XOR, or “light obfuscation” encryption; use vetted crypto APIs with managed keys.

```kotlin
val encrypted = Cipher.getInstance("AES/GCM/NoPadding").run {
init(Cipher.ENCRYPT_MODE, secretKey)
doFinal(plaintext)
}
```

**iOS:** Replace custom encoding tricks with CryptoKit or CommonCrypto primitives that provide real confidentiality.

```swift
let sealed = try AES.GCM.seal(data, using: key)
let ciphertext = sealed.combined!
```

### Relevant Tests

**Legacy Tests:** MASTG-TEST-0014, MASTG-TEST-0061
**New Tests:** MASTG-TEST-0205, MASTG-TEST-0211

### MASWE Weaknesses

- MASWE-0010, MASWE-0023: use of obfuscation or encoding where actual encryption is required.
