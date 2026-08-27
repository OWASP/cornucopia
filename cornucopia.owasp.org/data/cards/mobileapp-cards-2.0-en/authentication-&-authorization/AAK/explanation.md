## Scenario: Aatif can influence or alter authentication controls and can therefore bypass them

### Example

Aatif helps install a smart doorbell whose welcome screen says “administrator” whenever a reply contains the word “yes.” He changes the installer’s response to “yes, absolutely, I love stairs,” and the doorbell grants a master control panel that can unlock the front gate.

Because the authentication result can be altered, the device treats a forged decision as proof. A mobile app that lets untrusted code influence its authentication control can likewise promote an ordinary user into a privileged one.


## Threat Modeling

### STRIDE

This scenario is primarily **Spoofing**, **Tampering** in STRIDE. The named condition is: Aatif can influence or alter authentication controls and can therefore bypass them.

The mapped threat is described by the card's application-specific condition.

No separate attack-vector text is assigned; derive the path from the mapped threat.

### What can go wrong?

If Aatif can influence or alter authentication controls and can therefore bypass them, the failure is concrete rather than merely theatrical: the app could let an attacker cross the authentication-&-authorization boundary and reach data or capability that this flow should protect. In this card, the practical route includes the invented path still needs a concrete, observable security impact. That can turn a normal user action into unauthorized access, disclosure, alteration, or service disruption; the mapped weakness entries below identify the exact implementation evidence to check.

Mapped weaknesses that sharpen the review:

- No MASWE entry is assigned to this card; this page keeps the attack explicitly invented.

### What are we going to do about it?

Make authentication checks and their configuration tamper-resistant: use platform-protected keys, verify server-issued challenges, reject altered state, and fail closed when a hook or modified verifier is detected; exercise both static references and runtime behavior.


Mapped MASTG tests:

- No MASTG test is assigned to this card; define a focused test for the invented attack.

Mapped MASTG best practices:

- No MASTG best practice is assigned; use the narrowest platform control that blocks the attack.

Mapped MASTG knowledge:

- MASTG-KNOW-0266 — References to APIs for Event-Bound Biometric Authentication: This test checks if the app insecurely accesses sensitive resources (e.g., tokens, keys) that should be protected by user authentication relying **solely** on the LocalAuthentication API for access control instead of using the Keychain API and requiring user presence.
- MASTG-KNOW-0267 — Runtime Use Of Event-Bound Biometric Authentication: This test is the dynamic counterpart to @MASTG-TEST-0266.
- MASTG-KNOW-0268 — References to APIs Allowing Fallback to Non-Biometric Authentication: This test checks if the app uses authentication mechanisms that rely on the user's passcode instead of biometrics or allow fallback to device passcode when biometric authentication fails. Specifically, it checks for use of [`SecAccessControlCreateWithFlags`](https://developer.apple.com/documentation/security/secaccesscontrolcreateflags) with the [`kSecAccessControlDevicePasscode`](https://developer.apple.com/documentation/security/secaccesscontrolcreateflags/devicepasscode) or [`kSecAccessControlUserPresence`](https://developer.apple.com/documentation/security/secaccesscontrolcreateflags/userpresence) flags.
- MASTG-KNOW-0269 — Runtime Use Of APIs Allowing Fallback to Non-Biometric Authentication: This test is the dynamic counterpart to @MASTG-TEST-0268.
- MASTG-KNOW-0270 — References to APIs Detecting Biometric Enrollment Changes: This test checks whether the app fails to protect sensitive operations against unauthorized access following biometric enrollment changes. An attacker who obtains the device passcode could add a new fingerprint or facial representation via system settings and use it to authenticate in the app.
- MASTG-KNOW-0271 — Runtime Use Of APIs Detecting Biometric Enrollment Changes: This test is the dynamic counterpart to @MASTG-TEST-0270.
- MASTG-KNOW-0326 — References to APIs Allowing Fallback to Non-Biometric Authentication: This test checks if the app uses biometric authentication mechanisms (@MASTG-KNOW-0001) that allow fallback to device credentials (PIN, pattern, or password) for sensitive operations.
- MASTG-KNOW-0327 — References to APIs for Event-Bound Biometric Authentication: This test checks if the app implements event-bound biometric authentication (@MASTG-KNOW-0001) to access sensitive resources (e.g., tokens, keys), where authentication success relies solely on a callback result rather than being cryptographically bound to sensitive operations and requiring user presence.
- MASTG-KNOW-0328 — References to APIs Detecting Biometric Enrollment Changes: This test checks whether the app fails to protect sensitive operations against unauthorized access following biometric enrollment changes (@MASTG-KNOW-0001). An attacker who obtains the device passcode could add a new fingerprint or facial representation via system settings and use it to authenticate in the app.
- MASTG-KNOW-0329 — References to APIs Enforcing Authentication without Explicit User Action: This test checks if the app enforces biometric authentication (@MASTG-KNOW-0001) [without requiring explicit user action](https://developer.android.com/identity/sign-in/biometric-auth#no-explicit-user-action). When using [`android.hardware.biometrics.BiometricPrompt`](https://developer.android.com/reference/android/hardware/biometrics/BiometricPrompt) API (or its Jetpack counterpart [`androidx.biometric.BiometricPrompt`](https://developer.android.com/reference/androidx/biometric/BiometricPrompt) that backward compatibility to API level 23), the [`setConfirmationRequired()`](https://developer.android.com/reference/android/hardware/biometrics/BiometricPrompt.Builder#setConfirmationRequired(boolean)) method in [`BiometricPrompt.Builder`](https://developer.android.com/reference/android/hardware/biometrics/BiometricPrompt.Builder) controls whether the user must explicitly confirm their authentication, which is enforced by default.
- MASTG-KNOW-0330 — References to APIs for Keys used in Biometric Authentication with Extended Validity Duration: This test checks if the app configures cryptographic keys with an extended validity duration that allows keys to remain unlocked beyond the immediate operation. When using biometric authentication with [`CryptoObject`](https://developer.android.com/reference/androidx/biometric/BiometricPrompt.CryptoObject), the authentication validity duration determines how long a key remains usable after successful authentication.
