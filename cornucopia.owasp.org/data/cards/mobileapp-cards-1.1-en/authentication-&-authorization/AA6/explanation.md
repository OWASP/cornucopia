## Scenario: Anant can perform sensitive operations without additional authentication because authentication requirements are too weak or missing

Anant wants to see his saved "Ultra Secret" note in the app. The app asks for a PIN to "unlock" the note view. Anant bypasses the UI check using instrumentation. Because the note was encrypted with a hardcoded key (or no key bound to the biometric), he successfully views the note without providing the PIN.

### Example

Anant opens his "Vault" app. He navigates to the "View Secret" page. The app prompts for a fingerprint. Anant uses a script to hook the `onAuthenticationSucceeded` callback or the boolean check `isUnlocked`, forcing it to true. The app, which merely hid the text field behind a view overlap, now reveals the secret text. If the app had used the Android Keystore to encrypt the note, Anant's bypass would have failed because the decryption key would never have been released by the OS.

## Threat Modeling

### STRIDE

This scenario falls under the **Tampering** and **Information Disclosure** categories of STRIDE.

Anant performs **Tampering** by modifying the application's runtime logic to bypass the check, leading to **Information Disclosure** of the sensitive note.

### What can go wrong?

**Logic-Only Gates:** Relying on simple boolean flags (e.g., `if (isUnlocked)`) allows attackers to flip the flag and bypass the check.

**Insecure Storage:** If data is stored in plain text or encrypted with a static key, bypassing the authentication screen grants immediate access to the data.

### What are we going to do about it?

**Android Keystore / iOS Keychain:** Use cryptographic keys that mandate user authentication (e.g., `setUserAuthenticationRequired(true)`).

**Crypto-Binding:** Ensure the sensitive data can only be decrypted using the key that is released *only* after a successful biometric or PIN verification.


https://mas.owasp.org/MASTG/tests/ios/MASVS-AUTH/MASTG-TEST-0064/#static-analysis