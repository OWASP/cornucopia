## Technical Note: Sam can dump sensitive data from memory because the data is not stored as primitive data types and overwritten with random data after use or because the app's input fields use insecure SDKs to store the data in RAM

### Platform Guidance

**Android:** Keep secrets in the shortest-lived buffers you can manage and overwrite them when done, especially in native or hybrid layers.

```kotlin
val secret = CharArray(pin.length)
pin.toCharArray(secret, 0, 0, pin.length)
try {
signer.useSecret(secret)
} finally {
java.util.Arrays.fill(secret, '\u0000')
}
```

**iOS:** Prefer `Data` buffers that you clear promptly and avoid caching secrets in long-lived observable state.

```swift
var secret = Data(pin.utf8)
defer { secret.resetBytes(in: 0..<secret.count) }
try signer.use(secret)
```

### Relevant Tests

**Legacy Tests:** MASTG-TEST-0011, MASTG-TEST-0060
**New Tests:** MASTG-TEST-0207, MASTG-TEST-0296, MASTG-TEST-0314

### MASWE Weaknesses

- MASWE-0006: memory disclosure and failure to clear sensitive data after use.
