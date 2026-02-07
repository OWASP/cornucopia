## Scenario: Eiman bypasses local authentication using instrumentation tools

Consider Eiman, who is slightly impatient and thinks 4-digit PIN codes are a relic of the past. Why type 1-2-3-4 when you can just delete the code that asks for it? Eiman knows that the mobile app runs on his device, which means he controls the "physics" of that universe. If the app asks "Is the user authenticated?", Eiman can simply use tools to force the answer to be "Yes" without ever knowing the password.

### Example

Eiman downloads the popular "MySecretDiary" app to snoop on his sibling's secrets. The app is protected by a PIN screen. Instead of guessing the PIN, Eiman connects his phone to his computer and uses a dynamic instrumentation tool (like Frida). He identifies the function `checkPinAndUnlock()` in the app's code. He writes a tiny script that hooks into this function and forces it to always return `true`, regardless of what PIN is entered (or if one is entered at all). The app, trusting its own modified logic, unlocking the diary and revealing the secrets. Eiman didn't crack the password; he just convinced the app that he did.

## Threat Modeling

### STRIDE

This scenario falls under the **Tampering** category of STRIDE.

By modifying the application's runtime behavior or binary code (Tampering), Eiman bypasses the security controls, effectively leading to **Elevation of Privilege** and **Spoofing** (acting as the authenticated user).

### What can go wrong?

**Client-Side Bypass:** If authentication logic runs entirely on the client-side (the phone) without server-side validation, an attacker can modify the app to skip these checks.

**Feature Unlock:** Attackers might patch the app to unlock "Pro" features without paying.

**Data Access:** If the app relies solely on a UI screen to block access to data (and doesn't encrypt the data with a key derived from the user's PIN/password), bypassing the UI exposes the data immediately.

### What are we going to do about it?

**Server-Side Validation:** Distinct sensitive operations should require a fresh session token or validation from the server, not just a "flag" in the app.

**Root/Jailbreak Detection:** Implement checks to detect if the device environment is compromised or if tools like Frida are running (though these can also be bypassed, they raise the bar).

**Code Obfuscation:** Use obfuscation to make it harder for Eiman to find the critical specific checks like `checkPinAndUnlock()` function in the first place.

**Cryptography:** Ensure data is encrypted at rest using a key derived from the user's credential. If Eiman patches the auth check, he still won't have the key to decrypt the data.