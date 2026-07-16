## Technical Note: Eiman can bypass the local authentication through patching and/or by instrumentation because the authentication can be patched out or overloaded

### Platform Guidance

**Android:** Never let local UI state be the final authority for sensitive actions; instrumentation-friendly checks should be backed by server decisions or key use that the hook cannot fake cheaply.

```kotlin
suspend fun approvePayment(challenge: ByteArray): ByteArray {
val signature = biometricBackedSigner.sign(challenge)
return api.approvePayment(signature)
}
```

**iOS:** Tie local approval to a signed server challenge or a Keychain-protected operation so a Frida script cannot simply return `true` and go for coffee.

```swift
func approve(challenge: Data) throws -> Data {
let signature = try signer.sign(challenge)
return try api.approve(signature)
}
```

### Relevant Tests

**Legacy Tests:** MASTG-TEST-0017, MASTG-TEST-0018, MASTG-TEST-0064
**New Tests:** MASTG-TEST-0329

### MASWE Weaknesses

- MASWE-0030, MASWE-0042: bypass of local-only authentication controls through patching, hooking, or instrumentation.
