## Scenario: Ade can bypass authentication because it is not enforced using a remote endpoint, or it is not based on a cryptographic primitive protected by keystore/keychain access control flags.

### Example

Ade checks into a hostel using a tablet that normally phones the remote booking service, but the Wi-Fi disappears. The tablet accepts a locally stored “verified” badge anyway, so Ade can print a room key while the receptionist is still arguing with a vending machine.

The offline path has no remote enforcement and no key operation bound to protected device authentication. An attacker who controls the device or its local state can therefore bypass the missing proof instead of being denied.


## Threat Modeling

### STRIDE

This scenario is primarily **Spoofing**, **Information Disclosure**, **Elevation of Privilege** in STRIDE. The named condition is: Ade can bypass authentication because it is not enforced using a remote endpoint, or it is not based on a cryptographic primitive protected by keystore/keychain access control flags.

- **MAS-THREAT-0020:** Attackers can bypass local authentication and access protected data or functionality.
- **MAS-THREAT-0021:** Attackers can authenticate sensitive transactions without the user's biometrics.
- **MAS-THREAT-0022:** Attackers can use biometric-protected keys without the legitimate user's biometrics.

- **MAS-ATTACK-0002:** Debugging the app at runtime.
- **MAS-ATTACK-0003:** Using dynamic instrumentation.
- **MAS-ATTACK-0027:** Invoking keystore operations on a compromised or stolen device when key use does not require user authentication.
- **MAS-ATTACK-0040:** Patching or repackaging the app to remove or alter client-side checks.
- **MAS-ATTACK-0034:** Using a known, guessed, or shoulder-surfed device credential (PIN, pattern, or password).
- **MAS-ATTACK-0035:** Enrolling additional biometrics on the device after obtaining the device credential.

### What can go wrong?

If Ade can bypass authentication because it is not enforced using a remote endpoint, or it is not based on a cryptographic primitive protected by keystore/keychain access control flags., the failure is concrete rather than merely theatrical: the app could let an attacker cross the authentication-&-authorization boundary and reach data or capability that this flow should protect. In this card, the practical route includes Debugging the app at runtime. Also, Using dynamic instrumentation. That can turn a normal user action into unauthorized access, disclosure, alteration, or service disruption; the mapped weakness entries below identify the exact implementation evidence to check.

Mapped weaknesses that sharpen the review:

- MASWE-0020 — Local Authentication Can Be Bypassed: This weakness occurs when local authentication, such as biometrics, device credentials, or a custom app PIN, can be bypassed because it is implemented as an event-bound check rather than being cryptographically tied to a protected resource.
- MASWE-0021 — Fallback to Non-biometric Credentials Allowed for Sensitive Transactions: This weakness occurs when authentication for a sensitive transaction can silently fall back from biometrics to a weaker device credential such as a PIN, pattern, or password.
- MASWE-0022 — Crypto Keys Not Invalidated on New Biometric Enrollment: This weakness occurs when cryptographic keys gated by biometric authentication remain valid after the set of enrolled biometrics changes.

### What are we going to do about it?

Put the decisive authentication check on a remote endpoint and use a cryptographic key protected by Keystore or Keychain access controls; test debugger and instrumentation paths, reject local-only assertions, and fail closed when key use or server verification fails.


Mapped MASTG tests:

