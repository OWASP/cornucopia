## Scenario: Eiman bypasses local authentication using instrumentation tools

Consider Eiman, who is a slightly controlling brother who likes to know what his sister is up to. He knows the best secrets are those he can retrieve without her being aware. What better way is there than hacking her phone by bypassing local authentication using instrumentation tools?

### Example

Eiman's sister uses the popular "MySecretDiary" app on her phone. The app is protected by a PIN screen. One day, his sister leaves her phone unlocked on the table. To snoop on his sister's secrets, instead of guessing the PIN, Eiman connects her phone to his computer and uses a dynamic instrumentation tool. He identifies the function `checkPinAndUnlock()` in the app's code. He writes a tiny script that hooks into this function and forces it to always return `true`, regardless of which PIN is entered (or whether one is entered at all). The app, trusting its own modified logic, unlocks the diary and reveals the secrets. Eiman did not steal his sister's PIN; he just convinced the app that he was his sister.

## Threat Modeling

### STRIDE

This scenario falls under the **Spoofing** and **Tampering** categories of STRIDE.
By modifying the application's runtime behavior or binary code (Tampering), Eiman bypasses the security controls, effectively leading to **Spoofing** and **Information Disclosure** (acting as his sister and reading her secret diary).

### What can go wrong?

**Client-Side Bypass:** If authentication logic runs entirely on the client side (the phone) without server-side validation, an attacker can modify the app to skip these checks.

**Feature Unlock:** Attackers might patch the app to unlock features they are not meant to unlock.

**Data Access:** If the app relies solely on a UI screen to block access to data and does not encrypt the data with a key derived from the user's PIN/password, bypassing the UI exposes the data immediately.

### What are we going to do about it?

**Server-Side Validation:** Each sensitive operation should require a fresh session token or validation from the server, not just a "flag" in the app.

**Root/Jailbreak Detection:** Implement checks to detect if the device environment is compromised or if tools like Frida are running (though these can also be bypassed, they raise the bar).

**Code Obfuscation:** Use obfuscation to make it harder for Eiman to find critical checks, such as the `checkPinAndUnlock()` function, in the first place.

**Cryptography:** Ensure data is encrypted at rest using a key derived from the user's credential. If Eiman patches the auth check, he still won't have the key to decrypt the data.

See the mapped MASTG tests for how to verify that the app is safe. Follow the mapped MASTG best practices during coding, and prepare yourself by reading through the mapped MASTG knowledge.
