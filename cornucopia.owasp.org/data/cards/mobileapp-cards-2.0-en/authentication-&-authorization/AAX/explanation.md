## Scenario: Lack of Remote Authentication Enforcement and Hardware-Backed Cryptographic Protection

### Example

Ade is about to check into a hotel using the official hotel room key app downloaded onto her personal smartphone. The app utilizes NFC to provision digital room keys. Normally, when issuing a key, the app connects to the hotel's host computer to authorize it through the booking service. However, the local Wi-Fi goes down, and the system enters an offline fallback mode.

Instead of denying the transaction, the offline path accepts locally stored "verified" session badges without validating them cryptographically. Ade intercepts this offline process; using a Flipper Zero, she copies the digital room key data for the presidential suite onto her Flipper Zero instead of letting it sync to the app, exploiting the fact that the transmitted cryptographic primitive lacks Keystore/Keychain access control flags. She completes this while the receptionist is still arguing with a customer over poor Wi-Fi access.

The offline path has no remote enforcement and no key operation bound to protected device authentication. An attacker who controls the device or its local state can therefore bypass the missing proof instead of being denied.

## Threat Modeling

### STRIDE

This scenario is primarily **Spoofing**, **Information Disclosure**, and **Elevation of Privilege** in STRIDE. Ade can bypass authentication because authorization states are evaluated locally without remote endpoint enforcement or are not based on a cryptographic primitive protected by hardware-backed Keystore/Keychain access control flags.


### What can go wrong?

Ade can bypass local authentication checks because they are implemented as event-bound software logic rather than being cryptographically tied to a protected resource. They can do so by debugging the app at runtime or using dynamic instrumentation. That can turn a normal user action into unauthorized access, disclosure, alteration, or service disruption.

Known threats include:

- **MAS-THREAT-0020:** Attackers can bypass local authentication and access protected data or functionality.
- **MAS-THREAT-0021:** Attackers can authenticate sensitive transactions without the user's biometrics.
- **MAS-THREAT-0022:** Attackers can use biometric-protected keys without the legitimate user's biometrics.

Possible attacks are:

- **MAS-ATTACK-0002:** Debugging the app at runtime.
- **MAS-ATTACK-0003:** Using dynamic instrumentation.
- **MAS-ATTACK-0027:** Invoking keystore operations on a compromised or stolen device when key use does not require user authentication.
- **MAS-ATTACK-0040:** Patching or repackaging the app to remove or alter client-side checks.
- **MAS-ATTACK-0034:** Using a known, guessed, or shoulder-surfed device credential (PIN, pattern, or password).
- **MAS-ATTACK-0035:** Enrolling additional biometrics on the device after obtaining the device credential.

This could be because:

- Local Authentication Can Be Bypassed: This weakness occurs when local authentication, such as biometrics, device credentials, or a custom app PIN, can be bypassed because it is implemented as an event-bound check rather than being cryptographically tied to a protected resource.
- Fallback to Non-biometric Credentials Allowed for Sensitive Transactions: This weakness occurs when authentication for a sensitive transaction can silently fall back from biometrics to a weaker device credential such as a PIN, pattern, or password.
- Crypto Keys Not Invalidated on New Biometric Enrollment: This weakness occurs when cryptographic keys gated by biometric authentication remain valid after the set of enrolled biometrics changes.

### What are we going to do about it?

Put the decisive authentication check on a remote endpoint and use a cryptographic key protected by Keystore or Keychain access controls; test debugging and instrumentation paths, reject local-only assertions, and fail closed when key use or server verification fails.

See the mapped MASTG tests for how to verify that the app is safe. Follow the mapped MASTG best practices during coding, and prepare yourself by reading through the mapped MASTG knowledge.