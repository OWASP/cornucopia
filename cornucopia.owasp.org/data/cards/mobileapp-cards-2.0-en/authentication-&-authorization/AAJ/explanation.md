## Scenario: Prasad can bypass the centralized authentication and authorization controls since they are not being used comprehensively on all interactions

### Example

Prasad runs a charity book sale where the tablet asks for a volunteer PIN at the front door, then leaves the cash-drawer button exposed on every later screen. He taps through the catalog, opens the drawer, and discovers that the “honor system” comes with a surprisingly generous refund menu.

The check is centralized in appearance but missing from individual interactions. An app with the same gap lets a caller reach protected operations after passing one superficial checkpoint, so authentication and authorization must cover every relevant path.


## Threat Modeling

### STRIDE

This scenario is primarily **Spoofing**, **Information Disclosure**, **Elevation of Privilege** in STRIDE. The named condition is: Prasad can bypass the centralized authentication and authorization controls since they are not being used comprehensively on all interactions.

- **MAS-THREAT-0020:** Attackers can bypass local authentication and access protected data or functionality.
- **MAS-THREAT-0021:** Attackers can authenticate sensitive transactions without the user's biometrics.
- **MAS-THREAT-0022:** Attackers can use biometric-protected keys without the legitimate user's biometrics.
- **MAS-THREAT-0018:** Attackers can access sensitive data and functionality exposed by app components.

- **MAS-ATTACK-0002:** Debugging the app at runtime.
- **MAS-ATTACK-0003:** Using dynamic instrumentation.
- **MAS-ATTACK-0027:** Invoking keystore operations on a compromised or stolen device when key use does not require user authentication.
- **MAS-ATTACK-0040:** Patching or repackaging the app to remove or alter client-side checks.
- **MAS-ATTACK-0034:** Using a known, guessed, or shoulder-surfed device credential (PIN, pattern, or password).
- **MAS-ATTACK-0035:** Enrolling additional biometrics on the device after obtaining the device credential.
- **MAS-ATTACK-0038:** Invoking exported or unprotected app components from another app installed on the device.
- **MAS-ATTACK-0039:** Connecting to open ports or local services exposed by the app.

### What can go wrong?

If Prasad can bypass the centralized authentication and authorization controls since they are not being used comprehensively on all interactions, the failure is concrete rather than merely theatrical: the app could let an attacker cross the authentication-&-authorization boundary and reach data or capability that this flow should protect. In this card, the practical route includes Debugging the app at runtime. Also, Using dynamic instrumentation. That can turn a normal user action into unauthorized access, disclosure, alteration, or service disruption; the mapped weakness entries below identify the exact implementation evidence to check.

Mapped weaknesses that sharpen the review:

- MASWE-0020 — Local Authentication Can Be Bypassed: This weakness occurs when local authentication, such as biometrics, device credentials, or a custom app PIN, can be bypassed because it is implemented as an event-bound check rather than being cryptographically tied to a protected resource.
- MASWE-0021 — Fallback to Non-biometric Credentials Allowed for Sensitive Transactions: This weakness occurs when authentication for a sensitive transaction can silently fall back from biometrics to a weaker device credential such as a PIN, pattern, or password.
- MASWE-0022 — Crypto Keys Not Invalidated on New Biometric Enrollment: This weakness occurs when cryptographic keys gated by biometric authentication remain valid after the set of enrolled biometrics changes.
- MASWE-0018 — Lack of Authentication or Authorization on App Components: This weakness occurs when app components that expose functionality or data do not enforce proper authentication or authorization on their callers.

### What are we going to do about it?

Enforce authentication and authorization at every entry point, not just the main screen: test the release build while debugging and instrumenting it, protect IPC with narrow permissions, and have the server re-check identity and each sensitive action.


Mapped MASTG tests:

