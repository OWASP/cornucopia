## Scenario: Ade can bypass authentication because it is not enforced using a remote endpoint, or it is not based on a cryptographic primitive protected by keystore/keychain access control flags

Consider a scenario where Ade installs a modified version of the target app on a rooted device. The app performs biometric authentication locally and stores a boolean `loggedIn = true` in `SharedPreferences`. There is no server-side session; the app directly accesses a local database. Ade modifies `SharedPreferences` using a root file manager, sets `loggedIn = true`, and opens the app. The database is decrypted with a key that is not bound to any authentication event. Ade accesses all stored user data. No network request was ever made. The server never knew Ade existed.

1. Authentication enforced only locally can be bypassed on rooted or jailbroken devices by modifying local state.
2. Cryptographic keys not bound to authentication events can be used by any process with the right storage access, bypassing the intent of the authentication gate.
3. Purely offline apps that do not validate session state with a server have no authoritative trust anchor.

### Example

Ade examines the app's APK and finds it stores the authentication state in `SharedPreferences` and uses a symmetric encryption key in the keystore that has `setUserAuthenticationRequired(false)`. On a rooted device, Ade modifies the `SharedPreferences` XML file to set the authentication flag to `true`. The app reads the flag, skips the biometric prompt, and decrypts the database — because the key was never protected by authentication requirements. The biometric prompt was a visual gate with no cryptographic fence behind it.

## Threat Modeling

### STRIDE

This scenario falls under **Spoofing** and **Elevation of Privilege**.

By bypassing local-only authentication, Ade gains the ability to act as a legitimately authenticated user, accessing data and functionality that should require verified identity.

### What can go wrong?

- Local state manipulation on rooted devices bypasses all local-only authentication checks.
- Unbound cryptographic keys are accessible to any process with storage access, making them equivalent to no encryption.
- Without server-side session validation, there is no way to revoke access remotely.

### What are we going to do about it?

- Enforce authentication using a remote endpoint for all operations involving sensitive data: the server must issue a short-lived session token only after verifying the authentication factor.
- Bind local cryptographic keys to user authentication events: `setUserAuthenticationRequired(true)` (Android) and Secure Enclave with biometric access control (iOS).
- Use the hardware-backed keystore (StrongBox on Android; Secure Enclave on iOS) for authentication-critical keys.
- Store session state server-side; the app holds only a short-lived token, not a long-lived `isLoggedIn` flag.
