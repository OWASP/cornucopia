## Scenario: Eiman can bypass local authentication through patching and/or by instrumentation because the authentication can be patched out or overloaded

Consider a scenario where Eiman has obtained a jailbroken iOS device. She installs a Frida gadget in the target banking app, hooks the local authentication method, and replaces its return value with a success result. The app's authentication check is a simple function call `-> Bool`. The instrumented call returns `true`. The bank account is open. The biometric hardware was never consulted.

1. Local authentication implemented as a software flag or conditional branch is bypassable by patching the binary or injecting at runtime.
2. Hooking frameworks (Frida, Xposed, Substrate) allow method return values to be overridden at runtime on rooted/jailbroken devices.
3. A modified APK/IPA with the authentication check removed can be re-distributed and installed by an attacker who has physical access to the device or can perform MITM on the update channel.

### Example

Eiman downloads the target app's IPA, re-signs it with her own certificate, removes the biometric check with a binary patcher, and installs it on her jailbroken device. She then restores the app's user data from a backup. The app opens without any authentication. Every stored credential and session token is accessible. Eiman submits the finding as a bug report. The developer's initial response is "that requires a jailbroken device," which is technically true and strategically insufficient for a banking app.

## Threat Modeling

### STRIDE

This scenario falls under **Spoofing** and **Elevation of Privilege**.

Eiman bypasses identity verification, allowing her to act as the legitimate user. By patching the authentication logic, she elevates her effective privilege to that of an authenticated user without presenting valid credentials.

### What can go wrong?

- Authentication logic implemented purely in software is bypassable with widely available instrumentation tools.
- A patched app distributed to other users can bypass authentication for all of them.
- Credentials, tokens, and private data stored by the app are accessible once local authentication is bypassed.

### What are we going to do about it?

- Bind authentication to cryptographic operations backed by hardware-isolated key storage (Secure Enclave / StrongBox), so that bypassing the software check does not grant access to the cryptographic material needed to decrypt data.
- Implement runtime integrity checks that detect hooking frameworks (Frida, Xposed) and respond by terminating the session or refusing to load sensitive keys.
- Enforce re-authentication against a remote endpoint for high-value operations rather than relying solely on local checks.
- Apply obfuscation to authentication-related code paths as a defence-in-depth measure, increasing the cost of static patching.