- MASTG-TEST-0266 — References to APIs for Event-Bound Biometric Authentication: This test checks if the app insecurely accesses sensitive resources (e.g., tokens, keys) that should be protected by user authentication relying **solely** on the LocalAuthentication API for access control instead of using the Keychain...
- MASTG-TEST-0267 — Runtime Use Of Event-Bound Biometric Authentication: This test is the dynamic counterpart to @MASTG-TEST-0266.
- MASTG-TEST-0268 — References to APIs Allowing Fallback to Non-Biometric Authentication: This test checks if the app uses authentication mechanisms that rely on the user's passcode instead of biometrics or allow fallback to device passcode when biometric authentication fails. Specifically, it checks for use of...
- MASTG-TEST-0269 — Runtime Use Of APIs Allowing Fallback to Non-Biometric Authentication: This test is the dynamic counterpart to @MASTG-TEST-0268.
- MASTG-TEST-0270 — References to APIs Detecting Biometric Enrollment Changes: This test checks whether the app fails to protect sensitive operations against unauthorized access following biometric enrollment changes. An attacker who obtains the device passcode could add a new fingerprint or facial representation...
- MASTG-TEST-0271 — Runtime Use Of APIs Detecting Biometric Enrollment Changes: This test is the dynamic counterpart to @MASTG-TEST-0270.
- MASTG-TEST-0327 — References to APIs for Event-Bound Biometric Authentication: This test checks if the app implements event-bound biometric authentication (@MASTG-KNOW-0001) to access sensitive resources (e.g., tokens, keys), where authentication success relies solely on a callback result rather than being...
- MASTG-TEST-0330 — References to APIs for Keys used in Biometric Authentication with Extended Validity Duration: This test checks if the app configures cryptographic keys with an extended validity duration that allows keys to remain unlocked beyond the immediate operation. When using biometric authentication with `CryptoObject`, the authentication...
- MASTG-TEST-0364 — Exported And Unprotected Activities That Expose Sensitive Functionality: If an exported activity does not define `android:permission` with a proper protection level and performs or grants access to sensitive functionality, another third-party app outside the intended trust boundary can start it with an...
- MASTG-TEST-0365 — Exported And Unprotected Services That Expose Sensitive Functionality: If an exported service does not define `android:permission` with a proper protection level and performs or grants access to sensitive functionality, another third-party app outside the intended trust boundary can start or bind to it and...
- MASTG-TEST-0366 — Exported And Unprotected Broadcast Receivers That Expose Sensitive Functionality: If an exported receiver does not define `android:permission` with a proper protection level and performs or grants access to sensitive functionality, another third-party app outside the intended trust boundary can send a broadcast to it...

Mapped MASTG best practices:

- MASTG-BEST-0036 — Use Cryptographic Binding for Biometric Authentication: For sensitive operations protected by biometric authentication, use `BiometricPrompt.authenticate()`) with a `CryptoObject` backed by an Android Keystore key configured with `setUserAuthenticationRequired(true)`. This cryptographically...
- MASTG-BEST-0052 — Restrict Access to Android App Components: Only export an app component when another app genuinely needs to interact with it. Every exported component is an entry point that other apps on the device may be able to invoke, so keeping components private by default reduces the...

Mapped MASTG knowledge:

- MASTG-KNOW-0056 — Local Authentication Framework: The Local Authentication framework provides facilities for requesting a passphrase or Touch ID authentication from users. Developers can display and utilize an authentication prompt by utilizing the function `evaluatePolicy` of the...
- MASTG-KNOW-0057 — Keychain Services: The iOS keychain APIs can (and should) be used to implement local authentication. During this process, the app stores either a secret authentication token or another piece of secret data identifying the user in the keychain. In order to...
- MASTG-KNOW-0001 — Biometric Authentication: Android provides platform support for biometric authentication, such as fingerprint and face recognition, and exposes it to apps through the biometric APIs. At the framework level, Android includes support for face and fingerprint...
- MASTG-KNOW-0043 — Android KeyStore: The Android KeyStore provides relatively secure credential storage. As of Android 4.3 (API level 18), it provides public APIs for storing and using app-private keys. An app can use a public key to generate a new private/public key pair...
- MASTG-KNOW-0047 — Cryptographic Key Storage: To mitigate unauthorized use of keys on the Android device, Android KeyStore lets apps specify authorized uses of their keys when generating or importing the keys. Once made, authorizations cannot be changed.
- MASTG-KNOW-0012 — Key Generation: The Android SDK allows you to specify how a key should be generated, and under which circumstances it can be used. Android 6.0 (API level 23) introduced the `KeyGenParameterSpec` class that can be used to ensure the correct key usage in...
- MASTG-KNOW-0132 — Android Activities: An activity is an app component that provides a single screen with a user interface. An app typically implements one activity per screen, so an app with three screens implements three activities. Each activity extends the `Activity`...
- MASTG-KNOW-0017 — App Permissions: Android assigns a distinct system identity (Linux user ID and group ID) to every installed app. Because each Android app operates in a process sandbox, apps must explicitly request access to resources and data that are outside their...
- MASTG-KNOW-0020 — Inter-Process Communication (IPC) Mechanisms: Every Android process runs in its own sandboxed address space. Inter-process communication (IPC) lets apps and the system exchange data and invoke functionality across these process boundaries. Instead of relying on traditional...
- MASTG-KNOW-0133 — Android Services: A service is an app component that performs long-running operations in the background without a user interface, such as processing data, performing network transactions, or interacting with content providers. A service extends the...
- MASTG-KNOW-0134 — Android Broadcast Receivers: A broadcast receiver is an app component that responds to broadcast messages from other apps or from the system. Apps use broadcasts as a publish-subscribe messaging mechanism: the system delivers broadcasts for events such as boot...
