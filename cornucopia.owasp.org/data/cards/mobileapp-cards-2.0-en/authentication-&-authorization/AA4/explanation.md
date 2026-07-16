## Scenario: Vandana can bypass biometric authentication because the authentication is misconfigured or not implemented correctly

### Example

Vandana unlocks her mobile banking app using fingerprint authentication to quickly check her balance. The app treats this successful biometric check as valid for longer than it should and does not require re-authentication for sensitive actions.

Later, Vandana hands her phone to a colleague to show a photo. While swiping around, the colleague accidentally switches back to the banking app — which is still unlocked. Without any additional biometric prompt, it is possible to view account details and initiate actions that should have required Vandana’s fingerprint again.

What started as a quick balance check turns into an awkward conversation and a reminder that biometric authentication must be handled carefully.

## Threat Modeling

### STRIDE

The situation falls under the **Tampering** category in the STRIDE threat modeling framework. In this case, the risk arises when a mobile application relies on incorrectly implemented client-side controls for security-relevant decisions.

An attacker can install the mobile app and observe how it interacts with platform security components such as the keystore or keychain. By abusing weaknesses in local authentication logic — such as misuse of `CryptoObject`, improper exception handling, or misconfiguration of hardware-backed keystores or keychains — the attacker can influence authentication results. If these results are trusted without proper validation, unauthorized actions or data manipulation can occur.

This issue commonly arises when security-relevant decisions are enforced on the device using client-side controls that are implemented incorrectly or can be bypassed.

### What can go wrong?

If biometric authentication or local validation logic can be bypassed or manipulated, attackers can tamper with application logic, bypass access controls, and perform actions that should only be allowed after successful user authentication.

### What are we going to do about it?

Ensure that biometric authentication is implemented correctly and securely. Platform security features such as hardware-backed keystores or keychains must be used as intended, including correct use of `CryptoObject` and proper exception handling.

Biometric authentication must not be relied upon incorrectly for protecting sensitive actions. Use the OWASP Mobile Application Security Testing Guide (MASTG) to verify that biometric authentication, keystore usage, and related security controls are correctly implemented and tested.
