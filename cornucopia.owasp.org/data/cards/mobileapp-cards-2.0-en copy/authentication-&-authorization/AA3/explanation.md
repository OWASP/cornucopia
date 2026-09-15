## Scenario: Vandana can access sensitive features due to improperly bound or misconfigured biometric authentication controls, insecure fallbacks, or unhandled configuration changes

### Example

Henrietta likes to ask her colleagues for advice. There is one colleague in particular whom she trusts intimately: Vandana. Vandana recommends that Henrietta install a photo app her boyfriend has vibe-coded that allows her to look younger and more attractive in pictures taken by her phone without making the changes look obvious. Vandana borrows Henrietta's phone to install it. On the same phone, Henrietta also has her bank app, which blindly trusts the phone's biometric success callback without verifying a hardware-backed cryptographic key. Vandana is therefore able to add her own fingerprint to Henrietta's phone settings and use it to open the bank app without invalidating the app's internal session.
One of the apps to which this applies happens to belong to her local bank. Not long after, Vandana leaves for a sabbatical with her boyfriend while Henrietta is left figuring out why she has suddenly accumulated a large amount of credit card debt.

## Threat Modeling

### STRIDE

The situation falls under the **Tampering** and **Information Disclosure** categories in the STRIDE threat modeling framework. In this case, the risk arises when a mobile application relies on incorrectly implemented client-side controls for security-relevant decisions.
The banking app on Henrietta's phone does not securely interact with platform security components such as the keystore or keychain. By abusing weaknesses in biometric authentication logic (due to improperly bound or misconfigured biometric authentication controls, insecure fallbacks, or unhandled configuration changes), her colleague can influence authentication results. If these results are trusted without proper validation, unauthorized actions or data manipulation can occur.

This issue commonly arises when security-relevant decisions are enforced on the device using client-side controls that are implemented incorrectly or can be bypassed.

### What can go wrong?

If biometric authentication or local validation logic can be bypassed or manipulated, attackers can tamper with application logic, bypass access controls, and perform actions that should only be allowed after successful user authentication.

### What are we going to do about it?

Ensure that biometric authentication is implemented correctly and securely. Platform security features such as hardware-backed keystores or keychains must be used as intended, including correct use of `CryptoObject` and proper exception handling.

Biometric authentication must not be relied upon incorrectly for protecting sensitive actions. Use the OWASP Mobile Application Security Testing Guide (MASTG) to verify that biometric authentication, keystore usage, and related security controls are correctly implemented and tested.

See the mapped MASTG tests for how to verify that the app is safe. Follow the mapped MASTG best practices during coding, and prepare yourself by reading through the mapped MASTG knowledge.