## STRIDE: Tampering

The situation falls under the Tampering category in the STRIDE threat modeling framework. In this case, the risk arises when a mobile application relies on client-controlled data or incorrectly implemented client-side controls for security-relevant decisions.

An attacker can install the mobile app and observe how it communicates with backend services or platform security components. By intercepting and modifying requests, or by abusing weaknesses in local security mechanisms, the attacker can alter values such as identifiers, roles, or feature-related parameters. If these values or results are trusted without proper validation, unauthorized actions or data manipulation can occur.

This issue commonly arises when security-relevant decisions rely on client-side controls that are implemented incorrectly or can be bypassed, for example due to misuse of platform security APIs, improper exception handling, or misconfiguration of hardware-backed keystores or keychains.

### What can go wrong?

If request data or authentication results can be modified or influenced without proper validation, attackers can tamper with application logic, bypass access controls, and manipulate sensitive data in ways not intended by the application design.

### What are we going to do about it?

Ensure that security-relevant decisions are enforced within the correct trust boundary. When authorization is handled by a backend service, every request must be validated based on the authenticated user and intended action. When authentication or validation is performed on the device, platform security mechanisms such as hardware-backed keystores or keychains must be implemented correctly and must not be relied upon incorrectly.

Avoid trusting client-controlled values such as roles, identifiers, or feature flags. Design APIs and authentication flows so that request tampering or misuse of platform security APIs does not grant unauthorized functionality. Use the OWASP Mobile Application Security Testing Guide (MASTG) to verify that authentication, authorization, and request-integrity controls are correctly implemented and tested.
