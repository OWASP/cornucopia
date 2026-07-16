## Scenario: Fady can bypass cryptographic controls because they do not fail securely — they default to unprotected mode

Consider a scenario where Fady discovers the target app has an encryption module that, when it encounters an exception from the `KeyStore` (key not found, hardware error), catches the exception and returns the original plaintext data unmodified. The developer's intention was "graceful degradation." The result is that any condition causing a `KeyStore` failure — including a condition Fady can induce — results in sensitive data being returned in plaintext. The encryption fails open.

1. Catching cryptographic exceptions and continuing without encryption defaults to unprotected behaviour.
2. A `try { decrypt() } catch (Exception e) { return data; }` pattern is a classic fail-open cryptographic implementation.
3. Unavailability of the hardware security module resulting in plaintext fallback defeats hardware-backed security.

### Example

Fady triggers a `KeyStoreException` by deleting the app's `KeyStore` key entry using a root file manager. The app's encryption module catches the exception and returns the data unmodified (plaintext). Fady now has direct access to all data the app had "encrypted." The developer's fallback intent was "continue operating even if encryption fails." The secure intent would have been "fail closed: refuse to operate if encryption fails."

## Threat Modeling

### STRIDE

This scenario falls under **Information Disclosure** and **Spoofing**.

A fail-open cryptographic control means that any condition — hardware error, key deletion, induced exception — that causes the cryptographic operation to fail results in the protected data becoming accessible in plaintext.

### What can go wrong?

- Inducing a key error causes the app to return plaintext data instead of failing.
- Hardware errors in the secure element result in plaintext fallback, bypassing hardware-backed security.
- Exception handling logic that catches all exceptions and continues causes cryptographic operations to silently fail.

### What are we going to do about it?

- Cryptographic controls must fail closed: if the decrypt operation fails, the data must not be returned in any form.
- Propagate cryptographic exceptions to the caller; do not catch and swallow them.
- If the cryptographic key is unavailable, display an error and require re-authentication or re-setup; do not fall back to plaintext.
- Test fail-closed behaviour explicitly: delete the key and verify the app refuses to return the data.
