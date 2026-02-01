## STRIDE: Tampering

The situation falls under the Tampering category in the STRIDE threat modeling framework. In this case, the risk arises when a mobile application relies on client-controlled data for security-relevant decisions.

An attacker can install the mobile app and observe how it communicates with the backend service. By intercepting and modifying requests, the attacker may alter values such as identifiers, roles, or feature-related parameters sent by the app. If the backend assumes these values are trustworthy because they originate from the client, unauthorized actions or data manipulation may occur.

This issue commonly arises when security decisions are enforced on the device rather than being validated and authorized on the server.

### What could go wrong?

If requests can be modified without proper server-side validation and authorization, attackers can tamper with application logic, bypass access controls, and manipulate sensitive data in ways not intended by the application design.

### What are we going to do about it?

Ensure that all security-relevant decisions are enforced on the server and not delegated to the client. Every request must be validated and authorized based on the authenticated user and the action being performed, regardless of what parameters the mobile app sends.

Avoid trusting client-controlled values such as roles, identifiers, or feature flags. Design APIs so that request tampering does not allow access to unauthorized functionality. Use the OWASP Mobile Application Security Testing Guide (MASTG) to verify that authorization and request integrity controls are correctly implemented and tested.