- MASTG-TEST-0266 — References to APIs for Event-Bound Biometric Authentication: This test checks if the app insecurely accesses sensitive resources (e.g., tokens, keys) that should be protected by user authentication relying **solely** on the LocalAuthentication API for access control instead of using the Keychain...
- MASTG-TEST-0267 — Runtime Use Of Event-Bound Biometric Authentication: This test is the dynamic counterpart to @MASTG-TEST-0266.
- MASTG-TEST-0268 — References to APIs Allowing Fallback to Non-Biometric Authentication: This test checks if the app uses authentication mechanisms that rely on the user's passcode instead of biometrics or allow fallback to device passcode when biometric authentication fails. Specifically, it checks for use of...
- MASTG-TEST-0269 — Runtime Use Of APIs Allowing Fallback to Non-Biometric Authentication: This test is the dynamic counterpart to @MASTG-TEST-0268.
- MASTG-TEST-0270 — References to APIs Detecting Biometric Enrollment Changes: This test checks whether the app fails to protect sensitive operations against unauthorized access following biometric enrollment changes. An attacker who obtains the device passcode could add a new fingerprint or facial representation...
- MASTG-TEST-0271 — Runtime Use Of APIs Detecting Biometric Enrollment Changes: This test is the dynamic counterpart to @MASTG-TEST-0270.
- MASTG-TEST-0326 — References to APIs Allowing Fallback to Non-Biometric Authentication: This test checks if the app uses biometric authentication mechanisms (@MASTG-KNOW-0001) that allow fallback to device credentials (PIN, pattern, or password) for sensitive operations.
- MASTG-TEST-0327 — References to APIs for Event-Bound Biometric Authentication: This test checks if the app implements event-bound biometric authentication (@MASTG-KNOW-0001) to access sensitive resources (e.g., tokens, keys), where authentication success relies solely on a callback result rather than being...
- MASTG-TEST-0328 — References to APIs Detecting Biometric Enrollment Changes: This test checks whether the app fails to protect sensitive operations against unauthorized access following biometric enrollment changes (@MASTG-KNOW-0001). An attacker who obtains the device passcode could add a new fingerprint or...
- MASTG-TEST-0329 — References to APIs Enforcing Authentication without Explicit User Action: This test checks if the app enforces biometric authentication (@MASTG-KNOW-0001) without requiring explicit user action. When using `android.hardware.biometrics.BiometricPrompt` API (or its Jetpack counterpart...
- MASTG-TEST-0330 — References to APIs for Keys used in Biometric Authentication with Extended Validity Duration: This test checks if the app configures cryptographic keys with an extended validity duration that allows keys to remain unlocked beyond the immediate operation. When using biometric authentication with `CryptoObject`, the authentication...

Mapped MASTG best practices:

- MASTG-BEST-0031 — Enforce Strong Biometrics for Sensitive Operations: For sensitive operations protected by Android biometrics, configure `BiometricPrompt` to require `BIOMETRIC_STRONG` rather than allowing weaker biometric classes. Android defines `BIOMETRIC_STRONG` as authentication using a Class 3...
- MASTG-BEST-0036 — Use Cryptographic Binding for Biometric Authentication: For sensitive operations protected by biometric authentication, use `BiometricPrompt.authenticate()`) with a `CryptoObject` backed by an Android Keystore key configured with `setUserAuthenticationRequired(true)`. This cryptographically...
- MASTG-BEST-0037 — Invalidate Biometric Keys on Enrollment Changes: When generating cryptographic keys for biometric authentication, ensure keys are invalidated when new biometrics are enrolled. Either configure `setInvalidatedByBiometricEnrollment(true)`) explicitly, or rely on the default behavior,...
- MASTG-BEST-0038 — Require Explicit User Confirmation for Biometric Authentication: For sensitive operations requiring explicit user authorization (e.g., payments or access to health data), configure `setConfirmationRequired(true)`) in `BiometricPrompt.Builder`, or rely on the default behavior, which requires confirmation.

Mapped MASTG knowledge:

- MASTG-KNOW-0056 — Local Authentication Framework: The Local Authentication framework provides facilities for requesting a passphrase or Touch ID authentication from users. Developers can display and utilize an authentication prompt by utilizing the function `evaluatePolicy` of the...
- MASTG-KNOW-0057 — Keychain Services: The iOS keychain APIs can (and should) be used to implement local authentication. During this process, the app stores either a secret authentication token or another piece of secret data identifying the user in the keychain. In order to...
- MASTG-KNOW-0001 — Biometric Authentication: Android provides platform support for biometric authentication, such as fingerprint and face recognition, and exposes it to apps through the biometric APIs. At the framework level, Android includes support for face and fingerprint...
- MASTG-KNOW-0043 — Android KeyStore: The Android KeyStore provides relatively secure credential storage. As of Android 4.3 (API level 18), it provides public APIs for storing and using app-private keys. An app can use a public key to generate a new private/public key pair...
- MASTG-KNOW-0047 — Cryptographic Key Storage: To mitigate unauthorized use of keys on the Android device, Android KeyStore lets apps specify authorized uses of their keys when generating or importing the keys. Once made, authorizations cannot be changed.
- MASTG-KNOW-0012 — Key Generation: The Android SDK allows you to specify how a key should be generated, and under which circumstances it can be used. Android 6.0 (API level 23) introduced the `KeyGenParameterSpec` class that can be used to ensure the correct key usage in...
