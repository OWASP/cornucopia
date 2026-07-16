## Scenario: Tarik can influence or alter cryptographic operations and can therefore bypass them

Consider a scenario where Tarik has identified that the app's MAC verification function, `verifyMAC(data, mac)`, returns a boolean. He hooks the function with Frida and overrides the return value to `true`. The app proceeds as if the MAC was valid, even though Tarik has submitted arbitrary data with a forged MAC. The cryptographic operation was correct. Its result was overridden at the software level.

1. Cryptographic verification results stored as booleans or simple return values can be overridden by runtime instrumentation.
2. MAC and signature verification logic that can be hooked and overridden defeats the purpose of the verification.
3. Cryptographic operations performed outside the hardware security boundary are manipulable by anyone with process access.

### Example

Tarik uses Frida to hook `MessageDigest.isEqual(computedMAC, receivedMAC)`. He overrides the return value to `true` for all calls. The app's integrity-check logic accepts all data as authenticated. Tarik submits modified API responses with forged MACs. The app processes them as legitimate. The MAC algorithm was HMAC-SHA256 with a hardware-backed key. The verification result was a boolean in application memory.

## Threat Modeling

### STRIDE

This scenario falls under **Tampering** and **Spoofing**.

By overriding the cryptographic verification result, Tarik can make the app accept modified or forged data as authentic, bypassing the integrity and authenticity guarantees the cryptographic operation was intended to provide.

### What can go wrong?

- Modified data passes MAC/signature verification after hook injection.
- Forged certificates or tokens are accepted after verification override.
- The entire cryptographic security model depends on a single hookable boolean comparison.

### What are we going to do about it?

- Use the result of cryptographic operations directly rather than a boolean derived from them: let the decryption fail (throw an exception) if the MAC is invalid, rather than checking a boolean.
- For AES-GCM, `cipher.doFinal()` throws `AEADBadTagException` if the tag is invalid; this is not a boolean that can be overridden.
- Apply runtime integrity checks to detect Frida/hooking frameworks as a defence-in-depth measure.
- Use hardware-backed cryptographic operations (Secure Enclave / StrongBox) where the result is determined by hardware, not software-manipulable code.
