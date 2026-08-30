## Scenario: Abdullah can bypass authentication by altering the usual process sequence or flow, or by undertaking the process in incorrect order, or by manipulating date and time values used by the app, or by using valid features for unintended purposes

Consider Abdullah suspects his sibling Tim is secretly chatting late at night instead of studying. Determined to expose him to their parents, Abdullah attempts to access Tim’s chat app. Instead of using valid credentials, he bypasses authentication by manipulating the app’s logic and flow.

### Example
The app relies on client-side checks and assumes the authentication flow is followed correctly. Abdullah exploits this by modifying flags (e.g., `isLoggedIn = true`), triggering states out of sequence, manipulating time-based checks, and misusing valid features like deep links. Since there is no proper enforcement of authentication, he gains access to Tim’s chats.


## Threat Modeling

### STRIDE
This scenario falls under the **Tampering** and **Information Disclosure** categories of STRIDE. Abdullah performs Tampering by modifying the application's user interface to bypass authentication, leading to Information Disclosure.

### What can go wrong?
* Sensitive data may get disclosed.
* The user can lose access to services.
* The user's identity can be stolen.

### What are we going to do about it? 
* **Do not rely only on local authentication frameworks:** Always perform a secondary check on the server-side.
* **Enforce Android Confirmation:** Set `setConfirmationRequired` to `true` on Android to ensure user presence.
* **Secure Keychain Access:** Verify that access control flags are properly configured for keychain items (iOS) or Keystore (Android).
* **Configure Biometrics correctly:** Ensure biometric authentication is implemented according to the latest device documentation and security standards.