## Technical Note: Luis can influence or alter cryptographic methods to corrupt other users' data because the integrity of the encrypted data is not verified before being shared with external services

### Platform Guidance

**Android:** Verify ciphertext integrity before syncing or sharing encrypted blobs with other components or services.

```kotlin
val sealed = aead.encrypt(plaintext, aad)
api.upload(sealed)
// Receiver must decrypt and verify before use
```

**iOS:** On iOS, package encrypted data in an authenticated format and reject modified payloads before they influence shared state.

```swift
let sealed = try AES.GCM.seal(data, using: key)
try syncClient.upload(sealed.combined!)
```

### Relevant Tests

**Legacy Tests:** MASTG-TEST-0002
**New Tests:** MASTG-TEST-0209, MASTG-TEST-0372, MASTG-TEST-0228

### MASWE Weaknesses

- MASWE-0021, MASWE-0082: combined crypto and code weaknesses that let attackers corrupt other users' data or shared payloads.
